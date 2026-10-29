"""Acheminement ES-002 complet, copies temporaires et vrais patches du driver."""
import json
import os
import shutil
from dataclasses import replace
from pathlib import Path

import pytest

from scripts import build_language as driver
from src.core.item_description_routes import SystemTextRoutes
from src.core.text_codec import SPANISH_GLYPH_CHARS, TextEncoder

ROOT = Path(__file__).resolve().parents[3]
pytestmark = [pytest.mark.rom, pytest.mark.slow]


def test_thirteen_entries_and_six_relocated_neighbours(tmp_path, monkeypatch):
    fixture = json.loads((ROOT / 'tests/unit/fixtures/es002_routing.json').read_text())
    source = driver.ENGLISH_ROM.read_bytes()
    values = {int(e['offset'], 16): e['traduction'].replace('\\n', '\n') for e in fixture['entries']}
    neighbours = {e['offset']: e['pointer_offsets'] for e in fixture['neighbours']}
    for key in neighbours:
        end = source.index(255, key)
        values[key] = 'TEST B1032 ' + ''.join(f'<0x{b:02X}>' for b in source[key:end])
    combined = tmp_path / 'combined.txt'
    combined.write_text(''.join(f'0x{k:08X}: '+v.replace('\n', r'\n')+'\n' for k,v in values.items()))
    config = driver.load_registry().get('es-maint')
    config = replace(config, combined=str(combined), output_rom=str(tmp_path / 'probe.gba'),
                     text_aliases=str(ROOT / config.text_aliases),
                     item_descriptions=str(ROOT / config.item_descriptions),
                     system_texts=str(ROOT / config.system_texts))
    with monkeypatch.context() as patch:
        patch.setattr(driver, 'REPO_ROOT', tmp_path)
        patch.setattr(driver, 'TRANSLATION_DIR', tmp_path / 'output/translation')
        ready = driver.generate_translation_json(config)
    items = json.loads(ready.read_text())['translations']
    by_key = {i.get('contract_offset', i['offset']): i for i in items}
    for entry in fixture['entries']:
        key = int(entry['offset'],16)
        if 'cellule' not in entry:
            assert key in by_key
            assert by_key[key]['pointer_offsets'] == [int(p,16) for p in entry['referents_en']]
    # Consommateurs réels figés : les deux occurrences dans le code Thumb
    # pour 1C0DB0 ne sont pas des pointeurs et restent hors des plages autorisées.
    for key, refs in neighbours.items():
        for site in refs:
            assert source[site:site+4] == (key + 0x08000000).to_bytes(4, 'little')
        by_key[key]['pointer_offsets'] = refs
    output = driver.build_rom(config, ready)
    built = output.read_bytes()
    # The builder may only touch exact source spans, targets and pointer sites.
    allowed = bytearray(len(source))
    for item in items:
        offset = item['offset']
        length = item['original_length'] + 1
        allowed[offset:offset+length] = b'\x01' * length
        normalized = SystemTextRoutes.normalize(item)
        raw = TextEncoder.encode_pokemon(normalized['translation'], skip_aliases=SPANISH_GLYPH_CHARS)
        for site in item.get('pointer_offsets', []):
            allowed[site:site+4] = b'\x01'*4
            target = int.from_bytes(built[site:site+4], 'little')-0x08000000
            allowed[target:target+len(raw)] = b'\x01'*len(raw)
    assert not [i for i,(a,b) in enumerate(zip(source,built)) if a != b and not allowed[i]][:20]
    for key in neighbours:
        assert by_key[key]['pointer_offsets']
        assert all(int.from_bytes(built[p:p+4], 'little') != key+0x08000000
                   for p in by_key[key]['pointer_offsets']), hex(key)
        end = source.index(255,key)+1
        assert built[key:end+16] == source[key:end+16]
    # La passe inline doit ignorer ces cellules déjà prises en charge ; aucune
    # ancienne adresse ni traduction par template ne doit être réécrite.
    driver.apply_patches(replace(config, patches=['inline']), output, ready, build_number=0)
    assert output.read_bytes() == built
    driver.apply_patches(config, output, ready, build_number=0)
    final = output.read_bytes()
    SystemTextRoutes.load(ROOT / config.system_texts, source).verify(final, ready)
    for entry in fixture['entries']:
        key = int(entry['offset'],16)
        raw = TextEncoder.encode_pokemon(values[key], skip_aliases=SPANISH_GLYPH_CHARS)
        if 'cellule' in entry:
            assert len(raw) <= 13
            assert final[key:key+len(raw)] == raw
            assert final[key+13:key+14] == source[key+13:key+14] or key+13 in values
        else:
            for ref in entry['referents_en']:
                site = int(ref,16)
                live = int.from_bytes(final[site:site+4], 'little')-0x08000000
                assert final[live:live+len(raw)] == raw
            if 'offset_vivant_en' in entry:
                assert final[key] == source[key] == 0xAA
        end = key + len(bytes.fromhex(entry['en_complet_hex']))
        if 'cellule' not in entry:
            assert final[end:end+16] == source[end:end+16]
    for key in neighbours:
        end = source.index(255,key)+1
        assert final[key:end+16] == source[key:end+16]
    for site in [0xD80A0,0x11B4B4]:
        assert final[site:site+4] == (0x0823E558).to_bytes(4,'little')
    # No cell except the five requested indices may change in the fixed table.
    for index in range(107):
        off = 0x23E558 + 13*index
        if off not in values:
            assert final[off:off+13] == source[off:off+13]
    if os.environ.get('B1032_PROBE_ROM'):
        shutil.copy2(output, os.environ['B1032_PROBE_ROM'])
