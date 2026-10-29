"""Gardes du lot figé ES-002 : couverture, commandes binaires et budgets."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined, _normalize_text
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
REPORT = json.loads((ROOT / 'docs/analysis/es/es002_traitement.json').read_text())
ENTRIES = REPORT['entrees']
COMBINED, _ = _load_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')


def test_es002_couvre_exactement_le_lot_contractuel() -> None:
    """Une omission ou un doublon ne peut se cacher derrière un simple total."""
    lot = next(x for x in json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())
               if x['id'] == 'ES-002')
    assert len(ENTRIES) == len({x['offset'] for x in ENTRIES}) == 374
    assert {x['offset'] for x in ENTRIES} == set(lot['offsets'])
    assert all(x['traitement'] in {'traduit', 'importé', 'conservé', 'exclu'}
               and x['justification'] for x in ENTRIES)


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda x: x['offset'])
def test_es002_preserve_commandes_et_exclusions(entry: dict) -> None:
    """Compare les arguments complets aux octets EN, pas aux marqueurs du CSV."""
    offset = int(entry['offset'], 16)
    if entry['traitement'] in {'conservé', 'exclu'}:
        assert entry['traduction'] is None
        return
    expected = _normalize_text(entry['traduction'])
    assert COMBINED[offset] == expected
    encoded = TextEncoder.encode_pokemon(expected, skip_aliases=SPANISH_GLYPH_CHARS)
    source = bytes.fromhex(entry['en_complet_hex'])
    assert _extract_control_sequences_from_raw(encoded) == _extract_control_sequences_from_raw(source)
    assert len(encoded) <= 512
    assert max(line_widths(expected)) <= 192
    if entry.get('cellule'):
        assert len(encoded) <= entry['cellule']['stride']


def test_es002_objet_long_et_joueur_maximal_tiennent() -> None:
    """Trainer Catalogue fait 95 px, au-delà du buffer fictif de 54 px."""
    text = COMBINED[0x001A5218].split('\n')[0]
    assert line_widths(text)[0] + (95 - 54) <= 192
