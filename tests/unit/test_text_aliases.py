import json
from pathlib import Path

import pytest

from src.core.text_aliases import TextAliases

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / 'languages/es-maint/text_aliases.json'
FIXTURE = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es001.json').read_text())
EXTRA = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es003.json').read_text())
ES011 = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es011.json').read_text())
ES011_PREFIXES = {int(e['live_offset'], 16): bytes.fromhex(e['prefix_hex']) for e in json.loads((ROOT / 'docs/analysis/es/011_ROUTES.json').read_text())['aliases_candidates']}
ES015 = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es015.json').read_text())
ES013 = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es013.json').read_text())
ES013_PREFIXES = {int(e['live_offset'], 16): bytes.fromhex(e['prefix_hex']) for e in ES013['aliases']}
ES017 = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es017.json').read_text())
ES016 = json.loads((Path(__file__).parent / 'fixtures/text_aliases/es016.json').read_text())
for language in ('english', 'spanish'):
    FIXTURE[language].extend(e for e in ES016[language] if e['offset'] not in {0x7808DE, 0x780E34, 0x788538, 0x78D43E})
    FIXTURE[language].extend(ES017[language])
    FIXTURE[language].extend(ES013[language])
    FIXTURE[language].extend(ES015[language])
    FIXTURE[language].extend(e for e in ES011[language] if e['offset'] < 0x41D200)
    FIXTURE[language].extend(EXTRA[language])
    FIXTURE[language].extend(json.loads((Path(__file__).parent / 'fixtures/text_aliases/es008.json').read_text())[language])
    FIXTURE[language].extend(json.loads((Path(__file__).parent / 'fixtures/text_aliases/es002.json').read_text())[language])


def rom_fixture():
    rom = bytearray(0x2000000)
    for entry in FIXTURE['english'] + [e for e in ES011['english'] if e['offset'] >= 0x41D200]:
        offset = entry['offset']
        raw = bytes.fromhex(entry['raw_bytes'])
        prefix = {0x24F210: b'\x00\x00\x00', 0x24F3C4: b'\x05\x00\x00',
                  0x2779D5: b'\x00', 0x2779F2: b'\xfe',
                  0x415D48: bytes(3), 0x415D50: bytes(1), 0x415D60: bytes(2),
                  0x415D78: bytes(1), 0x415D8C: bytes(2), 0x4160FC: bytes(3), 0x416104: bytes(3)}.get(offset, ES013_PREFIXES.get(offset, ES011_PREFIXES.get(offset, b'\xaa')))
        rom[offset - len(prefix):offset + len(raw)] = prefix + raw
        for pointer in entry['pointer_offsets']:
            p = int(pointer, 16)
            rom[p:p + 4] = (0x08000000 + offset).to_bytes(4, 'little')
    for guard in json.loads((Path(__file__).parent / 'fixtures/text_aliases/es008.json').read_text())['guards'] + ES011['guards']:
        offset = int(guard['offset'], 16)
        raw = bytes.fromhex(guard['hex'])
        rom[offset:offset + len(raw)] = raw
    for part in ES015["slices"] + ES017["slices"] + ES016["slices"]:
        start = part["offset"]
        raw = bytes.fromhex(part["hex"])
        rom[start:start+len(raw)] = raw
    return bytes(rom)


def test_real_preimages_resolve_all_contract_keys():
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    assert len(aliases.entries) == 102
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
    mapping.write_text(json.dumps({'offset_map': [{'english_offset': e['offset'], 'spanish_offset': None if e['offset'] == 0x416104 else e['offset'], 'status': 'only_in_english' if e['offset'] == 0x416104 else 'matched'} for e in FIXTURE['english']]}))
    rom = bytearray(0x2000000)
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
    path.write_text(json.dumps({'translations': [{'offset': k, 'translation': ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(aliases.entries[k]['english_raw_hex'])[:-1])} for k in keys]}))
    payload = json.loads(path.read_text())
    next(i for i in payload['translations'] if i['offset'] == 0x41CF13)['translation'] = 'Registro<0xFE>Espera'
    next(i for i in payload['translations'] if i['offset'] == 0x781278)['translation'] = 'TEST<0xFE>TEST<0xFE>TEST'
    path.write_text(json.dumps(payload))
    payload = json.loads(path.read_text())
    next(i for i in payload['translations'] if i['offset'] == 0x7B3BE9)['translation'] = 'TEST<0xFE>TEST<0xFE>TEST'
    path.write_text(json.dumps(payload))
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


def test_es002_adds_only_the_four_contractual_aliases():
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    expected = {0x1A5AD5: 0x1A5AD6, 0x1B1D7C: 0x1B1D7D,
                0x1BC310: 0x1BC311, 0x1C27E6: 0x1C27E7}
    assert {k: e['live_offset'] for k,e in aliases.entries.items()
            if 0x1A5133 <= k <= 0x23E5A6} == expected
    for key, live in expected.items():
        with pytest.raises(ValueError, match='collision'):
            aliases.check_keys({key, live})


@pytest.mark.parametrize('position', [0x1A5AD5, 0x1B1D7C, 0x1BC310, 0x1C27E6,
                                    0x16E35F, 0x1B286E, 0x1BB44B, 0x1AABFD, 0x1AAC24])
def test_es002_aliases_reject_changed_prefixes_and_consumers(position):
    source = bytearray(rom_fixture())
    source[position] ^= 1
    with pytest.raises(ValueError):
        TextAliases.load(CONTRACT, source)


def test_english_only_alias_has_no_invented_spanish_reference(tmp_path):
    import csv
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    base, mapping, rom, es, en = csv_fixture(tmp_path)
    out = tmp_path / 'result.csv'
    aliases.prepare_csv(base, out, {0x416101}, mapping, rom, es, en)
    row = next(r for r in csv.DictReader(out.open()) if int(r['offset'], 16) == 0x416101)
    assert row['original_text'] == 'IDNo.'
    assert row['spanish_text'] == ''
    assert aliases.entries[0x416101]['spanish_offset'] is None


@pytest.mark.parametrize('mutation', ['matched', 'target', 'duplicate', 'no_opt_in'])
def test_english_only_requires_explicit_absence(tmp_path, mutation):
    data = json.loads(CONTRACT.read_text())
    record = next(r for r in data['aliases'] if r['contract_offset'] == '0x00416101')
    base, mapping, rom, es, en = csv_fixture(tmp_path)
    mapped = json.loads(mapping.read_text())
    entry = next(e for e in mapped['offset_map'] if e['english_offset'] == 0x416104)
    if mutation == 'matched':
        entry['status'] = 'matched'
    elif mutation == 'target':
        entry['spanish_offset'] = 0x416104
    elif mutation == 'duplicate':
        mapped['offset_map'].append(entry)
    else:
        record.pop('english_only')
    mapping.write_text(json.dumps(mapped))
    path = tmp_path / 'contract.json'
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        aliases = TextAliases.load(path, rom_fixture())
        aliases.prepare_csv(base, tmp_path / 'out.csv', {0x416101}, mapping, rom, es, en)


@pytest.mark.parametrize('position', [0x415D45, 0x415D4F, 0x415D5E, 0x415D77, 0x415D8A,
                                    0x4160F9, 0x416101, 0x12EF3C, 0x9F2868, 0x9F2B98])
def test_es008_rejects_changed_prefixes_or_consumers(position):
    rom = bytearray(rom_fixture())
    rom[position] ^= 1
    with pytest.raises(ValueError):
        TextAliases.load(CONTRACT, rom)


@pytest.mark.parametrize('mutation', ['prefix', 'pointer', 'text', 'missing', 'duplicate', 'restored_en'])
def test_final_verification_refuses_lost_aliases(tmp_path, mutation):
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    path = tmp_path / 'ready.json'
    text = 'PRUEBA'
    path.write_text(json.dumps({'translations': [{'offset': 0x416101, 'translation': text}]}))
    aliases.resolve_json(path, {0x416101})
    from src.core.text_codec import TextEncoder
    raw = TextEncoder.encode_pokemon(text)
    rom = bytearray(rom_fixture())
    target = 0x900000
    rom[target:target + len(raw)] = raw
    for ref in aliases.entries[0x416101]['pointer_offsets']:
        rom[ref:ref + 4] = (0x08000000 + target).to_bytes(4, 'little')
    aliases.verify(rom, path, {0x416101: text})
    if mutation == 'prefix':
        rom[0x416101] = 1
    elif mutation == 'pointer':
        rom[0xF33D8] ^= 1
    elif mutation == 'text':
        rom[target] ^= 1
    elif mutation == 'restored_en':
        rom[0x9F2B98:0x9F2B9C] = (0x08000000 + 0x416104).to_bytes(4, 'little')
    else:
        payload = json.loads(path.read_text())
        payload['translations'] = [] if mutation == 'missing' else payload['translations'] * 2
        path.write_text(json.dumps(payload))
    with pytest.raises(ValueError):
        aliases.verify(rom, path, {0x416101: text})


def test_es008_measures_keypad_and_latin_from_engine_tables():
    from src.core.item_description_routes import ItemDescriptionRoutes
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    entry = aliases.entries[0x415D45]
    item = {'offset': entry['live_offset'], 'translation': '<0xF8><0x00>Next',
                'english_raw_bytes': entry['english_raw_hex'], 'strict_encoded_layout': True,
                'layout': {**entry['layout'], 'max_width': 28}}
    ItemDescriptionRoutes.normalize(item)
    item['layout']['max_width'] = 27
    with pytest.raises(ValueError, match='budget'):
        ItemDescriptionRoutes.normalize(item)


@pytest.mark.parametrize('position', [0x1EEF00, 0x207300, 0x1EA6CE, 0x40C234, 0xF2754, 0x10F558])
def test_es008_refuses_changed_metrics_and_window_roots(position):
    source = bytearray(rom_fixture())
    source[position] ^= 1
    with pytest.raises(ValueError, match='racine'):
        TextAliases.load(CONTRACT, source)


@pytest.mark.parametrize('old,new', [('00', '01'), ('0A', '09')])
def test_es008_preserves_keypad_arguments(tmp_path, old, new):
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    entry = aliases.entries[0x415D5E]
    text = ''.join(f'<0x{b:02X}>' for b in bytes.fromhex(entry['english_raw_hex'])[:-1])
    path = tmp_path / 'bad.json'
    path.write_text(json.dumps({'translations': [{'offset': 0x415D5E,
        'translation': text.replace(f'<0xF8><0x{old}>', f'<0xF8><0x{new}>')}]}))
    with pytest.raises(ValueError, match='commandes'):
        aliases.resolve_json(path, {0x415D5E})


def test_es008_engine_metrics_include_f9_and_preserve_fc_arguments():
    from scripts import build_language as driver
    from src.core.item_description_routes import ItemDescriptionRoutes
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    layout = aliases.entries[0x415D45]['layout']
    builder = driver._load_module(driver.BUILD_SCRIPT).TranslatedROMBuilder
    assert builder._encoded_layout_widths(bytes.fromhex('f905ff'), layout) == [8]
    item = {'offset': 0, 'translation': '<0xFC><0x01><0x04><0xF9><0x05>',
            'english_raw_bytes': 'fc0104f905ff', 'layout': layout, 'strict_encoded_layout': True}
    ItemDescriptionRoutes.normalize(item)
    item['translation'] = '<0xFC><0x01><0x05><0xF9><0x05>'
    with pytest.raises(ValueError, match='commandes'):
        ItemDescriptionRoutes.normalize(item)


@pytest.mark.parametrize('text', ['A' * 39, '<0x00>' * 39, 'Name<0xFE>Deux', 'Name<0xFF>Fin'])
def test_es008_rejects_width_lines_and_internal_terminator(tmp_path, text):
    aliases = TextAliases.load(CONTRACT, rom_fixture())
    path = tmp_path / 'bad.json'
    path.write_text(json.dumps({'translations': [{'offset': 0x4160F9, 'translation': text}]}))
    with pytest.raises(ValueError):
        aliases.resolve_json(path, {0x4160F9})
