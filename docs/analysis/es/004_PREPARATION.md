# ES-004 — préparation technique, lot non livré

F-854, 6 novembre 2026. D-849 et F-850 terminés et intégrés, ainsi que
B-1030/B-1031/B-1032, consultés avant cette préparation. Le parent A-663
confirme le dépôt gba_translator. Aucune traduction n'est encore importée.

[004_PREPARATION.json](004_PREPARATION.json) couvre les **374 clés exactes**
de lots.json, sans sélection par plage ni `--skip-existing`. Chaque clé possède
sa préimage complète de la ROM EN actuelle, les occurrences directes de son
pointeur à tous les alignements, sa correspondance disponible dans l'offset map,
les octets ES correspondants et les trois colonnes originales de l'inventaire.
Les empreintes permettent de distinguer les sources du cache d'extraction.
Les qualifications sont des propositions techniques, pas le rapport final de
traduction et d'injection demandé par l'acceptation.
Les cibles ES aux sites physiques homologues sont également lues, mais marquées
comme candidates : la seule identité d'adresse ne prouve pas l'identité de
consommateur. Les points de correction linguistique déjà repérés sont consignés
pour 179 entrées, sans prétendre à une relecture finale des autres.

| Qualification provisoire | Nombre |
|---|---:|
| Descriptions d'objets | 221 |
| Anciennes descriptions CT/MO | 58 |
| Mots de groupes Easy Chat | 88 |
| Nom CHERI (Baya Zreza), consommateur à vérifier | 1 |
| Fragments résiduels | 4 |
| Données binaires | 2 |
| Total | 374 |

## Acheminement à compléter séparément

Le lot interdit les modifications de l'infrastructure partagée. Le routage
B-1031 existe, mais son manifeste contient les 17 descriptions d'ES-003,
**aucune des 221 d'ES-004**. Les trois descriptions `0x003D5934`,
`0x003D5968` et `0x003D5AB8` sont absentes de l'extraction EN disponible malgré
leurs consommateurs gItems. Trente-sept autres préimages de cette extraction
diffèrent de la ROM actuelle ; notamment sa chaîne française « Un lait très
nourrissant » à `0x003D5706` ne représente pas la source EN vivante.
Régénérer un cache dérivé est permis, mais ne fournit pas à lui seul le contrat
de fenêtre fixe, de refus du fallback et de contrôle final aux consommateurs.

La table CFRU réellement utilisée a pour base **0x876200**, stride 44 et champ
description +0x14. Les deux littéraux `0x9A8D8` et `0x9A98C`, ainsi que les
octets de l'accesseur `0x9A96C`, sont consignés et vérifiés. La base 0x876074
du contrat B-1031 est compatible avec un décalage d'ID de neuf ; ne pas confondre
ces indices techniques avec les IDs moteur. **167** descriptions du lot ont un
consommateur dans cette table ; les **54** autres possèdent des références dans
l'ancienne table d'objets 0x3DB028. Leur accessibilité doit être établie avant
d'affirmer qu'elles sont mortes ou avant de modifier leurs seuls pointeurs anciens.

Les 88 mots pointent vers des structures Easy Chat de 12 octets. Ces mots
comprennent des types, des habilités et des noms de versions ; ils ne sont ni
des dialogues de carte ni la table principale des habilités CFRU. Leurs largeurs
restent à établir. Les deux groupes commencent à 0x3E7FE0 et 0x3E8504,
référencés respectivement à 0x3ECEDC et 0x3ECEE4 dans la table de groupes
0x3ECED4. Les références à ces racines sont consignées séparément : l'absence
de référence au premier mot **du lot** ne prouve pas un groupe inaccessible.
CHERI possède deux
référents directs, `0x9C77C` et `0x14E294` ; sa traduction ne doit pas suivre
la règle PT de conservation des noms anglais. Les noyaux Pokémon/Pokédex
pourront être conservés après justification individuelle.

La préparation ne déduit aucune carte géographique de l'adresse. Elle identifie
la surface depuis les consommateurs : descriptions du Cube, groupes Easy Chat,
ou absence de consommateur textuel démontré. La seule occurrence vers
`0x3DA477` est à `0x653C71`, non alignée au milieu de données binaires :
elle n'autorise pas un repointage. Les 57 autres anciennes notices CT/MO n'ont
aucun pointeur direct. Ces notices doivent rester distinctes des descriptions
de mouvements vivantes et de leur table 0x99F190.
Le littéral de base repéré dans les consommateurs est 0x99F194 ; le premier
pointeur à 0x99F190 précède cette base. Ces deux adresses sont distinguées
dans le rapport pour éviter une conclusion fondée sur un décalage de quatre octets.

Le prérequis technique doit réutiliser B-1031 autant que possible, sans nouvelle
passe parallèle de réinsertion : préimages complètes, consommateurs exhaustifs,
fenêtres objets de trois lignes FE et 176 pixels, commandes et arguments intacts,
FA/FB interdits dans la fenêtre objet, plafond 512, refus de troncature/fallback,
contrôle après tous les patches et sentinelles sur le vrai CSV/JSON/builder.
Les mots Easy Chat exigent une ligne et un budget attesté depuis leur moteur.
Les caches EN/ES doivent être isolés dans le worktree ; aucun cache partagé
ne doit être réécrit par cette préparation.

## Reprise

Après intégration de ce prérequis, reprendre la relecture des 374 entrées depuis
les préimages ROM du rapport. Traduire/corriger/importer uniquement les clés
contractuelles dans combined_es-maint.txt, avec protection exacte dans le même
commit, puis produire le rapport final par offset. Vérifier commandes complètes,
budgets, octets aux pointeurs vivants et absence de changements hors lot.
La préparation ne remplace ni ces traductions, ni le build final, ni les preuves
d'affichage Playwright headless attachées après assertions.

## Vérifications de préparation

Le test unitaire contrôle l'exhaustivité contractuelle et empêche de présenter
ce rapport provisoire comme une livraison. Son test marqué `rom` contrôle les
374 préimages, toutes les références directes, les bases gItems et les octets ES
de l'offset map. Commande :

```sh
python3 -m pytest tests/unit/test_es004_preparation.py -q
```

Aucun combined, glossaire, manifeste d'acheminement, source ROM ni code de
production partagé n'est modifié. Aucun nouvel affichage n'est livré : aucune
preuve visuelle de traduction n'est revendiquée à cette phase. Le témoin FR
du checkout principal avant préparation vaut
`74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e` ;
il ne doit pas être confondu avec une reconstruction de développement à numéro 0.
Les résultats des commandes et des hooks seront consignés dans le ticket avant
la mise en attente du prérequis.

Résultats locaux de préparation : `make build-es-maint BUILD_NUMBER=0` réussi,
SHA-256 `708c0d1cd5abdc3138cc4663204a6cc7fba704c8a7ea9149cf5ecc893311f0bc`,
identique au lot ES-001 intégré. `make build-fr BUILD_NUMBER=0` réussi,
SHA-256 `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
La première passe `make test-python` a donné 9214 réussites, 55 skips et
12 échecs en 710 secondes : onze lectures FR pendant sa reconstruction et
un test de recette DE nécessitant l'artefact DE absent de ce worktree neuf.
Après stabilisation FR, les trois fichiers FR concernés et les deux tests de
préparation passent ensemble : **18 réussites**. Aucun attendu de test n'a été
modifié. Cette première passe ne constitue pas une suite intégralement verte ;
les résultats des contrôles suivants doivent être consultés dans le ticket.
