"""PT-83 : finalise les règles, menus et dialogues du Battle Frontier."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch


def make_patch(source: bytes) -> ScenarioTextPatch:
    """Charge les lecteurs prouvés ; exclut le message inactif sans pointeur."""
    audit = json.loads((ROOT / 'languages/pt/data/pt83_audit.json').read_text())
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('PT-83 : préimage ROM source différente')
    rows = []
    for row in audit['entries']:
        if row['status'] == 'exception':
            continue
        definition = dict(row)
        if 'consumer_offset' in row:
            offset, target = int(row['offset'], 16), int(row['consumer_offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            prefix = bytes.fromhex(row['prefix_hex'])
            if raw[:len(prefix)] != prefix or target != offset + len(prefix):
                raise ValueError('PT-83 : préfixe différent')
            definition.update(offset=row['consumer_offset'], source_hex=raw[len(prefix):].hex(),
                              prefix_start=offset, references=row['consumer_references'])
        rows.append(definition)
    patch = ScenarioTextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')
    for row in audit['entries']:
        if row['status'] != 'exception' and 'consumer_offset' in row:
            patch.texts[int(row['consumer_offset'], 16)] = patch.texts[int(row['offset'], 16)]
    return patch


def main() -> int:
    """Sauvegarde puis réinjecte verbatim aux seuls pointeurs audités du lot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-83 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
