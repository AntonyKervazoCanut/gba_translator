"""PT-73 : périmètre, réglages, pagination et terminologie des indices TM."""
import json
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]


def audit():
    """Charge le bilan individuel des 299 clés du lot."""
    return json.loads((ROOT / 'languages/pt/data/pt73_audit.json').read_text())


def test_scope_protection_and_exact_commands():
    rows = audit()['entries']
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-73')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == manifest
    assert len(rows) == 299
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene'] and row['source_hex']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex'])), row['offset']
        assert max(row['expanded_widths']) <= row['pixel_budget'], row['offset']


def test_settings_and_tm_hints_semantics():
    rows = audit()['entries']
    assert rows[94]['portuguese'] == r'Salvar\nIgnorar\nCancelar'
    assert 'Salvar' in rows[96]['portuguese'] and 'descartar' in rows[96]['portuguese']
    assert 'None' not in rows[96]['portuguese']
    assert 'Exp. Share' in rows[36]['portuguese']
    assert '120' in rows[243]['portuguese']
    for row in rows[250:]:
        assert 'TM' in row['portuguese']
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_73') == 1
    assert patches.index('batch_73') > patches.index('font')


def test_croagunk_variants_and_fishing_counter_are_bounded():
    data = audit()
    local = data['runtime_buffers']['croagunk_local_fix']
    assert [r['portuguese'] for r in local['descriptors']] == [
        'olhos redondos e fofos', 'bochechas laranja-vivo',
        'expressão de tédio', 'o maior sorriso']
    assert all(len(TextEncoder.encode_pokemon(r['portuguese'], strict=True)) <= 32
               for r in local['descriptors'])
    for index in (226, 228):
        assert data['entries'][index]['buffers']['3'] == '65535'
