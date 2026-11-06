"""Pipeline complet ES-016 avec sentinelles locales, sans traduction de production."""
import pytest

from tests.e2e.es.test_es015_routing import run_routing_pipeline

pytestmark = [pytest.mark.rom, pytest.mark.slow]


def test_es016_real_pipeline_preserves_all_unselected_consumers(tmp_path, monkeypatch):
    keys = {0x772093, 0x781278, 0x781668, 0x788255, 0x78C2A8, 0x78C2FD,
            0x7808DE, 0x788538, 0x78D43E}
    run_routing_pipeline(keys, tmp_path, monkeypatch, 'es016', 9)
