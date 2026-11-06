"""ES-008 : absence de racine exécutable du fragment de liste d'espèces.

Lecture seule de la source et du build : les faux pointeurs dans des ressources
ne doivent pas être confondus avec des consommateurs de texte vivants.
"""
from __future__ import annotations

import hashlib
import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
START, END = 0xE6648, 0xE6780
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module', params=[
    'input/roms/englishrom.gba', 'output/roms/GenedRom-es-maint.gba',
], ids=['source', 'es-maint'])
def rom(request: pytest.FixtureRequest) -> bytes:
    """Exige les deux artefacts réels, sans fabriquer ni ignorer un build absent."""
    return (ROOT / request.param).read_bytes()


def test_party_routine_preimage_and_sole_text_consumer(rom: bytes) -> None:
    """Le code, ses buffers et la terminaison du fragment restent intacts."""
    assert hashlib.sha256(rom[START:END]).hexdigest() == (
        '2c05409f41416a6c294399fd29fb66515975064d1757dddc8e294bb0821b0e45'
    )
    # Retour de la fonction précédente : aucune entrée par chute séquentielle.
    assert rom[0xE6632:START].hex() == '38bc9846a146aa46f0bc01bc0047c4204008ffff0000'
    assert rom[0x3FE864:0x3FE868] == bytes.fromhex('00dde7ff')
    assert rom.count(struct.pack('<I', 0x083FE864)) == 1
    assert struct.unpack_from('<I', rom, 0xE674C)[0] == 0x083FE864
    assert struct.pack('<I', 0x083FE865) not in rom
    assert struct.unpack_from('<I', rom, 0xE672C)[0] == 0x02021CD0
    assert struct.unpack_from('<11H', rom, 0x4020C4) == (
        151, 150, 250, 249, 251, 404, 405, 406, 409, 410, 0xFFFF,
    )


def test_absolute_roots_are_only_classified_resource_bytes(rom: bytes) -> None:
    """Cherche toutes les adresses internes, non alignées et miroir ROM inclus."""
    hits = set()
    for mirror in (0x08, 0x0A):
        suffix = bytes((0x0E, mirror))
        cursor = 0
        while (cursor := rom.find(suffix, cursor)) >= 0:
            if cursor >= 2:
                target = int.from_bytes(rom[cursor - 2:cursor + 2], 'little')
                if START <= target & 0x1FFFFFF < END:
                    hits.add((cursor - 2, target))
            cursor += 1

    assert hits == {(0x63A700, 0x080E66AB), (0xBEE198, 0x080E664A)}
    # Le premier motif est au milieu d'un échantillon compressé m4a type 1.
    assert struct.unpack_from('<4I', rom, 0x63A398) == (1, 10764288, 0, 6018)
    assert struct.unpack_from('<I', rom, 0x19EAC94)[0] == 0x0863A398
    assert 0x63A398 + 16 < 0x63A700 < 0x63A398 + 16 + 6018 // 2
    # Le second est dans une ressource LZ77, pas une table de fonctions.
    from languages.fr.patches.font import lz77_decompress

    compressed_offset = 0xBEDC3C
    decoded, size = lz77_decompress(rom, compressed_offset)
    assert (len(decoded), size) == (12000, 0x1826)
    assert compressed_offset < 0xBEE198 < compressed_offset + size


def test_no_relative_thumb_entry_to_any_instruction(rom: bytes) -> None:
    """Examine BL, B, Bcc et ADR vers tout le corps, pas seulement son entrée."""
    hits = []
    for address in range(0, len(rom) - 4, 2):
        if START <= address < END:
            continue
        first, second = struct.unpack_from('<HH', rom, address)
        target = None
        if first & 0xF800 == 0xF000 and second & 0xF800 == 0xF800:
            delta = ((first & 0x7FF) << 12) | ((second & 0x7FF) << 1)
            delta -= (1 << 23) if delta & (1 << 22) else 0
            target = address + 4 + delta
        elif first & 0xF800 == 0xE000:
            delta = (first & 0x7FF) << 1
            delta -= 0x1000 if delta & 0x800 else 0
            target = address + 4 + delta
        elif first & 0xF000 == 0xD000 and first & 0xF00 < 0xE00:
            delta = (first & 0xFF) << 1
            delta -= 0x200 if delta & 0x100 else 0
            target = address + 4 + delta
        elif first & 0xF800 == 0xA000:
            target = ((address + 4) & ~3) + (first & 0xFF) * 4
        if target is not None and START <= target < END:
            hits.append((address, target))

    assert hits == []


def test_arm_branch_match_is_text_not_an_entry(rom: bytes) -> None:
    """Un scan ARM naïf rencontre les octets du texte « Bright light »."""
    hits = []
    for address in range(0, len(rom) - 4, 4):
        word = struct.unpack_from('<I', rom, address)[0]
        if word & 0x0E000000 != 0x0A000000:
            continue
        delta = (word & 0xFFFFFF) << 2
        delta -= (1 << 26) if delta & (1 << 25) else 0
        target = address + 8 + delta
        if START <= target < END and not START <= address < END:
            hits.append((address, target))

    assert hits == [(0x96CC7C, 0xE6774)]
    assert rom[0x96CC7C:0x96CC89] == bytes.fromhex('BC E6 DD DB DC E8 00 E0 DD DB DC E8 00')
