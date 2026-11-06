"""Finalise HI-02 aux lecteurs audités, sans normaliser ses contrôles."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_inline_overrides_fr import FC_ARG_COUNTS, RAW_ARG_PREFIXES
from src.core.dialogue_linewrap import line_widths
from src.core.structured_text import StructuredTextPatch
from src.core.text_codec import TextEncoder


class HindiBatch02Patch(StructuredTextPatch):
    """Réutilise l'allocation atomique partagée ; protège aussi les cellules fixes."""

    def __init__(self, source: bytes, rows: list[dict], combined: Path):
        super().__init__(source, [r for r in rows if 'cell_start' not in r], combined)
        self.rows = rows

    @staticmethod
    def controls(raw: bytes) -> list[bytes]:
        """Inclut FE et consomme les arguments, même s'ils ressemblent à des sauts."""
        result, index = [], 0
        while index < len(raw) and raw[index] != 0xFF:
            value = raw[index]
            size = 1 + RAW_ARG_PREFIXES.get(value, 0)
            if value == 0xFC:
                size = 2 + FC_ARG_COUNTS.get(raw[index + 1], 0)
            if value >= 0xF7:
                result.append(raw[index:index + size])
            index += size
        return result

    def checked(self) -> list[tuple[dict, bytes]]:
        """Valide préimages, lecteurs, contrôles, largeur et budgets avant écriture."""
        result = []
        for row in self.rows:
            offset = int(row['offset'], 16)
            raw = bytes.fromhex(row['source_hex'])
            if self.source[offset:offset + len(raw)] != raw or not raw.endswith(b'\xff'):
                raise ValueError(f'{offset:#x}: préimage EN différente')
            for ref in row['references'] + row['non_text_references']:
                if int.from_bytes(self.source[ref:ref + 4], 'little') != offset + 0x08000000:
                    raise ValueError(f'{offset:#x}: lecteur EN différent')
            text = self.texts[offset].replace(r'\n', '\n')
            encoded = TextEncoder.encode_pokemon(text, strict=True)
            if self.controls(encoded) != self.controls(raw):
                raise ValueError(f'{offset:#x}: contrôles ou sauts différents')
            if max(line_widths(text), default=0) > row['max_width']:
                raise ValueError(f'{offset:#x}: largeur dépassée')
            if 'cell_start' in row:
                if (offset - 0x23E558) % 13 or len(encoded) > 13:
                    raise ValueError(f'{offset:#x}: cellule fixe dépassée ou désalignée')
                for site in row['table_readers']:
                    if int.from_bytes(self.source[site:site + 4], 'little') != 0x0823E558:
                        raise ValueError('Base de table différente')
            elif not row['references']:
                raise ValueError(f'{offset:#x}: lecteur absent')
            result.append((row, encoded))
        return result

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Livre au routeur partagé uniquement les chaînes relogeables."""
        return [(int(r['offset'], 16), r['references'], encoded)
                for r, encoded in self.checked() if 'cell_start' not in r]

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Applique toutes les écritures dans une copie validée avant publication."""
        working = bytearray(rom)
        for row, encoded in self.checked():
            for site in row['non_text_references']:
                working[site:site + 4] = self.source[site:site + 4]
            if 'cell_start' in row:
                offset = int(row['offset'], 16)
                working[offset:offset + 13] = encoded.ljust(13, b'\x00')
        stats = super().apply(working)
        rom[:] = working
        return stats

    def verify(self, rom: bytes | bytearray) -> None:
        """Redécode les lecteurs finaux et garantit les cellules et faux pointeurs."""
        super().verify(rom)
        for row, encoded in self.checked():
            for site in row['non_text_references']:
                if rom[site:site + 4] != self.source[site:site + 4]:
                    raise ValueError('Données non textuelles modifiées')
            if 'cell_start' in row:
                offset = int(row['offset'], 16)
                if rom[offset:offset + 13] != encoded.ljust(13, b'\x00'):
                    raise ValueError(f'{offset:#x}: cellule cible différente')


def make_patch(source: bytes) -> HindiBatch02Patch:
    """Charge le manifeste fermé et exige la ROM EN de référence."""
    audit = json.loads((ROOT / 'languages/indie/data/hi02_audit.json').read_text())
    if hashlib.sha256(source).hexdigest() != audit['source_sha256']:
        raise ValueError('HI-02 : ROM EN différente')
    rows = [r for r in audit['entries'] if r['status'] == 'translated']
    return HindiBatch02Patch(source, rows, ROOT / 'languages/indie/combined_indie.txt')


def main() -> None:
    """Sauvegarde puis finalise exclusivement le lot HI-02."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, required=True)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    stats = make_patch((ROOT / 'input/roms/englishrom.gba').read_bytes()).apply(rom)
    Path(str(args.rom) + '.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'HI-02 : {stats}')


if __name__ == '__main__':
    main()
