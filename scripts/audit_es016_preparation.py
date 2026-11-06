"""Relève un lot ES sans modifier les traductions ni déduire les zones de l'adresse."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.apply_inline_overrides_fr import FC_ARG_COUNTS, RAW_ARG_PREFIXES
from src.core.text_codec import TextDecoder


def snapshot(rom: bytes, offset: int) -> dict:
    """Lit jusqu'au FF hors arguments ; le décodage reste un diagnostic."""
    pos = offset
    parts, commands = [], []
    while pos < len(rom):
        value = rom[pos]
        if value == 0xFF:
            pos += 1
            break
        if value == 0xFC:
            size = 2 + FC_ARG_COUNTS.get(rom[pos + 1], 0)
        elif value in RAW_ARG_PREFIXES:
            size = 1 + RAW_ARG_PREFIXES[value]
        elif value in (0xFA, 0xFB):
            size = 1
        else:
            parts.append(r'\n' if value == 0xFE else TextDecoder.decode_pokemon(
                bytes([value]), preserve_unknown=True))
            pos += 1
            continue
        raw = rom[pos:pos + size]
        commands.append({'relative_offset': pos - offset, 'hex': raw.hex()})
        parts.extend(f'<0x{b:02X}>' for b in raw)
        pos += size
    else:
        raise ValueError(f'Unterminated source at {offset:#x}')
    return {'raw_hex': rom[offset:pos].hex(), 'bytes_including_ff': pos - offset,
            'decoded_control_aware': ''.join(parts), 'commands': commands}


def prepare(root: Path = ROOT, lot_id: str = 'ES-016') -> dict:
    """Fige les préimages, les références binaires et les correspondances ES."""
    source = (root / 'input/roms/englishrom.gba').read_bytes()
    spanish = (root / 'input/roms/spanishrom.gba').read_bytes()
    lots = json.loads((root / 'docs/analysis/es/lots.json').read_text())
    keys = next(lot['offsets'] for lot in lots if lot['id'] == lot_id)
    offsets = [int(key, 16) for key in keys]
    with (root / 'docs/analysis/es/inventaire.csv').open(newline='') as stream:
        inventory = {row['offset']: row for row in csv.DictReader(stream)
                     if row['lot'] == lot_id}
    mapping_path = root / 'output/differences/pointer_offset_map.json'
    mappings = defaultdict(list)
    for item in json.loads(mapping_path.read_text())['offset_map']:
        mappings[item['english_offset']].append(item)
    refs = defaultdict(list)
    # Toutes les occurrences, sans hypothèse d'alignement. Une occurrence n'est
    # pas une preuve de consommateur texte (PCM et bytecode peuvent coïncider).
    low, high = min(offsets) - 32, max(offsets) + 4096
    pos = source.find(b'\x08', 3)
    while pos >= 0:
        target = int.from_bytes(source[pos-3:pos+1], 'little') - 0x08000000
        if low <= target <= high:
            refs[target].append(pos - 3)
        pos = source.find(b'\x08', pos + 1)

    def references(target: int) -> list[dict]:
        return [{'offset': f'0x{site:08X}', 'context_start': f'0x{site-4:08X}',
                 'context_hex': source[site-4:site+12].hex()} for site in refs.get(target, [])]

    def matches(target: int) -> list[dict]:
        return [{'mapping': item, 'spanish_snapshot': snapshot(spanish, item['spanish_offset'])
                 if item.get('spanish_offset') is not None else None}
                for item in mappings[target]]

    aliases = json.loads((root / 'languages/es-maint/text_aliases.json').read_text())
    configured = {int(a['contract_offset'], 16) for a in aliases['aliases']}
    records = []
    for key, offset in zip(keys, offsets):
        image = snapshot(source, offset)
        end = offset + image['bytes_including_ff']
        nearby = []
        if not refs.get(offset):
            for live in range(offset + 1, min(offset + 33, end)):
                if refs.get(live):
                    nearby.append({'offset': f'0x{live:08X}',
                                   'prefix_hex': source[offset:live].hex(),
                                   'references': references(live),
                                   'snapshot': snapshot(source, live),
                                   'in_same_lot': live in offsets,
                                   'offset_map_matches': matches(live)})
        records.append({'offset': key, 'inventory': inventory[key],
                        'english_snapshot': image, 'direct_references': references(offset),
                        'offset_map_matches': matches(offset), 'nearby_candidates': nearby,
                        'interior_references': [
                            {'offset': f'0x{target:08X}', 'references': references(target)}
                            for target in sorted(refs) if offset < target < end],
                        'alias_configured': offset in configured,
                        'zone': None,
                        'translation_status': 'non traité — qualification des scripts requise',
                        'injection_certified': False})
    protected = ['languages/en/combined_en.txt', 'languages/es/combined_es.txt',
                 'languages/fr/combined_fr.txt', 'languages/es-maint/combined_es-maint.txt',
                 'languages/es-maint/protected_entries.yaml', 'languages/es-maint/glossary.md']
    return {'lot': lot_id, 'status': 'préparation technique ; lot non livré',
            'source_sha256': hashlib.sha256(source).hexdigest(),
            'spanish_sha256': hashlib.sha256(spanish).hexdigest(),
            'offset_map_sha256': hashlib.sha256(mapping_path.read_bytes()).hexdigest(),
            'preserved_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                                 for name in protected},
            'summary': {'entries': len(records),
                        'inventory_states': dict(Counter(r['inventory']['etat'] for r in records)),
                        'with_direct_references': sum(bool(r['direct_references']) for r in records),
                        'with_interior_references': sum(bool(r['interior_references']) for r in records),
                        'max_bytes_including_ff': max(r['english_snapshot']['bytes_including_ff']
                                                      for r in records)},
            'entries': records}


def probe_routing(root: Path = ROOT, lot_id: str = 'ES-016') -> dict:
    """Exerce la vraie conversion avec des sentinelles purement temporaires."""
    from scripts import build_language as driver

    number = lot_id.removeprefix('ES-')
    routes = json.loads((root / f'docs/analysis/es/{number}_ROUTES.json').read_text())['routes']
    chosen = [route for route in routes if not route['in_same_lot']]
    with tempfile.TemporaryDirectory(prefix=f'es{number}-route-') as temporary:
        tmp = Path(temporary)
        combined = tmp / 'combined.txt'
        # Une ancienne table ne constitue pas un lecteur moteur : le contrat
        # final refuse explicitement son import, au lieu d'un faux succès 7/7.
        from src.core.text_aliases import TextAliases
        aliases = TextAliases.load(root / 'languages/es-maint/text_aliases.json', driver.ENGLISH_ROM.read_bytes())
        blocked = [route for route in chosen if int(route['contract_offset'], 16) in aliases.excluded]
        active = [route for route in chosen if route not in blocked]
        texts = {}
        for route in active:
            raw = bytes.fromhex(route['snapshot']['raw_hex'])
            texts[route['contract_offset']] = '<0xD4>' + ''.join(f'<0x{b:02X}>' for b in raw[1:-1])
        if '0x00781278' in texts:
            texts['0x00781278'] = 'TEST<0xFE>TEST<0xFE>TEST'
        combined.write_text(''.join(key + ': ' + text + '\n' for key, text in texts.items()))
        config = driver.load_registry().get('es-maint')
        config = replace(config, combined=str(combined), output_rom=str(tmp / 'probe.gba'),
                         text_aliases=str(root / config.text_aliases),
                         item_descriptions=str(root / config.item_descriptions),
                         system_texts=str(root / config.system_texts))
        previous = driver.REPO_ROOT, driver.TRANSLATION_DIR
        try:
            driver.REPO_ROOT, driver.TRANSLATION_DIR = tmp, tmp / 'output/translation'
            result = driver.generate_translation_json(config)
        finally:
            driver.REPO_ROOT, driver.TRANSLATION_DIR = previous
        rows = json.loads(result.read_text())['translations']
        entries = []
        for route in chosen:
            key, live = int(route['contract_offset'], 16), int(route['offset'], 16)
            actual = [row for row in rows if row.get('contract_offset', row['offset']) == key]
            entries.append({'contract_offset': route['contract_offset'],
                            'expected_live': route['offset'], 'json_entries': actual,
                            'resolved_live': any(row['offset'] == live for row in actual),
                            'explicitly_blocked': route in blocked})
    return {'status': 'sonde temporaire ; aucune traduction de production', 'entries': entries}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lot', default='ES-016', help='Lot exact de lots.json')
    parser.add_argument('--probe-routing', action='store_true')
    parser.add_argument('--output', type=Path, help='Destination alternative du relevé ou de la sonde')
    args = parser.parse_args()
    number = args.lot.removeprefix('ES-')
    if args.probe_routing:
        report = probe_routing(lot_id=args.lot)
        destination = ROOT / f'docs/analysis/es/{number}_ACHEMINEMENT_REPRO.json'
    else:
        report = prepare(lot_id=args.lot)
        destination = ROOT / f'docs/analysis/es/{number}_PREPARATION.json'
        routes = [{'contract_offset': row['offset'], **candidate}
                  for row in report['entries'] for candidate in row['nearby_candidates']
                  if candidate['prefix_hex'] == 'aa']
        (ROOT / f'docs/analysis/es/{number}_ROUTES.json').write_text(json.dumps({
            'lot': args.lot,
            'status': 'candidats à certifier, aucune route autorisée par ce relevé',
            'routes': routes}, ensure_ascii=False, indent=2) + '\n')
    destination = args.output or destination
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(destination)
