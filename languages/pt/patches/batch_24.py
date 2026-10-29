#!/usr/bin/env python3
"""PT-24 : finalise les dialogues de Borrius et descriptions des objets."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from src.core.dialogue_linewrap import line_width
from src.core.structured_text import StructuredTextPatch


class BorriusTextPatch(StructuredTextPatch):
    """Conserve les preimages partagees avant de reloger les textes du lot."""

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Restaure les copies source pour proteger leurs references interieures."""
        # La passe generique peut avoir raccourci ces textes sur place.
        # Restaurer avant super.apply force leur relocation et preserve les
        # suffixes references (y compris les trois exceptions corrompues).
        working = bytearray(rom)
        for definition in self.definitions:
            offset = int(definition['offset'], 16)
            raw = bytes.fromhex(definition['source_hex'])
            if offset + len(raw) > len(working):
                raise ValueError('Preimage hors ROM')
            working[offset:offset + len(raw)] = raw
        stats = super().apply(working)
        self.verify_source_spans(working)
        rom[:] = working
        return stats

    def verify_source_spans(self, rom: bytes | bytearray) -> None:
        """Prouve que les copies originales et leurs suffixes restent intacts."""
        for definition in self.definitions:
            offset = int(definition['offset'], 16)
            raw = bytes.fromhex(definition['source_hex'])
            if rom[offset:offset + len(raw)] != raw:
                raise ValueError(f'{offset:#x}: copie source alteree')


def make_patch(source: bytes) -> BorriusTextPatch:
    """Charge les seuls consommateurs prouvés du manifeste PT-24."""
    rows = json.loads((ROOT / 'languages/pt/data/pt24_audit.json').read_text())['entries']
    patch = BorriusTextPatch(source, [dict(r) for r in rows if r['status'] != 'exception'],
                                ROOT / 'languages/pt/combined_pt.txt')
    for definition in patch.definitions:
        text = patch.texts[int(definition['offset'], 16)]
        layout = definition['layout']
        # Le validateur historique ne découpe que FE/FB. Vérifier chaque
        # ligne FA ici avant de lui déclarer la largeur cumulée du segment.
        lines = re.split(r'\\n|<0xFA>|<0xFB>', text)
        if max(map(line_width, lines)) > layout['max_width']:
            raise ValueError(f"{definition['offset']}: ligne visible trop large")
        segments = re.split(r'\\n|<0xFB>', text)
        definition['layout'] = dict(layout, max_width=max(
            layout['max_width'], max(map(line_width, segments))))
    return patch


def main() -> int:
    """Sauvegarde puis injecte les textes et contrôle tous leurs consommateurs."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-24 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
