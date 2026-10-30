"""Finalise les 296 consommateurs de la Pension et de Dehara du lot PT-62."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


class DeharaTextPatch(BorriusTextPatch):
    """Écarte les coïncidences PCM du repointage et restaure leurs quatre octets."""

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Valide aussi la provenance sonore avant toute écriture."""
        entries = super().entries()
        for row in self.definitions:
            for match in row.get('non_text_matches', []):
                site = int(match['site'], 16)
                base = int(match['wave_base'], 16)
                ref = int(match['instrument_pointer'], 16)
                header = bytes.fromhex(match['wave_header_hex'])
                start, end = int(match['sample_start'], 16), int(match['sample_end'], 16)
                address = (int(row['offset'], 16) + 0x08000000).to_bytes(4, 'little')
                if (len(header) != 16 or start != base + 16
                        or end != start + int.from_bytes(header[12:16], 'little')
                        or not 0 <= start <= site <= end - 4 <= len(self.source) - 4
                        or self.source[base:base + 16] != header
                        or int.from_bytes(self.source[ref:ref + 4], 'little') != base + 0x08000000
                        or self.source[site:site + 4] != address):
                    raise ValueError('Préimage PCM PT-62 différente')
        return entries

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Répare les seuls faux matches que le builder générique peut repointer."""
        self.entries()
        working = bytearray(rom)
        if len(working) != len(self.source):
            raise ValueError('Taille ROM PT-62 différente')
        for row in self.definitions:
            for match in row.get('non_text_matches', []):
                site = int(match['site'], 16)
                working[site:site + 4] = self.source[site:site + 4]
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Contrôle les textes vivants et l'absence de pointeur dans le PCM."""
        super().verify(rom)
        for row in self.definitions:
            for match in row.get('non_text_matches', []):
                site = int(match['site'], 16)
                if rom[site:site + 4] != self.source[site:site + 4]:
                    raise ValueError('Échantillons PCM PT-62 modifiés')


def make_patch(source: bytes) -> DeharaTextPatch:
    """Réutilise le contrat Borrius, y compris les menus et missions pointés."""
    audit = json.loads((ROOT / 'languages/pt/data/pt62_audit.json').read_text())
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-62')
    if [r['offset'] for r in audit['entries']] != manifest:
        raise ValueError('Manifeste PT-62 différent')
    rows = [row for row in audit['entries'] if row['status'] != 'exception']
    return DeharaTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> None:
    """Sauvegarde et finalise les textes après les passes génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-62 : {stats}')


if __name__ == '__main__':
    main()
