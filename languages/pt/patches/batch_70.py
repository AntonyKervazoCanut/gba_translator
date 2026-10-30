"""Finalise les 298 consommateurs PT-70 après les réparations génériques."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


class Batch70Patch(ScenarioTextPatch):
    """Adapte localement le tampon de genre du rapport des ruines."""

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Prépare le sujet ele/ela et les textes dans une transaction unique."""
        working = bytearray(rom)
        for row in self.definitions:
            setup = row.get('buffer_setup')
            if setup:
                site = setup['call_offset']
                if self.source[site:site + 5].hex() != setup['source_hex']:
                    raise ValueError('PT-70 : préimage du tampon de genre différente')
                working[site:site + 5] = bytes.fromhex(setup['replacement_hex'])
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les dialogues et la préparation du sujet, pour les deux genres."""
        super().verify(rom)
        for row in self.definitions:
            setup = row.get('buffer_setup')
            if setup:
                site = setup['call_offset']
                if rom[site:site + 5].hex() != setup['replacement_hex']:
                    raise ValueError('PT-70 : tampon de genre non finalisé')


def make_patch(source: bytes) -> Batch70Patch:
    """Charge les pointeurs de scripts et de tables audités, sans cellule brute."""
    audit = json.loads((ROOT / 'languages/pt/data/pt70_audit.json').read_text())
    rows = [r for r in audit['entries'] if r['status'] != 'exception']
    for row in rows:
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            if (source[base:base + 16].hex() != pcm['header_hex']
                    or int.from_bytes(source[ref:ref + 4], 'little') != base + 0x08000000
                    or not base + 16 <= site < base + 16 + int.from_bytes(source[base + 12:base + 16], 'little')):
                raise ValueError('PT-70 : préimage PCM différente')
    return Batch70Patch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis livre les textes complets aux consommateurs vivants."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-70 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
