# F-761 — PT-02 : dialogues historiques et services

F-758 et F-759 sont intégrés avant ce lot. Le manifeste PT-02 fait autorité :
277 offsets, 261 traductions protégées exactement, 16 exceptions documentées.
Aucun autre offset de combined n'est modifié, aucune traduction existante n'est supprimée.

Les textes réels couvrent Game Corner/Dehara, la pêche et ses records en pouces,
le maître des mouvements, les arènes et PNJ de Fallshore/Blizzard, les services PC,
le Centre Pokémon, les échanges et l'ancien système Link/Union Room de FireRed.
Les textes historiques ne décrivent pas tous une zone actuellement accessible.
La comparaison FR sert de contexte, sans reprise des noms localisés FR : Ayla,
Teala, Galavan, Mel, Professor Log, Bellin Town et les noms propres anglais restent conservés.
Les noms d'objets non attestés restent anglais ; mouvement, Treinador, Centro Pokémon,
Ataque et PS suivent F-759. Les unités de records restent des pouces (pas de conversion fictive).

## Preuve et limites

- `make build-pt` reconstruit la ROM depuis EN, puis exécute le patch PT dédié
  `languages/pt/patches/historical_dialogue.py` en fin de chaîne.
- Ce patch corrige 17 cellules autonomes omises ou restaurées par les passes génériques,
  dans leur budget EN strict ; les deux messages imbriqués `0x1a51f6` / `0x1a5200`
  sont relogés séparément avec leurs quatre consommateurs vérifiés (`67` message ou `0F 00`).
- `0x1a231b` conserve le début de son suffixe `TRI-PASS!` exactement à `0x1a2328` :
  «Você obteve: » occupe les treize octets du préfixe EN. Les trois pointeurs du suffixe restent valides.
- Aucun offset PT-02 n'est dans une table fixe protégée : aucun patch de table fixe n'est nécessaire.
- 246 entrées ont au moins un mot pointeur vérifié dans la ROM finale ; 15
  entrées sans pointeur absolu sont encodées en place et vérifiées dans leur cellule.
  Leur accessibilité dans un parcours naturel n'est pas revendiquée.
- Le test ROM compare le texte complet jusqu'au FF à toutes les cibles finales,
  avec tolérance uniquement aux espaces/retours repliés. Variables FD, couleurs,
  changement de police et pages FB gardent leur ordre et leurs octets source.
  Les FA/FE sont les retours de ligne du moteur ; les frontières de pages sont dures.
- Les lignes sources sont bornées à 192 pixels selon les métriques du moteur
  (réserve de 54 pixels par buffer). Les octets de chaque cellule sans pointeur sont bornés par son FF EN.
  Les tailles avec pointeurs peuvent dépasser le budget source grâce à la relocalisation.
- Trois fragments ont des mots ressemblant à des pointeurs dans des données non consommatrices ;
  ces mots restent strictement inchangés. Douze préfixes AA n'ont aucun pointeur vers le préfixe,
  seulement vers le véritable corps +1. `0x199bb3` est vide.

Source EN SHA256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
ROM PT SHA256 : `61d9d9c841025323c49f3771ab039f3401651ff8d64ec9d503fa010904b96543`.

## Validation locale

- 90 tests PT/registre/intégrité réussis.
- 8 tests ROM PT réussis : contenu intégral, cibles finales, commandes et pages,
  polices vivantes, absence de table fixe, patch idempotent et rejet atomique des budgets/pointeurs/variables invalides.
- Playwright : `npx playwright test --config tests/e2e-playwright/playwright.pt02-dialogues.config.ts`
  — 1 test réussi. Trois vrais msgbox consomment les cibles finales sans remplacer leur texte.
  Le déclencheur temporaire et la sauvegarde copiée servent seulement à appeler l'imprimante native.
  Assertions OCR positives PT et absence des phrases EN ; tolérance aux confusions OCR sur accents.
  mGBA Qt offscreen et Chromium headless, aucune sauvegarde en jeu.
- Capture hors dépôt, jointe au ticket : `attachment://de3984f3-2627-4781-b274-c1fa2b5b6bda`.

## Bilan exhaustif

«octets PT/EN» inclut FF. Les pixels indiquent le maximum de la mise en page source
avec réserve de buffers ; la vérification binaire autorise le repliement doux du build.
Les mots pointeurs et les cibles sont des offsets physiques ROM (base GBA soustraite).

| Offset manifeste | État / justification | Octets PT/EN ; largeur | Site(s) source / preuve | Cible(s) finale(s) |
| --- | --- | --- | --- | --- |
| `0x196df8` | traduit/vérifié, pointeur(s) | 31/35 ; 157px | `0x16c932` | `0x196df8` |
| `0x196e1b` | traduit/vérifié, pointeur(s) | 27/37 ; 103px | `0x16c944` | `0x196e1b` |
| `0x196e40` | traduit/vérifié, pointeur(s) | 35/41 ; 115px | `0x16c952` | `0x196e40` |
| `0x196f0d` | traduit/vérifié, pointeur(s) | 27/25 ; 143px | `0x16caa2` | `0xd10d20` |
| `0x196f26` | traduit/vérifié, pointeur(s) | 29/32 ; 132px | `0x16c83d` | `0x196f26` |
| `0x196f46` | traduit/vérifié, pointeur(s) | 41/30 ; 161px | `0x16c977` | `0xd10e96` |
| `0x196f64` | traduit/vérifié, pointeur(s) | 31/29 ; 90px | `0x16cb5c` | `0xd10d58` |
| `0x196f81` | traduit/vérifié, pointeur(s) | 34/31 ; 102px | `0x16cb65` | `0xd10ddb` |
| `0x196fa0` | traduit/vérifié, pointeur(s) | 34/33 ; 100px | `0x16cb6e` | `0x196fa0` |
| `0x19703e` | traduit/vérifié, pointeur(s) | 27/25 ; 143px | `0x16cd9d` | `0xd10d20` |
| `0x197057` | traduit/vérifié, pointeur(s) | 29/35 ; 156px | `0x7ec30c` | `0x197057` |
| `0x19707a` | traduit/vérifié, pointeur(s) | 23/28 ; 127px | `0x1a7ae3`, `0x7ec36a`, `0x7ec444`, `0x7ec5ac` | `0x19707a` |
| `0x19709d` | traduit/vérifié, pointeur(s) | 21/21 ; 158px | `0x16cc6b`, `0x16cf28`, `0x7ec523` | `0xd10c67` |
| `0x1970b2` | traduit/vérifié, pointeur(s) | 31/35 ; 134px | `0x16cf0b` | `0x1970b2` |
| `0x1970d5` | traduit/vérifié, pointeur(s) | 39/41 ; 125px | `0x16cda7` | `0x1970d5` |
| `0x19745d` | traduit/vérifié, pointeur(s) | 23/31 ; 124px | `0x16d109` | `0x19745d` |
| `0x197873` | exception : octet `AA` parasite (9), corps à `0x197874` | source `AA BE` | aucun ; corps référencé à `0x16d1d8` | préfixe non traduit |
| `0x197874` | traduit/vérifié, pointeur(s) | 68/56 ; 141px | `0x16d1d8` | `0xe6944c` |
| `0x1978ac` | traduit/vérifié, pointeur(s) | 72/60 ; 141px | `0x16d1e2` | `0x1978ac` |
| `0x1979c1` | traduit/vérifié, pointeur(s) | 93/96 ; 140px | `0x16d20a` | `0x1979c1` |
| `0x197a38` | traduit/vérifié, pointeur(s) | 31/38 ; 157px | `0x16d227` | `0x197a38` |
| `0x197a5e` | traduit/vérifié, pointeur(s) | 23/20 ; 125px | `0x16d243` | `0xd10cbf` |
| `0x197a72` | traduit/vérifié, pointeur(s) | 29/30 ; 158px | `0x16d24d` | `0x197a72` |
| `0x1980bc` | traduit/vérifié, pointeur(s) | 60/66 ; 177px | `0x16d4ec` | `0x1980bc` |
| `0x198bba` | exception : octet `AA` parasite (9), corps à `0x198bbb` | source `AA C9` | aucun ; corps référencé à `0x7c0a4c` | préfixe non traduit |
| `0x198bbb` | traduit/vérifié, pointeur(s) | 76/97 ; 152px | `0x7c0a4c` | `0x198bbb` |
| `0x198c1f` | traduit/vérifié, pointeur(s) | 44/48 ; 118px | `0x77f915` | `0x198c1f` |
| `0x19918e` | traduit/vérifié, pointeur(s) | 120/121 ; 162px | `0x16d824` | `0x19918e` |
| `0x199207` | traduit/vérifié, pointeur(s) | 83/87 ; 173px | `0x16d84b` | `0x199207` |
| `0x19925e` | traduit/vérifié, pointeur(s) | 49/56 ; 160px | `0x16d868` | `0x19925e` |
| `0x199296` | traduit/vérifié, pointeur(s) | 153/161 ; 165px | `0x16d87f` | `0x199296` |
| `0x199337` | traduit/vérifié, pointeur(s) | 22/29 ; 87px | `0x16d837` | `0x199337` |
| `0x199354` | traduit/vérifié, pointeur(s) | 30/42 ; 114px | `0x16d841` | `0x199354` |
| `0x19937e` | traduit/vérifié, pointeur(s) | 66/59 ; 176px | `0x16d88c` | `0xe58f0d` |
| `0x1993b9` | traduit/vérifié, pointeur(s) | 106/104 ; 152px | `0x16d899` | `0xe69757` |
| `0x199421` | traduit/vérifié, pointeur(s) | 41/36 ; 151px | `0x16d8b2` | `0xd10e6d` |
| `0x199445` | traduit/vérifié, pointeur(s) | 30/32 ; 167px | `0x16d8e5` | `0x199445` |
| `0x199465` | traduit/vérifié, pointeur(s) | 30/32 ; 136px | `0x16d92f` | `0x199465` |
| `0x199485` | traduit/vérifié, pointeur(s) | 41/44 ; 155px | `0x16d902` | `0x199485` |
| `0x1994b1` | traduit/vérifié, pointeur(s) | 45/57 ; 134px | `0x16d922` | `0x1994b1` |
| `0x1994ea` | traduit/vérifié, pointeur(s) | 42/53 ; 124px | `0x16d943` | `0x1994ea` |
| `0x19951f` | traduit/vérifié, pointeur(s) | 37/36 ; 165px | `0x16d939` | `0x19951f` |
| `0x199bb3` | exception : cellule vide, terminée dès le premier octet | source `FF FF FF FF` | aucun | aucune écriture |
| `0x19a4f7` | exception : octet `AA` parasite (9), corps à `0x19a4f8` | source `AA CE` | aucun ; corps référencé à `0x16e8fa` | préfixe non traduit |
| `0x19a4f8` | traduit/vérifié, pointeur(s) | 126/161 ; 158px | `0x16e8fa` | `0x19a4f8` |
| `0x19a5bd` | exception : octet `AA` parasite (9), corps à `0x19a5be` | source `AA BE` | aucun ; corps référencé à `0x7c3779`, `0x7c3811`, `0x7c383e` | préfixe non traduit |
| `0x19a5be` | traduit/vérifié, pointeur(s) | 129/146 ; 162px | `0x7c3779`, `0x7c3811`, `0x7c383e` | `0x19a5be` |
| `0x19a650` | traduit/vérifié sur place ; accès non prouvé | 54/57 ; 156px | aucun mot absolu | `0x19a650` |
| `0x19a6b1` | traduit/vérifié, pointeur(s) | 5/5 ; 23px | `0x7c386f`, `0x7c5462`, `0x7c550e` | `0x19a6b1` |
| `0x19a79f` | exception : octet `AA` parasite (9), corps à `0x19a7a0` | source `AA BE` | aucun ; corps référencé à `0x16ea12` | préfixe non traduit |
| `0x19a7a0` | traduit/vérifié, pointeur(s) | 75/81 ; 156px | `0x16ea12` | `0x19a7a0` |
| `0x19a7f1` | traduit/vérifié, pointeur(s) | 67/70 ; 191px | `0x16ea1b` | `0x19a7f1` |
| `0x19b86a` | traduit/vérifié, pointeur(s) | 15/14 ; 80px | `0x16eef7` | `0x19b86a` |
| `0x19b8b9` | traduit/vérifié, pointeur(s) | 48/43 ; 174px | `0x16ef01` | `0x19b8b9` |
| `0x19ba45` | traduit/vérifié, pointeur(s) | 16/11 ; 85px | `0x16eea5` | `0x19ba45` |
| `0x19bab4` | traduit/vérifié, pointeur(s) | 46/43 ; 149px | `0x16eeaf` | `0x19bab4` |
| `0x19bb49` | traduit/vérifié, pointeur(s) | 11/10 ; 59px | `0x16eec9` | `0xd10c0c` |
| `0x19bb53` | traduit/vérifié sur place ; accès non prouvé | 35/46 ; 109px | aucun mot absolu | `0x19bb53` |
| `0x19bbb3` | traduit/vérifié, pointeur(s) | 81/84 ; 175px | `0x16eed3` | `0x19bbb3` |
| `0x19bc57` | traduit/vérifié, pointeur(s) | 42/50 ; 134px | `0x16eee0` | `0x19bc57` |
| `0x19bdfe` | traduit/vérifié, pointeur(s) | 67/55 ; 156px | `0x16ef61` | `0xe58fd3` |
| `0x19be37` | traduit/vérifié, pointeur(s) | 71/59 ; 156px | `0x16ef6b` | `0x19be37` |
| `0x19bf8f` | traduit/vérifié sur place ; accès non prouvé | 84/98 ; 155px | aucun mot absolu | `0x19bf8f` |
| `0x19bff1` | traduit/vérifié, pointeur(s) | 111/122 ; 159px | `0x16efa5` | `0x19bff1` |
| `0x19c0b4` | traduit/vérifié, pointeur(s) | 61/67 ; 172px | `0x16f022` | `0x19c0b4` |
| `0x19c0f7` | traduit/vérifié, pointeur(s) | 106/128 ; 178px | `0x16f00b` | `0x19c0f7` |
| `0x19c177` | traduit/vérifié, pointeur(s) | 67/65 ; 153px | `0x16f02f` | `0x19c177` |
| `0x19e9e5` | traduit/vérifié, pointeur(s) | 193/217 ; 174px | `0x16fde9` | `0x19e9e5` |
| `0x19eabe` | traduit/vérifié sur place ; accès non prouvé | 30/34 ; 156px | aucun mot absolu | `0x19eabe` |
| `0x19eae4` | traduit/vérifié, pointeur(s) | 72/80 ; 175px | `0x16fe1a` | `0x19eae4` |
| `0x19eb59` | traduit/vérifié, pointeur(s) | 257/299 ; 170px | `0x16fe41`, `0x16fe52`, `0x16fe5c` | `0x19eb59` |
| `0x19efe0` | traduit/vérifié, pointeur(s) | 119/123 ; 162px | `0x16ff19` | `0x19efe0` |
| `0x19f05b` | traduit/vérifié, pointeur(s) | 83/87 ; 173px | `0x16ff4b` | `0x19f05b` |
| `0x19f0b2` | traduit/vérifié, pointeur(s) | 50/57 ; 160px | `0x16ff53` | `0x19f0b2` |
| `0x19f0eb` | traduit/vérifié, pointeur(s) | 235/271 ; 160px | `0x16ff6d` | `0x19f0eb` |
| `0x19f1fa` | traduit/vérifié, pointeur(s) | 22/29 ; 87px | `0x16ff2c` | `0x19f1fa` |
| `0x19f217` | traduit/vérifié, pointeur(s) | 172/196 ; 152px | `0x16fff7` | `0x19f217` |
| `0x19f2db` | traduit/vérifié, pointeur(s) | 52/64 ; 131px | `0x16ffaa` | `0x19f2db` |
| `0x19f31b` | traduit/vérifié, pointeur(s) | 101/122 ; 137px | `0x170036` | `0x19f31b` |
| `0x19f395` | traduit/vérifié, pointeur(s) | 43/54 ; 125px | `0x170055` | `0x19f395` |
| `0x19f3cb` | traduit/vérifié, pointeur(s) | 54/63 ; 118px | `0x170029` | `0x19f3cb` |
| `0x19f40a` | traduit/vérifié, pointeur(s) | 70/94 ; 175px | `0x170016` | `0x19f40a` |
| `0x19f468` | traduit/vérifié, pointeur(s) | 35/44 ; 119px | `0x170003` | `0x19f468` |
| `0x19f494` | traduit/vérifié, pointeur(s) | 66/59 ; 176px | `0x16ff77`, `0x17005f` | `0xe58f4f` |
| `0x19f4cf` | traduit/vérifié, pointeur(s) | 44/61 ; 118px | `0x170080` | `0x19f4cf` |
| `0x19f50c` | traduit/vérifié, pointeur(s) | 76/84 ; 162px | `0x170073` | `0x19f50c` |
| `0x1a1b8e` | traduit/vérifié sur place ; accès non prouvé | 39/41 ; 132px | aucun mot absolu | `0x1a1b8e` |
| `0x1a231b` | traduit/vérifié sur place ; accès non prouvé | 23/23 ; 130px | aucun mot absolu | `0x1a231b` |
| `0x1a2328` | traduit/vérifié, pointeur(s) | 10/10 ; 54px | `0xc70ffb`, `0x125eff8`, `0x12eddae` | `0x1a2328` |
| `0x1a2b88` | traduit/vérifié, pointeur(s) | 183/197 ; 156px | `0x171637` | `0x1a2b88` |
| `0x1a2c63` | traduit/vérifié, pointeur(s) | 74/89 ; 123px | `0x1716a7` | `0x1a2c63` |
| `0x1a2cc3` | traduit/vérifié, pointeur(s) | 28/30 ; 155px | `0x1716c0` | `0x1a2cc3` |
| `0x1a2ce1` | traduit/vérifié, pointeur(s) | 29/27 ; 157px | `0x1716f6` | `0xd10d3b` |
| `0x1a2cfc` | traduit/vérifié, pointeur(s) | 73/71 ; 177px | `0x171784` | `0xe695aa` |
| `0x1a2d43` | traduit/vérifié, pointeur(s) | 49/62 ; 169px | `0x1213918` | `0x1a2d43` |
| `0x1a2d75` | exception : fragment interne de `0x1a2d43`, mot fortuit au milieu du flux graphique | contexte `8e7875b8752d1a0847d8d257` | faux positif à `0x51bd6c` ; mot conservé | parent traduit ; aucun repointage du fragment |
| `0x1a2d85` | traduit/vérifié, pointeur(s) | 38/42 ; 129px | `0x17174a` | `0x1a2d85` |
| `0x1a2de0` | traduit/vérifié, pointeur(s) | 53/60 ; 157px | `0x1717a0` | `0x1a2de0` |
| `0x1a2e20` | traduit/vérifié, pointeur(s) | 52/57 ; 171px | `0x171792` | `0x1a2e20` |
| `0x1a2e4e` | exception : fragment interne de `0x1a2e20`, mot fortuit au milieu du flux graphique | contexte `e92b5c654e2e1a08fdf9efdc` | faux positif à `0x4e9294` ; mot conservé | parent traduit ; aucun repointage du fragment |
| `0x1a505b` | traduit/vérifié sur place ; accès non prouvé | 21/26 ; 114px | aucun mot absolu | `0x1a505b` |
| `0x1a5075` | traduit/vérifié, pointeur(s) | 15/21 ; 122px | `0x1a6979` | `0x1a5075` |
| `0x1a508a` | traduit/vérifié, pointeur(s) | 24/29 ; 133px | `0x09d284`, `0x1a6999` | `0x1a508a` |
| `0x1a50a7` | traduit/vérifié, pointeur(s) | 24/23 ; 134px | `0x1a6a36` | `0xd10cd6` |
| `0x1a50be` | traduit/vérifié, pointeur(s) | 34/31 ; 185px | `0x1a6a1c`, `0x74b472`, `0x1e7a32a` | `0xd10d97` |
| `0x1a50dd` | traduit/vérifié, pointeur(s) | 20/18 ; 153px | `0x1a69f5` | `0xd10c53` |
| `0x1a50ef` | traduit/vérifié, pointeur(s) | 22/20 ; 122px | `0x1a6a3f` | `0xd10c7c` |
| `0x1a5103` | traduit/vérifié sur place ; accès non prouvé | 46/48 ; 143px | aucun mot absolu | `0x1a5103` |
| `0x1a5133` | traduit/vérifié sur place ; accès non prouvé | 43/45 ; 126px | aucun mot absolu | `0x1a5133` |
| `0x1a5160` | traduit/vérifié sur place ; accès non prouvé | 48/48 ; 137px | aucun mot absolu | `0x1a5160` |
| `0x1a5190` | traduit/vérifié, pointeur(s) | 14/19 ; 74px | `0x16bb2d`, `0x16bb6b`, `0x16bc27`, `0x16bc79`, `0x16bcb3`, `0x7616f1`, `0x763565`, `0x763841`, `0x7729d3`, `0x772a1f`, `0x7ea757`, `0x7eb85f`, `0x7eb89f`, `0x1e56042`, `0x1e577ce`, `0x1e64372`, `0x1e6439e`, `0x1e643d0`, `0x1e643f6`, `0x1e6441c`, `0x1e64448`, `0x1e64470`, `0x1e644a4`, `0x1e69b35`, `0x1e6a20f`, `0x1e6a221`, `0x1e6a248`, `0x1e6a27e`, `0x1e6a2a8`, `0x1e7e13a`, `0x1e82335`, `0x1e8df05`, `0x1e8df17`, `0x1e8df3c`, `0x1e8df66`, `0x1e8fcb3` | `0x1a5190` |
| `0x1a51a3` | traduit/vérifié sur place ; accès non prouvé | 36/45 ; 141px | aucun mot absolu | `0x1a51a3` |
| `0x1a51d0` | traduit/vérifié sur place ; accès non prouvé | 36/38 ; 176px | aucun mot absolu | `0x1a51d0` |
| `0x1a51f6` | traduit/vérifié, pointeur(s) | 11/17 ; 101px | `0x1a674a`, `0x1a682f`, `0x9a48dd` | `0x904a88` |
| `0x1a5200` | traduit/vérifié, pointeur(s) | 4/7 ; 60px | `0x1a6990` | `0x1a5200` |
| `0x1a5207` | traduit/vérifié sur place ; accès non prouvé | 15/17 ; 77px | aucun mot absolu | `0x1a5207` |
| `0x1a5218` | traduit/vérifié, pointeur(s) | 21/25 ; 161px | `0x1a6752`, `0x1a681a`, `0x1a689f`, `0x1a8d75`, `0x1a8e68`, `0x9a483e`, `0x9a48ab`, `0x9a4910` | `0x1a5218` |
| `0x1a5231` | traduit/vérifié, pointeur(s) | 13/17 ; 156px | `0x1a6828`, `0x1a68ab`, `0x1a68c6`, `0x9a4854` | `0x1a5231` |
| `0x1a5242` | traduit/vérifié, pointeur(s) | 32/26 ; 117px | `0x16cf7d`, `0x780e1f` | `0xd10d77` |
| `0x1a525c` | traduit/vérifié, pointeur(s) | 16/16 ; 120px | `0x1a68b5`, `0x1a6921`, `0x1a6940` | `0xd10c43` |
| `0x1a526c` | traduit/vérifié, pointeur(s) | 35/40 ; 156px | `0x1a690c`, `0x1e6f4a0` | `0x1a526c` |
| `0x1a5294` | traduit/vérifié, pointeur(s) | 36/32 ; 139px | `0x1a6929` | `0xd10e20` |
| `0x1a52b4` | traduit/vérifié, pointeur(s) | 33/41 ; 126px | `0x1a6948` | `0x1a52b4` |
| `0x1a52dd` | traduit/vérifié, pointeur(s) | 16/19 ; 120px | `0x1a68bf` | `0x1a52dd` |
| `0x1a52f0` | traduit/vérifié, pointeur(s) | 11/17 ; 101px | `0x1a6799` | `0x1a52f0` |
| `0x1a5301` | traduit/vérifié, pointeur(s) | 33/46 ; 114px | `0x1a6c10`, `0x1a6c1a` | `0x1a5301` |
| `0x1a532f` | traduit/vérifié, pointeur(s) | 26/34 ; 120px | `0x1a67a1` | `0x1a532f` |
| `0x1a5375` | traduit/vérifié sur place ; accès non prouvé | 60/61 ; 174px | aucun mot absolu | `0x1a5375` |
| `0x1a5420` | traduit/vérifié, pointeur(s) | 15/21 ; 122px | `0x168cfa` | `0x1a5420` |
| `0x1a5446` | traduit/vérifié sur place ; accès non prouvé | 39/48 ; 131px | aucun mot absolu | `0x1a5446` |
| `0x1a5483` | traduit/vérifié, pointeur(s) | 76/94 ; 160px | `0x1a6588` | `0x1a5483` |
| `0x1a54e1` | traduit/vérifié, pointeur(s) | 56/48 ; 158px | `0x1a65bb` | `0xe58cea` |
| `0x1a5511` | traduit/vérifié, pointeur(s) | 22/21 ; 121px | `0x1a662f`, `0x1a6665` | `0x1a5511` |
| `0x1a552b` | traduit/vérifié, pointeur(s) | 65/67 ; 134px | `0x1a661e` | `0x1a552b` |
| `0x1a556e` | traduit/vérifié, pointeur(s) | 47/55 ; 172px | `0x1a6af8`, `0x9a4bc1`, `0x9a4c74` | `0x1a556e` |
| `0x1a55a5` | traduit/vérifié, pointeur(s) | 14/14 ; 117px | `0x1a6c5e` | `0xd10c25` |
| `0x1a55b3` | traduit/vérifié, pointeur(s) | 58/55 ; 164px | `0x1a6b10` | `0xe58d22` |
| `0x1a561a` | traduit/vérifié, pointeur(s) | 68/77 ; 157px | `0x1bb879` | `0x1a561a` |
| `0x1a5667` | traduit/vérifié, pointeur(s) | 37/41 ; 119px | `0x1bb883` | `0x1a5667` |
| `0x1a5690` | traduit/vérifié, pointeur(s) | 16/23 ; 105px | `0x1a74fa` | `0x1a5690` |
| `0x1a56a7` | traduit/vérifié, pointeur(s) | 31/43 ; 121px | `0x16cdc9`, `0x16cdf6`, `0x75cbb3`, `0x791aac`, `0x7b3851`, `0x7c4f1e`, `0x7ede3f`, `0x7ede61`, `0x7ee785`, `0x7ef3a0`, `0x8cee9f`, `0x8ceec2`, `0x1e55a78`, `0x1e55bc0`, `0x1e5f475`, `0x1e5f4bd`, `0x1e63659`, `0x1e6ae15`, `0x1e6e7b5`, `0x1e6f2e9`, `0x1e71f82`, `0x1e7a04e`, `0x1e7b06f`, `0x1e80154`, `0x1e8213d`, `0x1e84407`, `0x1e87093`, `0x1e8806a`, `0x1e8e7da`, `0x1e8ec60`, `0x1e8f08b`, `0x1e905d5`, `0x1e90d26`, `0x1e90d6e`, `0x1ea1282`, `0x1ea2cc2`, `0x1ea2fb2`, `0x1ea5e0a`, `0x1eb063a`, `0x1eb06d2` | `0x1a56a7` |
| `0x1a5700` | traduit/vérifié, pointeur(s) | 43/42 ; 181px | `0x1a8d6a`, `0x1a8d82` | `0x1a5700` |
| `0x1a58a7` | traduit/vérifié, pointeur(s) | 99/91 ; 174px | `0x1a7abf` | `0xe696f4` |
| `0x1a5909` | traduit/vérifié, pointeur(s) | 57/63 ; 182px | `0x1a7ad3` | `0x1a5909` |
| `0x1a594d` | traduit/vérifié, pointeur(s) | 33/46 ; 129px | `0x1a7ac9` | `0x1a594d` |
| `0x1a597b` | traduit/vérifié, pointeur(s) | 59/59 ; 149px | `0x16fd73` | `0xe58d5c` |
| `0x1a59b6` | traduit/vérifié, pointeur(s) | 16/16 ; 63px | `0x16fdb8` | `0xd10c33` |
| `0x1a59c6` | traduit/vérifié, pointeur(s) | 22/20 ; 123px | `0x16fdc6` | `0xd10c92` |
| `0x1a59da` | traduit/vérifié, pointeur(s) | 14/13 ; 72px | `0x16fdab` | `0xd10c17` |
| `0x1a59e7` | traduit/vérifié, pointeur(s) | 27/23 ; 189px | `0x16fdd0` | `0x1a59e7` |
| `0x1a5ad5` | exception : octet `AA` parasite (9), corps à `0x1a5ad6` | source `AA C2` | aucun ; corps référencé à `0x16e35f` | préfixe non traduit |
| `0x1a5ad6` | traduit/vérifié, pointeur(s) | 42/50 ; 115px | `0x16e35f` | `0x1a5ad6` |
| `0x1a5b08` | traduit/vérifié, pointeur(s) | 10/16 ; 52px | `0x16e3be`, `0x7c2c5f` | `0x1a5b08` |
| `0x1a5b18` | traduit/vérifié, pointeur(s) | 47/50 ; 175px | `0x16e3cc`, `0x7c2c77` | `0x1a5b18` |
| `0x1a5b4a` | traduit/vérifié, pointeur(s) | 25/22 ; 137px | `0x16e3b1` | `0xd10d07` |
| `0x1a5b60` | traduit/vérifié, pointeur(s) | 43/40 ; 174px | `0x16e3d6`, `0x7c2c4b` | `0xd10ee9` |
| `0x1a5b88` | traduit/vérifié, pointeur(s) | 31/37 ; 132px | `0x7d7cd1` | `0x1a5b88` |
| `0x1a5bc5` | exception : octet `AA` parasite (9), corps à `0x1a5bc6` | source `AA BB` | aucun ; corps référencé à `0x1a6a88` | préfixe non traduit |
| `0x1a5bc6` | traduit/vérifié, pointeur(s) | 78/61 ; 182px | `0x1a6a88` | `0xe695f3` |
| `0x1a5c03` | traduit/vérifié, pointeur(s) | 35/43 ; 104px | `0x1a6a90` | `0x1a5c03` |
| `0x1a5c2e` | traduit/vérifié, pointeur(s) | 29/31 ; 160px | `0x1a6ab4` | `0x1a5c2e` |
| `0x1a5c4d` | traduit/vérifié, pointeur(s) | 27/44 ; 83px | `0x1a7550` | `0x1a5c4d` |
| `0x1a5cdf` | traduit/vérifié, pointeur(s) | 23/18 ; 123px | `0x1a8141` | `0xd10ca8` |
| `0x1a5cf1` | traduit/vérifié, pointeur(s) | 60/64 ; 120px | `0x1a8c69`, `0x3e2280`, `0x3fe4c8` | `0x1a5cf1` |
| `0x1a5d31` | traduit/vérifié, pointeur(s) | 58/61 ; 120px | `0x1a8c94`, `0x3e2284`, `0x3fe4cc` | `0x1a5d31` |
| `0x1a5d6e` | traduit/vérifié, pointeur(s) | 72/67 ; 150px | `0x1a8c7b`, `0x3e2288`, `0x3fe4d0` | `0xe69562` |
| `0x1a5db1` | traduit/vérifié, pointeur(s) | 70/64 ; 138px | `0x1a8ca6`, `0x3e228c`, `0x3fe4d4` | `0xe694d5` |
| `0x1a5df1` | traduit/vérifié, pointeur(s) | 14/20 ; 95px | `0x16cdc1`, `0x16cdee` | `0x1a5df1` |
| `0x1a5e31` | traduit/vérifié, pointeur(s) | 91/88 ; 185px | `0x16cd78`, `0x1a9280` | `0xe69699` |
| `0x1a5e89` | traduit/vérifié, pointeur(s) | 50/55 ; 143px | `0x1a8d9c`, `0x1e9e22f` | `0x1a5e89` |
| `0x1a5ec0` | traduit/vérifié, pointeur(s) | 174/219 ; 144px | `0x1a8dc8` | `0x1a5ec0` |
| `0x1a5f9b` | traduit/vérifié, pointeur(s) | 62/68 ; 134px | `0x1a8dd1`, `0x1e9e268` | `0x1a5f9b` |
| `0x1a5fdf` | traduit/vérifié, pointeur(s) | 95/98 ; 121px | `0x1a8de7` | `0x1a5fdf` |
| `0x1a6046` | traduit/vérifié, pointeur(s) | 275/328 ; 173px | `0x1a8df4` | `0x1a6046` |
| `0x1a6196` | exception : octet `AA` parasite (9), corps à `0x1a6197` | source `AA FD` | aucun ; corps référencé à `0x1a8e41` | préfixe non traduit |
| `0x1a6197` | traduit/vérifié, pointeur(s) | 106/78 ; 166px | `0x1a8e41` | `0xe697c1` |
| `0x1a61e5` | traduit/vérifié, pointeur(s) | 66/44 ; 166px | `0x1a8e30` | `0xe58f91` |
| `0x1a6211` | traduit/vérifié, pointeur(s) | 19/27 ; 75px | `0x16a28a`, `0x16bb21`, `0x16bb5f`, `0x16bc1b`, `0x16bc6d`, `0x16bca7`, `0x7616e5`, `0x763559`, `0x763835`, `0x7729c7`, `0x772a13`, `0x7ea74b`, `0x7eb853`, `0x7eb893`, `0x1e55f84`, `0x1e55f99`, `0x1e577c2`, `0x1e64366`, `0x1e64392`, `0x1e643c4`, `0x1e643ea`, `0x1e64410`, `0x1e6443c`, `0x1e64464`, `0x1e64498`, `0x1e69b29`, `0x1e6a1f8`, `0x1e6a23c`, `0x1e7e12e`, `0x1e82329`, `0x1e8deee`, `0x1e8df30`, `0x1e8fca7` | `0x1a6211` |
| `0x1a622c` | traduit/vérifié, pointeur(s) | 45/57 ; 136px | `0x1a7707` | `0x1a622c` |
| `0x1a6265` | traduit/vérifié, pointeur(s) | 103/110 ; 155px | `0x1a7798` | `0x1a6265` |
| `0x1a62d3` | traduit/vérifié, pointeur(s) | 128/134 ; 161px | `0x1a7770` | `0x1a62d3` |
| `0x1a6359` | traduit/vérifié, pointeur(s) | 52/58 ; 152px | `0x1a7781` | `0x1a6359` |
| `0x1a6393` | traduit/vérifié, pointeur(s) | 45/49 ; 132px | `0x1bb1e6` | `0x1a6393` |
| `0x1a63c4` | traduit/vérifié, pointeur(s) | 16/18 ; 128px | `0x1a9243` | `0x1a63c4` |
| `0x1a63e8` | traduit/vérifié, pointeur(s) | 24/31 ; 156px | `0x1a6822` | `0x1a63e8` |
| `0x1a6447` | exception : octet `AA` parasite (9), corps à `0x1a6448` | source `AA C1` | aucun ; corps référencé à `0x1637d8`, `0x163b53`, `0x788909` | préfixe non traduit |
| `0x1a6448` | traduit/vérifié, pointeur(s) | 7/7 ; 36px | `0x1637d8`, `0x163b53`, `0x788909` | `0x1a6448` |
| `0x1a6c74` | traduit/vérifié, pointeur(s) | 31/31 ; 172px | `0x1a6c6c` | `0x1a6c74` |
| `0x1a6ca2` | exception : octet `AA` parasite (9), corps à `0x1a6ca3` | source `AA CE` | aucun ; corps référencé à `0x1a740e` | préfixe non traduit |
| `0x1a6ca3` | traduit/vérifié, pointeur(s) | 102/116 ; 168px | `0x1a740e` | `0x1a6ca3` |
| `0x1a6d17` | traduit/vérifié, pointeur(s) | 76/86 ; 164px | `0x0ca510` | `0x1a6d17` |
| `0x1a6d6d` | traduit/vérifié, pointeur(s) | 93/114 ; 176px | `0x0ca444` | `0x1a6d6d` |
| `0x1a6ddf` | traduit/vérifié, pointeur(s) | 88/87 ; 142px | `0x0ca450` | `0xe69641` |
| `0x1a6e36` | traduit/vérifié, pointeur(s) | 101/110 ; 182px | `0x0ca45c` | `0x1a6e36` |
| `0x1a6ea4` | traduit/vérifié, pointeur(s) | 93/103 ; 170px | `0x0ca468` | `0x1a6ea4` |
| `0x1a6f0b` | traduit/vérifié, pointeur(s) | 87/102 ; 163px | `0x0ca474` | `0x1a6f0b` |
| `0x1a6f71` | traduit/vérifié, pointeur(s) | 44/58 ; 126px | `0x0ca480` | `0x1a6f71` |
| `0x1a6fab` | traduit/vérifié, pointeur(s) | 67/70 ; 158px | `0x0ca48c` | `0x1a6fab` |
| `0x1a6ff1` | traduit/vérifié, pointeur(s) | 63/64 ; 177px | `0x0ca498` | `0x1a6ff1` |
| `0x1a7031` | traduit/vérifié, pointeur(s) | 39/50 ; 121px | `0x0ca4a4` | `0x1a7031` |
| `0x1a7063` | traduit/vérifié, pointeur(s) | 49/66 ; 158px | `0x0ca4b0` | `0x1a7063` |
| `0x1a70a5` | traduit/vérifié, pointeur(s) | 53/51 ; 166px | `0x0ca4bc` | `0xe58cb5` |
| `0x1a70d8` | traduit/vérifié, pointeur(s) | 50/48 ; 161px | `0x0ca4c8` | `0xd10fa1` |
| `0x1a7108` | traduit/vérifié, pointeur(s) | 41/47 ; 149px | `0x0ca4d4` | `0x1a7108` |
| `0x1a7137` | traduit/vérifié, pointeur(s) | 57/62 ; 160px | `0x0ca4fc` | `0x1a7137` |
| `0x1a7175` | traduit/vérifié, pointeur(s) | 38/53 ; 151px | `0x0ca520` | `0x1a7175` |
| `0x1a71aa` | traduit/vérifié, pointeur(s) | 69/68 ; 168px | `0x1a744b` | `0xe69490` |
| `0x1a71ee` | traduit/vérifié, pointeur(s) | 54/65 ; 149px | `0x1a7472` | `0x1a71ee` |
| `0x1a722f` | traduit/vérifié, pointeur(s) | 79/98 ; 138px | `0x1a7483` | `0x1a722f` |
| `0x1b1d7c` | exception : octet `AA` parasite (9), corps à `0x1b1d7d` | source `AA C3` | aucun ; corps référencé à `0x1b286e` | préfixe non traduit |
| `0x1b1d7d` | traduit/vérifié, pointeur(s) | 117/138 ; 181px | `0x1b286e` | `0x1b1d7d` |
| `0x1b1e07` | traduit/vérifié, pointeur(s) | 23/29 ; 114px | `0x1b292d`, `0x133f573` | `0x1b1e07` |
| `0x1b1e24` | traduit/vérifié, pointeur(s) | 29/30 ; 157px | `0x1b289f` | `0x1b1e24` |
| `0x1b1e42` | traduit/vérifié, pointeur(s) | 53/59 ; 129px | `0x1b2908` | `0x1b1e42` |
| `0x1b1e7d` | traduit/vérifié, pointeur(s) | 68/54 ; 192px | `0x1b291b` | `0x1b1e7d` |
| `0x1bc310` | exception : octet `AA` parasite (9), corps à `0x1bc311` | source `AA D1` | aucun ; corps référencé à `0x1bb44b` | préfixe non traduit |
| `0x1bc35e` | traduit/vérifié, pointeur(s) | 38/42 ; 133px | `0x1bb45b` | `0x1bc35e` |
| `0x1bc388` | traduit/vérifié, pointeur(s) | 63/63 ; 186px | `0x3e072c` | `0xe58e8e` |
| `0x1bc3c7` | traduit/vérifié, pointeur(s) | 58/60 ; 167px | `0x3e0730` | `0x1bc3c7` |
| `0x1bc409` | traduit/vérifié, pointeur(s) | 63/57 ; 186px | `0x1bb535`, `0x1bbd10` | `0xe58e4f` |
| `0x1bc442` | traduit/vérifié, pointeur(s) | 61/58 ; 178px | `0x1bb7c4` | `0xe58dd4` |
| `0x1bc47c` | traduit/vérifié, pointeur(s) | 48/48 ; 188px | `0x1bb7d2` | `0xd10f40` |
| `0x1bc4ac` | traduit/vérifié, pointeur(s) | 31/34 ; 118px | `0x0817bc`, `0x1bb55d`, `0x1bb6d1` | `0x1bc4ac` |
| `0x1bc4ce` | traduit/vérifié, pointeur(s) | 71/63 ; 183px | `0x080aa8`, `0x080c30` | `0xe6951b` |
| `0x1bc50d` | traduit/vérifié, pointeur(s) | 64/63 ; 192px | `0x080bc0` | `0xe58ecd` |
| `0x1bc54c` | traduit/vérifié, pointeur(s) | 44/38 ; 120px | `0x080ac8` | `0xd10f14` |
| `0x1bc590` | traduit/vérifié, pointeur(s) | 7/14 ; 32px | `0x1bb5c2`, `0x1bb748` | `0x1bc590` |
| `0x1bc59e` | traduit/vérifié, pointeur(s) | 29/34 ; 160px | `0x1bbf89` | `0x1bc59e` |
| `0x1bc5c0` | traduit/vérifié, pointeur(s) | 65/85 ; 130px | `0x1bb817` | `0x1bc5c0` |
| `0x1bc615` | traduit/vérifié, pointeur(s) | 51/57 ; 138px | `0x1bb807` | `0x1bc615` |
| `0x1bc64e` | traduit/vérifié, pointeur(s) | 56/60 ; 163px | `0x1bb827` | `0x1bc64e` |
| `0x1bc68a` | traduit/vérifié, pointeur(s) | 14/23 ; 73px | `0x1bb837` | `0x1bc68a` |
| `0x1bc6a1` | traduit/vérifié, pointeur(s) | 42/41 ; 139px | `0x1bb85f` | `0xd10ebf` |
| `0x1bc6ca` | traduit/vérifié, pointeur(s) | 45/54 ; 162px | `0x1bb68f` | `0x1bc6ca` |
| `0x1bc700` | traduit/vérifié, pointeur(s) | 50/54 ; 176px | `0x1bb67e` | `0x1bc700` |
| `0x1bc736` | traduit/vérifié, pointeur(s) | 45/53 ; 150px | `0x1bb66d` | `0x1bc736` |
| `0x1bc76b` | traduit/vérifié, pointeur(s) | 42/54 ; 122px | `0x1bb6a3` | `0x1bc76b` |
| `0x1bc7a1` | traduit/vérifié, pointeur(s) | 57/65 ; 161px | `0x1bb9d8` | `0x1bc7a1` |
| `0x1bc7e2` | traduit/vérifié, pointeur(s) | 67/69 ; 125px | `0x1bb9f3` | `0x1bc7e2` |
| `0x1bc827` | traduit/vérifié, pointeur(s) | 49/36 ; 158px | `0x1bb9a7` | `0xd10f70` |
| `0x1bc84b` | traduit/vérifié, pointeur(s) | 39/41 ; 133px | `0x1bb985` | `0x1bc84b` |
| `0x1bc874` | traduit/vérifié, pointeur(s) | 55/57 ; 133px | `0x1bb996` | `0x1bc874` |
| `0x1bc8ad` | traduit/vérifié, pointeur(s) | 31/45 ; 99px | `0x1bb9b6` | `0x1bc8ad` |
| `0x1bc8da` | traduit/vérifié, pointeur(s) | 29/44 ; 99px | `0x1bb9c8` | `0x1bc8da` |
| `0x1bc918` | traduit/vérifié, pointeur(s) | 52/43 ; 159px | `0x1bb3e7` | `0xe58c4c` |
| `0x1bc943` | traduit/vérifié, pointeur(s) | 25/25 ; 140px | `0x1bb3f0` | `0xd10cee` |
| `0x1bc95c` | traduit/vérifié, pointeur(s) | 89/100 ; 170px | `0x1bb7e7` | `0x1bc95c` |
| `0x1bc9c0` | traduit/vérifié, pointeur(s) | 35/32 ; 190px | `0x1bb7f7` | `0xd10dfd` |
| `0x1bc9e0` | traduit/vérifié, pointeur(s) | 49/51 ; 163px | `0x1bb86f` | `0x1bc9e0` |
| `0x1bca13` | traduit/vérifié, pointeur(s) | 53/48 ; 158px | `0x1bc018` | `0xe58c80` |
| `0x1bca43` | traduit/vérifié, pointeur(s) | 45/60 ; 122px | `0x1bc00b` | `0x1bca43` |
| `0x1bca95` | traduit/vérifié, pointeur(s) | 51/54 ; 167px | `0x3e0738`, `0x3e0748` | `0x1bca95` |
| `0x1bcacb` | traduit/vérifié, pointeur(s) | 41/39 ; 133px | `0x3e073c`, `0x3e074c` | `0xd10e44` |
| `0x1bcaf2` | traduit/vérifié, pointeur(s) | 61/53 ; 186px | `0x3e0740` | `0xe58d97` |
| `0x1bcb42` | traduit/vérifié, pointeur(s) | 34/32 ; 188px | `0x3e0734`, `0x3e0744`, `0x3e0750` | `0xd10db9` |
| `0x1bcb81` | traduit/vérifié, pointeur(s) | 55/66 ; 175px | `0x1bbd63` | `0x1bcb81` |
| `0x1bcbc3` | traduit/vérifié, pointeur(s) | 62/61 ; 190px | `0x1bbb46` | `0xe58e11` |
| `0x1bcc00` | traduit/vérifié, pointeur(s) | 55/58 ; 175px | `0x1bbb54` | `0x1bcc00` |
| `0x1bcc3a` | traduit/vérifié, pointeur(s) | 120/132 ; 176px | `0x1bbb62` | `0x1bcc3a` |
| `0x1bccca` | traduit/vérifié, pointeur(s) | 50/53 ; 175px | `0x1a664b` | `0x1bccca` |
| `0x1bd28d` | traduit/vérifié, pointeur(s) | 135/138 ; 156px | `0x1bbbd9` | `0x1bd28d` |
| `0x1bd317` | traduit/vérifié, pointeur(s) | 21/33 ; 114px | `0x1bbc6b` | `0x1bd317` |
| `0x1bd338` | traduit/vérifié, pointeur(s) | 35/42 ; 117px | `0x1bb4af`, `0x1bbc98` | `0x1bd338` |
| `0x1bd362` | traduit/vérifié, pointeur(s) | 33/46 ; 106px | `0x1bbd37` | `0x1bd362` |
| `0x1bd390` | traduit/vérifié, pointeur(s) | 366/395 ; 188px | `0x1bb503`, `0x1bbd29` | `0x1bd390` |
| `0x1bd51b` | traduit/vérifié, pointeur(s) | 85/103 ; 168px | `0x1bbdbf` | `0x1bd51b` |
| `0x1bd582` | traduit/vérifié, pointeur(s) | 91/111 ; 162px | `0x1bbe53` | `0x1bd582` |
| `0x1bd5f1` | traduit/vérifié, pointeur(s) | 84/106 ; 137px | `0x1bbee7` | `0x1bd5f1` |
| `0x1bd65b` | traduit/vérifié, pointeur(s) | 150/171 ; 153px | `0x1bba46` | `0x1bd65b` |
| `0x1bd706` | traduit/vérifié, pointeur(s) | 294/356 ; 157px | `0x1bba89` | `0x1bd706` |
| `0x1bd86a` | traduit/vérifié, pointeur(s) | 37/46 ; 117px | `0x1bbab6` | `0x1bd86a` |
| `0x1bd898` | traduit/vérifié, pointeur(s) | 196/206 ; 173px | `0x1bb424` | `0x1bd898` |
| `0x1bd966` | traduit/vérifié, pointeur(s) | 452/543 ; 166px | `0x1bb43a` | `0x1bd966` |
| `0x1bdb85` | traduit/vérifié, pointeur(s) | 94/115 ; 149px | `0x1bbb77` | `0x1bdb85` |
| `0x1bdbf8` | traduit/vérifié, pointeur(s) | 626/743 ; 166px | `0x1bbb8a` | `0x1bdbf8` |
| `0x1bdedf` | traduit/vérifié, pointeur(s) | 44/52 ; 123px | `0x1bbb94` | `0x1bdedf` |
| `0x1bdf08` | exception : fragment interne de `0x1bdedf`, mot emboîté dans des opérandes du script, sans opcode consommateur | contexte `0876df1b08df1b081b08ff69` | faux positif à `0x1bdf64` ; mot conservé | parent traduit ; aucun repointage du fragment |

## Non vérifié

Le parcours naturel vers chaque dialogue historique et les fonctionnalités Link avec
plusieurs consoles ne sont pas certifiés. La preuve visuelle porte sur trois msgbox
réelles, les 261 contenus étant contrôlés dans le binaire final. Les quinze cellules
sans pointeur absolu ne sont pas présentées comme accessibles en jeu. Aucun push,
aucune publication et aucun lancement de pipeline distant.
