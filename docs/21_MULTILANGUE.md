# Multi-language builds (FR / IT / DE …)

Pokémon Unbound can now be translated into several languages from the same
toolkit. The pipeline is split into a **shared, language-agnostic core** and a
small amount of **per-language data**. Duplication is kept to the minimum
strictly required by each language.

> **French is the reference and stays byte-perfect.** It keeps its dedicated,
> hand-tuned recipe (`make build-fr`) and is *never* rerouted through the
> generic driver. Adding Italian or German cannot change a single byte of the
> French ROM.

## The `languages/` registry

Every target language is declared by one descriptor:

```
languages/
  fr/lang.yaml                 # French — build: dedicated (combined_fr.txt at repo root)
  it/lang.yaml                 # Italian — build: generic
  it/combined_it.txt           #   translations  <offset_hex>: <text>
  de/lang.yaml                 # German — build: generic
  de/combined_de.txt
  indie/lang.yaml              # Indie — build: generic (reuses the FR font)
  indie/combined_indie.txt
  es-maint/lang.yaml           # Maintained Spanish — generic, in_progress
  es-maint/combined_es-maint.txt # Verified entries only; initially empty
```

`lang.yaml` is the single source of truth read by the Makefile, the build
driver and the test-suite. Key fields:

| field             | meaning                                                              |
|-------------------|---------------------------------------------------------------------|
| `code`            | short code, must equal the folder name (`fr`, `it`, `de`)           |
| `name` / `native_name` | display names                                                  |
| `builder_language`| value passed to the generic ROM builder `--language`               |
| `status`          | `complete` or `in_progress`                                         |
| `build`           | `dedicated` (FR) or `generic` (everything else)                    |
| `combined`        | path to the `combined_<code>.txt` translation file                 |
| `critical`        | optional always-win override file                                  |
| `output_rom`      | `GenedRom-<code>.gba`                                               |
| `version_label`   | shown on the NOT-FOR-SALE screen                                   |
| `font_glyphs`     | accented glyphs the language needs                                 |
| `status_abbrev`   | in-game status abbreviations (poison/burn/freeze/paralysis/sleep/faint) |
| `patches`         | ordered post-build patch steps                                    |

Load it from Python with:

```python
from src.i18n import load_registry
registry = load_registry()
cfg = registry.get("it")
```

## Building

```bash
make langs           # list registered languages
make build-fr        # French — dedicated, byte-perfect recipe (unchanged)
make build-it        # Italian — generic driver
make build-de        # German — generic driver
make build-indie     # Indie — generic driver (reuses the FR font)
make build-lang LANG_CODE=it   # any generic language
make build-es-maint  # Maintained Spanish, incremental from clean English
make build-all       # FR + IT + DE + Indie + PT-BR + es-maint
make release-all     # build every registered language + package output/release/
```

`release-all` writes one verified `.bps` per language plus global
`SHA256SUMS.txt` and `RELEASE_MANIFEST.json` to `output/release/`. BPS is used
instead of IPS because Unbound is 32 MB and translated data lives above
`0xFFFFFF`, beyond the 24-bit IPS offset field. The full ROM remains a local,
temporary build output and is never a release asset.

## The generic pipeline (`scripts/build_language.py`)

For a `build: generic` language the driver runs:

1. ensure EN/ES pointer extractions exist;
2. `combined_<code>.txt` → trilingual CSV (`apply_combined_fr.py`, which is
   language-agnostic) → translation-ready JSON
   (`output/translation/<code>_translation_ready.json`);
3. generic ROM builder (`19_build_translated_rom_generic.py`,
   `--allow-relocate --allow-fallback`);
4. the post-build patch steps from the descriptor (`font`, `inline`, …).

Offsets absent from `combined_<code>.txt` keep their English text, so a
partially-translated language still produces a bootable ROM.

## Adding a new language

1. `mkdir languages/<code>` and write `languages/<code>/lang.yaml`
   (copy `languages/it/lang.yaml` as a template).
2. Create `languages/<code>/combined_<code>.txt` and start translating, using
   the same `<offset_hex>: <text>` format as `combined_fr.txt`
   (`\n` line break, `\l` = `<0xFA>` scroll, `\p` = `<0xFB>` clear).
3. `make build-<code>` (after adding a `build-<code>` alias, or
   `make build-lang LANG_CODE=<code>`).
4. `python3 -m pytest tests/test_language_registry.py` to validate the
   descriptor.

### Charmap / font caveats

* The shared CFRU charmap already encodes the French and Italian accented
  vowels (`à è é ì í î ò ó ù ú`, `ç`, `ß`, …).
* German uses `ä ö ü Ä Ö Ü` at F1–F6 with its dedicated font patch and
  alias-preservation profile. Maintained Spanish preserves ü/Ü and ¡/¿ with
  its own explicit profile; default French/Italian alias behaviour is unchanged.
* Italian reuses the French font glyphs, so its `font` step is enabled.
* Indie also reuses the French font (no `patch_font_indie.py`), so the `font`
  step falls back to `patch_font_fr.py` and the full FR accented set renders.
  It seeds with a near-empty `combined_indie.txt`, so an untranslated offset
  stays English and the build is bootable from day one.

## What stays per-language (necessary duplication)

* `combined_<code>.txt` — the translated strings (irreducibly per-language).
* `lang.yaml` — a few lines of metadata.
* Status abbreviations / font glyph set — small data in the descriptor.

Everything else — extraction, diffing, the ROM builder, the CSV/JSON chain, the
font patch, inline overrides — is shared code.

## Espagnol maintenu (F-850)

`make build-es-maint` construit la cible générique incrémentale **in_progress**
`GenedRom-es-maint.gba` depuis l'anglais propre. `build-all` et `release-all`
l'incluent automatiquement ; le manifeste conserve son statut in_progress.
`make build-es`, la référence communautaire `es` et la recette FR restent inchangés.

Le combined et le manifeste de protection es-maint sont créés **vides**, conformément
à A-663/F-850 ; aucun texte communautaire n'est importé automatiquement. Les futurs
lots n'ajoutent que des textes vérifiés et leurs valeurs exactes protégées, dans le
même commit. Un fichier vide exige l'option explicite `--allow-empty-translations`
dans les deux étapes du driver générique ; le moteur historique garde son refus
par défaut, afin de détecter une entrée accidentellement absente.

Le profil ES est activé explicitement par `--preserve-spanish-glyphs` dans le builder
et l'étape inline. Il conserve ü/Ü (F6/F3), ¡/¿ (52/51) et tous les accents espagnols.
Les alias par défaut FR/IT et le builder ES historique ne changent pas. Les slots
inversés suivent la [charmap FireRed](https://github.com/pret/pokefirered/blob/master/charmap.txt).
Les copies TypeScript connaissent désormais ces deux ponctuations.

Les réparations mécaniques restent actives ; le patch de police suit les deux
réparations LZ77 et ne complète que Ü/ü dans les six blocs latins compressés
référencés. Il préserve les glyphes natifs des cinq polices moteur. Les badges
ENV/QUE/CON/PAR/DOR/DEB sont redessinés dans les quatre blocs graphiques, après
les réparations, selon le glossaire D-849. Aucun patch de traduction FR n'est repris.

Validation visuelle reproductible, entièrement hors écran, sans sauvegarde :

```sh
make build-es-maint
python3 -m pytest tests/e2e/es/test_maintained_infrastructure.py -m rom
npx playwright test --config tests/e2e-playwright/es-maint.config.ts
```

La sonde compile une petite sonde Thumb temporaire avec Clang, démarre une copie de la
ROM dans mGBA offscreen, puis appelle les cinq fonctions de décompression de glyphes
**du moteur original**, sans remplacer leurs données. Elle dessine leurs buffers
4bpp dans une mire GBA, ainsi que les quatre jeux de badges décompressés par le BIOS.
Playwright compare les pixels aux données 2bpp natives indépendamment de l'encodeur,
et contrôle les motifs des six badges. La capture reste dans le dossier temporaire
de l'OS ; ce n'est pas une capture d'un écran de gameplay ni une certification de la
traduction complète. Le boot réel est capturé avant d'installer la sonde en RAM.
