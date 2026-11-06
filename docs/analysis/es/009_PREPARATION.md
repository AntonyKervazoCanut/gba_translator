# ES-009 — préparation binaire, traduction non livrée

F-859, 6 novembre 2026. Projet gba_translator, parent A-663 vérifié ;
D-849 et F-850 terminés et intégrés.

[009_PREPARATION.json](009_PREPARATION.json) conserve les **374 clés exactes**
de lots.json, les colonnes EN/ES/FR de l’inventaire, les préimages EN ROM
intégrales, les occurrences binaires de pointeurs et leurs voisins à ±1/2/3,
la correspondance ES disponible par offset map, les octets ES correspondants
et les séquences de commandes du parseur actuel. Les deux ROMs sont épinglées
par SHA-256. Aucun texte EN ne manque dans l’inventaire de ce lot ; les seize
absences signalées par l’audit concernent ES. La plus longue préimage mesure
159 octets avec FF : aucune troncature au plafond 512 n’est nécessaire.

| Qualification provisoire | Nombre |
|---|---:|
| Clé possédant des occurrences de pointeurs, consommateurs à qualifier | 358 |
| Bourrage avant une autre clé du même lot | 6 |
| Sans occurrence directe de pointeur | 10 |
| Total | 374 |

Ces qualifications ne sont pas des décisions finales de traduction/exclusion.
Une occurrence binaire peut appartenir au graphisme ; une absence de pointeur
direct ne démontre pas l’inaccessibilité dynamique. Les zones géographiques
restent explicitement non certifiées, sans attribution depuis l’adresse ROM.

## Surfaces nécessitant un contrat distinct

**34 choix** comportent FC 13 puis FC 06 : noms, prix et positions partagent
une ligne. `_encoded_layout_widths` dans le builder saute actuellement les
commandes FC et leurs arguments ; il ne modélise ni le changement de police
ni le positionnement de la colonne prix. Une largeur statique ordinaire ne
prouve donc pas l’absence de chevauchement. Les sept messages F7 du stockage
doivent également être contrôlés après expansion effective de leur tampon.
La sémantique exacte des arguments est à confirmer dans le moteur ; le décodage
debug de l’inventaire ne fait pas autorité. Notamment FC 10 31 00 dans
0x416EC6 est une commande complète, pas des lettres espagnoles à importer.

Les racines candidates sont consignées avec leurs octets et leurs références :
0x3CEA88 (tables messages PC, littéraux 0x8FBC8/0x8FCE4), 0x3D353C
(actions PC, littéral 0x94E48), 0x3F5B44 (étages, littéral 0xCB634).
Les miroirs 0x9A425C/0x9A41B8 n’ont pas de référence directe à leur base.
Les bornes candidates doivent être confirmées depuis les routines : elles
ne sont pas présentées comme une cartographie de toutes les utilisations.

La référence PT-12 fournit un précédent vérifiable sur la même ROM EN :
docs/analysis/28_PT_BR_PT12.md, languages/pt/data/pt12_audit.json et son
finaliseur. Elle distingue cinq occurrences graphiques fortuites, aux sites
0x3BFC8A, 0x40F1AA, 0x1AAA166, 0x1BB7B57 et 0x1DA2F35, de vrais opérandes
de scripts non alignés. Ne pas recopier son patch ni déduire une corruption
actuelle : les protections génériques ont évolué. Vérifier ces cinq sites
avant/après une relocation forcée et tous les patches ES.

Le lot interdit de modifier l’infrastructure partagée. L’extension ciblée des
contrats de fenêtres/routage et ses sondes moteur doivent donc être livrées
séparément, en réutilisant les primitives existantes. Cette préparation ne
modifie ni manifeste technique, glossaire, combined, protection, ni ROM source.

## Reprise

Après le prérequis technique : relire/importer les traductions, documenter les
noms officiels inchangés, qualifier les dix chaînes sans pointeur et finaliser
les 374 décisions. Les six clés de bourrage ont déjà une autre clé vivante dans
le même lot : aucune nouvelle clé d’alias n’est nécessaire pour ces doublons.
Vérifier chaque valeur à tous ses consommateurs finaux, avec commandes et
arguments, largeur selon la police effective, pagination et isolation du lot.
Terminer par build es-maint, tests Python, témoin FR aux mêmes sources,
assertions Playwright en émulateur puis capture attachée.

Les gardes de préparation se reproduisent avec :

```sh
python3 -m pytest tests/unit/test_es009_preparation.py -q
```

Le troisième test relit les ROMs réelles et porte le marqueur rom ; il faut
l’exécuter explicitement, sans filtre qui exclut ce marqueur. Aucun rendu
traduit n’est revendiqué ; aucune capture de préparation ne certifie le lot.

Vérification initiale de cette préparation : trois tests réussis (dont la
relecture ROM exhaustive), Ruff et diff --check réussis, make build-es-maint
réussi. Témoin FR reconstruit avant les hooks, BUILD_NUMBER=0 :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
La suite Python standard, les hooks et la seconde comparaison FR sont
consignés dans le résultat d’orchestration ; ils ne certifient aucune des
traductions finales encore absentes.
