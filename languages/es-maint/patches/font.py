"""Complète les polices compressées ES ; les polices moteur natives sont conservées."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from languages.de.patches.font import (
    FreeSpaceAllocator,
    build_umlaut,
    extract_diaeresis_dots,
    find_font_blocks,
    patch_width_tables,
    repoint_pointers,
)
from languages.fr.patches.font import lz77_compress


def apply_patches(rom: bytearray) -> int:
    """Dessine uniquement Ü/ü dans les blocs référencés réellement textuels."""
    # Certains graphismes passent le test de densité général : exiger aussi
    # les deux paires latines Ë/E et ë/e avant toute écriture.
    blocks = [block for block in find_font_blocks(rom)
              if extract_diaeresis_dots(block.decompressed, 0x08, 0xBF)
              and extract_diaeresis_dots(block.decompressed, 0x1D, 0xD9)]
    if not blocks:
        raise ValueError("Aucune police ES trouvée")
    allocator = FreeSpaceAllocator(rom)
    for block in blocks:
        font = bytearray(block.decompressed)
        for target, base, reference, plain in ((0xF3, 0xCF, 0x08, 0xBF), (0xF6, 0xE9, 0x1D, 0xD9)):
            dots = extract_diaeresis_dots(block.decompressed, reference, plain)
            if not dots:
                raise ValueError(f"Tréma absent dans la police {block.offset:#x}")
            font[target * 32:(target + 1) * 32] = build_umlaut(block.decompressed, base, dots)
        compressed = lz77_compress(bytes(font), vram_safe=True)
        if len(compressed) <= block.compressed_len:
            dest = block.offset
        else:
            dest = allocator.allocate(len(compressed))
            if not repoint_pointers(rom, block.offset, dest):
                raise ValueError("Police relocalisée sans pointeur")
        rom[dest:dest + len(compressed)] = compressed
    patch_width_tables(rom, [(0xF3, 0xCF), (0xF6, 0xE9)])
    return len(blocks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    args = parser.parse_args()
    rom = bytearray(args.rom.read_bytes())
    Path(str(args.rom) + ".bak").write_bytes(rom)
    count = apply_patches(rom)
    args.rom.write_bytes(rom)
    print(f"Polices ES vérifiées et complétées : {count}")
