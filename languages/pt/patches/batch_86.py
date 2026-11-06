"""PT-86 : finalise les services BP, le Ring Challenge et les missions des gangs."""
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


class Batch86Patch(ScenarioTextPatch):
    """Prépare le pronom neutre uniquement pour la réplique de Big Mo du lot."""

    PRONOUN_CALL = 0x1EA3686
    ORIGINAL_HELPER = 0x1EAB8FD
    PRONOUN = TextEncoder.encode_pokemon("você", strict=True)

    HELPERS = (
        (0x1EAB8FD, (0x1EA3686,), 2, "você"),
        (0x1EA7B75, (0x1EA7AB0, 0x1EA7ABE, 0x1EA7AD6, 0x1EA7B10,
                     0x1EA7B48, 0x1EA7B68, 0x1EA7EDE, 0x1EA7FC2, 0x1EA8010), 0, "colega"),
        (0x1EA5F21, (0x1EA5ED9, 0x1EA5F0B), 0, "senhor"),
    )

    def _helper_bytes(self, helper: tuple, target: int) -> bytes:
        """Compose le script local et ses chaînes ; les titres gardent le genre."""
        original, _, buffer, text = helper
        raw = TextEncoder.encode_pokemon(text, strict=True)
        if original != 0x1EA5F21:
            return (b"\x04" + (original + 0x08000000).to_bytes(4, "little")
                    + b"\x85" + bytes([buffer]) + (target + 12 + 0x08000000).to_bytes(4, "little")
                    + b"\x03" + raw)
        # Même branchement checkgender que l'anglais, déplacé intégralement.
        code = bytearray(self.source[original:original + 38])
        for pos, delta in ((8, 24), (19, 31), (26, 38), (33, 38 + len(raw))):
            code[pos:pos + 4] = (target + delta + 0x08000000).to_bytes(4, "little")
        return bytes(code) + raw + TextEncoder.encode_pokemon("senhora", strict=True)

    def _verify_pronoun(self, rom: bytes | bytearray) -> None:
        for helper in self.HELPERS:
            for site in helper[1]:
                target = int.from_bytes(rom[site:site + 4], "little") - 0x08000000
                expected = self._helper_bytes(helper, target) if target >= 0 else b""
                if not expected or not 0 <= target <= len(rom) - len(expected) or rom[target:target + len(expected)] != expected:
                    raise ValueError("PT-86 : préparation locale du pronom différente")

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Copie les préparations de tampon aux seuls appels des dialogues du lot."""
        working = bytearray(rom)
        for helper in self.HELPERS:
            original, sites, _, _ = helper
            pointer = (original + 0x08000000).to_bytes(4, "little")
            if any(self.source[p - 1:p + 4] != b"\x04" + pointer for p in sites):
                raise ValueError("PT-86 : préimage de l'appel de tampon différente")
            if all(working[p:p + 4] == pointer for p in sites):
                target = FreeSpaceAllocator(working).allocate(len(self._helper_bytes(helper, 0)))
                if target is None:
                    raise ValueError("PT-86 : espace libre insuffisant pour le pronom")
                code = self._helper_bytes(helper, target)
                working[target:target + len(code)] = code
                for site in sites:
                    working[site:site + 4] = (target + 0x08000000).to_bytes(4, "little")
        self._verify_pronoun(working)
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Vérifie textes et routines locales, sans anglais dans les tampons."""
        super().verify(rom)
        self._verify_pronoun(rom)


def make_patch(source: bytes) -> Batch86Patch:
    """Charge les lecteurs prouvés ; exclut les quatre entrées sans lecteur texte."""
    audit = json.loads((ROOT / 'languages/pt/data/pt86_audit.json').read_text())
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('PT-86 : préimage ROM source différente')
    rows = [row for row in audit['entries'] if row['status'] != 'exception']
    return Batch86Patch(source, rows, ROOT / 'languages/pt/combined_pt.txt')


def main() -> int:
    """Sauvegarde puis réinjecte verbatim aux seuls pointeurs audités du lot."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    before = args.rom.read_bytes()
    rom = bytearray(before)
    source = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    audit = json.loads((ROOT / 'languages/pt/data/pt86_audit.json').read_text())
    # Le repointeur générique peut confondre instructions et échantillons avec des pointeurs.
    for row in audit['entries']:
        for site in row.get('non_text_references', []):
            rom[site:site + 4] = source[site:site + 4]
    stats = make_patch(source).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(before)
    args.rom.write_bytes(rom)
    print(f'PT-86 : {stats}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
