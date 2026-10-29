"""Finalise les consommateurs PT-20 sans écrire dans les fragments ou scripts EN."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_inline_overrides_fr import _extract_control_sequences_from_raw
from src.core.dialogue_linewrap import line_widths
from src.core.structured_text import StructuredTextPatch
from src.core.text_codec import TextEncoder


class BorriusTextPatch(StructuredTextPatch):
    """Conserve les pages, couleurs et tampons des dialogues partagés."""

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Valide les préimages et budgets avant la relocalisation atomique partagée."""
        entries = []
        used = set()
        for row in self.definitions:
            offset = int(row['offset'], 16)
            source = bytes.fromhex(row['source_hex'])
            refs = row['references']
            if not source.endswith(b'\xff') or self.source[offset:offset + len(source)] != source:
                raise ValueError(f'{offset:#x}: préimage différente')
            if not refs or used.intersection(refs):
                raise ValueError(f'{offset:#x}: références absentes ou dupliquées')
            used.update(refs)
            for ref in refs:
                if int.from_bytes(self.source[ref:ref + 4], 'little') != offset + 0x08000000:
                    raise ValueError(f'{offset:#x}: pointeur source différent')
            text = self.texts[offset].replace(r'\n', '\n')
            encoded = TextEncoder.encode_pokemon(text, strict=True)
            def commands(raw: bytes) -> list[list[int]]:
                return [s for s in _extract_control_sequences_from_raw(raw) if s[0] != 0xFE]
            if commands(encoded) != commands(source):
                raise ValueError(f'{offset:#x}: commandes différentes')
            if max(line_widths(text), default=0) > row['max_width']:
                raise ValueError(f'{offset:#x}: largeur dépassée')
            entries.append((offset, refs, encoded))
        return entries


def make_patch(source: bytes) -> BorriusTextPatch:
    """Charge exclusivement les consommateurs texte prouvés du manifeste PT-20."""
    audit = json.loads((ROOT / 'languages/pt/data/pt20_audit.json').read_text())
    rows = [r for r in audit['entries'] if r['status'] != 'exception']
    return BorriusTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis finalise les pointeurs de la ROM PT construite."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-20 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
