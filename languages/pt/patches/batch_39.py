"""Finalise les descriptions et les noms fixes du seul lot PT-39."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.structured_text import StructuredTextPatch
from src.core.text_codec import TextEncoder


def make_patch(source: bytes) -> StructuredTextPatch:
    """Vérifie chaque index, y compris les G-Max au-delà du compteur historique 893."""
    audit = json.loads((ROOT / 'languages/pt/data/pt39_audit.json').read_text())
    rows = []
    for row in audit['entries']:
        if row['kind'] != 'description':
            continue
        for index in row['move_ids']:
            site = 0x99F190 + 4 * index
            if (site not in row['references'] or
                    int.from_bytes(source[site:site + 4], 'little') != int(row['offset'], 16) + 0x08000000):
                raise ValueError(f"Index de mouvement PT-39 invalide : {index}")
        # Le helper partagé filtre les mouvements au-delà de 893 ; leurs cellules
        # sont validées ci-dessus sans changer le contrat des autres langues.
        rows.append(dict(row, move_ids=[]))
    return StructuredTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def apply_patches(rom: bytearray, source: bytes) -> dict[str, int]:
    """Écrit atomiquement aux pointeurs vivants et dans les cellules fixes prouvées."""
    audit = json.loads((ROOT / 'languages/pt/data/pt39_audit.json').read_text())
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    for data in (source, rom):
        if int.from_bytes(data[0x308A4:0x308A8], 'little') != 0x08A40A10:
            raise ValueError('Table de noms PT-39 inattendue')
        for site in (0xE5440, 0x137BC8, 0x9F3B64):
            if int.from_bytes(data[site:site + 4], 'little') != 0x0899F194:
                raise ValueError('Lecteur de descriptions PT-39 inattendu')
    names = {}
    for row in audit['entries']:
        off = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        if source[off:off + len(raw)] != raw:
            raise ValueError(f'Préimage PT-39 invalide : {off:#x}')
        text = texts[off]
        encoded = TextEncoder.encode_pokemon(text, strict=True)
        if row['kind'] == 'name':
            if (off != 0xA40A10 + row['move_ids'][0] * 13 or len(encoded) > 13
                    or text != row['english'] or max(line_widths(text)) > 120):
                raise ValueError(f'Nom fixe PT-39 invalide : {off:#x}')
            names[off] = encoded
        elif (text.count('\n') != row['english'].count('\n')
              or text.count('\n') >= 5 or max(line_widths(text)) > 122
              or any(c >= 0xF7 and c != 0xFE for c in encoded[:-1])):
            raise ValueError(f'Budget ou contrôles PT-39 invalides : {off:#x}')
    working = bytearray(rom)
    stats = make_patch(source).apply(working)
    for off, encoded in names.items():
        working[off:off + len(encoded)] = encoded
    rom[:] = working
    return dict(stats, names=len(names))


def main() -> None:
    """Sauvegarde la ROM et applique le contrat final du lot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = apply_patches(rom, source)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-39 : {stats}')


if __name__ == '__main__':
    main()
