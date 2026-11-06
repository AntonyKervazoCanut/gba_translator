"""Contrat HI-01 : source ROM figée, contrôles, protection et cibles vivantes."""

from __future__ import annotations

import hashlib
import json
import os
import re
import struct
from functools import lru_cache
from pathlib import Path

import pytest

from scripts.check_translation_integrity import load_last_wins, load_manifest
from src.core.fixed_tables import in_fixed_table
from src.core.text_codec import TextEncoder

ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / 'languages/indie/data/hi01_inventory.json').read_text())
ENTRIES = DATA['entries']
SNAPSHOT_SHA256 = '65e93f43b9f92f19ba011fb4971aea6f44d9cd419363d7b51d9dbe094235af19'
SEEDS = {0x1773FD, 0x177489, 0x183509}
ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?'-():/\n")
HEX_TOKEN = re.compile(r'<0x([0-9A-F]{2})>')
FONT_WIDTHS = bytes.fromhex(DATA['font_width_table_hex'])


@lru_cache(maxsize=1)
def _live() -> dict[int, str]:
    return load_last_wins(ROOT / 'languages/indie/combined_indie.txt')[0]


@lru_cache(maxsize=1)
def _manifest() -> dict:
    return {e.offset: e for e in load_manifest(ROOT / 'languages/indie/protected_entries.yaml')}


def _encoded(text: str) -> bytes:
    normalized = text.replace('\\n', '\n')
    expected = bytearray()
    for part in re.split(r'(<0x[0-9A-F]{2}>)', normalized):
        token = HEX_TOKEN.fullmatch(part)
        if token:
            expected.append(int(token[1], 16))
        else:
            assert set(part) <= ALPHABET, repr(part)
            expected.extend(0xFE if c == '\n' else TextEncoder.POKEMON_TABLE[c] for c in part)
    expected.append(0xFF)
    result = TextEncoder.encode_pokemon(normalized, strict=True)
    assert result == bytes(expected), 'Alias ou fallback non autorisé'
    assert 0xFF not in result[:-1], 'Terminateur injecté dans le texte'
    return result


def _units(raw: bytes) -> list[bytes]:
    """Décompose le sous-ensemble de contrôles effectivement présent dans HI-01."""
    units = []
    index = 0
    while index < len(raw):
        byte = raw[index]
        size = 1
        if byte == 0xFD:
            size = 2
        elif byte == 0xFC:
            assert raw[index + 1] == 0x01, 'Nouvelle commande FC à examiner'
            size = 3
        else:
            assert byte not in (0xF7, 0xF8, 0xF9), 'Nouveau contrôle à examiner'
        unit = raw[index:index + size]
        assert len(unit) == size
        units.append(unit)
        index += size
    return units


def _controls(raw: bytes) -> list[bytes]:
    return [u for u in _units(raw) if u[0] in (0xFD, 0xFC, 0xFE, 0xFA, 0xFB, 0xB0)]


def _widths(raw: bytes, buffer_widths: dict[str, int]) -> list[int]:
    widths = [0]
    for unit in _units(raw):
        byte = unit[0]
        if byte in (0xFE, 0xFA, 0xFB):
            widths.append(0)
        elif byte == 0xFD:
            widths[-1] += buffer_widths[f'{unit[1]:02X}']
        elif byte not in (0xFC, 0xFF):
            widths[-1] += FONT_WIDTHS[byte]
    return widths


def test_inventory_is_exactly_the_400_snapshot_offsets() -> None:
    """Les doublons ne deviennent pas de nouvelles entrées et les seeds sont exclues."""
    source = ROOT / 'languages/en/combined_en.txt'
    source_map, _ = load_last_wins(source)
    selected = {o: t for o, t in source_map.items() if 0x28780 <= o <= 0x1A5301 and o not in SEEDS}

    assert hashlib.sha256(source.read_bytes()).hexdigest() == SNAPSHOT_SHA256
    assert DATA['source_snapshot_sha256'] == SNAPSHOT_SHA256
    assert len(ENTRIES) == len(selected) == 400
    assert {int(e['offset'], 16): e['source_en'] for e in ENTRIES} == selected
    assert {e['category'] for e in ENTRIES} <= {'dialogue', 'combat', 'interface', 'tables'}
    assert {s: sum(e['status'] == s for e in ENTRIES) for s in ('traduit', 'conserve', 'exclu')} == {
        'traduit': 355, 'conserve': 5, 'exclu': 40,
    }


@pytest.mark.parametrize('entry', ENTRIES, ids=lambda e: e['offset'])
def test_status_matches_last_wins_protection(entry: dict) -> None:
    """Toute injection est protégée exactement ; toute exclusion reste absente."""
    offset = int(entry['offset'], 16)
    live = _live()
    manifest = _manifest()

    assert entry['reason']
    if entry['status'] == 'exclu':
        assert offset not in live
        return
    assert offset in live
    assert offset in manifest
    assert manifest[offset].expected == live[offset]
    assert any(p['valid'] for p in entry['pointers'])
    assert not in_fixed_table(offset)
    assert entry['fixed_cell_bytes'] is None


@pytest.mark.parametrize('entry', [e for e in ENTRIES if e['status'] != 'exclu'], ids=lambda e: e['offset'])
def test_translation_preserves_binary_controls_and_fits_lines(entry: dict) -> None:
    """Contrôle octets, ordre, pauses, retours et largeur avec la police ROM figée."""
    raw = _encoded(_live()[int(entry['offset'], 16)])
    source = bytes.fromhex(entry['source_rom_hex'])

    assert len(source) == entry['source_bytes_with_terminator']
    assert source[-1] == 0xFF
    assert _controls(raw) == _controls(source)
    widths = _widths(raw, entry['buffer_widths_pixels'])
    assert max(widths) <= entry['max_line_pixels'], widths
    # Aucune cellule fixe dans ce lot : dépassement du budget EN implique relocation.
    if len(raw) > len(source):
        assert any(p['valid'] for p in entry['pointers'])


def test_retained_names_and_numeric_format_are_explicit() -> None:
    """Les noms et le chronomètre ne sont pas comptés comme traductions hindi."""
    live = _live()
    assert live[0x17D866] == 'Log Pokemon Research Lab'
    assert live[0x183482] == 'Valley Cave'
    assert live[0x1964A8] == 'Unbound Development Room'
    assert live[0x19A6B1] == 'Bra!'
    numeric = next(e for e in ENTRIES if e['offset'] == '0x17CC56')
    assert _encoded(live[0x17CC56]) == bytes.fromhex(numeric['source_rom_hex'])


@lru_cache(maxsize=1)
def _built_rom() -> bytes:
    return Path(os.environ.get('HI01_ROM', str(ROOT / 'output/roms/GenedRom-indie.gba'))).read_bytes()


@pytest.mark.rom
@pytest.mark.parametrize('entry', [e for e in ENTRIES if e['status'] != 'exclu'], ids=lambda e: e['offset'])
def test_built_rom_contains_exact_translation_at_every_live_pointer(entry: dict) -> None:
    """Un build vert ne suffit pas : vérifie toutes les cibles vivantes et le FF."""
    rom = _built_rom()
    expected = _encoded(_live()[int(entry['offset'], 16)])

    for pointer in entry['pointers']:
        if not pointer['valid']:
            continue
        site = int(pointer['site'], 16)
        target = struct.unpack_from('<I', rom, site)[0] - 0x08000000
        assert 0 <= target <= len(rom) - len(expected), pointer
        assert rom[target:target + len(expected)] == expected, (entry['offset'], pointer, hex(target))


@pytest.mark.rom
def test_source_rom_and_font_still_match_inventory() -> None:
    """La fixture provient de la vraie ROM EN et inclut les témoins de pointeurs."""
    source = Path(os.environ.get('HI01_SOURCE_ROM', str(ROOT / 'input/roms/englishrom.gba'))).read_bytes()
    from src.core.text_aliases import TextAliases

    assert hashlib.sha256(source).hexdigest() == DATA['source_rom_sha256']
    aliases = TextAliases.load(ROOT / 'languages/indie/data/hi01_preserved_sources.json', source)
    assert aliases.preservation is not None
    assert set(aliases.preservation.routes) == {int(e['offset'], 16) for e in ENTRIES if e['status'] != 'exclu'}
    font_offset = int(DATA['font_width_table_offset'], 16)
    assert source[font_offset:font_offset + 256] == FONT_WIDTHS
    for entry in ENTRIES:
        offset = int(entry['offset'], 16)
        raw = bytes.fromhex(entry['source_rom_hex'])
        assert source[offset:offset + len(raw)] == raw
        for pointer in entry['pointers']:
            site = int(pointer['site'], 16)
            assert source[site - 10:site].hex().upper() == pointer['context_before_hex']
            assert source[site:site + 4].hex().upper() == pointer['pointer_hex']


def test_preservation_contract_forces_relocation_of_all_selected_sources(tmp_path: Path) -> None:
    """Les 360 textes sont relogés sans rewrap ni réécriture des sources partagées."""
    from src.core.text_aliases import TextAliases
    from src.i18n import load_registry

    config = next(c for c in load_registry() if c.code == 'indie')
    assert config.text_aliases == 'languages/indie/data/hi01_preserved_sources.json'
    contract_path = ROOT / config.text_aliases
    contract = json.loads(contract_path.read_text())
    inventory = {int(e['offset'], 16): e for e in ENTRIES}
    pairs = {0x192079: (0x192116, 0x16AA68), 0x1A51F6: (0x1A5200, 0x1A6990)}
    selected = {o for o, e in inventory.items() if e['status'] != 'exclu'}
    assert len(selected) == 360
    assert contract['aliases'] == []
    assert {int(r['offset'], 16) for r in contract['preserved_sources']} == selected
    # Reconstitue uniquement les tranches ROM réelles du contrat ; aucune I/O simulée.
    slices = []
    for record in contract['preserved_sources']:
        offset = int(record['offset'], 16)
        assert record['english_raw_hex'] == inventory[offset]['source_rom_hex']
        slices.append((offset, bytes.fromhex(record['english_raw_hex'])))
        assert record['selected_interior_keys'] == []
        expected_interior = {(o, int(p['site'], 16))
                             for o, e in inventory.items()
                             if offset < o < offset + len(bytes.fromhex(record['english_raw_hex']))
                             for p in e['pointers']}
        assert {(int(r['target'], 16), int(r['offset'], 16)) for r in record['interior_references']} == expected_interior
        if offset in pairs:
            assert inventory[pairs[offset][0]]['status'] == 'exclu'
        assert {int(p, 16) for p in record['pointer_offsets']} == {
            int(p['site'], 16) for p in inventory[offset]['pointers'] if p['valid']
        }
        for ref in record['direct_references'] + record['interior_references']:
            target = int(ref['target'], 16)
            witness = next(p for p in inventory[target]['pointers'] if int(p['site'], 16) == int(ref['offset'], 16))
            context = bytes.fromhex(ref['context_hex'])
            assert context[:14].hex().upper() == witness['context_before_hex'] + witness['pointer_hex']
            slices.append((int(ref['context_start'], 16), context))
    source = bytearray(max(start + len(raw) for start, raw in slices))
    for start, raw in slices:
        source[start:start + len(raw)] = raw
    aliases = TextAliases.load(contract_path, bytes(source))
    payload = tmp_path / 'translations.json'
    payload.write_text(json.dumps({'translations': [
        {'offset': o, 'translation': _live()[o]} for o in sorted(selected)
    ]}))

    aliases.resolve_json(payload, selected)

    assert aliases.preservation is not None
    assert set(aliases.preservation.routes) == selected
    for item in json.loads(payload.read_text())['translations']:
        assert item['force_relocation'] is True
        assert item['preserve_control_flow'] is True
        assert item['allow_fallback'] is False
        assert item['allow_truncate'] is False
        assert item['padding_available'] == 0


@pytest.mark.rom
@pytest.mark.parametrize('parent,fragment,site', [
    (0x192079, 0x192116, 0x16AA68),
    (0x1A51F6, 0x1A5200, 0x1A6990),
])
def test_built_rom_preserves_interior_consumers(parent: int, fragment: int, site: int) -> None:
    """Les fragments EN exclus et leurs lecteurs gardent leurs octets originaux."""
    rom = _built_rom()
    inventory = {int(e['offset'], 16): e for e in ENTRIES}
    parent_raw = bytes.fromhex(inventory[parent]['source_rom_hex'])
    fragment_raw = bytes.fromhex(inventory[fragment]['source_rom_hex'])

    assert rom[parent:parent + len(parent_raw)] == parent_raw
    assert rom[fragment:fragment + len(fragment_raw)] == fragment_raw
    assert struct.unpack_from('<I', rom, site)[0] == 0x08000000 + fragment
    for pointer in inventory[parent]['pointers']:
        if pointer['valid']:
            assert struct.unpack_from('<I', rom, int(pointer['site'], 16))[0] != 0x08000000 + parent
