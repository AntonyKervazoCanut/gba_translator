"""PT-88 : missions secondaires, périmètre et contrôles exacts."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]


def audit():
    """Retourne le bilan des 300 clés du manifeste."""
    return json.loads((ROOT / 'languages/pt/data/pt88_audit.json').read_text())


def test_closed_manifest_and_exact_protections():
    rows = audit()['entries']
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-88')
    assert len(rows) == 300
    assert sum(r['status'] == 'translated' for r in rows) == 290
    assert [r['offset'] for r in rows] == manifest
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['scene'] and row['source_hex']
        if row['status'] == 'exception':
            assert not row['references'] and offset not in texts
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        text = texts[offset].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(text, strict=True)
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert len(raw) == row['encoded_bytes']
        controls = lambda b: [c for c in commands(b) if c != b'\xfe']
        assert controls(raw) == controls(bytes.fromhex(row['source_hex']))
        assert line_widths(text) == row['line_widths']
        assert max(row['expanded_widths']) <= row['pixel_budget']
        if row['layout'] == 'mission':
            assert text.count('\n') <= 2
        if row['index'] < 100:
            assert chr(34) not in text
        if row['layout'] == 'dialogue':
            for page in text.split('<0xFB>'):
                for n, segment in enumerate(page.split('<0xFA>')):
                    assert segment.count('\n') <= (1 if n == 0 else 0), row['offset']


def test_quest_progress_and_canonical_names():
    rows = audit()['entries']
    assert [rows[i]['portuguese'].split('prender ')[1][0] for i in range(220, 224)] == list('5432')
    assert rows[200]['portuguese'] == 'Swords of Justice'
    assert rows[217]['portuguese'] == 'Terror Granbull'
    assert rows[145]['portuguese'] == 'Science Society'
    assert 'Dynamax' in rows[186]['portuguese']
    assert len(rows[288]['source_hex']) // 2 == 722
    assert 'Super Cube' in rows[288]['portuguese']


def test_finalizer_after_repoint_and_font():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_88') == 1
    assert patches.index('batch_88') > patches.index('font')
    assert patches.index('batch_88') > patches.index('repoint_stale')
