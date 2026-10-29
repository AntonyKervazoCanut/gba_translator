"""PT-29 : périmètre exact, ruptures, noms conservés et règles d'Antisis."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands
from tests.unit.pt.test_batch_pt10 import entries

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt29_audit.json').read_text())


def test_manifest_protection_and_exact_control_flow():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-29')
    rows = AUDIT['entries']
    texts = entries()
    guards = {int(r['offset'], 16): r.get('expected_raw', r['expected']) for r in yaml.safe_load(
        (ROOT / 'languages/pt/protected_entries.yaml').read_text())['entries']}
    assert [r['offset'] for r in rows] == offsets
    assert len(rows) == 288
    assert sum(r['status'] == 'translated' for r in rows) == 264
    assert sum(r['status'] == 'retained' for r in rows) == 3
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english_reference']
        if row['status'] == 'exception':
            assert offset not in texts
            # Un pointeur graphique vivant ne transforme pas les pixels en texte.
            assert not row['references'] or offset == 0x827F30
            continue
        assert texts[offset] == guards[offset] == row['portuguese']
        raw = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
        assert len(raw) == row['encoded_bytes'] <= 512
        assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
        assert commands(raw) == commands(bytes.fromhex(row['source_hex']))
        widths = [line_width(line) for line in re.split(r'<0xF[AB]>|\\n', texts[offset])]
        assert widths == row['line_widths'] and max(widths) <= 192


def test_antisis_mechanics_and_terminology():
    texts = entries()
    for offset, word in [(0x7FDCC4, '70'), (0x7FDCC4, 'Rock Climb'),
                         (0x7FDDAA, 'Drain Punch'), (0x7FDDAA, 'PS'),
                         (0x7FA7EC, '35'), (0x7FA7EC, 'Venenoso'),
                         (0x7F981F, 'SES Expressway'), (0x7FB2D9, 'dois Pokémon'),
                         (0x7F518D, 'Cinder Volcano'), (0x7F6B6D, 'The Shadows')]:
        assert word in texts[offset].replace(r'\n', ' ')
    rules = texts[0x7FD645].replace(r'\n', ' ')
    assert 'três Treinadores seguidos' in rules and 'um só Pokémon' in rules
    assert all(t in rules for t in ['Voador', 'Psíquico', 'Fada'])
    assert [texts[o] for o in [0x7FD4AC, 0x7FD4B2, 0x7FD4B8]] == ['Entrar', 'Regras', 'Sair']
    assert texts[0x7F57EC] != texts[0x7F5821]
    assert texts[0x7FB7E0] != texts[0x7FB835]
    assert texts[0x87622C] == 'Master Ball' and texts[0x876258] == 'Ultra Ball'
    assert texts[0x834AE7] == 'VISOR EV-IV'


def test_finalizer_runs_after_generic_repairs():
    config = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())
    assert config['patches'].count('batch_29') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert config['patches'].index(step) < config['patches'].index('batch_29')
