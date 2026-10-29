# ES-003 — traitement et preuves

F-853, 29 octobre 2026. Liste contractuelle inchangée : **374 offsets**.
D-849, F-850, B-1030 et B-1031 sont terminés et intégrés.
[003_TRAITEMENT.json](003_TRAITEMENT.json) contient une décision motivée pour
chaque offset, les préimages EN, correspondances ES disponibles, référents,
valeurs finales, octets attendus, cibles observées et budgets. Les tests résolvent
les pointeurs du build courant ; les cibles du rapport sont un instantané.

## Résultat

| Décision | Entrées |
|---|---:|
| Traduites et protégées | 221 |
| Noms propres ou formes également espagnoles conservés | 17 |
| Données nominales et copie technique conservées | 78 |
| Fragments chevauchant une autre clé vivante, exclus | 8 |
| Données binaires/graphiques, exclues | 50 |
| Total | 374 |

Les traductions comprennent 87 classes, 16 types, 78 descriptions de talents,
13 messages/dialogues et 27 descriptions d’objets. Chaque valeur est protégée
exactement dans protected_entries.yaml. Les seules sources modifiées sont
es-maint ; combined EN, ES référence et FR, glossaire et lots restent inchangés.

Les effets Wonder Guard, Color Change, Lightning Rod et Revive sont traduits
depuis l’EN vivant. Commandes FC/FD/F8/F9/F7 avec arguments et FA/FB sont
comparées dans l’ordre. La ponctuation finale de 0x270FA1 est B0 (points de
suspension), pas un guillemet. Autovía SES reste distincte de KBT ; Challenge
Road et Great Desert conservent leur noyau propre selon D-849.

Coleccion. abrège Collector au budget de 12 octets utiles. Fam. Karate remplace
le reliquat anglais Kin Karate ; Exad.Shadows abrège l’ancien administrateur
en conservant le nom de faction. Ces compactes de projet ne prétendent pas
être des dénominations officielles complètes. Pokéfan et Rival sont aussi
espagnols ; Black Horizo et Black Emboar restent des noms propres du hack.
Les noms/surnoms des structures de 60 octets et leurs préfixes restent intacts.

Les 77 extractions de l’ancienne table de talents (base 0x24FC40, stride13)
restent conservées techniquement : beaucoup commencent dans le bourrage
précédent. La table principale CFRU des noms est 0xA36398, stride17, référencée
notamment à 0xD8004/0xD8624/0x1367A0. La référence historique 0x8A123C est
explicitement consignée : l’absence de pointeur individuel ne prouve pas
qu’une routine est inaccessible. Le parcours de toutes les routines historiques
reste une limite à examiner à T-914 ; ce lot ne réécrit pas cette copie à des
débuts artificiels. fghijk est un champ nominal de données Dresseur conservé.

## Acheminement

B-1031 fournit les 17 routes gItems (34 consommateurs) : treize absences
reconstruites et quatre layouts fixes, trois lignes FE sans FA/FB ajouté,
176 pixels par ligne. La passe existante trainer_class_names_it écrit les
cellules de 13 octets depuis le combined es-maint, sans nouvelle infrastructure.

Quatre alias de données réutilisent B-1030, sans changer les clés du lot :

- 0x24F20D → 0x24F210 : DRAGÓN, préfixe 00 00 00.
- 0x24F3C1 → 0x24F3C4 : Sin habilidad., préfixe 05 00 00 ; trois consommateurs,
  dont les talents 0 et 77.
- 0x2779D4 → 0x2779D5 : dégâts des pierres, préfixe 00.
- 0x2779F1 → 0x2779F2 : toile gluante, préfixe FE.

Les deux messages de combat gardent FD00. Préimages, offset map, pointeurs EN/ES
et préfixes sont validés. Aucun ajout de clés +1/+3 au combined.
Le préfixe nul de DRAGON est aussi le padding de ICE : HIELO réutilise deux
octets de ce padding. Le test vérifie exactement HIELO, FF, 00, puis le début
vivant de DRAGÓN ; les textes consommés ne se chevauchent pas. Les préfixes
05 00 00, 00 et FE des trois autres alias restent inchangés.
Le suffixe 0x26D4E5 est vérifié derrière la structure 00 FC 03 00 00 00,
sans inventer un pointeur direct au suffixe.

## Vérifications reproductibles

Après make build-es-maint :

```sh
python3 -m pytest tests/e2e/es/test_es003_delivery.py tests/e2e/es/test_contractual_aliases.py -q
npx playwright test --config tests/e2e-playwright/es003.config.ts
make test-python
```

Les tests ROM contrôlent les 221 valeurs aux consommateurs finaux, les cellules,
préfixes, données conservées/exclues et l’exhaustivité des 374 décisions.
La sonde d’alias exerce le vrai CSV/JSON et force les relocalisations.
Les budgets du rapport réservent dix glyphes larges pour les buffers FD.
Builds et tests ROM doivent être exécutés en série : le hook reconstruit les
extractions partagées ; une lecture pendant leur écriture n’est pas exploitable.

Playwright headless vérifie huit textes imprimés par mGBA offscreen puis capture.
Pour les deux messages FD00, la sonde d’imprimante hors combat substitue dix W
sur une copie temporaire : le moteur overworld n’expanse pas les buffers combat.
Les octets ROM de production restent intacts et sont contrôlés séparément.
Une seconde sonde vérifie les 34 consommateurs et les trois lignes de la
Super Potion dans le Cube natif. Aucune sauvegarde en jeu.

ROM ES-003 validée :
9333f79b6f3b142cc157dce3c7d6cad7018771984a4ef54f5231c4dcc0751002.
Témoin FR aux mêmes sources, identique après les builds :
2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863.
Résultats finaux des suites et captures attachés à F-853.

## Non vérifié

Parcours naturel de chaque rencontre, carte numérique exacte des dialogues depuis
tous les niveaux de scripts, expansion des buffers dans un combat réel et
accessibilité de toutes les anciennes routines de talents. Les référents directs
et le rôle des scènes sont consignés sans déduire une zone de l’adresse.
La sonde d’imprimante ne prétend pas certifier ces parcours. Aucun passage de
la langue au statut complete, push, publication ou pipeline distant.
