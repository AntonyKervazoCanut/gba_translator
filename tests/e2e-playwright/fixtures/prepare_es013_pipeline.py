"""ES-013 : vrai CSV/JSON/builder, sentinelles privées et écritures bornées."""
import hashlib
import json
import sys
import tempfile
from dataclasses import replace
from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts import build_language as driver
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_aliases import TextAliases
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

VISIBLE = '¡PRUEBA ES 013!\nNiño y pingüino\nPrimera prueba\nSegunda prueba\n¿ÚLTIMA LÍNEA?'


def main() -> None:
    """Exerce les mécanismes de production sans modifier un combined de production."""
    source = driver.ENGLISH_ROM.read_bytes()
    config = driver.load_registry().get('es-maint')
    routes = SystemTextRoutes.load(ROOT / config.system_texts, source)
    aliases = TextAliases.load(ROOT / config.text_aliases, source)
    preparation = json.loads((ROOT / 'docs/analysis/es/013_PREPARATION.json').read_text())
    keys = {int(e['offset'], 16) for e in preparation['entries']}
    assert hashlib.sha256(source).hexdigest() == preparation['source_sha256']
    spanish = driver.SPANISH_ROM.read_bytes()
    assert hashlib.sha256(spanish).hexdigest() == preparation['es_sha256']
    mapping = json.loads(driver.OFFSET_MAP.read_text())['offset_map']
    selected = {k: e for k, e in routes.entries.items() if k in keys}
    selected_aliases = {k: e for k, e in aliases.entries.items() if k in keys}
    for record in preparation['entries']:
        key = int(record['offset'], 16)
        if key not in selected and key not in selected_aliases:
            continue
        matches = record['correspondances_es']
        assert len(matches) == 1, f'{key:X}: correspondance ES ambiguë ou absente'
        match = matches[0]
        live = selected_aliases[key]['live_offset'] if key in selected_aliases else key
        assert [e for e in mapping if e['english_offset'] == live] == [match['mapping']]
        if match['mapping']['status'] == 'only_in_english':
            assert match['mapping']['spanish_offset'] is None
        else:
            assert match['mapping']['status'] == 'matched'
            offset = match['mapping']['spanish_offset']
            raw = bytes.fromhex(match['preimage_hex'])
            assert spanish[offset:offset+len(raw)] == raw
    builder = import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    translations = {}
    for key, entry in {**selected, **selected_aliases}.items():
        raw = bytes.fromhex(entry.get('source_hex', entry.get('english_raw_hex', '')))
        commands = builder._extract_control_sequences_from_raw(raw, include_breaks=True)
        if commands:
            translations[key] = f'{key:X}i' + ''.join(''.join(f'<0x{b:02X}>' for b in cmd)+'i' for cmd in commands)
        elif key >= 0x482874:
            translations[key] = '\n'.join([f'{key:X}'+'i'*20]+['i'*28]*4)
        else:
            translations[key] = f'{key:X}i'
    translations[0x482874] = VISIBLE
    with tempfile.TemporaryDirectory(prefix='f1044-pipeline-') as directory:
        temporary = Path(directory)
        combined = temporary / 'combined.txt'
        combined.write_text(''.join(f'0x{k:08X}: '+v.replace('\n', r'\n')+'\n' for k,v in translations.items()))
        probe = replace(config, code='es013-probe', combined=str(combined), output_rom='GenedRom-f1044-sentinel.gba')
        ready = driver.generate_translation_json(probe)
        payload = json.loads(ready.read_text())
        assert {i.get('contract_offset', i['offset']) for i in payload['translations']} == translations.keys()
        rom = driver.build_rom(probe, ready)
        result = rom.read_bytes()
        routes.verify(result, ready, translations)
        aliases.verify(result, ready, translations)
        expected = bytearray(source)
        allowed = []
        records = []
        for item in payload['translations']:
            key = item.get('contract_offset', item['offset'])
            raw = TextEncoder.encode_pokemon(translations[key], skip_aliases=SPANISH_GLYPH_CHARS)
            entry = selected.get(key, selected_aliases.get(key))
            refs = entry['pointer_offsets']
            for ref in refs:
                target = int.from_bytes(result[ref:ref+4], 'little')-0x08000000
                assert result[target:target+len(raw)] == raw
                expected[ref:ref+4] = result[ref:ref+4]
                expected[target:target+len(raw)] = raw
                allowed.extend([(ref,ref+4),(target,target+len(raw))])
            records.append({'key':key, 'pointers':refs, 'expected_hex':raw.hex(), 'target':target, 'layout':entry.get('layout')})
        assert result == expected, 'Écriture builder hors des allocations/pointeurs autorisés'
        driver.apply_patches(replace(probe, code='es-maint'), rom, ready, build_number=0)
        result = rom.read_bytes()
        routes.verify(result, ready, translations)
        aliases.verify(result, ready, translations)
        baseline = temporary / 'baseline.gba'
        baseline.write_bytes(source)
        empty = temporary / 'empty.txt'; empty.write_text('')
        empty_json = temporary / 'empty.json'
        empty_json.write_text(json.dumps({'translations': [], 'total_translations': 0}))
        driver.apply_patches(replace(config, combined=str(empty)), baseline, empty_json, build_number=0)
        expected = bytearray(baseline.read_bytes())
        for start,end in allowed:
            expected[start:end] = result[start:end]
        assert result == expected, 'Écriture post-patches hors des allocations/pointeurs autorisés'
        report = {'rom':str(rom.relative_to(ROOT)), 'records':records, 'count':len(records), 'references':sum(len(r['pointers']) for r in records), 'all_bytes_compared':True}
        (ROOT / 'output/reports').mkdir(exist_ok=True)
        (ROOT / 'output/reports/es013-probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        for suffix in ('translation_ready.json', 'trilingual_translation.csv', 'alias_base.csv'):
            (driver.TRANSLATION_DIR / f'es013-probe_{suffix}').unlink(missing_ok=True)
        print(f"ES-013 : {len(records)} sentinelles, {report['references']} références, comparaison intégrale avant/après patches.")


if __name__ == '__main__':
    main()
