"""Finalise les seuls consommateurs vivants PT-87 et leur possessif féminin."""
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


class Batch87TextPatch(Batch29TextPatch):
    """Distingue her objet (ela) et her possessif (sua) au point de lecture."""

    def isolate_title(self, rom: bytearray) -> None:
        """Isole une seule fois le titre avec espace de son suffixe partagé."""
        entries = {offset: (refs, raw) for offset, refs, raw in self.entries()}
        prefix = int(self.shared_title['prefix_offset'], 16)
        suffix = int(self.shared_title['suffix_offset'], 16)
        refs, raw = entries[prefix]
        suffix_refs, suffix_raw = entries[suffix]
        if suffix != prefix + 1 or raw != b'\x00' + suffix_raw:
            raise ValueError('PT-87 : préfixe du titre partagé différent')
        targets = [int.from_bytes(rom[p:p + 4], 'little') - 0x08000000 for p in refs]
        suffix_targets = [int.from_bytes(rom[p:p + 4], 'little') - 0x08000000 for p in suffix_refs]
        if not any(a < b + len(suffix_raw) and b < a + len(raw)
                   for a in targets for b in suffix_targets):
            return
        target = FreeSpaceAllocator(rom).allocate(len(raw))
        if target is None:
            raise ValueError('PT-87 : espace insuffisant pour le titre partagé')
        rom[target:target + len(raw)] = raw
        for ref in refs:
            rom[ref:ref + 4] = (target + 0x08000000).to_bytes(4, 'little')

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Restaure le faux pointeur PCM avant la transaction des consommateurs."""
        working = bytearray(rom)
        for row in self.exceptions:
            for ref in row['non_text_references']:
                working[ref:ref + 4] = self.source[ref:ref + 4]
        self.isolate_title(working)
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les textes contextuels et l'absence d'écriture dans le PCM."""
        super().verify(rom)
        for row in self.exceptions:
            for ref in row['non_text_references']:
                if rom[ref:ref + 4] != self.source[ref:ref + 4]:
                    raise ValueError('PT-87 : faux pointeur PCM modifié')

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Valide le bufferstring et réemploie une valeur protégée du même lot."""
        entries = super().entries()
        context = self.contextual_possessive
        ref = context['pointer']
        instruction = bytes.fromhex(context['source_instruction_hex'])
        if self.source[ref - 2:ref + 4] != instruction:
            raise ValueError('PT-87 : préimage du possessif différente')
        original = int(context['source_offset'], 16)
        translated = int(context['translation_offset'], 16)
        result = []
        for offset, refs, raw in entries:
            if offset == original:
                if ref not in refs:
                    raise ValueError('PT-87 : lecteur possessif absent')
                result.append((offset, [p for p in refs if p != ref], raw))
                result.append((offset, [ref], TextEncoder.encode_pokemon(self.texts[translated], strict=True)))
            else:
                result.append((offset, refs, raw))
        return result


def make_patch(source: bytes) -> Batch87TextPatch:
    """Charge les textes audités et les six exceptions documentées de PT-87."""
    audit = json.loads((ROOT / 'languages/pt/data/pt87_audit.json').read_text())
    rows = [r for r in audit['entries'] if r['status'] != 'exception']
    # Les faux pointeurs des exceptions doivent également être restaurés.
    exceptions = [r for r in audit['entries'] if r['status'] == 'exception']
    patch = Batch87TextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')
    patch.contextual_possessive = audit['contextual_possessive']
    patch.shared_title = audit['shared_title']
    patch.exceptions = exceptions
    return patch


def main() -> int:
    """Sauvegarde et finalise la ROM PT après les réparations génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-87 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
