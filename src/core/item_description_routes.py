"""Préimages et consommateurs explicites des descriptions d'objets hors extraction."""
from __future__ import annotations

import importlib
import json
from pathlib import Path

from src.core.text_codec import SPANISH_GLYPH_CHARS, TextDecoder, TextEncoder

ITEM_TABLE_BASE = 0x876074
ITEM_STRIDE = 44
DESCRIPTION_FIELD = 0x14
ROM_BASE = 0x08000000


class ItemDescriptionRoutes:
    """Enrichit le JSON existant ; l'insertion reste celle du builder commun."""

    def __init__(self, entries: dict[int, dict]) -> None:
        self.entries = entries

    @classmethod
    def load(cls, path: Path, source: bytes) -> ItemDescriptionRoutes:
        """Valide préimages, exhaustivité des pointeurs et consommateurs gItems."""
        data = json.loads(path.read_text(encoding='utf-8'))
        if data.get('version') != 1 or not isinstance(data.get('entries'), list):
            raise ValueError('Invalid item description routes')
        entries = {}
        spans = []
        used = set()
        for entry in data['entries']:
            offset = int(entry['offset'], 16)
            raw = bytes.fromhex(entry['source_hex'])
            refs = entry['pointer_offsets']
            if offset in entries or not raw.endswith(b'\xff') or source[offset:offset+len(raw)] != raw:
                raise ValueError(f'0x{offset:X}: préimage absente, différente ou dupliquée')
            needle = (ROM_BASE + offset).to_bytes(4, 'little')
            actual = []
            pos = source.find(needle)
            while pos >= 0:
                actual.append(pos)
                pos = source.find(needle, pos + 1)
            if not refs or sorted(refs) != actual or used.intersection(refs):
                raise ValueError(f'0x{offset:X}: consommateurs ambigus ou différents')
            consumers = [ITEM_TABLE_BASE + item * ITEM_STRIDE + DESCRIPTION_FIELD
                         for item in entry['item_ids']]
            if not consumers or any(p not in refs for p in consumers):
                raise ValueError(f'0x{offset:X}: consommateur gItems absent')
            entries[offset] = entry
            spans.append((offset, offset + len(raw)))
            used.update(refs)
        spans.sort()
        if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):  # noqa: RUF007 (Python 3.9)
            raise ValueError('Préimages de descriptions chevauchantes')
        return cls(entries)

    @staticmethod
    def normalize(item: dict) -> dict:
        """Réutilise le contrat de normalisation du builder, sans rewrap parallèle."""
        builder_type = importlib.import_module(
            'src.translators.19_build_translated_rom_generic'
        ).TranslatedROMBuilder
        builder = builder_type.__new__(builder_type)
        builder.english_texts = None
        return builder._normalize_translation_item(item['offset'], item)

    def enrich_json(self, path: Path, combined: dict[int, str]) -> int:
        """Reconstruit les entrées manquantes et déclare leur fenêtre fixe gItems."""
        payload = json.loads(path.read_text(encoding='utf-8'))
        items = payload['translations']
        existing = {}
        for item in items:
            offset = item['offset']
            if offset in self.entries and offset in existing:
                raise ValueError(f'0x{offset:X}: entrée JSON ambiguë')
            existing[offset] = item
        for offset, entry in self.entries.items():
            if not combined.get(offset):
                continue
            raw = bytes.fromhex(entry['source_hex'])
            item = existing.get(offset)
            if item is None:
                item = {'offset': offset}
                items.append(item)
            item.update(
                translation=combined[offset],
                original_text=TextDecoder.decode_pokemon(raw, preserve_unknown=True),
                english_raw_bytes=raw.hex(), original_length=len(raw)-1,
                max_length=len(raw), padding_available=0,
                pointer_offsets=entry['pointer_offsets'], encoding='pokemon',
                category='description', layout={'max_lines': 3, 'max_width': 176, 'preserve_line_count': False},
                allow_fallback=False, allow_truncate=False,
            )
            # Validation immédiate : une mauvaise traduction ne peut devenir un
            # build vert avec une chaîne EN conservée ou une commande supprimée.
            self.normalize(item)
        payload['total_translations'] = len(items)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        return len(items)

    def verify(self, rom: bytes, path: Path) -> None:
        """Refuse tout fallback, pointeur perdu ou allocation chevauchante en sortie."""
        spans = set()
        for item in json.loads(path.read_text(encoding='utf-8'))['translations']:
            offset = item['offset']
            if offset not in self.entries:
                continue
            normalized = self.normalize(item)
            encoded = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
            for ref in self.entries[offset]['pointer_offsets']:
                target = int.from_bytes(rom[ref:ref+4], 'little') - ROM_BASE
                if target < 0 or rom[target:target+len(encoded)] != encoded:
                    raise ValueError(f'0x{offset:X}: description non injectée au consommateur {ref:X}')
                spans.add((target, target+len(encoded)))
        spans = sorted(spans)
        if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):  # noqa: RUF007 (Python 3.9)
            raise ValueError('Allocations de descriptions chevauchantes')
