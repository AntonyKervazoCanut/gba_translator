"""Contrôle les pixels des six statuts, sans réutiliser l'encodeur texte."""
import importlib

from languages.fr.patches.font import lz77_compress, lz77_decompress
from src.core.status_badge_patcher import StatusBadgePatcher


def test_six_statuses_preserve_borders_and_neighbours(tmp_path):
    module = importlib.import_module('languages.es-maint.patches.status_badges')
    labels = {'poison': 'ENV', 'paralysis': 'PAR', 'sleep': 'DOR', 'freeze': 'CON', 'burn': 'QUE', 'faint': 'DEB'}
    original = bytes([0x99] * 1024)
    compressed = lz77_compress(original)
    rom = bytearray(b'\xff' * 4096)
    rom[:len(compressed)] = compressed
    path = tmp_path / 'badges.gba'
    path.write_bytes(rom)
    class FixturePatcher(StatusBadgePatcher):
        BLOCKS = (0,)
    FixturePatcher.apply(path, labels, module.LETTERS)
    tiles, _ = lz77_decompress(path.read_bytes(), 0)
    # Lettre E : rangée haute pleine, rangée suivante à gauche seulement.
    assert tiles[36:38] == bytes.fromhex('29 22')
    assert tiles[40:42] == bytes.fromhex('29 99')
    for slot in [0, 1, 2, 3, 4, 6]:
        assert tiles[slot*128:slot*128+32] == original[slot*128:slot*128+32]
        assert tiles[slot*128+96:(slot+1)*128] == original[slot*128+96:(slot+1)*128]
    for slot in [5, 7]:
        assert tiles[slot*128:(slot+1)*128] == original[slot*128:(slot+1)*128]
    assert path.with_suffix('.gba.bak').read_bytes() == rom
