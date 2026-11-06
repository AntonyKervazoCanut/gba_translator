"""Prépare les preuves ES-013 sans toucher aux sources de traduction."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import sys
import tempfile
from collections import Counter
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.text_codec import TextDecoder


def pointer_sites(source: bytes, offset: int) -> list[str]:
    """Retourne toutes les occurrences LE32, sans supposer leur alignement."""
    needle = (offset + 0x08000000).to_bytes(4, 'little')
    sites = []
    site = source.find(needle)
    while site >= 0:
        sites.append(f'0x{site:08X}')
        site = source.find(needle, site + 1)
    return sites


def preimage(source: bytes, offset: int) -> bytes:
    """Lit jusqu'au FF réel, sans plafond arbitraire de 512 octets."""
    return source[offset:source.index(255, offset) + 1]


def command_aware_text(raw: bytes, builder: type) -> str:
    """Sépare les glyphes des commandes complètes, sans lettres d'argument."""
    parts = []
    index = 0
    while index < len(raw):
        value = raw[index]
        if value == 255:
            break
        if value == 254:
            parts.append(r'\n')
            index += 1
            continue
        if value == 0xFC:
            size = 2 + builder.FC_ARG_COUNTS.get(raw[index+1], 0)
        elif value in builder.CONTROL_PREFIXES:
            size = 1 + builder.RAW_ARG_PREFIXES.get(value, 0)
        elif value == 0xB0:
            size = 1  # Ponctuation moteur, jamais la quote du décodeur ancien.
        else:
            parts.append(TextDecoder.decode_pokemon(bytes([value]), preserve_unknown=True))
            index += 1
            continue
        parts.extend(f'<0x{byte:02X}>' for byte in raw[index:index+size])
        index += size
    return ''.join(parts)


def prepare(root: Path = ROOT) -> dict:
    """Reconstruit le dossier technique du lot exact depuis les ROMs locales."""
    source = (root / 'input/roms/englishrom.gba').read_bytes()
    spanish = (root / 'input/roms/spanishrom.gba').read_bytes()
    lots = json.loads((root / 'docs/analysis/es/lots.json').read_text())
    contract = next(lot['offsets'] for lot in lots if lot['id'] == 'ES-013')
    with (root / 'docs/analysis/es/inventaire.csv').open(newline='') as stream:
        inventory = {row['offset']: row for row in csv.DictReader(stream)
                     if row['lot'] == 'ES-013'}
    mappings = json.loads((root / 'output/differences/pointer_offset_map.json').read_text())['offset_map']
    by_en = {}
    for mapping in mappings:
        by_en.setdefault(mapping['english_offset'], []).append(mapping)
    builder = importlib.import_module(
        'src.translators.19_build_translated_rom_generic').TranslatedROMBuilder
    # Ces audits voisins apportent des hypothèses de consommateurs, jamais une
    # traduction ES. Chaque préimage et pointeur retenu est relu dans notre ROM.
    prior = {}
    for number in (17, 18):
        path = root / f'languages/pt/data/pt{number}_audit.json'
        for item in json.loads(path.read_text())['entries']:
            prior[int(item['offset'], 16)] = item
    natures = ['Fuerte', 'Huraña', 'Audaz', 'Firme', 'Pícara', 'Osada',
               'Dócil', 'Plácida', 'Agitada', 'Floja', 'Miedosa', 'Activa',
               'Seria', 'Alegre', 'Ingenua', 'Modesta', 'Afable', 'Mansa',
               'Tímida', 'Alocada', 'Serena', 'Amable', 'Grosera', 'Cauta', 'Rara']
    nature_keys = [int.from_bytes(source[0x463E60 + 4*i:0x463E64 + 4*i], 'little')
                   - 0x08000000 for i in range(25)]
    records = []
    for key in contract:
        offset = int(key, 16)
        raw = preimage(source, offset)
        sites = pointer_sites(source, offset)
        hint = prior.get(offset, {})
        replacement = hint.get('replacement', {})
        live = int(replacement.get('target', key), 16)
        if live == offset and not sites:
            # Noms/menus extraits avec un à trois octets de remplissage.
            for delta in range(1, 4):
                if raw[:delta] == bytes(delta) and pointer_sites(source, offset + delta):
                    live = offset + delta
                    break
        live_raw = preimage(source, live)
        live_sites = pointer_sites(source, live)
        if 'source_hex' in hint:
            assert bytes.fromhex(hint['source_hex']) == raw, key
        for site in hint.get('references', []):
            assert int.from_bytes(source[site:site+4], 'little') == live + 0x08000000, key
        sibling = f'0x{live:08X}' if live != offset and f'0x{live:08X}' in contract else None
        candidate = None
        if offset in nature_keys:
            qualification = 'nature'
            surface = 'Noms de natures / deux tables indexées par ID'
            reason = 'D-849 : nom officiel par ID ; vérifier les deux consommateurs après relocation.'
            candidate = natures[nature_keys.index(offset)]
        elif 0x454DA8 <= offset <= 0x4556CB:
            qualification = 'description de décoration'
            surface = 'Décorations / champ description de structure à stride 32'
            reason = 'Pointeur descriptif distinct des noms, prix et graphismes ; fenêtre à qualifier pour ES.'
        elif offset == 0x4556F6:
            qualification = 'fragment de structure'
            surface = 'Décorations / nom SMALL DESK dans une structure'
            reason = 'La clé précède le nom de trois octets ; aucun pointeur direct. Ne pas écrire une phrase dans la structure.'
        elif 0x4566C8 <= offset <= 0x4568DC or offset == 0x4716B4:
            qualification = 'données binaires'
            surface = 'Données non linguistiques / aucune référence texte directe'
            reason = 'Motifs binaires répétitifs, non une phrase ; aucune injection proposée.'
        elif offset == 0x458314:
            qualification = 'table de pointeurs'
            surface = 'Communication sans fil / choix de deux messages'
            reason = '11AE90 charge une table : 458314→458260, 458318→4582C0. Ne pas traduire les huit octets en préfixe.'
        elif offset == 0x45817E:
            qualification = 'coïncidence binaire'
            surface = 'Données graphiques / occurrence non alignée 1DCCF22'
            reason = 'Le référent graphique signalé dans PT-17 ne prouve pas un lecteur texte ; qualification moteur requise.'
        elif offset == 0x475638 or 0x47AAC1 <= offset <= 0x47AB15:
            qualification = 'alphabet conservé'
            surface = 'Saisie / groupes de lettres'
            reason = 'Lettres de saisie, pas un mot anglais à traduire ; conserver ordre et casse.'
        elif offset >= 0x482874:
            qualification = 'description de mouvement'
            surface = 'Résumé et tables historiques de descriptions de mouvements'
            reason = 'Préimage EN ROM prioritaire sur export EN francisé/vide ; trois références directes à qualifier.'
        elif offset >= 0x47B7AB:
            binary = offset in {0x47B7AB, 0x47B85B, 0x47E277, 0x47EDEB, 0x47EE9B, 0x4814AB}
            qualification = 'métadonnées Pokémon' if binary else 'nom propre conservé'
            surface = 'Trainer Tower / données de Pokémon' if binary else 'Trainer Tower / noms de Dresseurs'
            reason = ('Extraction démarrant dans les métadonnées avant un nom d’espèce ; ne pas injecter.' if binary
                      else 'D-849 : nom propre EN conservé dans sa cellule, espaces inclus ; accès par structure, pas pointeur vers chaque nom.')
        elif sibling:
            qualification = 'doublon de remplissage'
            surface = 'Communication sans fil / préfixe du message voisin'
            reason = f'Préfixe 00, sans lecteur propre ; seul le début vivant contractuel {sibling} doit recevoir la traduction.'
        elif live != offset:
            qualification = 'alias hors clé contractuelle'
            surface = 'Communication sans fil / menu ou message à début décalé'
            reason = f'Début candidat 0x{live:08X} référencé, clé contractuelle sans lecteur direct ; contrat d’alias nécessaire sans ajout hors lot.'
        else:
            qualification = 'texte système à router'
            surface = 'Communication sans fil / messages et tables de choix'
            reason = 'Contrôler consommateurs, commandes complètes, buffers et fenêtre avant import ; aucun fallback certifié.'
        es_matches = by_en.get(live, [])
        es = []
        for match in es_matches:
            target = match.get('spanish_offset')
            es.append({'mapping': match, 'preimage_hex': preimage(spanish, target).hex()
                       if target is not None else None,
                       'pointer_sites': pointer_sites(spanish, target) if target is not None else []})
        controls = [bytes(sequence).hex() for sequence in
                    builder._extract_control_sequences_from_raw(live_raw, include_breaks=True)]
        records.append({
            'offset': key, 'inventaire': inventory[key], 'qualification': qualification,
            'surface_provisoire': surface, 'justification': reason,
            'preimage_en_hex': raw.hex(), 'octets_avec_ff': len(raw),
            'en_rom_debug_non_normatif': TextDecoder.decode_pokemon(raw, preserve_unknown=True),
            'en_vivant_commandes_brutes': command_aware_text(live_raw, builder)
            if qualification not in {'données binaires', 'table de pointeurs',
                                     'métadonnées Pokémon', 'fragment de structure'} else None,
            'pointer_sites': sites, 'debut_candidat': f'0x{live:08X}',
            'autre_cle_vivante_du_lot': sibling,
            'preimage_vivante_hex': live_raw.hex(), 'pointeurs_debut_candidat': live_sites,
            'commandes_parseur_hex': controls, 'correspondances_es': es,
            'traduction_candidate_d849': candidate, 'traduction_finale': None,
            'injection_certifiee': False,
        })
    files = ['languages/en/combined_en.txt', 'languages/es/combined_es.txt',
             'languages/fr/combined_fr.txt', 'languages/es-maint/combined_es-maint.txt',
             'languages/es-maint/protected_entries.yaml', 'languages/es-maint/glossary.md']
    return {
        'lot': 'ES-013', 'phase': 'préparation technique, non livré',
        'source_sha256': hashlib.sha256(source).hexdigest(),
        'es_sha256': hashlib.sha256(spanish).hexdigest(),
        'offset_map_sha256': hashlib.sha256((root / 'output/differences/pointer_offset_map.json').read_bytes()).hexdigest(),
        'fichiers_preserves_sha256': {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files},
        'counts': dict(Counter(item['qualification'] for item in records)),
        'preuves_tables': [{'offset': f'0x{offset:08X}', 'hex': source[offset:offset+size].hex(),
                           'pointer_sites': pointer_sites(source, offset)}
                          for offset, size in [(0x45570C, 32), (0x458314, 8),
                                               (0x463E60, 100), (0x1FE65F4, 100),
                                               (0x4827B4, 32), (0x99F190, 28)]],
        'entries': records,
    }


def probe_routing(report: dict) -> dict:
    """Exerce la vraie conversion avec vingt sentinelles, dans un dossier temporaire."""
    from scripts import build_language as driver

    entries = [entry for entry in report['entries']
               if entry['qualification'] == 'alias hors clé contractuelle']
    with tempfile.TemporaryDirectory(prefix='es013-route-') as temporary:
        tmp = Path(temporary)
        combined = tmp / 'combined.txt'
        combined.write_text(''.join(entry['offset'] + ': Z' + entry['en_vivant_commandes_brutes']
                                    + '\n' for entry in entries))
        config = driver.load_registry().get('es-maint')
        config = replace(config, combined=str(combined), output_rom=str(tmp/'probe.gba'),
                         text_aliases=str(ROOT/config.text_aliases),
                         item_descriptions=str(ROOT/config.item_descriptions),
                         system_texts=str(ROOT/config.system_texts))
        previous = driver.REPO_ROOT, driver.TRANSLATION_DIR
        try:
            driver.REPO_ROOT = tmp
            driver.TRANSLATION_DIR = tmp / 'output/translation'
            ready = driver.generate_translation_json(config)
        finally:
            driver.REPO_ROOT, driver.TRANSLATION_DIR = previous
        actual = json.loads(ready.read_text())['translations']
        rows = {item.get('contract_offset', item['offset']): item for item in actual}
        probe = []
        for entry in entries:
            item = rows.get(int(entry['offset'], 16))
            probe.append({'offset': entry['offset'], 'live': entry['debut_candidat'],
                          'expected_pointer_sites': entry['pointeurs_debut_candidat'],
                          'json_entry': item, 'live_offset_resolved': bool(
                              item and item['offset'] == int(entry['debut_candidat'], 16))})
        return {'phase': 'sonde temporaire de conversion, sans traduction de production',
                'entries': probe}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe-routing', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'docs/analysis/es/013_PREPARATION.json'
    if args.probe_routing:
        report = probe_routing(json.loads(target.read_text()))
        target = ROOT / 'docs/analysis/es/013_ACHEMINEMENT_REPRO.json'
    else:
        report = prepare()
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(target)
