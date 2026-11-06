# PT-83 — Battle Frontier (F-842)

Périmètre : les 299 clés explicites du manifeste PT-83. Pré requis intégrés :
F-758 (polices/tildes) et F-759 (glossaire dcc6ce5d). Domaines réels : Battle
Mine, partenaires de combat, Battle Sands, Battle Tower, règles des formats,
démonstration et services du Battle Frontier.

292 valeurs protégées, dont noms propres conservés conformément au glossaire.
Sept exceptions documentées ci-dessous. Les sources EN/FR au même offset,
préimages intégrales de la ROM, pointeurs et preuves audio sont conservés dans
`languages/pt/data/pt83_audit.json`. Les textes EN tronqués sont complétés depuis
la ROM sans importer les erreurs ou omissions de la version française.

Le finaliseur `batch_83` réutilise le moteur de relocalisation atomique existant.
Il repointe exclusivement les lecteurs audités, y compris les tables de menus ;
aucune cellule texte de table fixe ne fait partie de ce lot. Le préfixe
00 C0 46 avant le vrai nom Battle Tower est préservé. Les coïncidences d'adresses
à l'intérieur des échantillons audio ne sont jamais des lecteurs texte.

Les codes FC/FD/F8, les pages FB et les défilements FA restent dans leur ordre
exact. Les retours de ligne sont adaptés au portugais. Les mesures utilisent
les cinq polices latines réelles, tildes inclus, avec noms joueur de 7 glyphes,
surnoms de 10 glyphes, compteurs de cinq chiffres et catégories longues.
Les valeurs de chaque buffer et les mesures sont figées dans le bilan JSON.
FD07 est un contrôle de couleur dans les explications de formats, et non un
mot visible. Le buffer pluriel anglais « s » complète « vitória », jamais
« vez ». L'espace final de « Equipe » est encodé explicitement par `<0x00>`.

## Validation reproductible

- `python3 -m pytest tests/unit/pt/test_batch_pt83.py tests/unit/test_translation_integrity.py -q`
- `make build-pt`
- `python3 -m pytest tests/e2e/pt/test_batch_pt83_rom.py -m rom -q`
- `npx playwright test --config tests/e2e-playwright/playwright.pt83.config.ts`

La sonde Playwright ouvre de véritables msgbox mGBA dans une copie temporaire
avec les pointeurs du build final. OCR des premières lignes de trois textes,
aucune sauvegarde, aucune fenêtre visible ; capture dans le répertoire temporaire
système. Les autres pages sont couvertes par comparaison binaire complète.
Ce contrôle ne prétend pas parcourir toutes les épreuves du Battle Frontier.

## Bilan individuel

| Offset | État | Lecteurs / justification |
|---|---|---|
| `0x1f8c7c5` | Traduit / contrôlé | 0x1e9e5b7 |
| `0x1f8c803` | Traduit / contrôlé | 0x1e9ec41 |
| `0x1f8c84e` | Traduit / contrôlé | 0x1e9e506, 0x1e9e770, 0x1e9e7ec |
| `0x1f8c85a` | Traduit / contrôlé | 0x1e9e514, 0x1e9e77e, 0x1e9e879 |
| `0x1f8c86a` | Traduit / contrôlé | 0x1e9e522, 0x1e9e78c, 0x1e9e906 |
| `0x1f8c878` | Traduit / contrôlé | 0x1e9e530, 0x1e9e79a, 0x1e9e97a |
| `0x1f8c88a` | Traduit / contrôlé | 0x1e9ed16 |
| `0x1f8c8c9` | Traduit / contrôlé | 0x1e9ed9a |
| `0x1f8c8fd` | Traduit / contrôlé | 0x1e9eec0 |
| `0x1f8c9f3` | Traduit / contrôlé | 0x1e9f020 |
| `0x1f8cafa` | Traduit / contrôlé | 0x1e9f078 |
| `0x1f8cc05` | Traduit / contrôlé | 0x1e9f041, 0x1e9f099, 0x1e9f13b, 0x1e9f152 |
| `0x1f8cc0b` | Traduit / contrôlé | 0x1e9f04c |
| `0x1f8cd94` | Traduit / contrôlé | 0x1e9f0a4 |
| `0x1f8ceaa` | Traduit / contrôlé | 0x1e9f146 |
| `0x1f8d026` | Traduit / contrôlé | 0x1e9f15d |
| `0x1f8d1ab` | Exception | Texte inutilisé : aucun lecteur texte direct ni intérieur dans la ROM EN. Une coïncidence binaire visant le suffixe 0x1f8d1f1 à 0x0d09bf traverse des instructions Thumb, pas un littéral pointeur. Les lecteurs des chaînes voisines sont distincts ; aucune cellule fixe identifiée. |
| `0x1f8d227` | Traduit / contrôlé | 0x1e9ee2a, 0x1e9f119 |
| `0x1f8d236` | Traduit / contrôlé | 0x1e9ec51 |
| `0x1f8d32c` | Traduit / contrôlé | 0x1e54ce8, 0x1e54e45, 0x1e54fa2, 0x1e550ff, 0x1e5525c, 0x1e553b9, 0x1e55516, 0x1e55673, 0x1e9ed3b, 0x1e9f44f, 0x1e9f683, 0x1ea01f1, 0x1ea3449, 0x1ea362e, 0x1ea5173, 0x1ea5697 |
| `0x1f8d35a` | Traduit / contrôlé | 0x1e9ee23, 0x1ea02d6, 0x1ea3495, 0x1ea570c |
| `0x1f8d393` | Traduit / contrôlé | 0x1ea02dc, 0x1ea51dd |
| `0x1f8d3cc` | Traduit / contrôlé | 0x1ea5770 |
| `0x1f8d406` | Traduit / contrôlé | 0x1ea5cb6 |
| `0x1f8d44f` | Traduit / contrôlé | 0x1ea5cbc |
| `0x1f8d49e` | Traduit / contrôlé | 0x1ea5ccd |
| `0x1f8d4ec` | Traduit / contrôlé | 0x1ea5cd3 |
| `0x1f8d540` | Traduit / contrôlé | 0x1e9ee3b, 0x1ea02f4, 0x1ea34f4, 0x1ea5263, 0x1ea57cc |
| `0x1f8d608` | Traduit / contrôlé | 0x1e8118b, 0x1e811bc, 0x1ea1002, 0x1ea10b3, 0x1ea1771, 0x1ea5a39 |
| `0x1f8d621` | Traduit / contrôlé | 0x1ea58d4, 0x1ea58eb, 0x1ea590e, 0x1ea5925 |
| `0x1f8d628` | Traduit / contrôlé | 0x1ea58df |
| `0x1f8d72a` | Traduit / contrôlé | 0x1ea5319, 0x1ea586e |
| `0x1f8d76b` | Traduit / contrôlé | 0x1ea531d, 0x1ea5872 |
| `0x1f8d79d` | Traduit / contrôlé | 0x1ea5919 |
| `0x1f8d88d` | Traduit / contrôlé | 0x1ea58f6 |
| `0x1f8d951` | Traduit / contrôlé | 0x1ea5930 |
| `0x1f8da71` | Traduit / contrôlé | 0x1e9f11f, 0x1ea3615, 0x1ea5375, 0x1ea58b8 |
| `0x1f8dae1` | Traduit / contrôlé | 0x1e9edf2, 0x1ea02a2, 0x1ea02bf, 0x1ea521d, 0x1ea523a, 0x1ea573c, 0x1ea5759 |
| `0x1f8db49` | Traduit / contrôlé | 0x1ea57a3 |
| `0x1f8db8d` | Traduit / contrôlé | 0x1ea5cff, 0x1ea5d5d |
| `0x1f8dbc8` | Traduit / contrôlé | 0x1ea5d97 |
| `0x1f8dc93` | Traduit / contrôlé | 0x1ea5e3a |
| `0x1f8dd0f` | Traduit / contrôlé | 0x1e9ee47, 0x1e9f4a7, 0x1ea577c, 0x1ea59fb |
| `0x1f8dd1a` | Traduit / contrôlé | 0x1e9ee55, 0x1ea5a09 |
| `0x1f8dd1f` | Traduit / contrôlé | 0x1e54c33, 0x1e54d90, 0x1e54eed, 0x1e5504a, 0x1e551a7, 0x1e55304, 0x1e55461, 0x1e555be, 0x1e9f4b5, 0x1ea578a |
| `0x1f8dd26` | Traduit / contrôlé | 0x1ea5252, 0x1ea536f, 0x1ea57bb, 0x1ea58b2 |
| `0x1f8dd33` | Traduit / contrôlé | 0x1e709fb, 0x1e9ee30, 0x1ea34e9, 0x1ea5258, 0x1ea57c1, 0x1eab91d |
| `0x1f8dd36` | Traduit / contrôlé | 0x1e9ee36, 0x1ea34ef, 0x1ea525e, 0x1ea57c7 |
| `0x1f8dd3c` | Traduit / contrôlé | 0x1ea3bd8, 0x1ea3c2c, 0x1ea3c62, 0x1ea3c9c |
| `0x1f8dd7f` | Traduit / contrôlé | 0x1ea3c4f, 0x1ea3c89 |
| `0x1f8ddf7` | Traduit / contrôlé | 0x1ea3fe0 |
| `0x1f8de48` | Traduit / contrôlé | 0x1ea4073 |
| `0x1f8de99` | Traduit / contrôlé | 0x1ea3cc4 |
| `0x1f8df40` | Traduit / contrôlé | 0x1ea3ce5 |
| `0x1f8df76` | Traduit / contrôlé | 0x1ea3d21 |
| `0x1f8dfa2` | Traduit / contrôlé | 0x1ea3d41 |
| `0x1f8dfc3` | Traduit / contrôlé | 0x1ea3d59 |
| `0x1f8e006` | Traduit / contrôlé | 0x1ea3d7a |
| `0x1f8e03a` | Traduit / contrôlé | 0x1ea3db6 |
| `0x1f8e064` | Traduit / contrôlé | 0x1ea3dd6 |
| `0x1f8e081` | Traduit / contrôlé | 0x1ea3e83 |
| `0x1f8e0ab` | Traduit / contrôlé | 0x1ea3ea4 |
| `0x1f8e0cd` | Traduit / contrôlé | 0x1ea3ee0 |
| `0x1f8e0f0` | Traduit / contrôlé | 0x1ea3f00 |
| `0x1f8e125` | Traduit / contrôlé | 0x1ea3dee |
| `0x1f8e179` | Traduit / contrôlé | 0x1ea3e0f |
| `0x1f8e19b` | Traduit / contrôlé | 0x1ea3e4b |
| `0x1f8e1c8` | Traduit / contrôlé | 0x1ea3e6b |
| `0x1f8e1e9` | Traduit / contrôlé | 0x1ea3f62 |
| `0x1f8e1ee` | Traduit / contrôlé | 0x1ea3f5b |
| `0x1f8e1f3` | Exception | Clé d'extraction commençant dans un octet de bourrage 00, sans lecteur propre. Les lecteurs réels ciblent 0x1f8e1f4, entrée suivante du même lot ; traduction et vérification assurées par cette entrée, aucun doublon injecté. |
| `0x1f8e1f4` | Traduit / contrôlé | 0x1e9f738, 0x1e9f753, 0x1e9f76e, 0x1e9f786, 0x1e9f7a1, 0x1e9f7bc, 0x1e9f7f0, 0x1e9f808 |
| `0x1f8e1fb` | Traduit / contrôlé | 0x1e9f18b |
| `0x1f8e229` | Traduit / contrôlé | 0x1e9f192 |
| `0x1f8e23e` | Traduit / contrôlé | 0x1e9f232 |
| `0x1f8e271` | Traduit / contrôlé | 0x1e9fa40 |
| `0x1f8e686` | Traduit / contrôlé | 0x1e9fa4d |
| `0x1f8e70f` | Traduit / contrôlé | 0x1e9fb24 |
| `0x1f8e87e` | Traduit / contrôlé | 0x1e9f210 |
| `0x1f8e893` | Traduit / contrôlé | 0x1e9fe4d |
| `0x1f8e90f` | Traduit / contrôlé | 0x1e9fe71 |
| `0x1f8e976` | Traduit / contrôlé | 0x1e9fe8a |
| `0x1f8e9ae` | Traduit / contrôlé | 0x1e9fdfe |
| `0x1f8e9f4` | Exception | Suffixe intérieur sans lecteur texte propre du dialogue 0x1f8e9ae, livré par les pointeurs du parent. Le seul match d'adresse se trouve dans un échantillon PCM M4A (preuve fournie) ; le repointer corromprait l'audio. |
| `0x1f8eab6` | Traduit / contrôlé | 0x1e9fe0b |
| `0x1f8eae7` | Traduit / contrôlé | 0x1e9fda7 |
| `0x1f8eaf0` | Traduit / contrôlé | 0x1e9fdb5, 0x1ea3a64 |
| `0x1f8eaf4` | Traduit / contrôlé | 0x1e9f2df |
| `0x1f8eb12` | Traduit / contrôlé | 0x1e9f35a |
| `0x1f8eb1a` | Traduit / contrôlé | 0x1e9f379 |
| `0x1f8ebb2` | Traduit / contrôlé | 0x1e9f3a0 |
| `0x1f8ebcc` | Traduit / contrôlé | 0x1e9f3cd |
| `0x1f8ebf3` | Traduit / contrôlé | 0x1e9f6f1 |
| `0x1f8ec20` | Traduit / contrôlé | 0x1e9f6fb |
| `0x1f8ec5c` | Traduit / contrôlé | 0x1e9f6a9 |
| `0x1f8ecc3` | Traduit / contrôlé | 0x1e9f6d5 |
| `0x1f8ed39` | Traduit / contrôlé | 0x1e9f6bb |
| `0x1f8ed62` | Traduit / contrôlé | 0x1e9f6e7 |
| `0x1f8ed84` | Traduit / contrôlé | 0x1e9f91f |
| `0x1f8edbb` | Traduit / contrôlé | 0x1e9f877 |
| `0x1f8ee2c` | Traduit / contrôlé | 0x1e9f87e |
| `0x1f8ee9d` | Traduit / contrôlé | 0x1e9f886 |
| `0x1f8eefe` | Traduit / contrôlé | 0x1e9fe9f |
| `0x1f8ef71` | Traduit / contrôlé | 0x1e9f743 |
| `0x1f8efc0` | Traduit / contrôlé | 0x1e9f75e |
| `0x1f8f012` | Traduit / contrôlé | 0x1e9f779 |
| `0x1f8f11a` | Traduit / contrôlé | 0x1e9f791 |
| `0x1f8f15b` | Traduit / contrôlé | 0x1e9f7ac |
| `0x1f8f22d` | Traduit / contrôlé | 0x1e9f7c7 |
| `0x1f8f29c` | Traduit / contrôlé | 0x1e9f7fb |
| `0x1f8f3d2` | Traduit / contrôlé | 0x1e9f813 |
| `0x1f8f5fe` | Traduit / contrôlé | 0x1fb2f8c |
| `0x1f8f60a` | Traduit / contrôlé | 0x1fb2f90 |
| `0x1f8f616` | Traduit / contrôlé | 0x1fb2f94 |
| `0x1f8f621` | Traduit / contrôlé | 0x1fb2fa0 |
| `0x1f8f630` | Traduit / contrôlé | 0x1fb2fa4 |
| `0x1f8f63b` | Exception | Clé d'extraction commençant dans un octet de bourrage 00, sans lecteur propre. Les lecteurs réels ciblent 0x1f8f63c, entrée suivante du même lot ; traduction et vérification assurées par cette entrée, aucun doublon injecté. |
| `0x1f8f63c` | Traduit / contrôlé | 0x1ea4096 |
| `0x1f8f690` | Traduit / contrôlé | 0x1ea4bf7 |
| `0x1f8f6d8` | Traduit / contrôlé | 0x1ea49b1 |
| `0x1f8f724` | Traduit / contrôlé | 0x1ea40bf, 0x1ea49bb |
| `0x1f8f756` | Traduit / contrôlé | 0x1ea4158 |
| `0x1f8f78a` | Traduit / contrôlé | 0x1ea4c2a |
| `0x1f8f7ac` | Traduit / contrôlé | 0x1ea42ba |
| `0x1f8f7ed` | Traduit / contrôlé | 0x1ea430f |
| `0x1f8f817` | Traduit / contrôlé | 0x1e9f293, 0x1ea0792, 0x1ea08ab, 0x1ea324f, 0x1ea41ea, 0x1ea4caf |
| `0x1f8f845` | Traduit / contrôlé | 0x1ea4245 |
| `0x1f8f86d` | Traduit / contrôlé | 0x1ea4d0a |
| `0x1f8f896` | Traduit / contrôlé | 0x1e54a79, 0x1ea090d, 0x1ea4d69 |
| `0x1f8f8c8` | Traduit / contrôlé | 0x1e9e6ae, 0x1e9f9bd, 0x1ea093a, 0x1ea3883, 0x1ea432f |
| `0x1f8f8eb` | Traduit / contrôlé | 0x1ea43de |
| `0x1f8fbef` | Traduit / contrôlé | 0x1ea43eb |
| `0x1f9000d` | Traduit / contrôlé | 0x1ea4bd6 |
| `0x1f90295` | Traduit / contrôlé | 0x1ea43f8 |
| `0x1f9033a` | Traduit / contrôlé | 0x1ea0a10, 0x1ea4405 |
| `0x1f9050a` | Exception | Suffixe intérieur sans lecteur texte propre du dialogue 0x1f9033a, livré par les pointeurs du parent. Le seul match d'adresse se trouve dans un échantillon PCM M4A (preuve fournie) ; le repointer corromprait l'audio. |
| `0x1f905ef` | Traduit / contrôlé | 0x1e9e750, 0x1e9fa5f, 0x1ea0a22, 0x1ea393e, 0x1ea4417 |
| `0x1f906b1` | Traduit / contrôlé | 0x1e9fa6c, 0x1ea0a2f, 0x1ea4424 |
| `0x1f9072e` | Traduit / contrôlé | 0x1e9fa78, 0x1ea0a3b, 0x1ea4430 |
| `0x1f90757` | Traduit / contrôlé | 0x1fb2d00 |
| `0x1f90803` | Traduit / contrôlé | 0x1fb2d04 |
| `0x1f90867` | Traduit / contrôlé | 0x1e9e9f3, 0x1fb2d08 |
| `0x1f9095a` | Traduit / contrôlé | 0x1e9ea83, 0x1fb2d0c |
| `0x1f909fc` | Traduit / contrôlé | 0x1e9ea5f, 0x1fb2d10 |
| `0x1f90abb` | Traduit / contrôlé | 0x1e9fb08, 0x1ea44c0, 0x1fb2d14 |
| `0x1f90c0e` | Traduit / contrôlé | 0x1ea44dc |
| `0x1f90d60` | Traduit / contrôlé | 0x1fb2d18 |
| `0x1f90ed0` | Traduit / contrôlé | 0x1e9ea05, 0x1fb2d1c |
| `0x1f90f9c` | Traduit / contrôlé | 0x1e9ea95, 0x1fb2d20 |
| `0x1f91096` | Traduit / contrôlé | 0x1e9ea71, 0x1fb2d24 |
| `0x1f911a0` | Traduit / contrôlé | 0x1ea0acb, 0x1fb2d28 |
| `0x1f91296` | Traduit / contrôlé | 0x1ea0ae7 |
| `0x1f9148e` | Traduit / contrôlé | 0x1e9ea29, 0x1fb2d2c |
| `0x1f916d8` | Traduit / contrôlé | 0x1e9ea4d, 0x1fb2d34 |
| `0x1f91970` | Traduit / contrôlé | 0x1e9ea3b, 0x1fb2d30 |
| `0x1f91b2b` | Traduit / contrôlé | 0x1e9ea17, 0x1fb2d38 |
| `0x1f91d26` | Traduit / contrôlé | 0x1fb2d3c |
| `0x1f91e48` | Traduit / contrôlé | 0x1fb2d40 |
| `0x1f91f4f` | Traduit / contrôlé | 0x1fb2d44 |
| `0x1f92055` | Traduit / contrôlé | 0x1ea38fb, 0x1ea4518 |
| `0x1f92074` | Traduit / contrôlé | 0x1e9eaf5, 0x1e9fb3f, 0x1ea0b02, 0x1ea394a, 0x1ea4532, 0x1ea4a80 |
| `0x1f9209d` | Traduit / contrôlé | 0x1e9fbdf, 0x1ea0ba2, 0x1ea4597 |
| `0x1f920e6` | Traduit / contrôlé | 0x1e9fc0e, 0x1ea0bd1, 0x1ea45c6 |
| `0x1f9210d` | Traduit / contrôlé | 0x1e9fc2f, 0x1ea0bfc, 0x1ea45fc |
| `0x1f92174` | Traduit / contrôlé | 0x1e9fc93, 0x1ea0c60, 0x1ea4660 |
| `0x1f921a0` | Traduit / contrôlé | 0x1e9fca0, 0x1ea0c6d, 0x1ea466d |
| `0x1f921de` | Traduit / contrôlé | 0x1ea467a |
| `0x1f9221f` | Traduit / contrôlé | 0x1ea4687 |
| `0x1f92268` | Traduit / contrôlé | 0x1ea0c7e, 0x1ea4698 |
| `0x1f922c6` | Traduit / contrôlé | 0x1ea0ce3, 0x1ea46fd |
| `0x1f922e7` | Traduit / contrôlé | 0x1e9fcb8, 0x1ea4714, 0x1ea4af9 |
| `0x1f9231d` | Traduit / contrôlé | 0x1e9fce4, 0x1ea4740, 0x1ea4b25 |
| `0x1f92347` | Traduit / contrôlé | 0x1e8f81e, 0x1e9eb4a, 0x1e9fcf5, 0x1ea0cf4, 0x1ea39a4, 0x1ea4751, 0x1ea4b39 |
| `0x1f923a7` | Traduit / contrôlé | 0x1e8f865, 0x1e9eb91, 0x1e9fd3c, 0x1ea0d3b, 0x1ea39eb, 0x1ea4798, 0x1ea4b83 |
| `0x1f923ea` | Traduit / contrôlé | 0x1e8f858, 0x1e9eb84, 0x1e9fd2f, 0x1ea0d2e, 0x1ea39de, 0x1ea478b, 0x1ea4b73 |
| `0x1f92412` | Traduit / contrôlé | 0x1e9eba2, 0x1e9fd4d, 0x1ea0d4c, 0x1ea39fc, 0x1ea47a9, 0x1ea4b97 |
| `0x1f924ee` | Traduit / contrôlé | 0x1e9ebd1, 0x1e9fd7c, 0x1ea0d7b, 0x1ea3a2b, 0x1ea47d8, 0x1ea4bc6 |
| `0x1f92513` | Exception | Texte inutilisé : aucun pointeur GBA direct ni intérieur vers la chaîne dans les 32 Mio EN. Les lecteurs des chaînes voisines sont distincts ; aucune cellule fixe identifiée. |
| `0x1f9253e` | Traduit / contrôlé | 0x1ea4124 |
| `0x1f92558` | Traduit / contrôlé | 0x1ea0df7, 0x1ea48a8 |
| `0x1f925f8` | Traduit / contrôlé | 0x1e9ec25, 0x1ea0e04, 0x1ea3b3b, 0x1ea48b5 |
| `0x1f9260f` | Traduit / contrôlé | 0x1ea494a |
| `0x1f92658` | Traduit / contrôlé | 0x1ea4916 |
| `0x1f926c3` | Traduit / contrôlé | 0x1ea4922 |
| `0x1f926f7` | Traduit / contrôlé | 0x1ea496c |
| `0x1f92746` | Traduit / contrôlé | 0x1ea4976 |
| `0x1f927e0` | Traduit / contrôlé | 0x1ea0f77 |
| `0x1f92818` | Traduit / contrôlé | 0x1ea0e8d |
| `0x1f928c7` | Traduit / contrôlé | 0x1ea0e94 |
| `0x1f92905` | Traduit / contrôlé | 0x1ea0f82 |
| `0x1f92927` | Traduit / contrôlé | 0x1ea0f97 |
| `0x1f92a22` | Traduit / contrôlé | 0x1ea0fa9 |
| `0x1f92ac5` | Traduit / contrôlé | 0x1ea0fbb |
| `0x1f92bc8` | Traduit / contrôlé | 0x1ea0fd0 |
| `0x1f92c5f` | Traduit / contrôlé | 0x1ea11c7 |
| `0x1f92c7b` | Traduit / contrôlé | 0x1ea1015 |
| `0x1f92cb6` | Traduit / contrôlé | 0x1ea109e |
| `0x1f92d1d` | Traduit / contrôlé | 0x1ea300f |
| `0x1f92d85` | Traduit / contrôlé | 0x1e6b82e, 0x1e6b9c4, 0x1e6f7d9, 0x1ea126f, 0x1ea2caf, 0x1ea2f9f |
| `0x1f92d98` | Traduit / contrôlé | 0x1ea40b7, 0x1ea4c18 |
| `0x1f92dd8` | Traduit / contrôlé | 0x1ea0ea0 |
| `0x1f92de8` | Traduit / contrôlé | 0x1ea0eae |
| `0x1f92e03` | Traduit / contrôlé | 0x1ea0ebc |
| `0x1f92e16` | Traduit / contrôlé | 0x1ea0eca |
| `0x1f92e29` | Traduit / contrôlé | 0x1ea101e |
| `0x1f92ea7` | Traduit / contrôlé | 0x1ea1027 |
| `0x1f92f5b` | Traduit / contrôlé | 0x1ea1030 |
| `0x1f93047` | Traduit / contrôlé | 0x1ea1039 |
| `0x1f9313a` | Traduit / contrôlé | 0x1ea1212 |
| `0x1f93195` | Traduit / contrôlé | 0x1ea12b9 |
| `0x1f931df` | Traduit / contrôlé | 0x1ea12c2 |
| `0x1f93235` | Traduit / contrôlé | 0x1ea129e |
| `0x1f93259` | Traduit / contrôlé | 0x1ea12cb |
| `0x1f93296` | Traduit / contrôlé | 0x1ea12b0 |
| `0x1f932f9` | Traduit / contrôlé | 0x1ea12da |
| `0x1f9333b` | Exception | Clé d'extraction commençant dans un octet de bourrage 00, sans lecteur propre. Les lecteurs réels ciblent 0x1f9333c, entrée suivante du même lot ; traduction et vérification assurées par cette entrée, aucun doublon injecté. |
| `0x1f9333c` | Traduit / contrôlé | 0x1e6c390 |
| `0x1f9337d` | Traduit / contrôlé | 0x1e6c21a |
| `0x1f9340d` | Traduit / contrôlé | 0x1e6c22e |
| `0x1f934df` | Traduit / contrôlé | 0x1e6c346 |
| `0x1f934fd` | Traduit / contrôlé | 0x1e6c2aa |
| `0x1f9351b` | Traduit / contrôlé | 0x1e6c34f |
| `0x1f93690` | Traduit / contrôlé | 0x1e6c35c |
| `0x1f937cb` | Traduit / contrôlé | 0x1e6c369 |
| `0x1f938cd` | Traduit / contrôlé | 0x1e6c376 |
| `0x1f939a0` | Traduit / contrôlé | 0x1e6c383 |
| `0x1f93a45` | Traduit / contrôlé | 0x1e6c2b6, 0x1eafd74, 0x1fb3ed4, 0x1fb4764 |
| `0x1f93a55` | Traduit / contrôlé | 0x1e6c2c4 |
| `0x1f93a61` | Traduit / contrôlé | 0x1e6c2d2 |
| `0x1f93a6f` | Traduit / contrôlé | 0x1e6c2e0 |
| `0x1f93a88` | Traduit / contrôlé | 0x1e6c2ee |
| `0x1f93a9c` | Traduit / contrôlé | 0x1e6bfb2 |
| `0x1f93afd` | Traduit / contrôlé | 0x1e6c3a1, 0x1e6ca00 |
| `0x1f93b17` | Traduit / contrôlé | 0x1e6c41c, 0x1e6ca52 |
| `0x1f93b33` | Traduit / contrôlé | 0x1e6c4c3, 0x1e6c4e7, 0x1e6c50b, 0x1e6c52f, 0x1e6c553, 0x1e6c577 |
| `0x1f93b4f` | Traduit / contrôlé | 0x1e6c594 |
| `0x1f93b6d` | Traduit / contrôlé | 0x1e6c622, 0x1e6c674, 0x1e6c6a7, 0x1e6c761, 0x1e6c799, 0x1e6c7d9 |
| `0x1f93b86` | Traduit / contrôlé | 0x1e6c6d3 |
| `0x1f93bb3` | Traduit / contrôlé | 0x1e6c805 |
| `0x1f93be5` | Traduit / contrôlé | 0x1e6c8ac, 0x1e6c8ee, 0x1e6c92f, 0x1e6c970, 0x1e6c9a8 |
| `0x1f93c12` | Traduit / contrôlé | 0x1e6c9df |
| `0x1f93c43` | Traduit / contrôlé | 0x1e6c3ad, 0x1e6ca1a |
| `0x1f93c54` | Traduit / contrôlé | 0x1e6c436, 0x1e6c4e1 |
| `0x1f93c5e` | Traduit / contrôlé | 0x1e6c460, 0x1e6c54d, 0x1e6c571, 0x1e6ca6c |
| `0x1f93c69` | Traduit / contrôlé | 0x1e6c3bb, 0x1e6ca0c |
| `0x1f93c70` | Traduit / contrôlé | 0x1e6c3c9 |
| `0x1f93c80` | Traduit / contrôlé | 0x1e6c5ca |
| `0x1f93c8d` | Traduit / contrôlé | 0x1e6c709 |
| `0x1f93c9f` | Traduit / contrôlé | 0x1e6bfbc, 0x1e6c01a, 0x1e6c066 |
| `0x1f93cb0` | Traduit / contrôlé | 0x1e6bfd4 |
| `0x1f93cf0` | Traduit / contrôlé | 0x1e6bffa |
| `0x1f93ddf` | Traduit / contrôlé | 0x1e6c00d |
| `0x1f93eae` | Traduit / contrôlé | 0x1e6c0b0 |
| `0x1f93ef6` | Traduit / contrôlé | 0x1e6c0a6 |
| `0x1f93f98` | Traduit / contrôlé | 0x1e6c04e |
| `0x1f9406b` | Traduit / contrôlé | 0x1e6c0ba |
| `0x1f940e9` | Traduit / contrôlé | Clé précédant le vrai nom Battle Tower de trois octets 00 C0 46 (bourrage et nop Thumb). Table vivante à 0x1fb3edc visant 0x1f940ec ; nom propre conservé, préfixe inchangé. Texte complet, contrôles et pages conservés ; lecteur final vérifié en ROM. |
| `0x1f940f9` | Traduit / contrôlé | 0x1eb7a68, 0x1eb7b7c |
| `0x1f940fe` | Traduit / contrôlé | 0x1eb7a5c, 0x1eb7b6c |
| `0x1f94105` | Traduit / contrôlé | 0x1e9e498, 0x1e9f19e, 0x1ea068b, 0x1ea3196, 0x1ea40cb, 0x1ea49c7 |
| `0x1f9410f` | Traduit / contrôlé | 0x1e549b2, 0x1e64155, 0x1e689ac, 0x1e6aa1c, 0x1e6f837, 0x1e6ff6a, 0x1e700fe, 0x1e70203, 0x1e791df, 0x1e8d8a2, 0x1e8db4c, 0x1e8f79b, 0x1e8fb7b, 0x1e98d89, 0x1e9cac5, 0x1e9e4b4, 0x1e9f1c8, 0x1ea06a7, 0x1ea31c0, 0x1ea40e7, 0x1ea49e3 |
| `0x1f94114` | Traduit / contrôlé | 0x1e9f1ba, 0x1ea31b2 |
| `0x1f94121` | Traduit / contrôlé | 0x1e9e4a6, 0x1e9f1ac, 0x1ea0699, 0x1ea31a4, 0x1ea40d9, 0x1ea49d5 |
| `0x1f94130` | Traduit / contrôlé | 0x1e60950, 0x1e6c2fc, 0x1e7fc06, 0x1e7fc4a, 0x1e8d8be, 0x1e8db68, 0x1e8e045, 0x1e8e089, 0x1e8f7b7, 0x1e9e4c2, 0x1e9f1d6, 0x1e9ff22, 0x1ea06b5, 0x1ea31ce, 0x1ea40f5, 0x1ea49f1, 0x1ea9b4a, 0x1ea9b8e, 0x1fb3104 |
| `0x1f94135` | Traduit / contrôlé | 0x1e9f23e, 0x1ea070c, 0x1ea4164, 0x1fb30e8 |
| `0x1f94143` | Traduit / contrôlé | 0x1e9f24c, 0x1ea071a, 0x1ea4172, 0x1fb30ec |
| `0x1f94151` | Traduit / contrôlé | 0x1ea0832, 0x1ea4c36, 0x1fb30f0 |
| `0x1f9415e` | Traduit / contrôlé | 0x1ea0840, 0x1ea4c44, 0x1fb30f4 |
| `0x1f94170` | Traduit / contrôlé | 0x1ea0728, 0x1ea4180, 0x1fb30f8 |
| `0x1f94185` | Traduit / contrôlé | 0x1ea0736, 0x1ea418e, 0x1fb30fc |
| `0x1f9419a` | Traduit / contrôlé | 0x1ea084e, 0x1ea4c52, 0x1fb3100 |
| `0x1f941ae` | Traduit / contrôlé | 0x1fb1ddc |
| `0x1f941b4` | Traduit / contrôlé | 0x1eb72cc |
| `0x1f941bc` | Traduit / contrôlé | 0x1e80db0, 0x1e80fbe, 0x1e8d9ea, 0x1e9e6ba, 0x1e9f9c9, 0x1ea0946, 0x1ea388f, 0x1ea433b |
| `0x1f941c9` | Traduit / contrôlé | 0x1e9e6c8, 0x1e9f9d7, 0x1ea0954, 0x1ea389d, 0x1ea4349 |
| `0x1f941d9` | Traduit / contrôlé | 0x1e9e6e4, 0x1e9f9f3, 0x1ea097e, 0x1ea38ab, 0x1ea4373 |
| `0x1f941e6` | Traduit / contrôlé | 0x1e9e6d6, 0x1e9f9e5, 0x1ea0962, 0x1ea4357 |
| `0x1f941f3` | Traduit / contrôlé | 0x1e9fb4b, 0x1ea0b0e, 0x1fb31f0 |
| `0x1f941ff` | Traduit / contrôlé | 0x1e9fb59, 0x1ea0b1c, 0x1fb31f4 |
| `0x1f9420d` | Traduit / contrôlé | 0x1ea0970, 0x1ea4365 |
| `0x1f94219` | Traduit / contrôlé | 0x1ea0b2a, 0x1fb31f8 |
| `0x1f94224` | Traduit / contrôlé | 0x1e9fb67, 0x1ea4a8c, 0x1fb31fc |
| `0x1f94233` | Traduit / contrôlé | 0x1e8f7a9, 0x1e9eb01, 0x1e9fb75, 0x1ea0b38, 0x1ea3956, 0x1ea4a9a, 0x1fb3200 |
| `0x1f94240` | Traduit / contrôlé | 0x1e9eb0f, 0x1e9fb83, 0x1ea0b46, 0x1ea3964, 0x1ea4aa8, 0x1fb3204 |
| `0x1f94252` | Traduit / contrôlé | 0x1fb2c78, 0x1fb320c, 0x1fb3248, 0x1fb326c |
| `0x1f9425b` | Traduit / contrôlé | 0x1fb2c7c, 0x1fb3210, 0x1fb3270, 0x1fb39fc |
| `0x1f9426b` | Traduit / contrôlé | 0x1e9e7fd, 0x1fb2c80, 0x1fb324c, 0x1fb3274 |
| `0x1f94275` | Traduit / contrôlé | 0x1e9e98b, 0x1fb2c84, 0x1fb3250, 0x1fb3278 |
| `0x1f94282` | Traduit / contrôlé | 0x1e9e917, 0x1fb2c88, 0x1fb3254, 0x1fb327c |
| `0x1f94294` | Traduit / contrôlé | 0x1fb2c8c, 0x1fb3258, 0x1fb3280 |
| `0x1f942a8` | Traduit / contrôlé | 0x1fb2c90, 0x1fb3214, 0x1fb325c, 0x1fb3284 |
| `0x1f942b8` | Traduit / contrôlé | 0x1e9fac3, 0x1ea447b |
| `0x1f942c3` | Traduit / contrôlé | 0x1e9fad1, 0x1ea4489 |
| `0x1f942ca` | Traduit / contrôlé | 0x1e9e80b, 0x1fb2c94, 0x1fb3218 |
| `0x1f942da` | Traduit / contrôlé | 0x1e9e999, 0x1fb2c98, 0x1fb321c |
| `0x1f942e8` | Traduit / contrôlé | 0x1e9e925, 0x1fb2c9c, 0x1fb3220 |
| `0x1f942fc` | Traduit / contrôlé | 0x1ea0a86 |
| `0x1f94310` | Traduit / contrôlé | 0x1fb2ca0, 0x1fb3224 |
| `0x1f9432d` | Traduit / contrôlé | 0x1e9e88a, 0x1fb2ca4, 0x1fb3228 |
