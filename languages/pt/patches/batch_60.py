"""Finalise les consommateurs PT-60 et la cellule fixe du titre des tenues."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch
from src.core.text_codec import TextEncoder


class ScenarioPatch(BorriusTextPatch):
    """Ajoute le titre à pointeur intérieur et préserve les faux pointeurs."""

    def __init__(self, source: bytes, rows: list[dict]):
        self.rows = rows
        super().__init__(source, [r for r in rows if r['layout'] != 'fixed_title'],
                         ROOT / 'languages/pt/combined_pt.txt')

    def title(self) -> tuple[dict, int, bytes]:
        """Valide le titre de 13 octets dont le consommateur saute l'espace."""
        row = next(r for r in self.rows if r['layout'] == 'fixed_title')
        offset = int(row['offset'], 16)
        raw = TextEncoder.encode_pokemon(self.texts[offset], strict=True)
        source = bytes.fromhex(row['source_hex'])
        if self.source[offset:offset + len(source)] != source:
            raise ValueError('PT-60 : préimage du titre différente')
        if len(raw) > len(source) or raw[0] != 0:
            raise ValueError('PT-60 : budget/espace initial du titre')
        for ref in row['references']:
            if int.from_bytes(self.source[ref:ref + 4], 'little') != offset + 1 + 0x08000000:
                raise ValueError('PT-60 : pointeur intérieur du titre différent')
        return row, offset, raw

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Applique atomiquement les textes et la cellule fixe, puis vérifie."""
        row, offset, raw = self.title()
        working = bytearray(rom)
        working[offset:offset + len(raw)] = raw
        for ref in row['references']:
            working[ref:ref + 4] = (offset + 1 + 0x08000000).to_bytes(4, 'little')
        # Les motifs de quatre octets dans les échantillons audio PCM ne sont pas
        # des consommateurs. Annule aussi un éventuel repointage générique.
        for definition in self.rows:
            for ref in definition['non_text_references']:
                working[ref:ref + 4] = self.source[ref:ref + 4]
        stats = super().apply(working)
        self.verify(working)
        rom[:] = working
        return dict(stats, verified=stats['verified'] + 1)

    def verify(self, rom: bytes | bytearray) -> None:
        """Contrôle les octets réellement lus par tous les consommateurs."""
        super().verify(rom)
        row, offset, raw = self.title()
        if rom[offset:offset + len(raw)] != raw:
            raise ValueError('PT-60 : titre non injecté')
        for ref in row['references']:
            if int.from_bytes(rom[ref:ref + 4], 'little') != offset + 1 + 0x08000000:
                raise ValueError('PT-60 : cible intérieure du titre différente')
        for definition in self.rows:
            for ref in definition['non_text_references']:
                if rom[ref:ref + 4] != self.source[ref:ref + 4]:
                    raise ValueError('PT-60 : échantillons PCM modifiés')


def make_patch(source: bytes) -> ScenarioPatch:
    """Charge exclusivement le manifeste audité PT-60."""
    rows = json.loads((ROOT / 'languages/pt/data/pt60_audit.json').read_text())['entries']
    return ScenarioPatch(source, [r for r in rows if r['status'] != 'exception'])


def main() -> int:
    """Sauvegarde la ROM puis applique le finaliseur du seul lot PT-60."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-60 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
