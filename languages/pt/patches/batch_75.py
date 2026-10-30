"""Finalise les consommateurs PT-75 et préserve les échantillons PCM."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Charge les dialogues et les tables de noms aux préimages contrôlées."""
    audit = json.loads((ROOT / 'languages/pt/data/pt75_audit.json').read_text())
    definitions, aliases = [], {}
    for row in audit['entries']:
        for pcm in row.get('pcm_matches', []):
            base, ref, site = pcm['wave_base'], pcm['instrument_pointer'], pcm['site']
            if (source[base:base + 16].hex() != pcm['header_hex']
                    or int.from_bytes(source[ref:ref + 4], 'little') != base + 0x08000000
                    or not base + 16 <= site < base + 16 + int.from_bytes(source[base + 12:base + 16], 'little')):
                raise ValueError('PT-75 : préimage PCM différente')
        if row['status'] == 'exception':
            continue
        definition = dict(row)
        if 'consumer_offset' in row:
            offset, target = int(row['offset'], 16), int(row['consumer_offset'], 16)
            raw, prefix = bytes.fromhex(row['source_hex']), bytes.fromhex(row['prefix_hex'])
            if (source[offset:offset + len(raw)] != raw or raw[:len(prefix)] != prefix
                    or target != offset + len(prefix)):
                raise ValueError('PT-75 : préimage alignement différente')
            definition.update(offset=row['consumer_offset'], source_hex=raw[len(prefix):].hex(),
                              prefix_start=offset, references=row['consumer_references'])
            aliases[target] = offset
        definitions.append(definition)
    patch = ScenarioTextPatch(source, definitions, ROOT / 'languages/pt/combined_pt.txt')
    for target, key in aliases.items():
        patch.texts[target] = patch.texts[key]
    return patch


def main() -> int:
    """Sauvegarde et injecte les seuls consommateurs texte du manifeste PT-75."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-75 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
