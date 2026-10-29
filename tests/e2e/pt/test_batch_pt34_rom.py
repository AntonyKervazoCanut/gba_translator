"""PT-34 : preuve binaire des tables obsolètes et des consommateurs réels."""
import hashlib
import json
import re
from pathlib import Path

import pytest

from languages.fr.patches.font import lz77_decompress
from src.core.text_codec import TextDecoder

ROOT = Path(__file__).resolve().parents[3]
AUDIT = json.loads((ROOT / 'languages/pt/data/pt34_audit.json').read_text())
pytestmark = pytest.mark.rom


@pytest.fixture(scope='module')
def source():
    return (ROOT / 'input/roms/englishrom.gba').read_bytes()


def test_every_source_preimage_and_all_absolute_references(source):
    assert hashlib.sha256(source).hexdigest() == AUDIT['source_sha256']
    for row in AUDIT['entries']:
        offset = int(row['offset'], 16)
        raw = bytes.fromhex(row['source_hex'])
        assert source[offset:offset + len(raw)] == raw
        refs = [m.start() for m in re.finditer(
            re.escape((offset + 0x08000000).to_bytes(4, 'little')), source)]
        assert refs == row['raw_references'], row['offset']
        for copy in row['related_copies']:
            for site in copy['legacy_references']:
                assert int.from_bytes(source[site:site + 4], 'little') == int(copy['offset'], 16) + 0x08000000
        for consumer in row['current_move_consumers']:
            site, target = int(consumer['pointer'], 16), int(consumer['target'], 16)
            assert int.from_bytes(source[site:site + 4], 'little') == target + 0x08000000
            assert TextDecoder.decode_pokemon(source[target:source.index(255, target)]) == consumer['english']


def test_old_table_has_no_consumer_and_false_pointers_are_not_text(source):
    table = AUDIT['legacy_move_table']
    start, end = int(table['start'], 16), int(table['end_exclusive'], 16)
    incoming = []
    # Recherche à chaque octet, pas uniquement aux adresses alignées.
    for match in re.finditer(b'[\x08-\x09]', source):
        site = match.start() - 3
        if site < 0:
            continue
        target = int.from_bytes(source[site:site + 4], 'little') - 0x08000000
        if start <= target < end:
            incoming.append((site, target))
    assert incoming == [(0xC48659, 0x904455)]
    for evidence in AUDIT['non_text_evidence']:
        if evidence['kind'] == 'lz77':
            block = int(evidence['start'], 16)
            decoded, length = lz77_decompress(source, block)
            assert length == evidence['compressed_bytes']
            assert len(decoded) == evidence['decoded_bytes']
            assert block < int(evidence['site'], 16) < block + length - 3
    # Motif 32 09 92 08 traversant trois instructions Thumb, pas un littéral.
    assert source[0x1E7B78:0x1E7B7E] == bytes.fromhex('013209920870')


def test_actual_readers_use_the_new_table(source):
    for literal in AUDIT['active_move_table_literals']:
        site = int(literal, 16)
        assert int.from_bytes(source[site:site + 4], 'little') == 0x0899F194
    for block in AUDIT['instruction_preimages']:
        start, raw = int(block['offset'], 16), bytes.fromhex(block['hex'])
        assert source[start:start + len(raw)] == raw
    # LDR littéral Thumb : les trois lecteurs chargent exactement ces cellules.
    for instruction, literal in [(0xE541A, 0xE5440), (0x137B7A, 0x137BC8), (0x9F3B4C, 0x9F3B64)]:
        opcode = int.from_bytes(source[instruction:instruction + 2], 'little')
        assert opcode & 0xF800 == 0x4800
        assert ((instruction + 4) & ~3) + (opcode & 0xFF) * 4 == literal
    for literal in (0x1C4, 0x1367A8, 0x9A945C):
        assert int.from_bytes(source[literal:literal + 4], 'little') == 0x0896DE04


def test_source_and_built_tables_never_reach_pt34(source):
    built = (ROOT / 'output/roms/GenedRom-pt.gba').read_bytes()
    spans = [(int(r['offset'], 16), int(r['offset'], 16) + len(bytes.fromhex(r['source_hex'])))
             for r in AUDIT['entries']]
    for rom in (source, built):
        for table, count in ((0x99F190, 894), (0x96DE04, 293)):
            for index in range(count):
                pointer = table + index * 4
                target = int.from_bytes(rom[pointer:pointer + 4], 'little') - 0x08000000
                assert not any(start <= target < end for start, end in spans), (hex(pointer), hex(target))
    # Aucune traduction PT-34 ni patch de table : les copies mortes restent intactes.
    for start, end in spans:
        assert built[start:end] == source[start:end]
