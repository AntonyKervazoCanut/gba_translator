"""PT-20 : couverture fermée, terminologie et budgets des textes Borrius."""
import json
from pathlib import Path

import pytest
import yaml

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import (
    _extract_control_sequences_from_raw,
    _normalize_text,
)
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt20_audit.json').read_text())
TEXTS, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')


def test_exact_scope_and_exception_justifications():
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-20')
    guards = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    protected = {int(e['offset'], 16): e['expected'] for e in guards['entries']}
    assert [r['offset'] for r in AUDIT['entries']] == manifest
    assert len(manifest) == 288
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        assert row['reason']
        if row['status'] == 'exception':
            assert offset not in TEXTS
            assert not row['references'] or offset in (0x74037D, 0x745132)
        else:
            assert row['references']
            assert TEXTS[offset] == _normalize_text(row['portuguese'])
            assert protected[offset] == row['portuguese']


@pytest.mark.parametrize('row', [r for r in AUDIT['entries'] if r['status'] != 'exception'],
                         ids=lambda r: r['offset'])
def test_commands_pages_and_width(row):
    text = TEXTS[int(row['offset'], 16)]
    raw = TextEncoder.encode_pokemon(text, strict=True)
    source = bytes.fromhex(row['source_hex'])
    def commands(data):
        return [s for s in _extract_control_sequences_from_raw(data) if s[0] != 0xFE]
    assert commands(raw) == commands(source)
    assert len(raw) == row['encoded_bytes']
    assert raw[-1] == 0xFF and 0xFF not in raw[:-1]
    assert line_widths(text) == row['line_widths']
    assert max(line_widths(text), default=0) <= row['max_width']
    # Deux lignes par segment avant chaque attente/scroll, sauf la description objet.
    if row['offset'] != '0x728430':
        import re
        assert all(part.count('\n') <= 1 for part in re.split(r'<0xF[AB]>', text))


def test_terms_story_and_distinct_expressways():
    assert 'HM Cut' in TEXTS[0x745A55] and 'Darkness Badge' in TEXTS[0x745A55]
    assert TEXTS[0x721438] == 'KBT Expressway'
    assert 'SES' in TEXTS[0x745D52]
    assert 'Cinder Volcano' in TEXTS[0x750370]
    assert 'The Shadows' in TEXTS[0x74AE91]
    assert all(term in TEXTS[0x741625] for term in ('Sombrio', 'Lutador', 'Inseto', 'Fada'))
    assert 'cinco' in TEXTS[0x7525D0] and 'saia e entre novamente' in TEXTS[0x7525D0]
    assert '16 anos' in TEXTS[0x74FC26]
    assert 'anéis' in TEXTS[0x74FB43]
    assert 'Poké Ball' in TEXTS[0x753510]  # Mécanique fangame, ne pas corriger en lancer.


def test_finalizer_follows_repairs_and_does_not_target_scripts_or_connections():
    steps = yaml.safe_load((ROOT / 'languages/pt/lang.yaml').read_text())['patches']
    assert steps.count('batch_20') == 1
    for step in ('inline', 'repair_lz77', 'repair_localized_lz77', 'repoint_stale'):
        assert steps.index(step) < steps.index('batch_20')
    rows = [r for r in AUDIT['entries'] if r['status'] != 'exception']
    offsets = {int(r['offset'], 16) for r in rows}
    assert not offsets.intersection({0x721340, 0x72134C, 0x74037D, 0x745132})


def test_live_suffixes_are_repaired_as_standalone_messages():
    assert TEXTS[0x741693].startswith('Use Pokémon fortes')
    assert TEXTS[0x7416B5].startswith('Use Pokémon Inseto')
    assert TEXTS[0x741717].startswith('Você enfrentou')
    assert TEXTS[0x7417CE].startswith('Libere sua fúria')
    assert TEXTS[0x74C34E] == 'Chegue ao topo.'
    assert TEXTS[0x74C367].startswith('Protective Pads')
    for row in AUDIT['entries']:
        if 'context_offset' in row:
            assert int(row['context_offset'], 16) < int(row['offset'], 16)
            assert row['references'] and 'corrompu' in row['reason']


def test_rescued_child_dialogue_is_safe_for_both_genders():
    text = TEXTS[0x754900]
    assert '\n<0xFD><0x02>, você me salvou!' in text
    assert 'O <0xFD>' not in text
