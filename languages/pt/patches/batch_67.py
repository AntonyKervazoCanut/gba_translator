"""Finalise les 298 consommateurs PT-67 et leurs deux tampons de temps verbal."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch
from src.core.text_codec import TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator


class GymCaveTextPatch(BorriusTextPatch):
    """Préserve les données binaires et localise les tampons du seul archéologue."""

    def context_entries(self) -> list[tuple[int, bytes]]:
        """Valide les deux bufferstring et leurs préimages anglaises."""
        result = []
        for row in self.definitions:
            for entry in row.get('context_buffers', []):
                ref = entry['pointer']
                offset = int(entry['source_offset'], 16)
                raw = bytes.fromhex(entry['source_hex'])
                if (self.source[ref - 2:ref] != b'\x85\x00'
                        or int.from_bytes(self.source[ref:ref + 4], 'little') != offset + 0x08000000
                        or self.source[offset:offset + len(raw)] != raw):
                    raise ValueError('PT-67 : préimage du tampon de temps verbal différente')
                result.append((ref, TextEncoder.encode_pokemon(entry['portuguese'], strict=True)))
        return result

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Refuse les préimages modifiées, y compris dans les actifs non textuels."""
        entries = super().entries()
        self.context_entries()
        for row in self.definitions:
            for evidence in row['non_text_matches']:
                start = int(evidence['context_start'], 16)
                raw = bytes.fromhex(evidence['context_hex'])
                site = int(evidence['site'], 16)
                if (self.source[start:start + len(raw)] != raw
                        or self.source[site:site + 4] !=
                        (int(row['offset'], 16) + 0x08000000).to_bytes(4, 'little')):
                    raise ValueError('PT-67 : préimage non textuelle différente')
        return entries

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Restaure les faux matches et applique atomiquement textes et tampons."""
        self.entries()
        working = bytearray(rom)
        if len(working) != len(self.source):
            raise ValueError('PT-67 : taille ROM différente')
        for row in self.definitions:
            for evidence in row['non_text_matches']:
                site = int(evidence['site'], 16)
                working[site:site + 4] = self.source[site:site + 4]
        allocator = FreeSpaceAllocator(working)
        for ref, raw in self.context_entries():
            target = int.from_bytes(working[ref:ref + 4], 'little') - 0x08000000
            if 0 <= target <= len(working) - len(raw) and working[target:target + len(raw)] == raw:
                continue
            target = allocator.allocate(len(raw))
            if target is None:
                raise ValueError('PT-67 : espace libre insuffisant pour le tampon')
            working[target:target + len(raw)] = raw
            working[ref:ref + 4] = (target + 0x08000000).to_bytes(4, 'little')
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les cibles réellement lues, les deux temps et les actifs intacts."""
        super().verify(rom)
        for ref, raw in self.context_entries():
            target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
            if not 0 <= target <= len(rom) - len(raw) or rom[target:target + len(raw)] != raw:
                raise ValueError('PT-67 : tampon de temps verbal non injecté')
        for row in self.definitions:
            for evidence in row['non_text_matches']:
                site = int(evidence['site'], 16)
                if rom[site:site + 4] != self.source[site:site + 4]:
                    raise ValueError('PT-67 : actif non textuel modifié')


def make_patch(source: bytes) -> GymCaveTextPatch:
    """Charge exclusivement les consommateurs du manifeste PT-67."""
    audit = json.loads((ROOT / 'languages/pt/data/pt67_audit.json').read_text())
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-67')
    if [r['offset'] for r in audit['entries']] != manifest:
        raise ValueError('PT-67 : manifeste différent')
    return GymCaveTextPatch(source, [r for r in audit['entries'] if r['status'] != 'exception'],
                           ROOT / 'languages/pt/combined_pt.txt')


def main() -> None:
    """Sauvegarde puis finalise la ROM PT après les réparations génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-67 : {stats}')


if __name__ == '__main__':
    main()
