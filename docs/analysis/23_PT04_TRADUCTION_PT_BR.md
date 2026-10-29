# PT-04 — audit des 277 offsets

Le nom provisoire « Dialogue historique » ne décrit pas le contenu réel : ce lot
contient des classes de Dresseurs, des noms de types, des descriptions et noms de
Habilidades, des structures de Dresseurs, quelques dialogues de Borrius, des
messages de combat et des faux positifs graphiques.

Le manifeste `languages/pt/translation_batches.json`, entrée PT-04, détermine seul
le périmètre. Aucun autre offset du combined n’est modifié. Les traductions déjà
présentes restent intactes ; chaque ajout possède sa valeur exacte dans
`languages/pt/protected_entries.yaml`.

## Bilan exhaustif

`languages/pt/data/pt04_audit.json` contient **une ligne de bilan par offset**, avec
anglais et comparaison française, préimage binaire, occurrences de pointeurs,
références consommées, mode d’injection, tailles et justification des exceptions.
L’anglais a été traduit directement ; les paramètres bruts priment sur le décodage
historique qui transforme des arguments de contrôle en lettres.

- **98 traductions** : descriptions de Habilidades, types compatibles avec leur
  cellule, Incêndio/Dilúvio, dialogues et messages de combat.
- **155 noms conservés en anglais** : noms non répertoriés par F-759
  (`policy.unlisted`), noms propres de Dresseurs, ou termes canoniques trop longs
  pour une cellule fixe (`policy.cells`). Il ne s’agit pas de traductions injectées.
- **6 alias** : padding précédant une cellule déjà traitée ou conservée ; pas de
  chaîne autonome avec un pointeur propre.
- **18 exceptions** : préfixes de cellules contenant un pointeur, descriptions
  historiques non référencées par la table vivante, données binaires/graphiques.

Les noms canoniques Lutador, Venenoso, Terrestre, Fantasma, Elétrico, Psíquico et
Sombrio dépassent la cellule de sept octets terminateur compris. Ils restent
anglais conformément au glossaire ; aucune abréviation ou relocation partielle
qui casserait un lecteur indexé n’est revendiquée. Supercrescimento dépasse de
même la cellule historique de treize octets : OVERGROW est conservé. Une extension
des tables et de leurs lecteurs constitue un travail distinct.

## Références et cellules

- Classes : base `0x23e558`, stride 13, littéraux du moteur `0xd80a0` et
  `0x11b4b4`. Les extractions `0x23e7af` et `0x23e7bb` commencent dans des cellules
  à pointeur : champs à `0x23e7ae` et `0x23e7bb`, cibles `0x1f2cb68` et
  `0x1f2cb5a` hors PT-04. Réencoder ces octets comme du texte casserait les noms.
- Descriptions : table vivante `0x96de04`, 293 pointeurs. La table vanilla
  `0x24fb08` n’est pas une preuve de consommation. Chaque description traduite
  possède une référence dans la table vivante ; ces références sont contrôlées
  dans la ROM construite, et pas seulement dans le combined.
- Noms de Habilidades : ancienne table `0x24fc40`, stride 13, encore référencée
  par le littéral `0x8a123c`. Ne pas la déclarer morte sous prétexte que la table
  principale CFRU est à `0xa36398`, hors lot.
- Types : cellules de sept octets et références à leur début réel. L’extraction
  `0x24f20d` commence dans le padding précédent ; Dragão est écrit à `0x24f210`.
- `0x2779d4` et `0x2779f1` : messages consommés à `0x2779d5` et `0x2779f2`, via
  les scripts `0x3074b2` et `0x307535`. Les traductions restent dans leurs budgets
  d’origine et conservent le paramètre FD 00. Le préfixe extrait n’est pas affiché.

Le patch `languages/pt/patches/batch_04.py`, déclaré en dernière étape du build PT,
écrit les cellules bornées depuis les valeurs du combined. Il vérifie les
préimages de la ROM source et les capacités avant toute mutation, restaure les
préfixes de padding mal alignés, puis écrit toutes les cellules. Cette double
passe protège notamment Incêndio du préfixe de l’extraction suivante de Dilúvio.
Les tests contrôlent les octets hors périmètre et l’idempotence.

## Vérification reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_04_pt.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_built_batch_04_pt.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt04.config.ts
```

Les contrôles ROM portent sur chacun des 277 offsets : tous les pointeurs vivants
des traductions, cellules fixes complètes avec terminateur et padding, préimages
des noms conservés et des données exclues. Les textes du résumé Habilidade restent
sur une ligne de 192 pixels au plus ; les pages et paramètres sont conservés.

Playwright lance mGBA avec `QT_QPA_PLATFORM=offscreen`. La copie de ROM temporaire
ajoute seulement un script msgbox, qui lit le **texte livré** de `0x26d5bf` via
son pointeur vivant `0x26d3d9`. Le test vérifie ses octets, le rendu des glyphes
natifs et l’absence de débordement. La capture se trouve dans le dossier temporaire
de l’OS puis dans les pièces jointes du ticket ; aucun screenshot n’est versionné.
Ce contrôle de dialogue ne prétend pas certifier tous les écrans ni un parcours
complet en jeu ; cette certification relève de T-848.
