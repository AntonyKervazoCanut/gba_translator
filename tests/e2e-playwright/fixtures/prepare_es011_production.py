"""Prépare les vues de production F-861 pour les sondes natives existantes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def prepare() -> None:
    """Sépare les textes sans commandes et les quinze alias, sans modifier la ROM."""
    records = json.loads((ROOT / 'docs/analysis/es/011_TRAITEMENT.json').read_text())['entries']
    # La mire charge un pointeur de table par LDR ; les opérandes de script
    # non alignés restent tous contrôlés octet par octet par le test Playwright.
    plain = [dict(row, references=sorted(row['references'], key=lambda ref: int(ref, 16) % 4 != 0))
             for row in records if 'texte' in row and not row['commandes_source']]
    assert all(int(row['references'][0], 16) % 4 == 0 for row in plain)
    aliases = [
        {'key': int(row['offset'], 16), 'live': int(row['live_offset'], 16),
         'pointers': [int(ref, 16) for ref in row['references']],
         'expected_hex': row['encoded_hex'], 'layout': row['layout']}
        for row in records if row.get('layout')
    ]
    assert len(plain) == 244
    assert len(aliases) == 15
    destination = ROOT / 'output/reports'
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'es011-native.json').write_text(json.dumps({'entries': plain}, ensure_ascii=False, indent=2) + '\n')
    (destination / 'es011-production-aliases.json').write_text(json.dumps({
        'rom': 'output/roms/GenedRom-es-maint.gba', 'records': aliases,
    }, indent=2) + '\n')


if __name__ == '__main__':
    prepare()
