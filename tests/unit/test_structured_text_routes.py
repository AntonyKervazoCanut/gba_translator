"""Routage canonique : consommateurs audités, config et isolation du JSON."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from languages.pt.patches.batch_20 import BorriusTextPatch
from scripts.build_language import structured_text_routes
from src.core.structured_text import StructuredTextRoutes
from src.i18n import load_registry

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def patch():
    # Préimage binaire réelle du manifeste PT-86 ; le reste n'est jamais alloué.
    row = next(r for r in json.loads((ROOT / 'languages/pt/data/pt86_audit.json').read_text())['entries']
               if r['offset'] == '0x1f9b330')
    offset = int(row['offset'], 16)
    raw = bytes.fromhex(row['source_hex'])
    source = bytearray(offset + len(raw))
    source[offset:] = raw
    for ref in row['references'] + row['non_text_references']:
        source[ref:ref + 4] = (offset + 0x08000000).to_bytes(4, 'little')
    return BorriusTextPatch(bytes(source), [row], ROOT / 'languages/pt/combined_pt.txt')


def test_enrichment_preserves_input_and_bounds_canonical_bytes(patch):
    routes = StructuredTextRoutes([patch])
    original = {'translations': [{'offset': 0x100, 'translation': 'intact'}]}

    result = routes.enrich(original)

    assert original == {'translations': [{'offset': 0x100, 'translation': 'intact'}]}
    entry = result['translations'][1]
    assert bytes.fromhex(entry['raw_bytes']) == patch.entries()[0][2]
    assert entry['max_length'] == 210
    assert entry['padding_available'] == 0
    assert entry['allow_fallback'] is False
    assert entry['allow_truncate'] is False
    assert routes.enrich(result) == result


def test_duplicate_owner_rejected(patch):
    with pytest.raises(ValueError, match='propriétaires'):
        StructuredTextRoutes([patch, patch])


@pytest.mark.parametrize('patches', [[], ['batch_86', 'batch_86']])
def test_missing_or_repeated_finalizer_rejected(patches):
    config = SimpleNamespace(structured_text_patches=['batch_86'], patches=patches)
    with pytest.raises(ValueError, match='exactement une fois'):
        structured_text_routes(config)


def test_only_portuguese_opts_in_to_canonical_structured_routing():
    registry = load_registry()
    assert set(registry.get('pt').structured_text_patches) == {
        'batch_83', 'batch_84', 'batch_85', 'batch_86', 'batch_87', 'batch_88'}
    for code in ('fr', 'it', 'de'):
        assert structured_text_routes(registry.get(code)) is None


def test_inline_dispatch_protects_only_canonical_cells(tmp_path, monkeypatch, patch):
    from dataclasses import replace

    from scripts import build_language
    from scripts.apply_inline_overrides_fr import _load_translation_offsets

    config = replace(load_registry().get('pt'), patches=['inline'])
    routes = StructuredTextRoutes([patch])
    path = tmp_path / 'pt.json'
    path.write_text(json.dumps(routes.enrich({'translations': [
        {'offset': 0x100, 'translation': 'autre'}]})))
    calls = []
    monkeypatch.setattr(build_language, 'run', lambda cmd: calls.append(cmd))

    build_language.apply_patches(config, tmp_path / 'pt.gba', path)

    command = calls[0]
    protected = command[command.index('--translations') + 1]
    assert _load_translation_offsets(protected) == {0x1F9B330}
    assert '--no-template-fallback' in command
