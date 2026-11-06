"""Finalise les consommateurs PT-80 et restaure les sept faux pointeurs PCM."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Valide les préimages audio avant de sélectionner les seuls lecteurs texte."""
    audit = json.loads((ROOT / 'languages/pt/data/pt80_audit.json').read_text())
    definitions = []
    for row in audit['entries']:
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            if (source[base:base + 16].hex() != pcm['header_hex']
                    or int.from_bytes(source[ref:ref + 4], 'little') != base + 0x08000000
                    or not base + 16 <= site <= base + 12 + int.from_bytes(source[base + 12:base + 16], 'little')
                    or source[site:site + 4] != (int(row['offset'], 16) + 0x08000000).to_bytes(4, 'little')):
                raise ValueError('PT-80 : préimage PCM différente')
        if row['status'] != 'exception':
            definitions.append(row)
    return ScenarioTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis injecte les 296 consommateurs vivants, sans toucher aux morts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    audit = json.loads((ROOT / 'languages/pt/data/pt80_audit.json').read_text())
    # Le repointeur générique a pu confondre les suffixes morts avec du PCM.
    # Les restaurer aussi lorsqu'ils n'ont aucune traduction à finaliser.
    for row in audit['entries']:
        for site in row.get('non_text_references', []):
            rom[site:site + 4] = source[site:site + 4]
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-80 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
