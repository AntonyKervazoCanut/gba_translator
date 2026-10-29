"""Contrat binaire ES indépendant des alias et des attentes calculées."""
from src.core.text_codec import TextEncoder


def test_spanish_bytes_preserve_every_glyph():
    from src.core.text_codec import SPANISH_GLYPH_CHARS
    assert TextEncoder.encode_pokemon("áéíóúüñÁÉÍÓÚÜÑ¡¿", skip_aliases=SPANISH_GLYPH_CHARS) == bytes.fromhex("17 1b 6f 23 27 f6 29 02 06 5a 0e 12 f3 14 52 51 ff")


def test_default_french_aliases_stay_identical():
    assert TextEncoder.encode_pokemon("üÜ¡¿") == bytes.fromhex("e9 cf ab ac ff")


def test_empty_seed_requires_explicit_builder_permission(tmp_path):
    import importlib
    mod = importlib.import_module('src.translators.19_build_translated_rom_generic')
    config = mod.BuildConfig(source_rom=tmp_path / 'source.gba')
    builder = mod.TranslatedROMBuilder(config)
    assert builder._strategy_translate() is False
    config.allow_empty_translations = True
    assert builder._strategy_translate() is True


def test_inline_empty_seed_preserves_rom(tmp_path):
    import subprocess
    import sys
    source = tmp_path / 'source.gba'
    source.write_bytes(b'\x00\xff' * 256)
    combined = tmp_path / 'combined.txt'
    combined.write_text('# Création initiale vide autorisée\n')
    result = subprocess.run([sys.executable, 'scripts/apply_inline_overrides_fr.py', '--rom', str(source), '--source', str(source), '--combined', str(combined), '--allow-empty-translations'], capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert source.read_bytes() == b'\x00\xff' * 256


def test_preservation_profile_is_opt_in_for_historical_spanish(tmp_path):
    import importlib
    mod = importlib.import_module('src.translators.19_build_translated_rom_generic')
    cfg = mod.BuildConfig(source_rom=tmp_path / 'source.gba', language='spanish')
    builder = mod.TranslatedROMBuilder(cfg)
    assert builder._skip_encode_aliases() == frozenset()
    cfg.preserve_spanish_glyphs = True
    assert TextEncoder.encode_pokemon('üÜ¡¿', skip_aliases=builder._skip_encode_aliases()) == bytes.fromhex('f6 f3 52 51 ff')


def test_spanish_release_manifest_stays_in_progress(tmp_path):
    from scripts.package_release import PatchReleasePackager
    from src.i18n import load_registry
    cfg = load_registry().get('es-maint')
    source = cfg.patch_source_path(tmp_path)
    target = cfg.output_rom_path(tmp_path)
    source.parent.mkdir(parents=True)
    target.parent.mkdir(parents=True)
    source.write_bytes(b'\x00' * 256)
    target.write_bytes(b'\x00' * 255 + b'\xff')
    manifest = PatchReleasePackager(root=tmp_path).package([cfg])
    entry = manifest['languages'][0]
    assert entry['code'] == 'es-maint'
    assert entry['status'] == 'in_progress'
    assert entry['patch'] == 'pokemon_unbound_es-maint.bps'
    assert entry['target']['file'] == 'GenedRom-es-maint.gba'


def test_spanish_profile_preserves_complete_control_commands():
    from src.core.text_codec import SPANISH_GLYPH_CHARS
    text = '<0xFD><0x01>ü<0xFC><0x01><0x02>¡¿<0xFA><0xFB>'
    assert TextEncoder.encode_pokemon(text, skip_aliases=SPANISH_GLYPH_CHARS) == bytes.fromhex('fd 01 f6 fc 01 02 52 51 fa fb ff')
