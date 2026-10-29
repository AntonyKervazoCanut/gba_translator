"""Garde le contrat terminologique consommé par F-850 et les lots ES."""

from pathlib import Path

GLOSSARY = Path(__file__).resolve().parents[2] / 'languages/es-maint/glossary.md'


def _table_rows(section: str) -> list:
    return [
        [cell.strip().replace('**', '') for cell in line.split('|')[1:-1]]
        for line in section.splitlines()
        if line.startswith('|') and not line.startswith('|---')
    ][1:]


def test_status_contract_preserves_the_six_spanish_video_game_badges():
    # Arrange: badges read from the Rubí/Zafiro sprites cited in the glossary.
    text = GLOSSARY.read_text(encoding='utf-8')
    section = text.split('## Statuts :', 1)[1].split('DEB est donc retenu', 1)[0]

    # Act: extract the exact descriptor key -> badge contract for infrastructure.
    rows = _table_rows(section)
    badges = {row[0]: row[3] for row in rows}

    # Assert: faint is DEB; CON cannot accidentally become the confusion label.
    assert len(rows) == 6
    assert badges == {
        'poison': 'ENV', 'burn': 'QUE', 'freeze': 'CON',
        'paralysis': 'PAR', 'sleep': 'DOR', 'faint': 'DEB',
    }
    assert all('S4' in row[4] and 'Rubí/Zafiro' in row[4] for row in rows)


def test_nature_contract_is_bijective_and_preserves_spanish_false_friends():
    # Arrange: nature identifiers must remain distinct across all 63 batches.
    text = GLOSSARY.read_text(encoding='utf-8')
    section = text.split('## Natures', 1)[1].split('## Statistiques', 1)[0]

    # Act: flatten the two English/Spanish pairs per row.
    pairs = [
        (row[i], row[i + 1])
        for row in _table_rows(section)
        for i in (0, 2)
        if row[i] != '—'
    ]
    names = dict(pairs)

    # Assert: never collapse Timid into Bashful, or translate Quiet literally.
    assert len(pairs) == len(names) == len(set(names.values())) == 25
    assert names['Timid'] == 'Miedosa'
    assert names['Bashful'] == 'Tímida'
    assert names['Quiet'] == 'Mansa'
    assert names['Adamant'] == 'Firme'
