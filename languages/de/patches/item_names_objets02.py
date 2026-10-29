"""B-1027 : noms inline du lot objets-02, depuis combined_de.txt uniquement."""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from languages.de.patches.item_names import apply_scoped_item_names, encode  # noqa: E402
from scripts.check_translation_integrity import load_last_wins  # noqa: E402

# Liste exclusive B-1027 ; aucune recherche globale de chaînes ni relocation.
EXPECTED_NAMES = {
    0x879E28: "Jade Orb",
    0x879E54: "Grimy Socks",
    0x879EAC: "Mega Ring",
    0x879F04: "Key Card: 1",
    0x879F30: "Time Turner",
    0x879FB4: "Baby Monitor",
    0x879FE0: "Motorcycle",
    0x87A0BC: "Berry Pouch",
    0x87A114: "Notebook",
    0x87AE7C: "Necrozium Z",
    0x87AEA8: "Venusaurite",
    0x87AED4: "Charizite X",
    0x87AF00: "Charizite Y",
    0x87AF2C: "Blastoisite",
    0x87AF58: "Beedrillite",
    0x87AF84: "Pidgeotite",
    0x87AFB0: "Alakazite",
    0x87AFDC: "Slowbronite",
    0x87B008: "Gengarite",
    0x87B034: "Kangaskhite",
    0x87B060: "Pinsirite",
    0x87B08C: "Gyaradosite",
    0x87B0B8: "Aerodactite",
    0x87B0E4: "Mewtwonite X",
    0x87B110: "Mewtwonite Y",
    0x87B13C: "Ampharosite",
    0x87B168: "Steelixite",
    0x87B194: "Scizorite",
    0x87B1C0: "Heracronite",
    0x87B1EC: "Houndoomite",
    0x87B218: "Tyranitarite",
    0x87B244: "Sceptilite",
    0x87B270: "Blazikenite",
    0x87B29C: "Swampertite",
    0x87B2C8: "Gardevoirite",
    0x87B2F4: "Sablenite",
    0x87B320: "Mawilite",
    0x87B34C: "Aggronite",
    0x87B378: "Medichamite",
    0x87B3A4: "Manectite",
    0x87B3D0: "Sharpedonite",
    0x87B3FC: "Cameruptite",
    0x87B428: "Altarianite",
    0x87B454: "Banettite",
    0x87B480: "Absolite",
    0x87B4AC: "Glalitite",
    0x87B4D8: "Salamencite",
    0x87B504: "Metagrossite",
    0x87B530: "Latiasite",
    0x87B55C: "Latiosite",
    0x87B588: "Lopunnite",
    0x87B5B4: "Garchompite",
    0x87B5E0: "Lucarionite",
    0x87B60C: "Abomasite",
    0x87B638: "Galladite",
    0x87B664: "Audinite",
    0x87B690: "Diancite",
    0x87B6E8: "Assault Vest",
    0x87B740: "Fist Plate",
    0x87B76C: "Sky Plate",
    0x87B798: "Toxic Plate",
    0x87B7C4: "Earth Plate",
    0x87B7F0: "Stone Plate",
    0x87B81C: "Insect Plate",
    0x87B848: "Spooky Plate",
    0x87B874: "Iron Plate",
    0x87B8A0: "Flame Plate",
    0x87B8CC: "Splash Plate",
    0x87B8F8: "Meadow Plate",
    0x87B924: "Zap Plate",
    0x87B950: "Mind Plate",
    0x87B97C: "Icicle Plate",
    0x87B9A8: "Draco Plate",
    0x87B9D4: "Dread Plate",
    0x87BA00: "Pixie Plate",
    0x87BA2C: "Comet Shard",
    0x87BAB0: "Casteliacone",
    0x87BADC: "Lumiose Gale",
    0x87BB08: "Ragecandybar",
    0x87BB60: "Old Gateau",
    0x87BBB8: "Armor Fossil",
    0x87BBE4: "Cover Fossil",
    0x87BC3C: "Jaw Fossil",
    0x87BC94: "Mega Earing",
    0x87BCC0: "Mega Charm",
    0x87BD18: "Mega Anklet",
    0x87BD44: "Mega Pendant",
    0x87BD70: "Adamant Orb",
    0x87BD9C: "Lustrous Orb",
    0x87BDC8: "Griseous Orb",
    0x87BE20: "DNA Splicers",
    0x87BE4C: "Reveal Glass",
    0x87C3F8: "Focus Sash",
    0x87C558: "Protect Pads",
    0x87C660: "Terrain Ext.",
    0x87C68C: "Wise Glasses",
    0x87C6E4: "Grassy Seed",
    0x87C710: "Misty Seed",
    0x87C73C: "Psychic Seed",
    0x87C978: "Electric Gem",
    0x87CA28: "Dark Gem",
    0x87CBE0: "Bottle Cap",
    0x87CCBC: "Purp Nectar",
    0x87CD98: "Love Ball",
}
ROUTINE_OFFSET = 0x9A8CA
ROUTINE = bytes.fromhex("2c2148430249401802bc0847000000628708")
NAME_SIZE = 14


def apply(data: bytearray, texts: dict[int, str], source: bytes) -> int:
    """Réutilise le raccordement B-1026 avec le périmètre distinct B-1027."""
    for rom in (source, data):
        if rom[ROUTINE_OFFSET:ROUTINE_OFFSET + len(ROUTINE)] != ROUTINE:
            raise ValueError("Routine/base de table des objets inattendue")
    preimages = {}
    for offset, english in EXPECTED_NAMES.items():
        cell = source[offset:offset + NAME_SIZE]
        if not cell.startswith(encode(english) + b"\xff"):
            raise ValueError(f"0x{offset:X}: préimage anglaise inattendue")
        preimages[offset] = cell
    return apply_scoped_item_names(data, source, texts, preimages=preimages)


def main() -> int:
    """Applique le raccordement à une ROM de sortie avec sauvegarde préalable."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path, required=True)
    parser.add_argument("--combined", type=Path, default=ROOT / "languages/de/combined_de.txt")
    args = parser.parse_args()
    original = args.rom.read_bytes()
    data = bytearray(original)
    texts, _ = load_last_wins(args.combined)
    source = (ROOT / "input/roms/englishrom.gba").read_bytes()
    if hashlib.sha256(source).hexdigest() != "7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7":
        raise ValueError("ROM source non canonique")
    count = apply(data, texts, source)
    if count:
        Path(str(args.rom) + ".bak").write_bytes(original)
        Path(str(args.rom) + ".objets02.bak").write_bytes(original)
        args.rom.write_bytes(data)
    print(f"Objets-02 DE : {count}/104 noms raccordés")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

