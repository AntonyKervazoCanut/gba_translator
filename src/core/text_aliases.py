"""Résolution opt-in des identifiants contractuels vers des textes ROM vivants."""
from __future__ import annotations

import csv
import json
from pathlib import Path


class TextAliases:
    """Contrat explicite, borné par préimages et références binaires exactes."""

    def __init__(self, entries: dict[int, dict], guards: list[dict] | None = None, excluded: set[int] | None = None) -> None:
        self.entries = entries
        self.guards = guards or []
        self.excluded = excluded or set()
        self.preservation = None

    @classmethod
    def load(cls, path: Path, english_rom: bytes) -> TextAliases:
        """Charge le contrat et refuse toute dérive de texte ou de pointeur EN."""
        data = json.loads(path.read_text(encoding='utf-8'))
        if data.get('version') != 1 or not isinstance(data.get('aliases'), list):
            raise ValueError('Invalid text alias schema')
        from src.core.item_description_routes import ItemDescriptionRoutes
        guards = list(data.get('fonts', {}).values())
        if data.get('keypad_icons'):
            guards.append(data['keypad_icons'])
        guards.extend(data.get('guards', []))
        ItemDescriptionRoutes.verify_guards(english_rom, guards)
        entries = {}
        targets = set()
        excluded = set()
        for record in data.get('excluded', []):
            for field in ('contract_offset', 'live_offset'):
                excluded.add(int(record[field], 16))
        for record in data['aliases'] + data.get('excluded', []):
            entry = dict(record)
            for field in ('contract_offset', 'live_offset'):
                entry[field] = int(entry[field], 16)
            if not isinstance(entry.get('english_only', False), bool):
                raise TypeError('English-only opt-in must be boolean')
            if entry.get('english_only', False):
                if entry.get('spanish_offset') is not None or 'spanish_raw_hex' in entry:
                    raise ValueError('English-only alias cannot declare a Spanish match')
                entry['spanish_offset'] = None
            else:
                if entry.get('spanish_offset') is None:
                    raise ValueError('Spanish match required without English-only opt-in')
                entry['spanish_offset'] = int(entry['spanish_offset'], 16)
            key, live = entry['contract_offset'], entry['live_offset']
            if key in entries or live in targets or key == live:
                raise ValueError('Text alias collision')
            prefix = bytes.fromhex(entry['prefix_hex'])
            raw = bytes.fromhex(entry['english_raw_hex'])
            if not prefix or live != key + len(prefix) or not raw.endswith(b'\xff'):
                raise ValueError('Invalid text alias span')
            if english_rom[key:live + len(raw)] != prefix + raw:
                raise ValueError(f'0x{key:08X}: alias preimage mismatch')
            false_pointer = (0x08000000 + key).to_bytes(4, 'little')
            if false_pointer in english_rom:
                raise ValueError(f'0x{key:08X}: contractual start has a direct pointer')
            pointers = [int(p, 16) for p in entry['pointer_offsets']]
            needle = (0x08000000 + live).to_bytes(4, 'little')
            actual = []
            pos = english_rom.find(needle)
            while pos >= 0:
                actual.append(pos)
                pos = english_rom.find(needle, pos + 1)
            if not pointers or sorted(pointers) != actual:
                raise ValueError(f'0x{key:08X}: alias pointer mismatch')
            entry['pointer_offsets'] = pointers
            if 'layout' in entry:
                layout = dict(entry['layout'])
                font = data.get('fonts', {}).get(layout.get('font'), {})
                if len(bytes.fromhex(font.get('hex', ''))) != 512:
                    raise ValueError('Engine font widths required for menu alias')
                layout['glyph_widths_hex'] = font['hex']
                layout['keypad_widths'] = list(bytes.fromhex(data['keypad_icons']['hex'])[2::4])
                entry['layout'] = layout
            entries[key] = entry
            targets.add(live)
            if key in excluded:
                # Une exclusion ne doit pas devenir une écriture muette après
                # les patches : conserver aussi préfixe, texte et table dormante.
                guards.append({'offset': f'0x{key:X}', 'hex': (prefix + raw).hex()})
                guards.extend({'offset': f'0x{p:X}', 'hex': needle.hex()} for p in pointers)
        if targets & entries.keys():
            raise ValueError('Text alias chain/collision')
        spans = sorted((e['contract_offset'], e['live_offset'] + len(bytes.fromhex(e['english_raw_hex']))) for e in entries.values())
        if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):  # noqa: RUF007
            raise ValueError('Overlapping text aliases')
        result = cls({key: entry for key, entry in entries.items() if key not in excluded}, guards, excluded)
        if data.get('preserved_sources'):
            from src.core.text_source_preservation import TextSourcePreservation
            result.preservation = TextSourcePreservation(data['preserved_sources'], result.entries, english_rom)
        return result

    def check_keys(self, keys: set[int]) -> None:
        """Refuse deux traductions revendiquant le même texte, même identiques."""
        for key, entry in self.entries.items():
            if key in keys and entry['live_offset'] in keys:
                raise ValueError(f'0x{key:08X}: translation key collision')
        if keys & self.excluded:
            raise ValueError('Clé exclue : table dormante sans consommateur moteur actuel')

    @staticmethod
    def _extracted_map(path: Path, offsets: set[int]) -> dict[int, dict]:
        entries = {}
        for entry in json.loads(path.read_text(encoding='utf-8'))['texts']:
            offset = entry['offset']
            if offset not in offsets:
                continue
            if offset in entries:
                raise ValueError(f'0x{offset:08X}: ambiguous extraction')
            entries[offset] = entry
        return entries

    def prepare_csv(self, source: Path, output: Path, keys: set[int],
                    offset_map: Path, spanish_rom: bytes, spanish_extract: Path,
                    english_extract: Path) -> None:
        """Crée une vue contractuelle du CSV sans modifier les sources ni les lots."""
        self.check_keys(keys)
        mapping = json.loads(offset_map.read_text(encoding='utf-8'))['offset_map']
        english = self._extracted_map(english_extract, {e['live_offset'] for e in self.entries.values()})
        spanish = self._extracted_map(spanish_extract, {e['spanish_offset'] for e in self.entries.values()})
        with source.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            fields = list(reader.fieldnames)
            rows = list(reader)
        if 'spanish_text' not in fields:
            fields.append('spanish_text')
        by_offset = {}
        for row in rows:
            by_offset.setdefault(int(row['offset'], 16), []).append(row)
        for key, entry in self.entries.items():
            live, es = entry['live_offset'], entry['spanish_offset']
            en = english.get(live, {})
            if bytes.fromhex(en.get('raw_bytes', '')) != bytes.fromhex(entry['english_raw_hex']):
                raise ValueError(f'0x{key:08X}: English extraction mismatch')
            matches = [e for e in mapping if e['english_offset'] == live]
            if entry.get('english_only', False):
                if len(matches) != 1 or matches[0].get('status') != 'only_in_english' or matches[0].get('spanish_offset') is not None:
                    raise ValueError(f'0x{key:08X}: English-only offset map changed')
                extracted = None
            else:
                if len(matches) != 1 or matches[0]['spanish_offset'] != es or matches[0].get('status') != 'matched':
                    raise ValueError(f'0x{key:08X}: ambiguous or changed offset map')
                raw = bytes.fromhex(entry['spanish_raw_hex'])
                if not raw.endswith(b'\xff') or spanish_rom[es:es + len(raw)] != raw:
                    raise ValueError(f'0x{key:08X}: Spanish preimage mismatch')
                for pointer in entry['pointer_offsets']:
                    if spanish_rom[pointer:pointer + 4] != (0x08000000 + es).to_bytes(4, 'little'):
                        raise ValueError(f'0x{key:08X}: Spanish pointer mismatch')
                extracted = spanish.get(es, {})
                if bytes.fromhex(extracted.get('raw_bytes', '')) != raw:
                    raise ValueError(f'0x{key:08X}: Spanish extraction mismatch')
            if key not in keys:
                continue
            if key in by_offset or len(by_offset.get(live, [])) != 1:
                raise ValueError(f'0x{key:08X}: ambiguous CSV source')
            row = by_offset[live][0]
            row['offset'] = f'0x{key:08X}'
            row['original_text'] = en.get('decoded_text') or en['text']
            row['spanish_text'] = (extracted.get('decoded_text') or extracted['text']) if extracted else ''
            # The exact original span is the budget; never include prefix/padding.
            length = len(bytes.fromhex(entry['english_raw_hex']))
            row.update(original_length=length, padding_available=0, real_max_length=length)
        with output.open('w', encoding='utf-8', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def resolve_json(self, path: Path, keys: set[int]) -> None:
        """Enrichit le JSON consommé par le builder avec adresse et préimage vivantes."""
        payload = json.loads(path.read_text(encoding='utf-8'))
        items = payload['translations']
        self.check_keys({e['offset'] for e in items})
        seen = set()
        for item in items:
            key = item['offset']
            if key not in self.entries:
                continue
            if key in seen:
                raise ValueError('Duplicate contractual translation')
            seen.add(key)
            entry = self.entries[key]
            item.update(contract_offset=key, offset=entry['live_offset'],
                        english_raw_bytes=entry['english_raw_hex'],
                        pointer_offsets=entry['pointer_offsets'],
                        original_length=len(bytes.fromhex(entry['english_raw_hex'])) - 1,
                        max_length=len(bytes.fromhex(entry['english_raw_hex'])),
                        allow_fallback=False, allow_truncate=False, preserve_control_flow=True,
                        spanish_offset=entry['spanish_offset'])
            if 'layout' in entry:
                item.update(layout=entry['layout'], strict_encoded_layout=True, category='description')
            from src.core.item_description_routes import ItemDescriptionRoutes
            ItemDescriptionRoutes.normalize(item)
        if seen != keys & self.entries.keys():
            raise ValueError('Contractual translation dropped during conversion')
        if self.preservation is not None:
            self.preservation.enrich(items, keys, self.entries)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    def verify(self, rom: bytes, path: Path, combined: dict[int, str]) -> None:
        """Vérifie les préfixes et tous les consommateurs après les patches finaux."""
        from src.core.item_description_routes import ItemDescriptionRoutes
        from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

        ItemDescriptionRoutes.verify_guards(rom, self.guards)
        if self.preservation is not None:
            self.preservation.verify(rom, path, combined, self.entries)
        self.check_keys(set(combined))
        required = {key for key in self.entries if combined.get(key)}
        items = json.loads(path.read_text(encoding='utf-8'))['translations']
        present = [item['contract_offset'] for item in items if 'contract_offset' in item]
        if set(present) != required or len(present) != len(set(present)):
            raise ValueError('Contractual translation dropped or duplicated after conversion')
        for key, entry in self.entries.items():
            if rom[key:entry['live_offset']] != bytes.fromhex(entry['prefix_hex']):
                raise ValueError(f'0x{key:08X}: alias prefix changed')
        spans = set()
        for key in required:
            entry = self.entries[key]
            # Les sources manuelles et le contrat restent autorités, même si le
            # JSON intermédiaire a perdu sa traduction ou ses garde-fous.
            item = dict(next(item for item in items if item.get('contract_offset') == key))
            item.update(translation=combined[key], english_raw_bytes=entry['english_raw_hex'],
                        preserve_control_flow=True)
            if 'layout' in entry:
                item.update(layout=entry['layout'], strict_encoded_layout=True)
            normalized = ItemDescriptionRoutes.normalize(item)
            encoded = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
            for ref in entry['pointer_offsets']:
                target = int.from_bytes(rom[ref:ref + 4], 'little') - 0x08000000
                if target < 0 or rom[target:target + len(encoded)] != encoded:
                    raise ValueError(f'0x{key:08X}: alias non injecté au consommateur {ref:X}')
                spans.add((target, target + len(encoded)))
        spans = sorted(spans)
        if any(end > start for (_, end), (start, _) in zip(spans, spans[1:])):  # noqa: RUF007
            raise ValueError('Overlapping alias allocations')
