"""PT-06 : contrôle des octets livrés et des consommateurs sur ROM réelle."""
import json
import re
import struct
from pathlib import Path

import pytest

from src.core.font_glyphs import LATIN_FONTS
from src.core.text_codec import TextEncoder
from tests.unit.pt.test_batch_pt06 import (
    FRAGMENTS,
    LEGACY_ITEMS,
    batch_offsets,
    exceptions,
    translations,
)

ROOT = Path(__file__).resolve().parents[3]
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def roms():
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes())


def sites(source, offset):
    needle = struct.pack('<I', offset + 0x08000000)
    return [m.start() for m in re.finditer(re.escape(needle), source)]


def test_every_active_pointer_delivers_the_exact_text(roms):
    source, built = roms
    report = json.loads((ROOT / 'docs/analysis/24_PT_BR_PT06.json').read_text())
    rows = {int(row['offset'], 16): row for row in report['entries']}
    failures = []
    for offset, text in translations().items():
        expected = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        original = source[offset:source.index(b'\xff', offset) + 1]
        assert expected.count(b'\xfe') == original.count(b'\xfe'), hex(offset)
        assert not any(byte in original for byte in [0xFC, 0xFD, 0xFA, 0xFB])
        refs = sites(source, offset)
        assert refs, hex(offset)
        assert rows[offset]['source_sites'] == [hex(site) for site in refs]
        # Les adresses du bilan décrivent son build historique. L'allocateur
        # peut les déplacer quand un autre lot est ajouté : le contrat porte
        # sur chaque consommateur et les octets à sa cible vivante ci-dessous.
        assert len(rows[offset]['targets']) == len(refs), hex(offset)
        if offset < 0x3DF7E8:
            assert any(0x876088 <= site < 0x880000
                       and (site - 0x876088) % 44 == 0 for site in refs), hex(offset)
        for site in refs:
            target = struct.unpack_from('<I', built, site)[0] - 0x08000000
            assert 0 <= target < len(built), (hex(offset), hex(site))
            if built[target:target + len(expected)] != expected:
                failures.append((hex(offset), hex(site), hex(target)))
        # Le budget est mesuré avec les vraies largeurs finales des cinq polices.
        for font in LATIN_FONTS:
            _, widths = font.offsets(built)
            for line in expected[:-1].split(b'\xfe'):
                budget = 186 if offset < 0x3E7F35 else 102
                assert sum(built[widths + byte] for byte in line) <= budget, hex(offset)
    assert not failures, failures


@pytest.mark.parametrize('damage', ['pointer', 'text'])
def test_live_delivery_guard_rejects_corruption_after_relocation(roms, damage):
    source, built = roms
    offset = next(iter(translations()))
    site = sites(source, offset)[0]
    corrupted = bytearray(built)
    if damage == 'pointer':
        struct.pack_into('<I', corrupted, site, 0x08000000 + len(built))
    else:
        target = struct.unpack_from('<I', corrupted, site)[0] - 0x08000000
        corrupted[target] ^= 1
    with pytest.raises(AssertionError):
        test_every_active_pointer_delivers_the_exact_text((source, bytes(corrupted)))


def test_exceptions_are_not_silently_claimed_as_translated(roms):
    source, built = roms
    # Les vraies tables CFRU n'utilisent aucune des 43 descriptions CT/CS
    # historiques. L'absence de référent seule ne prouverait pas ce point.
    move_targets = {struct.unpack_from('<I', source, 0x99F190 + n * 4)[0]
                    - 0x08000000 for n in range(893)}
    item_base = struct.unpack_from('<I', source, 0x9A8D8)[0] - 0x08000000
    assert item_base == 0x876200
    item_targets = {struct.unpack_from('<I', source, item_base + n * 44 + 20)[0]
                    - 0x08000000 for n in range(1000)}
    assert not (move_targets | item_targets) & exceptions()
    for offset in exceptions():
        end = source.index(b'\xff', offset) + 1
        assert built[offset:end] == source[offset:end], hex(offset)
        refs = sites(source, offset)
        if offset in LEGACY_ITEMS:
            assert len(refs) == 1 and 0x3DB000 < refs[0] < 0x3DF09C
        elif offset in FRAGMENTS:
            assert not refs
        elif offset == 0x3DA477:
            assert refs == [0x653C71]  # Mot non aligné dans les données graphiques.
            assert built[0x653C71:0x653C75] == source[0x653C71:0x653C75]
        else:
            assert not refs, (hex(offset), refs)
    assert len(batch_offsets()) == len(translations()) + len(exceptions())


def test_easy_chat_structures_keep_indices_and_availability(roms):
    source, built = roms
    # Chaque entrée est {pointeur, ordre alphabétique, disponible} : seuls
    # les quatre octets du pointeur peuvent changer, jamais l'index ni le flag.
    for offset in translations():
        if offset < 0x3E7F35:
            continue
        for site in sites(source, offset):
            assert built[site + 4:site + 12] == source[site + 4:site + 12], hex(site)
    # Tables racines des groupes Trainer/Pokémon/Battle/Greetings inchangées.
    assert built[0x3ECED0:0x3ECF10] == source[0x3ECED0:0x3ECF10]
    for literal in [0xBD788, 0xBD7C0, 0xBD84C, 0xBDA38, 0xBDD2C, 0xBE270, 0xBE414]:
        assert struct.unpack_from('<I', built, literal)[0] == 0x083ECED4
