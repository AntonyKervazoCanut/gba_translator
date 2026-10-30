# PT-61 — Crédits, Crystal Peak, Cube Corp. et Pension Pokémon

Le manifeste PT-61 est la seule liste de sélection : 300 offsets, de
`0x1ef09b5` à `0x1ef779a`. Prérequis F-758 et F-759 intégrés. Le lot comprend
268 traductions, 31 crédits/noms/cris conservés et une exception sans injection.
Aucun offset de traduction d'un autre lot n'est ajouté ou modifié.

## Sources et préservation

L'anglais de `combined_en.txt` est comparé au français au même offset et aux
chaînes complètes de la ROM anglaise. Les longues répliques de Cube Corp.
et de la mission quotidienne dépassent le texte tronqué du corpus EN : le
bilan conserve la préimage binaire complète et son décodage, ainsi que les
sources textuelles EN/FR. Les noms d'espèces, objets, mouvements et lieux sans
équivalent attesté restent anglais conformément au glossaire F-759.

`languages/pt/data/pt61_audit.json` fournit le bilan des 300 offsets : état,
justification, texte PT, octets source, nombre d'octets encodés, largeurs,
pointeurs et contexte binaire des références. Les 299 lignes ajoutées au
combined ont chacune leur protection exacte. Les crédits conservent leurs
noms, espaces et sauts de ligne à l'octet près. Le patch final réutilise les
primitives existantes sans changement de code partagé.

## Cas particuliers

- `0x1ef0c67` : clé qui commence dans un octet de bourrage. Les sept pointeurs
  vivants visent `0x1ef0c68`, dont `0x1fb477c` dans la table de carte. Le nom
  Crystal Peak est conservé ; le patch résout cette clé sans créer un offset
  de traduction supplémentaire et restaure le bourrage.
- `0x1ef5586` : réplique orpheline sans pointeur direct dans toute la ROM.
  Le refus vivant du script à `0x1e60fa2` utilise `0x1ef55f6`. Les occurrences
  numériques de pointeurs vers l'intérieur de la chaîne (`+7`, `+87`) à
  `0x1e107b3`, `0x1fbfdae` et `0x1fc0d1a` sont dans des données non-script,
  sans commande de dialogue. Aucune traduction n'est injectée et ces données
  ne sont pas repointées. Cette absence de consommateur identifié est une
  exception documentée, pas une traduction prétendument visible.

Les tables de crédits, titres, menus de pierres évolutives et sous-objectifs
sont des tables de pointeurs ; leurs cellules restent à leur place. Les textes
sont relogeables. La passe dédiée finale vérifie chaque consommateur après
les passes génériques, y compris les textes longs et les noms inchangés.

## Validation reproductible

- `python3 -m pytest -q tests/unit/pt/test_batch_pt61.py tests/unit/test_translation_integrity.py`
- `make build-pt`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt61_rom.py -m rom`
- `npx playwright test --config tests/e2e-playwright/playwright.pt61.config.ts`

Les tests contrôlent les préimages et pointeurs, les commandes FC/FD/FA/FB
exactes et ordonnées, les pages de dialogue, les budgets de 204 pixels
(dialogues) ou 172 pixels (missions), les cinq polices réelles, l'injection
finale, l'idempotence et les écritures strictement limitées aux pointeurs et
aux allocations. Les textes sans défilement gardent leur disposition dédiée.

La preuve Playwright utilise mGBA hors écran sur une copie temporaire de la ROM
construite. Deux vraies boîtes de dialogue sont appelées avec les pointeurs
finaux (totems de Crystal Peak et annonce de l'Ovo à la Pension). OCR portugais,
octets attendus et sauvegarde inchangée sont vérifiés. La capture est stockée
hors dépôt et jointe au ticket. Cette sonde ne prétend pas certifier le parcours
complet des missions ni toutes leurs branches en partie normale.

## Résultat local du lot

`make build-pt` réussit : 299 consommateurs vérifiés, 130 textes relogés par
la finalisation PT-61. Les tests ciblés d'intégrité, de métier et de ROM donnent
40 réussites. Playwright donne 1 réussite pour les deux scènes ; la sonde
initialise les tampons du compteur comme le script natif de la Pension avant
l'appel direct du dialogue. La sauvegarde temporaire est inchangée.

Le premier hook a détecté l'absence de l'artefact DE dans ce worktree neuf :
la recette historique `certify-de --dry-run` copie cet artefact malgré le mode
simulation. La copie locale de l'artefact existant permet de tester la recette ;
les builds FR/IT/DE du hook reconstruisent ensuite les vraies sorties locales.
Aucun correctif partagé ni contournement du hook n'est introduit.
