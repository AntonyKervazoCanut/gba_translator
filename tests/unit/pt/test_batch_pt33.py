"""PT-33 : périmètre fermé, contrôle des pages et mécanique du domaine réel."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt33_audit.json').read_text())


def test_manifest_exact_protection_and_commands():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-33')
    rows, texts = AUDIT['entries'], entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == offsets
    assert len(rows) == 288
    assert sum(r['status'] == 'exception' for r in rows) == 25
    assert sum(r['status'] == 'retained' for r in rows) == 3
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english_reference']
        if row['status'] == 'exception':
            assert offset not in texts and not row['references']
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] < 1000
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        # FE peut être repositionné, mais aucune page, pause, couleur ou variable.
        assert [c for c in commands(raw) if c[0] != 0xFE] == [
            c for c in commands(bytes.fromhex(row['source_hex'])) if c[0] != 0xFE]
        widths = [line_width(line) for line in re.split(r'<0xF[AB]>|\\n', texts[offset])]
        assert widths == row['line_widths'] and max(widths) <= row['max_width']
        if row['layout'] == 'move_description':
            assert len(texts[offset].split(r'\n')) <= 5
        elif row['layout'] == 'fullscreen':
            assert raw.count(b'\xfe') == bytes.fromhex(row['source_hex']).count(b'\xfe')
        else:
            for page in texts[offset].split('<0xFB>'):
                assert page.count(r'\n') <= 1, row['offset']


def test_history_missions_sky_battles_and_glossary():
    texts = entries()
    for offset, terms in {
        0x8cb260: ['Dresco Town', 'Icicle Cave'],
        0x8cb872: ['Thundercap Mountain', 'SES', 'Expressway', 'sul'],
        0x8cb932: ['Zapdos', 'The Shadows', 'Ruins of Void'],
        0x8cc605: ['Kalos', 'Pokémon'],
        0x8cca21: ['Arceus', 'três pássaros', 'garrafa'],
        0x8cf0e4: ['Quest Log', '5', 'registrada', 'recompensas'],
        0x8d0933: ['Vivill Town', 'The Shadows', 'Light of Ruin', 'policiais'],
        0x8d184b: ['Voador', 'Levitate'],
        0x8c8dd0: ['Throat Chop'], 0x8c8e10: ['Heal Block'],
        0x90a718: ['Sweet Veil'], 0x90b780: ['Power Herb'],
    }.items():
        for term in terms:
            assert term in texts[offset].replace(r'\n', ' ')
    assert [texts[o] for o in (0x8cca05, 0x8cca10, 0x8cca18)] == ['Articuno!', 'Zapdos!', 'Moltres!']
    # Les sources EN extraites sont tronquées ; le texte complet ROM est traduit.
    assert 'desligando' not in texts[0x8d0933] and 'acabar com essa loucura' in texts[0x8d0933]
    assert 'volte a falar comigo' in texts[0x8cf0e4]
    assert texts[0x90f9f0] != texts[0x90fa20]
    assert 'Defesa' in texts[0x9056b4] and 'Ataque Especial' in texts[0x905c40]


def test_finalizer_follows_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_33') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert steps.index(step) < steps.index('batch_33')


def test_padding_keys_do_not_claim_delivery_through_a_dead_table():
    rows = {r['offset']: r for r in AUDIT['entries']}
    padding = [r for r in rows.values() if 'owner_offset' in r]
    assert len(padding) == 7
    for row in padding:
        assert row['status'] == rows[row['owner_offset']]['status'] == 'exception'
        assert 'ancienne table' in row['reason']
        assert 'legacy_table_references' in rows[row['owner_offset']]
