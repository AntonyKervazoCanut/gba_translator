"""Écrit les badges graphiques de statut à partir de lettres 4×6."""
from pathlib import Path
from typing import ClassVar

from languages.fr.patches.font import lz77_compress, lz77_decompress


class StatusBadgePatcher:
    """Préserve les bordures et palettes des huit cellules de chaque bloc."""

    BLOCKS = (0xB1E11C, 0xB1E280, 0xE82EA0, 0xE9BF48)
    SLOT_KEYS: ClassVar[dict[int, str]] = {0: "poison", 1: "paralysis", 2: "sleep", 3: "freeze", 4: "burn", 6: "faint"}

    @classmethod
    def apply(cls, path: Path, labels: dict[str, str], letters: dict[str, tuple[str, ...]]) -> None:
        """Redessine les six statuts, en refusant les débordements de bloc."""
        rom = bytearray(path.read_bytes())
        Path(str(path) + ".bak").write_bytes(rom)
        for offset in cls.BLOCKS:
            result = lz77_decompress(rom, offset)
            if result is None or len(result[0]) != 1024:
                raise ValueError(f"Bloc de statuts invalide : {offset:#x}")
            data, old_size = result
            tiles = bytearray(data)
            for slot, key in cls.SLOT_KEYS.items():
                label = labels[key]
                if len(label) != 3:
                    raise ValueError(f"Statut hors budget : {label}")
                start = slot * 128
                bg = tiles[start + 36] & 15
                for y in range(1, 7):
                    pixels = [bg] * 16
                    for n, char in enumerate(label):
                        for x, ink in enumerate(letters[char][y - 1]):
                            pixels[1 + n * 5 + x] = 2 if ink == "1" else bg
                    for x in range(0, 16, 2):
                        tile, column = divmod(x, 8)
                        index = start + (tile + 1) * 32 + y * 4 + column // 2
                        tiles[index] = pixels[x] | pixels[x + 1] << 4
            compressed = lz77_compress(bytes(tiles), vram_safe=True)
            tail = rom[offset + old_size:offset + len(compressed)]
            if any(byte not in (0, 255) for byte in tail):
                raise ValueError(f"Badge hors budget à {offset:#x}")
            rom[offset:offset + len(compressed)] = compressed
        path.write_bytes(rom)
