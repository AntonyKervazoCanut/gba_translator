"""Préimages, commandes et budgets du lot contractuel ES-001."""
import json
import re
from pathlib import Path

from scripts.apply_combined_fr import _load_combined
from src.core.dialogue_linewrap import line_width
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]


def test_every_contract_key_has_one_evidenced_disposition():
    report = json.loads((ROOT / 'docs/analysis/es/0851_ES001_TRAITEMENT.json').read_text())
    contract = json.loads((ROOT / 'docs/analysis/es/lots.json').read_text())[0]
    rows = report['entries']
    assert len(rows) == len({e['offset'] for e in rows}) == 373
    assert {e['offset'] for e in rows} == set(contract['offsets'])
    assert sum(report['counts'].values()) == 373
    assert report['counts']['traduit_depuis_en'] == 350
    assert all(e['justification'] for e in rows)
    combined, _ = _load_combined(ROOT / 'languages/es-maint/combined_es-maint.txt')
    for entry in rows:
        key = int(entry['offset'], 16)
        if entry['decision'] == 'traduit_depuis_en':
            assert combined[key] == entry['translation']
        else:
            assert key not in combined


def test_all_translations_keep_commands_arguments_and_two_line_windows():
    rows = json.loads((ROOT / 'docs/analysis/es/0851_ES001_TRAITEMENT.json').read_text())['entries']
    for entry in rows:
        if entry['decision'] != 'traduit_depuis_en':
            continue
        value = entry['translation'].replace(r'\n', '\n')
        item = {'offset': int(entry['live_offset'], 16), 'translation': value,
                'encoding': 'pokemon', 'english_raw_bytes': entry['raw_hex'],
                'preserve_control_flow': True}
        normalized = SystemTextRoutes.normalize(item)
        raw = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        assert raw.hex() == entry['encoded_hex']
        assert len(raw) <= 512
        if entry['offset'] in {'0x0017D866', '0x00180300', '0x00185606',
                               '0x00188119', '0x00188555', '0x00196D87'}:
            # Une croissance pourrait déplacer une ressemblance de pointeur
            # dans des données : ces textes doivent tenir dans la préimage.
            assert len(raw) <= len(bytes.fromhex(entry['raw_hex']))
        for page in value.split('<0xFB>'):
            segments = page.split('<0xFA>')
            assert len(segments[0].split('\n')) <= 2
            assert all('\n' not in segment for segment in segments[1:])
        if entry['offset'] == '0x0017CC56':
            # Numeric min/seconds buffers, bounded to three digits each;
            # the general name-buffer estimate (54 px each) is inapplicable.
            value = re.sub(r'<0xFD><0x0[234]>', '999', value)
        assert all(line_width(line) <= 192 for line in re.split(r'\n|<0xF[AB]>', value)), entry['offset']


def test_named_buffers_fit_ten_wide_glyphs_and_numbers_fit_uint32():
    rows = json.loads((ROOT / 'docs/analysis/es/0851_ES001_TRAITEMENT.json').read_text())['entries']
    numeric = {'0x0019E9E5': ('02',), '0x0019EAE4': ('04',),
               '0x0019F31B': ('03',), '0x0019F3CB': ('03',),
               '0x0019F40A': ('03', '04'), '0x0019F4CF': ('04',)}
    for entry in rows:
        if entry['decision'] != 'traduit_depuis_en':
            continue
        value = entry['translation'].replace(r'\n', '\n')
        if entry['offset'] == '0x0017CC56':
            value = re.sub(r'<0xFD><0x0[234]>', '99999', value)
        for code in numeric.get(entry['offset'], ()):
            value = value.replace(f'<0xFD><0x{code}>', '4294967295')
        value = re.sub(r'<0xFD><0x[0-9A-F]{2}>', 'W' * 10, value)
        assert all(line_width(line) <= 192 for line in re.split(r'\n|<0xF[AB]>', value)), entry['offset']
