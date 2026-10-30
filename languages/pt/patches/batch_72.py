"""Livre les dialogues complets PT-72 et les options aux consommateurs audités."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_29 import Batch29TextPatch
from src.core.text_codec import TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator


class ScenarioTextPatch(Batch29TextPatch):
    """Localise les tampons de trois appels, sans modifier les routines communes."""

    def validate_buffers(self) -> None:
        """Exige les appels originaux et leurs préimages avant toute écriture."""
        for item in self.context_buffers:
            site = int(item['call_site'], 16)
            target = int(item['routine'], 16)
            if self.source[site:site + 5] != b'\x04' + (target + 0x08000000).to_bytes(4, 'little'):
                raise ValueError('PT-72 : appel du tampon différent')
            start = int(item['routine'], 16)
            if self.source[start:start + len(bytes.fromhex(item['routine_hex']))] != bytes.fromhex(item['routine_hex']):
                raise ValueError('PT-72 : routine du tampon différente')

    def wrapper(self, item: dict, start: int) -> bytes:
        """Compile un appel original suivi d'un bufferstring PT ; genre conservé."""
        raw = bytearray(b'\x04' + (int(item['routine'], 16) + 0x08000000).to_bytes(4, 'little'))
        def pointer(relative):
            return (start + relative + 0x08000000).to_bytes(4, 'little')
        if item['kind'] == 'fixed':
            # call(5), bufferstring(6), return(1), texte terminé FF.
            raw += b'\x85\x00' + pointer(12) + b'\x03'
            raw += TextEncoder.encode_pokemon(item['text'], strict=True)
        else:
            # Le helper EN laisse VAR_RESULT égal au genre (0/1).
            # compare + goto_if vers la branche masculine ; chaque branche retourne.
            raw += b'\x21\x0d\x80\x00\x00\x06\x01' + pointer(23)
            raw += b'\x85\x01' + pointer(30) + b'\x03'
            female = TextEncoder.encode_pokemon(item['female'], strict=True)
            raw += b'\x85\x01' + pointer(30 + len(female)) + b'\x03'
            raw += female + TextEncoder.encode_pokemon(item['male'], strict=True)
        return bytes(raw)

    def verify_buffers(self, rom: bytes | bytearray) -> None:
        """Contrôle le wrapper entier et les branches, pas seulement ses pointeurs."""
        self.validate_buffers()
        for item in self.context_buffers:
            site = int(item['call_site'], 16)
            target = int.from_bytes(rom[site + 1:site + 5], 'little') - 0x08000000
            raw = self.wrapper(item, target)
            if (rom[site] != 4 or not 0 <= target <= len(rom) - len(raw)
                    or rom[target:target + len(raw)] != raw):
                raise ValueError('PT-72 : tampon local non injecté')

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Injecte atomiquement wrappers et textes, puis vérifie l'ensemble."""
        self.validate_buffers()
        self.entries()
        working = bytearray(rom)
        allocator = FreeSpaceAllocator(working)
        for item in self.context_buffers:
            site = int(item['call_site'], 16)
            target = int.from_bytes(working[site + 1:site + 5], 'little') - 0x08000000
            raw = self.wrapper(item, target)
            if 0 <= target <= len(working) - len(raw) and working[target:target + len(raw)] == raw:
                continue
            target = allocator.allocate(len(raw))
            if target is None:
                raise ValueError('PT-72 : espace libre insuffisant pour tampon')
            raw = self.wrapper(item, target)
            working[target:target + len(raw)] = raw
            working[site + 1:site + 5] = (target + 0x08000000).to_bytes(4, 'little')
        stats = super().apply(working)
        self.verify_buffers(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie chaque cible finale et les tampons contextuels des deux genres."""
        super().verify(rom)
        self.verify_buffers(rom)


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Recompose le suffixe de victoire et préserve le faux pointeur PCM."""
    audit = json.loads((ROOT / 'languages/pt/data/pt72_audit.json').read_text())
    definitions = []
    aliases = {}
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        definition = dict(row)
        if 'consumer_offset' in row:
            key, owner = int(row['offset'], 16), int(row['consumer_offset'], 16)
            prefix = bytes.fromhex(row['prefix_hex'])
            raw = bytes.fromhex(row['source_hex'])
            if owner + len(prefix) != key or source[owner:key] != prefix:
                raise ValueError('PT-72 : préfixe du suffixe différent')
            definition.update(offset=row['consumer_offset'], source_hex=(prefix + raw).hex(),
                              references=row['consumer_references'])
            aliases[owner] = row
        definitions.append(definition)
    patch = ScenarioTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
    patch.context_buffers = audit['context_buffers']
    for owner, row in aliases.items():
        patch.texts[owner] = row['prefix_portuguese'] + patch.texts[int(row['offset'], 16)]
    return patch


def main() -> int:
    """Sauvegarde puis finalise les seuls textes vivants du manifeste PT-72."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-72 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
