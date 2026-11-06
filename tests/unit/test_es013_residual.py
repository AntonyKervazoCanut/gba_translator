"""Qualification résiduelle : distinguer références, lecteurs et allocation."""
import json
from pathlib import Path

import pytest

from scripts.audit_es013_residual import literal_loads, validate_sources

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'tests/unit/fixtures/es013_residual_rom.json'


def test_literal_loads_respect_thumb_pc_alignment_and_register():
    # Arrange : LDR r3,[pc,#4] à +2 charge le mot à +8, pas +10.
    raw = bytes.fromhex('0000014b00000000f8564508')
    # Act / Assert : un candidat n'est pas qualifié automatiquement comme code.
    assert literal_loads(raw, 8) == [{'offset': '0x00000002', 'register': 3}]
    assert literal_loads(raw, 10) == []


def test_rom_identity_rejects_different_source():
    with pytest.raises(ValueError, match='SHA-256 EN'):
        validate_sources(b'wrong ROM', b'wrong ROM', {'source_sha256': 'x', 'es_sha256': 'y'})


def test_report_never_promotes_unknowns_to_window_or_allocation():
    report = json.loads((ROOT / 'docs/analysis/es/013_RESIDUAL.json').read_text())
    assert len(report['decorations']['keys']) == 54
    assert report['decorations']['window'] is None
    assert report['buffer']['physical_capacity_proven'] is None
    assert report['buffer']['upstream_declared_capacity'] == 1000
    assert report['buffer']['script_81_target'] == '0x09EC9D39'
    assert len(report['unrooted_system']['keys']) == 6
    assert all(t['base_references'] == [] for t in report['unrooted_system']['tables'])
    assert report['decorations']['base_references'] == ['0x0000014C']


@pytest.mark.emulator
@pytest.mark.parametrize('size', [512, 1000, 1001])
def test_native_f7_expander_has_no_capacity_guard(size):
    # Arrange : machine privée, aucun rendu ou sauvegarde. Allocation simulée
    # volontairement plus grande : ce test ne certifie PAS celle du jeu.
    from unicorn import UC_ARCH_ARM, UC_HOOK_MEM_WRITE, UC_MODE_THUMB, Uc
    from unicorn.arm_const import (
        UC_ARM_REG_LR,
        UC_ARM_REG_PC,
        UC_ARM_REG_R0,
        UC_ARM_REG_R1,
        UC_ARM_REG_SP,
    )
    fixture = json.loads(FIXTURE.read_text())
    cpu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    for base, length in [(0x08000000, 0x2000000), (0x02000000, 0x40000), (0x03000000, 0x8000)]:
        cpu.mem_map(base, length)
    for part in fixture['slices']:
        cpu.mem_write(0x08000000 + part['offset'], bytes.fromhex(part['hex']))
    destination, source, slot = 0x02021D18, 0x02030000, 0x02031000
    cpu.mem_write(destination - 1, b'\xa5' * 1200)
    cpu.mem_write(source, bytes.fromhex('f700ff'))
    cpu.mem_write(slot, b'\xbb' * (size - 1) + b'\xff')
    table = int.from_bytes(cpu.mem_read(0x0813CCE4, 4), 'little')
    cpu.mem_write(table, slot.to_bytes(4, 'little'))
    writes = []
    cpu.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, count, value, data:
                 writes.append((address, count)))
    cpu.reg_write(UC_ARM_REG_SP, 0x03007000)
    cpu.reg_write(UC_ARM_REG_LR, 0x03007F01)
    cpu.reg_write(UC_ARM_REG_R0, destination)
    cpu.reg_write(UC_ARM_REG_R1, source)
    # Act : expanseur + trampoline CFRU + StringCopy natifs, sans stub.
    cpu.emu_start(0x0813CCC9, 0x03007F00, count=100000)
    # Assert : 1001 écrit réellement au-delà des 1000 postulés ; aucun clamp.
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x03007F00
    assert bytes(cpu.mem_read(destination, size)) == b'\xbb' * (size - 1) + b'\xff'
    assert cpu.reg_read(UC_ARM_REG_R0) == destination + size - 1
    assert all(destination <= a and a + n <= destination + size
               or 0x03006F00 <= a and a + n <= 0x03007000 for a, n in writes)
    output_writes = [(a, n) for a, n in writes if a < 0x03000000]
    assert min(a for a, _ in output_writes) == destination
    assert max(a + n for a, n in output_writes) == destination + size
    assert bytes(cpu.mem_read(destination - 1, 1)) == b'\xa5'
    assert bytes(cpu.mem_read(destination + size, 1)) == b'\xa5'


@pytest.mark.rom
def test_canonical_audit_reproduces_report_and_fixtures():
    from scripts.audit_es013_residual import audit
    # Arrange : sources en lecture seule, fixtures issues des octets canoniques.
    en = (ROOT / 'input/roms/englishrom.gba').read_bytes()
    es = (ROOT / 'input/roms/spanishrom.gba').read_bytes()
    # Act
    report, fixture = audit(en, es, ROOT / 'docs/analysis/es')
    # Assert
    assert report == json.loads((ROOT / 'docs/analysis/es/013_RESIDUAL.json').read_text())
    assert fixture == json.loads(FIXTURE.read_text())


@pytest.mark.rom
@pytest.mark.parametrize('mutation,error', [
    ('duplicate_es', 'ambiguë'), ('selection', 'Sélection exacte'),
    ('en_preimage', 'Préimage EN'), ('es_preimage', 'Préimage ES'),
])
def test_audit_refuses_corrupted_evidence(tmp_path, mutation, error):
    from scripts.audit_es013_residual import audit
    # Arrange : les octets restent canoniques mais deux correspondances sont proposées.
    for name in ['013_PREPARATION.json', '013_SURFACES.json', '013_SYSTEM.json']:
        (tmp_path / name).write_bytes((ROOT / 'docs/analysis/es' / name).read_bytes())
    path = tmp_path / '013_SURFACES.json'
    surfaces = json.loads(path.read_text())
    entry = surfaces['entries'][0]
    if mutation == 'duplicate_es':
        entry['correspondances_es'] *= 2
    elif mutation == 'selection':
        surfaces['entries'][0] = surfaces['entries'][1]
    elif mutation == 'en_preimage':
        entry['source_hex'] = 'ff'
    else:
        entry['correspondances_es'][0]['preimage_hex'] = 'ff'
    path.write_text(json.dumps(surfaces))
    # Act / Assert : aucun choix silencieux de la première correspondance.
    with pytest.raises(ValueError, match=error):
        audit((ROOT / 'input/roms/englishrom.gba').read_bytes(),
              (ROOT / 'input/roms/spanishrom.gba').read_bytes(), tmp_path)
