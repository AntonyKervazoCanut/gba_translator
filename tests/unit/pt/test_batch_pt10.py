"""PT-10 : périmètre, contrôles binaires et grammaire des messages de combat."""
import json
import re
from pathlib import Path

import yaml

from src.core.text_codec import TextEncoder
from tests.unit.de.test_combat_ui_03 import commands

ROOT = Path(__file__).resolve().parents[3]


def entries():
    """Résout les textes PT sans perdre les espaces explicites des buffers."""
    return {int(m[1], 16): m[2] for line in
            (ROOT / 'languages/pt/combined_pt.txt').read_text().splitlines()
            if (m := re.match(r'0x([0-9a-fA-F]+): ?(.*)', line))}


def audit():
    return json.loads((ROOT / 'languages/pt/data/pt10_audit.json').read_text())['entries']


def test_manifest_scope_and_exact_protection():
    batches = json.loads((ROOT / 'languages/pt/translation_batches.json').read_text())
    offsets = next(b['offsets'] for b in batches if b['id'] == 'PT-10')
    rows = audit()
    assert len(rows) == len(offsets) == 282
    assert {r['offset'] for r in rows} == set(offsets)
    texts = entries()
    protected = yaml.safe_load((ROOT / 'languages/pt/protected_entries.yaml').read_text())
    guards = {int(e['offset'], 16): e.get('expected') for e in protected['entries']}
    active = [r for r in rows if r['status'] == 'translated']
    assert len(active) == 260
    for row in rows:
        offset = int(row['offset'], 16)
        assert row['reason'] and row['source_hex'] and row['english']
        if row['status'] == 'exception':
            assert offset not in texts
            assert not row['source_sites']
        else:
            assert row['source_sites']
            assert guards[offset] == texts[offset]
            assert row['portuguese'] == texts[offset]
            encoded = TextEncoder.encode_pokemon(texts[offset].replace(r'\n', '\n'), strict=True)
            assert row['encoded_bytes'] == len(encoded)


def test_exact_command_arguments_and_break_positions():
    texts = entries()
    for row in audit():
        if row['status'] != 'translated':
            continue
        encoded = TextEncoder.encode_pokemon(texts[int(row['offset'], 16)].replace(r'\n', '\n'), strict=True)
        source = bytes.fromhex(row['source_hex'])
        assert encoded[-1] == 0xFF and 0xFF not in encoded[:-1]
        assert commands(encoded) == commands(source), row['offset']
        assert len(encoded) <= 512


def test_stat_change_buffers_form_correct_portuguese():
    texts = entries()
    for offset, verb, modifier, ending in [
        (0x3FCB5F, 'aumentou', 0x3FCB41, 0x3FCB4A),
        (0x3FCB6A, 'aumentou', 0x3FCB41, 0x3FCB4A),
        (0x3FCB8F, 'diminuiu', 0x3FCB50, 0x3FCB59),
        (0x3FCB9A, 'diminuiu', 0x3FCB50, 0x3FCB59),
    ]:
        template = texts[offset].split(r'\n')[1]
        assert template.replace('<0xFD><0x01>', texts[ending]) == verb + ' !'
        buffer = texts[modifier].replace('<0x00>', ' ') + texts[ending]
        assert template.replace('<0xFD><0x01>', buffer) == verb + ' muito!'
        assert template.replace('<0xFD><0x01>', 'drastically !') == verb + ' drastically !'
    assert 0x3FCB4B not in texts  # Ancien suffixe « ose! » : aucune écriture.


def test_glossary_and_capture_audio_are_preserved():
    texts = entries()
    assert [texts[o] for o in [0x3FD590, 0x3FD593, 0x3FD59A, 0x3FD5A2]] == [
        'PS', 'Ataque', 'Defesa', 'Velocidade']
    # F-759 interdit d'inventer une abréviation : le nom intégral déborde
    # avec un préfixe adversaire + surnom de dix W (230/229 > 224 px).
    assert texts[0x3FD5A8] == 'Sp. Atk' and texts[0x3FD5B0] == 'Sp. Def'
    assert 'Nature Power' in texts[0x3FC26D]
    assert 'Magic Coat' in texts[0x3FC4F0]
    assert 'Liquid Ooze' in texts[0x3FC9E5]
    assert 'Poké Ball' in texts[0x3FD697]
    assert 'HM' in texts[0x3FCC39]
    for offset in [0x3FD7A2, 0x3FD7C0]:
        assert '<0xFD><0x3A>' in texts[offset]
        assert '<0xFC><0x0A><0xFC><0x0B><0x42><0x01>' in texts[offset]
