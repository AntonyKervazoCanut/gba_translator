# PT-45 — Répliques du complexe de combat et messages CFRU

Périmètre : les 283 clés du manifeste PT-45, sans extension par plage.
F-758 et F-759 intégrés avant traduction. 282 traductions protégées ; une
fausse clé exclue et reliée au vrai consommateur. Aucune traduction existante supprimée.
Les sources EN et FR au même offset figurent dans `languages/pt/data/pt45_audit.json`,
avec préimage binaire, sites de pointeurs, valeur PT-BR, taille encodée et largeurs.
Ce fichier est le bilan détaillé reproductible, pas une preuve de parcours en jeu complet.

## Domaine et livraison

Les 241 premières entrées sont des répliques de Dresseurs et de personnages du complexe
de combat (avant/après combat, développeurs, Cynthia, Candice, Antisis). La fin contient
les messages de types, coups critiques, terrains, zones, Habilités et protections CFRU.
Les noms sans attestation F-759 restent anglais : Moomoo Milk, Gravity, Tailwind,
Lucky Chant, Infestation, Sky Drop, Crafty Shield, Quick Guard et Wide Guard.

Les tables indexées de répliques ont pour bases 0xa6f130, 0xa6f36c et 0xa6f574,
chargées notamment aux sites 0x9c584c, 0x9c5878, 0x9c5888 et 0x9e65b0–0x9e65b8.
Chaque pointeur de cellule est validé sur la ROM EN avant écriture. Les pointeurs
non alignés dans les scripts de combat sont des opérandes du motif `20 e0 03 02`
(printstring), notamment 0x9655d4, 0x965ab6, 0x96cefb, 0x96bd4a et 0x96bd8d.
Le finaliseur PT `batch_45` réutilise l'injection bornée existante ; il valide
préimages et commandes, alloue dans l'espace libre et repointe les seuls consommateurs
du lot, après les passes génériques. Les tables restent à leur adresse et conservent
leurs autres champs. Aucun changement du code partagé ou du rendu FR/IT/DE.

Les pages FA/FB, couleurs FC et variables FD gardent leurs octets et leur ordre.
Les retours FE sont positionnés pour deux lignes par page et des noms développés.
Budgets : 208 px pour les répliques, 224 px pour les messages de combat ; mesures
sur les cinq polices moteur réelles, tildes PT appliqués, avec noms de Pokémon maximaux,
préfixe adverse, noms de mouvements/objets et type développés. Les tailles encodées
et terminateurs sont contrôlés ; la relocalisation évite tout débordement de cellule.

## Bilan offset par offset

| Offset | Résultat | Sites de pointeurs EN |
|---|---|---|
| `0xa479fa` | traduit / contrôlé par les tests source et ROM | `0xa6fc14` |
| `0xa47a09` | traduit / contrôlé par les tests source et ROM | `0xa6fc20` |
| `0xa47a38` | traduit / contrôlé par les tests source et ROM | `0xa6fc24` |
| `0xa47a77` | traduit / contrôlé par les tests source et ROM | `0xa6fc28` |
| `0xa47ab3` | traduit / contrôlé par les tests source et ROM | `0xa6fc34` |
| `0xa47aef` | traduit / contrôlé par les tests source et ROM | `0xa6fc38` |
| `0xa47b1f` | traduit / contrôlé par les tests source et ROM | `0xa6fc3c` |
| `0xa47b4b` | traduit / contrôlé par les tests source et ROM | `0xa6fc48` |
| `0xa47b7c` | traduit / contrôlé par les tests source et ROM | `0xa6fc4c` |
| `0xa47b98` | traduit / contrôlé par les tests source et ROM | `0xa6fc50` |
| `0xa47bbe` | traduit / contrôlé par les tests source et ROM | `0xa6fc5c` |
| `0xa47bf4` | traduit / contrôlé par les tests source et ROM | `0xa6fc60` |
| `0xa47c30` | traduit / contrôlé par les tests source et ROM | `0xa6fc64` |
| `0xa47c62` | traduit / contrôlé par les tests source et ROM | `0xa6fc70` |
| `0xa47c7e` | traduit / contrôlé par les tests source et ROM | `0xa6fc74` |
| `0xa47ca2` | traduit / contrôlé par les tests source et ROM | `0xa6fc78` |
| `0xa47cc9` | traduit / contrôlé par les tests source et ROM | `0xa6fc84` |
| `0xa47cfc` | traduit / contrôlé par les tests source et ROM | `0xa6fc88` |
| `0xa47d0e` | traduit / contrôlé par les tests source et ROM | `0xa6fc8c` |
| `0xa47d1d` | traduit / contrôlé par les tests source et ROM | `0xa6fc98` |
| `0xa47d5b` | traduit / contrôlé par les tests source et ROM | `0xa6fc9c` |
| `0xa47d6d` | traduit / contrôlé par les tests source et ROM | `0xa6fca0` |
| `0xa47d7d` | traduit / contrôlé par les tests source et ROM | `0xa6fcac` |
| `0xa47db7` | traduit / contrôlé par les tests source et ROM | `0xa6fcb0` |
| `0xa47de9` | traduit / contrôlé par les tests source et ROM | `0xa6fcb4` |
| `0xa47e1c` | traduit / contrôlé par les tests source et ROM | `0xa6fcc0` |
| `0xa47e53` | traduit / contrôlé par les tests source et ROM | `0xa6fcc4` |
| `0xa47e5f` | traduit / contrôlé par les tests source et ROM | `0xa6fcc8` |
| `0xa47e6f` | traduit / contrôlé par les tests source et ROM | `0xa6fcd4` |
| `0xa47e9e` | traduit / contrôlé par les tests source et ROM | `0xa6fcd8` |
| `0xa47ec9` | traduit / contrôlé par les tests source et ROM | `0xa6fcdc` |
| `0xa47ef7` | traduit / contrôlé par les tests source et ROM | `0xa6fce8` |
| `0xa47f25` | traduit / contrôlé par les tests source et ROM | `0xa6fcec` |
| `0xa47f52` | traduit / contrôlé par les tests source et ROM | `0xa6fcf0` |
| `0xa47f8a` | traduit / contrôlé par les tests source et ROM | `0xa6fcfc` |
| `0xa47fa0` | traduit / contrôlé par les tests source et ROM | `0xa6fd00` |
| `0xa47fc0` | traduit / contrôlé par les tests source et ROM | `0xa6fd04` |
| `0xa47fe8` | traduit / contrôlé par les tests source et ROM | `0xa6fd10` |
| `0xa48018` | traduit / contrôlé par les tests source et ROM | `0xa6fd14` |
| `0xa4805a` | traduit / contrôlé par les tests source et ROM | `0xa6fd18` |
| `0xa48090` | traduit / contrôlé par les tests source et ROM | `0xa6fd24` |
| `0xa480c9` | traduit / contrôlé par les tests source et ROM | `0xa6fd28` |
| `0xa48102` | traduit / contrôlé par les tests source et ROM | `0xa6fd2c` |
| `0xa4812b` | traduit / contrôlé par les tests source et ROM | `0xa6fd38` |
| `0xa48151` | traduit / contrôlé par les tests source et ROM | `0xa6fd3c` |
| `0xa4816a` | traduit / contrôlé par les tests source et ROM | `0xa6fd40` |
| `0xa48183` | traduit / contrôlé par les tests source et ROM | `0xa6fd4c` |
| `0xa481ba` | traduit / contrôlé par les tests source et ROM | `0xa6fd50` |
| `0xa481dc` | traduit / contrôlé par les tests source et ROM | `0xa6fd54` |
| `0xa481f3` | traduit / contrôlé par les tests source et ROM | `0xa6fd60` |
| `0xa48226` | traduit / contrôlé par les tests source et ROM | `0xa6fd64` |
| `0xa48262` | traduit / contrôlé par les tests source et ROM | `0xa6fd68` |
| `0xa48293` | traduit / contrôlé par les tests source et ROM | `0xa6fd74` |
| `0xa482bc` | traduit / contrôlé par les tests source et ROM | `0xa6fd78` |
| `0xa482cf` | traduit / contrôlé par les tests source et ROM | `0xa6fd7c` |
| `0xa482e7` | traduit / contrôlé par les tests source et ROM | `0xa6fd88` |
| `0xa48323` | traduit / contrôlé par les tests source et ROM | `0xa6fd8c` |
| `0xa48362` | traduit / contrôlé par les tests source et ROM | `0xa6fd90` |
| `0xa48395` | traduit / contrôlé par les tests source et ROM | `0xa6fd9c` |
| `0xa483bb` | traduit / contrôlé par les tests source et ROM | `0xa6fda0` |
| `0xa483dc` | traduit / contrôlé par les tests source et ROM | `0xa6fda4` |
| `0xa483f9` | traduit / contrôlé par les tests source et ROM | `0xa6fdb0` |
| `0xa48438` | traduit / contrôlé par les tests source et ROM | `0xa6fdb4` |
| `0xa48463` | traduit / contrôlé par les tests source et ROM | `0xa6fdb8` |
| `0xa48477` | traduit / contrôlé par les tests source et ROM | `0xa6fdc4` |
| `0xa484b3` | traduit / contrôlé par les tests source et ROM | `0xa6fdc8` |
| `0xa484eb` | traduit / contrôlé par les tests source et ROM | `0xa6fdcc` |
| `0xa48522` | traduit / contrôlé par les tests source et ROM | `0xa6fdd8` |
| `0xa4854c` | traduit / contrôlé par les tests source et ROM | `0xa6fddc` |
| `0xa48567` | traduit / contrôlé par les tests source et ROM | `0xa6fde0` |
| `0xa4858b` | traduit / contrôlé par les tests source et ROM | `0xa6fdec` |
| `0xa48592` | traduit / contrôlé par les tests source et ROM | `0xa6fdf0` |
| `0xa485b6` | traduit / contrôlé par les tests source et ROM | `0xa6fdf4` |
| `0xa485df` | traduit / contrôlé par les tests source et ROM | `0xa6fe00` |
| `0xa48609` | traduit / contrôlé par les tests source et ROM | `0xa6fe04` |
| `0xa4862b` | traduit / contrôlé par les tests source et ROM | `0xa6fe08` |
| `0xa4866d` | traduit / contrôlé par les tests source et ROM | `0xa6fe14` |
| `0xa4869a` | traduit / contrôlé par les tests source et ROM | `0xa6fe18` |
| `0xa486b6` | traduit / contrôlé par les tests source et ROM | `0xa6fe1c` |
| `0xa486f7` | traduit / contrôlé par les tests source et ROM | `0xa6fe28` |
| `0xa48727` | traduit / contrôlé par les tests source et ROM | `0xa6fe2c` |
| `0xa4874e` | traduit / contrôlé par les tests source et ROM | `0xa6fe30` |
| `0xa48774` | traduit / contrôlé par les tests source et ROM | `0xa6fe3c` |
| `0xa487a6` | traduit / contrôlé par les tests source et ROM | `0xa6fe40` |
| `0xa487c6` | traduit / contrôlé par les tests source et ROM | `0xa6fe44` |
| `0xa487f5` | traduit / contrôlé par les tests source et ROM | `0xa6fe50` |
| `0xa4884f` | traduit / contrôlé par les tests source et ROM | `0xa6fe54` |
| `0xa4886b` | traduit / contrôlé par les tests source et ROM | `0xa6fe58` |
| `0xa48886` | traduit / contrôlé par les tests source et ROM | `0xa6fe64` |
| `0xa488cd` | traduit / contrôlé par les tests source et ROM | `0xa6fe68` |
| `0xa488f5` | traduit / contrôlé par les tests source et ROM | `0xa6fe6c` |
| `0xa4892a` | traduit / contrôlé par les tests source et ROM | `0xa6fe78` |
| `0xa48968` | traduit / contrôlé par les tests source et ROM | `0xa6fe7c` |
| `0xa48999` | traduit / contrôlé par les tests source et ROM | `0xa6fe80` |
| `0xa489bf` | traduit / contrôlé par les tests source et ROM | `0xa6fe8c` |
| `0xa489e7` | traduit / contrôlé par les tests source et ROM | `0xa6fe90` |
| `0xa48a0f` | traduit / contrôlé par les tests source et ROM | `0xa6fe94` |
| `0xa48a3d` | traduit / contrôlé par les tests source et ROM | `0xa6fea0` |
| `0xa48a58` | traduit / contrôlé par les tests source et ROM | `0xa6fea4` |
| `0xa48a74` | traduit / contrôlé par les tests source et ROM | `0xa6fea8` |
| `0xa48a92` | traduit / contrôlé par les tests source et ROM | `0xa6feb4` |
| `0xa48abe` | traduit / contrôlé par les tests source et ROM | `0xa6feb8` |
| `0xa48aed` | traduit / contrôlé par les tests source et ROM | `0xa6febc` |
| `0xa48b12` | traduit / contrôlé par les tests source et ROM | `0xa6fec8` |
| `0xa48b51` | traduit / contrôlé par les tests source et ROM | `0xa6fecc` |
| `0xa48b8f` | traduit / contrôlé par les tests source et ROM | `0xa6fed0` |
| `0xa48bc3` | traduit / contrôlé par les tests source et ROM | `0xa6fedc` |
| `0xa48bdd` | traduit / contrôlé par les tests source et ROM | `0xa6fee0` |
| `0xa48c01` | traduit / contrôlé par les tests source et ROM | `0xa6fee4` |
| `0xa48c45` | traduit / contrôlé par les tests source et ROM | `0xa6fef0` |
| `0xa48c64` | traduit / contrôlé par les tests source et ROM | `0xa6fef4` |
| `0xa48c91` | traduit / contrôlé par les tests source et ROM | `0xa6fef8` |
| `0xa48cbb` | traduit / contrôlé par les tests source et ROM | `0xa6ff04` |
| `0xa48ced` | traduit / contrôlé par les tests source et ROM | `0xa6ff08` |
| `0xa48d1d` | traduit / contrôlé par les tests source et ROM | `0xa6ff0c` |
| `0xa48d3e` | traduit / contrôlé par les tests source et ROM | `0xa6ff18` |
| `0xa48d62` | traduit / contrôlé par les tests source et ROM | `0xa6ff1c` |
| `0xa48d75` | traduit / contrôlé par les tests source et ROM | `0xa6ff20` |
| `0xa48d99` | traduit / contrôlé par les tests source et ROM | `0xa6ff2c` |
| `0xa48ddc` | traduit / contrôlé par les tests source et ROM | `0xa6ff30` |
| `0xa48e18` | traduit / contrôlé par les tests source et ROM | `0xa6ff34` |
| `0xa48e2d` | traduit / contrôlé par les tests source et ROM | `0xa6ff40` |
| `0xa48e57` | traduit / contrôlé par les tests source et ROM | `0xa6ff44` |
| `0xa48e81` | traduit / contrôlé par les tests source et ROM | `0xa6ff48` |
| `0xa48ea6` | traduit / contrôlé par les tests source et ROM | `0xa6ff54` |
| `0xa48edc` | traduit / contrôlé par les tests source et ROM | `0xa6ff58` |
| `0xa48eff` | traduit / contrôlé par les tests source et ROM | `0xa6ff5c` |
| `0xa48f2f` | traduit / contrôlé par les tests source et ROM | `0xa6ff68` |
| `0xa48f72` | traduit / contrôlé par les tests source et ROM | `0xa6ff6c` |
| `0xa48fac` | traduit / contrôlé par les tests source et ROM | `0xa6ff70` |
| `0xa48fe4` | traduit / contrôlé par les tests source et ROM | `0xa6ff7c` |
| `0xa48ffe` | traduit / contrôlé par les tests source et ROM | `0xa6ff80` |
| `0xa49024` | traduit / contrôlé par les tests source et ROM | `0xa6ff84` |
| `0xa4903b` | traduit / contrôlé par les tests source et ROM | `0xa6ff90` |
| `0xa49055` | traduit / contrôlé par les tests source et ROM | `0xa6ff94` |
| `0xa4908b` | traduit / contrôlé par les tests source et ROM | `0xa6ff98` |
| `0xa490a9` | traduit / contrôlé par les tests source et ROM | `0xa6ffa4` |
| `0xa490d5` | traduit / contrôlé par les tests source et ROM | `0xa6ffa8` |
| `0xa490e3` | traduit / contrôlé par les tests source et ROM | `0xa6ffac` |
| `0xa49101` | traduit / contrôlé par les tests source et ROM | `0xa6ffb8` |
| `0xa49117` | traduit / contrôlé par les tests source et ROM | `0xa6ffbc` |
| `0xa4913e` | traduit / contrôlé par les tests source et ROM | `0xa6ffc0` |
| `0xa4915f` | traduit / contrôlé par les tests source et ROM | `0xa6ffcc` |
| `0xa49190` | traduit / contrôlé par les tests source et ROM | `0xa6ffd0` |
| `0xa491c5` | traduit / contrôlé par les tests source et ROM | `0xa6ffd4` |
| `0xa491dc` | traduit / contrôlé par les tests source et ROM | `0xa6ffe0` |
| `0xa491ea` | traduit / contrôlé par les tests source et ROM | `0xa6ffe4` |
| `0xa491fd` | traduit / contrôlé par les tests source et ROM | `0xa6ffe8` |
| `0xa4921b` | traduit / contrôlé par les tests source et ROM | `0xa6fff4` |
| `0xa49247` | traduit / contrôlé par les tests source et ROM | `0xa6fff8` |
| `0xa49273` | traduit / contrôlé par les tests source et ROM | `0xa6fffc` |
| `0xa49299` | traduit / contrôlé par les tests source et ROM | `0xa70008` |
| `0xa492d8` | traduit / contrôlé par les tests source et ROM | `0xa7000c` |
| `0xa492fb` | traduit / contrôlé par les tests source et ROM | `0xa70010` |
| `0xa49308` | traduit / contrôlé par les tests source et ROM | `0xa7001c` |
| `0xa49346` | traduit / contrôlé par les tests source et ROM | `0xa70020` |
| `0xa4938c` | traduit / contrôlé par les tests source et ROM | `0xa70024` |
| `0xa493c6` | traduit / contrôlé par les tests source et ROM | `0xa70030` |
| `0xa49400` | traduit / contrôlé par les tests source et ROM | `0xa70034` |
| `0xa49439` | traduit / contrôlé par les tests source et ROM | `0xa70038` |
| `0xa49477` | traduit / contrôlé par les tests source et ROM | `0xa70044` |
| `0xa494a3` | traduit / contrôlé par les tests source et ROM | `0xa70048` |
| `0xa494d2` | traduit / contrôlé par les tests source et ROM | `0xa7004c` |
| `0xa49509` | traduit / contrôlé par les tests source et ROM | `0xa70058` |
| `0xa4952c` | traduit / contrôlé par les tests source et ROM | `0xa7005c` |
| `0xa4954e` | traduit / contrôlé par les tests source et ROM | `0xa70060` |
| `0xa49576` | traduit / contrôlé par les tests source et ROM | `0xa7006c` |
| `0xa495ad` | traduit / contrôlé par les tests source et ROM | `0xa70070` |
| `0xa495e5` | traduit / contrôlé par les tests source et ROM | `0xa70074` |
| `0xa49618` | traduit / contrôlé par les tests source et ROM | `0xa70080` |
| `0xa49651` | traduit / contrôlé par les tests source et ROM | `0xa70084` |
| `0xa49697` | traduit / contrôlé par les tests source et ROM | `0xa70088` |
| `0xa4969d` | traduit / contrôlé par les tests source et ROM | `0xa70094` |
| `0xa496dc` | traduit / contrôlé par les tests source et ROM | `0xa70098` |
| `0xa49719` | traduit / contrôlé par les tests source et ROM | `0xa7009c` |
| `0xa49767` | traduit / contrôlé par les tests source et ROM | `0xa700a8` |
| `0xa497ad` | traduit / contrôlé par les tests source et ROM | `0xa700ac` |
| `0xa497e6` | traduit / contrôlé par les tests source et ROM | `0xa700b0` |
| `0xa4982a` | traduit / contrôlé par les tests source et ROM | `0xa700bc` |
| `0xa49867` | traduit / contrôlé par les tests source et ROM | `0xa700c0` |
| `0xa498af` | traduit / contrôlé par les tests source et ROM | `0xa700c4` |
| `0xa498ea` | traduit / contrôlé par les tests source et ROM | `0xa700d0` |
| `0xa4992a` | traduit / contrôlé par les tests source et ROM | `0xa700d4` |
| `0xa49967` | traduit / contrôlé par les tests source et ROM | `0xa700d8` |
| `0xa499aa` | traduit / contrôlé par les tests source et ROM | `0xa700e4` |
| `0xa499e3` | traduit / contrôlé par les tests source et ROM | `0xa700e8` |
| `0xa49a17` | traduit / contrôlé par les tests source et ROM | `0xa700ec` |
| `0xa49a65` | traduit / contrôlé par les tests source et ROM | `0xa700f8` |
| `0xa49aa0` | traduit / contrôlé par les tests source et ROM | `0xa700fc` |
| `0xa49af2` | traduit / contrôlé par les tests source et ROM | `0xa70100` |
| `0xa49b3e` | traduit / contrôlé par les tests source et ROM | `0xa7010c` |
| `0xa49b6a` | traduit / contrôlé par les tests source et ROM | `0xa70110` |
| `0xa49b9d` | traduit / contrôlé par les tests source et ROM | `0xa70114` |
| `0xa49bd3` | traduit / contrôlé par les tests source et ROM | `0xa70120` |
| `0xa49c0a` | traduit / contrôlé par les tests source et ROM | `0xa70124` |
| `0xa49c34` | traduit / contrôlé par les tests source et ROM | `0xa70128` |
| `0xa49c59` | traduit / contrôlé par les tests source et ROM | `0xa70134` |
| `0xa49c8b` | traduit / contrôlé par les tests source et ROM | `0xa70138` |
| `0xa49cb5` | traduit / contrôlé par les tests source et ROM | `0xa7013c` |
| `0xa49ccb` | traduit / contrôlé par les tests source et ROM | `0xa70148` |
| `0xa49d05` | traduit / contrôlé par les tests source et ROM | `0xa7014c` |
| `0xa49d45` | traduit / contrôlé par les tests source et ROM | `0xa70150` |
| `0xa49d74` | traduit / contrôlé par les tests source et ROM | `0xa7015c` |
| `0xa49db9` | traduit / contrôlé par les tests source et ROM | `0xa70160` |
| `0xa49e02` | traduit / contrôlé par les tests source et ROM | `0xa70164` |
| `0xa49e36` | traduit / contrôlé par les tests source et ROM | `0xa70170` |
| `0xa49e76` | traduit / contrôlé par les tests source et ROM | `0xa70174` |
| `0xa49eb9` | traduit / contrôlé par les tests source et ROM | `0xa70178` |
| `0xa49efa` | traduit / contrôlé par les tests source et ROM | `0xa6f1a8`, `0xa6f1dc` |
| `0xa49f24` | traduit / contrôlé par les tests source et ROM | `0xa6f1ac`, `0xa6f1e0` |
| `0xa49f5f` | traduit / contrôlé par les tests source et ROM | `0xa6f210`, `0xa6f244` |
| `0xa49fa3` | traduit / contrôlé par les tests source et ROM | `0xa6f214`, `0xa6f248` |
| `0xa4a02d` | traduit / contrôlé par les tests source et ROM | `0xa6f278`, `0xa6f2ac` |
| `0xa4a061` | traduit / contrôlé par les tests source et ROM | `0xa6f27c`, `0xa6f2b0` |
| `0xa4a0b1` | traduit / contrôlé par les tests source et ROM | `0xa6f378` |
| `0xa4a13e` | traduit / contrôlé par les tests source et ROM | `0xa6f37c` |
| `0xa4a155` | traduit / contrôlé par les tests source et ROM | `0xa6f380` |
| `0xa4a18e` | traduit / contrôlé par les tests source et ROM | `0xa6f3ac` |
| `0xa4a213` | traduit / contrôlé par les tests source et ROM | `0xa6f3b0` |
| `0xa4a241` | traduit / contrôlé par les tests source et ROM | `0xa6f3b4` |
| `0xa4a28f` | traduit / contrôlé par les tests source et ROM | `0xa6f3e0` |
| `0xa4a2e9` | traduit / contrôlé par les tests source et ROM | `0xa6f3e4` |
| `0xa4a31c` | traduit / contrôlé par les tests source et ROM | `0xa6f3e8` |
| `0xa4a34b` | traduit / contrôlé par les tests source et ROM | `0xa6f414` |
| `0xa4a3e0` | traduit / contrôlé par les tests source et ROM | `0xa6f418` |
| `0xa4a417` | traduit / contrôlé par les tests source et ROM | `0xa6f41c` |
| `0xa4a45c` | traduit / contrôlé par les tests source et ROM | `0xa6f448` |
| `0xa4a4a1` | traduit / contrôlé par les tests source et ROM | `0xa6f44c` |
| `0xa4a4df` | traduit / contrôlé par les tests source et ROM | `0xa6f450` |
| `0xa4a514` | traduit / contrôlé par les tests source et ROM | `0xa6f4b0` |
| `0xa4a5b5` | traduit / contrôlé par les tests source et ROM | `0xa6f2e0`, `0xa6f314`, `0xa6f348`, `0xa6f4b4` |
| `0xa4a5e8` | traduit / contrôlé par les tests source et ROM | `0xa6f2e4`, `0xa6f318`, `0xa6f34c`, `0xa6f4b8` |
| `0xa4a617` | traduit / contrôlé par les tests source et ROM | `0xa6f4e4` |
| `0xa4a6c2` | traduit / contrôlé par les tests source et ROM | `0xa6f4e8` |
| `0xa4a6f3` | traduit / contrôlé par les tests source et ROM | `0xa6f4ec` |
| `0xa4a727` | traduit / contrôlé par les tests source et ROM | `0xa6f518` |
| `0xa4a817` | traduit / contrôlé par les tests source et ROM | `0xa6f51c` |
| `0xa4a848` | traduit / contrôlé par les tests source et ROM | `0xa6f520` |
| `0xa4a875` | traduit / contrôlé par les tests source et ROM | `0xa6f54c` |
| `0xa4a8a8` | traduit / contrôlé par les tests source et ROM | `0xa6f550` |
| `0xa4a8b9` | traduit / contrôlé par les tests source et ROM | `0xa6f554` |
| `0xa4a8dd` | exception : préfixe 00 c0 46 sans consommateur | aucun ; début réel `0xa4a8e0` via `0x9eb8f4` |
| `0xa4a8e0` | traduit / contrôlé par les tests source et ROM | `0x9eb8f4` |
| `0xa4a8fc` | traduit / contrôlé par les tests source et ROM | `0x9eb8f0` |
| `0xa4a922` | traduit / contrôlé par les tests source et ROM | `0x9eb90c` |
| `0xa4a941` | traduit / contrôlé par les tests source et ROM | `0x9eb908` |
| `0xa4a96a` | traduit / contrôlé par les tests source et ROM | `0x9eb928` |
| `0xa4a98c` | traduit / contrôlé par les tests source et ROM | `0x3fe270` |
| `0xa4a9a2` | traduit / contrôlé par les tests source et ROM | `0x9eb4d4` |
| `0xa4a9c4` | traduit / contrôlé par les tests source et ROM | `0x9eb4c4` |
| `0xa4a9f0` | traduit / contrôlé par les tests source et ROM | `0x9b7560` |
| `0xa4aa0b` | traduit / contrôlé par les tests source et ROM | `0x9b7570` |
| `0xa4aa55` | traduit / contrôlé par les tests source et ROM | `0x9b7578` |
| `0xa4aa96` | traduit / contrôlé par les tests source et ROM | `0x9b753c` |
| `0xa4aaab` | traduit / contrôlé par les tests source et ROM | `0x9b757c`, `0xa0a9ec` |
| `0xa4aad5` | traduit / contrôlé par les tests source et ROM | `0x9b7670` |
| `0xa4aaff` | traduit / contrôlé par les tests source et ROM | `0x9b7680` |
| `0xa4ab14` | traduit / contrôlé par les tests source et ROM | `0x9fc668`, `0xb2a440` |
| `0xa4ab45` | traduit / contrôlé par les tests source et ROM | `0x9fc674`, `0xb2a454` |
| `0xa4ab6a` | traduit / contrôlé par les tests source et ROM | `0x9fc678`, `0xb2a458` |
| `0xa4ab8e` | traduit / contrôlé par les tests source et ROM | `0x9fc67c`, `0xb2a45c` |
| `0xa4aba9` | traduit / contrôlé par les tests source et ROM | `0x9b7904` |
| `0xa4abc2` | traduit / contrôlé par les tests source et ROM | `0x3fe030` |
| `0xa4abdb` | traduit / contrôlé par les tests source et ROM | `0x9655d4`, `0x965ab6` |
| `0xa4abf4` | traduit / contrôlé par les tests source et ROM | `0x9b790c` |
| `0xa4ac0d` | traduit / contrôlé par les tests source et ROM | `0x965ad0` |
| `0xa4ac2f` | traduit / contrôlé par les tests source et ROM | `0x9b7b6c` |
| `0xa4ac4f` | traduit / contrôlé par les tests source et ROM | `0x9b7b78` |
| `0xa4ac7e` | traduit / contrôlé par les tests source et ROM | `0x9b7b7c` |
| `0xa4ac92` | traduit / contrôlé par les tests source et ROM | `0x9b7b8c` |
| `0xa4aca8` | traduit / contrôlé par les tests source et ROM | `0x9b80b8` |
| `0xa4accf` | traduit / contrôlé par les tests source et ROM | `0x9b80c0` |
| `0xa4ad04` | traduit / contrôlé par les tests source et ROM | `0x9b83c4`, `0x9b83c8`, `0x9b83e0` |
| `0xa4ad14` | traduit / contrôlé par les tests source et ROM | `0x96cefb`, `0x9b83dc` |
| `0xa4ad31` | traduit / contrôlé par les tests source et ROM | `0xa0a4f0` |
| `0xa4ad51` | traduit / contrôlé par les tests source et ROM | `0xa0a4d8` |
| `0xa4ad67` | traduit / contrôlé par les tests source et ROM | `0xa0a0cc` |
| `0xa4ad92` | traduit / contrôlé par les tests source et ROM | `0x96bd4a` |
| `0xa4adab` | traduit / contrôlé par les tests source et ROM | `0x96bd8d`, `0x9cb024`, `0x9ec564` |
| `0xa4adcb` | traduit / contrôlé par les tests source et ROM | `0x9ed510` |
| `0xa4adec` | traduit / contrôlé par les tests source et ROM | `0x9ed51c` |
| `0xa4ae24` | traduit / contrôlé par les tests source et ROM | `0x9ed520` |
| `0xa4ae43` | traduit / contrôlé par les tests source et ROM | `0x9ed524` |

## Validation reproductible

- `python3 -m pytest -q tests/unit/pt/test_batch_pt45.py tests/unit/test_translation_integrity.py`
- `make build-pt`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt45_rom.py -m rom`
- `npx playwright test --config tests/e2e-playwright/playwright.pt45.config.ts`

Playwright démarre mGBA avec Qt offscreen sur une copie privée de la ROM bâtie.
La sonde msgbox native lit trois vrais pointeurs du lot, vérifie leurs octets puis
contrôle le texte affiché par OCR. Elle ne remplace ni les glyphes ni les fenêtres.
La sauvegarde fixture est copiée, vérifiée intacte et jamais écrite en jeu.
La capture est enregistrée dans le temporaire système et jointe au ticket.

## Non vérifié

Le parcours manuel complet de chaque Dresseur et de chaque effet de combat relève
de la certification T-848. La sonde visuelle ne prétend pas jouer les 282 situations ;
les tests binaires contrôlent toutes les chaînes aux pointeurs vivants.
