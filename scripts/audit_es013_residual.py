"""Reproduit les constats résiduels ES-013, sans qualifier un scan comme CFG."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_es013_preparation import pointer_sites

SYSTEM_KEYS = (0x457860, 0x45787C, 0x457B2C, 0x457B4C, 0x458F2C, 0x458F60)
DECORATION_SELECTION_SHA256 = 'f9d5ce61f4a68d9e1c6f62d855d1b67f28cdd3cbb5ba2995d3529f018af9890c'
TABLES = ((0x457898, 2), (0x457B80, 4), (0x458F94, 2))
# Tranches exactes : expanseur, hook, copie, lecteurs déjà qualifiés et slot script.
SLICES = ((0x8D84, 0x8DA4), (0x9118, 0x9120), (0x13CCC8, 0x13CD14),
          (0x8A9270, 0x8A92B8), (0x119944, 0x1199B0), (0x11A0F8, 0x11A148),
          (0xF6CD0, 0xF6D20), (0xF6E08, 0xF6E54),
          (0x15FBB8, 0x15FBBC), (0x1EC9D38, 0x1EC9DC0))


def literal_loads(rom: bytes, site: int) -> list[dict]:
    """Liste les candidats LDR Thumb PC-relatifs, sans preuve d'exécution."""
    if site % 4:
        return []
    result = []
    for pc in range(max(0, site - 1024), site, 2):
        op = int.from_bytes(rom[pc:pc + 2], 'little')
        if op & 0xF800 == 0x4800 and ((pc + 4) & ~3) + (op & 255) * 4 == site:
            result.append({'offset': f'0x{pc:08X}', 'register': (op >> 8) & 7})
    return result


def validate_sources(en: bytes, es: bytes, preparation: dict) -> None:
    """Refuse toute identité ROM différente des préimages du checkpoint."""
    for label, data, key in [('EN', en, 'source_sha256'), ('ES', es, 'es_sha256')]:
        if hashlib.sha256(data).hexdigest() != preparation[key]:
            raise ValueError(f'SHA-256 {label} différent du checkpoint ES-013')


def interior_references(rom: bytes, start: int, size: int, ram: bool = False) -> list[dict]:
    """Scanne tous alignements et toutes cellules intérieures, y compris +24."""
    base = start if ram else start + 0x08000000
    # Le périmètre de lecture n'est jamais une sélection de traductions.
    if base >> 16 != (base + size - 1) >> 16:
        raise ValueError('La région de scan doit rester dans une banque de 64 Kio')
    suffix = (base >> 16).to_bytes(2, 'little')
    result, cursor = [], 2
    while (cursor := rom.find(suffix, cursor)) >= 0:
        site = cursor - 2
        target = int.from_bytes(rom[site:site + 4], 'little')
        if base <= target < base + size:
            result.append({'site': f'0x{site:08X}', 'target': f'0x{target:08X}',
                           'delta': target - base, 'thumb_ldr_candidates': literal_loads(rom, site)})
        cursor += 1
    return result


def audit(en: bytes, es: bytes, docs: Path) -> tuple[dict, dict]:
    """Relit sélection, préimages EN/ES et correspondances avant les scans."""
    preparation = json.loads((docs / '013_PREPARATION.json').read_text())
    surfaces = json.loads((docs / '013_SURFACES.json').read_text())
    system = json.loads((docs / '013_SYSTEM.json').read_text())
    validate_sources(en, es, preparation)
    decorations = [e for e in surfaces['entries'] if e['qualification'] == 'description de décoration']
    selected_system = [e for e in system['entries'] if int(e['offset'], 16) in SYSTEM_KEYS]
    selection_hash = hashlib.sha256('\n'.join(e['offset'] for e in decorations).encode()).hexdigest()
    system_selection = tuple(int(e['offset'], 16) for e in selected_system)
    if selection_hash != DECORATION_SELECTION_SHA256 or system_selection != SYSTEM_KEYS:
        raise ValueError('Sélection exacte résiduelle incohérente')
    for entry in decorations:
        offset = int(entry['offset'], 16)
        sites = pointer_sites(en, offset)
        if sites != entry['pointer_offsets'] or len(sites) != 1:
            raise ValueError(f'Champ descriptif ambigu : {offset:08X}')
        site = int(sites[0], 16)
        if (site - 0x4556F8) % 32 != 24:
            raise ValueError(f'Champ hors description : {offset:08X}')
    for entry in decorations + selected_system:
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['source_hex'])
        if en[offset:offset + len(raw)] != raw:
            raise ValueError(f'Préimage EN différente : {offset:08X}')
        matches = entry.get('correspondances_es', entry.get('spanish_matches', []))
        matched = [m for m in matches if m['mapping'].get('spanish_offset') is not None]
        if len(matched) != 1:
            raise ValueError(f'Correspondance ES absente ou ambiguë : {offset:08X}')
        match = matched[0]
        es_offset = match['mapping']['spanish_offset']
        es_raw = bytes.fromhex(match['preimage_hex'])
        if es[es_offset:es_offset + len(es_raw)] != es_raw:
            raise ValueError(f'Préimage ES différente : {offset:08X}')
        if pointer_sites(es, es_offset) != match['pointer_sites']:
            raise ValueError(f'Références ES différentes : {offset:08X}')
    tables = []
    for start, count in TABLES:
        tables.append({'offset': f'0x{start:08X}', 'cells': count,
                       'hex': en[start:start + count * 4].hex(),
                       'base_references': pointer_sites(en, start),
                       'interior_references': interior_references(en, start, count * 4)})
    report = {
        'source_sha256': preparation['source_sha256'], 'es_sha256': preparation['es_sha256'],
        'method': 'LE32 tous alignements, ROM entière ; LDR Thumb candidats, PAS graphe de contrôle',
        'decorations': {
            'keys': [e['offset'] for e in decorations], 'table': '0x004556F8', 'stride': 32,
            'description_field': 24, 'base_references': pointer_sites(en, 0x4556F8),
            'interior_references': interior_references(en, 0x4556F8, 121 * 32),
            'window': None, 'font': None, 'pixel_budget': None,
            'external_header_consumer_proven': False,
            'decision': 'exclusion conservatoire ; ni dormant ni inaccessible certifié'},
        'unrooted_system': {'keys': [e['offset'] for e in selected_system], 'tables': tables,
                            'decision': 'héritage inutilisé FireRed identifié ; accessibilité Unbound inconnue'},
        'buffer': {
            'address': '0x02021D18', 'upstream_declared_capacity': 1000,
            'physical_capacity_proven': None, 'contract_limit_unchanged': 512,
            'interior_references': interior_references(en, 0x02021D18, 1000, ram=True),
            'next_symbol_getter': {'offset': '0x00009118', 'hex': en[0x9118:0x9120].hex()},
            'script_81_cell': '0x0015FBB8',
            'script_81_target': f'0x{struct.unpack_from("<I", en, 0x15FBB8)[0]:08X}',
            'allocation_status': 'déclaration FireRed corroborée, édition de liens Unbound non disponible',
            'expansion': ['0x0011995E -> 0x0011AF6C', '0x0013CCC8 -> 0x008A9270',
                          'F7 -> 0x0013CCE8 -> StringCopy 0x00008D84'],
            'reader': ['0x0011A0F8', '0x000F6E08', '0x000F6CD0'],
            'native_limit_check': False},
        'unknowns': ['allocation EWRAM canonique et éventuels alias CFRU',
                     'racines calculées ARM/Thumb, scripts et consommateurs externes',
                     'fenêtre/police naturelle des 54 décorations'],
    }
    fixture = {'source_sha256': preparation['source_sha256'], 'slices': [
        {'offset': a, 'hex': en[a:b].hex()} for a, b in SLICES]}
    return report, fixture


def main() -> None:
    """Produit un rapport déterministe et des tranches réelles en sortie choisie."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--en', type=Path, default=ROOT / 'input/roms/englishrom.gba')
    parser.add_argument('--es', type=Path, default=ROOT / 'input/roms/spanishrom.gba')
    parser.add_argument('--output', type=Path, default=ROOT / 'output/analysis/es013_residual.json')
    parser.add_argument('--fixture', type=Path, default=ROOT / 'output/analysis/es013_residual_rom.json')
    args = parser.parse_args()
    report, fixture = audit(args.en.read_bytes(), args.es.read_bytes(), ROOT / 'docs/analysis/es')
    for path, data in [(args.output, report), (args.fixture, fixture)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('54 décorations et 6 textes contrôlés ; aucune nouvelle autorisation d’injection')


if __name__ == '__main__':
    main()
