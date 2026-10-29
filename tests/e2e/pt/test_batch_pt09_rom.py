"""PT-09 : chaque consommateur livre la traduction exacte dans la ROM finale."""
from __future__ import annotations

import re
import struct

import pytest

from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt09 import ROOT, controls, entries, translations

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes]:
    """Charge les deux ROMs réelles, sans matérialiser de bundle distribué."""
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())


def test_all_consumers_and_structures(roms: tuple[bytes, bytes]) -> None:
    source, built = roms
    actual = translations()
    failures = []
    for row in entries():
        offset = int(row['offset'], 16)
        refs = [m.start() for m in re.finditer(
            re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert refs == [int(s, 16) for s in row['source_sites']]
        assert source[offset:source.index(255, offset) + 1].hex() == row['source_hex']
        if row['status'] == 'exception':
            assert not refs
            # Un suffixe interne peut être réécrit avec son parent vivant.
            if offset not in {0x3FB284, 0x3FB827, 0x3FB9D6, 0x3FBA2C}:
                assert built[offset:offset + len(bytes.fromhex(row['source_hex']))] == bytes.fromhex(row['source_hex'])
            continue
        encoded = TextEncoder.encode_pokemon(actual[offset].replace(r'\n', '\n'), strict=True)
        assert controls(encoded) == controls(bytes.fromhex(row['source_hex']))
        for site in [int(s, 16) for s in row['live_sites']]:
            target = struct.unpack_from('<I', built, site)[0] - 0x08000000
            assert 0 <= target < len(built), (row['offset'], hex(site))
            if built[target:target + len(encoded)] != encoded:
                failures.append((row['offset'], hex(site), hex(target),
                                 built[target:target + len(encoded)].hex(), encoded.hex()))
            if offset < 0x3EED08:
                # Ne jamais écraser le tri ni le drapeau d'un mot Easy Chat.
                assert source[site + 4:site + 12] == built[site + 4:site + 12]
    assert not failures, failures
    # Faux pointeur : les données graphiques doivent rester intactes.
    assert built[0x54482E:0x544832] == source[0x54482E:0x544832]
    # Le moteur de combat consulte toujours la même table de pointeurs.
    assert built[0x3ECED0:0x3ECF10] == source[0x3ECED0:0x3ECF10]


def test_real_font_widths_with_expanded_buffers(roms: tuple[bytes, bytes]) -> None:
    _, built = roms
    for row in entries():
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        # Nom Pokémon de dix lettres et préfixe anglais conservé hors du lot.
        text = row['portuguese'].replace(r'\n', '\n')
        def expand(match: re.Match) -> str:
            code = int(match[1], 16)
            if code in {0x0F, 0x10, 0x11, 0x13, 0x2A}:
                return 'Foe CHARMANDER'
            if code in {0x06, 0x08, 0x1D}:
                return 'CHARMANDER'
            if code == 0x00:
                return 'Ataque'
            if code in {0x14, 0x19, 0x1A}:
                return 'Intimidate'
            if code == 0x38:
                return 'adversária'
            return '999'
        # Bornes structurelles et budget statique vérifiés indépendamment du
        # moteur ; la preuve Playwright vérifie aussi un nom long en msgbox.
        expanded = re.sub(r'<0xFD><0x([0-9A-F]{2})>', expand, text)
        expanded = re.sub(r'<0xFC><0x08><0x20>|<0xFC><0x0A>', '', expanded)
        expanded = expanded.replace('<0x00>', ' ')
        expanded = expanded.replace('<0xFA>', '\n').replace('<0xFB>', '\n')
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in expanded.splitlines():
                raw = TextEncoder.encode_pokemon(line, strict=True)[:-1]
                budget = 102 if offset < 0x3EED08 else 216
                assert sum(built[widths + b] for b in raw) <= budget, (row['offset'], font, line)


def test_final_patch_is_idempotent_and_rejects_wrong_source(roms: tuple[bytes, bytes]) -> None:
    from languages.pt.patches.batch_09 import definitions
    from src.core.structured_text import StructuredTextPatch

    source, built = roms
    patch = StructuredTextPatch(source, definitions(), ROOT / 'languages/pt/combined_pt.txt')
    candidate = bytearray(built)
    assert patch.apply(candidate) == {'verified': 36, 'relocated': 0}
    assert candidate == built
    altered = bytearray(source)
    offset = int(definitions()[0]['offset'], 16)
    altered[offset] ^= 1
    invalid = StructuredTextPatch(bytes(altered), definitions(), ROOT / 'languages/pt/combined_pt.txt')
    with pytest.raises(ValueError, match='préimage EN différente'):
        invalid.apply(candidate)
    assert candidate == built
