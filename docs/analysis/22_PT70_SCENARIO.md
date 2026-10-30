# PT-70 — scénario : audit des 299 offsets

Le manifeste PT-70 définit seul le périmètre. F-758 et F-759 sont intégrés ; le glossaire PT-BR est appliqué. Les sources EN et FR sont comparées au même offset, avec lecture des octets EN complets. Les 298 entrées vivantes sont protégées exactement dans `protected_entries.yaml`. Aucune traduction préexistante supprimée.

## Consommateurs et exceptions

- Les huit extractions tronquées (indices 58, 70, 142, 149, 217, 218, 221, 282) sont complétées depuis la ROM EN, terminateur compris.
- `0x1f34cc9` (Mrs. Harth) est orpheline : zéro pointeur exact/intérieur. Les six appels du voisin Dr. Harth chargent `0x1f34cbf` et appellent `0x9eb59d1`. Le désassemblage montre une copie du pointeur chargé, sans accès à la chaîne suivante. Aucun patch de table fixe n’est nécessaire ; cette entrée reste intacte.
- `0x1f31cef` est lu à `0x1e57d4a`. Les motifs similaires à `0x13df497` et `0x13e7d7b` appartiennent aux WaveData Sappy `0x13ddf7c` et `0x13e6860`, pas à des pointeurs texte. Leurs en-têtes, bornes et pointeurs instrument sont consignés dans le JSON ; les quatre octets de chaque faux pointeur sont restaurés après le build générique.
- `0x1f3932d` utilise FD02 comme sujet. Son unique appel de préparation à `0x1e8a91c` est dirigé vers le helper existant `0x1e6e06a` : ele/ela, au lieu du possessif dele/ela. Les codes FD restent inchangés ; aucune chaîne hors lot n’est modifiée.
- Sept offsets ne figurent pas dans le corpus FR : indices 4, 55, 67, 179, 214, 216 et 293. Cette absence est conservée comme `french: null`, jamais remplacée par une traduction supposée.

## Vérification reproductible

Le finaliseur `languages/pt/patches/batch_70.py` réutilise les primitives PT existantes : validation des préimages, écriture atomique en espace libre, repointage des seuls consommateurs audités, contrôle des octets et de leur non-chevauchement. Il suit toutes les réparations et la police. Les pages FA/FB et les paramètres FC/FD/F8 gardent leur ordre exact ; seuls les sauts FE sont repliés. Les budgets sont contrôlés dans les cinq tables de largeurs vivantes, avec neuf glyphes larges par tampon runtime.

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt70.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt70_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt70.config.ts
```

La sonde Playwright utilise une copie temporaire de la ROM finale, appelle de vrais msgbox aux pointeurs vivants et vérifie le texte par OCR. mGBA et Chromium restent hors écran. La capture est écrite dans le répertoire temporaire OS et jointe au ticket, jamais versionnée. Cette sonde ne prétend pas parcourir toutes les scènes de l’histoire ; le contrôle binaire couvre les 298 textes.

## Bilan offset par offset

Les préimages, comparaisons EN/FR, traductions, références de scripts, budgets encodés et largeurs sont détaillés dans `languages/pt/data/pt70_audit.json`.

| Offset | Décision | Pointeur(s) lecteur(s) | Octets PT |
|---|---|---|---|
| `0x1f317f2` | Texte identique vérifié en ROM | `0x1e57b61` | 10 |
| `0x1f317fc` | Texte identique vérifié en ROM | `0x1e69d17`, `0x1e8a6d7` | 11 |
| `0x1f31807` | Texte identique vérifié en ROM | `0x1e57e31` | 22 |
| `0x1f3181d` | Texte identique vérifié en ROM | `0x1e57ec8` | 26 |
| `0x1f31837` | Texte identique vérifié en ROM | `0x1e57e40` | 10 |
| `0x1f31841` | Traduit / vérifié en ROM | `0x1e57bba` | 105 |
| `0x1f318b2` | Traduit / vérifié en ROM | `0x1e57bda` | 225 |
| `0x1f319a3` | Traduit / vérifié en ROM | `0x1e57bfa` | 178 |
| `0x1f31a70` | Traduit / vérifié en ROM | `0x1e57c1e` | 122 |
| `0x1f31af5` | Traduit / vérifié en ROM | `0x1e57c68` | 116 |
| `0x1f31b80` | Traduit / vérifié en ROM | `0x1e57c90` | 140 |
| `0x1f31c2f` | Traduit / vérifié en ROM | `0x1e57caa` | 45 |
| `0x1f31c5c` | Traduit / vérifié en ROM | `0x1e57cca` | 43 |
| `0x1f31c8c` | Traduit / vérifié en ROM | `0x1e57cf6`, `0x1e5955a`, `0x1e5daf5`, `0x1e5de3a`, `0x1e5f5d9`, `0x1e6002d`, `0x1e6c636`, `0x1e89c2a`, `0x1e89dc1`, `0x1e8d2f2` | 43 |
| `0x1f31cba` | Traduit / vérifié en ROM | `0x1e57d46` | 46 |
| `0x1f31cef` | Traduit / vérifié en ROM | `0x1e57d4a` | 25 |
| `0x1f31d07` | Traduit / vérifié en ROM | `0x1e57d6f` | 85 |
| `0x1f31d5c` | Traduit / vérifié en ROM | `0x1e57d8c` | 162 |
| `0x1f31e0d` | Traduit / vérifié en ROM | `0x1e57daa` | 15 |
| `0x1f31e19` | Traduit / vérifié en ROM | `0x1e57deb` | 92 |
| `0x1f31e7a` | Traduit / vérifié en ROM | `0x1e57e09` | 110 |
| `0x1f31ef3` | Traduit / vérifié en ROM | `0x1e68434` | 133 |
| `0x1f31f9f` | Traduit / vérifié en ROM | `0x1e68454` | 68 |
| `0x1f31fed` | Traduit / vérifié en ROM | `0x1e68474` | 272 |
| `0x1f3212d` | Traduit / vérifié en ROM | `0x1e68494` | 19 |
| `0x1f32141` | Traduit / vérifié en ROM | `0x1e684b4` | 375 |
| `0x1f32300` | Traduit / vérifié en ROM | `0x1e684f5` | 164 |
| `0x1f323b2` | Traduit / vérifié en ROM | `0x1e68541` | 126 |
| `0x1f3244c` | Traduit / vérifié en ROM | `0x1e68562` | 24 |
| `0x1f32467` | Traduit / vérifié en ROM | `0x1e685b9` | 90 |
| `0x1f324ca` | Traduit / vérifié en ROM | `0x1e5ab8a` | 55 |
| `0x1f324fe` | Traduit / vérifié en ROM | `0x1e5abab` | 33 |
| `0x1f32527` | Traduit / vérifié en ROM | `0x1e5ac5e` | 25 |
| `0x1f3253b` | Traduit / vérifié en ROM | `0x1e58ad2` | 146 |
| `0x1f325de` | Traduit / vérifié en ROM | `0x1e58aeb` | 341 |
| `0x1f3275f` | Traduit / vérifié en ROM | `0x1e58b0c` | 78 |
| `0x1f327be` | Traduit / vérifié en ROM | `0x1e58b4c` | 114 |
| `0x1f32841` | Traduit / vérifié en ROM | `0x1e58b7a` | 26 |
| `0x1f32861` | Traduit / vérifié en ROM | `0x1e58bcc` | 89 |
| `0x1f328c6` | Traduit / vérifié en ROM | `0x1e58bec` | 59 |
| `0x1f328fe` | Traduit / vérifié en ROM | `0x1e58c14` | 94 |
| `0x1f3296e` | Traduit / vérifié en ROM | `0x1e58c4a` | 54 |
| `0x1f329ae` | Traduit / vérifié en ROM | `0x1e58c6e` | 72 |
| `0x1f329fd` | Traduit / vérifié en ROM | `0x1e58c88` | 97 |
| `0x1f32a79` | Traduit / vérifié en ROM | `0x1e58cb1` | 14 |
| `0x1f32a8e` | Traduit / vérifié en ROM | `0x1e58cfb` | 134 |
| `0x1f32b21` | Traduit / vérifié en ROM | `0x1e58d30` | 116 |
| `0x1f32b9d` | Traduit / vérifié en ROM | `0x1e58d50` | 27 |
| `0x1f32bb7` | Traduit / vérifié en ROM | `0x1e58d6e` | 355 |
| `0x1f32d2e` | Traduit / vérifié en ROM | `0x1e58dc4` | 57 |
| `0x1f32d77` | Traduit / vérifié en ROM | `0x1e58dec` | 84 |
| `0x1f32dd5` | Traduit / vérifié en ROM | `0x1e58e72` | 146 |
| `0x1f32e7e` | Traduit / vérifié en ROM | `0x1e58e97` | 44 |
| `0x1f32eb9` | Traduit / vérifié en ROM | `0x1e58ecf` | 161 |
| `0x1f32f75` | Traduit / vérifié en ROM | `0x1e58f08` | 170 |
| `0x1f33055` | Texte identique vérifié en ROM | `0x1e58f51` | 18 |
| `0x1f33067` | Traduit / vérifié en ROM | `0x1e79379` | 199 |
| `0x1f3316d` | Traduit / vérifié en ROM | `0x1e7938c` | 384 |
| `0x1f33351` | Traduit / vérifié en ROM | `0x1e793a5` | 448 |
| `0x1f3356e` | Traduit / vérifié en ROM | `0x1e888ab` | 295 |
| `0x1f336b1` | Traduit / vérifié en ROM | `0x1e888ce` | 17 |
| `0x1f336c0` | Traduit / vérifié en ROM | `0x1e88916` | 80 |
| `0x1f3371d` | Traduit / vérifié en ROM | `0x1e6cb82` | 230 |
| `0x1f33815` | Traduit / vérifié en ROM | `0x1e6cba2` | 107 |
| `0x1f338a2` | Traduit / vérifié en ROM | `0x1e6cbc2` | 118 |
| `0x1f33916` | Traduit / vérifié en ROM | `0x1e6cbe2` | 49 |
| `0x1f3394e` | Texte identique vérifié en ROM | `0x1e6cc00` | 26 |
| `0x1f33968` | Texte identique vérifié en ROM | `0x1e5dcae`, `0x1e69d8d`, `0x1e6cc10` | 13 |
| `0x1f33975` | Traduit / vérifié en ROM | `0x1e6cc4c` | 30 |
| `0x1f33999` | Traduit / vérifié en ROM | `0x1e5dedc`, `0x1e6ccc9` | 24 |
| `0x1f339b2` | Traduit / vérifié en ROM | `0x1e6cd2b` | 649 |
| `0x1f33cae` | Traduit / vérifié en ROM | `0x1e6ce0c`, `0x1e6ce17`, `0x1e6ce22` | 18 |
| `0x1f33cc0` | Traduit / vérifié en ROM | `0x1e6cda1` | 303 |
| `0x1f33e17` | Traduit / vérifié en ROM | `0x1e6ce40` | 52 |
| `0x1f33e54` | Traduit / vérifié en ROM | `0x1e56584` | 114 |
| `0x1f33ee0` | Traduit / vérifié en ROM | `0x1e565a4` | 31 |
| `0x1f33f05` | Traduit / vérifié en ROM | `0x1e56422` | 80 |
| `0x1f33f55` | Traduit / vérifié en ROM | `0x1e56474` | 165 |
| `0x1f34012` | Traduit / vérifié en ROM | `0x1e56495` | 25 |
| `0x1f3402b` | Traduit / vérifié en ROM | `0x1e564bd` | 16 |
| `0x1f3403c` | Traduit / vérifié en ROM | `0x1e564de` | 311 |
| `0x1f341a9` | Texte identique vérifié en ROM | `0x1e69d0d` | 30 |
| `0x1f341c7` | Traduit / vérifié en ROM | `0x1e69d4a` | 93 |
| `0x1f34226` | Traduit / vérifié en ROM | `0x1e69d6a` | 164 |
| `0x1f342c8` | Traduit / vérifié en ROM | `0x1e69d83` | 28 |
| `0x1f342e5` | Traduit / vérifié en ROM | `0x1e69db9` | 48 |
| `0x1f34315` | Traduit / vérifié en ROM | `0x1e69e08` | 34 |
| `0x1f34335` | Traduit / vérifié en ROM | `0x1e69e2c` | 54 |
| `0x1f3437c` | Traduit / vérifié en ROM | `0x1e69f0e` | 45 |
| `0x1f343a8` | Traduit / vérifié en ROM | `0x1e6a06b` | 117 |
| `0x1f34427` | Traduit / vérifié en ROM | `0x1e6a082` | 50 |
| `0x1f34454` | Traduit / vérifié en ROM | `0x1e69f6f` | 421 |
| `0x1f3463c` | Traduit / vérifié en ROM | `0x1e69f90` | 139 |
| `0x1f346d6` | Traduit / vérifié en ROM | `0x1e69fd6` | 112 |
| `0x1f34747` | Traduit / vérifié en ROM | `0x1e6a03e` | 18 |
| `0x1f3475c` | Traduit / vérifié en ROM | `0x1e6a09c` | 68 |
| `0x1f347ae` | Traduit / vérifié en ROM | `0x1e95351` | 18 |
| `0x1f347b9` | Traduit / vérifié en ROM | `0x1e953b2` | 69 |
| `0x1f34804` | Traduit / vérifié en ROM | `0x1e953d2` | 101 |
| `0x1f3487e` | Traduit / vérifié en ROM | `0x1e953fb` | 140 |
| `0x1f34914` | Traduit / vérifié en ROM | `0x1e893d4` | 196 |
| `0x1f349e6` | Traduit / vérifié en ROM | `0x1e89489`, `0x1e895ec` | 186 |
| `0x1f34aa1` | Traduit / vérifié en ROM | `0x1e89404` | 163 |
| `0x1f34b4a` | Traduit / vérifié en ROM | `0x1e8961a` | 78 |
| `0x1f34b9a` | Traduit / vérifié en ROM | `0x1e895ca` | 111 |
| `0x1f34c15` | Traduit / vérifié en ROM | `0x1e894ce` | 53 |
| `0x1f34c4b` | Traduit / vérifié en ROM | `0x1e894ff` | 49 |
| `0x1f34c76` | Traduit / vérifié en ROM | `0x1e89583` | 64 |
| `0x1f34cbf` | Texte identique vérifié en ROM | `0x1e8999e`, `0x1e899b5`, `0x1e89eca`, `0x1e89f1e`, `0x1e89f7f`, `0x1e89fbf` | 10 |
| `0x1f34cc9` | Exception : chaîne orpheline |  | — |
| `0x1f34cd4` | Traduit / vérifié en ROM | `0x1e89a08` | 166 |
| `0x1f34d94` | Traduit / vérifié en ROM | `0x1e89a28` | 197 |
| `0x1f34e4d` | Traduit / vérifié en ROM | `0x1e89a48` | 140 |
| `0x1f34ed3` | Traduit / vérifié en ROM | `0x1e89a68` | 92 |
| `0x1f34f2e` | Traduit / vérifié en ROM | `0x1e89a88` | 77 |
| `0x1f34f7c` | Traduit / vérifié en ROM | `0x1e89aa8` | 229 |
| `0x1f3506d` | Traduit / vérifié en ROM | `0x1e89ac8` | 76 |
| `0x1f350b8` | Traduit / vérifié en ROM | `0x1e89ae8` | 131 |
| `0x1f35149` | Traduit / vérifié en ROM | `0x1e89b1a` | 147 |
| `0x1f351dd` | Traduit / vérifié en ROM | `0x1e89b4a` | 75 |
| `0x1f35222` | Traduit / vérifié en ROM | `0x1e89b68` | 56 |
| `0x1f3525e` | Traduit / vérifié en ROM | `0x1e89b88` | 57 |
| `0x1f35293` | Traduit / vérifié en ROM | `0x1e89c07`, `0x1e8a0bb` | 84 |
| `0x1f352f0` | Traduit / vérifié en ROM | `0x1e89c86` | 47 |
| `0x1f35323` | Traduit / vérifié en ROM | `0x1e89c8a` | 30 |
| `0x1f35342` | Traduit / vérifié en ROM | `0x1e89cb9` | 128 |
| `0x1f353bd` | Traduit / vérifié en ROM | `0x1e8a067` | 63 |
| `0x1f35405` | Traduit / vérifié en ROM | `0x1e8a087` | 24 |
| `0x1f3541d` | Traduit / vérifié en ROM | `0x1e89ce8` | 111 |
| `0x1f35493` | Traduit / vérifié en ROM | `0x1e89d10` | 115 |
| `0x1f3551b` | Traduit / vérifié en ROM | `0x1e89d3a` | 105 |
| `0x1f3557d` | Traduit / vérifié en ROM | `0x1e89d5e` | 122 |
| `0x1f35602` | Traduit / vérifié en ROM | `0x1e89da0` | 172 |
| `0x1f356c3` | Traduit / vérifié en ROM | `0x1e89df3` | 29 |
| `0x1f356df` | Traduit / vérifié en ROM | `0x1e89ed5` | 44 |
| `0x1f35706` | Traduit / vérifié en ROM | `0x1e89f01` | 29 |
| `0x1f3571f` | Traduit / vérifié en ROM | `0x1e89f29` | 123 |
| `0x1f3579e` | Traduit / vérifié en ROM | `0x1e89f49` | 46 |
| `0x1f357c4` | Traduit / vérifié en ROM | `0x1e89f66` | 51 |
| `0x1f357f8` | Traduit / vérifié en ROM | `0x1e89f8a` | 162 |
| `0x1f35890` | Traduit / vérifié en ROM | `0x1e89faa` | 53 |
| `0x1f358ce` | Traduit / vérifié en ROM | `0x1e89fca` | 129 |
| `0x1f3595f` | Traduit / vérifié en ROM | `0x1e89ff2` | 530 |
| `0x1f35b93` | Traduit / vérifié en ROM | `0x1e954a5` | 224 |
| `0x1f35ca5` | Traduit / vérifié en ROM | `0x1e954c6` | 47 |
| `0x1f35cdb` | Traduit / vérifié en ROM | `0x1e954e1` | 49 |
| `0x1f35d05` | Traduit / vérifié en ROM | `0x1e954ff` | 176 |
| `0x1f35db2` | Traduit / vérifié en ROM | `0x1e95529` | 310 |
| `0x1f35ef7` | Traduit / vérifié en ROM | `0x1e6a128` | 60 |
| `0x1f35f2d` | Traduit / vérifié en ROM | `0x1e6a156` | 478 |
| `0x1f36150` | Traduit / vérifié en ROM | `0x1e6a178` | 311 |
| `0x1f3629b` | Traduit / vérifié en ROM | `0x1e694e7` | 51 |
| `0x1f362d1` | Traduit / vérifié en ROM | `0x1e69507` | 91 |
| `0x1f3632a` | Traduit / vérifié en ROM | `0x1e69532` | 19 |
| `0x1f36341` | Traduit / vérifié en ROM | `0x1e69590` | 123 |
| `0x1f363d2` | Traduit / vérifié en ROM | `0x1e695b0` | 47 |
| `0x1f36401` | Traduit / vérifié en ROM | `0x1e695d9` | 162 |
| `0x1f364ab` | Traduit / vérifié en ROM | `0x1e96447` | 20 |
| `0x1f364ba` | Traduit / vérifié en ROM | `0x1e963bb` | 6 |
| `0x1f364c0` | Traduit / vérifié en ROM | `0x1e963f6` | 190 |
| `0x1f3658d` | Traduit / vérifié en ROM | `0x1e96406` | 32 |
| `0x1f365b2` | Traduit / vérifié en ROM | `0x1e96417` | 138 |
| `0x1f36643` | Traduit / vérifié en ROM | `0x1e96f34` | 64 |
| `0x1f3667f` | Traduit / vérifié en ROM | `0x1e975f0` | 64 |
| `0x1f366be` | Traduit / vérifié en ROM | `0x1e975fc` | 31 |
| `0x1f366de` | Traduit / vérifié en ROM | `0x1e97613` | 39 |
| `0x1f36704` | Traduit / vérifié en ROM | `0x1e9762d` | 63 |
| `0x1f3674a` | Traduit / vérifié en ROM | `0x1e97636` | 100 |
| `0x1f367b4` | Traduit / vérifié en ROM | `0x1e97649` | 28 |
| `0x1f367d2` | Traduit / vérifié en ROM | `0x1e9767e` | 59 |
| `0x1f3680c` | Traduit / vérifié en ROM | `0x1e976bf` | 57 |
| `0x1f3683c` | Traduit / vérifié en ROM | `0x1e9784d` | 245 |
| `0x1f36947` | Traduit / vérifié en ROM | `0x1e9788b` | 55 |
| `0x1f36988` | Traduit / vérifié en ROM | `0x1e978ff` | 100 |
| `0x1f369ed` | Traduit / vérifié en ROM | `0x1e9791f` | 54 |
| `0x1f36a1d` | Traduit / vérifié en ROM | `0x1e9797b` | 46 |
| `0x1f36a45` | Traduit / vérifié en ROM | `0x1e9799b` | 37 |
| `0x1f36a6b` | Traduit / vérifié en ROM | `0x1e979dd` | 68 |
| `0x1f36aab` | Texte identique vérifié en ROM | `0x1e979f6` | 28 |
| `0x1f36ac7` | Texte identique vérifié en ROM | `0x1e97a05` | 9 |
| `0x1f36ad0` | Traduit / vérifié en ROM | `0x1e97c5c` | 21 |
| `0x1f36ae3` | Traduit / vérifié en ROM | `0x1e97a3e` | 63 |
| `0x1f36b1a` | Traduit / vérifié en ROM | `0x1e97a78` | 56 |
| `0x1f36b4b` | Traduit / vérifié en ROM | `0x1e97aa9` | 54 |
| `0x1f36b8d` | Traduit / vérifié en ROM | `0x1e97aeb` | 306 |
| `0x1f36cd3` | Traduit / vérifié en ROM | `0x1e97b04` | 295 |
| `0x1f36e21` | Traduit / vérifié en ROM | `0x1e97c34` | 77 |
| `0x1f36e74` | Traduit / vérifié en ROM | `0x1e97b30` | 62 |
| `0x1f36eb1` | Traduit / vérifié en ROM | `0x1e97b41` | 302 |
| `0x1f36fe6` | Traduit / vérifié en ROM | `0x1e693aa` | 228 |
| `0x1f370d2` | Traduit / vérifié en ROM | `0x1e693c4` | 392 |
| `0x1f37282` | Traduit / vérifié en ROM | `0x1e6941b` | 52 |
| `0x1f372c3` | Traduit / vérifié en ROM | `0x1e693de` | 401 |
| `0x1f37486` | Traduit / vérifié en ROM | `0x1e69439` | 18 |
| `0x1f374a2` | Traduit / vérifié en ROM | `0x1e83bf2` | 367 |
| `0x1f37640` | Traduit / vérifié en ROM | `0x1e83c3f` | 53 |
| `0x1f3766c` | Traduit / vérifié en ROM | `0x1e83c73` | 87 |
| `0x1f376d7` | Traduit / vérifié en ROM | `0x1e83ce3` | 57 |
| `0x1f37714` | Traduit / vérifié en ROM | `0x1e83d03` | 70 |
| `0x1f3775e` | Traduit / vérifié en ROM | `0x1e83d23` | 276 |
| `0x1f3789e` | Traduit / vérifié en ROM | `0x1e83d43` | 80 |
| `0x1f37918` | Traduit / vérifié en ROM | `0x1e83d6d` | 102 |
| `0x1f3797e` | Traduit / vérifié en ROM | `0x1e83d9e` | 74 |
| `0x1f379d3` | Traduit / vérifié en ROM | `0x1e83dbe` | 246 |
| `0x1f37aee` | Traduit / vérifié en ROM | `0x1e83dde` | 66 |
| `0x1f37b33` | Traduit / vérifié en ROM | `0x1e83e02` | 395 |
| `0x1f37d04` | Traduit / vérifié en ROM | `0x1e83e22` | 162 |
| `0x1f37db8` | Traduit / vérifié en ROM | `0x1e83e40` | 76 |
| `0x1f37e09` | Traduit / vérifié en ROM | `0x1e83e70` | 122 |
| `0x1f37e91` | Traduit / vérifié en ROM | `0x1e83fb1` | 278 |
| `0x1f37fae` | Traduit / vérifié en ROM | `0x1e84001` | 292 |
| `0x1f380eb` | Traduit / vérifié en ROM | `0x1e840eb` | 162 |
| `0x1f38196` | Traduit / vérifié en ROM | `0x1e84107` | 73 |
| `0x1f381e1` | Traduit / vérifié en ROM | `0x1e84120` | 218 |
| `0x1f382e5` | Texte identique vérifié en ROM | `0x1e5f141`, `0x1e8413d`, `0x1e8423d` | 8 |
| `0x1f382ed` | Traduit / vérifié en ROM | `0x1e8418e` | 32 |
| `0x1f38317` | Texte identique vérifié en ROM | `0x1e841e7` | 22 |
| `0x1f3832d` | Traduit / vérifié en ROM | `0x1e84209` | 477 |
| `0x1f3853f` | Traduit / vérifié en ROM | `0x1e84223` | 624 |
| `0x1f387f2` | Traduit / vérifié en ROM | `0x1e6f699` | 327 |
| `0x1f38960` | Traduit / vérifié en ROM | `0x1e6f6cd` | 79 |
| `0x1f389bb` | Traduit / vérifié en ROM | `0x1e62709` | 625 |
| `0x1f38c8f` | Traduit / vérifié en ROM | `0x1e6272d` | 252 |
| `0x1f38db0` | Traduit / vérifié en ROM | `0x1e62776` | 25 |
| `0x1f38dcd` | Traduit / vérifié en ROM | `0x1e8a5ba` | 153 |
| `0x1f38e6b` | Traduit / vérifié en ROM | `0x1e8a5d3` | 59 |
| `0x1f38ea9` | Traduit / vérifié en ROM | `0x1e8a5f3` | 63 |
| `0x1f38eef` | Traduit / vérifié en ROM | `0x1e8a648` | 147 |
| `0x1f38fa1` | Traduit / vérifié en ROM | `0x1e8a6cd` | 107 |
| `0x1f39010` | Traduit / vérifié en ROM | `0x1e8a761` | 31 |
| `0x1f3902f` | Traduit / vérifié en ROM | `0x1e8a77f` | 156 |
| `0x1f390d6` | Traduit / vérifié en ROM | `0x1e8a79c` | 77 |
| `0x1f3911d` | Traduit / vérifié en ROM | `0x1e8a7b6` | 149 |
| `0x1f391c9` | Traduit / vérifié en ROM | `0x1e8a7d6` | 119 |
| `0x1f3923c` | Traduit / vérifié en ROM | `0x1e8aafa`, `0x1e8abdf`, `0x1e8b54c`, `0x1e8b5ca`, `0x1e8b925`, `0x1e8bb70`, `0x1e8d0b1`, `0x1e8d183` | 11 |
| `0x1f3924b` | Traduit / vérifié en ROM | `0x1e8b557`, `0x1e8d0bc` | 101 |
| `0x1f392c5` | Traduit / vérifié en ROM | `0x1e8b5d5`, `0x1e8d18e` | 96 |
| `0x1f39326` | Traduit / vérifié en ROM | `0x1e8a90b` | 9 |
| `0x1f3932d` | Traduit / vérifié en ROM | `0x1e8a92e` | 58 |
| `0x1f39377` | Traduit / vérifié en ROM | `0x1e8a951` | 135 |
| `0x1f39418` | Traduit / vérifié en ROM | `0x1e8a9a0` | 113 |
| `0x1f39495` | Traduit / vérifié en ROM | `0x1e8aa68` | 50 |
| `0x1f394c0` | Traduit / vérifié en ROM | `0x1e8aaef` | 12 |
| `0x1f394cb` | Traduit / vérifié en ROM | `0x1e8ab05` | 91 |
| `0x1f39530` | Traduit / vérifié en ROM | `0x1e8ab23` | 121 |
| `0x1f395b2` | Traduit / vérifié en ROM | `0x1e8abd1` | 4 |
| `0x1f395b9` | Traduit / vérifié en ROM | `0x1e8abea` | 75 |
| `0x1f39608` | Traduit / vérifié en ROM | `0x1e8ac70` | 22 |
| `0x1f3961e` | Traduit / vérifié en ROM | `0x1e8acb3` | 53 |
| `0x1f39664` | Traduit / vérifié en ROM | `0x1e8acd7` | 337 |
| `0x1f397b5` | Traduit / vérifié en ROM | `0x1e8b930` | 97 |
| `0x1f3982c` | Traduit / vérifié en ROM | `0x1e8b974` | 153 |
| `0x1f398e7` | Traduit / vérifié en ROM | `0x1e8ba17`, `0x1e8baab`, `0x1e8bb3f` | 34 |
| `0x1f39908` | Traduit / vérifié en ROM | `0x1e8ba22`, `0x1e8bab6` | 42 |
| `0x1f3993e` | Traduit / vérifié en ROM | `0x1e8bb7b` | 91 |
| `0x1f399a0` | Traduit / vérifié en ROM | `0x1e8ad5a` | 136 |
| `0x1f39a35` | Traduit / vérifié en ROM | `0x1e8ad69` | 30 |
| `0x1f39a54` | Traduit / vérifié en ROM | `0x1e8ad8b` | 48 |
| `0x1f39a87` | Traduit / vérifié en ROM | `0x1e8ada7` | 8 |
| `0x1f39a8d` | Traduit / vérifié en ROM | `0x1e8addd` | 105 |
| `0x1f39b06` | Traduit / vérifié en ROM | `0x1e8adf6` | 227 |
| `0x1f39c0d` | Traduit / vérifié en ROM | `0x1e8be28` | 47 |
| `0x1f39c40` | Traduit / vérifié en ROM | `0x1e8be48` | 37 |
| `0x1f39c6e` | Traduit / vérifié en ROM | `0x1e8be90` | 93 |
| `0x1f39ccc` | Traduit / vérifié en ROM | `0x1e8beb0` | 99 |
| `0x1f39d2f` | Traduit / vérifié en ROM | `0x1e8bed0` | 219 |
| `0x1f39e20` | Traduit / vérifié en ROM | `0x1e8bef0` | 157 |
| `0x1f39ec5` | Traduit / vérifié en ROM | `0x1e8bf09` | 51 |
| `0x1f39f06` | Traduit / vérifié en ROM | `0x1e8bf3a` | 214 |
| `0x1f39fe5` | Traduit / vérifié en ROM | `0x1e8bf6d` | 43 |
| `0x1f3a00f` | Traduit / vérifié en ROM | `0x1e8bfb5` | 33 |
| `0x1f3a036` | Traduit / vérifié en ROM | `0x1e8bffd` | 38 |
| `0x1f3a061` | Traduit / vérifié en ROM | `0x1e8c045` | 99 |
| `0x1f3a0cc` | Traduit / vérifié en ROM | `0x1e8c061` | 164 |
| `0x1f3a16b` | Traduit / vérifié en ROM | `0x1e8c0b5` | 71 |
| `0x1f3a1ae` | Traduit / vérifié en ROM | `0x1e8c0d1` | 57 |
| `0x1f3a1e6` | Traduit / vérifié en ROM | `0x1e8c0f6` | 10 |
| `0x1f3a1f3` | Traduit / vérifié en ROM | `0x1e8c136` | 65 |
| `0x1f3a247` | Traduit / vérifié en ROM | `0x1e8c156` | 83 |
| `0x1f3a29d` | Traduit / vérifié en ROM | `0x1e8c176` | 47 |
| `0x1f3a2cd` | Traduit / vérifié en ROM | `0x1e8c196` | 143 |
| `0x1f3a389` | Traduit / vérifié en ROM | `0x1e8c1b6` | 36 |
| `0x1f3a3b5` | Traduit / vérifié en ROM | `0x1e8c1d6` | 525 |
| `0x1f3a61d` | Traduit / vérifié en ROM | `0x1e8c1f6` | 66 |
| `0x1f3a661` | Traduit / vérifié en ROM | `0x1e8c213` | 35 |
| `0x1f3a685` | Traduit / vérifié en ROM | `0x1e8c259` | 25 |
| `0x1f3a69f` | Traduit / vérifié en ROM | `0x1e8c2db` | 90 |
| `0x1f3a6f8` | Traduit / vérifié en ROM | `0x1e8c300` | 451 |
| `0x1f3a8e7` | Traduit / vérifié en ROM | `0x1e8c320` | 63 |
| `0x1f3a922` | Traduit / vérifié en ROM | `0x1e8c340` | 42 |
| `0x1f3a94d` | Traduit / vérifié en ROM | `0x1e8c37f` | 125 |
| `0x1f3a9cf` | Traduit / vérifié en ROM | `0x1e8c3a6` | 41 |
| `0x1f3a9f2` | Traduit / vérifié en ROM | `0x1e8c3ce` | 142 |
| `0x1f3aa87` | Texte identique vérifié en ROM | `0x1e8c3ef` | 15 |
| `0x1f3aa96` | Traduit / vérifié en ROM | `0x1e8c434` | 94 |
| `0x1f3aafd` | Texte identique vérifié en ROM | `0x1e5edc6`, `0x1e8c44e`, `0x1e8c606`, `0x1e8c711` | 16 |
| `0x1f3ab0d` | Traduit / vérifié en ROM | `0x1e8c476` | 111 |
| `0x1f3ab89` | Traduit / vérifié en ROM | `0x1e8c49a` | 390 |
| `0x1f3ad0f` | Traduit / vérifié en ROM | `0x1e8c4ba` | 110 |

## Résultat de validation locale

- `make build-pt` réussi : 298 textes vérifiés par le finaliseur, dont 89 relocalisés à cette étape.
- 10 tests ciblés unitaires/ROM réussis : périmètre, protections, séquences de contrôle,
  préimages, pointeurs, transaction atomique/idempotente, budgets des cinq polices,
  exception orpheline, exclusion PCM et genre ele/ela aux pointeurs finaux.
- Playwright hors écran : 1 test réussi, deux msgbox natives et assertions OCR.
  Capture jointe au ticket F-829, hors dépôt.
- TypeScript et lint des fichiers Python PT-70 réussis.
- Hooks du commit source : 7 557 tests Python réussis, 2 skips préexistants,
  80 tests Vitest réussis et builds FR/IT/DE réussis.

Non vérifié : parcours manuel de toutes les scènes et de toutes les pages en jeu.
La preuve visuelle échantillonne deux premières pages ; le contrôle des octets et
pointeurs porte sur la totalité des 298 entrées vivantes. Aucun push ni pipeline distant.
