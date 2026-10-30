"""Finalise les routes et missions PT-76 aux seuls consommateurs audités."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Résout les labels préfixés sans modifier leurs instructions ou bourrages."""
    audit = json.loads((ROOT / 'languages/pt/data/pt76_audit.json').read_text())
    rows, aliases = [], {}
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        definition = dict(row)
        if 'consumer_offset' in row:
            offset, target = int(row['offset'], 16), int(row['consumer_offset'], 16)
            raw, prefix = bytes.fromhex(row['source_hex']), bytes.fromhex(row['prefix_hex'])
            if (source[offset:offset + len(raw)] != raw or raw[:len(prefix)] != prefix
                    or target != offset + len(prefix)):
                raise ValueError('PT-76 : préimage du préfixe différente')
            definition.update(offset=row['consumer_offset'], source_hex=raw[len(prefix):].hex(),
                              prefix_start=offset, references=row['consumer_references'])
            aliases[target] = offset
        rows.append(definition)
    patch = ScenarioTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')
    for target, key in aliases.items():
        patch.texts[target] = patch.texts[key]
    return patch


def main() -> int:
    """Sauvegarde puis finalise les seuls pointeurs texte audités de PT-76."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-76 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
