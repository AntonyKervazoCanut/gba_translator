"""PT-22 : périmètre fermé, commandes exactes et scènes de Borrius."""
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]
AUDIT_PATH = ROOT / 'languages/pt/data/pt22_audit.json'


def audit():
    """Charge les décisions sourcées du lot, dans l'ordre du manifeste."""
    return json.loads(AUDIT_PATH.read_text())


def values():
    """Résout les traductions selon la dernière occurrence gagnante."""
    return {int(match[1], 16): match[2]
            for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
            if (match := re.match(r'0x([\da-fA-F]+): ?(.*)', line))}


def test_manifest_exact_coverage_protections_and_commands():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(batch['offsets'] for batch in batches if batch['id'] == 'PT-22')
    rows = audit()['entries']
    actual = values()
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(entry['offset'], 16): entry['expected'] for entry in guards['entries']}

    assert len(rows) == len(manifest) == 288
    assert [row['offset'] for row in rows] == manifest
    assert sum(row['status'] == 'translated' for row in rows) == 240
    assert sum(row['status'] == 'exception' for row in rows) == 48
    assert sum(len(row['references']) for row in rows) == 297
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english']
        if row['status'] == 'exception':
            assert offset not in actual
            assert not row['references']
            continue
        assert actual[offset] == protected[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(actual[offset].replace(r'\n', '\n'), strict=True)
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex'])), row['offset']
        assert len(raw) == row['encoded_bytes']


def test_live_fragments_are_translated_and_movement_is_excluded():
    rows = {int(row['offset'], 16): row for row in audit()['entries']}
    assert rows[0x778EAF]['status'] == 'exception'
    assert rows[0x778EAF]['source_sites'] == [
        '0x7635d7', '0x7635de', '0x7635e5', '0x7636fa', '0x763701',
    ]
    assert bytes.fromhex(rows[0x778EAF]['source_hex']).startswith(b'\x04\xfe')
    for offset in (0x788BAB, 0x788BCD, 0x788BFF, 0x788C15):
        assert rows[offset]['status'] == 'translated'
        assert rows[offset]['references']
        assert 'névoa densa' in rows[offset]['portuguese'].lower()


def test_integrated_batches_distinguish_script_opcodes_from_text_pointers():
    batches = {
        number: json.loads((ROOT / f'languages/pt/data/pt{number}_audit.json').read_text())['entries']
        for number in (20, 22, 25)
    }
    script = next(row for row in batches[20] if row['offset'] == '0x745132')
    dialogue = next(row for row in batches[25] if row['offset'] == '0x7c56ca')

    assert script['status'] == 'exception'
    assert bytes.fromhex(script['source_hex'])[:9] == bytes.fromhex('0f00ca567c08090602')
    assert dialogue['status'] == 'translated'
    assert dialogue['references'] == [0x745134]
    owners = [
        {site for row in batches[number] if row['status'] == 'translated' for site in row['references']}
        for number in (20, 22, 25)
    ]
    assert all(not left & right for index, left in enumerate(owners) for right in owners[index + 1:])


def test_glossary_names_gender_buffers_and_domain_semantics():
    actual = values()
    assert actual[0x77389C] == 'Fallshore City'
    assert actual[0x77F003] == 'Frost Mountain'
    assert actual[0x78095F] == 'Afterlife'
    assert 'Planta' in actual[0x788D2D] and 'Grama' not in actual[0x788D2D]
    assert 'Planta' in actual[0x788DF4] and 'Grama' not in actual[0x788DF4]
    assert 'Rock Climb' in actual[0x77365A]
    assert 'The Shadows' in actual[0x775B90]
    assert 'Poção' in actual[0x775C6A]
    assert 'SES' in actual[0x788429]
    assert 'KBT' not in actual[0x788429]
    assert 'Shadow Sneak' in actual[0x78158D] and 'Aerial Ace' in actual[0x78158D]
    assert actual[0x77F57B] == 'filho'
    assert actual[0x77F57F] == 'filha'
    assert actual[0x781697] == 'senhor'
    assert actual[0x78169B] == 'senhora'
    assert 'Grass Knot' in actual[0x788E54]
    assert '3' in actual[0x7789B9] and 'Combee' in actual[0x7789B9]
    assert 'Articuno' in actual[0x776197] and 'Zapdos' in actual[0x77624A]
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_22') == 1
    assert steps.index('batch_22') > steps.index('repoint_stale')
    # Le lot concurrent PT-20 exige de conserver son finaliseur en dernier.
    assert steps.index('batch_22') < steps.index('batch_20') == len(steps) - 1
