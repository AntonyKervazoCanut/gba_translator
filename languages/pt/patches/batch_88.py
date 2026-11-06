"""PT-88 : finalise les missions secondaires et dialogues du scénario étendu."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.pt.patches.batch_63 import ScenarioTextPatch
from src.core.text_codec import TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator

# Seul appel du helper de genre qui prépare cette réplique du lot.
GENDER_CALL = 0x1EAED7A
GENDER_HELPER = 0x1E8A141
GENDER_HEADER = bytes.fromhex('a0210d8000000701a1d17b08210d8001000701aed17b0803')


def gender_script(target: int) -> bytes:
    """Construit le helper privé, avec possessif et pronom objet distincts."""
    script = bytearray(GENDER_HEADER)
    script[8:12] = (target + 24 + 0x08000000).to_bytes(4, 'little')
    script[19:23] = (target + 37 + 0x08000000).to_bytes(4, 'little')
    labels = ['dele', 'ele', 'dela', 'ela']
    address = target + 50
    pointers = []
    strings = bytearray()
    for label in labels:
        pointers.append((address + 0x08000000).to_bytes(4, 'little'))
        encoded = TextEncoder.encode_pokemon(label, strict=True)
        strings.extend(encoded)
        address += len(encoded)
    for first, second in [(0, 1), (2, 3)]:
        script.extend(b'\x85\x00' + pointers[first] + b'\x85\x01' + pointers[second] + b'\x03')
    return bytes(script + strings)


class Batch88TextPatch(ScenarioTextPatch):
    """Isole la grammaire de la réplique sans changer les chaînes hors lot."""

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Installe le helper privé puis finalise atomiquement les textes."""
        if (self.source[GENDER_HELPER:GENDER_HELPER + 24] != GENDER_HEADER
                or int.from_bytes(self.source[GENDER_CALL:GENDER_CALL + 4], 'little')
                != GENDER_HELPER + 0x08000000):
            raise ValueError('PT-88 : préimage du helper de genre différente')
        working = bytearray(rom)
        target = int.from_bytes(working[GENDER_CALL:GENDER_CALL + 4], 'little') - 0x08000000
        if not 0 <= target < len(working):
            raise ValueError('PT-88 : cible de genre hors ROM')
        current = gender_script(target)
        if working[target:target + len(current)] != current:
            target = FreeSpaceAllocator(working).allocate(len(gender_script(0)))
            if target is None:
                raise ValueError('PT-88 : espace libre insuffisant pour le genre')
            data = gender_script(target)
            working[target:target + len(data)] = data
            working[GENDER_CALL:GENDER_CALL + 4] = (target + 0x08000000).to_bytes(4, 'little')
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie aussi les branches, labels privés et helper partagé intact."""
        super().verify(rom)
        target = int.from_bytes(rom[GENDER_CALL:GENDER_CALL + 4], 'little') - 0x08000000
        expected = gender_script(target)
        if not 0 <= target <= len(rom) - len(expected) or rom[target:target + len(expected)] != expected:
            raise ValueError('PT-88 : helper de genre différent')
        if rom[GENDER_HELPER:GENDER_HELPER + 24] != GENDER_HEADER:
            raise ValueError('PT-88 : helper partagé modifié')


def make_patch(source: bytes) -> Batch88TextPatch:
    """Charge les lecteurs prouvés ; exclut les dix clés sans consommateur texte propre."""
    audit = json.loads((ROOT / 'languages/pt/data/pt88_audit.json').read_text())
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('PT-88 : préimage ROM source différente')
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
                raise ValueError('PT-88 : préfixe différent')
            definition.update(offset=row['consumer_offset'], source_hex=raw[len(prefix):].hex(),
                              prefix_start=offset, references=row['consumer_references'])
        rows.append(definition)
    patch = Batch88TextPatch(source, rows, ROOT / 'languages/pt/combined_pt.txt')
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
    print(f'PT-88 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
