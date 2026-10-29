import json
from pathlib import Path

import pytest

from src.core.text_aliases import TextAliases

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'languages/es-maint/text_aliases.json'
FIXTURE = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es001.json').read_text())
EXTRA = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es003.json').read_text())
for language in ('english', 'spanish'):
    FIXTURE[language].extend(EXTRA[language])


def rom_fixture():
    rom = bytearray(0xA00000)
    for entry in FIXTURE['english']:
        offset = entry['offset']
        raw = bytes.fromhex(entry['raw_bytes'])
        prefix = {0x24F210: b'\x00\x00\x00', 0x24F3C4: b'\x05\x00\x00',
                  0x2779D5: b'\x00', 0x2779F2: b'\xfe'}.get(offset, b'\xaa')
        rom[offset - len(prefix):offset + len(raw)] = prefix + raw
        for pointer in entry['pointer_offsets']:
            p = int(pointer, 16)
            rom[p:p + 4] = (0x08000000 + offset).to_bytes(4, 'little')
    return bytes(rom)


def test_real_preimages_resolve_ten_contract_keys():
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    assert len(aliases.entries) == 14
    assert aliases.entries[0x24F3C1]['live_offset'] == 0x24F3C4
    assert aliases.entries[0x24F20D]['live_offset'] == 0x24F210
    assert 0x18D43D not in aliases.entries
    assert aliases.entries[0x17FF49]['live_offset'] == 0x17FF4A


@pytest.mark.parametrize('position', [0x17FF49, 0x17FF4A, 0x166CAF,
                                    0x24F3C1, 0x24F3C4, 0x96DF38,
                                    0x2779D4, 0x2779D5, 0x3074B2,
                                    0x2779F1, 0x2779F2, 0x307535])
def test_changed_prefix_text_or_pointer_is_rejected(position):
    rom = bytearray(rom_fixture())
    rom[position] ^= 1
    with pytest.raises(ValueError):
        TextAliases.load(CONTRACT, bytes(rom))


def test_contract_and_live_key_cannot_coexist():
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    with pytest.raises(ValueError, match='collision'):
        aliases.check_keys({0x17FF49, 0x17FF4A})


def test_new_direct_pointer_to_false_start_is_rejected():
    rom = bytearray(rom_fixture())
    rom[16:20] = (0x08000000 + 0x17FF49).to_bytes(4, 'little')
    with pytest.raises(ValueError):
        TextAliases.load(CONTRACT, bytes(rom))


@pytest.mark.parametrize('field,value', [('contract_offset','0x0017FF49'), ('live_offset','0x0017FF4A')])
def test_duplicate_contract_or_live_target_is_rejected(tmp_path, field, value):
    data = json.loads(CONTRACT.read_text())
    data['aliases'][1][field] = value
    path = tmp_path / 'aliases.json'
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        TextAliases.load(path, rom_fixture())


def csv_fixture(tmp_path):
    import csv

    from src.core.text_converter import JSONToCSVConverter
    path = tmp_path / 'base.csv'
    with path.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=JSONToCSVConverter.CSV_FIELDNAMES)
        writer.writeheader()
        for entry in FIXTURE['english']:
            writer.writerow({'offset': f"0x{entry['offset']:08X}", 'original_text': entry['text'],
                                 'original_length': entry['length'], 'padding_available': 0,
                                 'real_max_length': entry['length'], 'encoding': 'pokemon',
                                 'category': 'dialogue', 'translation': '', 'notes': ''})
    en = tmp_path / 'en.json'
    en.write_text(json.dumps({'texts': FIXTURE['english']}))
    es = tmp_path / 'es.json'
    es.write_text(json.dumps({'texts': FIXTURE['spanish']}))
    mapping = tmp_path / 'map.json'
    mapping.write_text(json.dumps({'offset_map': [{'english_offset': e['offset'], 'spanish_offset': e['offset'], 'status': 'matched'} for e in FIXTURE['english']]}))
    rom = bytearray(0xA00000)
    for entry in FIXTURE['spanish']:
        raw = bytes.fromhex(entry['raw_bytes'])
        rom[entry['offset']:entry['offset'] + len(raw)] = raw
        for pointer in entry['pointer_offsets']:
            p = int(pointer, 16)
            rom[p:p + 4] = (0x08000000 + entry['offset']).to_bytes(4, 'little')
    return path, mapping, bytes(rom), es, en


def test_csv_uses_live_preimages_and_json_keeps_provenance(tmp_path):
    import csv
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    base, mapping, rom, es, en = csv_fixture(tmp_path)
    output = tmp_path / 'alias.csv'
    keys = set(aliases.entries)
    aliases.prepare_csv(base, output, keys, mapping, rom, es, en)
    rows = list(csv.DictReader(output.open()))
    assert {int(r['offset'], 16) for r in rows} == keys
    assert rows[0]['original_text'] == FIXTURE['english'][0]['text']
    assert rows[0]['spanish_text'] == FIXTURE['spanish'][0]['text']
    path = tmp_path / 'ready.json'
    path.write_text(json.dumps({'translations': [{'offset': k, 'translation': 'ALIAS SENTINEL'} for k in keys]}))
    aliases.resolve_json(path, keys)
    items = json.loads(path.read_text())['translations']
    for item in items:
        entry = aliases.entries[item['contract_offset']]
        assert item['offset'] == entry['live_offset']
        assert item['english_raw_bytes'] == entry['english_raw_hex']
        assert item['pointer_offsets'] == entry['pointer_offsets']
        assert item['original_length'] == len(bytes.fromhex(entry['english_raw_hex'])) - 1


@pytest.mark.parametrize('mutation', ['ambiguous_map', 'missing_map', 'spanish_bytes', 'english_extract', 'csv_collision', 'duplicate_en', 'duplicate_es'])
def test_csv_refuses_ambiguous_or_changed_sources(tmp_path, mutation):
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    base, mapping, rom, es, en = csv_fixture(tmp_path)
    data = json.loads(mapping.read_text())
    if mutation == 'ambiguous_map':
        data['offset_map'].append(data['offset_map'][0])
    elif mutation == 'missing_map':
        data['offset_map'].pop(0)
    elif mutation == 'spanish_bytes':
        rom = bytes(len(rom))
    elif mutation == 'english_extract':
        en.write_text('{"texts": []}')
    elif mutation in ('duplicate_en', 'duplicate_es'):
        path = en if mutation == 'duplicate_en' else es
        extracted = json.loads(path.read_text())
        extracted['texts'].append(extracted['texts'][0])
        path.write_text(json.dumps(extracted))
    elif mutation == 'csv_collision':
        base.write_text(base.read_text().replace('0x0017FF4A', '0x0017FF49'))
    mapping.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        aliases.prepare_csv(base, tmp_path / 'out.csv', set(aliases.entries), mapping, rom, es, en)


def test_json_refuses_silently_dropped_alias(tmp_path):
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    path = tmp_path / 'ready.json'
    path.write_text('{"translations": []}')
    with pytest.raises(ValueError, match='dropped'):
        aliases.resolve_json(path, {0x17FF49})


def test_spanish_reference_follows_map_not_contract_or_english_address(tmp_path):
    data = json.loads(CONTRACT.read_text())
    record = data['aliases'][0]
    record['spanish_offset'] = '0x001B0000'
    contract = tmp_path / 'aliases.json'
    contract.write_text(json.dumps(data))
    aliases = TextAliases.load(contract, rom_fixture())
    base, mapping, rom, es, en = csv_fixture(tmp_path)
    mapped = json.loads(mapping.read_text())
    mapped['offset_map'][0]['spanish_offset'] = 0x1B0000
    mapping.write_text(json.dumps(mapped))
    extracted = json.loads(es.read_text())
    extracted['texts'][0]['offset'] = 0x1B0000
    es.write_text(json.dumps(extracted))
    relocated = bytearray(rom)
    raw = bytes.fromhex(record['spanish_raw_hex'])
    relocated[0x1B0000:0x1B0000 + len(raw)] = raw
    for pointer in record['pointer_offsets']:
        p = int(pointer, 16)
        relocated[p:p + 4] = (0x08000000 + 0x1B0000).to_bytes(4, 'little')
    aliases.prepare_csv(base, tmp_path / 'result.csv', {0x17FF49}, mapping,
                        bytes(relocated), es, en)
    assert FIXTURE['spanish'][0]['text'] in (tmp_path / 'result.csv').read_text()


def test_alias_resolution_is_only_enabled_for_es_maint():
    from src.i18n import load_registry
    configs = list(load_registry())
    assert {c.code for c in configs if c.text_aliases} == {'es-maint'}


def test_inline_cli_never_writes_short_translation_at_false_start(tmp_path):
    import subprocess
    import sys

    source = tmp_path / 'source.gba'
    source.write_bytes(rom_fixture())
    output = tmp_path / 'out.gba'
    output.write_bytes(source.read_bytes())
    combined = tmp_path / 'combined.txt'
    combined.write_text('0x0017FF49: ALIAS\n')
    en = tmp_path / 'en.json'
    en.write_text(json.dumps({'texts': FIXTURE['english']}))
    # A misleading reference at AA must not let the inline fallback claim it.
    false = dict(FIXTURE['english'][0])
    false.update(offset=0x17FF49, raw_bytes='aa' + false['raw_bytes'],
                 byte_length=false['byte_length'] + 1)
    es = tmp_path / 'es.json'
    es.write_text(json.dumps({'texts': [false]}))
    result = subprocess.run([
        sys.executable, str(ROOT / 'scripts/apply_inline_overrides_fr.py'),
        '--rom', str(output), '--source', str(source), '--combined', str(combined),
        '--english-texts', str(en), '--reference-texts', str(es),
        '--text-aliases', str(CONTRACT), '--allow-empty-translations',
    ], check=False, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'No combined entries found.' in result.stdout
    assert output.read_bytes() == source.read_bytes()


@pytest.mark.parametrize('replacement', ['<0xFA>', '<0xFE>'])
def test_builder_preserves_or_rejects_alias_control_flow(replacement):
    from scripts import build_language as driver
    module = driver._load_module(driver.BUILD_SCRIPT)
    builder = module.TranslatedROMBuilder(module.BuildConfig(source_rom=Path('unused')))
    entry = FIXTURE['english'][7]  # actual FA + FB dialogue preimage
    translation = ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(entry['raw_bytes'])[:-1])
    item = {'translation': translation.replace('<0xFA>', replacement),
            'english_raw_bytes': entry['raw_bytes'], 'original_text': entry['text'],
            'category': 'dialogue', 'preserve_control_flow': True}
    if replacement == '<0xFE>':
        with pytest.raises(ValueError, match='commandes'):
            builder._normalize_translation_item(entry['offset'], item)
    else:
        result = builder._normalize_translation_item(entry['offset'], item)
        from src.core.text_codec import TextEncoder
        assert TextEncoder.encode_pokemon(result['translation']) == bytes.fromhex(entry['raw_bytes'])


@pytest.mark.parametrize('index,old,new', [(0, '<0x06>', '<0x07>'), (5, '<0x06>', '<0x05>')])
def test_builder_refuses_changed_fc_or_fd_arguments(index, old, new):
    from scripts import build_language as driver
    module = driver._load_module(driver.BUILD_SCRIPT)
    builder = module.TranslatedROMBuilder(module.BuildConfig(source_rom=Path('unused')))
    entry = FIXTURE['english'][index]
    text = ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(entry['raw_bytes'])[:-1])
    with pytest.raises(ValueError, match='commandes'):
        builder._normalize_translation_item(entry['offset'], {
            'translation': text.replace(old, new), 'english_raw_bytes': entry['raw_bytes'],
            'preserve_control_flow': True,
        })


def test_builder_refuses_alias_above_512_bytes():
    from scripts import build_language as driver
    module = driver._load_module(driver.BUILD_SCRIPT)
    builder = module.TranslatedROMBuilder(module.BuildConfig(source_rom=Path('unused')))
    entry = FIXTURE['english'][1]
    with pytest.raises(ValueError, match='512'):
        builder._normalize_translation_item(entry['offset'], {
            'translation': 'A' * 512, 'english_raw_bytes': entry['raw_bytes'],
            'preserve_control_flow': True,
        })
