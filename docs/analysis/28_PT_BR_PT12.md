# PT-BR - PT-12 : menus et systèmes (F-771)

## Périmètre

282 offsets explicites du manifeste : 263 traductions ou noms conservés suivant F-759, 19 exceptions sans pointeur autonome. Sources EN et comparaison FR au même offset. Aucun offset extérieur au lot ni aucune traduction existante supprimée. Prérequis F-758 et F-759 intégrés.

Le domaine réel couvre les menus d’équipe, les soins et apprentissages, le PC et son courrier, les échanges, les choix de combat, les boutiques et les anciens menus Kanto/Sevii. Espèces, objets et noms propres non attestés restent anglais suivant F-759. Statistiques PS/Ataque/Defesa/Velocidade et conventions PSN/PAR/DRM/QMD/CNG respectées.

## Livraison bornée

Les consommateurs sont des pointeurs littéraux Thumb, des scripts loadword/message et des tables. Aucune cellule indexée à pas fixe identifiée dans ce lot. Le patch final batch_12.py réutilise StructuredTextPatch, contrôle les préimages EN et chaque référence, alloue une chaîne terminée sans écraser ses voisines et repointe les seuls consommateurs déclarés. FE/FA/FB, FD et commandes FC avec leurs paramètres restent identiques à EN. Le contrat empêche un fallback ou rewrap générique de livrer une valeur différente. La table native de multichoix à 0x3e04b0 et ses enregistrements pointeur/nombre de choix gardent leur structure.

Cinq coïncidences binaires graphiques sont exclues : 0x40f1aa, 0x1bb7b57, 0x3bfc8a, 0x1aaa166, 0x1da2f35. Leurs quatre octets sont restaurés depuis EN après le scanner générique. En revanche, les opérandes de scripts non alignés 0x8c5795, 0x8c10b3, 0x1e5202e et 0x1e51feb sont conservés. Le journal JSON expose aussi les sites rejetés.

Les six préfixes de padding sans pointeur possèdent une chaîne utile suivante, traduite à son propre offset. Les suffixes 0x41735b et 0x41736b ne sont jamais injectés seuls. Les onze autres exceptions sont des textes historiques sans référence littérale ni entrée dans les tables identifiées ; aucune traduction livrée n’est revendiquée pour eux.

## Validation

Tests unitaires : couverture fermée, 263 protections exactes, encodage strict, commandes et ruptures, budgets statiques. Tests ROM : tous les sites consommateurs, octets exacts, cinq faux pointeurs graphiques intacts, idempotence et rejet atomique de préimage invalide. Largeurs mesurées sur les cinq polices moteur avec variables longues et positions des prix.

`make build-pt` réussi. Les trois tests ROM PT-12 passent : 263 valeurs exactes aux 426 sites consommateurs, contrôles et largeurs sur les cinq polices, patch idempotent et validation atomique. Aucun changement dans src/core/ ni les scripts partagés.

Playwright hors écran : 1 test réussi (9,3 s). Deux vrais menus multichoice, appelés par un script de sonde sur une copie temporaire, affichent BATALHA INDIVIDUAL/DUPLA/MÚLTIPLA et 50/500 FICHAS. Deux messages livrés sont rendus par le moteur msgbox ; la sonde de soin remplace uniquement FD02/FD03 par CHARMANDER/999 et compare les octets de substitution avant rendu. OCR portugais et contrôle négatif des anciens libellés anglais. Ni sauvegarde en jeu, ni fenêtre visible. Capture jointe au ticket : `attachment://27b79b96-7d79-4eb1-891f-cd76378785cf`.

ROM PT vérifiée : SHA256 `e0690d021379985d7b1197a76aaf1f5fd49fbec852f9ec7ce5cd467389e0a8be`.

Non vérifié : parcours manuel exhaustif des 263 entrées et activation naturelle de tous les anciens menus Kanto ; cela relève de T-848. Le libellé Exit visible dans les deux sondes provient de 0x4161c8, hors PT-12, et reste volontairement inchangé. Les noms propres/objets anglais conservés ne sont pas présentés comme traduits officiellement. Aucun push ni pipeline distant.

La passe élargie `tests/unit/pt tests/e2e/pt tests/unit/test_release_recipes.py tests/unit/test_translation_integrity.py` réussit : **1939 tests**. Après les dernières assertions de table et de métadonnées, les **8 tests PT-12** repassent. Ruff ciblé et `git diff --check` passent.

Le test ROM PT-06 comparait ses cibles absolues historiques avec celles de tout nouveau build : 97 chaînes ont changé d’allocation, mais les 222 textes sont toujours exacts. Son assertion porte désormais sur le nombre de consommateurs ; les contrôles de source, de pointeurs vivants, d’octets livrés et de largeur demeurent. Aucun texte PT-06 modifié. Le premier hook a aussi révélé une ROM DE locale absente dans un sous-Make exécuté malgré dry-run ; `make build-de` a préparé cet artefact, sans changer les sources.

## Reprise après interruption

Le commit initial avait conservé le patch et les preuves, mais pas les ajouts des sources. La reprise restaure exactement les 263 valeurs auditées et leurs protections, et active `batch_12` dans le registre, sans réécrire les entrées existantes. Commit de restauration : `ff257cf8`, hooks actifs (5347 tests Python réussis, un skip préexistant, 68 tests Vitest et builds FR/IT/DE réussis).

Le rebuild PT réussit ; 38 contrôles ciblés PT-12/intégrité passent et le test Playwright hors écran repasse (10,4 s). SHA256 de ce rebuild : `9dca48753cfbaa227df0bccb257a598babee3bc38896d16189e9a54ef48d443a`. Le hash et les cibles du journal JSON restent les métadonnées de la capture initiale : le test de régression résout désormais les pointeurs vivants et compare chaque texte exact sans figer l'allocation ni le hash global, sensibles aux lots voisins. Les préimages EN, les 426 consommateurs, les faux pointeurs, les largeurs et l'idempotence restent contrôlés.

## Bilan offset par offset

Le journal languages/pt/data/pt12_audit.json contient les préimages, sites, tailles et largeurs. La vérification binaire couvre tous les consommateurs déclarés ; la preuve visuelle ne prétend pas visiter chaque écran.

| Offset | État | Consommateurs EN | Décision |
|---|---|---|---|
| `0x416a3a` | Traduit/conservé, vérifié ROM | `0x127c60` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416a55` | Traduit/conservé, vérifié ROM | `0x127bd4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416a75` | Traduit/conservé, vérifié ROM | `0x127b38` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416a98` | Traduit/conservé, vérifié ROM | `0x127b04` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416acb` | Traduit/conservé, vérifié ROM | `0x127ba0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416ae2` | Traduit/conservé, vérifié ROM | `0x12464c`, `0x8c5795` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416b16` | Traduit/conservé, vérifié ROM | `0x1241fc`, `0xa02d58`, `0xa6c928` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416b3e` | Traduit/conservé, vérifié ROM | `0x124180`, `0xa02e88`, `0xa6c924` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416b64` | Traduit/conservé, vérifié ROM | `0x123e4c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416b86` | Traduit/conservé, vérifié ROM | `0x123eec` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416ba6` | Traduit/conservé, vérifié ROM | `0x123f10` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416bc3` | Traduit/conservé, vérifié ROM | `0x123f40` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416bfb` | Traduit/conservé, vérifié ROM | `0x127378` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416c2a` | Traduit/conservé, vérifié ROM | `0x1204a8`, `0xa0190c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416c49` | Traduit/conservé, vérifié ROM | `0x120554` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416c8f` | Traduit/conservé, vérifié ROM | `0x123cbc`, `0xa016e8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416cac` | Traduit/conservé, vérifié ROM | `0x120508` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416cc7` | Traduit/conservé, vérifié ROM | `0x124004` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416cea` | Traduit/conservé, vérifié ROM | `0x1205c4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416d17` | Traduit/conservé, vérifié ROM | `0x127468` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416d4f` | Traduit/conservé, vérifié ROM | `0x12749c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416d78` | Traduit/conservé, vérifié ROM | `0x1206a4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416db3` | Traduit/conservé, vérifié ROM | `0x125ce8`, `0x126888`, `0x1e5202e` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416dc2` | Traduit/conservé, vérifié ROM | `0x125bf8`, `0x9a34ac` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416df7` | Traduit/conservé, vérifié ROM | `0x125c2c`, `0x126280`, `0x1267f8`, `0x126ea4`, `0x1e51feb` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416e6b` | Traduit/conservé, vérifié ROM | `0x126130` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416e84` | Traduit/conservé, vérifié ROM | `0x126204` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416ea4` | Traduit/conservé, vérifié ROM | `0x125dfc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416ec6` | Traduit/conservé, vérifié ROM | `0x126070` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416f10` | Traduit/conservé, vérifié ROM | `0x125c08`, `0x126e80`, `0x9a34b0`, `0x1ed551c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416f27` | Traduit/conservé, vérifié ROM | `0xe5894`, `0x1255b0`, `0x126b54` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416f4e` | Traduit/conservé, vérifié ROM | `0x1250d8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416f6f` | Traduit/conservé, vérifié ROM | `0x125128` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416f8c` | Traduit/conservé, vérifié ROM | `0x1250ec` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416f9a` | Traduit/conservé, vérifié ROM | `0x125100` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416fb2` | Traduit/conservé, vérifié ROM | `0x125114` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416fc7` | Traduit/conservé, vérifié ROM | `0x125200` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x416fed` | Traduit/conservé, vérifié ROM | `0x125164` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417002` | Traduit/conservé, vérifié ROM | `0x1251ec` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417017` | Traduit/conservé, vérifié ROM | `0x126434` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417032` | Traduit/conservé, vérifié ROM | `0x1251d8`, `0x8c10b3` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417052` | Traduit/conservé, vérifié ROM | `0x12513c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417075` | Traduit/conservé, vérifié ROM | `0x125150` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417094` | Traduit/conservé, vérifié ROM | `0x261f00` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4170b9` | Exception | Aucun | Préfixe de padding sans pointeur ; la chaîne utile suivante possède ses pointeurs propres et est traduite séparément. |
| `0x4170bc` | Traduit/conservé, vérifié ROM | `0x124428`, `0x261f0c`, `0x45a7f0`, `0x45a7f4`, `0x820e28`, `0x820e2c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4170de` | Exception | Aucun | Préfixe de padding sans pointeur ; la chaîne utile suivante possède ses pointeurs propres et est traduite séparément. |
| `0x4170e0` | Traduit/conservé, vérifié ROM | `0x12447c`, `0x261f10`, `0x45a7fc`, `0x820e34` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4170fc` | Traduit/conservé, vérifié ROM | `0x261f14`, `0x45a7f8`, `0x820e30` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41712d` | Exception | Aucun | Préfixe de padding sans pointeur ; la chaîne utile suivante possède ses pointeurs propres et est traduite séparément. |
| `0x417130` | Traduit/conservé, vérifié ROM | `0x45a800`, `0x820e38` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417161` | Exception | Aucun | Préfixe de padding sans pointeur ; la chaîne utile suivante possède ses pointeurs propres et est traduite séparément. |
| `0x417164` | Traduit/conservé, vérifié ROM | `0x45a804`, `0x45a808`, `0x820e3c`, `0x820e40` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41718b` | Exception | Aucun | Préfixe de padding sans pointeur ; la chaîne utile suivante possède ses pointeurs propres et est traduite séparément. |
| `0x41718c` | Traduit/conservé, vérifié ROM | `0x45a7e8`, `0x820e20` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4171c9` | Exception | Aucun | Préfixe de padding sans pointeur ; la chaîne utile suivante possède ses pointeurs propres et est traduite séparément. |
| `0x4171cc` | Traduit/conservé, vérifié ROM | `0x45a7ec`, `0x820e24` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4171df` | Traduit/conservé, vérifié ROM | `0x45a2e8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4171f1` | Traduit/conservé, vérifié ROM | `0x45a2f4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417200` | Traduit/conservé, vérifié ROM | `0x45a2f8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417215` | Traduit/conservé, vérifié ROM | `0x45a2fc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41722b` | Traduit/conservé, vérifié ROM | `0x45a300` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417242` | Traduit/conservé, vérifié ROM | `0x45a340` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417258` | Traduit/conservé, vérifié ROM | `0x45a304` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417270` | Traduit/conservé, vérifié ROM | `0x45a308` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417281` | Traduit/conservé, vérifié ROM | `0x45a30c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417299` | Traduit/conservé, vérifié ROM | `0x45a31c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4172ae` | Traduit/conservé, vérifié ROM | `0x45a344` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4172c2` | Traduit/conservé, vérifié ROM | `0x45a348` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4172d5` | Traduit/conservé, vérifié ROM | `0x45a34c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4172eb` | Traduit/conservé, vérifié ROM | `0x45a320` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417301` | Traduit/conservé, vérifié ROM | `0x45a324` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417313` | Traduit/conservé, vérifié ROM | `0x45a328` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417322` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417337` | Traduit/conservé, vérifié ROM | `0x45a334` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41734d` | Traduit/conservé, vérifié ROM | `0x45a338` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41735b` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; préfixe/suffixe interne sans consommateur autonome. |
| `0x417361` | Traduit/conservé, vérifié ROM | `0x45a310` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41736b` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; préfixe/suffixe interne sans consommateur autonome. |
| `0x41737f` | Traduit/conservé, vérifié ROM | `0x45a350` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417396` | Traduit/conservé, vérifié ROM | `0x45a2ec` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4173b0` | Traduit/conservé, vérifié ROM | `0x45a2f0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4173cc` | Traduit/conservé, vérifié ROM | `0x45a330` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4173e4` | Traduit/conservé, vérifié ROM | `0x45a314` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4173f9` | Traduit/conservé, vérifié ROM | `0x45a318` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417411` | Traduit/conservé, vérifié ROM | `0x45a354` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417419` | Traduit/conservé, vérifié ROM | `0x45a358` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41741e` | Traduit/conservé, vérifié ROM | `0x45a35c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417424` | Traduit/conservé, vérifié ROM | `0x45a360` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41742b` | Traduit/conservé, vérifié ROM | `0x45a364` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417431` | Traduit/conservé, vérifié ROM | `0x45a368` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417436` | Traduit/conservé, vérifié ROM | `0x45a36c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41743f` | Traduit/conservé, vérifié ROM | `0x45a370` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417445` | Traduit/conservé, vérifié ROM | `0x45a374` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41744f` | Traduit/conservé, vérifié ROM | `0x45a378` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417457` | Traduit/conservé, vérifié ROM | `0x12210c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417494` | Traduit/conservé, vérifié ROM | `0x120dd8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417533` | Traduit/conservé, vérifié ROM | `0x8209e4`, `0xa6c96c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417548` | Traduit/conservé, vérifié ROM | `0x45a384`, `0x8209e8`, `0xa6c970` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41755d` | Traduit/conservé, vérifié ROM | `0x45a38c`, `0x8209f0`, `0xa6c978` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41756e` | Traduit/conservé, vérifié ROM | `0x45a388`, `0x8209ec`, `0xa6c974` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417583` | Traduit/conservé, vérifié ROM | `0x8209e0`, `0xa6c968` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417596` | Traduit/conservé, vérifié ROM | `0x45a390`, `0x8209f4`, `0xa6c97c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4175ae` | Traduit/conservé, vérifié ROM | `0x45a394`, `0x8209f8`, `0xa6c980` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4175cc` | Traduit/conservé, vérifié ROM | `0x45a39c`, `0x820a00`, `0xa6c988` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4175de` | Traduit/conservé, vérifié ROM | `0x45a3a8`, `0x820a0c`, `0xa6c994` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4175f1` | Traduit/conservé, vérifié ROM | `0x45a3a0`, `0x45a3a4`, `0x820a04`, `0x820a08`, `0xa6c98c`, `0xa6c990` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4175fb` | Traduit/conservé, vérifié ROM | `0x45a398`, `0x8209fc`, `0xa6c984` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417615` | Traduit/conservé, vérifié ROM | `0x124744` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417640` | Traduit/conservé, vérifié ROM | `0x1246ec` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417674` | Traduit/conservé, vérifié ROM | `0x125184` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41767b` | Traduit/conservé, vérifié ROM | `0x125194` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41768d` | Traduit/conservé, vérifié ROM | `0x1251a4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417696` | Traduit/conservé, vérifié ROM | `0x120a4c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4176b8` | Traduit/conservé, vérifié ROM | `0x120a84` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4176cf` | Traduit/conservé, vérifié ROM | `0x11fe64` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4176e2` | Traduit/conservé, vérifié ROM | `0x4021f8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4176f1` | Traduit/conservé, vérifié ROM | `0x4021e8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4176fe` | Traduit/conservé, vérifié ROM | `0xebf34`, `0x4021f0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417706` | Traduit/conservé, vérifié ROM | `0x402210` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417713` | Traduit/conservé, vérifié ROM | `0x402208` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41772a` | Traduit/conservé, vérifié ROM | `0x4021e0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417741` | Traduit/conservé, vérifié ROM | `0x4021dc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417774` | Traduit/conservé, vérifié ROM | `0xebca4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41778a` | Traduit/conservé, vérifié ROM | `0x1eba79c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4177ac` | Traduit/conservé, vérifié ROM | `0x10e668` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4177c5` | Traduit/conservé, vérifié ROM | `0x10e4b0`, `0x1eba794` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4177d8` | Traduit/conservé, vérifié ROM | `0x402228` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4177dd` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x4177e9` | Traduit/conservé, vérifié ROM | `0x402238` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4177ee` | Traduit/conservé, vérifié ROM | `0xeb938`, `0xeb9b0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417806` | Traduit/conservé, vérifié ROM | `0xec08c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417830` | Traduit/conservé, vérifié ROM | `0xec2f4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417858` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x41786b` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x4178a7` | Traduit/conservé, vérifié ROM | `0x10db58` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178b5` | Traduit/conservé, vérifié ROM | `0x453f74` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178be` | Traduit/conservé, vérifié ROM | `0x10da18` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178d0` | Traduit/conservé, vérifié ROM | `0x113444` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178da` | Traduit/conservé, vérifié ROM | `0x113458` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178e6` | Traduit/conservé, vérifié ROM | `0x3dfe58`, `0x3dfe78`, `0x3dfe98` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178eb` | Traduit/conservé, vérifié ROM | `0x3dfd90`, `0x3dfdb8`, `0x3dfde0`, `0x3dfe00` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178f0` | Traduit/conservé, vérifié ROM | `0x3dfd80`, `0x3dfdb0`, `0x3dfdc8`, `0x3dfdf8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4178fd` | Traduit/conservé, vérifié ROM | `0x3dfda0`, `0x3dfdd0`, `0x3dfde8`, `0x3dfe08` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417907` | Traduit/conservé, vérifié ROM | `0x3dfd88`, `0x3dfd98`, `0x3dfda8`, `0x3dfdc0`, `0x3dfdd8`, `0x3dfdf0`, `0x3dfe10` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41790c` | Traduit/conservé, vérifié ROM | `0x3dfe20` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417910` | Traduit/conservé, vérifié ROM | `0x3dfe28` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417914` | Traduit/conservé, vérifié ROM | `0x3dfe18` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417918` | Traduit/conservé, vérifié ROM | `0x3dfe30` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41791c` | Traduit/conservé, vérifié ROM | `0x3dfe38` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417920` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417926` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417929` | Traduit/conservé, vérifié ROM | `0x3e0260`, `0x3f5c98` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417938` | Traduit/conservé, vérifié ROM | `0x12a514`, `0x155858`, `0x155914`, `0x3dfd50`, `0x3dfe48`, `0x3dfe88` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41793c` | Traduit/conservé, vérifié ROM | `0x12a518`, `0x15585c`, `0x155918`, `0x3dfd58`, `0x3dfe50`, `0x3dfe90` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417944` | Traduit/conservé, vérifié ROM | `0x3dfe60` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417952` | Traduit/conservé, vérifié ROM | `0x3dfe68` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417960` | Traduit/conservé, vérifié ROM | `0x3dfe70` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41796d` | Traduit/conservé, vérifié ROM | `0x3dfea0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41797f` | Traduit/conservé, vérifié ROM | `0x3dfea8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417984` | Traduit/conservé, vérifié ROM | `0x3dff30` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x41799a` | Traduit/conservé, vérifié ROM | `0x3dff38` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4179ad` | Traduit/conservé, vérifié ROM | `0x3dff40` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4179c0` | Traduit/conservé, vérifié ROM | `0x3dffb0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4179d6` | Traduit/conservé, vérifié ROM | `0x3dffb8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4179ed` | Traduit/conservé, vérifié ROM | `0x3dffc8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x4179f7` | Traduit/conservé, vérifié ROM | `0x3dffd0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a02` | Traduit/conservé, vérifié ROM | `0x3e00c0`, `0x3e00f0`, `0x3e0128`, `0x3e0168` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417a0c` | Traduit/conservé, vérifié ROM | `0x3e00d8`, `0x3e00f8`, `0x3e0148`, `0x3e0170` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417a19` | Traduit/conservé, vérifié ROM | `0x3e0110`, `0x3e0130`, `0x3e0150`, `0x3e0178` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417a24` | Traduit/conservé, vérifié ROM | `0x3e00b0`, `0x3e00c8`, `0x3e00e0`, `0x3e0100`, `0x3e0118`, `0x3e0138`, `0x3e0158`, `0x3e0180` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417a37` | Traduit/conservé, vérifié ROM | `0x3dffd8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a3d` | Traduit/conservé, vérifié ROM | `0x3dffe0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a42` | Traduit/conservé, vérifié ROM | `0x3dff50` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a58` | Traduit/conservé, vérifié ROM | `0x3dff58` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a6e` | Traduit/conservé, vérifié ROM | `0x3dff60` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a84` | Traduit/conservé, vérifié ROM | `0x3dff68` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417a9a` | Traduit/conservé, vérifié ROM | `0x3dff70` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ab0` | Traduit/conservé, vérifié ROM | `0x3e0008` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ab3` | Traduit/conservé, vérifié ROM | `0x3e0000` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ab6` | Traduit/conservé, vérifié ROM | `0x3dfff8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ab9` | Traduit/conservé, vérifié ROM | `0x3dfff0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417abc` | Traduit/conservé, vérifié ROM | `0x3dffe8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417abf` | Traduit/conservé, vérifié ROM | `0x3e06b8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ac4` | Traduit/conservé, vérifié ROM | `0x3e06bc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417acb` | Traduit/conservé, vérifié ROM | `0x3e06c0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ad0` | Traduit/conservé, vérifié ROM | `0x3e06c4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ad6` | Traduit/conservé, vérifié ROM | `0x3e06c8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417adc` | Traduit/conservé, vérifié ROM | `0x3dfd60` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ae3` | Traduit/conservé, vérifié ROM | `0x3dfd68` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ae9` | Traduit/conservé, vérifié ROM | `0x3dfd70` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417aee` | Traduit/conservé, vérifié ROM | `0x3dfd78` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417af4` | Traduit/conservé, vérifié ROM | `0x3e06cc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417af9` | Traduit/conservé, vérifié ROM | `0x3e06d0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b00` | Traduit/conservé, vérifié ROM | `0x3e06d4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b05` | Traduit/conservé, vérifié ROM | `0x3e06d8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b0b` | Traduit/conservé, vérifié ROM | `0x3e06dc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b11` | Traduit/conservé, vérifié ROM | `0x3e06e0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b17` | Traduit/conservé, vérifié ROM | `0x3e06e4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b21` | Traduit/conservé, vérifié ROM | `0x3e06e8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b2c` | Traduit/conservé, vérifié ROM | `0x3e06ec` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b36` | Traduit/conservé, vérifié ROM | `0x3e06f0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417b3e` | Traduit/conservé, vérifié ROM | `0x3e06f4` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b4b` | Traduit/conservé, vérifié ROM | `0x3e06f8` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b58` | Traduit/conservé, vérifié ROM | `0x3e06fc` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b65` | Traduit/conservé, vérifié ROM | `0x3e0700` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b72` | Traduit/conservé, vérifié ROM | `0x3e0704` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b7c` | Traduit/conservé, vérifié ROM | `0x3e0708` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b87` | Traduit/conservé, vérifié ROM | `0x3e070c` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b94` | Traduit/conservé, vérifié ROM | `0x3e0710` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417b9f` | Traduit/conservé, vérifié ROM | `0x9d248`, `0x1ec3f8c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417bac` | Traduit/conservé, vérifié ROM | `0x9d1e0`, `0x1ec3f70` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417bb6` | Traduit/conservé, vérifié ROM | `0x9d11c`, `0x9d250` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417bbe` | Traduit/conservé, vérifié ROM | `0x9d12c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417bcb` | Traduit/conservé, vérifié ROM | `0x9d130`, `0x9d1d8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417bd3` | Traduit/conservé, vérifié ROM | `0x9d128`, `0x9d1d4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417be2` | Traduit/conservé, vérifié ROM | `0x3e0190` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417be8` | Traduit/conservé, vérifié ROM | `0x3e0198` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417bf0` | Traduit/conservé, vérifié ROM | `0x3e01a0` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417bf8` | Traduit/conservé, vérifié ROM | `0x3e01a8` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417c01` | Traduit/conservé, vérifié ROM | `0x3e01b0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c0f` | Traduit/conservé, vérifié ROM | `0x3e0018`, `0x3e0038`, `0x3e0060`, `0x3e0090` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417c1b` | Traduit/conservé, vérifié ROM | `0x3e0028`, `0x3e0040`, `0x3e0078`, `0x3e0098` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417c24` | Traduit/conservé, vérifié ROM | `0x3e0050`, `0x3e0068`, `0x3e0080`, `0x3e00a0` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417c2d` | Traduit/conservé, vérifié ROM | `0xd06cc`, `0xd07c4`, `0x3e0714` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c33` | Traduit/conservé, vérifié ROM | `0x3e01b8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c4b` | Traduit/conservé, vérifié ROM | `0x3e01c0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c55` | Traduit/conservé, vérifié ROM | `0x3e01c8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c6a` | Traduit/conservé, vérifié ROM | `0x3e01d0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c83` | Traduit/conservé, vérifié ROM | `0x3e01d8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417c9d` | Traduit/conservé, vérifié ROM | `0x3e01e0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417cb7` | Traduit/conservé, vérifié ROM | `0x3e01e8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417cd1` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417ce6` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417cff` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417d18` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417d32` | Exception | Aucun | Aucun pointeur littéral dans la ROM EN ; ancien texte isolé sans consommateur dans les tables de menus. |
| `0x417d4c` | Traduit/conservé, vérifié ROM | `0x3dff78`, `0x3dffa8`, `0x3e01f0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417d56` | Traduit/conservé, vérifié ROM | `0x3dfed0`, `0x3dff00` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417d63` | Traduit/conservé, vérifié ROM | `0x3dfee0`, `0x3dff18` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417d6f` | Traduit/conservé, vérifié ROM | `0x3dfef0`, `0x3dff08`, `0x3dff20` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417d79` | Traduit/conservé, vérifié ROM | `0x3e01f8`, `0x3e02b0`, `0x3e02e8`, `0x3e0328`, `0x3e0350` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417d86` | Traduit/conservé, vérifié ROM | `0x3e0200` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417d90` | Traduit/conservé, vérifié ROM | `0x3e0210` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417da0` | Traduit/conservé, vérifié ROM | `0x3e0218` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417da9` | Traduit/conservé, vérifié ROM | `0x3e0718` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417db6` | Traduit/conservé, vérifié ROM | `0x3e071c` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417dc7` | Traduit/conservé, vérifié ROM | `0x3e0720` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417dd9` | Traduit/conservé, vérifié ROM | `0x3e0724` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417de1` | Traduit/conservé, vérifié ROM | `0x3e0728` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ded` | Traduit/conservé, vérifié ROM | `0x9d8b8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417df3` | Traduit/conservé, vérifié ROM | `0x3e0280`, `0x3e0298`, `0x3e03c0`, `0x3e0408`, `0x3e0428`, `0x3e17e4` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417dfe` | Traduit/conservé, vérifié ROM | `0x3e0268`, `0x3e02a0`, `0x3e03c8`, `0x3e03e8`, `0x3e0430`, `0x3e17e8` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e09` | Traduit/conservé, vérifié ROM | `0x3e0270`, `0x3e0288`, `0x3e03d0`, `0x3e03f0`, `0x3e0410`, `0x3e17ec` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e16` | Traduit/conservé, vérifié ROM | `0x3e17f0` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e22` | Traduit/conservé, vérifié ROM | `0x3e17f4` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e2e` | Traduit/conservé, vérifié ROM | `0x3e17f8` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e39` | Traduit/conservé, vérifié ROM | `0x3e17fc` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e46` | Traduit/conservé, vérifié ROM | `0x3e03e0`, `0x3e0400`, `0x3e0420`, `0x3e0440`, `0x3e17e0` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417e50` | Traduit/conservé, vérifié ROM | `0x3e02b8`, `0x3e02f0`, `0x3e0330`, `0x3e0358` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417e5a` | Traduit/conservé, vérifié ROM | `0x3e02c0`, `0x3e0340` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417e72` | Traduit/conservé, vérifié ROM | `0x3e0300` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417e7f` | Traduit/conservé, vérifié ROM | `0x3e0308` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417e94` | Traduit/conservé, vérifié ROM | `0x3e0318` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ea4` | Traduit/conservé, vérifié ROM | `0x3e0320` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417eb3` | Traduit/conservé, vérifié ROM | `0x3e0370`, `0x3e0388`, `0x3e03a0` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417ec1` | Traduit/conservé, vérifié ROM | `0x3e0378`, `0x3e03a8` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417ecc` | Traduit/conservé, vérifié ROM | `0x3e0390`, `0x3e03b0` | Nom propre ou nom d’objet conservé selon F-759. |
| `0x417ed9` | Traduit/conservé, vérifié ROM | `0x3dff88` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417ef7` | Traduit/conservé, vérifié ROM | `0x3dff90` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f11` | Traduit/conservé, vérifié ROM | `0x3dff98` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f2f` | Traduit/conservé, vérifié ROM | `0x3dffa0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f4d` | Traduit/conservé, vérifié ROM | `0x3dff80` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f69` | Traduit/conservé, vérifié ROM | `0x3e0470` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f77` | Traduit/conservé, vérifié ROM | `0x3e0468` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f82` | Traduit/conservé, vérifié ROM | `0x3e0480`, `0x3fe9c4` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f89` | Traduit/conservé, vérifié ROM | `0x3e0488`, `0x3fe9c8` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f90` | Traduit/conservé, vérifié ROM | `0x3e0490`, `0x3fe9cc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417f99` | Traduit/conservé, vérifié ROM | `0x3e0498`, `0x3fe9d0` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417fbb` | Traduit/conservé, vérifié ROM | `0xca6fc` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417fc3` | Traduit/conservé, vérifié ROM | `0xca710` | Traduction PT-BR ; commandes et ruptures conservées. |
| `0x417fcc` | Traduit/conservé, vérifié ROM | `0xca748` | Traduction PT-BR ; commandes et ruptures conservées. |
