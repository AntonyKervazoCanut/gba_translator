# PT-34 — Descriptions obsolètes de mouvements et de Habilités

## Résultat

Les **288 offsets du manifeste sont des exceptions documentées**, pas des
traductions livrées. Le domaine réel est celui des descriptions de mouvements et
de Habilités, et non des zones de Borrius. Aucun texte PT, manifeste de protection,
patch, registre, code partagé ou offset d'un autre lot n'est modifié.

F-758 (`c5b5e0b9`) et F-759 (`dcc6ce5d`) sont intégrés dans l'ascendance du
worktree. La politique du glossaire ne justifie pas de traduire des copies mortes.

Le bilan exhaustif est [pt34_audit.json](../../languages/pt/data/pt34_audit.json) :
une ligne logique par offset, dans l'ordre exact du manifeste, avec anglais,
comparaison française, préimage ROM, toutes les occurrences de pointeur absolu,
classification et justification. Aucun offset n'est déduit de la seule plage.

| Classe | Entrées | Décision |
| --- | ---: | --- |
| Anciennes descriptions de mouvements | 133 | Copies de la table abandonnée ; une chaîne sans référence |
| Préfixes nuls de descriptions anciennes | 101 | Offsets sans pointeur, texte réel à `offset + 1` |
| Anciennes descriptions de Habilités | 54 | Aucun pointeur, aucune cellule de la table active |
| Traductions ajoutées | 0 | Aucune entrée vivante PT-34 à injecter |

## Preuve des consommateurs

L'ancienne table commence à `0x903ffc` (entrée zéro `ffffffff`) ; les 664
cellules suivantes finissent avant `0x904a60`. Elle conserve des pointeurs vers
132 descriptions PT-34, mais **n'est plus utilisée par les lecteurs actuels**.
Un scan à chaque octet de toute la ROM ne trouve qu'un motif visant son intérieur :
`0xc48659 → 0x904455`. Il vise le milieu d'une cellule et appartient au flux
compressé LZ77 `0xc476f0` (7 814 octets compressés, 12 224 décompressés).
Il ne constitue pas un consommateur de la table.

Les trois lecteurs de descriptions chargent au contraire `0x0899f194` :

| Instruction Thumb LDR | Littéral ROM | Calcul de cellule |
| --- | --- | --- |
| `0x0e541a` | `0x0e5440` | `0x99f194 + (id - 1) * 4` |
| `0x137b7a` | `0x137bc8` | `0x99f194 + (id - 1) * 4` |
| `0x9f3b4c` | `0x9f3b64` | `0x99f194 + (id - 1) * 4` |

Leurs instructions et littéraux sont figés dans l'audit et testés. La table
actuelle est donc `0x99f190`, indexée par ID, comme dans `src/core/moves.py`.
Les cibles actuelles des IDs de l'ancienne table appartiennent à **PT-37 et
PT-38** ; l'audit indique chaque ID, cellule, cible et lot propriétaire. Elles
ne sont pas traduites depuis PT-34. Certaines descriptions ont changé de sens
ou de formulation depuis les anciennes copies : aucune copie automatique n'est faite.

Exemple : `0x920285` (Air Slash) est référencé par l'ancienne cellule `0x90458c`.
La cellule active de l'ID 356 est `0x99f720`, cible `0xa37f07` (PT-37).
`0x921f70` n'a aucun pointeur, même dans l'ancienne table.
`0x920a3f` est un préfixe nul : `0x904638` vise `0x920a40`, hors PT-34.

Deux autres motifs vers les anciennes descriptions ne sont pas du texte :

- `0x1e7b79 → 0x920932` traverse trois instructions Thumb (`01 32`, `09 92`,
  `08 70` : addition, stockage sur pile, stockage d'un octet).
- `0xa97f5d → 0x9208ac` appartient au flux LZ77 `0xa96fe0`
  (6 488 octets compressés, 7 200 décompressés).

Les 54 descriptions de Habilités, `0x9229a9` à `0x922fa4` selon la liste du
manifeste, n'ont aucune occurrence de pointeur absolu dans la ROM entière.
Les 293 cellules de la table active `0x96de04` ne pointent sur aucune d'elles.
Les références à cette table en `0x1c4`, `0x1367a8` et `0x9a945c` sont vérifiées,
ainsi que les tests préexistants de découverte et d'alignement des Habilités.

## Validation reproductible

```sh
make build-pt
python3 -m pytest tests/unit/pt/test_batch_pt34.py \
  tests/e2e/pt/test_batch_pt34_rom.py \
  tests/unit/en/test_ability_description_table.py \
  tests/unit/test_translation_integrity.py -q
python3 -m ruff check tests/unit/pt/test_batch_pt34.py \
  tests/e2e/pt/test_batch_pt34_rom.py
```

Résultat initial : build réussi, **44 tests réussis**, lint réussi.
Les tests ROM vérifient les 288 préimages, toutes les occurrences absolues,
les flux LZ77, les littéraux des lecteurs et les tables sur la ROM source **et
sur la ROM PT construite**. Aucune cellule active ne vise les chaînes du lot,
y compris leur intérieur, et les copies anciennes sont identiques après build.
Les tests unitaires imposent le périmètre exact et empêchent de présenter ces
exceptions comme des traductions ajoutées.

## Non vérifié / non applicable

Aucune traduction injectée : les budgets PT en octets/pixels, protections de
nouvelles lignes, correctifs de tables fixes et preuve Playwright d'un rendu
modifié ne s'appliquent pas. Aucune modification de rendu ni capture visuelle
n'est revendiquée. La traduction des consommateurs actifs reste dans leurs lots
respectifs ; la certification générale reste à T-848.

L'analyse prouve les consommateurs directs et les tables du moteur de la ROM
source identifiée par SHA-256 dans l'audit ; elle ne prétend pas prouver
l'inaccessibilité pour toute autre révision de ROM ou tout script futur.
