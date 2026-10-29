#!/usr/bin/env python3
"""Achemine uniquement les sept dialogues et huit consommateurs prouvés B-1016."""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.fr.patches.meteorite_dialogue import load_combined
from scripts.apply_inline_overrides_fr import (
    _apply_control_placeholders,
    _extract_control_sequences_from_raw,
    _normalize_text,
    _read_raw_entry,
)
from src.core.dialogue_linewrap import line_widths, rewrap
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator

GBA_BASE = 0x08000000
# Consommateurs vérifiés dans la source EN : aucun balayage de pointeurs.
TARGETS = {
    0x7A9A75: (0x74B0AA,),
    0x1EEE8BE: (0x1E5B206,),
    0x1F0F004: (0x1E70293,),
    0x1F8E271: (0x1E9FA40,),
    0x1F4C2ED: (0x1E6D700,),
    0x1FB052C: (0x1EAF7F5,),
    0x1FB07FE: (0x1285745, 0x1EAF820),
}


def prepared_text(text: str, source: bytes, offset: int) -> str:
    """Résout les commandes EN et ajuste les lignes sans déplacer les pages."""
    entry = _read_raw_entry(source, offset, 'pokemon')
    if not entry:
        raise ValueError(f'source non terminée à {offset:#x}')
    normalized = _apply_control_placeholders(
        _normalize_text(text), entry['decoded_text'], entry['raw_bytes'])
    # Chaque FB reste une frontière dure ; les FA sont les défilements de lignes.
    wrapped = '<0xFB>'.join(rewrap(page) for page in normalized.split('<0xFB>'))
    if max(line_widths(wrapped)) > 192:
        raise ValueError(f'budget de boîte dépassé à {offset:#x}')
    return wrapped


def encode_dialogue(text: str, source: bytes, offset: int) -> bytes:
    """Encode le DE avec umlauts et contrôle l'ordre exact des commandes."""
    encoded = TextEncoder.encode(prepared_text(text, source, offset), 'pokemon',
                                 skip_aliases=GERMAN_UMLAUT_CHARS)
    original = bytes.fromhex(_read_raw_entry(source, offset, 'pokemon')['raw_bytes'])
    def commands(raw: bytes) -> list[list[int]]:
        return [seq for seq in _extract_control_sequences_from_raw(raw)
                if seq[0] not in (0xFA, 0xFB)]
    if commands(encoded) != commands(original):
        raise ValueError(f'commandes différentes à {offset:#x}')
    return encoded


def apply(rom: bytearray, combined: dict[int, str], source: bytes) -> list[dict]:
    """Valide tous les sites, puis relocalise atomiquement les copies nécessaires."""
    planned = []
    for offset, sites in TARGETS.items():
        for site in sites:
            if struct.unpack_from('<I', source, site)[0] != GBA_BASE + offset:
                raise ValueError(f'pointeur source inattendu à {site:#x}')
            current = struct.unpack_from('<I', rom, site)[0] - GBA_BASE
            if not 0 <= current < len(rom):
                raise ValueError(f'pointeur cible invalide à {site:#x}')
        planned.append((offset, sites, encode_dialogue(combined[offset], source, offset)))
    result = bytearray(rom)
    allocator = FreeSpaceAllocator(result)
    report = []
    for offset, sites, encoded in planned:
        before = [struct.unpack_from('<I', result, site)[0] - GBA_BASE for site in sites]
        target = next((p for p in before if result[p:p+len(encoded)] == encoded), None)
        if target is None:
            target = allocator.allocate(len(encoded))
            if target is None:
                raise ValueError(f'espace libre insuffisant pour {offset:#x}')
            result[target:target+len(encoded)] = encoded
        for site in sites:
            struct.pack_into('<I', result, site, target + GBA_BASE)
        report.append({'offset': offset, 'sites': list(sites), 'before': before,
                       'target': target, 'size': len(encoded)})
    rom[:] = result
    return report


def main() -> int:
    """Applique le patch DE en fin de build avec sauvegarde préalable."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', required=True, type=Path)
    args = parser.parse_args()
    original = args.rom.read_bytes()
    rom = bytearray(original)
    report = apply(rom, load_combined(ROOT / 'languages/de/combined_de.txt'),
                   (ROOT / 'input/roms/englishrom.gba').read_bytes())
    if rom != original:
        Path(f'{args.rom}.bak').write_bytes(original)
        args.rom.write_bytes(rom)
    for row in report:
        print(f"dialogue DE {row['offset']:#x} → {row['target']:#x} "
              f"({row['size']} octets), sites: {[hex(s) for s in row['sites']]}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
