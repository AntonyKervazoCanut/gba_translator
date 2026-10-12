"""Garde les pages du récit d'Aros dans la boîte de dialogue (#203)."""
import re
from pathlib import Path

from scripts.check_translation_integrity import load_last_wins
from src.core.dialogue_linewrap import DEFAULT_MAX_LINE_WIDTH, line_width

ROOT = Path(__file__).resolve().parents[2]


def test_crateris_story_fits_dialogue_pages():
    texts, _ = load_last_wins(ROOT / 'languages/fr/combined_fr.txt')
    story = texts[0x1EEE8BE]

    # Les commandes de couleur ne consomment aucune largeur visible.
    visible = re.sub(r'\{COLOR\}.', '', story)
    for page in visible.split(r'\p'):
        lines = re.split(r'\\[nl]', page)
        assert all(line.strip() for line in lines), 'Page ou ligne vide'
        assert all(line_width(line) <= DEFAULT_MAX_LINE_WIDTH for line in lines), lines
        breaks = re.findall(r'\\[nl]', page)
        assert breaks == ([r'\n'] + [r'\l'] * (len(breaks) - 1) if breaks else [])
