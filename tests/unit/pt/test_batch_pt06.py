"""PT-06 : périmètre fermé, vocabulaire des phrases faciles et descriptions."""
import json
import re
from pathlib import Path

import yaml

from src.core.dialogue_linewrap import line_width
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[3]
LEGACY_ITEMS = {
    0x3DA81A, 0x3DAA0A, 0x3DAB13, 0x3DAB59, 0x3DAC51, 0x3DAD5C,
    0x3DADAE, 0x3DAE08, 0x3DAE68, 0x3DAEB6, 0x3DAF07, 0x3DAF8D, 0x3DAFD6,
}
FRAGMENTS = {0x3DDD0B, 0x3DEC2D, 0x3E1448, 0x3E144E}


def batch_offsets():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    return {int(x, 16) for b in batches if b['id'] == 'PT-06' for x in b['offsets']}


def translations():
    return {int(m[1], 16): m[2]
            for line in (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
            if (m := re.match(r'0x([0-9a-f]+): (.*)', line))
            and int(m[1], 16) in batch_offsets()}


def exceptions():
    return {o for o in batch_offsets() if o < 0x3DA7D1} | LEGACY_ITEMS | FRAGMENTS


def test_exact_coverage_and_protections():
    actual = translations()
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    expected = {int(e['offset'], 16): e['expected'] for e in protected['entries']}
    assert len(batch_offsets()) == 282
    assert len(exceptions()) == 60
    assert set(actual) == batch_offsets() - exceptions()
    assert all(expected[o] == text for o, text in actual.items())
    assert not any(in_fixed_table(offset) for offset in actual)


def test_encoding_and_display_budgets():
    for offset, text in translations().items():
        raw = TextEncoder.encode_pokemon(text.replace(r'\n', '\n'), strict=True)
        assert raw[-1] == 0xFF
        assert not re.search(r'<0x|[{}]', text), hex(offset)
        lines = text.split(r'\n')
        assert len(lines) <= 3
        budget = 186 if offset < 0x3E7F35 else 102
        assert all(line_width(line) <= budget for line in lines), (hex(offset), lines)


def test_glossary_and_domain_meaning():
    actual = translations()
    assert actual[0x3E8295] == 'SUPERCRESCIMENTO'
    assert actual[0x3E84B2] == 'INCÊNDIO'
    assert actual[0x3E8223] == 'DILÚVIO'
    assert actual[0x3E814B] == 'INTIMIDATE'
    assert actual[0x3E8414] == 'PLUS'
    assert actual[0x3DF7E8] == 'CHERI'
    assert actual[0x3E8BED] == 'movimento'
    assert actual[0x3E8AAC] == 'Ataque'
    assert 'Bellin Town' in actual[0x3DA7D1]
    assert 'The Shadow' in actual[0x3DA9BB]
    assert 'TM' in actual[0x3DACA5] and 'HM' in actual[0x3DACA5]
    assert 'Mega Stone' in actual[0x3DA907]


def test_audit_report_covers_all_offsets_and_justifies_exceptions():
    audit = json.loads((ROOT / 'docs/analysis/24_PT_BR_PT06.json').read_text())
    rows = {int(row['offset'], 16): row for row in audit['entries']}
    assert len(audit['entries']) == len(rows) == 282
    assert set(rows) == batch_offsets()
    assert {o for o, row in rows.items() if row['status'] == 'exception'} == exceptions()
    assert len(audit['source_sha256']) == 64
    for offset, text in translations().items():
        assert rows[offset]['portuguese'] == text
        assert rows[offset]['source_sites'] and rows[offset]['targets']
        assert rows[offset]['french_reference']
    assert all(row['reason'] and row['english'] for row in rows.values())
    report = (ROOT / 'docs/analysis/24_PT_BR_PT06.md').read_text()
    documented = re.findall(r'^\| `(0x[0-9a-f]+)` \|', report, re.MULTILINE)
    assert len(documented) == 282
    assert {int(offset, 16) for offset in documented} == batch_offsets()
