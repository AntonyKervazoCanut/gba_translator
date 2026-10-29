# PT-29 — Antisis, Distortion World et messages système (F-788)

## Périmètre et livraison

Manifeste exact de 288 offsets : 264 traductions PT-BR, 3 noms anglais conservés
(Cube, Master Ball, Ultra Ball), 21 exceptions motivées ci-dessous. Aucun offset
source d’un autre lot n’est ajouté ; aucune traduction préexistante n’est supprimée.
Prérequis F-758 et F-759 terminés et intégrés avant traduction.

Le contenu réel couvre Aklove/Hoopa, Distortion World, Rift Cave, Route 16,
Antisis City (gangs, chaussettes, égouts et ringue), puis messages de terrain,
combat et méga-évolution. Les noms propres Borrius, factions, mouvements et objets
sans équivalent officiel attesté restent anglais selon F-759. Types Voador,
Psíquico, Fada, Venenoso ; statistique PS. Les deux variantes genrées sont conservées.

Le fichier `languages/pt/data/pt29_audit.json` est le bilan machine offset par
offset : source EN et comparaison FR last-wins, préimage binaire EN, pointeurs
alignés et non alignés, commandes, tailles encodées, budgets pixels et décision.
Les faux caractères du décodage EN ne sont jamais recopiés comme contrôles :
les octets FC/FD et leurs arguments sont lus dans la ROM propre.
À 0x876258, le corpus EN historique dit Hyper Ball alors que la ROM propre
contient Ultra Ball ; la vraie cellule gItems fait autorité.

## Injection dédiée

`languages/pt/patches/batch_29.py` réutilise BorriusTextPatch et StructuredTextPatch,
après les réparations/repointages génériques, pour vérifier 265 consommateurs
texte, relocaliser si nécessaire et contrôler les octets aux pointeurs vivants.
Les deux noms de Balls sont vérifiés dans gItems 0x876200 (44 octets/cellule),
racine moteur 0x9a8d8 ; aucun repointage de ces cellules fixes.

La clé 0x834ae7 inclut 13 octets de bourrage avant le titre réel 0x834af4,
consommé par 0x834270. Son finaliseur vérifie le préfixe et sa préimage, restaure
le bourrage que l’étape générique pourrait écraser et repointe le titre réel.
Il ne modifie ni la palette voisine ni une autre entrée du manifeste.
Les pixels 4bpp à 0x827f30 ont un pointeur vivant **graphique** : ils restent intacts.
Les motifs de pixels à 0xfa6636 et 0xfa6c32 imitent l’adresse du message
0x800880 : seul le pointeur de table combat 0x3fdf78 est textuel. Le finaliseur
restaure aussi ces deux motifs après le passage générique et les tests comparent
leurs voisins à la source. Le relevé distingue références brutes et consommateurs texte.

Tous les FC/FD/FA/FB/FE restent dans le même ordre, arguments et nombres de ruptures
compris. Chaque ligne est protégée dans protected_entries.yaml. La limite locale
est 192 pixels estimés ; les tests mesurent aussi les cinq vraies polices avec
tampons développés (limite 208 pixels), ainsi que l’isolation, l’atomicité,
l’idempotence, les préimages et l’absence de chevauchement.

## Validation

Les résultats exécutés et la limite de couverture visuelle sont consignés dans
le bilan du ticket. La recette locale reproductible est :

```sh
python3 -m pytest tests/unit/pt/test_batch_pt29.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt29_rom.py -q
npx playwright test --config tests/e2e-playwright/playwright.pt29.config.ts
```

La sonde Playwright lance mGBA hors écran, utilise les pointeurs et textes de la
ROM finale et vérifie les lignes affichées par OCR. Elle ajoute seulement un
script msgbox à une copie temporaire. Elle ne modifie ni les glyphes ni les textes,
et vérifie que la copie de sauvegarde est intacte. La capture est dans le dossier
temporaire système et jointe au ticket ; aucune image de preuve dans Git.
Cette sonde ne certifie pas un parcours complet des événements ni toutes les pages
en émulateur. Les 267 entrées sont contrôlées en binaire ; T-848 garde la recette
complète de certification du jeu. Aucun code partagé, ROM distribuée, push ou
pipeline distant n’est modifié par ce lot.

## Bilan des 288 offsets

| Offset | Décision | Pointeurs / justification |
| --- | --- | --- |
| `0x7f518d` | traduit / vérifié par test ROM | 0x7f41d9 |
| `0x7f5200` | traduit / vérifié par test ROM | 0x7f41f5 |
| `0x7f521d` | traduit / vérifié par test ROM | 0x7f4208 |
| `0x7f527b` | traduit / vérifié par test ROM | 0x7f4229 |
| `0x7f5342` | traduit / vérifié par test ROM | 0x7f423c |
| `0x7f5401` | traduit / vérifié par test ROM | 0x7f426d |
| `0x7f5448` | traduit / vérifié par test ROM | 0x7f4280 |
| `0x7f5522` | traduit / vérifié par test ROM | 0x7f428c |
| `0x7f55f4` | traduit / vérifié par test ROM | 0x7f429f |
| `0x7f564f` | traduit / vérifié par test ROM | 0x7f42b9 |
| `0x7f5670` | traduit / vérifié par test ROM | 0x7f42d0 |
| `0x7f5680` | traduit / vérifié par test ROM | 0x7f42f9 |
| `0x7f56f1` | traduit / vérifié par test ROM | 0x7f4305 |
| `0x7f5700` | traduit / vérifié par test ROM | 0x7f4313 |
| `0x7f5709` | traduit / vérifié par test ROM | 0x7f4412 |
| `0x7f5754` | traduit / vérifié par test ROM | 0x7f441c |
| `0x7f57ec` | traduit / vérifié par test ROM | 0x7f4426 |
| `0x7f5821` | traduit / vérifié par test ROM | 0x7f4430 |
| `0x7f5857` | traduit / vérifié par test ROM | 0x7f4374 |
| `0x7f5869` | traduit / vérifié par test ROM | 0x7f4378 |
| `0x7f589b` | traduit / vérifié par test ROM | 0x7f445d |
| `0x7f58ff` | traduit / vérifié par test ROM | 0x7f4470 |
| `0x7f5932` | traduit / vérifié par test ROM | 0x7f447a |
| `0x7f59db` | traduit / vérifié par test ROM | 0x7f4394 |
| `0x7f5a1f` | traduit / vérifié par test ROM | 0x7f443a |
| `0x7f5a45` | traduit / vérifié par test ROM | 0x7f4444 |
| `0x7f5a6b` | traduit / vérifié par test ROM | 0x7f43cc |
| `0x7f5ae0` | traduit / vérifié par test ROM | 0x7a59fc |
| `0x7f5bfd` | traduit / vérifié par test ROM | 0x7a5a12 |
| `0x7f5ca1` | traduit / vérifié par test ROM | 0x7f5c54 |
| `0x7f5d1e` | traduit / vérifié par test ROM | 0x7a5b46, 0x7a69db |
| `0x7f5d67` | exception | Extraction démarrant dans le script à 0x7f5d63 (pointeur 0x7a5b3d), pas dans un texte. Aucun pointeur vers 0x7f5d67. Le texte réel est 0x7f5daf, référencé par 0x7f5d74 et traité dans ce lot. |
| `0x7f5daf` | traduit / vérifié par test ROM | 0x7f5d74 |
| `0x7f5e95` | traduit / vérifié par test ROM | 0x7f5d80, 0x7f5da8 |
| `0x7f5ef3` | traduit / vérifié par test ROM | 0x7f5ee6, 0x7f6224 |
| `0x7f5fcf` | traduit / vérifié par test ROM | 0x7f61c0 |
| `0x7f60d7` | traduit / vérifié par test ROM | 0x7f60a7 |
| `0x7f62f0` | traduit / vérifié par test ROM | 0x7f6237 |
| `0x7f6331` | traduit / vérifié par test ROM | 0x7f6244 |
| `0x7f6350` | traduit / vérifié par test ROM | 0x7f6267 |
| `0x7f636c` | traduit / vérifié par test ROM | 0x7f62b2 |
| `0x7f6452` | traduit / vérifié par test ROM | 0x7f5f8e |
| `0x7f6497` | traduit / vérifié par test ROM | 0x7f5fa1 |
| `0x7f691e` | traduit / vérifié par test ROM | 0x7f6877 |
| `0x7f6932` | traduit / vérifié par test ROM | 0x7f68dc |
| `0x7f6960` | traduit / vérifié par test ROM | 0x7f68e7 |
| `0x7f6aca` | traduit / vérifié par test ROM | 0x7f6a6b |
| `0x7f6ae0` | traduit / vérifié par test ROM | 0x7f6a81 |
| `0x7f6b6d` | traduit / vérifié par test ROM | 0x7f6a9b |
| `0x7f6e4c` | traduit / vérifié par test ROM | 0x7f6d0c, 0x7f6d16 |
| `0x7f6e6f` | traduit / vérifié par test ROM | 0x7f6d32 |
| `0x7f6e9c` | traduit / vérifié par test ROM | 0x7f6d45 |
| `0x7f6ee7` | traduit / vérifié par test ROM | 0x7f6d51 |
| `0x7f6f28` | traduit / vérifié par test ROM | 0x7f6d66 |
| `0x7f6f4c` | traduit / vérifié par test ROM | 0x7f6d70 |
| `0x7f6f8c` | traduit / vérifié par test ROM | 0x7f6d88 |
| `0x7f6fd5` | traduit / vérifié par test ROM | 0x7f6d98 |
| `0x7f6ff4` | traduit / vérifié par test ROM | 0x7f6e16 |
| `0x7f7004` | traduit / vérifié par test ROM | 0x7f6e30 |
| `0x7f715d` | traduit / vérifié par test ROM | 0x7f70e7, 0x7f710e |
| `0x7f7198` | traduit / vérifié par test ROM | 0x7f70fd |
| `0x7f7231` | traduit / vérifié par test ROM | 0x7f71e0, 0x7f7207 |
| `0x7f7251` | traduit / vérifié par test ROM | 0x7f71f6 |
| `0x7f72cb` | traduit / vérifié par test ROM | 0x7f7297, 0x7f72be |
| `0x7f7309` | traduit / vérifié par test ROM | 0x7f729b, 0x7f72c2 |
| `0x7f732f` | traduit / vérifié par test ROM | 0x7f72b1 |
| `0x7f73e1` | traduit / vérifié par test ROM | 0x7f737a, 0x7f73a1 |
| `0x7f73f4` | traduit / vérifié par test ROM | 0x7f7390 |
| `0x7f7486` | traduit / vérifié par test ROM | 0x7f742b, 0x7f7452 |
| `0x7f7493` | traduit / vérifié par test ROM | 0x7f7441 |
| `0x7f7563` | traduit / vérifié par test ROM | 0x7f74df, 0x7f7506 |
| `0x7f759b` | traduit / vérifié par test ROM | 0x7f74f5 |
| `0x7f7666` | traduit / vérifié par test ROM | 0x7f75e4, 0x7f760b |
| `0x7f7670` | traduit / vérifié par test ROM | 0x7f75fa |
| `0x7f772a` | traduit / vérifié par test ROM | 0x7f76b6, 0x7f76dd |
| `0x7f7741` | traduit / vérifié par test ROM | 0x7f76cc |
| `0x7f7862` | traduit / vérifié par test ROM | 0x7f77cb, 0x7f77f2 |
| `0x7f7880` | traduit / vérifié par test ROM | 0x7f77e1 |
| `0x7f790b` | traduit / vérifié par test ROM | 0x7f78ad, 0x7f78d4 |
| `0x7f791e` | traduit / vérifié par test ROM | 0x7f78c3 |
| `0x7f7994` | traduit / vérifié par test ROM | 0x7a5af4 |
| `0x7f79c2` | traduit / vérifié par test ROM | 0x7a5af8 |
| `0x7f79d5` | traduit / vérifié par test ROM | 0x7a5afe |
| `0x7f79f9` | traduit / vérifié par test ROM | 0x7a5b6d |
| `0x7f7bef` | traduit / vérifié par test ROM | 0x7f7a22 |
| `0x7f7c2d` | traduit / vérifié par test ROM | 0x7f7a42 |
| `0x7f7c71` | traduit / vérifié par test ROM | 0x7f7a55 |
| `0x7f7cd9` | traduit / vérifié par test ROM | 0x7f7a6b |
| `0x7f7dcc` | traduit / vérifié par test ROM | 0x7f7a7e |
| `0x7f8011` | traduit / vérifié par test ROM | 0x7f7a9f |
| `0x7f805a` | traduit / vérifié par test ROM | 0x7f7ab2 |
| `0x7f80cb` | traduit / vérifié par test ROM | 0x7f7ac5 |
| `0x7f8154` | traduit / vérifié par test ROM | 0x7f7ad8 |
| `0x7f819f` | traduit / vérifié par test ROM | 0x7f7afe |
| `0x7f81d9` | traduit / vérifié par test ROM | 0x7f7b32 |
| `0x7f820c` | traduit / vérifié par test ROM | 0x7f7b82 |
| `0x7f8229` | traduit / vérifié par test ROM | 0x7f7bb0 |
| `0x7f8248` | traduit / vérifié par test ROM | 0x7f7bcc |
| `0x7f885a` | traduit / vérifié par test ROM | 0x7c0a65 |
| `0x7f89b6` | traduit / vérifié par test ROM | 0x7c0a0c |
| `0x7f8a44` | traduit / vérifié par test ROM | 0x7f8a33 |
| `0x7f8b25` | traduit / vérifié par test ROM | 0x7f8adb |
| `0x7f8ba7` | traduit / vérifié par test ROM | 0x7f8ae4 |
| `0x7f8c2b` | traduit / vérifié par test ROM | 0x7f8aed |
| `0x7f8ca4` | traduit / vérifié par test ROM | 0x7f8b15 |
| `0x7f8cd6` | traduit / vérifié par test ROM | 0x7f8b1e |
| `0x7f8cea` | traduit / vérifié par test ROM | 0x7c0a22 |
| `0x7f8dfa` | traduit / vérifié par test ROM | 0x7f8d51 |
| `0x7f8e1b` | traduit / vérifié par test ROM | 0x1a6641, 0x7f8d9d |
| `0x7f8e80` | traduit / vérifié par test ROM | 0x1a6656, 0x7f8da9, 0x7f8db6 |
| `0x7f8eae` | traduit / vérifié par test ROM | 0x7c0a78 |
| `0x7f8f39` | traduit / vérifié par test ROM | 0x7f8ff7 |
| `0x7f9015` | traduit / vérifié par test ROM | 0x7f900a |
| `0x7f90ba` | traduit / vérifié par test ROM | 0x7f90a9 |
| `0x7f912c` | traduit / vérifié par test ROM | 0x7c0aa3 |
| `0x7f924c` | traduit / vérifié par test ROM | 0x7f923b |
| `0x7f92af` | traduit / vérifié par test ROM | 0x7f929e |
| `0x7f9425` | traduit / vérifié par test ROM | 0x7f940c |
| `0x7f95a4` | traduit / vérifié par test ROM | 0x7f94c2 |
| `0x7f9624` | traduit / vérifié par test ROM | 0x7f94cb |
| `0x7f96a5` | traduit / vérifié par test ROM | 0x7f947c |
| `0x7f97ca` | traduit / vérifié par test ROM | 0x7f94d4 |
| `0x7f97f4` | traduit / vérifié par test ROM | 0x7f94dd |
| `0x7f981f` | traduit / vérifié par test ROM | 0x7f94ae |
| `0x7f987d` | traduit / vérifié par test ROM | 0x7f94e6 |
| `0x7f98f6` | traduit / vérifié par test ROM | 0x7f94fa |
| `0x7f991f` | traduit / vérifié par test ROM | 0x7f9503 |
| `0x7f9957` | traduit / vérifié par test ROM | 0x7f9514 |
| `0x7f999a` | traduit / vérifié par test ROM | 0x7f9540 |
| `0x7f9a0d` | traduit / vérifié par test ROM | 0x7f9592 |
| `0x7f9a69` | traduit / vérifié par test ROM | 0x7f957e |
| `0x7f9a9a` | traduit / vérifié par test ROM | 0x78a9c5 |
| `0x7f9b92` | traduit / vérifié par test ROM | 0x7f9b81 |
| `0x7f9c4a` | traduit / vérifié par test ROM | 0x7f9c04 |
| `0x7f9c81` | traduit / vérifié par test ROM | 0x7f9c21 |
| `0x7f9dea` | traduit / vérifié par test ROM | 0x7f9db5 |
| `0x7f9ece` | traduit / vérifié par test ROM | 0x7f9dc8 |
| `0x7f9f05` | traduit / vérifié par test ROM | 0x7f9de2 |
| `0x7f9f48` | traduit / vérifié par test ROM | 0x761749 |
| `0x7fa1f7` | exception | Texte isolé après bourrage FF, sans aucun pointeur 32 bits (aligné ou non) vers son début, ni table de cellules identifiée ; aucune injection hasardeuse. Le dialogue de vol actif commence à 0x7fa4c8, pointeur 0x7fa274. |
| `0x7fa4c8` | traduit / vérifié par test ROM | 0x7fa274 |
| `0x7fa546` | traduit / vérifié par test ROM | 0x7fa287 |
| `0x7fa608` | traduit / vérifié par test ROM | 0x7fa292 |
| `0x7fa624` | exception | Réplique sans pointeur, non consommée par le script de vol actif. La question du déguisement est à 0x7fa608 via 0x7fa292 ; les branches actives aboutissent notamment à 0x7fa63f via 0x7fa2c3. |
| `0x7fa63f` | traduit / vérifié par test ROM | 0x7fa2c3 |
| `0x7fa65e` | traduit / vérifié par test ROM | 0x7fa4c0 |
| `0x7fa68e` | traduit / vérifié par test ROM | 0x7fa3c2 |
| `0x7fa7bf` | traduit / vérifié par test ROM | 0x7fa3d5 |
| `0x7fa7ec` | traduit / vérifié par test ROM | 0x7fa490 |
| `0x7fa834` | traduit / vérifié par test ROM | 0x7fa49a |
| `0x7fa85f` | traduit / vérifié par test ROM | 0x7fa40d |
| `0x7fa877` | traduit / vérifié par test ROM | 0x7fa44d |
| `0x7fa8dd` | traduit / vérifié par test ROM | 0x7fa481 |
| `0x7fa940` | traduit / vérifié par test ROM | 0x7fa4a8 |
| `0x7faf90` | traduit / vérifié par test ROM | 0x7faf88 |
| `0x7fb0fb` | traduit / vérifié par test ROM | 0x7fb014 |
| `0x7fb156` | traduit / vérifié par test ROM | 0x7fb027 |
| `0x7fb28a` | traduit / vérifié par test ROM | 0x7fb046 |
| `0x7fb2b6` | traduit / vérifié par test ROM | 0x7fb05d |
| `0x7fb2d9` | traduit / vérifié par test ROM | 0x7fb067 |
| `0x7fb318` | traduit / vérifié par test ROM | 0x7fb0d1 |
| `0x7fb369` | traduit / vérifié par test ROM | 0x7fb071 |
| `0x7fb3c9` | traduit / vérifié par test ROM | 0x7fb09d |
| `0x7fb449` | traduit / vérifié par test ROM | 0x7fb0e9 |
| `0x7fb47f` | traduit / vérifié par test ROM | 0x7fb0f3 |
| `0x7fb6f3` | traduit / vérifié par test ROM | 0x7fb4c7, 0x7fb6b6 |
| `0x7fb735` | traduit / vérifié par test ROM | 0x7fb4eb |
| `0x7fb779` | traduit / vérifié par test ROM | 0x7fb50c |
| `0x7fb7e0` | traduit / vérifié par test ROM | 0x7fb632 |
| `0x7fb835` | traduit / vérifié par test ROM | 0x7fb639 |
| `0x7fb88a` | traduit / vérifié par test ROM | 0x7fb54a |
| `0x7fb8db` | traduit / vérifié par test ROM | 0x7fb55d |
| `0x7fb93c` | traduit / vérifié par test ROM | 0x7fb583 |
| `0x7fb97b` | traduit / vérifié par test ROM | 0x7fb590 |
| `0x7fb9a1` | traduit / vérifié par test ROM | 0x7fb594 |
| `0x7fb9d2` | traduit / vérifié par test ROM | 0x7fb5b2 |
| `0x7fba42` | traduit / vérifié par test ROM | 0x7fb5c8 |
| `0x7fbabb` | traduit / vérifié par test ROM | 0x7fb5e2 |
| `0x7fbb84` | traduit / vérifié par test ROM | 0x7fb646 |
| `0x7fbbd2` | traduit / vérifié par test ROM | 0x7fb660 |
| `0x7fbc63` | traduit / vérifié par test ROM | 0x7fb6ce |
| `0x7fbe45` | traduit / vérifié par test ROM | 0x7fbdd0 |
| `0x7fbe82` | traduit / vérifié par test ROM | 0x7fbdd6 |
| `0x7fbee1` | traduit / vérifié par test ROM | 0x7fbecb |
| `0x7fbeeb` | traduit / vérifié par test ROM | 0x7fbed1 |
| `0x7fbf6e` | traduit / vérifié par test ROM | 0x7fbf31 |
| `0x7fbfc1` | traduit / vérifié par test ROM | 0x7fbf37 |
| `0x7fc046` | traduit / vérifié par test ROM | 0x7fc01a |
| `0x7fc0a2` | traduit / vérifié par test ROM | 0x7fc06d |
| `0x7fc0c0` | traduit / vérifié par test ROM | 0x7fc073 |
| `0x7fc150` | traduit / vérifié par test ROM | 0x7fc10c |
| `0x7fc163` | traduit / vérifié par test ROM | 0x7fc112 |
| `0x7fc3b4` | traduit / vérifié par test ROM | 0x7fc20c |
| `0x7fc4cd` | traduit / vérifié par test ROM | 0x7fc2ad, 0x7fc2d7, 0x7fc301, 0x7fc32b, 0x7fc355, 0x7fc37f |
| `0x7fc51e` | traduit / vérifié par test ROM | 0x7fc3a7 |
| `0x7fc549` | traduit / vérifié par test ROM | 0x7fc27f |
| `0x7fc819` | traduit / vérifié par test ROM | 0x7fc757 |
| `0x7fc845` | traduit / vérifié par test ROM | 0x7fc78c |
| `0x7fc89b` | traduit / vérifié par test ROM | 0x7fc7bb |
| `0x7fca8c` | traduit / vérifié par test ROM | 0x7fc8eb |
| `0x7fcb63` | traduit / vérifié par test ROM | 0x7fc8fe |
| `0x7fcbe9` | traduit / vérifié par test ROM | 0x7fc911 |
| `0x7fccf4` | traduit / vérifié par test ROM | 0x7fc92b |
| `0x7fcd16` | traduit / vérifié par test ROM | 0x7fc93e |
| `0x7fcd63` | traduit / vérifié par test ROM | 0x7fc951 |
| `0x7fcde1` | traduit / vérifié par test ROM | 0x7fc97c |
| `0x7fce25` | traduit / vérifié par test ROM | 0x7fc98e |
| `0x7fce4d` | traduit / vérifié par test ROM | 0x7fc9b6 |
| `0x7fcf19` | traduit / vérifié par test ROM | 0x7fc9d0 |
| `0x7fcf40` | traduit / vérifié par test ROM | 0x7fc9ef |
| `0x7fd049` | traduit / vérifié par test ROM | 0x7fca0f |
| `0x7fd0a5` | traduit / vérifié par test ROM | 0x7fca6e |
| `0x7fd164` | traduit / vérifié par test ROM | 0x7fd154 |
| `0x7fd1b3` | traduit / vérifié par test ROM | 0x7fd15d |
| `0x7fd4ac` | traduit / vérifié par test ROM | 0x7fd226 |
| `0x7fd4b2` | traduit / vérifié par test ROM | 0x7fd234 |
| `0x7fd4b8` | traduit / vérifié par test ROM | 0x7fd242 |
| `0x7fd4be` | traduit / vérifié par test ROM | 0x7fd2c9 |
| `0x7fd4c9` | traduit / vérifié par test ROM | 0x7fd305 |
| `0x7fd50f` | traduit / vérifié par test ROM | 0x7fd362 |
| `0x7fd545` | traduit / vérifié par test ROM | 0x7fd3bf |
| `0x7fd59c` | traduit / vérifié par test ROM | 0x7fd317 |
| `0x7fd5a4` | traduit / vérifié par test ROM | 0x7fd374 |
| `0x7fd5c0` | traduit / vérifié par test ROM | 0x7fd3d1 |
| `0x7fd5ee` | traduit / vérifié par test ROM | 0x7fd421 |
| `0x7fd645` | traduit / vérifié par test ROM | 0x7fd437 |
| `0x7fd75b` | traduit / vérifié par test ROM | 0x7fd444 |
| `0x7fd7ca` | traduit / vérifié par test ROM | 0x7fd46e |
| `0x7fd829` | traduit / vérifié par test ROM | 0x7fd477 |
| `0x7fd8a5` | traduit / vérifié par test ROM | 0x7fd44d |
| `0x7fd8ac` | traduit / vérifié par test ROM | 0x7fd458 |
| `0x7fd8b4` | traduit / vérifié par test ROM | 0x7fd463 |
| `0x7fda18` | traduit / vérifié par test ROM | 0x7fd934 |
| `0x7fdb0d` | traduit / vérifié par test ROM | 0x7fd973 |
| `0x7fdb88` | traduit / vérifié par test ROM | 0x7fd986 |
| `0x7fdc0a` | traduit / vérifié par test ROM | 0x7fd977, 0x7fd98a |
| `0x7fdc3d` | traduit / vérifié par test ROM | 0x7fd9ac |
| `0x7fdc9b` | traduit / vérifié par test ROM | 0x7fd9b9 |
| `0x7fdcc4` | traduit / vérifié par test ROM | 0x7fd9c4 |
| `0x7fdd8c` | traduit / vérifié par test ROM | 0x7fd9e6 |
| `0x7fdd98` | exception | Suffixe intérieur de 0x7fdd8c ; aucun pointeur autonome. La chaîne complète est référencée par 0x7fd9e6, traduite dans ce lot sans écrire dans son suffixe. |
| `0x7fddaa` | traduit / vérifié par test ROM | 0x7fda03 |
| `0x7fde03` | traduit / vérifié par test ROM | 0x7fda10 |
| `0x7fde41` | traduit / vérifié par test ROM | 0x7fd965 |
| `0x7fdee5` | traduit / vérifié par test ROM | 0x7fded5 |
| `0x7fdf17` | traduit / vérifié par test ROM | 0x7fdede |
| `0x7fdf61` | traduit / vérifié par test ROM | 0x7fdf51 |
| `0x7fdf99` | traduit / vérifié par test ROM | 0x7fdf5a |
| `0x800880` | traduit / vérifié par test ROM | Message vivant dans la table combat via 0x3fdf78. Les deux motifs 80 08 80 08 à 0xfa6636 et 0xfa6c32 sont des pixels 4bpp au milieu de tuiles 80/86/66/8F/76/7F/77/87 et de bourrage nul, pas des pointeurs. Ils sont exclus et restaurés après le passage générique. |
| `0x800fc0` | nom conservé / vérifié par test ROM | Nom propre Cube conservé selon F-759, vérifié via le pointeur 0x3a7354. |
| `0x800fd0` | traduit / vérifié par test ROM | 0x452024 |
| `0x80dc10` | traduit / vérifié par test ROM | 0x80dbe8 |
| `0x81e670` | exception | Données graphiques, pas du texte : motif binaire F0 DD BB BB D0 BB BB BB et mots FFFFFFF0 voisins. Aucun pointeur vers cette extraction ; octets conservés. |
| `0x81f370` | exception | Pixels 4bpp (EEEEEEEE puis FF5F9559...), pas la chaîne zzzz. Aucun pointeur texte vers cette adresse ; octets conservés. |
| `0x81f3f0` | exception | Pixels 4bpp (EEEEEEEE puis FFFFFF5F répétés), pas la chaîne zzzz. Aucun pointeur texte ; octets conservés. |
| `0x820da0` | traduit / vérifié par test ROM | 0x820a10 |
| `0x821093` | traduit / vérifié par test ROM | 0x82108b |
| `0x8210bf` | traduit / vérifié par test ROM | 0x821079 |
| `0x8210e0` | exception | Copie isolée sans pointeur, suivie de bourrage FF puis graphismes compressés. Le mur actif est 0x8254bf via 0x82540f et 0x8254fd via 0x82545e, tous deux traduits ici. |
| `0x8217fd` | exception | Extraction au milieu de données graphiques compressées, pas du texte (EE CC CD AA...). Aucun pointeur vers cette adresse ; octets conservés. |
| `0x8254bf` | traduit / vérifié par test ROM | 0x82540f |
| `0x8254f1` | traduit / vérifié par test ROM | 0x825422 |
| `0x8254fd` | traduit / vérifié par test ROM | 0x82545e |
| `0x825535` | traduit / vérifié par test ROM | 0x825469 |
| `0x825660` | traduit / vérifié par test ROM | 0x800df5 |
| `0x825680` | traduit / vérifié par test ROM | 0x800dd5, 0x82564c |
| `0x82595c` | exception | Ancienne réplique isolée de marchand, sans pointeur 32 bits aligné ou non et sans consommateur de table identifié. Aucun texte injecté dans cette copie sans référence. |
| `0x827f30` | exception | Tuiles graphiques 4bpp : le pointeur 0x8280f0 est une entrée de table graphique, voisin de 0x828010 à 0x8280f4 ; table à 0x8280f0 référencée par 0x828108. Ce pointeur est vivant mais ne consomme PAS du texte. |
| `0x827fa4` | exception | Motifs de tuiles 4bpp dans le bloc 0x827f30, référencé comme graphisme par 0x8280f0 ; aucun pointeur vers cette sous-adresse. |
| `0x827fc0` | exception | Motifs de tuiles 4bpp CC/DD dans le bloc graphique 0x827f30 (pointeur 0x8280f0), aucun pointeur texte propre. |
| `0x827fe0` | exception | Motifs de tuiles 4bpp CC/DD dans le bloc graphique 0x827f30 (pointeur 0x8280f0), aucun pointeur texte propre. |
| `0x828088` | exception | Motifs de tuiles 4bpp dans le bloc 0x828010 (pointeur graphique 0x8280f4), aucun pointeur texte propre. |
| `0x8280a4` | exception | Motifs de tuiles 4bpp dans le bloc 0x828010 (pointeur graphique 0x8280f4), aucun pointeur texte propre. |
| `0x83001c` | traduit / vérifié par test ROM | 0x82ffcc, 0x82ffd4 |
| `0x83003b` | exception | Bourrage 00 avant le vrai début 0x83003c ; aucun pointeur vers 0x83003b. Le message actif est 0x83003c via 0x82ffe8, traduit ici. |
| `0x83003c` | traduit / vérifié par test ROM | 0x82ffe8 |
| `0x830066` | exception | Deux octets de bourrage 00 avant le message actif 0x830068, référencé par 0x82ffe4 et traduit ici. Aucun pointeur vers 0x830066. |
| `0x830068` | traduit / vérifié par test ROM | 0x82ffe4 |
| `0x83008a` | exception | Deux octets de bourrage 00 avant le message actif 0x83008c, référencé par 0x82ffdc et traduit ici. Aucun pointeur vers 0x83008a. |
| `0x83008c` | traduit / vérifié par test ROM | 0x82ffdc |
| `0x830cd0` | exception | Nom anglais Power Construct conservé selon F-759 ; copie sans pointeur direct, aucune table de noms à cet emplacement. Aucune traduction officielle inventée ni écriture sans consommateur démontré. |
| `0x830ce0` | traduit / vérifié par test ROM | 0x8b855f |
| `0x830cf6` | traduit / vérifié par test ROM | 0x8b8537 |
| `0x830d1a` | traduit / vérifié par test ROM | 0x8b8587 |
| `0x834acc` | exception | POKéMON est une marque conservée. Copie sans pointeur direct, entre la fin du texte précédent et une palette 16 bits (7FFF...). Aucune écriture nécessaire ni traduction revendiquée. |
| `0x834ae7` | traduit / vérifié par test ROM | Clé du manifeste commençant dans 13 octets de bourrage nul ; consommateur réel 0x834af4 via 0x834270. Patch dédié de ce seul consommateur, sans écrire dans la palette ni le bourrage. |
| `0x87622c` | nom conservé / vérifié par test ROM | Nom anglais conservé selon F-759, déjà correct dans la vraie table gItems à 0x876200, cellules 44 octets, indices 1 et 2. Racine moteur 0x9a8d8. Aucun repointage de cellule fixe. |
| `0x876258` | nom conservé / vérifié par test ROM | Nom anglais conservé selon F-759, déjà correct dans la vraie table gItems à 0x876200, cellules 44 octets, indices 1 et 2. Racine moteur 0x9a8d8. Aucun repointage de cellule fixe. |
