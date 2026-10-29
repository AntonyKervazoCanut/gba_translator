# PT-35 — Types et messages de combat (F-794)

Les prérequis F-758 et F-759 sont intégrés. Le domaine réel ne correspond pas
au titre provisoire « Zones Borrius » : copies anciennes de talents et objets,
table de types, aides de matchups et messages de combat CFRU.

Le manifeste explicite de 288 offsets est la seule frontière de ce travail.
Le bilan complet, préimages EN, comparaison FR, références source et valeurs PT
se trouvent dans `languages/pt/data/pt35_audit.json`. La table ci-dessous donne
la décision de chaque offset ; les exceptions ne sont pas comptées comme traduites.

## Livraison

162 textes traduits, 1 nom inchangé, 125 exceptions documentées.

Le finaliseur `batch_35` utilise le mécanisme partagé de relocalisation atomique.
Il livre 154 textes pointés sans reformatage des commandes FD, F9, FE, FA et FB.
Les neuf cellules de types sont écrites à leur véritable début, dans la table
indexée de 24 cellules de sept octets (base 0x961b50, références 0x309c8 et
0x456e74). Les clés décalées dans le bourrage ne sont jamais traitées comme
le début d'une nouvelle chaîne. Le script de 0x75cd82 lit aussi la cellule Rock
à 0x961b73 : ce pointeur reste sur la cellule traduite Pedra.

Huit clés de types ne peuvent contenir le nom canonique entier : Lutador,
Venenoso, Terrestre, Fantasma, Elétrico, Psíquico, Sombrio (Lutador a deux cellules).
Conformément à F-759, ces cellules EN sont conservées sans abréviation improvisée.
La table graphique des types et les cases Bug/Ice absentes du lot ne sont pas modifiées.
Les aides de matchups utilisent les noms PT entiers, avec les mêmes pages et icônes.

Les descriptions historiques 0x922fc6–0x9513d0 ne sont plus référencées :
les descriptions courantes résident derrière 0x96de04 (talents) et les cellules
gItems (objets). Les noms de talents courants appartiennent à 0xa36398, pas
au bloc historique 0x92fb74. Les cibles de remplacement sont consignées sans
les modifier car elles appartiennent à d'autres lots. Certaines descriptions
ont aussi changé de sens entre versions (Friend Guard, Rivalry) ; pas de
traduction d'une copie ancienne dans le consommateur courant. Le fragment
0x950cfa commence après deux FF et n'a aucun pointeur.

Les motifs de 0x95f9f4–0x95fecb et 0x962f43 sont des pixels ; les FD y sont
des octets de motif, pas des tampons à traduire. Les cinq messages de combat
non référencés sont également exclus ; les copies identiques vivantes sont
indiquées lorsqu'elles existent. Une recherche de pointeur négative porte
sur les 32 Mio complets de la source, pas seulement le voisinage.

## Validation reproductible

- `make build-pt` : construction complète réussie ; 154 textes pointés et neuf
  cellules fixes vérifiés par le finaliseur.
- `python3 -m pytest tests/unit/pt/test_batch_pt35.py
  tests/e2e/pt/test_batch_pt35_rom.py tests/unit/test_translation_integrity.py -q` :
  36 tests réussis. Ils couvrent les 288 préimages/décisions, chaque référence,
  les valeurs protégées, les exceptions, les bornes d'écriture, l'atomicité,
  l'idempotence et les cinq vraies polices avec des tampons longs.
- Les budgets sont de 208 pixels pour les messages et 224 pour l'aide plein
  écran. Les cellules de types ont sept octets et au plus 42 pixels. Les octets
  encodés et largeurs de chaque entrée sont consignés dans l'audit.
- `npx playwright test --config tests/e2e-playwright/playwright.pt35.config.ts` :
  un test réussi, mGBA offscreen et Chromium headless. Les octets sont lus aux
  pointeurs de la ROM finale, puis le moteur affiche la cellule Pedra et le
  message de dissipation du soleil. L'OCR exact passe à l'échelle six ; à
  l'échelle quatre, Vision confondait le « a » de solar avec un « o ».
  La capture temporaire est jointe au ticket, jamais au dépôt.

## Non vérifié

La preuve visuelle utilise des sondes msgbox natives sur une copie temporaire
de la ROM. Elle ne constitue pas un parcours de tous les effets de combat,
ni une capture du menu d'aide entier. Aucun texte, glyphe ou tampon de combat
n'est substitué par cette sonde. Les pages restantes, les icônes et les tampons
des 154 textes sont contrôlés en binaire et par leurs budgets de rendu.

## Bilan par offset

| Offset | Décision | Références / cellule / exception |
|---|---|---|
| `0x922fc6` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x922fe8` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923004` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923019` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923038` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92304f` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923063` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923080` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923098` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9230b5` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9230d2` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9230eb` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92310b` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923129` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923147` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92315a` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92316e` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x923180` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9231a2` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9231c2` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fb74` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fb7e` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fb8f` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fb9f` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fbad` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fbbc` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fbca` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fbd9` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fbea` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fbf8` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc06` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc14` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc22` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc30` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc4c` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc67` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fc8a` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fcaf` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x92fcd5` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950a60` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950a80` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950aa0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ac0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ae0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950b00` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950b20` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950b40` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950b60` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950b80` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ba0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950bc0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950be0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950c00` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950c20` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950c40` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950c60` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950c81` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950c9a` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950cb7` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950cda` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950cfa` | exception | Fragment « oves. » isolé entre deux terminateurs FF à 0x950cf8/0x950cf9 ; aucun pointeur. Les vrais messages voisins commencent à 0x950cda et 0x950d00, également historiques. |
| `0x950d00` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950d20` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950d40` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950d60` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950d7c` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950da0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950dbf` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950de0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950e00` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950e20` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950e40` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950e60` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950e80` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ea0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ec0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ee0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950f00` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950f20` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950f90` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x950ff0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951050` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9510c0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9510e0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951100` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951120` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951140` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951160` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9511d0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x95122f` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951250` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951270` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951290` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9512f0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951310` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951330` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x951345` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9513b0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x9513d0` | exception | Copie historique sans référence directe ; la table vivante utilise un autre offset, hors PT-35. Aucune écriture sur cette copie morte. |
| `0x95f9f4` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fa2b` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fa30` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fa4b` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fc34` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fc6b` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fc70` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fc8b` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fe74` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95feab` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95feb0` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x95fecb` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x961b50` | retained | cellule 0x961b50 ; 0x309c8 ; 0x456e74 |
| `0x961b57` | exception | cellule 0x961b57 ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961b5d` | translated | cellule 0x961b5e ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x961b65` | exception | cellule 0x961b65 ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961b6c` | exception | cellule 0x961b6c ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961b73` | translated | cellule 0x961b73 ; 0x75cd82 |
| `0x961b7e` | exception | cellule 0x961b81 ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961b87` | translated | cellule 0x961b88 ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x961b93` | translated | cellule 0x961b96 ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x961b9b` | translated | cellule 0x961b9d ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x961ba3` | translated | cellule 0x961ba4 ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x961baa` | exception | cellule 0x961bab ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961bb2` | exception | cellule 0x961bb2 ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961bbd` | translated | cellule 0x961bc0 ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x961bc7` | exception | cellule 0x961bc7 ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961bcc` | exception | cellule 0x961bce ; Exception de rendu F-759 : nom canonique PT-BR supérieur à six octets ; cellule EN conservée sans abréviation inventée. Table indexée 0x961b50, pointeurs 0x309c8/0x456e74. |
| `0x961bf1` | translated | cellule 0x961bf1 ; Cellule indexée de sept octets : nom canonique entier, écrit par le patch dédié ; préfixe de bourrage préservé. |
| `0x962f43` | exception | Motif de tuiles/pixels, pas une chaîne : répétitions DD/EE/FD, aucun pointeur texte, fragments identiques dans trois blocs graphiques. Ne pas injecter. |
| `0x964160` | translated | 0x964090 |
| `0x964180` | translated | 0x964094 |
| `0x9641a0` | translated | 0x9640a4 |
| `0x964210` | translated | 0x9640b8 |
| `0x9642a0` | translated | 0x9640bc |
| `0x964300` | translated | 0x9640e8 |
| `0x964370` | translated | 0x9640ec |
| `0x9643e0` | translated | 0x964120 |
| `0x964460` | translated | 0x964100 |
| `0x9644c0` | translated | 0x964114 |
| `0x964540` | translated | 0x9640f0 |
| `0x964590` | translated | 0x9640f4 |
| `0x964600` | translated | 0x964128 |
| `0x964660` | translated | 0x96412c |
| `0x964a7e` | translated | 0x964a30 |
| `0x965b87` | translated | 0x96506f |
| `0x965b94` | translated | 0x965138 |
| `0x965ba5` | translated | 0x965159 |
| `0x965bba` | translated | 0x96517e |
| `0x965bcb` | translated | 0x965361 ; 0x969368 ; 0x96d30f |
| `0x965be8` | translated | 0x965446 |
| `0x965c16` | translated | 0x9654fc ; 0x96552f |
| `0x965c2e` | translated | 0x965591 |
| `0x965c46` | translated | 0x9655ee |
| `0x965c69` | translated | 0x965620 |
| `0x965c9a` | exception | Ancien message de combat non référencé ; aucune référence directe dans les 32 Mio de la source, aucun consommateur de table indexée de texte dans ce bloc de scripts. |
| `0x966083` | translated | 0x965dc4 |
| `0x9660a7` | translated | 0x965dde |
| `0x9660cd` | translated | 0x965df8 |
| `0x9660fd` | translated | 0x965e37 |
| `0x966135` | translated | 0x965e23 |
| `0x966169` | translated | 0x965e56 ; 0x9fd114 |
| `0x966193` | translated | 0x965e81 |
| `0x9661c9` | translated | 0x965eb3 |
| `0x9661ed` | translated | 0x965ed9 |
| `0x966212` | translated | 0x965ef3 ; 0x965f20 |
| `0x966239` | translated | 0x965f0b ; 0x965f33 |
| `0x96625d` | translated | 0x965f68 |
| `0x966275` | translated | 0x965f94 |
| `0x9665b0` | translated | 0x9662e1 ; 0x966319 ; 0x966377 |
| `0x9665ca` | translated | 0x9663e3 |
| `0x966601` | translated | 0x9663f3 |
| `0x966632` | translated | 0x966407 |
| `0x966650` | translated | 0x96641b |
| `0x966674` | translated | 0x96642f |
| `0x96668e` | translated | 0x9664f7 |
| `0x9666ae` | translated | 0x966514 |
| `0x966b45` | translated | 0x96671e |
| `0x966b67` | translated | 0x9668b5 |
| `0x966b8c` | translated | 0x966922 |
| `0x966bb6` | translated | 0x96693c ; 0x967223 |
| `0x966bd7` | translated | 0x966739 ; 0x9668cf |
| `0x966bfe` | translated | 0x96697b |
| `0x966c1a` | translated | 0x966995 ; 0x967238 |
| `0x966c33` | exception | Ancien message de combat non référencé ; aucune référence directe dans les 32 Mio de la source, aucun consommateur de table indexée de texte dans ce bloc de scripts. |
| `0x966c4d` | exception | Ancien message de combat non référencé ; aucune référence directe dans les 32 Mio de la source, aucun consommateur de table indexée de texte dans ce bloc de scripts. |
| `0x966c61` | translated | 0x9667f2 |
| `0x966c8b` | translated | 0x966824 |
| `0x966ca3` | translated | 0x966a4a |
| `0x967539` | translated | 0x966f9b |
| `0x96754c` | translated | 0x966fe5 |
| `0x967575` | translated | 0x967009 |
| `0x967599` | translated | 0x967105 |
| `0x9675b9` | translated | 0x96711b |
| `0x9675dc` | translated | 0x96712b |
| `0x9675f6` | translated | 0x96713b |
| `0x96760a` | translated | 0x967191 ; 0x9b7558 |
| `0x967635` | translated | 0x96719f |
| `0x967655` | translated | 0x9671ad |
| `0x967673` | translated | 0x9671bb ; 0x9b756c |
| `0x9676c0` | translated | 0x9671c9 ; 0x9b7574 |
| `0x967701` | translated | 0x9671d7 ; 0x9b7554 |
| `0x96771d` | translated | 0x967205 ; 0x9fc65c ; 0xa0a528 |
| `0x96773d` | exception | Ancien message de combat non référencé ; aucune référence directe dans les 32 Mio de la source, aucun consommateur de table indexée de texte dans ce bloc de scripts. |
| `0x967750` | translated | 0x96724b |
| `0x967770` | translated | 0x967271 |
| `0x967797` | translated | 0x9672e1 |
| `0x9677aa` | translated | 0x967308 |
| `0x9677bf` | translated | 0x964fa7 ; 0x967335 ; 0x967362 ; 0x96b6e2 ; 0x96ceca |
| `0x9678f0` | translated | 0x967837 |
| `0x96be0c` | translated | 0x96806e |
| `0x96be2f` | translated | 0x96818b ; 0x968271 ; 0x9682c9 ; 0x968333 |
| `0x96be4f` | translated | 0x968608 |
| `0x96be61` | translated | 0x968973 |
| `0x96be88` | translated | 0x968983 |
| `0x96beab` | translated | 0x968993 |
| `0x96bec2` | translated | 0x968d15 |
| `0x96bedd` | translated | 0x9693e5 |
| `0x96bef3` | translated | 0x969506 |
| `0x96bf07` | translated | 0x96973e |
| `0x96bf2a` | translated | 0x969992 |
| `0x96bf45` | translated | 0x969de9 |
| `0x96bf66` | translated | 0x96a293 |
| `0x96bf82` | translated | 0x96a373 |
| `0x96bfad` | translated | 0x965fd0 |
| `0x96bfc8` | translated | 0x965fee |
| `0x96bfef` | translated | 0x96a823 |
| `0x96c016` | translated | 0x96b312 |
| `0x96c02d` | translated | 0x9689dd ; 0x96b3cb |
| `0x96c05c` | translated | 0x9b64b4 |
| `0x96c080` | translated | 0x9b64bc |
| `0x96c0bb` | translated | 0x9b6494 |
| `0x96c0f7` | translated | 0x9b64c0 |
| `0x96c112` | translated | 0x9b64c4 |
| `0x96c134` | translated | 0x9b64c8 |
| `0x96c159` | translated | 0x9b64cc |
| `0x96c17e` | translated | 0x96b745 |
| `0x96c19b` | translated | 0x96b759 |
| `0x96c1d7` | translated | 0x9b72e8 |
| `0x96c1f2` | translated | 0x9b72f0 |
| `0x96c213` | translated | 0x9b72f8 |
| `0x96c244` | translated | 0x96b7f1 |
| `0x96c255` | translated | 0x96b85e |
| `0x96c290` | translated | 0x96b8cd |
| `0x96c2af` | translated | 0x96b905 |
| `0x96c2cb` | translated | 0x96b93f |
| `0x96c2e4` | translated | 0x96b978 |
| `0x96c300` | translated | 0x9682eb ; 0x96ba4c |
| `0x96c331` | translated | 0x96babc |
| `0x96c353` | translated | 0x96ba97 |
| `0x96c375` | translated | 0x96bb4e |
| `0x96c38d` | translated | 0x96bb72 |
| `0x96c3a6` | translated | 0x96bbd9 |
| `0x96c3ca` | translated | 0x96bc37 |
| `0x96c9b2` | translated | 0x96c693 |
| `0x96c9c5` | translated | 0x96c6f7 ; 0x96c727 |
| `0x96c9d6` | translated | 0x96c757 |
| `0x96c9ed` | translated | 0x96c77a |
| `0x96ca24` | translated | 0x96c7a1 |
| `0x96ca42` | translated | 0x96c7c0 |
| `0x96ca62` | translated | 0x96c83b |
| `0x96ca80` | translated | 0x96c881 |
| `0x96caa7` | translated | 0x96c895 |
| `0x96cac6` | exception | Ancien message de combat non référencé ; aucune référence directe dans les 32 Mio de la source, aucun consommateur de table indexée de texte dans ce bloc de scripts. |
| `0x96cae2` | translated | 0x96c8c8 |
| `0x96cb07` | translated | 0x96c8e9 |
| `0x96cc1c` | translated | 0x96cb29 |
| `0x96cc3c` | translated | 0x96cb42 |
| `0x96cc5a` | translated | 0x96cb57 |
| `0x96cc7c` | translated | 0x96cb6b |
| `0x96cca6` | translated | 0x96cb84 |
| `0x96cd83` | translated | 0x96ccf7 |
| `0x96cdad` | translated | 0x96cd04 |
| `0x96cdd0` | translated | 0x96cd2b |
| `0x96cdfe` | translated | 0x96cd38 |
| `0x96ce2f` | translated | 0x96cd45 |
| `0x96d56e` | translated | 0x96ce6f |
| `0x96d584` | translated | 0x96ce89 |
| `0x96db53` | translated | 0x96d5f6 |
| `0x96db7c` | translated | 0x9b8df0 ; 0xa0d4b8 |
| `0x96db97` | translated | 0x9b8e0c ; 0xa0d4d0 |
| `0x96dbbb` | translated | 0x9b8e10 ; 0xa0d4d4 |
| `0x96dcfd` | translated | 0x96dc71 |
| `0x96dd24` | translated | 0x96dc1d |
| `0x96dd4c` | translated | 0x96dc2d |
| `0x96dd81` | translated | 0x96dc51 |
| `0x96dda7` | translated | 0x96dc81 |
| `0x96dddf` | translated | 0x96dca1 |
| `0x9a436f` | translated | 0x9a4354 |
