# ES-016 — contrats mécaniques et ancienne description (F-1045)

Aucune traduction de production. Les 393 clés, combined, protections et glossaire
restent inchangés. Les relevés de préparation restent les preuves historiques,
pas des consommateurs automatiquement qualifiés.

## Résultat de qualification : six alias vivants, pas sept

| Clé contractuelle | Début | Lecteur | Budget |
|---|---|---|---|
| 772093 | 772094 | 762C7F, `0F 00` puis `09 06` | 208 px, deux lignes par page |
| 781278 | 781279 | 877344, description objet | 176 px, trois lignes |
| 781668 | 781669 | 765974, `0F 00` puis `09 06` | 208 px, deux lignes |
| 788255 | 788256 | 7C871E **et** 7C8745, trainerbattle | 208 px, deux lignes par page |
| 78C2A8 | 78C2A9 | 78C280, `0F 00` puis `09 03` | 208 px, deux lignes |
| 78C2FD | 78C2FE | 78C2C0, `0F 00` puis `09 03` | 208 px, deux lignes |

**780E33 → 780E34 ne constitue pas une septième route moteur.** Sa référence
9047D0 appartient à l'ancienne table 904000. Les racines E5440, 137BC8 et 9F3B64
chargent 99F194 ; la cellule de cette capacité (501) est 99F964, vers A3A6D6.
L'ancien texte parle de « frozen », le texte courant de « frostbite ». Aucune
référence absolue vers 904000/904004 n'existe dans la ROM EN ; le seul pointeur
vers 780E34 est 9047D0. La qualification réutilise les routines et conclusions
F-1042, contrôlées sur les octets locaux. Les racines, la cellule actuelle et les
préimages sont gardées. Le contrat `excluded` refuse les deux clés 780E33/780E34,
et garde l'ancienne cellule et son texte intacts après patches.

Repoint­er uniquement 9047D0 serait un faux succès ; réaffecter le texte à
A3A6D6 changerait de source sémantique et sortirait de la sélection contractuelle.
Aucun de ces contournements n'est réalisé. **L'acceptation littérale « sept
consommateurs vivants » est donc contredite par la ROM.** F-866 doit compter
780E33 comme description ancienne justifiée, sans ligne de traduction. La
traduction de la description actuelle appartient au lot ES-025.

## Consommateurs, tampons et fenêtres

La description objet est lue par 9A96C : ID normalisé via 9A8A4, multiplication
par 44, champ +14h. Son littéral 9A98C contient la base courante 876200 ;
877344 = 876200 + 100×44 + 14h. La convention de compatibilité 876074 donne
le même champ avec l'ID 109. La fenêtre trois lignes / 176 pixels est celle des
contrats d'objets déjà livrés. Les autres champs de la structure sont gardés.
La préimage EN de cette description dépasse le budget : elle n'autorise pas à
élargir le validateur. La sentinelle utilise trois lignes conformes ; F-866 doit
recomposer sa traduction dans cette fenêtre.

Les dialogues réutilisent les métriques normales 207300, les polices dynamiques
et la fenêtre 41F42C déjà gardées par F-1043 (26 tuiles, 208 pixels). FE sépare
les lignes, FA fait défiler et FB ouvre une page. Le plafond encodé reste 512,
avec préimage et commandes intégrales : pas de fallback ou de troncature.

FD02 dans 781669 n'est **pas** le nom joueur. Le distributeur 231E78 mène à
912C qui renvoie gStringVar1, 02021CD0. Le script 76594D appelle selon le sexe
76597F ou 765986 ; `85 00` copie « sir » (781697) ou « madam » (78169B).
Ces scripts et chaînes sont gardés. Réserve conservatrice : cinq glyphes de
12 pixels, soit 60 pixels. La sonde native développe cinq M temporaires dans
ce tampon RAM, sans modifier une sauvegarde ou une ROM source.

Trainerbattle : 7C8718 (`5C 00`) et 7C873F (`5C 05`), dresseur 013F. Les deux
champs d'introduction ciblent 788256. Les champs suivants continuent à cibler
7882B8 ; les autres répliques et opcodes ne changent pas. Les occurrences
intérieures non qualifiées (772100, 78129A) restent des octets à préserver,
jamais des lecteurs ajoutés à la liste de repointage.

## Trois doublons : le vrai début est canonique

7808DE, 788538 et 78D43E sont déjà dans ES-016. **Seules ces trois clés peuvent
recevoir du texte.** Les préfixes 7808DD, 788537 et 78D43D sont refusés via la
préservation existante ; aucun alias ne les relie et `check_keys` n'est pas modifié.
Les trois vrais débuts utilisent `SystemTextRoutes`, avec commandes, métriques,
fenêtres paginées et relocalisation forcée. Les préimages restent intactes,
y compris les coïncidences intérieures. Un import des deux représentations,
même avec des textes identiques, échoue avant toute injection.

## Pipeline et preuves

Les six alias utilisent uniquement `TextAliases` et `TextSourcePreservation`.
Le CSV expose la clé contractuelle ; le JSON conserve `contract_offset` et
l'adresse vivante `offset`. Chaque route impose la préimage, les seuls pointeurs
qualifiés et `force_relocation`. L'allocateur, le réinserteur, les patches et
les vérificateurs existants sont réutilisés ; aucun code de production partagé
n'est modifié. Aucun texte n'est ajouté à une clé hors lot.

- `tests/unit/test_es016_routing.py` : activation sélective, anciennes tables,
  refus des doublons, perte d'arguments, dépassements, relocation même courte
  et comparaison de tous les octets.
- `python3 scripts/audit_es016_preparation.py --probe-routing --output output/reports/es016-routing.json` : la sonde indique
  six résolutions et un refus explicite. Le relevé historique 0/7 est conservé
  dans Git ; ne pas confondre sa date avec les contrats maintenant présents.
- `python3 -m pytest tests/e2e/es/test_es016_routing.py -q` : neuf sentinelles
  temporaires (six alias, trois canoniques), vrai CSV → JSON → builder → tous
  les patches. Dix champs pointeurs contrôlés ; comparaison binaire exhaustive
  avant patches et contre un témoin subissant les mêmes patches après build.
  Les seules différences autorisées sont ces champs et leurs allocations.
  Les empreintes des sources de traduction et des ROM d'entrée sont comparées.
- `npx playwright test --config tests/e2e-playwright/fixtures/es016-routing.config.ts` :
  navigateur headless, mGBA explicitement `QT_QPA_PLATFORM=offscreen`, lectures
  natives de tous les pointeurs (octet par octet pour les non-alignés), expansion
  native des tampons, mesure par GetStringWidth et rendu par l'imprimeur moteur.
  Neuf mires, toutes les lignes mesurées, au plus sept affichées par mire.
  Aucune sauvegarde en jeu ; la flash créée reste intégralement FF.

Le banc ES-015 est paramétré et partagé pour éviter une copie du pipeline ou
de l'imprimeur. Son périmètre reste fixé à son propre lot. La capture OS temporaire
après assertions est attachée à F-1045 :
`attachment://b8d13145-5a92-441a-899b-183362e2b49e`.
Après rebase, pipeline et assertions natives repassés :
`attachment://35774412-5577-4fce-b156-9ba55b5062ee`.
Les parcours naturels, les traductions finales et la certification linguistique
restent à F-866 ; la mire native ne prétend pas les remplacer.
