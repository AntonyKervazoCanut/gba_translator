# PT-BR — PT-06 : qualification des 282 offsets (F-765)

Périmètre fermé du manifeste `languages/pt/translation_batches.json`, lot PT-06.
Les 282 sources EN et références FR au même offset ont été lues en dernière
occurrence gagnante. La ROM anglaise propre tranche les suffixes et les données
binaires ; le français n'est pas repris comme nomenclature PT-BR.
Prérequis F-758 et F-759 intégrés avant traduction.

## Résultat et zones réelles

- **140 traductions**, dont 13 descriptions d'objets actifs et 127 mots de phrases faciles.
- **82 valeurs conservées et vérifiées** : noms sans localisation attestée selon F-759,
  noms de versions, baie CHERI et formes identiques (Pokémon, Pokédex, Normal…).
- **60 exceptions sans ajout** : 43 anciennes descriptions CT/CS, 13 descriptions
  d'objets dont seul le vieux gItems FireRed garde une référence, 4 suffixes/faux textes.
- Aucune entrée d'un autre lot, aucune suppression de traduction existante.
  Chaque ajout possède sa protection exacte dans `protected_entries.yaml`.

Les capacités non attestées restent en anglais, y compris PLUS et MINUS.
Overgrow/Torrent/Blaze suivent Supercrescimento/Dilúvio/Incêndio. Types, Ataque,
Treinador et movimento suivent le glossaire. TM/HM, Berries, Mega Stone,
Cube, Bellin Town, Antisis City et The Shadow conservent les noms du projet.
Les versions RUBY/SAPPHIRE/GOLD/SILVER restent leurs noms source.

## Structures, budgets et consommateurs

Les 13 descriptions sont accessibles dans la vraie table objets CFRU, résolue
par le littéral 0x9A8D8 → 0x876200 (stride 44, description +0x14). Tous les
référents EN, y compris ceux de l'ancienne table, sont contrôlés après build.
Les 893 pointeurs capacités à 0x99F190 et les 1000 descriptions objets CFRU
ne visent aucune des exceptions. L'ancienne table FireRed 0x3DB028 n'est plus
le gItems du moteur. Les exceptions ne sont pas revendiquées comme traduites.

Les mots Easy Chat sont des chaînes référencées par des structures de 12 octets
{pointeur, ordre, disponibilité}. La table des groupes 0x3ECED4 est lue par les
littéraux 0xBD788/0xBD7C0/0xBD84C/0xBDA38/0xBDD2C/0xBE270/0xBE414.
Les pointeurs de mots sont suivis dans la ROM finale ; ordres, disponibilités,
identifiants et racines restent inchangés. Les listes gardent l'ordre du moteur.
Aucune cellule de nom fixe n'appartient aux 222 ajouts : pas de patch de table
fixe nécessaire. Une valeur qui serait ignorée par le builder fait échouer le test.

Encodage strict, terminateur FF, retours FE de la source en même nombre et ordre ;
aucun placeholder ni contrôle FC/FD/FA/FB n'existe dans les 222 entrées actives.
Mesures sur les cinq polices réellement pointées par la ROM finale : descriptions
≤186 px/ligne et trois lignes au plus ; mots ≤102 px. Les tailles indiquées
ci-dessous comprennent le terminateur. Les textes dépassant leur ancien espace
sont vérifiés à la cible vivante, sans présumer d'une écriture à l'adresse EN.
`docs/analysis/24_PT_BR_PT06.json` conserve EN/FR, prérequis de décision,
référents et mesures de chaque entrée pour la certification T-848.

## Vérification locale

`make build-pt` réussi ; 222 valeurs exactes contrôlées à travers 238 référents,
dont 97 entrées avec une cible relocalisée. Maximum constaté sur les cinq polices :
182 px pour les descriptions, 96 px pour les mots.
Tests source + ROM dédiés : **7 réussis** ; Playwright : **1 réussi**, avec
assertions OCR de contenu dans quatre scènes. TypeScript et Ruff ciblé passent.
Le hook du commit de traduction a validé 4543 tests Python rapides (un skip
préexistant), 68 tests Vitest et les constructions locales FR/IT/DE.
Les résultats définitifs après intégration sont consignés dans le bilan du ticket.
Tests dédiés : `tests/unit/pt/test_batch_pt06.py`,
`tests/e2e/pt/test_batch_pt06_rom.py` et Playwright
`tests/e2e-playwright/playwright.pt06.config.ts`.
La preuve Playwright ouvre le vrai Cube sur une copie temporaire : seul le
pointeur description du Repel détenu par la sauvegarde est remplacé par le
pointeur de l'objet testé. Aucun texte n'est réécrit dans la sonde.
Deux mots sont rendus par le vrai msgbox ; cette sonde vérifie les glyphes,
mais ne prétend pas parcourir l'éditeur complet de phrases faciles.
Captures dans le temporaire OS, hors dépôt ; aucune sauvegarde en jeu.

## Non vérifié

Navigation exhaustive de tous les contextes Easy Chat et objets historiques
retirés ; ces derniers ne sont pas réintroduits. Pas de certification globale PT,
ni de statut complete : cette responsabilité appartient à T-848.
Les badges graphiques de statut ne sont pas concernés par ce lot.
Aucun changement du code partagé ni des sources FR/IT/DE.

## Bilan offset par offset

Les référents sont les sites dans la ROM EN ; les cibles sont les adresses
finales pointées dans la ROM PT construite. ∅ signifie aucun référent/aucune
injection, pas une traduction ignorée présentée comme un succès.

| Offset | Décision | Référents EN | Cibles PT | Octets / px max | Justification |
|---|---|---|---|---|---|
| `0x3d98dc` | exception | ∅ | ∅ | 84 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9930` | exception | ∅ | ∅ | 104 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9998` | exception | ∅ | ∅ | 90 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d99f2` | exception | ∅ | ∅ | 95 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9a51` | exception | ∅ | ∅ | 78 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9a9f` | exception | ∅ | ∅ | 80 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9aef` | exception | ∅ | ∅ | 105 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9b58` | exception | ∅ | ∅ | 88 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9bb0` | exception | ∅ | ∅ | 78 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9bfe` | exception | ∅ | ∅ | 65 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9c3f` | exception | ∅ | ∅ | 77 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9c8c` | exception | ∅ | ∅ | 77 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9cd9` | exception | ∅ | ∅ | 99 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9d3c` | exception | ∅ | ∅ | 96 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9d9c` | exception | ∅ | ∅ | 81 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9ded` | exception | ∅ | ∅ | 99 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9e50` | exception | ∅ | ∅ | 92 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9eac` | exception | ∅ | ∅ | 99 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9f0f` | exception | ∅ | ∅ | 81 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9f60` | exception | ∅ | ∅ | 84 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3d9fb4` | exception | ∅ | ∅ | 83 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da007` | exception | ∅ | ∅ | 100 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da06b` | exception | ∅ | ∅ | 83 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da0be` | exception | ∅ | ∅ | 83 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da111` | exception | ∅ | ∅ | 72 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da159` | exception | ∅ | ∅ | 93 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da1b6` | exception | ∅ | ∅ | 89 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da20f` | exception | ∅ | ∅ | 83 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da262` | exception | ∅ | ∅ | 98 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da2c4` | exception | ∅ | ∅ | 90 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da31e` | exception | ∅ | ∅ | 75 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da369` | exception | ∅ | ∅ | 84 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da3bd` | exception | ∅ | ∅ | 89 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da416` | exception | ∅ | ∅ | 97 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da477` | exception | `0x653c71` | ∅ | 101 / — | Description CT/CS abandonnée ; seule coïncidence 77 A4 3D 08 à 0x653C71, non alignée au milieu de données binaires. Ni table capacités 0x99F190 ni table objets CFRU ne la visent. Aucun repointage de cette coïncidence. |
| `0x3da4dc` | exception | ∅ | ∅ | 105 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da545` | exception | ∅ | ∅ | 102 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da5ab` | exception | ∅ | ∅ | 93 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da608` | exception | ∅ | ∅ | 101 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da66d` | exception | ∅ | ∅ | 96 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da6cd` | exception | ∅ | ∅ | 81 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da71e` | exception | ∅ | ∅ | 78 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da76c` | exception | ∅ | ∅ | 101 / — | Description CT/CS FireRed abandonnée : absente des 893 pointeurs 0x99F190 et des 1000 descriptions objets CFRU. Aucun référent absolu. |
| `0x3da7d1` | traduit/vérifié | `0x3dec38`, `0x879e10` | `0x3da7d1`, `0x3da7d1` | 69 / 162 | Description objet CFRU. |
| `0x3da81a` | exception | `0x3dec64` | ∅ | 76 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3da866` | traduit/vérifié | `0x3dec90`, `0x879e68` | `0x3da866`, `0x3da866` | 55 / 160 | Description objet CFRU. |
| `0x3da8b4` | traduit/vérifié | `0x3decbc`, `0x879e94` | `0x3da8b4`, `0x3da8b4` | 39 / 182 | Description objet CFRU. |
| `0x3da907` | traduit/vérifié | `0x3dece8`, `0x87bca8`, `0x87bd2c`, `0x87bd58` | `0x3da907`, `0x3da907`, `0x3da907`, `0x3da907` | 78 / 158 | Description objet CFRU. |
| `0x3da95a` | traduit/vérifié | `0x3ded14`, `0x879eec` | `0x3da95a`, `0x3da95a` | 78 / 169 | Description objet CFRU. |
| `0x3da9bb` | traduit/vérifié | `0x3ded40`, `0x8792e4` | `0x3da9bb`, `0x3da9bb` | 55 / 162 | Description objet CFRU. |
| `0x3daa0a` | exception | `0x3ded6c` | ∅ | 90 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3daa64` | traduit/vérifié | `0x3ded98`, `0x879f70` | `0x3daa64`, `0x3daa64` | 77 / 157 | Description objet CFRU. |
| `0x3daabd` | traduit/vérifié | `0x3dedc4`, `0x879f9c` | `0x3daabd`, `0x3daabd` | 69 / 157 | Description objet CFRU. |
| `0x3dab13` | exception | `0x3dedf0` | ∅ | 70 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3dab59` | exception | `0x3dee1c` | ∅ | 70 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3dab9f` | traduit/vérifié | `0x3dee48`, `0x87a020` | `0x3dab9f`, `0x3dab9f` | 85 / 163 | Description objet CFRU. |
| `0x3dabf7` | traduit/vérifié | `0x3dee74`, `0x87a04c` | `0x7b20c6`, `0x7b20c6` | 91 / 173 | Description objet CFRU. |
| `0x3dac51` | exception | `0x3deea0` | ∅ | 84 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3daca5` | traduit/vérifié | `0x3deecc`, `0x87a0a4` | `0x3daca5`, `0x3daca5` | 73 / 162 | Description objet CFRU. |
| `0x3dad01` | traduit/vérifié | `0x3deef8`, `0x87a0d0` | `0x3dad01`, `0x3dad01` | 73 / 156 | Description objet CFRU. |
| `0x3dad5c` | exception | `0x3def24` | ∅ | 82 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3dadae` | exception | `0x3def50` | ∅ | 90 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3dae08` | exception | `0x3def7c` | ∅ | 96 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3dae68` | exception | `0x3defa8` | ∅ | 78 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3daeb6` | exception | `0x3defd4` | ∅ | 81 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3daf07` | exception | `0x3df000` | ∅ | 75 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3daf52` | traduit/vérifié | `0x3df02c`, `0x87a204` | `0xbe0296`, `0xbe0296` | 59 / 176 | Description objet CFRU. |
| `0x3daf8d` | exception | `0x3df058` | ∅ | 73 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3dafd6` | exception | `0x3df084` | ∅ | 74 / — | Description de la table objets FireRed abandonnée : unique référence dans 0x3DB028–0x3DF09B ; absente des 1000 pointeurs description de la table CFRU (base 0x876200 via littéral 0x9A8D8). Aucune injection. |
| `0x3ddd0b` | exception | ∅ | ∅ | 4 / — | Suffixe résiduel de nom dans une structure objet ancienne ; aucun pointeur vers ce suffixe. |
| `0x3dec2d` | exception | ∅ | ∅ | 4 / — | Suffixe résiduel de nom dans une structure objet ancienne ; aucun pointeur vers ce suffixe. |
| `0x3df7e8` | conservé/vérifié | `0x9c77c`, `0x14e294` | `0x3df7e8`, `0x3df7e8` | 6 / 30 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e1448` | exception | ∅ | ∅ | 6 / — | Données binaires faussement décodées en hkiii/ki… ; aucun pointeur, aucun texte autonome. |
| `0x3e144e` | exception | ∅ | ∅ | 10 / — | Données binaires faussement décodées en hkiii/ki… ; aucun pointeur, aucun texte autonome. |
| `0x3e7f35` | traduit/vérifié | `0x3e7fec` | `0xd10cbe` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f3c` | traduit/vérifié | `0x3e7ff8` | `0xd10c6c` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f42` | conservé/vérifié | `0x3e8004` | `0x3e7f42` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e7f4b` | traduit/vérifié | `0x3e8010` | `0xd10d2f` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f52` | traduit/vérifié | `0x3e801c` | `0xd10ef7` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f5f` | traduit/vérifié | `0x3e8028` | `0xd10db8` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f66` | traduit/vérifié | `0x3e8034` | `0xd10c9b` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f71` | traduit/vérifié | `0x3e804c` | `0xd10cff` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f76` | traduit/vérifié | `0x3e8058` | `0x3e7f76` | 11 / 60 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f82` | traduit/vérifié | `0x3e8064` | `0xd10e4e` | 10 / 49 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f8a` | traduit/vérifié | `0x3e8070` | `0x3e7f8a` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7f92` | conservé/vérifié | `0x3e807c` | `0x3e7f92` | 8 / 42 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e7f9a` | conservé/vérifié | `0x3e8088` | `0x3e7f9a` | 8 / 40 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e7fa6` | conservé/vérifié | `0x3e80a0` | `0x3e7fa6` | 8 / 41 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e7fae` | conservé/vérifié | `0x3e80ac` | `0x3e7fae` | 5 / 24 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e7fb3` | traduit/vérifié | `0x3e80b8` | `0xd10c4e` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7fbd` | traduit/vérifié | `0x3e80d0` | `0xd10c72` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7fc7` | traduit/vérifié | `0x3e80e8` | `0xd10c24` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7fcd` | conservé/vérifié | `0x3e80f4` | `0x3e7fcd` | 5 / 24 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e7fd2` | traduit/vérifié | `0x3e8100` | `0xd10c36` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e7fd7` | conservé/vérifié | `0x3e810c` | `0x3e7fd7` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e811d` | conservé/vérifié | `0x3e8510` | `0x3e811d` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8124` | conservé/vérifié | `0x3e851c` | `0x3e8124` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e812e` | conservé/vérifié | `0x3e8528` | `0x3e812e` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8138` | conservé/vérifié | `0x3e8534` | `0x3e8138` | 8 / 42 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8140` | conservé/vérifié | `0x3e8540` | `0x3e8140` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e814b` | conservé/vérifié | `0x3e854c` | `0x3e814b` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8156` | conservé/vérifié | `0x3e8558` | `0x3e8156` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8160` | traduit/vérifié | `0x3e8564` | `0x3e8160` | 4 / 18 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8166` | traduit/vérifié | `0x3e8570` | `0x3e8166` | 9 / 47 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8171` | traduit/vérifié | `0x3e857c` | `0xd10c54` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8176` | traduit/vérifié | `0x3e8588` | `0x3e8176` | 5 / 24 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8180` | traduit/vérifié | `0x3e8594` | `0xd10c8d` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8187` | conservé/vérifié | `0x3e85a0` | `0x3e8187` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8190` | traduit/vérifié | `0x3e85ac` | `0xd10dd3` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8198` | conservé/vérifié | `0x3e85b8` | `0x3e8198` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e81a5` | traduit/vérifié | `0x3e85c4` | `0x3e81a5` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81ae` | conservé/vérifié | `0x3e85d0` | `0x3e81ae` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e81b9` | traduit/vérifié | `0x3e85dc` | `0xd10d27` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81bf` | traduit/vérifié | `0x3e85e8` | `0xd10e1c` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81c9` | conservé/vérifié | `0x3e85f4` | `0x3e81c9` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e81d5` | traduit/vérifié | `0x3e8600` | `0xd10c42` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81da` | traduit/vérifié | `0x3e860c` | `0x3e81da` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81e3` | conservé/vérifié | `0x3e8618` | `0x3e81e3` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e81f0` | traduit/vérifié | `0x3e8624` | `0xd10c10` | 5 / 24 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81f5` | traduit/vérifié | `0x3e8630` | `0x3e81f5` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e81fe` | conservé/vérifié | `0x3e863c` | `0x3e81fe` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8205` | conservé/vérifié | `0x3e8648` | `0x3e8205` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8212` | traduit/vérifié | `0x3e8654` | `0xd10cda` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8218` | conservé/vérifié | `0x3e8660` | `0x3e8218` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8223` | traduit/vérifié | `0x3e866c` | `0xd10d17` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e822b` | traduit/vérifié | `0x3e8678` | `0xd10da6` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8231` | traduit/vérifié | `0x3e8684` | `0xd10c1a` | 5 / 24 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8235` | conservé/vérifié | `0x3e8690` | `0x3e8235` | 5 / 24 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e823a` | conservé/vérifié | `0x3e869c` | `0x3e823a` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8245` | conservé/vérifié | `0x3e86a8` | `0x3e8245` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8251` | conservé/vérifié | `0x3e86b4` | `0x3e8251` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e825e` | conservé/vérifié | `0x3e86c0` | `0x3e825e` | 5 / 24 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8263` | traduit/vérifié | `0x3e86cc` | `0xd10e30` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e826a` | conservé/vérifié | `0x3e86d8` | `0x3e826a` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8271` | conservé/vérifié | `0x3e86e4` | `0x3e8271` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e827d` | conservé/vérifié | `0x3e86f0` | `0x3e827d` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8289` | conservé/vérifié | `0x3e86fc` | `0x3e8289` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8295` | traduit/vérifié | `0x3e8708` | `0xe58c7e` | 17 / 96 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e829e` | conservé/vérifié | `0x3e8714` | `0x3e829e` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82a9` | conservé/vérifié | `0x3e8720` | `0x3e82a9` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82b5` | conservé/vérifié | `0x3e872c` | `0x3e82b5` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82bf` | conservé/vérifié | `0x3e8738` | `0x3e82bf` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82c8` | conservé/vérifié | `0x3e8744` | `0x3e82c8` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82d4` | conservé/vérifié | `0x3e8750` | `0x3e82d4` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82db` | traduit/vérifié | `0x3e875c` | `0xd10c1f` | 5 / 22 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e82e0` | traduit/vérifié | `0x3e8768` | `0xd10c2a` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e82e6` | traduit/vérifié | `0x3e8774` | `0x3e82e6` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e82f0` | conservé/vérifié | `0x3e8780` | `0x3e82f0` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e82fa` | conservé/vérifié | `0x3e878c` | `0x3e82fa` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8305` | conservé/vérifié | `0x3e8798` | `0x3e8305` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8311` | conservé/vérifié | `0x3e87a4` | `0x3e8311` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e831e` | traduit/vérifié | `0x3e87b0` | `0xd10d94` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8327` | conservé/vérifié | `0x3e87bc` | `0x3e8327` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8330` | conservé/vérifié | `0x3e87c8` | `0x3e8330` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e833d` | traduit/vérifié | `0x3e87d4` | `0xd10e00` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8344` | conservé/vérifié | `0x3e87e0` | `0x3e8344` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8351` | traduit/vérifié | `0x3e87ec` | `0xd10ca9` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8358` | conservé/vérifié | `0x3e87f8` | `0x3e8358` | 6 / 30 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e835e` | conservé/vérifié | `0x3e8804` | `0x3e835e` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8368` | conservé/vérifié | `0x3e8810` | `0x3e8368` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e836f` | conservé/vérifié | `0x3e881c` | `0x3e836f` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8378` | conservé/vérifié | `0x3e8828` | `0x3e8378` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8384` | conservé/vérifié | `0x3e8834` | `0x3e8384` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e838f` | conservé/vérifié | `0x3e8840` | `0x3e838f` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8396` | traduit/vérifié | `0x3e884c` | `0x3e8396` | 4 / 18 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e839c` | conservé/vérifié | `0x3e8858` | `0x3e839c` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83a7` | conservé/vérifié | `0x3e8864` | `0x3e83a7` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83b2` | conservé/vérifié | `0x3e8870` | `0x3e83b2` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83b9` | traduit/vérifié | `0x3e887c` | `0xd10c94` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e83bf` | traduit/vérifié | `0x3e8888` | `0xd10ce8` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e83c6` | conservé/vérifié | `0x3e8894` | `0x3e83c6` | 8 / 42 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83ce` | conservé/vérifié | `0x3e88a0` | `0x3e83ce` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83db` | conservé/vérifié | `0x3e88ac` | `0x3e83db` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83e8` | conservé/vérifié | `0x3e88b8` | `0x3e83e8` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e83f5` | conservé/vérifié | `0x3e88c4` | `0x3e83f5` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8402` | conservé/vérifié | `0x3e88d0` | `0x3e8402` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e840b` | conservé/vérifié | `0x3e88dc` | `0x3e840b` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8414` | conservé/vérifié | `0x3e88e8` | `0x3e8414` | 5 / 24 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8419` | conservé/vérifié | `0x3e88f4` | `0x3e8419` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8422` | conservé/vérifié | `0x3e8900` | `0x3e8422` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e842e` | conservé/vérifié | `0x3e890c` | `0x3e842e` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e843b` | conservé/vérifié | `0x3e8918` | `0x3e843b` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8446` | conservé/vérifié | `0x3e8924` | `0x3e8446` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8457` | traduit/vérifié | `0x3e893c` | `0xd10c15` | 5 / 24 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e845c` | conservé/vérifié | `0x3e8948` | `0x3e845c` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8467` | conservé/vérifié | `0x3e8954` | `0x3e8467` | 6 / 30 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e846d` | conservé/vérifié | `0x3e8960` | `0x3e846d` | 10 / 54 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8477` | conservé/vérifié | `0x3e896c` | `0x3e8477` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8483` | traduit/vérifié | `0x3e8978` | `0x3e8483` | 5 / 24 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8489` | conservé/vérifié | `0x3e8984` | `0x3e8489` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8494` | traduit/vérifié | `0x3e8990` | `0xd10cb7` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8498` | conservé/vérifié | `0x3e899c` | `0x3e8498` | 6 / 30 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e849e` | conservé/vérifié | `0x3e89a8` | `0x3e849e` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84a9` | conservé/vérifié | `0x3e89b4` | `0x3e84a9` | 9 / 48 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84b2` | traduit/vérifié | `0x3e89c0` | `0xd10daf` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e84b8` | conservé/vérifié | `0x3e89cc` | `0x3e84b8` | 7 / 36 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84bf` | traduit/vérifié | `0x3e89d8` | `0x3e84bf` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e84c7` | conservé/vérifié | `0x3e89e4` | `0x3e84c7` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84d2` | conservé/vérifié | `0x3e89f0` | `0x3e84d2` | 13 / 72 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84df` | conservé/vérifié | `0x3e89fc` | `0x3e84df` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84eb` | conservé/vérifié | `0x3e8a08` | `0x3e84eb` | 11 / 60 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e84f6` | conservé/vérifié | `0x3e8a14` | `0x3e84f6` | 12 / 66 | Nom anglais conservé selon F-759, ou forme PT identique. |
| `0x3e8a32` | traduit/vérifié | `0x3e8c18` | `0xd10d07` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a39` | traduit/vérifié | `0x3e8c24` | `0xd10fd9` | 16 / 90 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a44` | traduit/vérifié | `0x3e8c30` | `0xd10e09` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a51` | traduit/vérifié | `0x3e8c54` | `0xd10f2b` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a5a` | traduit/vérifié | `0x3e8c60` | `0xe58c6d` | 17 / 96 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a65` | traduit/vérifié | `0x3e8c6c` | `0xe58c5c` | 17 / 96 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a6f` | traduit/vérifié | `0x3e8c78` | `0xd10f1e` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a77` | traduit/vérifié | `0x3e8c84` | `0xd10ea4` | 11 / 60 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a80` | traduit/vérifié | `0x3e8c90` | `0xd10d9d` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a87` | traduit/vérifié | `0x3e8c9c` | `0xd10d79` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a8f` | traduit/vérifié | `0x3e8ca8` | `0x3e8a8f` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8a9a` | traduit/vérifié | `0x3e8cb4` | `0xd10e3a` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8aa4` | traduit/vérifié | `0x3e8cc0` | `0xd10df7` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8aac` | traduit/vérifié | `0x3e8ccc` | `0xd10c7f` | 7 / 35 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ab3` | traduit/vérifié | `0x3e8cd8` | `0x3e8ab3` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8abd` | traduit/vérifié | `0x3e8ce4` | `0xd10d57` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ac3` | traduit/vérifié | `0x3e8cf0` | `0xd10d4f` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8aca` | traduit/vérifié | `0x3e8cfc` | `0xd10e8e` | 11 / 60 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ad3` | traduit/vérifié | `0x3e8d08` | `0xd10d37` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ad9` | traduit/vérifié | `0x3e8d14` | `0xd10d3f` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8adf` | traduit/vérifié | `0x3e8d20` | `0xd10d5f` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ae7` | traduit/vérifié | `0x3e8d2c` | `0x3e8ae7` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8af1` | traduit/vérifié | `0x3e8d38` | `0xd10c66` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8af7` | traduit/vérifié | `0x3e8d44` | `0xd10ca2` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8afe` | traduit/vérifié | `0x3e8d50` | `0x3e8afe` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b05` | traduit/vérifié | `0x3e8d5c` | `0xd10c5a` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b0b` | traduit/vérifié | `0x3e8d68` | `0x3e8b0b` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b15` | traduit/vérifié | `0x3e8d74` | `0x3e8b15` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b1c` | traduit/vérifié | `0x3e8d80` | `0xd10f04` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b27` | traduit/vérifié | `0x3e8d8c` | `0xd10e26` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b33` | traduit/vérifié | `0x3e8da4` | `0x3e8b33` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b3a` | traduit/vérifié | `0x3e8db0` | `0x3e8b3a` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b41` | traduit/vérifié | `0x3e8dbc` | `0xd10d1f` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b4c` | traduit/vérifié | `0x3e8dd4` | `0xd10cf7` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b53` | traduit/vérifié | `0x3e8de0` | `0xd10c48` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b59` | traduit/vérifié | `0x3e8dec` | `0xd10ede` | 12 / 66 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b65` | traduit/vérifié | `0x3e8df8` | `0xd10ce1` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b6c` | traduit/vérifié | `0x3e8e04` | `0x3e8b6c` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b74` | traduit/vérifié | `0x3e8e10` | `0xd10d8b` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b7c` | traduit/vérifié | `0x3e8e1c` | `0xd10d0f` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b81` | traduit/vérifié | `0x3e8e28` | `0xd10f38` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b8b` | traduit/vérifié | `0x3e8e34` | `0xd10cd3` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b90` | traduit/vérifié | `0x3e8e40` | `0xd10ccc` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b95` | traduit/vérifié | `0x3e8e4c` | `0xd10cb0` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8b9b` | traduit/vérifié | `0x3e8e58` | `0xd10dca` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ba3` | traduit/vérifié | `0x3e8e64` | `0xd10de5` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8baa` | traduit/vérifié | `0x3e8e70` | `0xd10cef` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bb1` | traduit/vérifié | `0x3e8e7c` | `0xd10e99` | 11 / 60 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bbc` | traduit/vérifié | `0x3e8e88` | `0xd10ddc` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bc5` | traduit/vérifié | `0x3e8e94` | `0xd10c30` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bca` | traduit/vérifié | `0x3e8ea0` | `0xd10c3c` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bcf` | traduit/vérifié | `0x3e8eac` | `0xd10f11` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bd8` | traduit/vérifié | `0x3e8eb8` | `0x3e8bd8` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8be1` | traduit/vérifié | `0x3e8ec4` | `0x3e8be1` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8be8` | traduit/vérifié | `0x3e8ed0` | `0xd10c60` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8bed` | traduit/vérifié | `0x3e8edc` | `0xd10e58` | 10 / 50 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8eef` | traduit/vérifié | `0x3e9040` | `0xd10c0c` | 4 / 16 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8ef3` | traduit/vérifié | `0x3e904c` | `0x3e8ef3` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8efd` | traduit/vérifié | `0x3e9058` | `0xd10eba` | 12 / 66 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f09` | traduit/vérifié | `0x3e9064` | `0x3e8f09` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f14` | traduit/vérifié | `0x3e9070` | `0xd10c78` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f19` | traduit/vérifié | `0x3e907c` | `0xd10e12` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f24` | traduit/vérifié | `0x3e9094` | `0xd10d70` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f2b` | traduit/vérifié | `0x3e90a0` | `0xd10dc1` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f34` | traduit/vérifié | `0x3e90ac` | `0x3e8f34` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f3c` | traduit/vérifié | `0x3e90b8` | `0xd10d82` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f42` | traduit/vérifié | `0x3e90c4` | `0xd10eea` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f4c` | traduit/vérifié | `0x3e90d0` | `0xd10d47` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f54` | traduit/vérifié | `0x3e90dc` | `0x3e8f54` | 9 / 47 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f5f` | traduit/vérifié | `0x3e90e8` | `0x3e8f5f` | 4 / 18 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f65` | traduit/vérifié | `0x3e90f4` | `0x3e8f65` | 6 / 30 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f6e` | traduit/vérifié | `0x3e9100` | `0x3e8f6e` | 9 / 48 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f78` | traduit/vérifié | `0x3e910c` | `0x3e8f78` | 8 / 42 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f85` | traduit/vérifié | `0x3e9118` | `0xd10cc5` | 7 / 36 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f8c` | traduit/vérifié | `0x3e9124` | `0xd10ec6` | 12 / 66 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f93` | traduit/vérifié | `0x3e9130` | `0xd10d67` | 9 / 44 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8f9a` | traduit/vérifié | `0x3e913c` | `0xd10e78` | 11 / 60 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8fa4` | traduit/vérifié | `0x3e9148` | `0xd10e62` | 11 / 59 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8faf` | traduit/vérifié | `0x3e9154` | `0xd10f45` | 13 / 72 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
| `0x3e8fb8` | traduit/vérifié | `0x3e9160` | `0x3e8fb8` | 10 / 54 | Mot du lexique des phrases faciles ; pointeur de structure, pas cellule de nom fixe. |
