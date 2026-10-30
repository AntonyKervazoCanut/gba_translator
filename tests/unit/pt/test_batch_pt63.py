"""PT-63 : périmètre exact, intégrité des pages et formats métier."""
import json
import re
from pathlib import Path

import yaml

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.structured_text import StructuredTextPatch
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt63_audit.json').read_text())


def test_manifest_protections_and_exact_control_order():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-63')
    texts = {k: v.replace(r'\n', '\n') for k, v in StructuredTextPatch(
        b'', [], ROOT / 'languages/pt/combined_pt.txt').texts.items()}
    guards = {int(r['offset'], 16): r['expected'] for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 299
    assert sum(r['status'] == 'exception' for r in AUDIT['entries']) == 8
    assert sum(r['status'] == 'retained' for r in AUDIT['entries']) == 19
    for row in AUDIT['entries']:
        off = int(row['offset'], 16)
        assert row['reason'] and row['source_hex']
        if row['status'] == 'exception':
            assert not row['references'] and off not in texts and row['context_hex']
            continue
        assert texts[off] == guards[off].replace(r'\n', '\n') == row['portuguese'].replace(r'\n', '\n')
        raw = TextEncoder.encode_pokemon(texts[off], strict=True)
        assert raw[-1] == 255 and 255 not in raw[:-1]
        assert len(raw) == row['encoded_bytes']
        commands = lambda b: [s for s in _extract_control_sequences_from_raw(b) if s[0] != 254]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        assert line_widths(texts[off]) == row['line_widths']
        # Le modèle générique réserve 54px même à un compteur ou au suffixe s.
        # Les budgets réels, avec tampons contextualisés, sont testés dans les cinq polices.
        assert max(row['line_widths']) <= row['max_width']
        assert row['native_max_width'] <= 198


def test_window_geometry_and_complete_long_dialogues():
    for row in AUDIT['entries']:
        if row['status'] == 'exception':
            continue
        text = row['portuguese']
        if row['kind'] == 'mission':
            assert 1 < len(text.split(r'\n')) <= 3
        elif row['kind'] in ('label', 'menu'):
            assert r'\n' not in text
        elif row['kind'] == 'dialogue':
            parts = re.split(r'(<0xF[AB]>)', text)
            for i in range(0, len(parts), 2):
                assert len(parts[i].split(r'\n')) <= (1 if i and parts[i - 1] == '<0xFA>' else 2)
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    assert texts[0x1EFEDA8].endswith('mas poderia batalhar comigo?')
    assert texts[0x1F00D23].endswith('tenham a chance de usá-la.')
    assert 'Defog' in texts[0x1F01BEF] and 'neblina' in texts[0x1F01BEF]
    assert 'Habilidade Oculta' in texts[0x1F027CD]
    assert 'salvamentos manuais' in texts[0x1F01867]
    assert 'PS' in texts[0x1F047E3] and '¥550' in texts[0x1F047E3]
    assert 'dez pontos' in texts[0x1F04EDD]
    assert texts[0x1F031C8] == 'Epidimy Town'
    assert texts[0x1F04760] == 'Fallshore City'


def test_finalizer_order():
    patches = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert patches.count('batch_63') == 1
    assert all(patches.index(step) < patches.index('batch_63') for step in
               ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale', 'font'))
