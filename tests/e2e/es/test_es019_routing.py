"""CSV réel, builder et patches : ES-019 sans traduction de production."""
import hashlib
import json
import shutil
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.item_description_routes import ItemDescriptionRoutes
from src.core.text_aliases import TextAliases
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]


def test_es019_real_pipeline_preserves_all_unselected_consumers(tmp_path, monkeypatch):
    config = load_registry().get('es-maint')
    source = driver.ENGLISH_ROM.read_bytes()
    aliases = TextAliases.load(ROOT / config.text_aliases, source)
    report = json.loads((ROOT/'docs/analysis/es/019_ROUTES.json').read_text())
    keys = {int(r['contract_offset'], 16) for r in report['routes'] if not r['in_same_lot']}
    keys.update(int(r['offset'], 16) for r in report['routes'] if r['in_same_lot'])
    # Les vrais débuts des quatre alias ne sont pas de nouvelles clés du lot.
    keys.difference_update(int(r['offset'], 16) for r in report['routes'] if not r['in_same_lot'])
    sources = list((ROOT/'languages').glob('*/combined_*.txt'))
    sources += list((ROOT/'languages').glob('*/protected_entries.yaml'))
    sources += list((ROOT/'input/roms').glob('*.gba'))
    sources += [ROOT/'docs/analysis/es/lots.json']
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    combined = {}
    for key in sorted(keys):
        live = aliases.entries[key]['live_offset'] if key in aliases.entries else key
        raw = bytes.fromhex(aliases.preservation.routes[live]['english_raw_bytes'])
        # Remplacement d'un glyphe seulement : même longueur, relocation pourtant obligatoire.
        # Les commandes et tous leurs arguments restent les octets EN.
        index = 3 if raw[0] == 0xFC else 0
        raw = raw[:index] + bytes([0xD4]) + raw[index+1:]  # Z après une éventuelle commande de couleur.
        combined[key] = ''.join(f'<0x{v:02X}>' for v in raw[:-1])
    combined_path = tmp_path/'combined.txt'
    combined_path.write_text(''.join(f'0x{k:08X}: {v}\n' for k, v in combined.items()))
    config = replace(config, combined=str(combined_path),
                     text_aliases=str(ROOT/config.text_aliases),
                     item_descriptions=str(ROOT/config.item_descriptions),
                     system_texts=str(ROOT/config.system_texts), output_rom=str(tmp_path/'sentinel.gba'))
    with monkeypatch.context() as patch:
        patch.setattr(driver, 'REPO_ROOT', tmp_path)
        patch.setattr(driver, 'TRANSLATION_DIR', tmp_path/'output/translation')
        ready = driver.generate_translation_json(config)
    items = json.loads(ready.read_text())['translations']
    assert len(items) == len(keys) == 6
    assert all(item['force_relocation'] for item in items)
    output = driver.build_rom(config, ready)
    built = output.read_bytes()
    allowed = bytearray(len(built))
    observations = []
    for item in items:
        raw = TextEncoder.encode_pokemon(ItemDescriptionRoutes.normalize(item)['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        for site in item['pointer_offsets']:
            target = int.from_bytes(built[site:site+4], 'little')-0x08000000
            assert target != item['offset']
            assert built[target:target+len(raw)] == raw
            allowed[site:site+4] = b'\1'*4
            allowed[target:target+len(raw)] = b'\1'*len(raw)
        observations.append({'key': item.get('contract_offset',item['offset']), 'live': item['offset'],
                                 'pointers': item['pointer_offsets'], 'expected_hex': raw.hex(),
                                 'target': target, 'layout': item.get('layout')})
    assert all(allowed[i] for i,(a,b) in enumerate(zip(source,built)) if a != b)
    driver.apply_patches(config, output, ready, build_number=0)
    final = output.read_bytes()
    aliases.verify(final, ready, combined)
    empty = tmp_path/'empty.txt'
    empty.write_text('')
    empty_json = tmp_path/'empty.json'
    empty_json.write_text('{"translations": [], "total_translations": 0}')
    baseline = tmp_path/'baseline.gba'
    baseline.write_bytes(source)
    driver.apply_patches(replace(config, combined=str(empty)), baseline, empty_json, build_number=0)
    assert all(allowed[i] for i, (a, b) in enumerate(zip(baseline.read_bytes(), final)) if a != b), 'Écriture hors sélection après patches'
    # Patches peuvent toucher leurs surfaces prévues, pas ces consommateurs et préimages.
    for item in items:
        raw = bytes.fromhex(item['english_raw_bytes'])
        assert final[item['offset']:item['offset']+len(raw)] == raw
    assert {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources} == before
    proof_dir = ROOT/'output/reports'
    proof_dir.mkdir(exist_ok=True)
    proof_rom = ROOT/'output/roms/es019-sentinel.gba'
    shutil.copyfile(output, proof_rom)
    (proof_dir/'es019-routing-probe.json').write_text(json.dumps({
        'rom': str(proof_rom), 'records': observations,
        'source_sha256': hashlib.sha256(source).hexdigest(),
        'source_hashes': before}, indent=2)+'\n')
