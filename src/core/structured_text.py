"""Injection bornée de textes dont la structure est prouvée par la ROM source."""
from __future__ import annotations

import importlib
import re
from pathlib import Path

from src.core import moves
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder
from src.core.text_reinserter import FreeSpaceAllocator


class StructuredTextPatch:
    """Résout les tables vivantes et repointe des textes sans modifier leurs voisins."""

    def __init__(self, source: bytes, definitions: list[dict], combined: Path):
        self.source = source
        self.definitions = definitions
        self.texts: dict[int, str] = {}
        for line in combined.read_text(encoding='utf-8').splitlines():
            match = re.match(r'^0x([0-9a-fA-F]+): ?(.*)$', line)
            if match:
                self.texts[int(match[1], 16)] = match[2]

    def entries(self) -> list[tuple[int, list[int], bytes]]:
        """Valide préimages, tables, commandes et budgets avant toute écriture."""
        builder_type = importlib.import_module(
            'src.translators.19_build_translated_rom_generic'
        ).TranslatedROMBuilder
        builder = builder_type.__new__(builder_type)
        builder.english_texts = None
        live_moves = {entry.index: entry for entry in moves.iter_entries(self.source)}
        entries = []
        used_refs: set[int] = set()
        for definition in self.definitions:
            offset = int(definition['offset'], 16)
            raw = bytes.fromhex(definition['source_hex'])
            if not raw.endswith(b'\xff') or self.source[offset:offset + len(raw)] != raw:
                raise ValueError(f'0x{offset:X}: préimage EN différente')
            refs = definition['references']
            if not refs or used_refs.intersection(refs):
                raise ValueError(f'0x{offset:X}: références absentes ou dupliquées')
            used_refs.update(refs)
            for index in definition['move_ids']:
                entry = live_moves.get(index)
                if entry is None or entry.text_offset != offset or entry.struct_offset not in refs:
                    raise ValueError(f'0x{offset:X}: table des attaques différente')
            for ref in refs:
                if int.from_bytes(self.source[ref:ref + 4], 'little') != offset + moves.ROM_POINTER_BASE:
                    raise ValueError(f'0x{offset:X}: pointeur EN invalide à {ref:X}')
            text = self.texts[offset]
            for escape, code in [(r'\n', '\n'), (r'\l', '<0xFA>'), (r'\p', '<0xFB>')]:
                text = text.replace(escape, code)
            normalized = builder._normalize_translation_item(offset, {
                'translation': text, 'english_raw_bytes': raw.hex(),
                'layout': definition['layout'], 'encoding': 'pokemon',
            })
            encoded = TextEncoder.encode_pokemon(
                normalized['translation'], skip_aliases=GERMAN_UMLAUT_CHARS
            )
            entries.append((offset, refs, encoded))
        return entries

    def apply(self, rom: bytearray) -> dict[str, int]:
        """Injecte atomiquement dans l'espace libre final, sans réutiliser un voisin."""
        entries = self.entries()
        working = bytearray(rom)
        allocator = FreeSpaceAllocator(working)
        relocated = 0
        for offset, refs, encoded in entries:
            targets = [int.from_bytes(working[p:p + 4], 'little') - moves.ROM_POINTER_BASE for p in refs]
            if any(not 0 <= target < len(working) for target in targets):
                raise ValueError(f'0x{offset:X}: cible vivante hors ROM')
            if all(working[target:target + len(encoded)] == encoded for target in targets):
                continue
            # Ne jamais écrire sur place : une cellule peut être partagée avec
            # un texte hors lot ou avoir été raccourcie par un patch précédent.
            target = allocator.allocate(len(encoded))
            if target is None:
                raise ValueError(f'0x{offset:X}: espace libre insuffisant')
            working[target:target + len(encoded)] = encoded
            pointer = (target + moves.ROM_POINTER_BASE).to_bytes(4, 'little')
            for ref in refs:
                working[ref:ref + 4] = pointer
            relocated += 1
        self.verify(working)
        rom[:] = working
        return {'verified': len(entries), 'relocated': relocated}

    def verify(self, rom: bytes | bytearray) -> None:
        """Contrôle chaque cible, son terminateur et l'absence de chevauchement."""
        spans = set()
        for offset, refs, encoded in self.entries():
            for ref in refs:
                target = int.from_bytes(rom[ref:ref + 4], 'little') - moves.ROM_POINTER_BASE
                if not 0 <= target <= len(rom) - len(encoded) or rom[target:target + len(encoded)] != encoded:
                    raise ValueError(f'0x{offset:X}: octets DE différents à {target:X}')
                spans.add((target, target + len(encoded)))
        previous_end = -1
        for start, end in sorted(spans):
            if start < previous_end:
                raise ValueError('Chevauchement des textes structurés')
            previous_end = end
