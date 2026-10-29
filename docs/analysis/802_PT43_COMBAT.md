# 802 — PT-43 : combat, règles et participants

Le manifeste contient exactement 282 clés. Le bilan exhaustif, les comparaisons
EN/FR, préimages binaires, pointeurs, tailles encodées et largeurs sont dans
`languages/pt/data/pt43_audit.json` : 77 textes traduits, 203 noms conservés et
2 exceptions. Les deux prérequis F-758/F-759 sont intégrés. Aucun offset d'un autre
lot n'est ajouté au combined et aucune traduction antérieure n'est supprimée.

## Décisions

Les noms de participants, de formats Smogon et de mouvements sans attestation
restent anglais conformément au glossaire. Les effets sont ceux du CFRU Unbound :
le terrain brumeux renforce ici les mouvements Fada ; le champ négatif épargne
les types Sombrio/Fantasma/Psíquico et Unaware/Oblivious/Magic Guard. L'interdiction
Mega/Primal/Ultra/Z reste dans les deux pages du texte Dynamax.

Les séquences FD, FA et FB sont comparées aux octets EN, pas aux lettres parasites
du corpus (`Œ`, `;`, `=`). Les retours de ligne sont ajustés aux fenêtres sans
changer les sauts de page/défilement ni l'ordre des paramètres. Les textes de
combat réservent l'espace des noms dynamiques ; les lignes statiques sont limitées
à 204 pixels. Les tailles incluent le terminateur FF. Il n'y a aucune écriture
allongée dans une cellule anglaise : le patch final réutilise le repointage
atomique existant, avec vérification de préimage et de tous les consommateurs.
Les tables restent en place ; seules leurs cibles texte peuvent être relocalisées.

## Clés particulières

- `0xa43d8e` : « Cube », sans pointeur absolu dans la ROM canonique. Aucun
  consommateur identifié, aucune injection et aucune revendication de texte
  visible traduit. Le mot est identique en portugais.
- `0xa43d93` : clé sur l'espace de remplissage avant Spikes. Aucun pointeur ;
  `0xa6b9e0` pointe à `0xa43d94`, autre clé explicite de PT-43, traduite et vérifiée.
- `0xa43fbb` : remplissage avant Single Battle Record ; `0xa6b87c` vise
  `0xa43fbc`. Le combined utilise exclusivement la clé du manifeste ; le patch
  résout le décalage prouvé et livre « Recorde Individual » au consommateur.
- `0xa44c9f` : remplissage avant Liam ; `0xa76484` vise `0xa44ca0`.
  Le prénom et ses octets sont conservés, sans écrire sur le remplissage.
- `0xa45000` : Lillian est référencé par la table de prénoms à `0xa7635c`.
  La coïncidence binaire non alignée `0x16d31ed`, hors table de noms, n'est pas
  utilisée comme consommateur et n'est pas repointée.

Bases des tables vérifiées : formats `0xa6b6e8` (littéraux `0x9e6b18`,
`0x9e6db4`), modes `0xa6b768`, terrains `0xa6b7a0`, records `0xa6b870`
(littéral `0x9e97b8`), prénoms `0xa762f4` et `0xa76484`.

## Vérification reproductible

```sh
make build-pt
python3 -m pytest tests/unit/pt/test_batch_pt43.py tests/unit/test_translation_integrity.py -q
python3 -m pytest tests/e2e/pt/test_batch_pt43_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt43.config.ts
```

Le test Playwright démarre mGBA hors écran sur une copie temporaire de la ROM
construite. Une sonde appelle les vraies chaînes par leurs pointeurs, sans changer
leurs octets ni leurs glyphes ; elle vérifie par OCR le message DexNav et la page
sur les effets du terrain électrique. Ce n'est pas un parcours manuel des menus
compétitifs ni une partie multijoueur. Les 282 décisions sont couvertes par les
contrôles binaires et de source, pas par 282 captures de gameplay.
La capture finale reste dans le répertoire temporaire du système et est jointe
au ticket ; aucune image de preuve n'est versionnée.
