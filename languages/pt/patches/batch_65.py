"""Finalise les seuls consommateurs vivants du scénario PT-65."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_20 import BorriusTextPatch


class ScenarioPatch(BorriusTextPatch):
    """Préserve les échantillons PCM contenant deux motifs de faux pointeurs."""

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Annule les repointages audio génériques avant l'injection atomique."""
        working = bytearray(rom)
        for row in self.definitions:
            for ref in row['non_text_references']:
                working[ref:ref + 4] = self.source[ref:ref + 4]
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les textes et la préservation des deux sons complets."""
        super().verify(rom)
        for row in self.definitions:
            for pcm in row.get('pcm_consumers', []):
                start = int(pcm['wave_header'], 16)
                end = start + 16 + pcm['sample_bytes']
                if rom[start:end] != self.source[start:end]:
                    raise ValueError(f'PT-65 : échantillon PCM modifié à {start:#x}')


def make_patch(source: bytes) -> BorriusTextPatch:
    """Charge les textes et les références auditées du seul manifeste PT-65."""
    rows = json.loads((ROOT / 'languages/pt/data/pt65_audit.json').read_text())['entries']
    return ScenarioPatch(source, [r for r in rows if r['status'] != 'exception'],
                         ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde la ROM et vérifie les cibles après les réparations génériques."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-65 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
