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

    def __init__(self, entries: dict[int, dict], excluded: set[int] | None = None, guards: list[dict] | None = None) -> None:
        self.entries = entries
        self.excluded = excluded or set()
        self.guards = guards or []

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
            cls.validate_consumers(entry, source)
            entries[offset] = entry
            spans.append((offset, offset + len(raw)))
            used.update(refs)
        spans.sort()
        if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):  # noqa: RUF007 (Python 3.9)
            raise ValueError('Préimages de descriptions chevauchantes')
        guards = data.get('guards', [])
        cls.verify_guards(source, guards)
        excluded = {int(entry['offset'], 16) for entry in data.get('excluded', [])}
        if excluded & entries.keys():
            raise ValueError('Routes et exclusions se chevauchent')
        return cls(entries, excluded, guards)

    @staticmethod
    def verify_guards(rom: bytes, guards: list[dict]) -> None:
        """Refuse une modification des racines, routines ou métadonnées gelées."""
        for guard in guards:
            offset = int(guard['offset'], 16)
            raw = bytes.fromhex(guard['hex'])
            if rom[offset:offset + len(raw)] != raw:
                raise ValueError(f'0x{offset:X}: racine ou métadonnées modifiées')

    @staticmethod
    def validate_consumers(entry: dict, source: bytes) -> None:
        """Vérifie la fenêtre gItems à partir de ses consommateurs."""
        if entry.get('layout', ItemDescriptionRoutes.layout_metadata()['layout']) != ItemDescriptionRoutes.layout_metadata()['layout']:
            raise ValueError(f"{entry['offset']}: budget objet différent")
        consumers = [ITEM_TABLE_BASE + item * ITEM_STRIDE + DESCRIPTION_FIELD
                     for item in entry['item_ids']]
        if not consumers or any(p not in entry['pointer_offsets'] for p in consumers):
            raise ValueError(f"{entry['offset']}: consommateur gItems absent")

    @staticmethod
    def layout_metadata(entry: dict | None = None) -> dict:
        """Déclare les contraintes de la fenêtre des descriptions."""
        return {'category': 'description', 'strict_encoded_layout': True, 'layout': {
            'max_lines': 3, 'max_width': 176, 'preserve_line_count': False}}

    @staticmethod
    def normalize(item: dict) -> dict:
        """Réutilise le contrat de normalisation du builder, sans rewrap parallèle."""
        module = importlib.import_module('src.translators.19_build_translated_rom_generic')
        builder = module.TranslatedROMBuilder.__new__(module.TranslatedROMBuilder)
        builder.english_texts = None
        builder.config = module.BuildConfig(source_rom=Path(), preserve_spanish_glyphs=True)
        return builder._normalize_translation_item(item['offset'], item)

    def enrich_json(self, path: Path, combined: dict[int, str]) -> int:
        """Reconstruit les entrées manquantes et déclare leur fenêtre fixe gItems."""
        if self.excluded & {offset for offset, text in combined.items() if text}:
            raise ValueError('Clé conservée sans injection : consommateur actuel hors lot ou donnée non textuelle')
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
                max_length=entry.get('fixed_capacity', len(raw)), padding_available=0,
                pointer_offsets=[] if entry.get('fixed_capacity') else entry['pointer_offsets'], encoding='pokemon',
                **self.layout_metadata(entry),
                allow_fallback=False, allow_truncate=False,
            )
            item.pop('raw_bytes', None)
            # Validation immédiate : une mauvaise traduction ne peut devenir un
            # build vert avec une chaîne EN conservée ou une commande supprimée.
            self.normalize(item)
        payload.setdefault('required_routes', {})[type(self).__name__] = [
            offset for offset in self.entries if combined.get(offset)
        ]
        payload['total_translations'] = len(items)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        return len(items)

    def verify(self, rom: bytes, path: Path, combined: dict[int, str] | None = None) -> None:
        """Refuse tout fallback, pointeur perdu ou allocation chevauchante en sortie."""
        self.verify_guards(rom, self.guards)
        payload = json.loads(path.read_text(encoding='utf-8'))
        required = set(payload.get('required_routes', {}).get(type(self).__name__, []))
        if combined is not None:
            required.update(offset for offset in self.entries if combined.get(offset))
        present = [item['offset'] for item in payload['translations'] if item['offset'] in self.entries]
        if required - set(present) or len(present) != len(set(present)):
            raise ValueError('Entrée acheminée disparue ou dupliquée après conversion')
        spans = set()
        for item in payload['translations']:
            offset = item['offset']
            if offset not in self.entries:
                continue
            normalized = self.normalize(item)
            encoded = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
            entry = self.entries[offset]
            for ref in ([offset] if entry.get('fixed_capacity') else entry['pointer_offsets']):
                target = offset if entry.get('fixed_capacity') else int.from_bytes(rom[ref:ref+4], 'little') - ROM_BASE
                if target < 0 or rom[target:target+len(encoded)] != encoded:
                    raise ValueError(f'0x{offset:X}: description non injectée au consommateur {ref:X}')
                spans.add((target, target+len(encoded)))
        spans = sorted(spans)
        if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):  # noqa: RUF007 (Python 3.9)
            raise ValueError('Allocations de descriptions chevauchantes')


class SystemTextRoutes(ItemDescriptionRoutes):
    """Réutilise le routage validé pour les consommateurs système paginés."""

    @staticmethod
    def validate_consumers(entry: dict, source: bytes) -> None:
        """Vérifie aussi les opcodes lorsqu'un consommateur est un script."""
        for offset, expected in entry.get('script_opcodes', {}).items():
            site = int(offset, 16)
            raw = bytes.fromhex(expected)
            if site + len(raw) not in entry['pointer_offsets'] or source[site:site+len(raw)] != raw:
                raise ValueError(f"{entry['offset']}: opcode consommateur différent")

    @staticmethod
    def layout_metadata(entry: dict | None = None) -> dict:
        """Conserve le contrat de commandes existant, notamment FA et FB."""
        if entry and 'layout' in entry:
            return {'category': 'description', 'strict_encoded_layout': True, 'layout': entry['layout']}
        return {'category': 'dialogue', 'preserve_control_flow': True}
