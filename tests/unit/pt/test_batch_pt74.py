"""PT-74 : guides TM/raids, journal Missions et services de Redwood."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]


def audit():
    """Charge le bilan individuel des offsets PT-74."""
    return json.loads((ROOT / 'languages/pt/data/pt74_audit.json').read_text())


def test_manifest_protections_and_exact_controls():
    rows = audit()['entries']
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-74')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == manifest
    assert len(rows) == 300
    assert sum(r['status'] == 'exception' for r in rows) == 4
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene'] and row['source_hex']
        if row['status'] == 'exception':
            assert not row['references'] and offset not in texts
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        text = texts[offset].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        # Le marqueur explicite vide produit un terminateur suivi du terminateur automatique.
        assert raw == b'\xff\xff' or (raw[-1] == 255 and 255 not in raw[:-1])
        assert len(raw) == row['encoded_bytes']
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        assert line_widths(text) == row['line_widths']
        assert max(row['expanded_widths']) <= row['pixel_budget']
        if 'small_font_budget' in row:
            assert row['expanded_widths'][0] <= row['small_font_budget'] == 32
        if row['layout'] == 'dialogue':
            for page in text.split('<0xFB>'):
                for n, segment in enumerate(page.split('<0xFA>')):
                    assert segment.count('\n') <= (1 if n == 0 else 0), row['offset']
        else:
            assert '<0xFA>' not in text and '<0xFB>' not in text
            assert text.count('\n') <= 2


def test_missions_headers_and_actual_all_label():
    rows = audit()['entries']
    assert rows[71]['portuguese'] == '<0xFF>'
    assert rows[73]['portuguese'] == 'Ativ.'
    assert rows[82]['english_reference'] is None
    assert rows[82]['english_full'] == 'All'
    assert rows[82]['portuguese'] == 'Todas'
    assert rows[72]['portuguese'] == '<0xF8><0x03>Tipo'
    assert rows[85]['portuguese'].endswith('<0x00>')
    assert rows[114]['references'] == [0x1EBFACC]
    assert rows[114]['non_text_references'] == [0x1D877D8]
    for i in range(71):
        assert rows[i]['references'] == [0x1E80614 + 16 * i]
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_74') == 1
    assert patches.index('batch_74') > patches.index('font')
    assert patches.index('batch_74') > patches.index('repoint_stale')


def test_raid_mechanics_rewards_and_services_are_preserved():
    rows = audit()['entries']
    assert 'três turnos' in rows[156]['portuguese']
    assert 'dois escudos' in rows[157]['portuguese']
    assert '5 equipes' in rows[158]['portuguese']
    assert 'Poké Ball' in rows[236]['portuguese']
    assert 'NÃO uma Great Ball ou Ultra Ball' in rows[236]['portuguese']
    assert '30' in rows[256]['portuguese']
    assert '7h' in rows[270]['portuguese'] and '19h' in rows[270]['portuguese']
    assert 'chocarem muito mais rápido' in rows[277]['portuguese']
    assert 'todos' in rows[289]['portuguese'] and 'todos' in rows[290]['portuguese']
    for i in (292, 293):
        assert 'Ovo<0xFD><0x04>' in rows[i]['portuguese']
    assert 'Charcoal' in rows[299]['portuguese']
    assert re.search(r'golpe<0xFD><0x08>', rows[211]['portuguese'])
