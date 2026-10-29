"""PT-12 : preuves binaires des consommateurs et largeurs des vraies polices."""
from __future__ import annotations

import hashlib
import importlib
import re
import struct

import pytest

from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt12 import ROOT, audit, encoded

pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes]:
    """Charge les ROMs réelles sans modifier les sources ni les bundles."""
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())


def test_every_live_consumer_delivers_exact_text(roms: tuple[bytes, bytes]) -> None:
    source, built = roms
    assert hashlib.sha256(source).hexdigest() == audit()['source_sha256']
    assert hashlib.sha256(built).hexdigest() == audit()['built_sha256']
    for row in audit()['entries']:
        offset = int(row['offset'], 16)
        refs = [hex(m.start()) for m in re.finditer(re.escape(struct.pack('<I', offset + 0x08000000)), source)]
        assert refs == row['source_sites']
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        if row['status'] == 'exception':
            assert not refs
            continue
        expected = encoded(row)
        for site, recorded in zip(row['live_sites'], row['targets']):
            target = struct.unpack_from('<I', built, int(site, 16))[0] - 0x08000000
            assert target == int(recorded, 16)
            assert 0 <= target < len(built), (row['offset'], site)
            assert built[target:target + len(expected)] == expected, (row['offset'], site, hex(target))
    assert built[0x3e04b0:0x3e06b8] == source[0x3e04b0:0x3e06b8]
    for site in audit()['rejected_sites']:
        start = int(site, 16)
        assert built[start:start + 4] == source[start:start + 4], site


def test_idempotence_and_atomic_source_validation(roms: tuple[bytes, bytes]) -> None:
    from languages.pt.patches.batch_12 import apply

    source, built = roms
    candidate = bytearray(built)
    stats = apply(candidate, source)
    assert stats == {'verified': 263, 'relocated': 0}
    assert candidate == built
    wrong = bytearray(source)
    wrong[0x416a3a] ^= 1
    with pytest.raises(ValueError, match='préimage EN différente'):
        apply(candidate, bytes(wrong))
    assert candidate == built


def test_expanded_variables_fit_the_real_font_windows(roms: tuple[bytes, bytes]) -> None:
    _, built = roms
    builder = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    for row in audit()['entries']:
        if row['status'] == 'exception':
            continue
        offset = int(row['offset'], 16)
        text = row['portuguese'].replace(r'\n', '\n')
        def expand(match: re.Match, offset: int = offset) -> str:
            code = int(match[1], 16)
            if code == 1:
                return 'WWWWWWW'  # Nom joueur, sept caractères.
            if offset in {0x416f27, 0x417017} and code == 3:
                return '999'
            if offset == 0x417032 and code == 3:
                return 'Defesa Especial'
            if offset == 0x4177c5 and code == 3:
                return '999'
            return 'WWWWWWWWWW' if code == 2 else 'WWWWWWWWWWWWW'
        text = re.sub(r'<0xFD><0x([0-9A-F]{2})>', expand, text)
        raw = TextEncoder.encode_pokemon(text, strict=True)
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            x = 0
            index = 0
            while index < len(raw) - 1:
                value = raw[index]
                if value in (0xFE, 0xFA, 0xFB):
                    x = 0
                    index += 1
                elif value == 0xFC:
                    command = raw[index + 1]
                    count = builder.FC_ARG_COUNTS.get(command, 0)
                    if command == 0x13:
                        x = raw[index + 2]  # Déplacement horizontal absolu du prix.
                    index += 2 + count
                elif value in (0x53, 0x54):
                    x += 8  # Deux tuiles du glyphe PKMN.
                    index += 1
                else:
                    x += built[widths + value]
                    index += 1
                assert x <= 216, (row['offset'], font.name, text, x)
