"""Contrôle les textes indépendants ES-007 aux pointeurs du build final."""
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
REPORT = json.loads((ROOT / 'docs/analysis/es/007_TRAITEMENT.json').read_text())
pytestmark = pytest.mark.rom


def test_every_prepared_text_reaches_all_its_live_pointers() -> None:
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    built = (ROOT / 'output/roms/GenedRom-es-maint.gba').read_bytes()
    for entry in REPORT['entries']:
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['preimage_en_hex'])
        assert source[offset:offset + len(raw)] == raw, entry['offset']
        if entry['decision'] != 'traduit':
            if entry.get('text_owners'):
                continue
            assert built[offset:offset + len(raw)] == raw, entry['offset']
            continue
        expected = bytes.fromhex(entry['expected_hex'])
        assert entry['pointer_sites'], entry['offset']
        for site in entry['pointer_sites']:
            site = int(site, 16)
            target = int.from_bytes(built[site:site + 4], 'little') - 0x08000000
            assert 0 <= target <= len(built) - len(expected), entry['offset']
            assert built[target:target + len(expected)] == expected, entry['offset']
    # Occurrence non alignée dans les données audio, sans consommateur texte.
    assert built[0x54482E:0x544832] == source[0x54482E:0x544832]


def test_audited_input_roms_stay_unchanged() -> None:
    """Fige les fixtures ROM ; le témoin FR du ticket reste une preuve ponctuelle.

    Une future correction FR autorisée ne doit pas casser le lot espagnol en
    faisant évoluer légitimement son combined. Les empreintes de ces sources
    dans le rapport décrivent la provenance, pas une interdiction permanente.
    """
    for filename in ('input/roms/englishrom.gba', 'input/roms/spanishrom.gba'):
        expected = REPORT['sources'][filename]
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == expected
