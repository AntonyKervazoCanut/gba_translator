# PT-BR — PT-09 : phrases faciles, zones et combat (F-768)

## Périmètre et décisions

Les 281 offsets explicites de `translation_batches.json` sont tous comptabilisés. Les bornes ne sont pas utilisées comme liste implicite. F-758 et F-759 sont intégrés ; aucune traduction existante n’est supprimée ni modifiée.

- 88 mots de phrases faciles, dans des structures de 12 octets `{pointeur, tri, disponibilité}` ; les deux derniers champs restent inchangés.
- 54 noms de lieux conservés exactement selon la politique F-759 des noms propres non attestés. Le mot générique `BATTLE TOWER` dans les phrases faciles est traduit ; le nom de zone `Battle Tower` reste anglais.
- 124 templates/tampons de combat : variables FD explicites, FC avec leurs paramètres, FE/FA/FB dans le même ordre. Quatre entrées ne contiennent qu’un tampon FD et sont conservées sans prose à traduire.
- 15 exceptions : un ancien doublon de Route 4, quatre suffixes internes sans pointeur et dix messages historiques sans référent, remplacés par des messages CFRU. Les remplacements sont hors PT-09 et ne sont pas traduits dans ce ticket.

La comparaison française est stockée pour chaque offset dans `languages/pt/data/pt09_audit.json`. Les contrôles réels proviennent des octets EN : plusieurs représentations du corpus anglais décodent à tort les paramètres FD en lettres accentuées. Par exemple le préfixe `FD1D` des rappels est conservé même lorsqu’il manque dans la traduction FR.

`Cancelar`, `movimento`, `PS`, `Nocauteado`, `Terrestre` et les noms anglais de mouvements non attestés suivent le glossaire. L’abréviation de Defesa Especial est `Def. Esp.`. Le tampon de bonus Exp. commence par `<0x00>` : l’espace est ainsi conservé malgré le trim des lecteurs du combined.

## Injection et budgets

Aucune entrée active n’appartient aux régions de tables fixes de `in_fixed_table`. Les mots, zones et templates disposent de pointeurs relocalisables ; aucun patch de table fixe n’est nécessaire. Tous les consommateurs vivants sont vérifiés, y compris les pointeurs de scripts non alignés vers `0x3fb6d3`. Le motif `0x54482e` qui ressemble à un pointeur de `0x3ecab7` est graphique et doit rester intact.

Budget source : mots de phrases faciles ≤ 102 px, autres lignes ≤ 192 px, octets encodés strictement valides, aucun terminateur interne. Les tailles exactes et les largeurs sont enregistrées par offset dans le JSON. Les tests ROM contrôlent également les cinq tables de largeur finales avec des variables représentatives (dont `Foe CHARMANDER`, `Intimidate`), ainsi que la concaténation du bonus Exp.

La passe finale `languages/pt/patches/batch_09.py` réutilise `StructuredTextPatch` sans modifier le code partagé. Elle contrôle 36 entrées / 40 consommateurs et reloge 35 chaînes dans le build final. Elle préserve les ruptures choisies face au rebalancement générique et force le terminateur Pokémon du tampon `FD2F` à `0x3fb262` : l’extraction le classe à tort ASCII (`length=2`, `original_length=4`), produisant `00` au lieu de `FF`. Les préimages, contrôles, tailles et pointeurs sont validés atomiquement ; aucune cellule voisine n’est écrasée et une seconde application ne modifie rien.

## Vérification

- `make build-pt` réussi après rebase sur les lots PT-05/PT-07 et ES-003 ; les conflits d’ajout ont conservé toutes les traductions et protections concurrentes.
- `python3 -m pytest tests/unit/pt tests/e2e/pt tests/unit/test_translation_integrity.py -m 'not emulator' -q` : **1 926 réussis**, sans échec ni skip. Les 284 consommateurs PT-09 livrent les octets exacts ; les cinq polices finales respectent les budgets testés, les champs Easy Chat restent inchangés, les préimages invalides sont rejetées et la passe finale est idempotente.
- Contrôle TypeScript des deux nouveaux fichiers et lint Ruff ciblé réussis après rebase.
- Playwright hors écran, assertions OCR sur EXPECTATIVA, Cancelar, Bellin Town et le template de combat avec Foe CHARMANDER : capture finale jointe au ticket F-768. Les textes sont lus via les pointeurs de la ROM livrée ; seul le tampon du template de combat est résolu en nom représentatif dans la copie temporaire.
- Les hooks actifs ont exécuté la suite rapide Python, les 68 tests Vitest et les builds FR/IT/DE. Aucun fichier partagé, aucune ROM ni capture ajoutés au commit, aucun push ni pipeline distant.
- Après contrôle strict des 238 consommateurs PT-06, 97 cibles de son bilan JSON/Markdown ont été actualisées : métadonnées d’allocation uniquement, sans changement de traduction hors PT-09.

ROM anglaise SHA256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
ROM PT vérifiée SHA256 : `20cefebf41eba1b9df74f85f221904a7776c1508b17c15dd7d44db5a9069285b`.

## Non vérifié

La sonde mGBA prouve le rendu typographique des exemples ; elle ne constitue pas un parcours naturel de tous les menus, de toutes les situations de combat ou du jeu complet. Cette certification globale relève de T-848. Le test ignoré par la configuration de la suite rapide historique n’est pas présenté comme réussi.

## Bilan offset par offset

Les sites sont les adresses des pointeurs dans la ROM EN ; les cibles sont leurs valeurs résolues dans la ROM PT finale. Une cible conservée à l’adresse EN reste vérifiée octet par octet.

| Offset | Résultat | Pointeurs source → cibles PT | Décision / valeur PT |
|---|---|---|---|
| `0x3ec2ae` | traduit/vérifié | `0x3ec3d4` → `0x3ec2ae` | `SÓLIDO` |
| `0x3ec2b9` | traduit/vérifié | `0x3ec3e0` → `0xe58c6c` | `FAMINTO` |
| `0x3ec2c0` | traduit/vérifié | `0x3ec3ec` → `0xe58d5d` | `APERTADO` |
| `0x3ec2c6` | traduit/vérifié | `0x3ec3f8` → `0x3ec2c6` | `CÓCEGAS` |
| `0x3ec2cf` | traduit/vérifié | `0x3ec404` → `0x3ec2cf` | `GIRANDO` |
| `0x3ec2d8` | traduit/vérifié | `0x3ec410` → `0xe69583` | `EM ESPIRAL` |
| `0x3ec2e2` | traduit/vérifié | `0x3ec41c` → `0xe58d04` | `SEDENTO` |
| `0x3ec2ea` | traduit/vérifié | `0x3ec428` → `0x3ec2ea` | `À TOA` |
| `0x3ec2f2` | traduit/vérifié | `0x3ec434` → `0xd10f02` | `SEDOSO` |
| `0x3ec2f8` | traduit/vérifié | `0x3ec440` → `0xe696ca` | `TRISTEMENTE` |
| `0x3ec2fe` | traduit/vérifié | `0x3ec44c` → `0xe69837` | `SEM ESPERANÇA` |
| `0x3ec307` | traduit/vérifié | `0x3ec458` → `0x3ec307` | `INÚTIL` |
| `0x3ec30f` | traduit/vérifié | `0x3ec464` → `0x3ec30f` | `BABANDO` |
| `0x3ec318` | traduit/vérifié | `0x3ec470` → `0xe6958e` | `EMPOLGANTE` |
| `0x3ec321` | traduit/vérifié | `0x3ec47c` → `0xd10e5a` | `GROSSO` |
| `0x3ec327` | traduit/vérifié | `0x3ec488` → `0x3ec327` | `LISO` |
| `0x3ec32e` | traduit/vérifié | `0x3ec494` → `0xe58d3c` | `VISCOSO` |
| `0x3ec334` | traduit/vérifié | `0x3ec4a0` → `0xd10c41` | `FINO` |
| `0x3ec339` | traduit/vérifié | `0x3ec4ac` → `0xe58cec` | `QUEBRAR` |
| `0x3ec33f` | traduit/vérifié | `0x3ec4b8` → `0x3ec33f` | `VORAZ` |
| `0x3ec349` | traduit/vérifié | `0x3ec4c4` → `0xe58e23` | `ESPALHAR` |
| `0x3ec351` | traduit/vérifié | `0x3ec4d0` → `0xe58e74` | `INCRÍVEL` |
| `0x3ec359` | traduit/vérifié | `0x3ec4dc` → `0xd10cee` | `FRACO` |
| `0x3ec35f` | traduit/vérifié | `0x3ec4e8` → `0x3ec35f` | `BAMBO` |
| `0x3ec366` | traduit/vérifié | `0x3ec4f4` → `0xe58d24` | `TRÊMULO` |
| `0x3ec36c` | traduit/vérifié | `0x3ec500` → `0xe58cf4` | `RASGADO` |
| `0x3ec373` | traduit/vérifié | `0x3ec50c` → `0xe694e2` | `TRITURADO` |
| `0x3ec37c` | traduit/vérifié | `0x3ec518` → `0xe6952b` | `AUMENTANDO` |
| `0x3ec38b` | traduit/vérifié | `0x3ec530` → `0xe58fea` | `DESTRUÍDO` |
| `0x3ec395` | traduit/vérifié | `0x3ec53c` → `0xd10f53` | `ARDENTE` |
| `0x3ec39b` | traduit/vérifié | `0x3ec548` → `0x3ec39b` | `APAIXONADO` |
| `0x3ec3a7` | traduit/vérifié | `0x3ec554` → `0xe695ba` | `FELIZMENTE` |
| `0x3ec3af` | traduit/vérifié | `0x3ec560` → `0x3ec3af` | `EXPECTATIVA` |
| `0x3ec573` | traduit/vérifié | `0x3ec650` → `0xe58c4c` | `EVENTOS` |
| `0x3ec57a` | traduit/vérifié | `0x3ec65c` → `0x3ec57a` | `CASEIRO` |
| `0x3ec587` | traduit/vérifié | `0x3ec668` → `0xd10cf4` | `FRUTA` |
| `0x3ec58d` | traduit/vérifié | `0x3ec674` → `0xe58da5` | `CONCURSO` |
| `0x3ec598` | traduit/vérifié | `0x3ec68c` → `0x3ec598` | `JUIZ` |
| `0x3ec59e` | traduit/vérifié | `0x3ec698` → `0x3ec59e` | `SUPER` |
| `0x3ec5a4` | traduit/vérifié | `0x3ec6a4` → `0xd10d5a` | `PALCO` |
| `0x3ec5aa` | traduit/vérifié | `0x3ec6b0` → `0xe69749` | `HALL DA FAMA` |
| `0x3ec5b7` | traduit/vérifié | `0x3ec6bc` → `0x3ec5b7` | `EVOLUÇÃO` |
| `0x3ec5c1` | traduit/vérifié | `0x3ec6c8` → `0xd10d00` | `HIPER` |
| `0x3ec5c7` | traduit/vérifié | `0x3ec6d4` → `0x904b96` | `TORRE DE BATALHA` |
| `0x3ec5d4` | traduit/vérifié | `0x3ec6e0` → `0xe58c7c` | `LÍDERES` |
| `0x3ec5dc` | traduit/vérifié | `0x3ec6ec` → `0x904b12` | `SALA DE BATALHA` |
| `0x3ec5e8` | traduit/vérifié | `0x3ec6f8` → `0xd10ea0` | `OCULTO` |
| `0x3ec5ef` | traduit/vérifié | `0x3ec704` → `0xe696fb` | `BASE SECRETA` |
| `0x3ec5fb` | traduit/vérifié | `0x3ec710` → `0xe58e7d` | `MISTURAR` |
| `0x3ec607` | traduit/vérifié | `0x3ec728` → `0xd10e92` | `MESTRE` |
| `0x3ec60e` | traduit/vérifié | `0x3ec734` → `0xe58ce4` | `POSIÇÃO` |
| `0x3ec613` | traduit/vérifié | `0x3ec740` → `0x3ec613` | `FITA` |
| `0x3ec61a` | traduit/vérifié | `0x3ec74c` → `0xd10fe3` | `ESMAGAR` |
| `0x3ec620` | traduit/vérifié | `0x3ec758` → `0xd10e37` | `DIRETO` |
| `0x3ec627` | traduit/vérifié | `0x3ec764` → `0xd10d96` | `TORRE` |
| `0x3ec62d` | traduit/vérifié | `0x3ec770` → `0xd10da2` | `UNIÃO` |
| `0x3ec633` | traduit/vérifié | `0x3ec77c` → `0xd10c73` | `SALA` |
| `0x3ec638` | traduit/vérifié | `0x3ec788` → `0x3ec638` | `SEM FIO` |
| `0x3eca63` | traduit/vérifié | `0x3ecb5c` → `0xe697b1` | `SIM, SENHOR!` |
| `0x3eca6d` | traduit/vérifié | `0x3ecb68` → `0x3eca6d` | `VANGUARDA` |
| `0x3eca79` | traduit/vérifié | `0x3ecb74` → `0x3eca79` | `CASAL` |
| `0x3eca80` | traduit/vérifié | `0x3ecb80` → `0x904aa4` | `MUITO OBRIGADO` |
| `0x3eca8d` | traduit/vérifié | `0x3ecb8c` → `0x3eca8d` | `IUPI!` |
| `0x3eca95` | traduit/vérifié | `0x3ecb98` → `0x3eca95` | `MEGA` |
| `0x3eca9a` | traduit/vérifié | `0x3ecba4` → `0xe6981b` | `NOCAUTE EM 1!` |
| `0x3ecaa4` | traduit/vérifié | `0x3ecbb0` → `0xd10fb3` | `DESTINO` |
| `0x3ecaac` | traduit/vérifié | `0x3ecbbc` → `0xe58db7` | `Cancelar` |
| `0x3ecab7` | traduit/vérifié | `0x3ecbd4` → `0xd10f3b` | `ACHATAR` |
| `0x3ecabf` | traduit/vérifié | `0x3ecbe0` → `0xe58fd6` | `BRINCANDO` |
| `0x3ecac7` | traduit/vérifié | `0x3ecbec` → `0xe58ee0` | `PERDEDOR` |
| `0x3ecacd` | traduit/vérifié | `0x3ecbf8` → `0xe58ee9` | `PERDENDO` |
| `0x3ecad4` | traduit/vérifié | `0x3ecc04` → `0x3ecad4` | `AGITADO` |
| `0x3ecade` | traduit/vérifié | `0x3ecc10` → `0xe6946a` | `NA MODA E` |
| `0x3ecae6` | traduit/vérifié | `0x3ecc1c` → `0xe58cfc` | `SACUDIR` |
| `0x3ecaec` | traduit/vérifié | `0x3ecc28` → `0xe58f67` | `SUSPEITO` |
| `0x3ecaf2` | traduit/vérifié | `0x3ecc34` → `0xd10f43` | `ANIMADO` |
| `0x3ecaf9` | traduit/vérifié | `0x3ecc40` → `0xe58c8c` | `MODERNO` |
| `0x3ecb00` | traduit/vérifié | `0x3ecc4c` → `0xe58d6f` | `ATÉ MAIS` |
| `0x3ecb09` | traduit/vérifié | `0x3ecc58` → `0x3ecb09` | `BUM` |
| `0x3ecb0e` | traduit/vérifié | `0x3ecc64` → `0x3ecb0e` | `NOCAUTE` |
| `0x3ecb17` | traduit/vérifié | `0x3ecc70` → `0xe58e6b` | `INCÔMODO` |
| `0x3ecb1e` | traduit/vérifié | `0x3ecc7c` → `0xe58f94` | `VENCEDOR` |
| `0x3ecb25` | traduit/vérifié | `0x3ecc88` → `0xd10cd6` | `FEBRE` |
| `0x3ecb2b` | traduit/vérifié | `0x3ecc94` → `0xe58fc2` | `ASPIRANTE` |
| `0x3ecb33` | traduit/vérifié | `0x3ecca0` → `0xd10c1e` | `BEBÊ` |
| `0x3ecb38` | traduit/vérifié | `0x3eccac` → `0xd10f93` | `CORAÇÃO` |
| `0x3ecb42` | traduit/vérifié | `0x3eccc4` → `0xd10d0c` | `JOVEM` |
| `0x3ecb48` | traduit/vérifié | `0x3eccd0` → `0x3ecb48` | `FEIO` |
| `0x3eed08` | conservé/vérifié | `0x3f1cb0` → `0x3eed08` | `Bellin Town` |
| `0x3eed22` | conservé/vérifié | `0x3f1cb8` → `0x3eed22` | `Crater Town` |
| `0x3eed67` | conservé/vérifié | `0x3f1ccc` → `0x3eed67` | `Tarmigan Town` |
| `0x3eed77` | conservé/vérifié | `0x3f1cd0` → `0x3eed77` | `INDIGO PLATEAU` |
| `0x3eed93` | conservé/vérifié | `0x3f1cd8` → `0x3eed93` | `Route 4` |
| `0x3eed9b` | conservé/vérifié | `0x3f1cdc` → `0x3eed9b` | `Route 10` |
| `0x3eeda4` | conservé/vérifié | `0x3f1ce0` → `0x3eeda4` | `Route 1` |
| `0x3eedac` | conservé/vérifié | `0x3f1ce4` → `0x3eedac` | `Route 2` |
| `0x3eedb4` | conservé/vérifié | `0x3f1ce8` → `0x3eedb4` | `Route 3` |
| `0x3eedbc` | exception justifiée | `aucun` → `sans objet` | Ancien doublon ROUTE 4 sans pointeur ; nom vivant Route 4 à 0x3eed93, table 0x3f1cd8. |
| `0x3eedc4` | conservé/vérifié | `0x3f1cf0` → `0x3eedc4` | `Route 5` |
| `0x3eedcc` | conservé/vérifié | `0x3f1cf4` → `0x3eedcc` | `Route 6` |
| `0x3eedd4` | conservé/vérifié | `0x3f1cf8` → `0x3eedd4` | `Route 7` |
| `0x3eeddc` | conservé/vérifié | `0x3f1cfc` → `0x3eeddc` | `Route 8` |
| `0x3eede4` | conservé/vérifié | `0x3f1d00` → `0x3eede4` | `Route 9` |
| `0x3eedec` | conservé/vérifié | `0x3f1d04` → `0x3eedec` | `ROUTE 10` |
| `0x3eedf5` | conservé/vérifié | `0x3f1d08` → `0x3eedf5` | `Route 11` |
| `0x3eedfe` | conservé/vérifié | `0x3f1d0c` → `0x3eedfe` | `Route 12` |
| `0x3eee07` | conservé/vérifié | `0x3f1d10` → `0x3eee07` | `Route 13` |
| `0x3eee10` | conservé/vérifié | `0x3f1d14` → `0x3eee10` | `Route 14` |
| `0x3eee19` | conservé/vérifié | `0x3f1d18` → `0x3eee19` | `Route 15` |
| `0x3eee22` | conservé/vérifié | `0x3f1d1c` → `0x3eee22` | `Route 16` |
| `0x3eee2b` | conservé/vérifié | `0x3f1d20` → `0x3eee2b` | `Route 17` |
| `0x3eee34` | conservé/vérifié | `0x3f1d24` → `0x3eee34` | `Route 18` |
| `0x3eee7c` | conservé/vérifié | `0x3f1b40, 0x3f1d44` → `0x3eee7c, 0x3eee7c` | `Grim Woods` |
| `0x3eee9f` | conservé/vérifié | `0x3f1d50` → `0x3eee9f` | `Underground Pass` |
| `0x3eeec1` | conservé/vérifié | `0x3f1b58, 0x3f1d58` → `0x3eeec1, 0x3eeec1` | `Valley Cave` |
| `0x3eeed0` | conservé/vérifié | `0x3f1b64, 0x3f1d5c` → `0x3eeed0, 0x3eeed0` | `Victory Road` |
| `0x3eef12` | conservé/vérifié | `0x3f1d70` → `0x3eef12` | `Pokémon League` |
| `0x3eef2d` | conservé/vérifié | `0x3f1b94, 0x3f1d78` → `0x3eef2d, 0x3eef2d` | `Rift Cave` |
| `0x3eef3d` | conservé/vérifié | `0x3f1ba0, 0x3f1d7c` → `0x3eef3d, 0x3eef3d` | `Vivill Woods` |
| `0x3eef4b` | conservé/vérifié | `0x3f1bac, 0x3f1d80` → `0x3eef4b, 0x3eef4b` | `Icicle Cave` |
| `0x3eef94` | conservé/vérifié | `0x3f1d98` → `0x3eef94` | `Cube Corp.` |
| `0x3eefa0` | conservé/vérifié | `0x3f1d9c` → `0x3eefa0` | `SEVEN ISLAND` |
| `0x3eefad` | conservé/vérifié | `0x3f1da0` → `0x3eefad` | `SIX ISLAND` |
| `0x3eefea` | conservé/vérifié | `0x3f1db4` → `0x3eefea` | `Cave of Being` |
| `0x3ef094` | conservé/vérifié | `0x3f1de4` → `0x3ef094` | `RUIN VALLEY` |
| `0x3ef0ae` | conservé/vérifié | `0x3f1dec` → `0x3ef0ae` | `CANYON ENTRANCE` |
| `0x3ef0be` | conservé/vérifié | `0x3f1df0` → `0x3ef0be` | `SEVAULT CANYON` |
| `0x3ef0cd` | conservé/vérifié | `0x3f1df4` → `0x3ef0cd` | `TANOBY RUINS` |
| `0x3ef0da` | conservé/vérifié | `0x3f1df8` → `0x3ef0da` | `SEVII ISLE 22` |
| `0x3ef0e8` | conservé/vérifié | `0x3f1dfc` → `0x3ef0e8` | `SEVII ISLE 23` |
| `0x3ef0f6` | conservé/vérifié | `0x3f1e00` → `0x3ef0f6` | `SEVII ISLE 24` |
| `0x3ef104` | conservé/vérifié | `0x3f1e04` → `0x3ef104` | `NAVEL ROCK` |
| `0x3ef119` | conservé/vérifié | `0x3f1bd0, 0x3f1e0c` → `0x3ef119, 0x3ef119` | `BERRY FOREST` |
| `0x3ef133` | conservé/vérifié | `0x3f1e14` → `0x3ef133` | `Battle Mine` |
| `0x3ef144` | conservé/vérifié | `0x3f1e18` → `0x3ef144` | `Battle Tower` |
| `0x3ef183` | conservé/vérifié | `0x3f1bf4, 0x3f1e2c` → `0x3ef183, 0x3ef183` | `Autl Woods` |
| `0x3ef193` | conservé/vérifié | `0x3f1e30` → `0x3ef193` | `Cliff Cave` |
| `0x3ef1ae` | conservé/vérifié | `0x3f1e38` → `0x3ef1ae` | `Battleground` |
| `0x3ef1d9` | conservé/vérifié | `0x3f1e44` → `0x3ef1d9` | `S.S. Marine` |
| `0x3ef1e8` | conservé/vérifié | `0x3f1e48` → `0x3ef1e8` | `Ferrothorn Turf` |
| `0x3ef207` | conservé/vérifié | `0x3f1e50` → `0x3ef207` | `Desert Ruins` |
| `0x3ef214` | conservé/vérifié | `0x3f1e54` → `0x3ef214` | `Frozen Tomb` |
| `0x3ef22e` | conservé/vérifié | `0xc4da0, 0x3f1e5c` → `0x3ef22e, 0x3ef22e` | `Dehara Dept.` |
| `0x3fb219` | conservé/vérifié | `0x3fdf3c` → `0xd10c0c` | `<0xFD><0x24>` |
| `0x3fb21c` | conservé/vérifié | `0x3fe4e8` → `0xd10c12` | `<0xFD><0x2E>` |
| `0x3fb21f` | traduit/vérifié | `0x3fe504` → `0x3fb21f` | `<0xFD><0x1D>: <0xFD><0x06>, volte!` |
| `0x3fb232` | conservé/vérifié | `0x3fe508` → `0xd10c0f` | `<0xFD><0x25>` |
| `0x3fb235` | traduit/vérifié | `0x3fe50c` → `0x3fb235` | `<0xFD><0x1D>: <0xFD><0x08>, volte!` |
| `0x3fb248` | traduit/vérifié | `0x3fe510` → `0x16bce4` | `<0xFD><0x1D>: <0xFD><0x06> e\n<0xFD><0x08>, voltem!` |
| `0x3fb262` | conservé/vérifié | `0x3fe4ec` → `0x16bcf9` | `<0xFD><0x2F>` |
| `0x3fb265` | traduit/vérifié | `0x3fdf40` → `0x7a3b5b` | `<0xFD><0x00> ganhou<0xFD><0x01>\n<0xFD><0x34> pontos de Exp.!<0xFB>` |
| `0x3fb283` | traduit/vérifié | `0x3fe434` → `0xe696ee` | `<0x00>um bônus de` |
| `0x3fb284` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb283, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fb28e` | traduit/vérifié | `0x3fdf44` → `0x7b1f93` | `<0xFD><0x00> subiu para\no Nv. <0xFD><0x01>!<0xFC><0x0A><0xFB>` |
| `0x3fb2a4` | traduit/vérifié | `0x3fdf48` → `0x904c45` | `<0xFD><0x00> aprendeu\n<0xFD><0x01>!<0xFC><0x0A><0xFB>` |
| `0x3fb2b6` | traduit/vérifié | `0x3fdf4c` → `0x3fb2b6` | `<0xFD><0x00> tenta aprender\n<0xFD><0x01>.<0xFB>` |
| `0x3fb2d1` | traduit/vérifié | `0x3fdf50` → `0x3fb2d1` | `Mas <0xFD><0x00> só pode ter\nquatro movimentos.<0xFB>` |
| `0x3fb2fc` | traduit/vérifié | `0x3fdf54` → `0x80ebc4` | `Esquecer um movimento\npara aprender <0xFD><0x01>?` |
| `0x3fb31f` | traduit/vérifié | `0x3fdf58` → `0x904bb8` | `<0xFD><0x00> esqueceu\n<0xFD><0x01>.<0xFB>` |
| `0x3fb32e` | traduit/vérifié | `0x3fdf5c` → `0xbe054d` | `<0xFC><0x08><0x20>Parar de aprender\n<0xFD><0x01>?` |
| `0x3fb343` | traduit/vérifié | `0x3fdf60` → `0x16bcfc` | `<0xFD><0x00> não aprendeu\n<0xFD><0x01>.<0xFB>` |
| `0x3fb359` | traduit/vérifié | `0x3fe450` → `0x904d59` | `Usar outro Pokémon?` |
| `0x3fb36b` | traduit/vérifié | `0x3fdf68` → `0x16bd11` | `<0xFD><0x0F> errou\no ataque!` |
| `0x3fb37f` | traduit/vérifié | `0x3fdf6c` → `0x3fb37f` | `<0xFD><0x10>\nse protegeu!` |
| `0x3fb394` | traduit/vérifié | `0x3fdf74` → `0x16bd24` | `<0xFD><0x10> evitou danos\ncom <0xFD><0x19>!` |
| `0x3fb3af` | traduit/vérifié | `0x3fe43c` → `0x80eb75` | `<0xFD><0x10> evita movimentos\nTerrestres com <0xFD><0x19>!` |
| `0x3fb3d3` | traduit/vérifié | `0x3fe470` → `0x3fb3d3` | `<0xFD><0x10> desviou\ndo ataque!` |
| `0x3fb400` | traduit/vérifié | `0x3fdf7c` → `0x904d95` | `<0xFD><0x0F> foi\nnocauteado!<0xFB>` |
| `0x3fb40d` | traduit/vérifié | `0x3fdf80` → `0x904da9` | `<0xFD><0x10> foi\nnocauteado!<0xFB>` |
| `0x3fb41a` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdf84 pointe vers 0xa4c670, pas cet offset. |
| `0x3fb433` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdf88 pointe vers 0xa4c689, pas cet offset. |
| `0x3fb451` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdf8c pointe vers 0xa4c6b3, pas cet offset. |
| `0x3fb484` | exception justifiée | `aucun` → `sans objet` | Ancien message de défaite sans aucun pointeur. Le chemin actuel utilise les cellules 0x3fdf88 → 0xa4c689 (équipe épuisée) et 0x3fdf8c → 0xa4c6b3 (défaite), hors PT-09. |
| `0x3fb4be` | exception justifiée | `aucun` → `sans objet` | Ancien message de défaite sans aucun pointeur. Le chemin actuel utilise les cellules 0x3fdf88 → 0xa4c689 (équipe épuisée) et 0x3fdf8c → 0xa4c6b3 (défaite), hors PT-09. |
| `0x3fb4f7` | exception justifiée | `aucun` → `sans objet` | Ancien message de défaite sans aucun pointeur. Le chemin actuel utilise les cellules 0x3fdf88 → 0xa4c689 (équipe épuisée) et 0x3fdf8c → 0xa4c6b3 (défaite), hors PT-09. |
| `0x3fb508` | traduit/vérifié | `0x3fdf90` → `0x16bd3c` | `<0xFD><0x13> impede a fuga\ncom <0xFD><0x1A>!<0xFB>` |
| `0x3fb525` | traduit/vérifié | `0x3fe354` → `0x904b52` | `Não pode fugir!<0xFB>` |
| `0x3fb534` | traduit/vérifié | `0x3fe4a0` → `0x904c6b` | `<0xFD><0x0F> não pode fugir!` |
| `0x3fb545` | traduit/vérifié | `0x3fdf94` → `0x904c91` | `Acertou <0xFD><0x00> vez(es)!` |
| `0x3fb555` | traduit/vérifié | `0x3fdf98` → `0x904e64` | `<0xFD><0x11> ficou\nadormecido!` |
| `0x3fb565` | traduit/vérifié | `0x3fdf9c` → `0x7b1fe4` | `<0xFD><0x13>, com <0xFD><0x1A>,\nfez <0xFD><0x11> dormir!` |
| `0x3fb57c` | traduit/vérifié | `0x3fdfa0, 0x9fdfe8, 0x9fe1f4` → `0x16bd56, 0x16bd56, 0x16bd56` | `<0xFD><0x10> já está\nadormecido!` |
| `0x3fb592` | traduit/vérifié | `0x3fdfa4` → `0x16bd6d` | `<0xFD><0x0F> já está\nadormecido!` |
| `0x3fb5a8` | traduit/vérifié | `0x3fdfa8` → `0x16bd84` | `<0xFD><0x10>\nnão foi afetado!` |
| `0x3fb5bc` | traduit/vérifié | `0x3fdfac` → `0x904c7e` | `<0xFD><0x11> foi\nenvenenado!` |
| `0x3fb5cd` | traduit/vérifié | `0x3fdfb0` → `0x7b1e50` | `<0xFD><0x13>, com <0xFD><0x1A>,\nenvenenou <0xFD><0x11>!` |
| `0x3fb5e2` | traduit/vérifié | `0x3fdfb4` → `0xbe036a` | `<0xFD><0x0F> sofre\ncom o veneno!` |
| `0x3fb5f8` | traduit/vérifié | `0x3fdfb8, 0x9fe8a0` → `0x3fb5f8, 0x3fb5f8` | `<0xFD><0x10> já está\nenvenenado.` |
| `0x3fb610` | traduit/vérifié | `0x3fdfbc` → `0x7a38e4` | `<0xFD><0x11> foi\ngravemente envenenado!` |
| `0x3fb626` | traduit/vérifié | `0x3fdfc0` → `0x7a384f` | `<0xFD><0x10> teve sua\nenergia drenada!` |
| `0x3fb641` | traduit/vérifié | `0x3fdfc4` → `0x904beb` | `<0xFD><0x11> foi queimado!` |
| `0x3fb650` | traduit/vérifié | `0x3fdfc8` → `0xbe04a0` | `<0xFD><0x13>, com <0xFD><0x1A>,\nqueimou <0xFD><0x11>!` |
| `0x3fb663` | traduit/vérifié | `0x3fdfcc` → `0x7b1fae` | `<0xFD><0x0F> sofre\ncom a queimadura!` |
| `0x3fb67b` | traduit/vérifié | `0x3fe47c, 0x9fe638` → `0x3fb67b, 0x3fb67b` | `<0xFD><0x10> já está\nqueimado.` |
| `0x3fb692` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdfd0 pointe vers 0xa4b23c, pas cet offset. |
| `0x3fb6a7` | traduit/vérifié | `0x3fdfd4` → `0xbe05b1` | `<0xFD><0x13>, com <0xFD><0x1A>,\ncongelou <0xFD><0x11>!` |
| `0x3fb6bf` | traduit/vérifié | `0x3fdfd8` → `0x3fb6bf` | `<0xFD><0x0F> está\ncongelado!` |
| `0x3fb6d3` | traduit/vérifié | `0x8bbe33, 0x90531e` → `0x3fb6d3, 0x3fb6d3` | `<0xFD><0x10> descongelou!` |
| `0x3fb6e5` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdfe0 pointe vers 0xa4b2a5, pas cet offset. |
| `0x3fb6f7` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdfe4 pointe vers 0xa4b26b, pas cet offset. |
| `0x3fb70f` | traduit/vérifié | `0x3fdfe8` → `0x16b6c7` | `<0xFD><0x11> está paralisado!\nPode não conseguir agir!` |
| `0x3fb73a` | traduit/vérifié | `0x3fdfec` → `0x16b93d` | `<0xFD><0x13>, com <0xFD><0x1A>,\nparalisou <0xFD><0x11>!<0xFA>Pode não conseguir agir!` |
| `0x3fb76a` | traduit/vérifié | `0x3fdff0` → `0x80eb4e` | `<0xFD><0x0F> está paralisado!\nNão consegue agir!` |
| `0x3fb78a` | traduit/vérifié | `0x3fdff4, 0x9fe44c` → `0x16bd98, 0x16bd98` | `<0xFD><0x10> já está\nparalisado!` |
| `0x3fb7a3` | traduit/vérifié | `0x3fdff8` → `0x16bdaf` | `<0xFD><0x10> foi curado\nda paralisia!` |
| `0x3fb7bf` | traduit/vérifié | `0x3fdffc` → `0x7b214f` | `<0xFD><0x10> teve seu\nsonho devorado!` |
| `0x3fb7d5` | traduit/vérifié | `0x3fe000` → `0x7b2117` | `<0xFD><0x0F>: <0xFD><0x00>\nnão pode subir mais!` |
| `0x3fb7ee` | traduit/vérifié | `0x3fe004` → `0x7b1fc9` | `<0xFD><0x10>: <0xFD><0x00>\nnão pode cair mais!` |
| `0x3fb806` | traduit/vérifié | `0x3fe008` → `0xc277f2` | `Na sua equipe, <0xFD><0x00>\nparou de funcionar!` |
| `0x3fb826` | traduit/vérifié | `0x3fe00c` → `0x80ec14` | `Na equipe rival, <0xFD><0x00>\nparou de funcionar!` |
| `0x3fb827` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb826, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fb844` | traduit/vérifié | `0x3fe010` → `0x16bdcb` | `<0xFD><0x0F> está\nconfuso!` |
| `0x3fb854` | traduit/vérifié | `0x3fe014` → `0x3fb854` | `<0xFD><0x0F> saiu\nda confusão!` |
| `0x3fb871` | traduit/vérifié | `0x3fe018` → `0x16bddc` | `<0xFD><0x11> ficou\nconfuso!` |
| `0x3fb885` | traduit/vérifié | `0x3fe01c, 0x9feb40` → `0x16bdee, 0x16bdee` | `<0xFD><0x10> já está\nconfuso!` |
| `0x3fb89d` | traduit/vérifié | `0x3fe020` → `0x16be02` | `<0xFD><0x10>\nse apaixonou!` |
| `0x3fb8ae` | traduit/vérifié | `0x3fe024` → `0xbe0458` | `<0xFD><0x0F> se apaixonou\npor <0xFD><0x13>!` |
| `0x3fb8c5` | traduit/vérifié | `0x3fe028` → `0x3fb8c5` | `<0xFD><0x0F> está\nimóvel de amor!` |
| `0x3fb8e0` | traduit/vérifié | `0x3fe02c` → `0x7b1e36` | `<0xFD><0x10> foi\nlevado pelo vento!` |
| `0x3fb8f3` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fe030 pointe vers 0xa4abc2, pas cet offset. |
| `0x3fb914` | traduit/vérifié | `0x3fe034` → `0x3fb914` | `<0xFD><0x0F> hesitou!` |
| `0x3fb921` | traduit/vérifié | `0x3fe038` → `0x16be13` | `<0xFD><0x10> recuperou\na saúde!` |
| `0x3fb935` | traduit/vérifié | `0x3fe03c` → `0x16be29` | `<0xFD><0x10> está com\nPS no máximo!` |
| `0x3fb946` | traduit/vérifié | `0x3fe040` → `0xc275fd` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou a Def. Esp.!` |
| `0x3fb95e` | traduit/vérifié | `0x3fe490` → `0x80ee80` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou um pouco a Def. Esp.!` |
| `0x3fb97f` | traduit/vérifié | `0x3fe044` → `0x7a39bc` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou a Defesa!` |
| `0x3fb997` | traduit/vérifié | `0x3fe48c` → `0x80ec64` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou um pouco a Defesa!` |
| `0x3fb9b8` | traduit/vérifié | `0x3fe048` → `0x16be43` | `A equipe <0xFD><0x38> foi coberta\npor um véu!` |
| `0x3fb9d6` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb9b8, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fb9d9` | traduit/vérifié | `0x3fe04c` → `0x16b69a` | `A equipe de <0xFD><0x10> está\nprotegida por Safeguard!` |
| `0x3fb9ff` | traduit/vérifié | `0x3fe050` → `0x16be67` | `A equipe <0xFD><0x38> não está mais\nprotegida por Safeguard!` |
| `0x3fba2c` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb9ff, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fba2f` | traduit/vérifié | `0x3fe054` → `0x16be9a` | `<0xFD><0x0F> foi\ndormir!` |
| `0x3fba41` | traduit/vérifié | `0x3fe058` → `0x7a397e` | `<0xFD><0x0F> dormiu e\nrecuperou a saúde!` |
| `0x3fba5e` | traduit/vérifié | `0x3fe05c` → `0x3fba5e` | `<0xFD><0x0F> criou\num redemoinho!` |
| `0x3fba79` | traduit/vérifié | `0x3fe060` → `0xbe0566` | `<0xFD><0x0F> absorveu\na luz solar!` |
| `0x3fba8e` | traduit/vérifié | `0x3fe064` → `0x16bea9` | `<0xFD><0x0F> abaixou\na cabeça!` |
| `0x3fbab2` | traduit/vérifié | `0x3fe06c` → `0x16bebe` | `<0xFD><0x0F> voou\nbem alto!` |
| `0x3fbac3` | traduit/vérifié | `0x3fe070` → `0x904d6d` | `<0xFD><0x0F> cavou um buraco!` |
| `0x3fbad2` | traduit/vérifié | `0x3fe400` → `0x7a399d` | `<0xFD><0x0F> se escondeu\ndebaixo d'água!` |
| `0x3fbae5` | traduit/vérifié | `0x3fe404` → `0x3fbae5` | `<0xFD><0x0F> saltou!` |
| `0x3fbaf3` | traduit/vérifié | `0x3fe074` → `0xc274cc` | `<0xFD><0x10> foi apertado\npelo Bind de <0xFD><0x0F>!` |
| `0x3fbb11` | traduit/vérifié | `0x3fe078` → `0x16bed0` | `<0xFD><0x10> ficou preso\nno vórtice!` |
| `0x3fbb2f` | traduit/vérifié | `0x3fe42c` → `0x16beeb` | `<0xFD><0x10> ficou preso\npor <0xFD><0x14>!` |
| `0x3fbb4c` | traduit/vérifié | `0x3fe07c` → `0x16bf02` | `<0xFD><0x10> foi enrolado por\n<0xFD><0x0F>!` |
| `0x3fbb62` | traduit/vérifié | `0x3fe080` → `0x16bf1a` | `<0xFD><0x0F> usou Clamp em\n<0xFD><0x10>!` |
| `0x3fbb71` | traduit/vérifié | `0x3fe084` → `0x3fbb71` | `<0xFD><0x0F> sofre\ncom <0xFD><0x00>!` |
| `0x3fbb83` | traduit/vérifié | `0x3fe088` → `0xbe0440` | `<0xFD><0x0F> foi libertado\nde <0xFD><0x00>!` |
| `0x3fbb99` | traduit/vérifié | `0x3fe08c` → `0x3fbb99` | `<0xFD><0x0F> continuou\ne se chocou!` |
| `0x3fbbb4` | traduit/vérifié | `0x42e94` → `0x3fbbb4` | `<0xFD><0x2A> ficou\nenvolto em Mist!` |
| `0x3fbbd0` | traduit/vérifié | `0x3fe094` → `0x16bf2f` | `<0xFD><0x13> está protegido\npor Mist!` |
| `0x3fbbe9` | traduit/vérifié | `0x42e8c, 0x3fe098` → `0xbe057f, 0xbe057f` | `<0xFD><0x0F> está\nse concentrando!` |
| `0x3fbbff` | traduit/vérifié | `0x3fe09c` → `0xbe0470` | `<0xFD><0x0F> sofre\ndano de recuo!` |
| `0x3fbc16` | traduit/vérifié | `0x3fe0a0` → `0x16bf4b` | `<0xFD><0x0F> se\nprotegeu!` |
| `0x3fbc2b` | traduit/vérifié | `0x3fe0a4` → `0x16bf5b` | `<0xFD><0x0F> sofre com\na tempestade de areia!` |
| `0x3fbc4c` | traduit/vérifié | `0x3fe0a8` → `0x16bf7f` | `<0xFD><0x0F> é atingido\npor Hail!` |
| `0x3fbc62` | traduit/vérifié | `0x3fe488` → `0xbe04b8` | `<0xFD><0x28>: <0xFD><0x00>\nperdeu o efeito!` |
| `0x3fbc74` | traduit/vérifié | `0x3fe0ac` → `0x904b42` | `<0xFD><0x10> foi semeado!` |
| `0x3fbc83` | traduit/vérifié | `0x3fe0b0` → `0xbe029d` | `<0xFD><0x10> escapou\ndo ataque!` |
| `0x3fbc99` | traduit/vérifié | `0x3fe0b4` → `0x16bf97` | `<0xFD><0x0F> perde PS\npor Leech Seed!` |
| `0x3fbcbe` | traduit/vérifié | `0x3fe0b8` → `0x904d81` | `<0xFD><0x0F> está\nadormecido.` |
| `0x3fbcd1` | traduit/vérifié | `0x3fe0bc` → `0xe696e2` | `<0xFD><0x0F> acordou!` |
| `0x3fbcdd` | traduit/vérifié | `0x3fe0c0` → `0xc2783f` | `Mas o Uproar de <0xFD><0x13>\no manteve acordado!` |
| `0x3fbcfc` | traduit/vérifié | `0x3fe0c4` → `0x3fbcfc` | `<0xFD><0x0F> acordou\ncom o Uproar!` |
| `0x3fbd16` | traduit/vérifié | `0x3fe0c8` → `0x904e3a` | `<0xFD><0x0F> causou\num Uproar!` |
| `0x3fbd2b` | traduit/vérifié | `0x3fe0cc` → `0x16bfb3` | `<0xFD><0x0F> está causando\num Uproar!` |
| `0x3fbd43` | traduit/vérifié | `0x3fe0d0` → `0x3fbd43` | `<0xFD><0x0F> se acalmou.` |
| `0x3fbd53` | traduit/vérifié | `0x3fe0d4` → `0xc27642` | `Mas <0xFD><0x10> não pode\ndormir com Uproar!` |
| `0x3fbd74` | traduit/vérifié | `0x3fe0d8` → `0x3fbd74` | `<0xFD><0x0F> acumulou\n<0xFD><0x00>!` |
| `0x3fbd86` | traduit/vérifié | `0x3fe0dc` → `0x3fbd86` | `<0xFD><0x0F> não pode\nacumular mais!` |
| `0x3fbda3` | traduit/vérifié | `0x3fe0e0` → `0xc27642` | `Mas <0xFD><0x10> não pode\ndormir com Uproar!` |
| `0x3fbdc4` | traduit/vérifié | `0x3fe0e4, 0x9fe010` → `0xc27597, 0xc27597` | `Mas o Uproar manteve\n<0xFD><0x10> acordado!` |
| `0x3fbde2` | traduit/vérifié | `0x3fe0e8` → `0x3fbde2` | `<0xFD><0x10> ficou acordado\nusando <0xFD><0x19>!` |
| `0x3fbe00` | traduit/vérifié | `0x3fe0ec` → `0x16bfcf` | `<0xFD><0x0F> está acumulando\nenergia!` |
| `0x3fbe16` | traduit/vérifié | `0x3fe0f0` → `0x16bfeb` | `<0xFD><0x0F> liberou\nenergia!` |
| `0x3fbe2b` | traduit/vérifié | `0x3fe0f4` → `0x3fbe2b` | `<0xFD><0x0F> ficou\nconfuso de cansaço!` |
| `0x3fbe4e` | traduit/vérifié | `0x3fe0f8` → `0x3fbe4e` | `<0xFD><0x23> recolheu\n¥<0xFD><0x00>!<0xFB>` |
| `0x3fbe61` | traduit/vérifié | `0x3fe0fc` → `0x16bfff` | `<0xFD><0x10>\nnão é afetado!` |
| `0x3fbe73` | traduit/vérifié | `0x3fe100` → `0xbe0598` | `<0xFD><0x0F> se transformou\nem <0xFD><0x00>!` |
| `0x3fbe8b` | traduit/vérifié | `0x3fe104` → `0xbe0428` | `<0xFD><0x0F> criou\num Substitute!` |
| `0x3fbea1` | traduit/vérifié | `0x3fe108` → `0x3fbea1` | `<0xFD><0x0F> já tem\num Substitute!` |
