"""B-667 : qualification fermée et conservation des commandes de combat_ui-01."""
from __future__ import annotations

import hashlib
import importlib
import json
import re
import struct
from functools import lru_cache
from pathlib import Path

import pytest

from src.core.dialogue_linewrap import line_width, line_widths
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[2]
ROWS = json.loads((ROOT / 'tests/unit/fixtures/combat_ui_01.json').read_text())
CORRECTED = [r for r in ROWS if r['decision'] == 'corrigé']
BUILDER = importlib.import_module('src.translators.19_build_translated_rom_generic').TranslatedROMBuilder


@lru_cache(maxsize=1)
def combined() -> dict[int, str]:
    """Lit les dernières valeurs sans modifier le corpus cumulatif."""
    result = {}
    for line in (ROOT / 'languages/de/combined_de.txt').read_text().splitlines():
        match = re.match(r'^(0x[0-9a-fA-F]+): ?(.*)$', line)
        if match:
            result[int(match[1], 16)] = match[2]
    return result


def encoded(text: str) -> bytes:
    """Encode les commandes brutes, les ruptures et les umlauts allemands."""
    for escaped, raw in [(r'\n', '\n'), (r'\l', '<0xFA>'), (r'\p', '<0xFB>')]:
        text = text.replace(escaped, raw)
    return TextEncoder.encode_pokemon(text, skip_aliases=GERMAN_UMLAUT_CHARS)


def test_scope_and_decisions() -> None:
    """Aucun oubli ou offset d'un lot voisin dans les 300 décisions."""
    offsets = [int(row['offset'], 16) for row in ROWS]
    digest = hashlib.sha256(b''.join(o.to_bytes(4, 'little') for o in offsets)).hexdigest()
    assert len(offsets) == len(set(offsets)) == 300
    assert digest == 'ca179097b066fa5b076900b0cde041a945ae64e5928edf533c2fa111633f72dc'
    report = (ROOT / 'docs/analysis/667_COMBAT_UI_01_DE.md').read_text()
    assert re.findall(r'^\| (0x[0-9A-F]+) \|', report, re.MULTILINE) == [
        row['offset'] for row in ROWS
    ]
    for row in ROWS:
        assert row['reason'] and row['zone'] and row['canonical']
        assert row['decision'] in {
            'corrigé', 'déjà correct', 'déjà correct/patché',
            'nom propre légitime', 'fragment non vivant', 'besoin de patch séparé',
        }


@pytest.mark.parametrize('row', CORRECTED, ids=lambda row: row['offset'])
def test_source_controls_and_budget(row: dict) -> None:
    """Garde chaque commande EN, arguments et ruptures compris, dans l'ordre."""
    actual = combined()[int(row['offset'], 16)]
    assert actual == row['after']
    expected = bytes.fromhex(row['expected_hex'])
    assert encoded(actual) == expected
    controls = BUILDER._extract_control_sequences_from_raw
    assert controls(expected, include_breaks=True) == controls(
        bytes.fromhex(row['hex']), include_breaks=True,
    )
    visible = re.sub(r'<0xFC>(?:<0x[0-9A-F]{2}>){2}', '', actual)
    visible = re.sub(r'<0xFD><0x[0-9A-F]{2}>', 'MMMMMMMMMM', visible)
    assert max(line_width(line) for line in re.split(r'\\[nlp]', visible)) <= 192
    assert row['sites']  # Aucun nouveau texte sur un suffixe sans référence.


@pytest.fixture(scope='module')
def roms() -> tuple[bytes, bytes]:
    """Charge une seule fois les deux ROM privées pour les contrôles de pointeurs."""
    return ((ROOT / 'input/roms/englishrom.gba').read_bytes(),
            (ROOT / 'output/roms/GenedRom-de.gba').read_bytes())


@pytest.mark.rom
@pytest.mark.private_build
@pytest.mark.parametrize('row', CORRECTED, ids=lambda row: row['offset'])
def test_every_live_pointer(row: dict, roms: tuple[bytes, bytes]) -> None:
    """Les sites EN doivent viser la traduction exacte après reconstruction DE."""
    source, built = roms
    offset = int(row['offset'], 16)
    original = bytes.fromhex(row['hex'])
    expected = bytes.fromhex(row['expected_hex'])
    assert source[offset:offset + len(original)] == original
    pointer = struct.pack('<I', offset + 0x08000000)
    sites = []
    pos = source.find(pointer)
    while pos >= 0:
        sites.append(pos)
        pos = source.find(pointer, pos + 1)
    assert sites == [int(site, 16) for site in row['sites']]
    for site in sites:
        target = struct.unpack_from('<I', built, site)[0] - 0x08000000
        assert 0 <= target <= len(built) - len(expected)
        end = built.index(b'\xff', target)
        actual = built[target:end + 1]
        assert meaningful_tokens(actual) == meaningful_tokens(expected), (
            row['offset'], hex(site), hex(target), actual.hex(),
        )
        controls = BUILDER._extract_control_sequences_from_raw
        # Le moteur ré-enveloppe les mots. Les commandes, leurs arguments,
        # l'ordre des pages et la forme FE/FA/FB doivent tous rester identiques.
        src_controls = controls(expected, include_breaks=True)
        dst_controls = controls(actual, include_breaks=True)
        for breaks in (False, True):
            src = [c for c in src_controls if (c[0] in (0xFA, 0xFB, 0xFE)) == breaks]
            dst = [c for c in dst_controls if (c[0] in (0xFA, 0xFB, 0xFE)) == breaks]
            assert src == dst, row['offset']
        assert max(line_widths(visible_rom_text(actual))) <= 192, row['offset']
        if target == offset:
            # Une chaîne peut grandir en place dans son padding FF prouvé.
            extra_start = offset + len(original)
            extra_end = offset + len(actual)
            assert all(byte == 0xFF for byte in source[extra_start:extra_end])
            for address in range(extra_start, extra_end):
                assert struct.pack('<I', address + 0x08000000) not in source


def meaningful_tokens(raw: bytes) -> list[bytes]:
    """Compare le texte et les pages sans confondre les arguments avec les espaces."""
    result = []
    index = 0
    while index < len(raw):
        code = raw[index]
        size = (2 + BUILDER.FC_ARG_COUNTS.get(raw[index + 1], 0)
                if code == 0xFC else 1 + BUILDER.RAW_ARG_PREFIXES.get(code, 0))
        if size > 1 or code not in (0, 0xFE, 0xFA):
            result.append(raw[index:index + size])
        index += size
    return result


def visible_rom_text(raw: bytes) -> str:
    """Mesure les lignes affichées en réservant dix glyphes par buffer."""
    from src.core.text_codec import TextDecoder
    result = []
    index = 0
    while index < len(raw):
        code = raw[index]
        if code == 0xFF:
            break
        size = (2 + BUILDER.FC_ARG_COUNTS.get(raw[index + 1], 0)
                if code == 0xFC else 1 + BUILDER.RAW_ARG_PREFIXES.get(code, 0))
        if code == 0xFD:
            result.append('MMMMMMMMMM')
        elif code in (0xFA, 0xFB, 0xFE):
            result.append('\n')
        elif size == 1:
            result.append(TextDecoder.decode_pokemon(bytes([code])))
        index += size
    return ''.join(result)


@pytest.mark.rom
@pytest.mark.private_build
def test_relocations_and_non_overlap(roms: tuple[bytes, bytes]) -> None:
    """Toute relocalisation occupe du FF ; les corrections restent disjointes."""
    source, built = roms
    spans = set()
    for row in CORRECTED:
        original = int(row['offset'], 16)
        for site in row['sites']:
            target = struct.unpack_from('<I', built, int(site, 16))[0] - 0x08000000
            end = built.index(b'\xff', target) + 1
            if target != original:
                assert source[target:end] == b'\xff' * (end - target), row['offset']
            spans.add((target, end, original))
    ordered = sorted(spans)
    for index in range(1, len(ordered)):
        left, right = ordered[index - 1], ordered[index]
        assert left[1] <= right[0], (left, right)


@pytest.mark.rom
@pytest.mark.private_build
def test_structured_prefix_is_already_translated(roms: tuple[bytes, bytes]) -> None:
    """Le suffixe traduit voisin rend 0x26D4DF correct sans écriture chevauchante."""
    _, built = roms
    expected = encoded(' <0xFC><0x03><0x00>  Fangen wir an!')
    for site in (0x26D3C6, 0x26D3E4):
        target = struct.unpack_from('<I', built, site)[0] - 0x08000000
        assert built[target:target + len(expected)] == expected
