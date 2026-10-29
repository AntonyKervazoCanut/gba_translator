"""Contrat éditorial PT-02 : couverture fermée, protections et affichage."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
PREFIXES = {
    0x197873, 0x198BBA, 0x19A4F7, 0x19A5BD, 0x19A79F, 0x1A5AD5,
    0x1A5BC5, 0x1A6196, 0x1A6447, 0x1A6CA2, 0x1B1D7C, 0x1BC310,
}
FRAGMENTS = {0x1A2D75, 0x1A2E4E, 0x1BDF08}
EXCEPTIONS = PREFIXES | FRAGMENTS | {0x199BB3}


def batch_offsets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    return {int(x, 16) for b in batches if b['id'] == 'PT-02' for x in b['offsets']}


def translations():
    lines = (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
    return {int(m[1], 16): m[2] for line in lines
            if (m := re.match(r'0x([0-9a-f]+): (.*)', line))
            and int(m[1], 16) in batch_offsets()}


def normalized(text):
    return text.replace(r'\n', '\n').replace(r'\p', '<0xFB>').replace(r'\l', '<0xFA>')


def test_closed_batch_and_exact_protections():
    actual = translations()
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    expected = {int(e['offset'], 16): e['expected'] for e in protected['entries']}
    assert len(batch_offsets()) == 277
    assert len(actual) == 261
    assert set(actual) == batch_offsets() - EXCEPTIONS
    assert all(expected[x] == value for x, value in actual.items())
    assert not any(in_fixed_table(x) for x in actual)


def test_dialogue_width_encoding_and_page_structure():
    for offset, text in translations().items():
        assert TextEncoder.encode_pokemon(normalized(text), strict=True)[-1] == 0xFF
        for page in text.split(r'\p'):
            assert page.count(r'\n') <= 1, hex(offset)
        for line in re.split(r'\\[nlp]', text):
            assert line_width(line) <= 192, (hex(offset), line)


def test_domain_semantics_and_retained_names():
    actual = translations()
    assert 'Good Rod' in actual[0x19925E] and 'Super Rod' in actual[0x19F0B2]
    assert 'Galavan' in actual[0x197874] and 'Mel' in actual[0x19BDFE]
    assert 'Teala' in actual[0x1BD898]
    assert 'Bellin Town' in actual[0x1A6046]
    assert 'Centro Pokémon' in actual[0x1A5483]
    assert 'Batalha Individual' in actual[0x1BC6CA]
    assert 'Batalha Dupla' in actual[0x1BC409]
    assert 'polegadas' in actual[0x19F3CB]
    assert 'comunicação sem fio.' in actual[0x1BD966]
    assert 'comunicação sem fio.' in actual[0x1BDBF8]


def test_audit_report_covers_offsets_and_keeps_source_pointer_column():
    """Le bilan ne perd ni exception ni site source lors d'un changement de cible."""
    report = (ROOT / 'docs/analysis/23_PT_BR_PT02.md').read_text()
    rows = {}
    for line in report.splitlines():
        if re.match(r'^\| `0x[0-9a-f]+` \|', line):
            columns = [column.strip() for column in line.split('|')]
            assert len(columns) == 7
            offset = int(columns[1].strip('`'), 16)
            assert offset not in rows
            rows[offset] = columns
    assert set(rows) == batch_offsets()
    assert {offset for offset, columns in rows.items()
            if columns[2].startswith('exception')} == EXCEPTIONS
    assert rows[0x196DF8][4] == '`0x16c932`'
    assert rows[0x1A51F6][4] == '`0x1a674a`, `0x1a682f`, `0x9a48dd`'
    assert rows[0x1A5200][4] == '`0x1a6990`'
    for offset in set(rows) - EXCEPTIONS:
        assert re.fullmatch(r'`0x[0-9a-f]+`(?:, `0x[0-9a-f]+`)*', rows[offset][5])
