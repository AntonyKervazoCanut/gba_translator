# Boîte CT : sigle CS (#189)

Le sigle orange « HM » est un bitmap brut 4 bpp à `0x00E99118`, référencé par
le pointeur `0x001335DC`. Ses quatre tuiles occupent 128 octets (16 × 16 pixels),
mais `PlaceHMTileInWindow` ne dessine que les 12 premières lignes.
La ressource correspond à `gTMCaseHM_Gfx` du
[moteur FireRed](https://github.com/pret/pokefirered/blob/master/src/tm_case.c).

`languages/fr/sprites/tm_case_cs.png` remplace les lettres par « CS » en gardant
le fond, les coins transparents et les quatre lignes de remplissage. Les indices
0, 6 et 7 sont conservés ; la palette PNG représente les couleurs observées en jeu.
Le registre FR expose `tm_case_cs`. Le build FR le réinsère après les réparations
graphiques avec l'outil existant, qui sauvegarde la ROM avant écriture.

## Extraction et réinsertion

```sh
python3 scripts/extract_sprite.py --rom output/roms/GenedRom-fr.gba \
  --lang fr --sprite tm_case_cs -o output/tm_case_cs.png
python3 scripts/insert_sprite.py --rom output/roms/GenedRom-fr.gba \
  --lang fr --sprite tm_case_cs --image languages/fr/sprites/tm_case_cs.png
```

Conserver le PNG indexé, ses dimensions et ses indices de palette lors d'une
édition. L'extraction générique utilise sa palette d'aperçu si aucune palette ROM
n'est déclarée ; les indices restent identiques.

## Vérification

```sh
python3 -m pytest tests/unit/test_tm_case_cs_sprite.py -q
ROM_PATH="$PWD/output/roms/GenedRom-fr.gba" \
  npx playwright test -c tests/e2e-playwright/playwright.tm-case.config.ts
```

Le test Playwright lance mGBA compatible `--script` en `QT_QPA_PLATFORM=offscreen`
(`MGBA_PATH` permet de choisir le binaire). Il utilise la sauvegarde
`party_hp_bar_fr.sav` dans un répertoire temporaire. Comme celle-ci n'a aucune CS,
la copie temporaire de la ROM remplace la fiche CT56 par la fiche CS01 existante.
La ROM construite et la sauvegarde source ne sont pas modifiées.

Le moteur affiche alors « CS No1 Coupe ». Les pixels des deux lettres sont
vérifiés avant et après navigation vers CT86, et le changement d'écran est
contrôlé. Un second test remet le bitmap HM original et vérifie qu'il ne satisfait
pas l'oracle CS. La capture finale agrandie est écrite dans le dossier temporaire
système (`TM_CASE_PROOF` permet de choisir le chemin), jamais dans le dépôt.
