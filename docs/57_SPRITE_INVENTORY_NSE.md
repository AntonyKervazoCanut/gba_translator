# Unbound 2.1.1.1: known sprite inventory and indexed editing pilot

## Coverage and provenance

The checked-in [manifest](../languages/de/sprite_inventory.json) covers **all 18
families / 30 block instances in the current German registry**, not all graphics
in the ROM. It is generated directly from [the DE registry](../languages/de/sprites.py)
and its [shared definitions](../languages/fr/sprites.py). Unknown asset counts,
unknown palettes, undeclared pointer references and undeclared tilemaps remain
explicitly unknown. An empty pointer list does **not** prove that no pointers exist.
A missing tilemap means the tool exposes a linear tile window, not that the game
never uses a tilemap or runtime OBJ arrangement. Dimensions describe the editable
window, which may cover only part of a larger decompressed block.

The target is v2.1.1.1; filenames and the GBA header do not prove the release version.
The static manifest therefore says `rom_version_verified: false` and
`extractability: registered-unverified`. Pilot bundles record the exact source
SHA-256 and successful extraction separately. Do not apply these offsets blindly
to a different release or an independently patched ROM.

```sh
python3 scripts/sprite_inventory.py manifest > output/sprite_inventory.json
# Compare against the checked-in registry snapshot:
cmp output/sprite_inventory.json languages/de/sprite_inventory.json
```

All offsets are file offsets, not GBA bus addresses. A ROM pointer stores
`0x08000000 + offset` as a 32-bit little-endian value. `pointer_locations` identifies
where pointers are stored. Only declared pointers can be checked; dynamic code
references require separate reverse engineering.

Existing coverage includes Trainer Card front/back, title screen (8bpp), status
badges, type icons in summary/battle, summary and party KP, four battle KP copies,
raw KP elements, battle status badges, the level marker, PC box labels, Cube sort,
Mart signs, naming help and START-menu reorder help. The registry is not a
translation-status detector: registration does not mean every English pixel has
been translated. Other graphics generators such as world-map/DexNav patches,
fonts, Pokémon/overworld sprites, animations, runtime-composed UI and undiscovered
assets are outside this manifest. Extend it through reviewed registry entries,
not by calling an LZ77 signature scan a complete inventory.

## Three-asset pilot

The pilot processes six independently editable copies. They are **linear windows**,
so there is no registered tilemap to rewrite in this first stage.

| Asset | Offsets | Window | Encoding | Palette |
| --- | --- | --- | --- | --- |
| `battle_kp_labels` | `0x00D1F604`, `0x00EEF0AC`, `0x00EEF380`, `0x00EEF688` | 16×8, starting at tiles 19/20/19/19 | 4bpp LZ77 | display-only; ROM palette unknown |
| `type_icons_summary` | `0x00B1EC64` | 128×152 | raw 4bpp | display-only; ROM palette unknown |
| `summary_stat_labels` | `0x00E9A460` | 128×256 | 4bpp LZ77 | BGR555 at `0x00E9B310` |

Use Python 3.11+ from the repository root. Supply your own legally obtained ROM;
no ROM, extracted commercial graphic, or asset-bearing patch is supplied here.
Choose a fresh bundle directory and fresh output ROM on each run.

```sh
python3 scripts/sprite_inventory.py export \
  --rom input/roms/englishrom.gba \
  --directory output/sprite-workflow/2026-10-13_pilot --format bmp

# Before editing: proves export/readback preserves every pixel index and ROM byte.
python3 scripts/sprite_inventory.py verify \
  --rom input/roms/englishrom.gba \
  --directory output/sprite-workflow/2026-10-13_pilot

# Edit the six BMPs in place, retaining filenames and bundle.json.
# Insert checks every copy before writing a new ROM; no partial success.
python3 scripts/sprite_inventory.py insert \
  --rom input/roms/englishrom.gba \
  --directory output/sprite-workflow/2026-10-13_pilot \
  --out output/sprite-workflow/2026-10-13_edited.gba
```

PNG uses identical commands with `--format png`; do not change extensions within a
bundle. The output is accompanied by `.gba.bak` holding source bytes. The original
input is read-only. Export refuses existing directories; insertion refuses existing
outputs and requires them under `output/`. Keep bundles private: unlike the static
manifest, their images contain extracted artwork. `output/sprite-workflow/` is ignored
by Git. The CLI is [scripts/sprite_inventory.py](../scripts/sprite_inventory.py);
shared checks live in [SpriteInventory](../src/core/sprite_inventory.py).

To move beyond the default pilot without changing the safety model, add one or
more `--asset` flags. The asset must be registered and must not use a tilemap;
the command refuses mapped screens so they stay on the mapped workflow below.
Use small batches first, because every selected copy is verified as one bundle.

```sh
python3 scripts/sprite_inventory.py export \
  --rom input/roms/englishrom.gba \
  --directory output/sprite-workflow/2026-10-13_status --format bmp \
  --asset status_badges

python3 scripts/sprite_inventory.py verify \
  --rom input/roms/englishrom.gba \
  --directory output/sprite-workflow/2026-10-13_status \
  --asset status_badges
```

## NSE interchange contract

Use ordinary **indexed Windows BMP** (BITMAPINFOHEADER, uncompressed BI_RGB), or
non-interlaced **indexed PNG**, with exactly 16 RGB palette entries for 4bpp and
256 for 8bpp. Width/height stay multiples of eight. Keep the palette in its original
order, index zero in place, and each copy separate. Never convert to RGB, quantize,
sort/optimize the palette, dither or merge colours. Editing palette RGB values is
also rejected by the pilot: this workflow edits tile indices, not ROM palettes.
Transparency is not a new ROM colour; preserve the existing index semantics.

NSE 2.x source provides a bitmap importer with 16/256-colour paths and an
8-pixel dimension check: [Import.cs](https://github.com/TetradogOther/NSE/blob/master/Nameless%20Data%20Manipulation/IO/Import.cs).
This supports indexed BMP as a reasonable interchange candidate, **not a claim of
end-to-end certification with every NSE build**. NSE's GUI has not been exercised
in this ticket. Import a standalone image, export it unchanged, and run `verify`
before drawing anything. If that no-op fails, retain the originals and use an editor
that preserves indexed data. Record Misa's exact NSE version and successful no-op
result before declaring that version compatible. No `.nsl`/`.nslx` project or NSE
bookmark generator is provided. Do not use stock FireRed Pokémon bookmarks to
infer Unbound UI offsets, and do not let NSE repoint the ROM directly for this pilot.

Real ROM colours are embedded only where the registry supplies a palette address.
Otherwise colours are a display aid; matching how an export looks does not prove
its indices are correct. The guarded importer compares the entire ordered palette
against a fresh source-derived palette. The older `insert_sprite.py` reads pixel
indices but ignores image palette RGB, so it alone cannot detect palette reordering.

## Reinsertion and validation guarantees

The pilot checks the bundle source hash and registry fingerprint, all images, dimensions, ordered palette
and index range. It resolves/validates declared pointers using
[resolve_live_offset](../src/graphics/sprite_rom.py), rejects out-of-ROM locations,
and re-extracts every changed window for an exact index comparison. The pilot's
chosen assets currently have **no declared pointers**; this is limited pointer
coverage, not proof of pointer discovery.

For compressed edits the budget is the **original consumed LZ77 stream length**,
not adjacent zero/FF padding and not the full decompressed size. It recompresses
the complete payload while preserving tiles outside the edited window. Overflow
is a hard failure, even if a registry entry permits a larger physical slot. There
is no relocation or pointer rewriting in the pilot. Unchanged grids retain the
original compressed bytes, guaranteeing byte-identical no-op output even when
multiple valid LZ77 encodings exist. Each insert runs twice from the same source
and compares results, then writes only after both runs succeed.

The metadata-only local pilot result on 2026-10-13 used a 33,554,432-byte source with
SHA-256 `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`, matching
[the repository baseline](roms_baseline.json). Consumed budgets for the four KP
streams were 424/690/424/379 bytes; the type sheet was 9,728 raw bytes; the summary
stream was 3,084 bytes (16,384 decompressed). PNG and BMP no-op returned the same source
hash. These observations do not establish a universal v2.1.1.1 fingerprint.

Public tests generate geometric byte patterns at runtime, with no commercial
fixtures. They cover PNG/BMP no-op, successful raw/compressed edits, preservation
of neighbouring tiles, wrong ROM, dimensions, palette reorder, invalid pointer,
compressed overflow and refusal of mapped screens:

```sh
python3 -m pytest tests/unit/test_sprite_inventory.py -q
python3 -m pytest tests/unit/test_sprite_rom.py tests/unit/test_sprite_png.py \
  tests/unit/test_sprite_bmp.py tests/unit/test_insert_sprite_safety.py -q
make test-python-fast
```

## Mapped screens and expansion beyond the pilot

The existing [extract script](../scripts/extract_sprite.py) and
[insert script](../scripts/insert_sprite.py) support the larger registry, including
mapped Trainer Cards and the 8bpp title screen:

```sh
python3 scripts/extract_sprite.py --rom input/roms/englishrom.gba \
  --lang de --sprite trainer_card_front \
  -o output/sprite-workflow/trainer_card_front.png
```

For these assets, [sprite_rom.py](../src/graphics/sprite_rom.py) reconstructs screens
through compressed tilemaps, including shared tiles, horizontal/vertical flips
and 4bpp palette banks. Mapped insertion can split shared tiles, update indices and
relocate via declared pointers. A flattened screenshot is insufficient to preserve
that structure. Use [the mapped-sprite tests](../tests/unit/test_trainer_card_sprites.py)
and [title tests](../tests/unit/test_title_screen_sprite.py) as the starting point;
check all visible tilemap entries, bank/flip bits, surviving offscreen entries,
re-extracted pixels, pointer convergence and compressed capacities. The conservative
pilot deliberately rejects mapped assets. Existing broad insertion can warn/skip
individual copies while returning success for others: review every result, or add
an all-or-nothing contract before expanding this pilot.

Keep vram-safe compression enabled where the registry requires it. A stream that
decompresses in Python is not necessarily accepted by BIOS VRAM decompression.
After any real edited asset is adopted, check it in the relevant game screen and
all affected copies. No game artwork or rendered UI was changed by this feature.

## Build reproducibility and reuse

Pilot determinism is separate from a full translation build. Existing DE raster
integration is [battle_summary_sprites.py](../languages/de/patches/battle_summary_sprites.py),
with [screen](../languages/de/patches/screen_graphics.py) and
[menu](../languages/de/patches/menu_sprites.py) passes. These apply versioned indexed
assets late enough to avoid earlier generators overwriting them. An independent
DE project should explicitly choose which assets/passes to adopt rather than run
all translation patches over its custom build.

For the repository's complete build, fix the checkout, original ROM hashes,
translation inputs, generated translation metadata, Python/dependency versions and
build number. Reuse the existing [Makefile](../Makefile) target:

```sh
make verify-de-determinism   # builds DE twice with BUILD_NUMBER=0 and compares bytes
```

A successful pilot no-op is not a claim that a full DE rebuild or NSE GUI test was
performed. Do not publish private build outputs, and do not start remote workflows
for this check.

No repository-wide LICENSE granting reuse was found in this checkout. This ticket
does not assign a new license or grant rights on behalf of contributors. The linked
code and registry are the technical reuse candidates; obtain explicit applicable
terms from their owners before copying them into another project. Versioned art
can include commercial source pixels; credit alone is not a redistribution grant.
Keep original code/metadata, contributor-created art and extracted game data
separate when requesting terms. The synthetic test patterns contain no game art.
