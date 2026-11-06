"""Préservation opt-in de préimages partagées, via le réinserteur existant."""
from __future__ import annotations

import json
from pathlib import Path

from src.core.item_description_routes import ItemDescriptionRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder


class TextSourcePreservation:
    """Garde les consommateurs non sélectionnés sans qualifier leur texte."""

    def __init__(self, records: list[dict], aliases: dict[int, dict], source: bytes) -> None:
        self.records = records
        self.routes: dict[int, dict] = {}
        self.blocked: set[int] = set()
        self.guards: list[dict] = []
        for record in records:
            key = int(record['offset'], 16)
            raw = bytes.fromhex(record['english_raw_hex'])
            if source[key:key + len(raw)] != raw:
                raise ValueError(f'0x{key:X}: préimage de préservation différente')
            refs = record['direct_references'] + record['interior_references']
            for ref in refs:
                start = int(ref['context_start'], 16)
                context = bytes.fromhex(ref['context_hex'])
                if source[start:start + len(context)] != context:
                    raise ValueError(f'0x{start:X}: contexte de lecteur différent')
            length = record.get('protected_length', len(raw))
            self.guards.append({'offset': record['offset'], 'hex': raw[:length].hex()})
            if record.get('nontext', False):
                self.blocked.add(key)
                continue
            live = aliases[key]['live_offset'] if key in aliases else key
            pointers = aliases[key]['pointer_offsets'] if key in aliases else [int(p, 16) for p in record['pointer_offsets']]
            self.routes[live] = {
                'english_raw_bytes': raw[live-key:].hex(), 'pointer_offsets': pointers,
                'force_relocation': True, 'preserve_control_flow': True,
                'allow_fallback': False, 'allow_truncate': False,
                'original_length': len(raw)-(live-key)-1,
                'max_length': len(raw)-(live-key), 'padding_available': 0,
            }
            if key in aliases and 'layout' in aliases[key]:
                self.routes[live].update(layout=aliases[key]['layout'], strict_encoded_layout=True, category='description')

    def enrich(self, items: list[dict], keys: set[int], aliases: dict[int, dict]) -> None:
        """Force la relocalisation des seuls débuts explicitement sélectionnés."""
        if self.blocked & keys:
            raise ValueError('Clé de script ou donnée non textuelle hors écriture')
        resolved = {aliases[k]['live_offset'] if k in aliases else k for k in keys}
        required = resolved & self.routes.keys()
        seen = set()
        for item in items:
            offset = item['offset']
            if offset not in required:
                continue
            if offset in seen:
                raise ValueError('Route de préservation dupliquée')
            seen.add(offset)
            route = self.routes[offset]
            if not route['pointer_offsets']:
                raise ValueError(f'0x{offset:X}: lecteur à qualifier avant écriture de la préimage partagée')
            item.update(route)
            item.pop('raw_bytes', None)
            ItemDescriptionRoutes.normalize(item)
        if seen != required:
            raise ValueError('Entrée à préserver disparue dans le CSV/JSON')

    def verify(self, rom: bytes, path: Path, combined: dict[int, str], aliases: dict[int, dict]) -> None:
        """Vérifie préimages, lecteurs non sélectionnés et textes finaux sélectionnés."""
        if self.blocked & {k for k, text in combined.items() if text}:
            raise ValueError('Clé non textuelle hors écriture')
        items = json.loads(path.read_text(encoding='utf-8'))['translations']
        selected = {aliases[k]['live_offset'] if k in aliases else k: text
                    for k, text in combined.items() if text}
        selected_items = [item['offset'] for item in items if item['offset'] in selected]
        if len(selected_items) != len(set(selected_items)):
            raise ValueError('Route sélectionnée dupliquée dans le JSON final')
        present = {item['offset']: item for item in items}
        updated_sites = set()
        guards = [dict(g) for g in self.guards]
        # Une structure hors traduction peut contenir le pointeur d'une autre
        # clé sélectionnée (panneau). Seul ce champ prouvé peut être repointé ;
        # les opcodes et données restent intégralement protégés.
        for record, guard in zip(self.records, guards):
            if not record.get('nontext'):
                continue
            start = int(record['offset'], 16)
            expected = bytearray.fromhex(guard['hex'])
            for ref in record['interior_references']:
                key = int(ref['target'], 16)
                if ref['target'] not in record['selected_interior_keys'] or key not in selected:
                    continue
                if ref['qualification'] != 'loadpointer_bank0' or key not in present:
                    raise ValueError('Consommateur intérieur sélectionné non qualifié')
                raw = bytes.fromhex(record['english_raw_hex'])[key-start:]
                item = dict(present[key], translation=selected[key],
                            english_raw_bytes=raw.hex(), preserve_control_flow=True)
                normalized = ItemDescriptionRoutes.normalize(item)
                encoded = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
                site = int(ref['offset'], 16)
                target = int.from_bytes(rom[site:site+4], 'little')-0x08000000
                if target < 0 or rom[target:target+len(encoded)] != encoded:
                    raise ValueError('Texte intérieur sélectionné non injecté')
                updated_sites.add(site)
                if start <= site and site+4 <= start+len(expected):
                    expected[site-start:site-start+4] = rom[site:site+4]
            guard['hex'] = expected.hex()
        ItemDescriptionRoutes.verify_guards(rom, guards)
        for offset in selected.keys() & self.routes.keys():
            if not self.routes[offset]['pointer_offsets']:
                raise ValueError('Lecteur non qualifié dans le JSON final')
            if offset not in present:
                raise ValueError('Entrée préservée absente du JSON final')
            item = dict(present[offset], **self.routes[offset])
            item['translation'] = selected[offset]
            normalized = ItemDescriptionRoutes.normalize(item)
            encoded = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
            for site in self.routes[offset]['pointer_offsets']:
                updated_sites.add(site)
                target = int.from_bytes(rom[site:site+4], 'little')-0x08000000
                if target == offset or target < 0 or rom[target:target+len(encoded)] != encoded:
                    raise ValueError(f'0x{offset:X}: relocalisation obligatoire non vérifiée')
        for record in self.records:
            for ref in record['direct_references'] + record['interior_references']:
                site = int(ref['offset'], 16)
                if site in updated_sites:
                    continue
                target = int(ref.get('target', record['offset']), 16)
                if rom[site:site+4] != (0x08000000+target).to_bytes(4, 'little'):
                    raise ValueError(f'0x{site:X}: consommateur non sélectionné modifié')
