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

La passe finale `languages/pt/patches/batch_09.py` réutilise `StructuredTextPatch` sans modifier le code partagé. Elle fixe 36 entrées / 40 consommateurs : retours de ligne rebalancés par le moteur générique et terminateur du tampon FD2F à `0x3fb262` perdu lors du traitement du voisin. La relocalisation finale évite toute écriture dans la cellule voisine ; les préimages EN, contrôles, tailles et pointeurs sont validés atomiquement. L’idempotence est contrôlée.

## Vérification

À compléter après le build PT et les sondes hors écran.

## Bilan offset par offset

Les sites sont les adresses des pointeurs dans la ROM EN ; les cibles sont leurs valeurs résolues dans la ROM PT finale. Une cible conservée à l’adresse EN reste vérifiée octet par octet.

| Offset | Résultat | Pointeurs source → cibles PT | Décision / valeur PT |
|---|---|---|---|
| `0x3ec2ae` | traduit/vérifié | `0x3ec3d4` → `en attente` | `SÓLIDO` |
| `0x3ec2b9` | traduit/vérifié | `0x3ec3e0` → `en attente` | `FAMINTO` |
| `0x3ec2c0` | traduit/vérifié | `0x3ec3ec` → `en attente` | `APERTADO` |
| `0x3ec2c6` | traduit/vérifié | `0x3ec3f8` → `en attente` | `CÓCEGAS` |
| `0x3ec2cf` | traduit/vérifié | `0x3ec404` → `en attente` | `GIRANDO` |
| `0x3ec2d8` | traduit/vérifié | `0x3ec410` → `en attente` | `EM ESPIRAL` |
| `0x3ec2e2` | traduit/vérifié | `0x3ec41c` → `en attente` | `SEDENTO` |
| `0x3ec2ea` | traduit/vérifié | `0x3ec428` → `en attente` | `À TOA` |
| `0x3ec2f2` | traduit/vérifié | `0x3ec434` → `en attente` | `SEDOSO` |
| `0x3ec2f8` | traduit/vérifié | `0x3ec440` → `en attente` | `TRISTEMENTE` |
| `0x3ec2fe` | traduit/vérifié | `0x3ec44c` → `en attente` | `SEM ESPERANÇA` |
| `0x3ec307` | traduit/vérifié | `0x3ec458` → `en attente` | `INÚTIL` |
| `0x3ec30f` | traduit/vérifié | `0x3ec464` → `en attente` | `BABANDO` |
| `0x3ec318` | traduit/vérifié | `0x3ec470` → `en attente` | `EMPOLGANTE` |
| `0x3ec321` | traduit/vérifié | `0x3ec47c` → `en attente` | `GROSSO` |
| `0x3ec327` | traduit/vérifié | `0x3ec488` → `en attente` | `LISO` |
| `0x3ec32e` | traduit/vérifié | `0x3ec494` → `en attente` | `VISCOSO` |
| `0x3ec334` | traduit/vérifié | `0x3ec4a0` → `en attente` | `FINO` |
| `0x3ec339` | traduit/vérifié | `0x3ec4ac` → `en attente` | `QUEBRAR` |
| `0x3ec33f` | traduit/vérifié | `0x3ec4b8` → `en attente` | `VORAZ` |
| `0x3ec349` | traduit/vérifié | `0x3ec4c4` → `en attente` | `ESPALHAR` |
| `0x3ec351` | traduit/vérifié | `0x3ec4d0` → `en attente` | `INCRÍVEL` |
| `0x3ec359` | traduit/vérifié | `0x3ec4dc` → `en attente` | `FRACO` |
| `0x3ec35f` | traduit/vérifié | `0x3ec4e8` → `en attente` | `BAMBO` |
| `0x3ec366` | traduit/vérifié | `0x3ec4f4` → `en attente` | `TRÊMULO` |
| `0x3ec36c` | traduit/vérifié | `0x3ec500` → `en attente` | `RASGADO` |
| `0x3ec373` | traduit/vérifié | `0x3ec50c` → `en attente` | `TRITURADO` |
| `0x3ec37c` | traduit/vérifié | `0x3ec518` → `en attente` | `AUMENTANDO` |
| `0x3ec38b` | traduit/vérifié | `0x3ec530` → `en attente` | `DESTRUÍDO` |
| `0x3ec395` | traduit/vérifié | `0x3ec53c` → `en attente` | `ARDENTE` |
| `0x3ec39b` | traduit/vérifié | `0x3ec548` → `en attente` | `APAIXONADO` |
| `0x3ec3a7` | traduit/vérifié | `0x3ec554` → `en attente` | `FELIZMENTE` |
| `0x3ec3af` | traduit/vérifié | `0x3ec560` → `en attente` | `EXPECTATIVA` |
| `0x3ec573` | traduit/vérifié | `0x3ec650` → `en attente` | `EVENTOS` |
| `0x3ec57a` | traduit/vérifié | `0x3ec65c` → `en attente` | `CASEIRO` |
| `0x3ec587` | traduit/vérifié | `0x3ec668` → `en attente` | `FRUTA` |
| `0x3ec58d` | traduit/vérifié | `0x3ec674` → `en attente` | `CONCURSO` |
| `0x3ec598` | traduit/vérifié | `0x3ec68c` → `en attente` | `JUIZ` |
| `0x3ec59e` | traduit/vérifié | `0x3ec698` → `en attente` | `SUPER` |
| `0x3ec5a4` | traduit/vérifié | `0x3ec6a4` → `en attente` | `PALCO` |
| `0x3ec5aa` | traduit/vérifié | `0x3ec6b0` → `en attente` | `HALL DA FAMA` |
| `0x3ec5b7` | traduit/vérifié | `0x3ec6bc` → `en attente` | `EVOLUÇÃO` |
| `0x3ec5c1` | traduit/vérifié | `0x3ec6c8` → `en attente` | `HIPER` |
| `0x3ec5c7` | traduit/vérifié | `0x3ec6d4` → `en attente` | `TORRE DE BATALHA` |
| `0x3ec5d4` | traduit/vérifié | `0x3ec6e0` → `en attente` | `LÍDERES` |
| `0x3ec5dc` | traduit/vérifié | `0x3ec6ec` → `en attente` | `SALA DE BATALHA` |
| `0x3ec5e8` | traduit/vérifié | `0x3ec6f8` → `en attente` | `OCULTO` |
| `0x3ec5ef` | traduit/vérifié | `0x3ec704` → `en attente` | `BASE SECRETA` |
| `0x3ec5fb` | traduit/vérifié | `0x3ec710` → `en attente` | `MISTURAR` |
| `0x3ec607` | traduit/vérifié | `0x3ec728` → `en attente` | `MESTRE` |
| `0x3ec60e` | traduit/vérifié | `0x3ec734` → `en attente` | `POSIÇÃO` |
| `0x3ec613` | traduit/vérifié | `0x3ec740` → `en attente` | `FITA` |
| `0x3ec61a` | traduit/vérifié | `0x3ec74c` → `en attente` | `ESMAGAR` |
| `0x3ec620` | traduit/vérifié | `0x3ec758` → `en attente` | `DIRETO` |
| `0x3ec627` | traduit/vérifié | `0x3ec764` → `en attente` | `TORRE` |
| `0x3ec62d` | traduit/vérifié | `0x3ec770` → `en attente` | `UNIÃO` |
| `0x3ec633` | traduit/vérifié | `0x3ec77c` → `en attente` | `SALA` |
| `0x3ec638` | traduit/vérifié | `0x3ec788` → `en attente` | `SEM FIO` |
| `0x3eca63` | traduit/vérifié | `0x3ecb5c` → `en attente` | `SIM, SENHOR!` |
| `0x3eca6d` | traduit/vérifié | `0x3ecb68` → `en attente` | `VANGUARDA` |
| `0x3eca79` | traduit/vérifié | `0x3ecb74` → `en attente` | `CASAL` |
| `0x3eca80` | traduit/vérifié | `0x3ecb80` → `en attente` | `MUITO OBRIGADO` |
| `0x3eca8d` | traduit/vérifié | `0x3ecb8c` → `en attente` | `IUPI!` |
| `0x3eca95` | traduit/vérifié | `0x3ecb98` → `en attente` | `MEGA` |
| `0x3eca9a` | traduit/vérifié | `0x3ecba4` → `en attente` | `NOCAUTE EM 1!` |
| `0x3ecaa4` | traduit/vérifié | `0x3ecbb0` → `en attente` | `DESTINO` |
| `0x3ecaac` | traduit/vérifié | `0x3ecbbc` → `en attente` | `Cancelar` |
| `0x3ecab7` | traduit/vérifié | `0x3ecbd4` → `en attente` | `ACHATAR` |
| `0x3ecabf` | traduit/vérifié | `0x3ecbe0` → `en attente` | `BRINCANDO` |
| `0x3ecac7` | traduit/vérifié | `0x3ecbec` → `en attente` | `PERDEDOR` |
| `0x3ecacd` | traduit/vérifié | `0x3ecbf8` → `en attente` | `PERDENDO` |
| `0x3ecad4` | traduit/vérifié | `0x3ecc04` → `en attente` | `AGITADO` |
| `0x3ecade` | traduit/vérifié | `0x3ecc10` → `en attente` | `NA MODA E` |
| `0x3ecae6` | traduit/vérifié | `0x3ecc1c` → `en attente` | `SACUDIR` |
| `0x3ecaec` | traduit/vérifié | `0x3ecc28` → `en attente` | `SUSPEITO` |
| `0x3ecaf2` | traduit/vérifié | `0x3ecc34` → `en attente` | `ANIMADO` |
| `0x3ecaf9` | traduit/vérifié | `0x3ecc40` → `en attente` | `MODERNO` |
| `0x3ecb00` | traduit/vérifié | `0x3ecc4c` → `en attente` | `ATÉ MAIS` |
| `0x3ecb09` | traduit/vérifié | `0x3ecc58` → `en attente` | `BUM` |
| `0x3ecb0e` | traduit/vérifié | `0x3ecc64` → `en attente` | `NOCAUTE` |
| `0x3ecb17` | traduit/vérifié | `0x3ecc70` → `en attente` | `INCÔMODO` |
| `0x3ecb1e` | traduit/vérifié | `0x3ecc7c` → `en attente` | `VENCEDOR` |
| `0x3ecb25` | traduit/vérifié | `0x3ecc88` → `en attente` | `FEBRE` |
| `0x3ecb2b` | traduit/vérifié | `0x3ecc94` → `en attente` | `ASPIRANTE` |
| `0x3ecb33` | traduit/vérifié | `0x3ecca0` → `en attente` | `BEBÊ` |
| `0x3ecb38` | traduit/vérifié | `0x3eccac` → `en attente` | `CORAÇÃO` |
| `0x3ecb42` | traduit/vérifié | `0x3eccc4` → `en attente` | `JOVEM` |
| `0x3ecb48` | traduit/vérifié | `0x3eccd0` → `en attente` | `FEIO` |
| `0x3eed08` | conservé/vérifié | `0x3f1cb0` → `en attente` | `Bellin Town` |
| `0x3eed22` | conservé/vérifié | `0x3f1cb8` → `en attente` | `Crater Town` |
| `0x3eed67` | conservé/vérifié | `0x3f1ccc` → `en attente` | `Tarmigan Town` |
| `0x3eed77` | conservé/vérifié | `0x3f1cd0` → `en attente` | `INDIGO PLATEAU` |
| `0x3eed93` | conservé/vérifié | `0x3f1cd8` → `en attente` | `Route 4` |
| `0x3eed9b` | conservé/vérifié | `0x3f1cdc` → `en attente` | `Route 10` |
| `0x3eeda4` | conservé/vérifié | `0x3f1ce0` → `en attente` | `Route 1` |
| `0x3eedac` | conservé/vérifié | `0x3f1ce4` → `en attente` | `Route 2` |
| `0x3eedb4` | conservé/vérifié | `0x3f1ce8` → `en attente` | `Route 3` |
| `0x3eedbc` | exception justifiée | `aucun` → `sans objet` | Ancien doublon ROUTE 4 sans pointeur ; nom vivant Route 4 à 0x3eed93, table 0x3f1cd8. |
| `0x3eedc4` | conservé/vérifié | `0x3f1cf0` → `en attente` | `Route 5` |
| `0x3eedcc` | conservé/vérifié | `0x3f1cf4` → `en attente` | `Route 6` |
| `0x3eedd4` | conservé/vérifié | `0x3f1cf8` → `en attente` | `Route 7` |
| `0x3eeddc` | conservé/vérifié | `0x3f1cfc` → `en attente` | `Route 8` |
| `0x3eede4` | conservé/vérifié | `0x3f1d00` → `en attente` | `Route 9` |
| `0x3eedec` | conservé/vérifié | `0x3f1d04` → `en attente` | `ROUTE 10` |
| `0x3eedf5` | conservé/vérifié | `0x3f1d08` → `en attente` | `Route 11` |
| `0x3eedfe` | conservé/vérifié | `0x3f1d0c` → `en attente` | `Route 12` |
| `0x3eee07` | conservé/vérifié | `0x3f1d10` → `en attente` | `Route 13` |
| `0x3eee10` | conservé/vérifié | `0x3f1d14` → `en attente` | `Route 14` |
| `0x3eee19` | conservé/vérifié | `0x3f1d18` → `en attente` | `Route 15` |
| `0x3eee22` | conservé/vérifié | `0x3f1d1c` → `en attente` | `Route 16` |
| `0x3eee2b` | conservé/vérifié | `0x3f1d20` → `en attente` | `Route 17` |
| `0x3eee34` | conservé/vérifié | `0x3f1d24` → `en attente` | `Route 18` |
| `0x3eee7c` | conservé/vérifié | `0x3f1b40, 0x3f1d44` → `en attente` | `Grim Woods` |
| `0x3eee9f` | conservé/vérifié | `0x3f1d50` → `en attente` | `Underground Pass` |
| `0x3eeec1` | conservé/vérifié | `0x3f1b58, 0x3f1d58` → `en attente` | `Valley Cave` |
| `0x3eeed0` | conservé/vérifié | `0x3f1b64, 0x3f1d5c` → `en attente` | `Victory Road` |
| `0x3eef12` | conservé/vérifié | `0x3f1d70` → `en attente` | `Pokémon League` |
| `0x3eef2d` | conservé/vérifié | `0x3f1b94, 0x3f1d78` → `en attente` | `Rift Cave` |
| `0x3eef3d` | conservé/vérifié | `0x3f1ba0, 0x3f1d7c` → `en attente` | `Vivill Woods` |
| `0x3eef4b` | conservé/vérifié | `0x3f1bac, 0x3f1d80` → `en attente` | `Icicle Cave` |
| `0x3eef94` | conservé/vérifié | `0x3f1d98` → `en attente` | `Cube Corp.` |
| `0x3eefa0` | conservé/vérifié | `0x3f1d9c` → `en attente` | `SEVEN ISLAND` |
| `0x3eefad` | conservé/vérifié | `0x3f1da0` → `en attente` | `SIX ISLAND` |
| `0x3eefea` | conservé/vérifié | `0x3f1db4` → `en attente` | `Cave of Being` |
| `0x3ef094` | conservé/vérifié | `0x3f1de4` → `en attente` | `RUIN VALLEY` |
| `0x3ef0ae` | conservé/vérifié | `0x3f1dec` → `en attente` | `CANYON ENTRANCE` |
| `0x3ef0be` | conservé/vérifié | `0x3f1df0` → `en attente` | `SEVAULT CANYON` |
| `0x3ef0cd` | conservé/vérifié | `0x3f1df4` → `en attente` | `TANOBY RUINS` |
| `0x3ef0da` | conservé/vérifié | `0x3f1df8` → `en attente` | `SEVII ISLE 22` |
| `0x3ef0e8` | conservé/vérifié | `0x3f1dfc` → `en attente` | `SEVII ISLE 23` |
| `0x3ef0f6` | conservé/vérifié | `0x3f1e00` → `en attente` | `SEVII ISLE 24` |
| `0x3ef104` | conservé/vérifié | `0x3f1e04` → `en attente` | `NAVEL ROCK` |
| `0x3ef119` | conservé/vérifié | `0x3f1bd0, 0x3f1e0c` → `en attente` | `BERRY FOREST` |
| `0x3ef133` | conservé/vérifié | `0x3f1e14` → `en attente` | `Battle Mine` |
| `0x3ef144` | conservé/vérifié | `0x3f1e18` → `en attente` | `Battle Tower` |
| `0x3ef183` | conservé/vérifié | `0x3f1bf4, 0x3f1e2c` → `en attente` | `Autl Woods` |
| `0x3ef193` | conservé/vérifié | `0x3f1e30` → `en attente` | `Cliff Cave` |
| `0x3ef1ae` | conservé/vérifié | `0x3f1e38` → `en attente` | `Battleground` |
| `0x3ef1d9` | conservé/vérifié | `0x3f1e44` → `en attente` | `S.S. Marine` |
| `0x3ef1e8` | conservé/vérifié | `0x3f1e48` → `en attente` | `Ferrothorn Turf` |
| `0x3ef207` | conservé/vérifié | `0x3f1e50` → `en attente` | `Desert Ruins` |
| `0x3ef214` | conservé/vérifié | `0x3f1e54` → `en attente` | `Frozen Tomb` |
| `0x3ef22e` | conservé/vérifié | `0xc4da0, 0x3f1e5c` → `en attente` | `Dehara Dept.` |
| `0x3fb219` | conservé/vérifié | `0x3fdf3c` → `en attente` | `<0xFD><0x24>` |
| `0x3fb21c` | conservé/vérifié | `0x3fe4e8` → `en attente` | `<0xFD><0x2E>` |
| `0x3fb21f` | traduit/vérifié | `0x3fe504` → `en attente` | `<0xFD><0x1D>: <0xFD><0x06>, volte!` |
| `0x3fb232` | conservé/vérifié | `0x3fe508` → `en attente` | `<0xFD><0x25>` |
| `0x3fb235` | traduit/vérifié | `0x3fe50c` → `en attente` | `<0xFD><0x1D>: <0xFD><0x08>, volte!` |
| `0x3fb248` | traduit/vérifié | `0x3fe510` → `en attente` | `<0xFD><0x1D>: <0xFD><0x06> e\n<0xFD><0x08>, voltem!` |
| `0x3fb262` | conservé/vérifié | `0x3fe4ec` → `en attente` | `<0xFD><0x2F>` |
| `0x3fb265` | traduit/vérifié | `0x3fdf40` → `en attente` | `<0xFD><0x00> ganhou<0xFD><0x01>\n<0xFD><0x34> pontos de Exp.!<0xFB>` |
| `0x3fb283` | traduit/vérifié | `0x3fe434` → `en attente` | `<0x00>um bônus de` |
| `0x3fb284` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb283, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fb28e` | traduit/vérifié | `0x3fdf44` → `en attente` | `<0xFD><0x00> subiu para\no Nv. <0xFD><0x01>!<0xFC><0x0A><0xFB>` |
| `0x3fb2a4` | traduit/vérifié | `0x3fdf48` → `en attente` | `<0xFD><0x00> aprendeu\n<0xFD><0x01>!<0xFC><0x0A><0xFB>` |
| `0x3fb2b6` | traduit/vérifié | `0x3fdf4c` → `en attente` | `<0xFD><0x00> tenta aprender\n<0xFD><0x01>.<0xFB>` |
| `0x3fb2d1` | traduit/vérifié | `0x3fdf50` → `en attente` | `Mas <0xFD><0x00> só pode ter\nquatro movimentos.<0xFB>` |
| `0x3fb2fc` | traduit/vérifié | `0x3fdf54` → `en attente` | `Esquecer um movimento\npara aprender <0xFD><0x01>?` |
| `0x3fb31f` | traduit/vérifié | `0x3fdf58` → `en attente` | `<0xFD><0x00> esqueceu\n<0xFD><0x01>.<0xFB>` |
| `0x3fb32e` | traduit/vérifié | `0x3fdf5c` → `en attente` | `<0xFC><0x08><0x20>Parar de aprender\n<0xFD><0x01>?` |
| `0x3fb343` | traduit/vérifié | `0x3fdf60` → `en attente` | `<0xFD><0x00> não aprendeu\n<0xFD><0x01>.<0xFB>` |
| `0x3fb359` | traduit/vérifié | `0x3fe450` → `en attente` | `Usar outro Pokémon?` |
| `0x3fb36b` | traduit/vérifié | `0x3fdf68` → `en attente` | `<0xFD><0x0F> errou\no ataque!` |
| `0x3fb37f` | traduit/vérifié | `0x3fdf6c` → `en attente` | `<0xFD><0x10>\nse protegeu!` |
| `0x3fb394` | traduit/vérifié | `0x3fdf74` → `en attente` | `<0xFD><0x10> evitou danos\ncom <0xFD><0x19>!` |
| `0x3fb3af` | traduit/vérifié | `0x3fe43c` → `en attente` | `<0xFD><0x10> evita movimentos\nTerrestres com <0xFD><0x19>!` |
| `0x3fb3d3` | traduit/vérifié | `0x3fe470` → `en attente` | `<0xFD><0x10> desviou\ndo ataque!` |
| `0x3fb400` | traduit/vérifié | `0x3fdf7c` → `en attente` | `<0xFD><0x0F> foi\nnocauteado!<0xFB>` |
| `0x3fb40d` | traduit/vérifié | `0x3fdf80` → `en attente` | `<0xFD><0x10> foi\nnocauteado!<0xFB>` |
| `0x3fb41a` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdf84 pointe vers 0xa4c670, pas cet offset. |
| `0x3fb433` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdf88 pointe vers 0xa4c689, pas cet offset. |
| `0x3fb451` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdf8c pointe vers 0xa4c6b3, pas cet offset. |
| `0x3fb484` | exception justifiée | `aucun` → `sans objet` | Ancien message de défaite sans aucun pointeur. Le chemin actuel utilise les cellules 0x3fdf88 → 0xa4c689 (équipe épuisée) et 0x3fdf8c → 0xa4c6b3 (défaite), hors PT-09. |
| `0x3fb4be` | exception justifiée | `aucun` → `sans objet` | Ancien message de défaite sans aucun pointeur. Le chemin actuel utilise les cellules 0x3fdf88 → 0xa4c689 (équipe épuisée) et 0x3fdf8c → 0xa4c6b3 (défaite), hors PT-09. |
| `0x3fb4f7` | exception justifiée | `aucun` → `sans objet` | Ancien message de défaite sans aucun pointeur. Le chemin actuel utilise les cellules 0x3fdf88 → 0xa4c689 (équipe épuisée) et 0x3fdf8c → 0xa4c6b3 (défaite), hors PT-09. |
| `0x3fb508` | traduit/vérifié | `0x3fdf90` → `en attente` | `<0xFD><0x13> impede a fuga\ncom <0xFD><0x1A>!<0xFB>` |
| `0x3fb525` | traduit/vérifié | `0x3fe354` → `en attente` | `Não pode fugir!<0xFB>` |
| `0x3fb534` | traduit/vérifié | `0x3fe4a0` → `en attente` | `<0xFD><0x0F> não pode fugir!` |
| `0x3fb545` | traduit/vérifié | `0x3fdf94` → `en attente` | `Acertou <0xFD><0x00> vez(es)!` |
| `0x3fb555` | traduit/vérifié | `0x3fdf98` → `en attente` | `<0xFD><0x11> ficou\nadormecido!` |
| `0x3fb565` | traduit/vérifié | `0x3fdf9c` → `en attente` | `<0xFD><0x13>, com <0xFD><0x1A>,\nfez <0xFD><0x11> dormir!` |
| `0x3fb57c` | traduit/vérifié | `0x3fdfa0, 0x9fdfe8, 0x9fe1f4` → `en attente` | `<0xFD><0x10> já está\nadormecido!` |
| `0x3fb592` | traduit/vérifié | `0x3fdfa4` → `en attente` | `<0xFD><0x0F> já está\nadormecido!` |
| `0x3fb5a8` | traduit/vérifié | `0x3fdfa8` → `en attente` | `<0xFD><0x10>\nnão foi afetado!` |
| `0x3fb5bc` | traduit/vérifié | `0x3fdfac` → `en attente` | `<0xFD><0x11> foi\nenvenenado!` |
| `0x3fb5cd` | traduit/vérifié | `0x3fdfb0` → `en attente` | `<0xFD><0x13>, com <0xFD><0x1A>,\nenvenenou <0xFD><0x11>!` |
| `0x3fb5e2` | traduit/vérifié | `0x3fdfb4` → `en attente` | `<0xFD><0x0F> sofre\ncom o veneno!` |
| `0x3fb5f8` | traduit/vérifié | `0x3fdfb8, 0x9fe8a0` → `en attente` | `<0xFD><0x10> já está\nenvenenado.` |
| `0x3fb610` | traduit/vérifié | `0x3fdfbc` → `en attente` | `<0xFD><0x11> foi muito\nenvenenado!` |
| `0x3fb626` | traduit/vérifié | `0x3fdfc0` → `en attente` | `<0xFD><0x10> teve sua\nenergia drenada!` |
| `0x3fb641` | traduit/vérifié | `0x3fdfc4` → `en attente` | `<0xFD><0x11> foi queimado!` |
| `0x3fb650` | traduit/vérifié | `0x3fdfc8` → `en attente` | `<0xFD><0x13>, com <0xFD><0x1A>,\nqueimou <0xFD><0x11>!` |
| `0x3fb663` | traduit/vérifié | `0x3fdfcc` → `en attente` | `<0xFD><0x0F> sofre\ncom a queimadura!` |
| `0x3fb67b` | traduit/vérifié | `0x3fe47c, 0x9fe638` → `en attente` | `<0xFD><0x10> já está\nqueimado.` |
| `0x3fb692` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdfd0 pointe vers 0xa4b23c, pas cet offset. |
| `0x3fb6a7` | traduit/vérifié | `0x3fdfd4` → `en attente` | `<0xFD><0x13>, com <0xFD><0x1A>,\ncongelou <0xFD><0x11>!` |
| `0x3fb6bf` | traduit/vérifié | `0x3fdfd8` → `en attente` | `<0xFD><0x0F> está\ncongelado!` |
| `0x3fb6d3` | traduit/vérifié | `0x8bbe33, 0x90531e` → `en attente` | `<0xFD><0x10> descongelou!` |
| `0x3fb6e5` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdfe0 pointe vers 0xa4b2a5, pas cet offset. |
| `0x3fb6f7` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fdfe4 pointe vers 0xa4b26b, pas cet offset. |
| `0x3fb70f` | traduit/vérifié | `0x3fdfe8` → `en attente` | `<0xFD><0x11> está paralisado!\nPode não conseguir agir!` |
| `0x3fb73a` | traduit/vérifié | `0x3fdfec` → `en attente` | `<0xFD><0x13>, com <0xFD><0x1A>,\nparalisou <0xFD><0x11>!<0xFA>Pode não conseguir agir!` |
| `0x3fb76a` | traduit/vérifié | `0x3fdff0` → `en attente` | `<0xFD><0x0F> está paralisado!\nNão consegue agir!` |
| `0x3fb78a` | traduit/vérifié | `0x3fdff4, 0x9fe44c` → `en attente` | `<0xFD><0x10> já está\nparalisado!` |
| `0x3fb7a3` | traduit/vérifié | `0x3fdff8` → `en attente` | `<0xFD><0x10> foi curado\nda paralisia!` |
| `0x3fb7bf` | traduit/vérifié | `0x3fdffc` → `en attente` | `<0xFD><0x10> teve seu\nsonho devorado!` |
| `0x3fb7d5` | traduit/vérifié | `0x3fe000` → `en attente` | `<0xFD><0x0F>: <0xFD><0x00>\nnão pode subir mais!` |
| `0x3fb7ee` | traduit/vérifié | `0x3fe004` → `en attente` | `<0xFD><0x10>: <0xFD><0x00>\nnão pode cair mais!` |
| `0x3fb806` | traduit/vérifié | `0x3fe008` → `en attente` | `Na sua equipe, <0xFD><0x00>\nparou de funcionar!` |
| `0x3fb826` | traduit/vérifié | `0x3fe00c` → `en attente` | `Na equipe rival, <0xFD><0x00>\nparou de funcionar!` |
| `0x3fb827` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb826, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fb844` | traduit/vérifié | `0x3fe010` → `en attente` | `<0xFD><0x0F> está\nconfuso!` |
| `0x3fb854` | traduit/vérifié | `0x3fe014` → `en attente` | `<0xFD><0x0F> saiu\nda confusão!` |
| `0x3fb871` | traduit/vérifié | `0x3fe018` → `en attente` | `<0xFD><0x11> ficou\nconfuso!` |
| `0x3fb885` | traduit/vérifié | `0x3fe01c, 0x9feb40` → `en attente` | `<0xFD><0x10> já está\nconfuso!` |
| `0x3fb89d` | traduit/vérifié | `0x3fe020` → `en attente` | `<0xFD><0x10>\nse apaixonou!` |
| `0x3fb8ae` | traduit/vérifié | `0x3fe024` → `en attente` | `<0xFD><0x0F> se apaixonou\npor <0xFD><0x13>!` |
| `0x3fb8c5` | traduit/vérifié | `0x3fe028` → `en attente` | `<0xFD><0x0F> está\nimóvel de amor!` |
| `0x3fb8e0` | traduit/vérifié | `0x3fe02c` → `en attente` | `<0xFD><0x10> foi\nlevado pelo vento!` |
| `0x3fb8f3` | exception justifiée | `aucun` → `sans objet` | Ancien message remplacé par CFRU, aucun référent binaire. Cellule de comparaison 0x3fe030 pointe vers 0xa4abc2, pas cet offset. |
| `0x3fb914` | traduit/vérifié | `0x3fe034` → `en attente` | `<0xFD><0x0F> hesitou!` |
| `0x3fb921` | traduit/vérifié | `0x3fe038` → `en attente` | `<0xFD><0x10> recuperou\na saúde!` |
| `0x3fb935` | traduit/vérifié | `0x3fe03c` → `en attente` | `<0xFD><0x10> está com\nPS no máximo!` |
| `0x3fb946` | traduit/vérifié | `0x3fe040` → `en attente` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou a Def. Esp.!` |
| `0x3fb95e` | traduit/vérifié | `0x3fe490` → `en attente` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou um pouco a Def. Esp.!` |
| `0x3fb97f` | traduit/vérifié | `0x3fe044` → `en attente` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou a Defesa!` |
| `0x3fb997` | traduit/vérifié | `0x3fe48c` → `en attente` | `<0xFD><0x2A>, com <0xFD><0x14>,\naumentou um pouco a Defesa!` |
| `0x3fb9b8` | traduit/vérifié | `0x3fe048` → `en attente` | `A equipe <0xFD><0x38> foi coberta\npor um véu!` |
| `0x3fb9d6` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb9b8, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fb9d9` | traduit/vérifié | `0x3fe04c` → `en attente` | `A equipe de <0xFD><0x10> está\nprotegida por Safeguard!` |
| `0x3fb9ff` | traduit/vérifié | `0x3fe050` → `en attente` | `A equipe <0xFD><0x38> não está mais\nprotegida por Safeguard!` |
| `0x3fba2c` | exception justifiée | `aucun` → `sans objet` | Suffixe interne de 0x3fb9ff, aucun pointeur vers cet offset ; ne pas écraser le message parent. |
| `0x3fba2f` | traduit/vérifié | `0x3fe054` → `en attente` | `<0xFD><0x0F> foi\ndormir!` |
| `0x3fba41` | traduit/vérifié | `0x3fe058` → `en attente` | `<0xFD><0x0F> dormiu e\nrecuperou a saúde!` |
| `0x3fba5e` | traduit/vérifié | `0x3fe05c` → `en attente` | `<0xFD><0x0F> criou\num redemoinho!` |
| `0x3fba79` | traduit/vérifié | `0x3fe060` → `en attente` | `<0xFD><0x0F> absorveu\na luz solar!` |
| `0x3fba8e` | traduit/vérifié | `0x3fe064` → `en attente` | `<0xFD><0x0F> abaixou\na cabeça!` |
| `0x3fbab2` | traduit/vérifié | `0x3fe06c` → `en attente` | `<0xFD><0x0F> voou\nbem alto!` |
| `0x3fbac3` | traduit/vérifié | `0x3fe070` → `en attente` | `<0xFD><0x0F> cavou um buraco!` |
| `0x3fbad2` | traduit/vérifié | `0x3fe400` → `en attente` | `<0xFD><0x0F> se escondeu\ndebaixo d'água!` |
| `0x3fbae5` | traduit/vérifié | `0x3fe404` → `en attente` | `<0xFD><0x0F> saltou!` |
| `0x3fbaf3` | traduit/vérifié | `0x3fe074` → `en attente` | `<0xFD><0x10> foi apertado\npelo Bind de <0xFD><0x0F>!` |
| `0x3fbb11` | traduit/vérifié | `0x3fe078` → `en attente` | `<0xFD><0x10> ficou preso\nno vórtice!` |
| `0x3fbb2f` | traduit/vérifié | `0x3fe42c` → `en attente` | `<0xFD><0x10> ficou preso\npor <0xFD><0x14>!` |
| `0x3fbb4c` | traduit/vérifié | `0x3fe07c` → `en attente` | `<0xFD><0x10> foi enrolado por\n<0xFD><0x0F>!` |
| `0x3fbb62` | traduit/vérifié | `0x3fe080` → `en attente` | `<0xFD><0x0F> usou Clamp em\n<0xFD><0x10>!` |
| `0x3fbb71` | traduit/vérifié | `0x3fe084` → `en attente` | `<0xFD><0x0F> sofre\ncom <0xFD><0x00>!` |
| `0x3fbb83` | traduit/vérifié | `0x3fe088` → `en attente` | `<0xFD><0x0F> foi libertado\nde <0xFD><0x00>!` |
| `0x3fbb99` | traduit/vérifié | `0x3fe08c` → `en attente` | `<0xFD><0x0F> continuou\ne se chocou!` |
| `0x3fbbb4` | traduit/vérifié | `0x42e94` → `en attente` | `<0xFD><0x2A> ficou\nenvolto em Mist!` |
| `0x3fbbd0` | traduit/vérifié | `0x3fe094` → `en attente` | `<0xFD><0x13> está protegido\npor Mist!` |
| `0x3fbbe9` | traduit/vérifié | `0x42e8c, 0x3fe098` → `en attente` | `<0xFD><0x0F> está\nse concentrando!` |
| `0x3fbbff` | traduit/vérifié | `0x3fe09c` → `en attente` | `<0xFD><0x0F> sofre\ndano de recuo!` |
| `0x3fbc16` | traduit/vérifié | `0x3fe0a0` → `en attente` | `<0xFD><0x0F> se\nprotegeu!` |
| `0x3fbc2b` | traduit/vérifié | `0x3fe0a4` → `en attente` | `<0xFD><0x0F> sofre com\na tempestade de areia!` |
| `0x3fbc4c` | traduit/vérifié | `0x3fe0a8` → `en attente` | `<0xFD><0x0F> é atingido\npor Hail!` |
| `0x3fbc62` | traduit/vérifié | `0x3fe488` → `en attente` | `<0xFD><0x28>: <0xFD><0x00>\nperdeu o efeito!` |
| `0x3fbc74` | traduit/vérifié | `0x3fe0ac` → `en attente` | `<0xFD><0x10> foi semeado!` |
| `0x3fbc83` | traduit/vérifié | `0x3fe0b0` → `en attente` | `<0xFD><0x10> escapou\ndo ataque!` |
| `0x3fbc99` | traduit/vérifié | `0x3fe0b4` → `en attente` | `<0xFD><0x0F> perde PS\npor Leech Seed!` |
| `0x3fbcbe` | traduit/vérifié | `0x3fe0b8` → `en attente` | `<0xFD><0x0F> está\nadormecido.` |
| `0x3fbcd1` | traduit/vérifié | `0x3fe0bc` → `en attente` | `<0xFD><0x0F> acordou!` |
| `0x3fbcdd` | traduit/vérifié | `0x3fe0c0` → `en attente` | `Mas o Uproar de <0xFD><0x13>\no manteve acordado!` |
| `0x3fbcfc` | traduit/vérifié | `0x3fe0c4` → `en attente` | `<0xFD><0x0F> acordou\ncom o Uproar!` |
| `0x3fbd16` | traduit/vérifié | `0x3fe0c8` → `en attente` | `<0xFD><0x0F> causou\num Uproar!` |
| `0x3fbd2b` | traduit/vérifié | `0x3fe0cc` → `en attente` | `<0xFD><0x0F> está causando\num Uproar!` |
| `0x3fbd43` | traduit/vérifié | `0x3fe0d0` → `en attente` | `<0xFD><0x0F> se acalmou.` |
| `0x3fbd53` | traduit/vérifié | `0x3fe0d4` → `en attente` | `Mas <0xFD><0x10> não pode\ndormir com Uproar!` |
| `0x3fbd74` | traduit/vérifié | `0x3fe0d8` → `en attente` | `<0xFD><0x0F> acumulou\n<0xFD><0x00>!` |
| `0x3fbd86` | traduit/vérifié | `0x3fe0dc` → `en attente` | `<0xFD><0x0F> não pode\nacumular mais!` |
| `0x3fbda3` | traduit/vérifié | `0x3fe0e0` → `en attente` | `Mas <0xFD><0x10> não pode\ndormir com Uproar!` |
| `0x3fbdc4` | traduit/vérifié | `0x3fe0e4, 0x9fe010` → `en attente` | `Mas o Uproar manteve\n<0xFD><0x10> acordado!` |
| `0x3fbde2` | traduit/vérifié | `0x3fe0e8` → `en attente` | `<0xFD><0x10> ficou acordado\nusando <0xFD><0x19>!` |
| `0x3fbe00` | traduit/vérifié | `0x3fe0ec` → `en attente` | `<0xFD><0x0F> está acumulando\nenergia!` |
| `0x3fbe16` | traduit/vérifié | `0x3fe0f0` → `en attente` | `<0xFD><0x0F> liberou\nenergia!` |
| `0x3fbe2b` | traduit/vérifié | `0x3fe0f4` → `en attente` | `<0xFD><0x0F> ficou\nconfuso de cansaço!` |
| `0x3fbe4e` | traduit/vérifié | `0x3fe0f8` → `en attente` | `<0xFD><0x23> recolheu\n¥<0xFD><0x00>!<0xFB>` |
| `0x3fbe61` | traduit/vérifié | `0x3fe0fc` → `en attente` | `<0xFD><0x10>\nnão é afetado!` |
| `0x3fbe73` | traduit/vérifié | `0x3fe100` → `en attente` | `<0xFD><0x0F> se transformou\nem <0xFD><0x00>!` |
| `0x3fbe8b` | traduit/vérifié | `0x3fe104` → `en attente` | `<0xFD><0x0F> criou\num Substitute!` |
| `0x3fbea1` | traduit/vérifié | `0x3fe108` → `en attente` | `<0xFD><0x0F> já tem\num Substitute!` |
