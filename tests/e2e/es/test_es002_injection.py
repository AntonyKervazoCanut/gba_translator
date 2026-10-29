"""Compare les 374 décisions ES-002 aux octets des vrais consommateurs ROM."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from scripts.apply_combined_fr import _load_combined
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.collision_check import live_target
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

pytestmark = pytest.mark.rom
ROOT = Path(__file__).resolve().parents[3]
ENTRIES = json.loads((ROOT / 'docs/analysis/es/es002_traitement.json').read_text())['entrees']


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes, dict]:
    """Charge les binaires locaux une seule fois, sans altérer les sources."""
    combined, _ = _load_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes(), combined)


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda x: x['offset'])
def test_es002_consommateurs_vivants(entry: dict, roms: tuple[bytes, bytes, dict]) -> None:
    """Un build vert ne suffit pas : aucun fallback ni argument perdu accepté."""
    english, built, combined = roms
    offset = int(entry['offset'], 16)
    raw = bytes.fromhex(entry['en_complet_hex'])
    assert english[offset:offset + len(raw)] == raw
    if entry['traitement'] == 'exclu':
        assert offset not in combined
        return
    sites = [int(site, 16) for site in entry['referents_en']]
    targets = [live_target(built, site) for site in sites] or [offset]
    expected = (TextEncoder.encode_pokemon(combined[offset], skip_aliases=SPANISH_GLYPH_CHARS)
                if entry['traduction'] else raw)
    for target in targets:
        assert target is not None
        actual = built[target:built.index(0xFF, target) + 1]
        # FE et espaces peuvent être rééquilibrés par le constructeur ; aucune
        # lettre ou commande n'est retirée de cette comparaison.
        def normalize(text: bytes) -> bytes:
            return re.sub(b'[\x00\xfe]+', b'\x00', text).strip(b'\x00')
        assert normalize(actual) == normalize(expected), (entry['offset'], hex(target))
        assert _extract_control_sequences_from_raw(actual) == _extract_control_sequences_from_raw(raw)
        if entry.get('cellule'):
            assert target == offset
            assert len(actual) <= entry['cellule']['stride']
