"""Le vocabulaire de Coupe emploie arbuste, au singulier comme au pluriel."""

import re
from pathlib import Path


def test_french_translation_has_no_skinny_tree_literal() -> None:
    source = Path(__file__).resolve().parents[1] / 'languages/fr/combined_fr.txt'

    text = source.read_text(encoding='utf-8')

    assert not re.search(r'\barbres?\s+maigres?\b', text, re.IGNORECASE)
