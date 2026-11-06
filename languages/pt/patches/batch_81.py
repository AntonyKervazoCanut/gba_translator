"""Finalise les consommateurs PT-81 et préserve les échantillons PCM."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


class Batch81Patch(ScenarioTextPatch):
    """Neutralise uniquement le suffixe anglais a/an du mini-jeu de minage."""

    SUFFIX_INSTRUCTIONS = ((0x1EDBF5A, bytes.fromhex('e223'), bytes.fromhex('ff23')),
                           (0x1EDBF5E, bytes.fromhex('1d33'), bytes.fromhex('0033')))

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Vide STR_VAR_2 dans les deux branches, puis injecte atomiquement."""
        working = bytearray(rom)
        for offset, before, after in self.SUFFIX_INSTRUCTIONS:
            if self.source[offset:offset + 2] != before or working[offset:offset + 2] not in (before, after):
                raise ValueError('PT-81 : préimage du suffixe a/an différente')
            working[offset:offset + 2] = after
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie les consommateurs et le terminateur du suffixe minage."""
        super().verify(rom)
        for offset, _, after in self.SUFFIX_INSTRUCTIONS:
            if rom[offset:offset + 2] != after:
                raise ValueError('PT-81 : suffixe anglais du minage actif')


def make_patch(source: bytes) -> Batch81Patch:
    """Charge les dialogues et les tables de noms aux préimages contrôlées."""
    audit = json.loads((ROOT / 'languages/pt/data/pt81_audit.json').read_text())
    definitions, aliases = [], {}
    for row in audit['entries']:
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            if (source[base:base + 16].hex() != pcm['header_hex']
                    or int.from_bytes(source[ref:ref + 4], 'little') != base + 0x08000000
                    or not base + 16 <= site < base + 16 + int.from_bytes(source[base + 12:base + 16], 'little')):
                raise ValueError('PT-81 : préimage PCM différente')
        if row['status'] == 'exception':
            continue
        definition = dict(row)
        if 'consumer_offset' in row:
            offset, target = int(row['offset'], 16), int(row['consumer_offset'], 16)
            raw, prefix = bytes.fromhex(row['source_hex']), bytes.fromhex(row['prefix_hex'])
            if (source[offset:offset + len(raw)] != raw or raw[:len(prefix)] != prefix
                    or target != offset + len(prefix)):
                raise ValueError('PT-81 : préimage alignement différente')
            definition.update(offset=row['consumer_offset'], source_hex=raw[len(prefix):].hex(),
                              prefix_start=offset, references=row['consumer_references'])
            aliases[target] = offset
        definitions.append(definition)
    patch = Batch81Patch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
    for target, key in aliases.items():
        patch.texts[target] = patch.texts[key]
    return patch


def main() -> int:
    """Sauvegarde et injecte les seuls consommateurs texte du manifeste PT-81."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-81 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
