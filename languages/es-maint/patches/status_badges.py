"""Badges ENV/QUE/CON/PAR/DOR/DEB, contrat du glossaire D-849."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.core.status_badge_patcher import StatusBadgePatcher
from src.i18n import load_registry

LETTERS = {
    "E": ("1111", "1000", "1110", "1000", "1000", "1111"),
    "N": ("1001", "1101", "1011", "1011", "1001", "1001"),
    "V": ("1001", "1001", "1001", "1001", "0110", "0110"),
    "Q": ("0110", "1001", "1001", "1001", "1010", "0101"),
    "U": ("1001", "1001", "1001", "1001", "1001", "0110"),
    "C": ("0111", "1000", "1000", "1000", "1000", "0111"),
    "O": ("0110", "1001", "1001", "1001", "1001", "0110"),
    "P": ("1110", "1001", "1001", "1110", "1000", "1000"),
    "A": ("0110", "1001", "1001", "1111", "1001", "1001"),
    "R": ("1110", "1001", "1001", "1110", "1010", "1001"),
    "D": ("1110", "1001", "1001", "1001", "1001", "1110"),
    "B": ("1110", "1001", "1110", "1001", "1001", "1110"),
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    args = parser.parse_args()
    StatusBadgePatcher.apply(args.rom, load_registry().get("es-maint").status_abbrev, LETTERS)
