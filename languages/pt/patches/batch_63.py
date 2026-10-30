"""PT-63 : finalise les dialogues, missions et menus aux pointeurs audités."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_29 import Batch29TextPatch


class ScenarioTextPatch(Batch29TextPatch):
    """Vérifie aussi que les préfixes et les échantillons restent intacts."""

    def verify(self, rom: bytes | bytearray) -> None:
        """Contrôle les lecteurs texte et les régions exclues du repointage."""
        super().verify(rom)
        for row in self.definitions:
            for site in row.get('non_text_references', []):
                if rom[site:site + 4] != self.source[site:site + 4]:
                    raise ValueError('PT-63 : région non textuelle modifiée')
            if 'prefix_start' in row:
                start, end = row['prefix_start'], int(row['offset'], 16)
                if rom[start:end] != self.source[start:end]:
                    raise ValueError('PT-63 : alignement modifié')


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Charge exclusivement les consommateurs texte prouvés du manifeste PT-63."""
    audit = json.loads((ROOT / 'languages/pt/data/pt63_audit.json').read_text())
    rows, aliases = [], {}
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        definition = dict(row)
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            header = bytes.fromhex(pcm['header_hex'])
            if (len(header) != 16 or source[base:base + 16] != header
                    or int.from_bytes(source[ref:ref + 4], 'little') != base + 0x08000000
                    or not base + 16 <= site <= base + 12 + int.from_bytes(header[12:16], 'little')
                    or source[site:site + 4] != (int(row['offset'], 16) + 0x08000000).to_bytes(4, 'little')):
                raise ValueError('PT-63 : préimage PCM différente')
        for binary in row.get('binary_matches', []):
            base, site = binary['base'], binary['site']
            data = bytes.fromhex(binary['source_hex'])
            if (source[base:base + len(data)] != data or not base <= site <= base + len(data) - 4
                    or source[site:site + 4] != (int(row['offset'], 16) + 0x08000000).to_bytes(4, 'little')):
                raise ValueError('PT-63 : préimage code/graphisme différente')
        if 'consumer_offset' in row:
            offset, target = int(row['offset'], 16), int(row['consumer_offset'], 16)
            raw, prefix = bytes.fromhex(row['source_hex']), bytes.fromhex(row['prefix_hex'])
            if (source[offset:offset + len(raw)] != raw or raw[:len(prefix)] != prefix
                    or target != offset + len(prefix)):
                raise ValueError('PT-63 : préimage alignement différente')
            definition.update(offset=row['consumer_offset'], source_hex=raw[len(prefix):].hex(),
                              prefix_start=offset, references=row['consumer_references'])
            aliases[target] = offset
        rows.append(definition)
    patch = ScenarioTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')
    for target, key in aliases.items():
        patch.texts[target] = patch.texts[key]
    return patch


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
    print(f'PT-63 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
