"""Relit les 228 descriptions B-688 aux pointeurs actifs, sans écrire de ROM."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from languages.fr.patches.tm_item_descriptions import load_combined
from src.core import moves
from src.core.pokedex import line_width
from src.core.text_codec import GERMAN_UMLAUT_CHARS, TextEncoder


def inspect_reference(rom: bytes, source: bytes, row: dict, combined: dict) -> dict:
    """Conserve l'index du consommateur ; ne cherche pas le texte dans la ROM."""
    pointer = (moves.struct_offset(row['index']) if row['kind'] == 'move'
               else 0x876074 + row['index'] * 44 + 0x14)
    original = moves._deref(source, pointer)
    target = moves._deref(rom, pointer)
    assert original == int(row['offset'], 16), 'La table source a changé'
    text = moves._decode(rom, target, 1000)
    original_text = moves._decode(source, original, 1000)
    expected = combined.get(original)
    expected = expected.replace('\\n', '\n') if expected else None
    lines = text.splitlines() if text else []
    raw = b'' if target is None or text is None else rom[target:rom.find(b'\xff', target) + 1]
    exact = bool(expected) and raw == TextEncoder.encode_pokemon(expected, skip_aliases=GERMAN_UMLAUT_CHARS)
    same_words = bool(expected and text) and ' '.join(expected.split()) == ' '.join(text.split())
    width = max(map(line_width, lines), default=0)
    fits = bool(lines) and len(lines) <= (5 if row['kind'] == 'move' else 4) and width <= (122 if row['kind'] == 'move' else 144)
    return {
        'kind': row['kind'], 'index': row['index'], 'owner': row['owner'],
        'pointer': hex(pointer), 'source_offset': hex(original),
        'target': hex(target) if target is not None else None,
        'text': text, 'hex': raw.hex(), 'expected': expected,
        'english': text == original_text, 'exact': exact, 'same_words': same_words,
        'line_count': len(lines), 'max_width': width, 'fits': fits,
        'ok': same_words and fits and text != original_text and not any(code in raw[:-1] for code in range(0xF7, 0xFE)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom', type=Path, default=ROOT / 'output/roms/GenedRom-de.gba')
    parser.add_argument('--source', type=Path, default=ROOT / 'input/roms/englishrom.gba')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source, rom = args.source.read_bytes(), args.rom.read_bytes()
    evidence = json.loads((ROOT / 'tests/unit/fixtures/de_move_parity_688.json').read_text())
    combined = load_combined(ROOT / 'languages/de/combined_de.txt')
    rows = [inspect_reference(rom, source, row, combined) for row in evidence['references']]
    result = {'rom_sha256': hashlib.sha256(rom).hexdigest(), 'references': rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    own = [row for row in rows if row['owner'] == 'B-688']
    print(f"Toutes références : {sum(row['ok'] for row in rows)}/{len(rows)} conformes")
    print(f"B-688 : {sum(row['ok'] for row in own)}/{len(own)} conformes ; "
          f"{sum(row['english'] for row in own)} encore EN")
    return int(not all(row['ok'] for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
