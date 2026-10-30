"""Finalise les lecteurs audités PT-73 : réglages, Ligue et Polder Town."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch
from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.text_codec import TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator


class Batch73Patch(ScenarioTextPatch):
    """Conserve la pagination exacte et les cellules RAM du menu Options."""

    def __init__(self, source: bytes, audit: dict):
        self.local = audit['runtime_buffers']['croagunk_local_fix']
        super().__init__(source, [r for r in audit['entries'] if r['status'] != 'exception'],
                         ROOT / 'languages/pt/combined_pt.txt')

    def local_strings(self) -> list[bytes]:
        """Encode les quatre variantes du tampon propre au spectacle de Croagunk."""
        return [TextEncoder.encode_pokemon(row['portuguese'], strict=True)
                for row in self.local['descriptors']]

    def verify_local(self, rom: bytes | bytearray) -> None:
        """Suit le littéral du helper ; les quatre pointeurs doivent livrer du PT."""
        site = int(self.local['literal_site'], 16)
        table = int.from_bytes(rom[site:site + 4], 'little') - 0x08000000 + 32
        if not 0 <= table <= len(rom) - 16:
            raise ValueError('PT-73 : table locale hors ROM')
        for index, raw in enumerate(self.local_strings()):
            target = int.from_bytes(rom[table + index * 4:table + index * 4 + 4], 'little') - 0x08000000
            if not 0 <= target <= len(rom) - len(raw) or rom[target:target + len(raw)] != raw:
                raise ValueError('PT-73 : description Croagunk non localisée')

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Clone la table de ce seul helper avant la transaction des textes."""
        working = bytearray(rom)
        site = int(self.local['literal_site'], 16)
        source_literal = bytes.fromhex(self.local['literal_source_hex'])
        if working[site:site + 4] != source_literal:
            self.verify_local(working)
        else:
            strings = self.local_strings()
            size = 48 + sum(map(len, strings))
            base = FreeSpaceAllocator(working).allocate(size)
            if base is None:
                raise ValueError('PT-73 : espace insuffisant pour la table locale')
            cursor = base + 48
            for index, raw in enumerate(strings):
                working[cursor:cursor + len(raw)] = raw
                slot = base + 32 + index * 4
                working[slot:slot + 4] = (cursor + 0x08000000).to_bytes(4, 'little')
                cursor += len(raw)
            working[site:site + 4] = (base + 0x08000000).to_bytes(4, 'little')
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Contrôle textes et tampon natif, sans modifier la table commune."""
        super().verify(rom)
        self.verify_local(rom)

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Refuse tout changement de commandes et tout débordement de cellule."""
        entries = super().entries()
        for row, (offset, _, encoded) in zip(self.definitions, entries):
            source = bytes.fromhex(row['source_hex'])
            if _extract_control_sequences_from_raw(encoded) != _extract_control_sequences_from_raw(source):
                raise ValueError(f'{offset:#x}: pagination ou commandes différentes')
            if row.get('byte_budget') and len(encoded) > row['byte_budget']:
                raise ValueError(f'{offset:#x}: cellule RAM Options dépassée')
        return entries


def make_patch(source: bytes) -> Batch73Patch:
    """Charge uniquement les consommateurs du manifeste et vérifie la ROM source."""
    audit = json.loads((ROOT / 'languages/pt/data/pt73_audit.json').read_text())
    manifest = next(b['offsets'] for b in json.loads(
        (ROOT / 'languages/pt/translation_batches.json').read_text()) if b['id'] == 'PT-73')
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('PT-73 : préimage ROM différente')
    if [r['offset'] for r in audit['entries']] != manifest:
        raise ValueError('PT-73 : manifeste différent')
    return Batch73Patch(source, audit)


def main() -> int:
    """Sauvegarde et finalise atomiquement les seuls pointeurs texte du lot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-73 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
