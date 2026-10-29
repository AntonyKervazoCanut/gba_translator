# PT-03 — terrain, pension, système, objets et classes

Le manifeste `languages/pt/translation_batches.json`, lot PT-03, définit exactement
277 offsets. F-758 et F-759 étaient terminés et intégrés avant les traductions.
Le domaine historique est hétérogène : mouvements de terrain, profils, pension,
Safari, mobilier, sauvegarde, aide initiale, descriptions d'objets, menus d'objets
et de Rotom, noms proposés au joueur et classes de Dresseurs.

## Bilan exhaustif

`languages/pt/data/pt03_audit.json` fournit une ligne par offset avec anglais,
comparaison française, octets EN, références directes, taille PT et largeur lorsque
une entrée PT est ajoutée. La source anglaise est identifiée par SHA256.
Les tests suivent les 236 références directes et les références indexées de classes.

| État | Nombre | Traitement |
|---|---:|---|
| traduit | 163 | Traduction PT-BR protégée et vérifiée dans la ROM finale |
| conservé/vérifié | 75 | Noms propres, noms d'objets anglais et noms complets trop longs pour une cellule, selon F-759 |
| exception justifiée | 39 | Données non textuelles, fragments sans référence ou indirections ; détail par offset dans le JSON |

177 valeurs PT sont ajoutées ou corrigées avec leur protection exacte. La seule
traduction préexistante corrigée est le seed `0x238d6a`, Voltar → Cancelar selon le
glossaire. Aucun offset des autres lots ni aucune traduction préexistante n'est
supprimé. Les noms de mouvements restent anglais (Strength, Rock Smash, Dive,
Waterfall). Les espèces, objets et noms propres sans traduction attestée restent
anglais. Poison emploie bien le type **Venenoso** du glossaire.

## Exceptions et lecture réelle

- 23 offsets de `0x1eaf1a` à `0x223a38` sont des fragments de tables de glyphes
  2bpp, protégées par `fixed_tables.py`. Aucun pointeur texte ne les vise.
- Neuf offsets sans référence directe : `0x1c27e6`, `0x1c5762`, `0x1c5792`,
  `0x1c579d`, `0x1c57c6`, `0x1c57cb`, `0x1c59f7`, `0x23700c`, `0x237503`.
  Ils restent intacts ; il ne s'agit pas de traductions injectées.
  `0x1c59f7` contient le résidu « you a girl? » après la question référencée
  `0x1c59d5` par `0x12fe34`. Le parent tient dans les 34 octets précédents.
- Sept offsets de classes interprètent à tort des octets de pointeur comme du
  texte. La table est adressée par index depuis `0x23e558`, via `0x0d80a0` et
  `0x11b4b4`. Les cibles vivantes sont vérifiées, sans édition hors manifeste :

| Offset PT-03 | Cellule/pointeur | Cible EN | Nom vivant conservé |
|---|---|---|---|
| 0x23e572 | 0x23e572 | 0x1f2cb7c | Light of Ruin Leader |
| 0x23e610 | 0x23e60e | 0x1fae6f4 | Terror Granbull |
| 0x23e678 | 0x23e676 | 0x1fa1ee4 | Black Ferrothorn |
| 0x23e6ac | 0x23e6aa | 0x1fa1ef5 | Black Ferrothorn Boss |
| 0x23e6e1 | 0x23e6de | 0x1f949ec | Frontier Brain |
| 0x23e6ec | 0x23e6eb | 0x1facb8d | Science Society |
| 0x23e763 | 0x23e760 | 0x1eea039 | Sinnoh Leader |

## Injection et budgets

Le patch PT `trainer_class_names` est déclaré dans `lang.yaml`. Il écrit les
24 classes effectivement traduites dans leurs cellules de 13 octets, sans toucher
aux cellules indirectes ou à celles d'autres lots. Il valide toutes les préimages
avant toute mutation, refuse les dépassements et les cibles inattendues, et est
idempotent. Les noms PT sont lus depuis le combined, jamais dupliqués dans le patch.
Les autres classes sont conservées entières, sans abréviation improvisée.

Les tests vérifient commandes FD/FC, paramètres, ordre, pages FA/FB, terminateur,
largeurs de dialogue (192 px), classes (80 px), descriptions d'objets (122 px,
trois lignes) et ligne vide de l'introduction. La sonde ROM accepte uniquement le
rewrap des espaces/sauts de ligne du constructeur ; les mots, paramètres et pages
restent contrôlés. Toutes les références d'une entrée sont vérifiées, pas une
simple recherche globale de la traduction dans le fichier ROM.

## Validation reproductible

```sh
make build-pt
python3 -m pytest -q tests/unit/pt tests/unit/test_translation_integrity.py tests/e2e/pt/test_built_batch_03_pt.py -m 'not emulator'
npx playwright test --config tests/e2e-playwright/playwright.pt03.config.ts
```

La preuve Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen`, une copie
éphémère de la ROM et une sauvegarde d'état existante. Le seul ajout temporaire
est un script déclenchant la chaîne livrée par le build, lue via son pointeur
`0x1bf549` : « Hã? » à l'offset source `0x1bfb5a`. Le test contrôle les octets,
le tilde de ã et l'absence de pixels parasites après le message et sur la ligne
suivante. Capture dans le répertoire temporaire de l'OS, jointe au ticket ; aucune
capture ni ROM ajoutée au dépôt. Aucune sauvegarde en jeu.

## Non vérifié

La sonde valide un vrai rendu de message ; elle ne certifie pas le parcours de
chaque écran de pension, sauvegarde, Safari, aide ou combat. La vérification
exhaustive de ces textes dans cette livraison est binaire et structurelle.
La certification complète du parcours reste à T-848. Aucun code partagé modifié.
Aucun push, publication ou pipeline distant lancé.
