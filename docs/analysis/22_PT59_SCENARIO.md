# PT-59 — Battleground, Bellin Town, Blizzard City et DexNav

## Périmètre et méthode

300 offsets du manifeste fermé ; 281 traductions, 17 noms conservés selon F-759, 2 exceptions sans lecteur de script identifié. Aucun offset des autres lots modifié. Sources EN/FR comparées à chaque adresse. Les dialogues tronqués du corpus EN sont complétés depuis la ROM source (préimages intégrales dans `languages/pt/data/pt59_audit.json`).

Les 298 textes livrables sont ajoutés avec protections exactes. Le finaliseur PT dédié réutilise le moteur transactionnel existant après les réparations génériques ; il conserve les commandes, pages, pauses, couleurs et tampons, et reloge via tous les lecteurs identifiés. La description de mission 0x1ee55de conserve trois lignes <=172 px ; les dialogues sont bornés à 192 px estimés puis vérifiés avec les cinq polices réelles et les tampons développés (208 px). Les menus sont des tables de pointeurs ; la classe Sinnoh Leader passe par la cellule indirecte CFRU 0x23e760, jamais par une écriture débordant une cellule fixe.

Le motif 0x575fd4 ressemblant à un pointeur vers 0x1edfd0c est du son : échantillon à 0x5758ac, lecteurs instruments 0x19e9ec0/0x19edb68. Le finaliseur restaure ces quatre octets après le repointage générique et le test compare l’échantillon entier.

## Vérifications reproductibles

- `make build-pt`
- `python3 -m pytest -q tests/unit/pt/test_batch_pt59.py tests/unit/test_translation_integrity.py`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt59_rom.py -m rom`
- `npx playwright test --config tests/e2e-playwright/playwright.pt59.config.ts`

La sonde Playwright hors écran affiche les deux premières lignes de deux dialogues issus des pointeurs finaux dans une copie temporaire de ROM. Elle compare les octets et le texte OCR du moteur mGBA ; aucun texte ni glyphe n’est remplacé. Elle ne prétend pas parcourir les 298 scènes. Toutes les pages sont contrôlées en binaire. Capture hors dépôt.

## Bilan offset par offset

Le JSON joint au code donne pour chaque ligne : sources EN/FR, préimage complète, pointeurs, texte PT, commandes, tailles et largeurs. Les exceptions ne sont pas présentées comme des chaînes mortes démontrées par désassemblage exhaustif : elles sont sans lecteur identifié.

| Offset | Décision | Pointeurs source |
|---|---|---|
| `0x1edf7a0` | Traduit / contrôle ROM requis | 0x1e52e71 |
| `0x1edf821` | Traduit / contrôle ROM requis | 0x1e52e90 |
| `0x1edf85c` | Traduit / contrôle ROM requis | 0x1e52ea4, 0x1e52ecb |
| `0x1edf883` | Traduit / contrôle ROM requis | 0x1e52ea8, 0x1e52ecf |
| `0x1edf89d` | Traduit / contrôle ROM requis | 0x1e52ebe, 0x1e52ed5 |
| `0x1edf8d9` | Traduit / contrôle ROM requis | 0x1e52ee2, 0x1e52f09 |
| `0x1edf90e` | Traduit / contrôle ROM requis | 0x1e52ee6, 0x1e52f0d |
| `0x1edf942` | Traduit / contrôle ROM requis | 0x1e52efc, 0x1e52f13 |
| `0x1edf987` | Traduit / contrôle ROM requis | 0x1e52f20, 0x1e52f47 |
| `0x1edf9c0` | Traduit / contrôle ROM requis | 0x1e52f24, 0x1e52f4b |
| `0x1edf9dc` | Traduit / contrôle ROM requis | 0x1e52f3a, 0x1e52f51 |
| `0x1edfa03` | Traduit / contrôle ROM requis | 0x1e52f5e, 0x1e52f85 |
| `0x1edfa2b` | Traduit / contrôle ROM requis | 0x1e52f62, 0x1e52f89 |
| `0x1edfa51` | Traduit / contrôle ROM requis | 0x1e52f78, 0x1e52f8f |
| `0x1edfaaf` | Traduit / contrôle ROM requis | 0x1e52f9c, 0x1e52fc3 |
| `0x1edfae4` | Traduit / contrôle ROM requis | 0x1e52fa0, 0x1e52fc7 |
| `0x1edfb13` | Traduit / contrôle ROM requis | 0x1e52fb6, 0x1e52fcd |
| `0x1edfb68` | Nom conservé F-759 / contrôle ROM requis | 0x1e6c428, 0x1e6c4bd, 0x1fb3ec4 |
| `0x1edfb75` | Traduit / contrôle ROM requis | 0x1e53128 |
| `0x1edfcc5` | Traduit / contrôle ROM requis | 0x1e533d2, 0x1e53672, 0x1e53909, 0x1e53ba0, 0x1e53e59, 0x1e540f0, 0x1e54387, 0x1e54622 |
| `0x1edfd0c` | Traduit / contrôle ROM requis | 0x1e54758 |
| `0x1edfd2f` | Traduit / contrôle ROM requis | 0x1e5498a |
| `0x1edfd74` | Traduit / contrôle ROM requis | 0x1e54afe |
| `0x1edfdec` | Traduit / contrôle ROM requis | 0x1e54b17 |
| `0x1edfe25` | Traduit / contrôle ROM requis | 0x1e54b0b |
| `0x1edfe72` | Traduit / contrôle ROM requis | 0x1e54b36 |
| `0x1edff51` | Traduit / contrôle ROM requis | 0x1e549f4 |
| `0x1edff92` | Traduit / contrôle ROM requis | 0x1e54a88 |
| `0x1edffbb` | Traduit / contrôle ROM requis | 0x1e54ade |
| `0x1ee02b5` | Traduit / contrôle ROM requis | 0x1e54aee |
| `0x1ee04f0` | Traduit / contrôle ROM requis | 0x1e54a1b |
| `0x1ee0539` | Traduit / contrôle ROM requis | 0x1e54a2e |
| `0x1ee0578` | Traduit / contrôle ROM requis | 0x1e54a49 |
| `0x1ee05cd` | Traduit / contrôle ROM requis | 0x1e54a5a |
| `0x1ee06ab` | Traduit / contrôle ROM requis | 0x1e54d0b, 0x1e54e68, 0x1e54fc5, 0x1e5527f, 0x1e553dc, 0x1e55539 |
| `0x1ee0761` | Traduit / contrôle ROM requis | 0x1e55122 |
| `0x1ee0839` | Traduit / contrôle ROM requis | 0x1e5571c |
| `0x1ee08b4` | Traduit / contrôle ROM requis | 0x1e54c19, 0x1e54d76, 0x1e54ed3, 0x1e55030, 0x1e5518d, 0x1e552ea, 0x1e55447, 0x1e555a4 |
| `0x1ee08f8` | Traduit / contrôle ROM requis | 0x1e54d2b, 0x1e54e88, 0x1e54fe5, 0x1e55142, 0x1e5529f, 0x1e553fc, 0x1e55559, 0x1e556d3 |
| `0x1ee0941` | Traduit / contrôle ROM requis | 0x1e54d50, 0x1e54ead, 0x1e5500a, 0x1e55167, 0x1e552c4, 0x1e55421, 0x1e5557e, 0x1e556f8 |
| `0x1ee09a8` | Traduit / contrôle ROM requis | 0x1e55693 |
| `0x1ee0a84` | Traduit / contrôle ROM requis | 0x1e558a5 |
| `0x1ee0ad1` | Traduit / contrôle ROM requis | 0x1e556ae |
| `0x1ee0b4e` | Traduit / contrôle ROM requis | 0x1e54996, 0x1e54a94 |
| `0x1ee0b56` | Nom conservé F-759 / contrôle ROM requis | 0x1e549a4, 0x1e54aa2 |
| `0x1ee0b5f` | Traduit / contrôle ROM requis | 0x1e54c25, 0x1e54d82, 0x1e54edf, 0x1e5503c, 0x1e55199, 0x1e552f6, 0x1e55453, 0x1e555b0 |
| `0x1ee0b68` | Traduit / contrôle ROM requis | 0x1e54c41, 0x1e54d9e, 0x1e54efb, 0x1e55058, 0x1e551b5, 0x1e55312, 0x1e5546f, 0x1e555cc |
| `0x1ee0b70` | Traduit / contrôle ROM requis | 0x1e5323e |
| `0x1ee0d34` | Traduit / contrôle ROM requis | 0x1e532a7 |
| `0x1ee0d75` | Traduit / contrôle ROM requis | 0x1e53264 |
| `0x1ee0dc0` | Traduit / contrôle ROM requis | 0x1e5342b |
| `0x1ee0dfb` | Traduit / contrôle ROM requis | 0x1e53444 |
| `0x1ee0e18` | Traduit / contrôle ROM requis | 0x1e53305 |
| `0x1ee0eee` | Traduit / contrôle ROM requis | 0x1e5333d |
| `0x1ee0fcf` | Traduit / contrôle ROM requis | 0x1e532c7 |
| `0x1ee106d` | Traduit / contrôle ROM requis | 0x1e53359 |
| `0x1ee10ca` | Traduit / contrôle ROM requis | 0x1e533bc |
| `0x1ee1185` | Traduit / contrôle ROM requis | 0x1e55982 |
| `0x1ee118a` | Traduit / contrôle ROM requis | 0x1e53501 |
| `0x1ee13fe` | Traduit / contrôle ROM requis | 0x1e53560 |
| `0x1ee144f` | Traduit / contrôle ROM requis | 0x1e53522 |
| `0x1ee1486` | Traduit / contrôle ROM requis | 0x1e536c6 |
| `0x1ee14c1` | Traduit / contrôle ROM requis | 0x1e536df |
| `0x1ee14e2` | Traduit / contrôle ROM requis | 0x1e535b4 |
| `0x1ee15cc` | Traduit / contrôle ROM requis | 0x1e535e7 |
| `0x1ee1779` | Traduit / contrôle ROM requis | 0x1e5357b |
| `0x1ee185c` | Traduit / contrôle ROM requis | 0x1e535fe |
| `0x1ee1904` | Traduit / contrôle ROM requis | 0x1e5365c |
| `0x1ee1a1f` | Exception : aucun lecteur de script identifié | 0x1ee1904 via 0x1e5365c; 0x1ee1b37 via 0x1e53798 |
| `0x1ee1b37` | Traduit / contrôle ROM requis | 0x1e53798 |
| `0x1ee1d11` | Traduit / contrôle ROM requis | 0x1e537f7 |
| `0x1ee1d63` | Traduit / contrôle ROM requis | 0x1e537b9 |
| `0x1ee1da9` | Traduit / contrôle ROM requis | 0x1e5395d |
| `0x1ee1def` | Traduit / contrôle ROM requis | 0x1e53976 |
| `0x1ee1e1c` | Traduit / contrôle ROM requis | 0x1e5384b |
| `0x1ee1f1e` | Traduit / contrôle ROM requis | 0x1e5387e |
| `0x1ee203b` | Traduit / contrôle ROM requis | 0x1e53812 |
| `0x1ee2113` | Traduit / contrôle ROM requis | 0x1e53895 |
| `0x1ee21be` | Traduit / contrôle ROM requis | 0x1e538f3 |
| `0x1ee22c9` | Traduit / contrôle ROM requis | 0x1e53a2f |
| `0x1ee24c3` | Traduit / contrôle ROM requis | 0x1e53a8e |
| `0x1ee2521` | Traduit / contrôle ROM requis | 0x1e53a50 |
| `0x1ee2567` | Traduit / contrôle ROM requis | 0x1e53bf4 |
| `0x1ee25a8` | Traduit / contrôle ROM requis | 0x1e53c0d |
| `0x1ee25de` | Traduit / contrôle ROM requis | 0x1e53ae2 |
| `0x1ee26e8` | Traduit / contrôle ROM requis | 0x1e53b15 |
| `0x1ee286d` | Traduit / contrôle ROM requis | 0x1e53aa9 |
| `0x1ee2954` | Traduit / contrôle ROM requis | 0x1e53b2c |
| `0x1ee29f6` | Traduit / contrôle ROM requis | 0x1e53b8a |
| `0x1ee2b4f` | Traduit / contrôle ROM requis | 0x1e53cc6 |
| `0x1ee2d68` | Traduit / contrôle ROM requis | 0x1e53d25 |
| `0x1ee2db1` | Traduit / contrôle ROM requis | 0x1e53ce7 |
| `0x1ee2e33` | Traduit / contrôle ROM requis | 0x1e53ead |
| `0x1ee2e74` | Traduit / contrôle ROM requis | 0x1e53ec6 |
| `0x1ee2e8d` | Traduit / contrôle ROM requis | 0x1e53d79 |
| `0x1ee2f9f` | Traduit / contrôle ROM requis | 0x1e53dbb |
| `0x1ee3151` | Traduit / contrôle ROM requis | 0x1e53d40 |
| `0x1ee3248` | Traduit / contrôle ROM requis | 0x1e53dd2 |
| `0x1ee32da` | Traduit / contrôle ROM requis | 0x1e53e43 |
| `0x1ee3416` | Traduit / contrôle ROM requis | 0x1e53f7f |
| `0x1ee3641` | Traduit / contrôle ROM requis | 0x1e53fde |
| `0x1ee36d4` | Traduit / contrôle ROM requis | 0x1e53fa0 |
| `0x1ee3716` | Traduit / contrôle ROM requis | 0x1e54144 |
| `0x1ee3760` | Traduit / contrôle ROM requis | 0x1e5415d |
| `0x1ee379a` | Traduit / contrôle ROM requis | 0x1e54032 |
| `0x1ee38b9` | Traduit / contrôle ROM requis | 0x1e54065 |
| `0x1ee39ee` | Traduit / contrôle ROM requis | 0x1e53ff9 |
| `0x1ee3ab6` | Traduit / contrôle ROM requis | 0x1e5407c |
| `0x1ee3b3f` | Traduit / contrôle ROM requis | 0x1e540da |
| `0x1ee3c49` | Traduit / contrôle ROM requis | 0x1e54216 |
| `0x1ee3e82` | Traduit / contrôle ROM requis | 0x1e54275 |
| `0x1ee3ed9` | Traduit / contrôle ROM requis | 0x1e54237 |
| `0x1ee3f1d` | Traduit / contrôle ROM requis | 0x1e543db |
| `0x1ee3f60` | Traduit / contrôle ROM requis | 0x1e543f4 |
| `0x1ee3f9e` | Traduit / contrôle ROM requis | 0x1e542c9 |
| `0x1ee409a` | Traduit / contrôle ROM requis | 0x1e542fc |
| `0x1ee41e4` | Traduit / contrôle ROM requis | 0x1e54290 |
| `0x1ee42c4` | Traduit / contrôle ROM requis | 0x1e54313 |
| `0x1ee4343` | Traduit / contrôle ROM requis | 0x1e54371 |
| `0x1ee44ac` | Traduit / contrôle ROM requis | 0x1e544b1 |
| `0x1ee4798` | Traduit / contrôle ROM requis | 0x1e54510 |
| `0x1ee4804` | Traduit / contrôle ROM requis | 0x1e544d2 |
| `0x1ee4849` | Traduit / contrôle ROM requis | 0x1e54676 |
| `0x1ee488f` | Traduit / contrôle ROM requis | 0x1e54694 |
| `0x1ee48c6` | Traduit / contrôle ROM requis | 0x1e54564 |
| `0x1ee49b2` | Traduit / contrôle ROM requis | 0x1e54597 |
| `0x1ee4b99` | Traduit / contrôle ROM requis | 0x1e5452b |
| `0x1ee4cc1` | Traduit / contrôle ROM requis | 0x1e545ae |
| `0x1ee4d83` | Traduit / contrôle ROM requis | 0x1e5460c |
| `0x1ee4eb6` | Traduit / contrôle ROM requis | 0x1e53477, 0x1e53493, 0x1e534af, 0x1e5370e, 0x1e5372a, 0x1e53746, 0x1e539a5, 0x1e539c1, 0x1e539dd, 0x1e53c3c, 0x1e53c58, 0x1e53c74, 0x1e53ef5, 0x1e53f11, 0x1e53f2d, 0x1e5418c, 0x1e541a8, 0x1e541c4, 0x1e54427, 0x1e54443, 0x1e5445f, 0x1e546c3, 0x1e546df, 0x1e546fb, 0x1e54c0f, 0x1e54cdd, 0x1e54d00, 0x1e54d45, 0x1e54d6c, 0x1e54e3a, 0x1e54e5d, 0x1e54ea2, 0x1e54ec9, 0x1e54f97, 0x1e54fba, 0x1e54fff, 0x1e55026, 0x1e550f4, 0x1e55117, 0x1e5515c, 0x1e55183, 0x1e55251, 0x1e55274, 0x1e552b9, 0x1e552e0, 0x1e553ae, 0x1e553d1, 0x1e55416, 0x1e5543d, 0x1e5550b, 0x1e5552e, 0x1e55573, 0x1e5559a, 0x1e55668, 0x1e55688, 0x1e556a3, 0x1e556ed, 0x1e55711 |
| `0x1ee4ebe` | Traduit / contrôle ROM requis | 0x1e53482, 0x1e5349e, 0x1e534ba |
| `0x1ee4f1d` | Traduit / contrôle ROM requis | 0x1e53719, 0x1e53735, 0x1e53751 |
| `0x1ee4f74` | Traduit / contrôle ROM requis | 0x1e539cc, 0x1e539e8 |
| `0x1ee4fdc` | Traduit / contrôle ROM requis | 0x1e539b0 |
| `0x1ee5089` | Traduit / contrôle ROM requis | 0x1e53c47, 0x1e53c63, 0x1e53c7f |
| `0x1ee50e4` | Traduit / contrôle ROM requis | 0x1e53f1c, 0x1e53f38 |
| `0x1ee5164` | Traduit / contrôle ROM requis | 0x1e53f00 |
| `0x1ee521a` | Traduit / contrôle ROM requis | 0x1e541b3 |
| `0x1ee5281` | Traduit / contrôle ROM requis | 0x1e54197, 0x1e541cf |
| `0x1ee52e3` | Traduit / contrôle ROM requis | 0x1e5444e |
| `0x1ee5371` | Traduit / contrôle ROM requis | 0x1e54432, 0x1e5446a |
| `0x1ee5408` | Traduit / contrôle ROM requis | 0x1e546ce, 0x1e546ea, 0x1e54706 |
| `0x1ee546b` | Traduit / contrôle ROM requis | 0x1e5594d |
| `0x1ee54cb` | Traduit / contrôle ROM requis | 0x1e5595b |
| `0x1ee559f` | Traduit / contrôle ROM requis | 0x1e55969 |
| `0x1ee55d4` | Traduit / contrôle ROM requis | 0x1e55994, 0x1e559d2, 0x1e55a9e |
| `0x1ee55de` | Traduit / contrôle ROM requis | 0x1e559a0 |
| `0x1ee563c` | Traduit / contrôle ROM requis | 0x1e559b2 |
| `0x1ee590f` | Traduit / contrôle ROM requis | 0x1e55aae |
| `0x1ee597f` | Traduit / contrôle ROM requis | 0x1e559c5 |
| `0x1ee5af6` | Traduit / contrôle ROM requis | 0x1e559f6 |
| `0x1ee5bda` | Traduit / contrôle ROM requis | 0x1e55a03 |
| `0x1ee5c80` | Traduit / contrôle ROM requis | 0x1e55abb |
| `0x1ee5cb7` | Traduit / contrôle ROM requis | 0x1e55a1f |
| `0x1ee5cd5` | Traduit / contrôle ROM requis | 0x1e55a91 |
| `0x1ee5d41` | Traduit / contrôle ROM requis | 0x1e55ac8 |
| `0x1ee5d9c` | Nom conservé F-759 / contrôle ROM requis | 0x1e939bc, 0x1eaf534, 0x1eaf8e4 |
| `0x1ee5da8` | Nom conservé F-759 / contrôle ROM requis | 0x1fb3cdc |
| `0x1ee5db6` | Nom conservé F-759 / contrôle ROM requis | 0x1fb3ce4 |
| `0x1ee5dc4` | Traduit / contrôle ROM requis | 0x1e55b34 |
| `0x1ee5e3a` | Traduit / contrôle ROM requis | 0x1e55bec |
| `0x1ee5f02` | Traduit / contrôle ROM requis | 0x1e55bf5 |
| `0x1ee5f36` | Traduit / contrôle ROM requis | 0x1e55bfe |
| `0x1ee5fb4` | Traduit / contrôle ROM requis | 0x1e55be3 |
| `0x1ee5ff1` | Traduit / contrôle ROM requis | 0x1e55c07 |
| `0x1ee6051` | Traduit / contrôle ROM requis | 0x1e55a63, 0x1e55ba8, 0x1e63643, 0x1e6adff, 0x1e6b367, 0x1e6e79f, 0x1e6f2d1, 0x1e71f6c, 0x1e7a038, 0x1e7b059, 0x1e8013e, 0x1e82127, 0x1e8707b, 0x1e88054, 0x1e8e7c4, 0x1e8ec4a, 0x1e8f075, 0x1e8faae, 0x1eaf749, 0x1eb0622, 0x1eb06ba |
| `0x1ee6082` | Traduit / contrôle ROM requis | 0x1e55c27 |
| `0x1ee60b2` | Traduit / contrôle ROM requis | 0x1e55c30 |
| `0x1ee6115` | Traduit / contrôle ROM requis | 0x1e55b03 |
| `0x1ee621d` | Traduit / contrôle ROM requis | 0x1e55b0d |
| `0x1ee6359` | Traduit / contrôle ROM requis | 0x1e55cc9 |
| `0x1ee6377` | Traduit / contrôle ROM requis | 0x1e55cbb |
| `0x1ee6398` | Traduit / contrôle ROM requis | 0x1e55cd8 |
| `0x1ee63d8` | Traduit / contrôle ROM requis | 0x1e55d2c |
| `0x1ee6496` | Traduit / contrôle ROM requis | 0x1e55cfd |
| `0x1ee6521` | Traduit / contrôle ROM requis | 0x1e55d1f |
| `0x1ee655a` | Traduit / contrôle ROM requis | 0x1e55d7a |
| `0x1ee65f3` | Traduit / contrôle ROM requis | 0x1e55d4b |
| `0x1ee667b` | Traduit / contrôle ROM requis | 0x1e55d6d |
| `0x1ee66c0` | Traduit / contrôle ROM requis | 0x1fb3f44 |
| `0x1ee66d1` | Traduit / contrôle ROM requis | 0x1fb3f4c |
| `0x1ee66e2` | Traduit / contrôle ROM requis | 0x1e55d99 |
| `0x1ee6834` | Traduit / contrôle ROM requis | 0x1e55da3 |
| `0x1ee692e` | Traduit / contrôle ROM requis | 0x1e55dbd |
| `0x1ee6a49` | Traduit / contrôle ROM requis | 0x1e55ded |
| `0x1ee6aae` | Traduit / contrôle ROM requis | 0x1e55e00 |
| `0x1ee6ad5` | Traduit / contrôle ROM requis | 0x1e55e7c |
| `0x1ee6b13` | Traduit / contrôle ROM requis | 0x1e55e61 |
| `0x1ee6b5a` | Traduit / contrôle ROM requis | 0x1e55e6a |
| `0x1ee6bb1` | Traduit / contrôle ROM requis | 0x1e55e73 |
| `0x1ee6bd8` | Traduit / contrôle ROM requis | 0x1e55e12 |
| `0x1ee6c1d` | Traduit / contrôle ROM requis | 0x1e55e29 |
| `0x1ee6c5c` | Nom conservé F-759 / contrôle ROM requis | 0x1fb3f54 |
| `0x1ee6c66` | Traduit / contrôle ROM requis | 0x1e55f90 |
| `0x1ee6cc7` | Traduit / contrôle ROM requis | 0x1e56138 |
| `0x1ee6d4f` | Traduit / contrôle ROM requis | 0x1e56142 |
| `0x1ee6dc4` | Nom conservé F-759 / contrôle ROM requis | 0x1eaf554, 0x1eafa84 |
| `0x1ee6dd2` | Nom conservé F-759 / contrôle ROM requis | 0x1fb3d0c |
| `0x1ee6de2` | Nom conservé F-759 / contrôle ROM requis | 0x1fb3d14 |
| `0x1ee6df2` | Traduit / contrôle ROM requis | 0x1e568b6 |
| `0x1ee6e91` | Traduit / contrôle ROM requis | 0x1e568e0 |
| `0x1ee6f37` | Traduit / contrôle ROM requis | 0x1e568c9, 0x1e568f3 |
| `0x1ee6f55` | Traduit / contrôle ROM requis | 0x1e568d5, 0x1e568ff |
| `0x1ee6f82` | Traduit / contrôle ROM requis | 0x1e56905 |
| `0x1ee6f9f` | Traduit / contrôle ROM requis | 0x1e5690e |
| `0x1ee6fd4` | Traduit / contrôle ROM requis | 0x1e5699a |
| `0x1ee7074` | Traduit / contrôle ROM requis | 0x1e569bf |
| `0x1ee70c0` | Traduit / contrôle ROM requis | 0x1e569d2 |
| `0x1ee70fc` | Traduit / contrôle ROM requis | 0x1e569f4 |
| `0x1ee7188` | Traduit / contrôle ROM requis | 0x1e5665c, 0x1e566da, 0x1e56843 |
| `0x1ee71a0` | Traduit / contrôle ROM requis | 0x1e56668 |
| `0x1ee71f5` | Traduit / contrôle ROM requis | 0x1e566a0 |
| `0x1ee7369` | Traduit / contrôle ROM requis | 0x1e566ca |
| `0x1ee76d5` | Traduit / contrôle ROM requis | 0x1e56889 |
| `0x1ee78fb` | Traduit / contrôle ROM requis | 0x1e56707 |
| `0x1ee792b` | Traduit / contrôle ROM requis | 0x1e56732 |
| `0x1ee794d` | Traduit / contrôle ROM requis | 0x1e56797 |
| `0x1ee79b4` | Traduit / contrôle ROM requis | 0x1e567d7 |
| `0x1ee79b9` | Traduit / contrôle ROM requis | 0x1e56814 |
| `0x1ee7b08` | Traduit / contrôle ROM requis | 0x1e56892 |
| `0x1ee7b47` | Traduit / contrôle ROM requis | 0x1e56867 |
| `0x1ee7b7b` | Traduit / contrôle ROM requis | 0x1e56923 |
| `0x1ee7c01` | Traduit / contrôle ROM requis | 0x1e5692c |
| `0x1ee7c8b` | Traduit / contrôle ROM requis | 0x1e56974 |
| `0x1ee7d73` | Traduit / contrôle ROM requis | 0x1e5697d |
| `0x1ee7e2a` | Traduit / contrôle ROM requis | 0x1e56987 |
| `0x1ee7ebb` | Traduit / contrôle ROM requis | 0x1e56937 |
| `0x1ee7ed2` | Traduit / contrôle ROM requis | 0x1e5ad4c |
| `0x1ee7eeb` | Traduit / contrôle ROM requis | 0x1e56ac0 |
| `0x1ee7f03` | Traduit / contrôle ROM requis | 0x1e56bd4, 0x1e62fa4, 0x1e6a5b7 |
| `0x1ee7f15` | Traduit / contrôle ROM requis | 0x1e56c15 |
| `0x1ee7fb0` | Traduit / contrôle ROM requis | 0x1e56d32 |
| `0x1ee8013` | Traduit / contrôle ROM requis | 0x1e56c28 |
| `0x1ee8046` | Traduit / contrôle ROM requis | 0x1e56d44 |
| `0x1ee80ac` | Traduit / contrôle ROM requis | 0x1e56d56 |
| `0x1ee811f` | Traduit / contrôle ROM requis | 0x1e56c5c |
| `0x1ee8184` | Traduit / contrôle ROM requis | 0x1e56d11 |
| `0x1ee81a0` | Traduit / contrôle ROM requis | 0x1e56d24 |
| `0x1ee81be` | Traduit / contrôle ROM requis | 0x1e56d04 |
| `0x1ee81f5` | Traduit / contrôle ROM requis | 0x1e56d63 |
| `0x1ee8259` | Nom conservé F-759 / contrôle ROM requis | 0x1e56c68 |
| `0x1ee8265` | Nom conservé F-759 / contrôle ROM requis | 0x1e56c76 |
| `0x1ee8272` | Nom conservé F-759 / contrôle ROM requis | 0x1e56c84 |
| `0x1ee827e` | Nom conservé F-759 / contrôle ROM requis | 0x1e56c92 |
| `0x1ee828a` | Nom conservé F-759 / contrôle ROM requis | 0x1e56ca0 |
| `0x1ee8297` | Nom conservé F-759 / contrôle ROM requis | 0x1e56cae |
| `0x1ee82a3` | Traduit / contrôle ROM requis | 0x1e56d7a |
| `0x1ee82e1` | Traduit / contrôle ROM requis | 0x1e56d87 |
| `0x1ee832f` | Traduit / contrôle ROM requis | 0x1e56d9e |
| `0x1ee83cd` | Traduit / contrôle ROM requis | 0x1e56dab |
| `0x1ee8477` | Traduit / contrôle ROM requis | 0x1e56db9 |
| `0x1ee8520` | Traduit / contrôle ROM requis | 0x1e56dd7 |
| `0x1ee85fb` | Traduit / contrôle ROM requis | 0x1e56df7 |
| `0x1ee866d` | Traduit / contrôle ROM requis | 0x1e56e00 |
| `0x1ee8761` | Traduit / contrôle ROM requis | 0x1e56e12 |
| `0x1ee87ff` | Traduit / contrôle ROM requis | 0x1e56e35 |
| `0x1ee8849` | Traduit / contrôle ROM requis | 0x1e56e56 |
| `0x1ee8876` | Traduit / contrôle ROM requis | 0x1e56e63 |
| `0x1ee88c7` | Traduit / contrôle ROM requis | 0x1e56e81 |
| `0x1ee88f4` | Traduit / contrôle ROM requis | 0x1e56eab |
| `0x1ee89a9` | Traduit / contrôle ROM requis | 0x1e56eb4 |
| `0x1ee89b9` | Traduit / contrôle ROM requis | 0x1e56ebe |
| `0x1ee8a66` | Traduit / contrôle ROM requis | 0x1e56f8b |
| `0x1ee8ad5` | Traduit / contrôle ROM requis | 0x1e56fc4 |
| `0x1ee8b0c` | Traduit / contrôle ROM requis | 0x1e56fd4 |
| `0x1ee8b71` | Traduit / contrôle ROM requis | 0x1e56fe2 |
| `0x1ee8bb3` | Traduit / contrôle ROM requis | 0x1e56ff4 |
| `0x1ee8be6` | Traduit / contrôle ROM requis | 0x1e57002 |
| `0x1ee8ce0` | Traduit / contrôle ROM requis | 0x1e57010 |
| `0x1ee8e92` | Nom conservé F-759 / contrôle ROM requis | 0x1e5702b, 0x1e5707a, 0x1e57094 |
| `0x1ee8e9a` | Traduit / contrôle ROM requis | 0x1e57036 |
| `0x1ee8f94` | Traduit / contrôle ROM requis | 0x1e5709f |
| `0x1ee8fee` | Traduit / contrôle ROM requis | 0x1e57071 |
| `0x1ee9022` | Traduit / contrôle ROM requis | 0x1e57085 |
| `0x1ee9125` | Traduit / contrôle ROM requis | 0x1e570ed |
| `0x1ee9228` | Traduit / contrôle ROM requis | 0x1e570ab |
| `0x1ee926a` | Traduit / contrôle ROM requis | 0x1e570dc |
| `0x1ee92d1` | Traduit / contrôle ROM requis | 0x1fb1ef0 |
| `0x1ee965f` | Traduit / contrôle ROM requis | 0x1fb1ef4 |
| `0x1ee983c` | Traduit / contrôle ROM requis | 0x1fb1ef8 |
| `0x1ee9946` | Traduit / contrôle ROM requis | 0x1fb1efc |
| `0x1ee9a79` | Traduit / contrôle ROM requis | 0x1fb1f00 |
| `0x1ee9b98` | Traduit / contrôle ROM requis | 0x1fb1f04 |
| `0x1ee9c12` | Traduit / contrôle ROM requis | 0x1fb1f08 |
| `0x1ee9d32` | Traduit / contrôle ROM requis | 0x1fb1f0c |
| `0x1ee9fd2` | Traduit / contrôle ROM requis | 0x1fb1ec8 |
| `0x1ee9fdd` | Traduit / contrôle ROM requis | 0x1fb1ecc |
| `0x1ee9fe7` | Traduit / contrôle ROM requis | 0x1fb1ed0 |
| `0x1ee9ff1` | Traduit / contrôle ROM requis | 0x1fb1ed4 |
| `0x1ee9fff` | Traduit / contrôle ROM requis | 0x1fb1ed8 |
| `0x1eea010` | Traduit / contrôle ROM requis | 0x1fb1edc |
| `0x1eea01b` | Traduit / contrôle ROM requis | 0x1fb1ee0 |
| `0x1eea028` | Traduit / contrôle ROM requis | 0x1fb1ee4 |
| `0x1eea031` | Nom conservé F-759 / contrôle ROM requis | 0x1e57131, 0x1e5717e, 0x1e571ae, 0x1e571c9, 0x1e571e4, 0x1e571fb, 0x1e57212 |
| `0x1eea039` | Traduit / contrôle ROM requis | 0x23e760 |
| `0x1eea047` | Traduit / contrôle ROM requis | 0x1e571ef |
| `0x1eea180` | Traduit / contrôle ROM requis | 0x1e57206 |
| `0x1eea1ef` | Traduit / contrôle ROM requis | 0x1e5713c |
| `0x1eea2a7` | Exception : aucun lecteur de script identifié | 0x1eea1ef via 0x1e5713c; 0x1eea2d9 via 0x1e5721d |
| `0x1eea2d9` | Traduit / contrôle ROM requis | 0x1e5721d |
