"""PT-85 : manifeste fermé, noms canoniques et structure des échanges BP."""
import json
from pathlib import Path

import yaml

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt85_audit.json').read_text())


def test_closed_manifest_protections_and_commands():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-85')
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    texts = entries()
    assert len(manifest) == 300
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    for row in AUDIT['entries']:
        text = texts[int(row['offset'], 16)]
        assert text == row['portuguese'] == guards[int(row['offset'], 16)]
        encoded = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert len(encoded) == row['encoded_bytes']
        commands = lambda raw: [c for c in _extract_control_sequences_from_raw(raw) if c[0] != 0xFE]
        assert commands(encoded) == commands(bytes.fromhex(row['source_hex']))
        assert row['references']
        assert all(page.split(b'\xfa')[0].count(b'\xfe') <= 1 for page in encoded.split(b'\xfb'))
        assert all(b'\xfe' not in part for page in encoded.split(b'\xfb') for part in page.split(b'\xfa')[1:])


def test_prices_and_canonical_names_are_preserved():
    for row in AUDIT['entries'][63:]:
        if row['index'] == 155:
            assert row['portuguese'].startswith('Cancelar<')
        else:
            assert row['portuguese'] == row['english']
    rows = AUDIT['entries']
    assert 'grátis' in rows[39]['portuguese'] and 'amanhã' in rows[45]['portuguese']
    assert all(name in rows[6]['portuguese'] for name in ('Battle', 'Tower', 'Mine', 'Circus'))
    assert 'Ataque Especial' in rows[59]['portuguese']
    assert 'senhorita' == rows[62]['portuguese']


def test_finalizer_runs_after_repairs():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_85') == 1
    assert all(patches.index(p) < patches.index('batch_85') for p in ('inline', 'font', 'repoint_stale'))


def test_audit_matches_reference_sources():
    import re

    def read(path):
        return {int(m[1], 16): m[2] for line in path.read_text().splitlines()
                if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}

    english = read(ROOT / 'languages/en/combined_en.txt')
    french = read(ROOT / 'languages/fr/combined_fr.txt')
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['english'] == english[offset]
        assert row['french_reference'] == french.get(offset, '')
