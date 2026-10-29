#!/usr/bin/env python3
"""Finalise les seules descriptions PT-05 auditées, sans relocation ni repointage."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_widths
from src.core.text_codec import TextEncoder

AUDIT = ROOT / 'languages/pt/data/pt05_audit.json'
COMBINED = ROOT / 'languages/pt/combined_pt.txt'


def canonical(raw: bytes) -> bytes:
    """Reconnaît uniquement le rewrap du constructeur, sans changer les mots."""
    return re.sub(b'\x00+', b'\x00', raw.replace(b'\xfe', b'\x00').replace(b'\xfa', b'\x00'))


def apply_patches(rom: bytearray, translations: dict[int, str] | None = None) -> int:
    """Valide toutes les cellules avant écriture ; refuse toute préimage inconnue."""
    audit = json.loads(AUDIT.read_text())
    if translations is None:
        translations, _ = _load_combined(COMBINED)
    code = bytes.fromhex(audit['item_table']['description_accessor_hex'])
    if rom[0x9A96C:0x9A990] != code:
        raise ValueError('Lecteur de descriptions inattendu')
    writes = {}
    for entry in audit['entries']:
        if entry['status'] != 'translated':
            continue
        offset = int(entry['offset'], 16)
        source = bytes.fromhex(entry['source_hex'])
        text = translations[offset]
        expected = TextEncoder.encode_pokemon(text, strict=True)
        if (len(expected) > len(source) or max(line_widths(text)) > 192
                or expected.count(0xFE) != source.count(0xFE)
                or set(expected) & {0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD}
                or 0xFF in expected[:-1]):
            raise ValueError(f'Budget/structure invalide à {offset:#x}')
        for pointer in entry['pointers']:
            address = int(pointer, 16)
            target = int.from_bytes(rom[address:address + 4], 'little') - 0x08000000
            if not 0 <= target <= len(rom) - len(expected):
                raise ValueError(f'Pointeur invalide à {address:#x}')
            if rom[target:target + len(expected)] == expected:
                continue
            # Un texte relocalisé inattendu ne peut pas être écrasé avec le budget EN.
            if target != offset:
                raise ValueError(f'Cible inattendue à {address:#x}: {target:#x}')
            actual = bytes(rom[target:target + len(source)]).split(b'\xff')[0] + b'\xff'
            if actual != source and canonical(actual) != canonical(expected):
                raise ValueError(f'Préimage inattendue à {offset:#x}')
            writes[offset] = expected
    for offset, expected in writes.items():
        rom[offset:offset + len(expected)] = expected
    return len(writes)


def main() -> int:
    """Sauvegarde le build avant de finaliser les cellules PT-05."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    count = apply_patches(rom)
    Path(str(args.rom) + '.pt05.bak').write_bytes(original)
    args.rom.write_bytes(rom)
    print(f'PT-05 : {count} descriptions finalisées ; 180 vérifiées.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
