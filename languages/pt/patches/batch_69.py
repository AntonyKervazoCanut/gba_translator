"""PT-69 : lecteurs audités, messages du café et tampons de genre locaux."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch
from src.core.text_reinserter import FreeSpaceAllocator

ROM_BASE = 0x08000000


class Batch69Patch(ScenarioTextPatch):
    """Réutilise l’injection bornée ; adapte uniquement les consommateurs PT-69."""

    def __init__(self, source: bytes, audit: dict):
        definitions = [dict(row) for row in audit['entries'] if row['status'] != 'exception']
        # Le suffixe exclu peut avoir été repointé à tort par une passe générique.
        definitions[0]['non_text_references'] = audit['preserved_sites']
        super().__init__(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
        self.audit = audit

    def _empty_pointer(self, row: dict, rom: bytes | bytearray) -> bytes:
        offset = int(row['offset'], 16)
        _, refs, encoded = next(entry for entry in self.entries() if entry[0] == offset)
        target = int.from_bytes(rom[refs[0]:refs[0] + 4], 'little')
        return (target + len(encoded) - 1).to_bytes(4, 'little')

    def _wrapper(self, row: dict, rom: bytes | bytearray) -> bytes:
        # CALL original ; BUFFERSTRING slot, chaîne vide ; RETURN.
        # Les autres tampons et les effets du helper sont conservés.
        return (bytes.fromhex(row['source_hex']) + bytes([0x85, row['buffer_slot']])
                + self._empty_pointer(row, rom) + b'\x03')

    def verify_consumers(self, rom: bytes | bytearray) -> None:
        """Contrôle les textes, quatre appels locaux, possessifs et régions exclues."""
        self.verify(rom)
        for site in self.audit['preserved_sites']:
            if rom[site:site + 4] != self.source[site:site + 4]:
                raise ValueError('PT-69 : faux pointeur binaire modifié')
        for row in self.audit['native_edits']:
            start, expected = row['offset'], bytes.fromhex(row['expected_hex'])
            if rom[start:start + len(expected)] != expected:
                raise ValueError('PT-69 : possessif du café non localisé')
        for row in self.audit['local_buffers']:
            site = row['call_site']
            target = int.from_bytes(rom[site + 1:site + 5], 'little') - ROM_BASE
            expected = self._wrapper(row, rom)
            if rom[site] != 4 or not 0 <= target <= len(rom) - len(expected):
                raise ValueError('PT-69 : appel local hors ROM')
            if rom[target:target + len(expected)] != expected:
                raise ValueError('PT-69 : tampon local différent')

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Applique tous les changements dans une copie avant validation finale."""
        working = bytearray(rom)
        # Une application précédente est acceptée ; toute autre préimage est refusée.
        for row in self.audit['native_edits']:
            site = row['offset']
            before, after = bytes.fromhex(row['source_hex']), bytes.fromhex(row['expected_hex'])
            if working[site:site + len(before)] not in (before, after):
                raise ValueError('PT-69 : préimage café différente')
        for row in self.audit['local_buffers']:
            site = row['call_site']
            before = bytes.fromhex(row['source_hex'])
            if working[site:site + len(before)] != before:
                target = int.from_bytes(working[site + 1:site + 5], 'little') - ROM_BASE
                expected = self._wrapper(row, working)
                if working[site] != 4 or target < 0 or working[target:target + len(expected)] != expected:
                    raise ValueError('PT-69 : préimage appel différente')
        stats = super().apply(working)
        allocator = FreeSpaceAllocator(working)
        for row in self.audit['native_edits']:
            site, encoded = row['offset'], bytes.fromhex(row['expected_hex'])
            working[site:site + len(encoded)] = encoded
        for row in self.audit['local_buffers']:
            site = row['call_site']
            expected = self._wrapper(row, working)
            current = int.from_bytes(working[site + 1:site + 5], 'little') - ROM_BASE
            if current >= 0 and working[current:current + len(expected)] == expected:
                continue
            target = allocator.allocate(len(expected))
            if target is None:
                raise ValueError('PT-69 : espace insuffisant pour le tampon local')
            working[target:target + len(expected)] = expected
            working[site:site + 5] = b'\x04' + (target + ROM_BASE).to_bytes(4, 'little')
        self.verify_consumers(working)
        rom[:] = working
        return stats


def make_patch(source: bytes) -> Batch69Patch:
    """Refuse une ROM source différente de celle auditée, code et PCM compris."""
    audit = json.loads((ROOT / 'languages/pt/data/pt69_audit.json').read_text())
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('PT-69 : préimage ROM source différente')
    return Batch69Patch(source, audit)


def main() -> int:
    """Sauvegarde puis finalise les seuls consommateurs du manifeste PT-69."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-69 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
