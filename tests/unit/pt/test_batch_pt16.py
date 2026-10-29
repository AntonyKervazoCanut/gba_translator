"""PT-16 : couverture fermée et contrat de la fenêtre Pokédex."""
import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextDecoder, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt16_audit.json').read_text())


def test_exact_scope_and_protections():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    manifest = next(b['offsets'] for b in batches if b['id'] == 'PT-16')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {e['offset']: e['expected'] for e in guards['entries']}
    texts = {m[1]: m[2] for line in
             (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
             if (m := re.match(r'^(0x[0-9a-f]+): ?(.*)', line))}
    assert len(AUDIT['entries']) == len(manifest) == 282
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        assert row['status'] == 'translated'
        assert texts[row['offset']] == protected[row['offset']] == row['portuguese']
        raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes']
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert raw.count(b'\xfe') == bytes.fromhex(row['source_hex']).count(b'\xfe') == 2
        assert not any(c in raw for c in (0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD))
        assert row['references'] and row['reason']


def test_source_meaning_and_retained_names():
    texts = {r['offset']: r['portuguese'].replace(r'\n', ' ') for r in AUDIT['entries']}
    # Ces faits diffèrent du FR/du fichier nommé EN : traduire l'anglais réel.
    assert 'frio' in texts['0x446e63'] and 'gelo flutuante' in texts['0x446e63']
    assert 'Koffing' in texts['0x447800'] and 'murcha' in texts['0x447800']
    assert 'Screech' in texts['0x44741e'] and 'Selfdestruct' in texts['0x44741e']
    assert 'Poké Ball' in texts['0x44c05e'] and 'Nincada' in texts['0x44c05e']
    assert 'Zangoose' in texts['0x44d1d0'] and 'Seviper' in texts['0x44d15b']
    assert 'desastre natural' in texts['0x44db35']
    assert 'pérola' in texts['0x44ddfb']


def test_finalizer_after_repairs():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_16') == 1
    assert all(steps.index(s) < steps.index('batch_16') for s in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))


def test_electrode_quote_aliases_are_lossless():
    row = next(r for r in AUDIT['entries'] if r['offset'] == '0x447476')
    raw = TextEncoder.encode_pokemon(row['portuguese'].replace(r'\n', '\n'), strict=True)
    decoded = TextDecoder.decode_pokemon(raw)
    assert '“Bola-Bomba”' in decoded
    assert TextEncoder.encode_pokemon(decoded, strict=True) == raw
    assert decoded.replace('“', '"').replace('”', '"') == row['portuguese'].replace(r'\n', '\n')
