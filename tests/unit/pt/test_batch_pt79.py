"""PT-79 : panneaux, conseils, S.S. Marine, Stat Scanner et Tarmigan."""
import json
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]


def audit():
    """Charge le bilan individuel des 300 offsets du manifeste."""
    return json.loads((ROOT / 'languages/pt/data/pt79_audit.json').read_text())


def test_manifest_protections_controls_and_pages():
    rows = audit()['entries']
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-79')
    texts = entries()
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == manifest
    assert len(rows) == 300
    assert [r['index'] for r in rows if r['status'] == 'exception'] == [232]
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
        measured = row['expanded_widths']
        if 225 <= row['index'] <= 231:
            measured = measured[:1]  # La routine utilise la police small, font0.
        assert max(measured) <= row['pixel_budget']
        if row['layout'] == 'dialogue':
            for page in text.split('<0xFB>'):
                for n, segment in enumerate(page.split('<0xFA>')):
                    assert segment.count('\n') <= (1 if n == 0 else 0), row['offset']


def test_gameplay_advice_and_truncated_sources_are_complete():
    rows = audit()['entries']
    assert '10 turnos' in rows[141]['portuguese']
    assert '100' in rows[141]['portuguese'] and 'Dusk Ball' in rows[141]['portuguese']
    assert 'uma única vez' in rows[120]['portuguese']
    assert 'Uma única vez' in rows[121]['portuguese']
    assert 'cinco vezes' in rows[148]['portuguese']
    assert 'The Shadows' in rows[187]['portuguese']
    assert 'Zeph começou' in rows[187]['portuguese']
    assert 'ADM' in rows[298]['portuguese']
    assert 'Habilidade oculta' in rows[296]['portuguese']
    assert 'adormecidos' in rows[296]['portuguese']
    for index in (141, 185, 187, 298):
        assert len(rows[index]['english_full']) > len(rows[index]['english_reference'])
    assert rows[263]['portuguese'] == 'Tarmigan Town D'
    assert rows[264]['portuguese'] == 'Tarmigan Town N'


def test_finalizer_runs_after_font_and_repointing():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_79') == 1
    assert patches.index('batch_79') > patches.index('font')
    assert patches.index('batch_79') > patches.index('repoint_stale')
