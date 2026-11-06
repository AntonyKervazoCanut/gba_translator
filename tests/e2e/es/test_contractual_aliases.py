"""Preuve du pipeline réel : aucune sentinelle n'est écrite dans les sources."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.text_codec import TextEncoder
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]


def test_all_contractual_sentinels_reach_live_pointers(tmp_path, monkeypatch):
    config = load_registry().get('es-maint')
    contract_path = ROOT / config.text_aliases
    records = json.loads(contract_path.read_text())['aliases']
    sources = [ROOT / c.combined for c in load_registry()]
    sources += list((ROOT / 'languages').glob('*/protected_entries.yaml'))
    sources += list((ROOT / 'input/roms').glob('*.gba'))
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    combined = tmp_path / 'combined_sentinel.txt'
    sentinel = 'ALIASB1030 '
    lines = []
    for record in records:
        raw = bytes.fromhex(record['english_raw_hex'])[:-1]
        # Literal bytes preserve every command AND its arguments, FA/FB and FD order.
        text = ('Z' if 'layout' in record else sentinel) + ''.join(f'<0x{b:02X}>' for b in raw)
        lines.append(f"{record['contract_offset']}: {text}\n")
    combined.write_text(''.join(lines))
    config = replace(config, combined=str(combined), text_aliases=str(contract_path),
                     item_descriptions=str(ROOT / config.item_descriptions),
                     system_texts=str(ROOT / config.system_texts),
                     output_rom=str(tmp_path / 'sentinel.gba'))
    with monkeypatch.context() as patch:
        patch.setattr(driver, 'REPO_ROOT', tmp_path)
        patch.setattr(driver, 'TRANSLATION_DIR', tmp_path / 'output/translation')
        ready = driver.generate_translation_json(config)
    items = json.loads(ready.read_text())['translations']
    assert len(items) == len(records)
    assert {i['contract_offset'] for i in items} == {int(r['contract_offset'], 16) for r in records}
    for item in items:
        record = next(r for r in records if int(r['contract_offset'], 16) == item['contract_offset'])
        assert item['offset'] == int(record['live_offset'], 16)
        assert item['pointer_offsets']
    output = driver.build_rom(config, ready)
    driver.apply_patches(config, output, ready, build_number=0)
    rom = output.read_bytes()
    english = driver.ENGLISH_ROM.read_bytes()
    prefix = TextEncoder.encode_pokemon(sentinel)[:-1]
    for record in records:
        key = int(record['contract_offset'], 16)
        raw = bytes.fromhex(record['english_raw_hex'])
        # Relocation is required: sentinel + complete source exceeds the old budget.
        expected = (TextEncoder.encode_pokemon('Z')[:-1] if 'layout' in record else prefix) + raw
        for pointer in record['pointer_offsets']:
            p = int(pointer, 16)
            live = int.from_bytes(rom[p:p + 4], 'little') - 0x08000000
            assert live != key and live != int(record['live_offset'], 16)
            assert rom[live:live + len(expected)] == expected
        end = int(record['live_offset'], 16) + len(raw)
        assert rom[key:end] == english[key:end]
    assert {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources} == before
