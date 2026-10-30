"""PT-68 : manifeste fermé, pages exactes et conditions des missions/services."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt68_audit.json').read_text())


def test_manifest_protections_and_controls():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-68')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 299
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 3
    for row in AUDIT['entries']:
        assert row['reason'] and row['scene'] and row['english_full']
        if row['status'] == 'exception':
            assert not row['references']
            continue
        offset = int(row['offset'], 16)
        assert texts[offset] == guards[offset] == row['portuguese']
        text = texts[offset].replace(r'\n', '\n')
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        assert len(encoded) == row['encoded_bytes']
        assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
        assert [c for c in commands(encoded) if c != b'\xfe'] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c != b'\xfe']
        assert line_widths(text) == row['line_widths']
        assert max(row['expanded_widths']) <= row['pixel_budget']
        if row['pixel_budget'] == 172:
            assert text.count('\n') <= 2
        elif '<0xFB>' in text or '<0xFA>' in text:
            for page in text.split('<0xFB>'):
                for index, segment in enumerate(page.split('<0xFA>')):
                    assert segment.count('\n') <= (1 if index == 0 else 0)


def test_missions_services_and_source_tail():
    rows = AUDIT['entries']
    assert 'começando' in rows[60]['portuguese']
    assert 'over 200' in rows[62]['english_full'] and '200 espécies' in rows[62]['portuguese']
    assert '25' in rows[95]['portuguese'] and 'Safari Zone' in rows[95]['portuguese']
    assert '30 Safari Balls' in rows[97]['portuguese']
    assert '20 formas' in rows[127]['portuguese'] and '19' in rows[127]['portuguese']
    assert 'Não precisa capturá-los' in rows[127]['portuguese']
    assert 'derrotar' in rows[128]['portuguese']
    assert 'sexta-feira de manhã' in rows[210]['portuguese']
    assert '50000' in rows[202]['portuguese'] and '100000' in rows[203]['portuguese']
    assert 'Master Balls' in rows[12]['portuguese'] and 'Articuno' in rows[13]['portuguese']
    assert 'Habilidade' in rows[55]['portuguese'] and 'Hidden Power' in rows[55]['portuguese']
    for index in (136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156,
                  158, 160, 162, 164, 166, 169, 171, 183, 184, 185, 186,
                  187, 188, 189, 190, 191, 192, 286, 287):
        assert rows[index]['status'] == 'retained'
    assert rows[127]['english_reference'].endswith("you're up to")
    assert rows[127]['english_full'].endswith('you may wish to.')


def test_finalizer_after_repairs():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_68') == 1
    for earlier in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'):
        assert patches.index(earlier) < patches.index('batch_68')


def test_gem_family_and_pointer_tables():
    rows = AUDIT['entries']
    assert all('Gem Family' in row['scene'] for row in rows[:3])
    # Table contiguë des coupes Furfrou : cellules pointeurs, pas textes fixes.
    assert [row['references'] for row in rows[183:193]] == [
        [0x1FB1DF8 + index * 4] for index in range(10)]
    # Couple nom/description de Vivillon dans une table de structures de 16 octets.
    assert rows[138]['references'] == [0x1E7AE10]
    assert rows[139]['references'] == [0x1E7AE14]
    assert rows[140]['references'] == [0x1E7AE20]
    assert rows[141]['references'] == [0x1E7AE24]
    assert not any(row['fixed_region'] for row in rows)


def test_unaligned_callback_match_is_not_a_text_reader():
    row = AUDIT['entries'][276]
    assert row['offset'] == '0x1f2a508'
    assert row['references'] == [0x1E7C8AE]
    assert row['binary_matches'][0]['site'] == 0x3E23E3
    assert row['binary_matches'][0]['source_hex'] == '9df20908a5f20908'
    assert sum(len(r['references']) for r in AUDIT['entries']) == 374


def test_player_and_rival_names_have_ten_wide_glyphs_of_margin():
    for row in AUDIT['entries']:
        for key in ('1', '6'):
            if key in row.get('buffers', {}):
                assert row['buffers'][key] == 'W' * 10
    assert max(AUDIT['entries'][9]['expanded_widths']) == 193
