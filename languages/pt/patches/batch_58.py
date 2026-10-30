"""PT-58 : catégories fixes et dialogues d'Antisis aux consommateurs réels."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch
from scripts.apply_combined_fr import _load_combined
from src.core.text_codec import TextEncoder


def make_patch(source: bytes) -> BorriusTextPatch:
    """Charge les 126 textes d’Antisis aux pointeurs audités."""
    audit = json.loads((ROOT / 'languages/pt/data/pt58_audit.json').read_text())
    return BorriusTextPatch(source, [r for r in audit['entries'] if r['kind'] == 'dialogue'],
                            ROOT / 'languages/pt/combined_pt.txt')


def apply_patches(rom: bytearray, source: bytes) -> dict[str, int]:
    """Valide les cellules indexées avant toute écriture ; conserve les champs voisins."""
    audit = json.loads((ROOT / 'languages/pt/data/pt58_audit.json').read_text())
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-58')
    if [r['offset'] for r in audit['entries']] != manifest:
        raise ValueError('Manifeste PT-58 différent')
    texts, _ = _load_combined(ROOT / 'languages/pt/combined_pt.txt')
    base = int(audit['table_base'], 16)
    for ref in audit['table_references']:
        pointer = (base + 0x08000000).to_bytes(4, 'little')
        if source[ref:ref + 4] != pointer or rom[ref:ref + 4] != pointer:
            raise ValueError(f'Lecteur Pokédex différent : {ref:#x}')
    writes = {}
    for row in audit['entries']:
        if row['kind'] != 'category':
            continue
        key, cell = int(row['offset'], 16), int(row['consumer_offset'], 16)
        before = bytes.fromhex(row['cell_hex'])
        raw = TextEncoder.encode_pokemon(texts[key], strict=True)
        if (cell != key + 2 or (cell - base) % 36 or len(before) != 12
                or source[cell:cell + 12] != before or source[key:cell] != b'\0\0'
                or not 0 <= cell <= len(rom) - 12 or len(raw) > 12):
            raise ValueError(f'Préimage ou budget catégorie différent : {key:#x}')
        # Clé extraite deux octets avant la vraie cellule : restaurer ces octets
        # si la passe inline générique y a placé le début du libellé.
        writes[key] = source[key:cell] + raw + b'\xff' * (12 - len(raw))
    working = bytearray(rom)
    stats = make_patch(source).apply(working)
    for key, data in writes.items():
        working[key:key + len(data)] = data
    rom[:] = working
    return dict(stats, categories=len(writes))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = apply_patches(rom, (ROOT / 'input/roms/englishrom.gba').read_bytes())
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-58 : {stats}')


if __name__ == '__main__':
    main()
