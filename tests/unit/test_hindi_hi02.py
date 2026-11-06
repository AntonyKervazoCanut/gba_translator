"""Contrat fermé HI-02 : source, décisions, contrôles et protections exactes."""
import hashlib
import json
from pathlib import Path

from languages.indie.patches.batch_02 import HindiBatch02Patch
from scripts.check_translation_integrity import load_last_wins
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[2]


def test_hi02_inventory_and_exact_protections():
    source = ROOT / 'languages/en/combined_en.txt'
    entries, _ = load_last_wins(source)
    selection = {o for o in entries if 0x1A532F <= o <= 0x23E635}
    audit = json.loads((ROOT / 'languages/indie/data/hi02_audit.json').read_text())
    actual, _ = load_last_wins(ROOT / 'languages/indie/combined_indie.txt')
    assert hashlib.sha256(source.read_bytes()).hexdigest() == audit['snapshot_sha256']
    assert len(selection) == len(audit['entries']) == 400
    assert {int(r['offset'], 16) for r in audit['entries']} == selection
    for row in audit['entries']:
        offset = int(row['offset'], 16)
        assert row['status'] in {'translated', 'retained', 'excluded'}
        assert row['reason'] and row['category'] in {'dialogue', 'combat', 'interface', 'table'}
        if row['status'] == 'translated':
            assert actual[offset] == row['translation']
            encoded = TextEncoder.encode_pokemon(actual[offset].replace(r'\n', '\n'), strict=True)
            assert HindiBatch02Patch.controls(encoded) == HindiBatch02Patch.controls(bytes.fromhex(row['source_hex']))
            if row.get('cell_bytes'):
                assert len(encoded) <= row['cell_bytes']
        else:
            assert offset not in actual


def test_controls_distinguish_newlines_from_control_arguments():
    raw = bytes.fromhex('fdfe fc01fe fe fa fb ff')
    assert HindiBatch02Patch.controls(raw) == [b'\xfd\xfe', b'\xfc\x01\xfe', b'\xfe', b'\xfa', b'\xfb']
