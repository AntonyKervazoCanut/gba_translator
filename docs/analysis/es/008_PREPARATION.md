# ES-008 — préparation technique, traduction non livrée

F-858, 6 novembre 2026. Parent A-663 et prérequis D-849/F-850 consultés,
terminés et intégrés. Dépôt : gba_translator.

[008_PREPARATION.json](008_PREPARATION.json) couvre les **373 clés exactes**
de lots.json. Il conserve les colonnes de l'inventaire, les préimages EN
complètes depuis la ROM, les commandes avec arguments et FE/FA/FB dans
l'ordre, toutes les occurrences directes de pointeurs, les voisins référencés
à -1/+1/+2/+3 et la correspondance ES disponible par offset map.
Les préimages ne sont pas limitées à 512 octets ; aucune ne dépasse ce plafond
dans ce lot. Les empreintes des deux ROM sources sont incluses.

Il s'agit d'une préparation, pas du rapport d'acceptation : aucune traduction
finale, exclusion définitive, attribution géographique ou injection n'est
revendiquée. Les surfaces proposées doivent être confirmées depuis les scripts
et les consommateurs réels, pas depuis la position dans une banque ROM.
L'absence d'un pointeur direct ne prouve jamais une chaîne morte.

| Qualification provisoire | Entrées |
|---|---:|
| Clé avec consommateur direct à qualifier | 324 |
| Début décalé ou fragment, voisin référencé | 19 |
| Sans pointeur direct retrouvé | 30 |
| Total | 373 |

## Prérequis d'acheminement distinct

Le ticket interdit la modification de l'infrastructure partagée. Les sept
clés suivantes ne figurent pas dans text_aliases.json, alors que leurs textes
vivants ont des consommateurs. La clé reste contractuelle ; il faut ajouter
un contrat technique sans traduire une autre clé ni écrire le bourrage :

| Clé du lot | Début vivant | Référents |
|---|---|---|
| 0x415D45 | 0x415D48 | 0x12EF3C, 0x12F484, 0x12F62C |
| 0x415D4F | 0x415D50 | 0x12F038, 0x12F640 |
| 0x415D5E | 0x415D60 | 0x0F2D54, 0x9F2868 |
| 0x415D77 | 0x415D78 | 0x0F2D20, 0x9F285C |
| 0x415D8A | 0x415D8C | 0x0F30FC |
| 0x4160F9 | 0x4160FC | 0x0F35F8 |
| 0x416101 | 0x416104 | 0x0F33D8, 0x0F3600, 0x9F2B98 |

Le dernier début vivant n'a pas de correspondance ES dans l'offset map :
la vérification stricte actuelle de TextAliases exige un match ES et ne suffit
donc pas sans adaptation contrôlée. Ne pas inventer une correspondance.
Les racines de tables et les contrôles de largeur des aides F8/F9 doivent
être vérifiés par le prérequis, avec sentinelles et pointeurs finaux.

Deux clés sont des suffixes intérieurs : 0x3FE865 correspond au texte
référencé à 0x3FE864 (littéral 0xE674C), et 0x3FE88C au texte référencé à
0x3FE88B (littéral 0xD8704). Le suffixe apostrophe-s 0x3FE88F est consommé
à 0xD871C. B-1033 documente déjà la routine 0xD86C8 et la concaténation
0x8D84 pour PT-BR, mais son périmètre ne couvre pas es-maint. Il faut qualifier
les branches et leurs appelants puis établir la construction espagnole complète,
sans considérer « is » et apostrophe-s comme de simples mots à traduire.
Cette préparation ne conclut pas que chaque branche a un sens possessif.

La clé 0x415FAD n'a pas de texte EN dans l'inventaire, mais la ROM contient
F8 04 BD E6 ED FF : commande F8 04 suivie de « Cry ». Les deux pointeurs
0x105FE4 et 0x1067B8 la référencent. L'argument 04 n'est pas une lettre.
Cette absence est reconstruite, sans déduire une phrase depuis le FR.

Les fragments voisins d'une autre clé du lot (par exemple 0x3FCFE5,
0x3FD851, 0x3FE673 et 0x416007) restent recensés séparément. Ne pas créer
deux traductions concurrentes pour un même texte vivant. Les autres absences
de pointeur doivent encore être suivies depuis leurs racines/accès relatifs.

## Reprise et validation

Après livraison du prérequis technique, reprendre la relecture linguistique,
les 373 décisions finales, les imports chirurgicaux et protections exactes.
Vérifier chaque valeur au consommateur vivant après tous les patches ; contrôler
les budgets par fenêtre, buffers, pagination et commandes. Le rapport actuel
ne remplace pas ces contrôles ni les assertions Playwright et captures finales.

Les gardes de préparation se reproduisent avec :

```sh
python3 -m pytest tests/unit/test_es008_preparation.py -q
```

Aucun combined, glossaire, manifeste d'acheminement, source ROM ou code partagé
n'est modifié. Aucun affichage changé : aucune preuve visuelle de traduction
n'est revendiquée. Les résultats des builds, tests et hooks sont consignés
dans le ticket avant la mise en attente. Aucun push ni pipeline distant.
