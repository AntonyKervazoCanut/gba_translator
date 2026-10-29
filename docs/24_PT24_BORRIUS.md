# PT-24 — Borrius et objets (F-783)

Les 288 offsets explicites du manifeste : 243 traductions, 12 textes conservés selon F-759 et 33 exceptions (30 sans référence, trois fragments corrompus pointés). Les prérequis c5b5e0b9 et dcc6ce5d sont intégrés.

Zones : Blizzard City, Thundercap Mountain, Route 9, Antisis City, Fallshore City, Tarmigan Town, panneaux routiers, Shadows et accompagnement de Milo. Le lot inclut 23 descriptions d’objets.

## Livraison et budgets

Les sources EN/FR sont confrontées aux octets de la ROM propre. Certaines extractions EN sont vides, françaises ou tronquées. 0x7b3c6a est Life Orb (pas une potion) et 0x7b3eb0 est Quick Ball (pas Master Ball). Les longs dialogues 0x7a9a75 et 0x7aaeca sont traduits jusqu’au vrai terminateur.

Le patch batch_24 réutilise StructuredTextPatch après les passes génériques. Chaque consommateur est repointé. La table fixe des objets (base 0x876074, pas 44, pointeur +20) garde sa structure : aucun agrandissement de cellule. Aucun code partagé ni autre langue modifié.

Codes, paramètres et ruptures FE/FA/FB conservés dans leur ordre exact. Budgets : dialogues 208 pixels, descriptions 192 pixels sur deux ou trois lignes ; cinq polices réelles et tampons de dix W. Le validateur partagé additionne les segments FA : le wrapper contrôle les lignes séparément avant de déclarer la largeur cumulée.

## Exceptions

Les fragments 0x7ab089 (pointeur 0x7538cb), 0x7b4a4e (0xb50347) et 0x7b8edd (0x7a8c9a) sont déjà incomplets dans la ROM source. Aucune restitution narrative arbitraire. Une absence de pointeur n’est jamais présentée comme une traduction. Le JSON donne chaque préimage et les références du propriétaire voisin lorsqu’il existe.

## Validation reproductible

```sh
make build-pt
python3 -m pytest -q tests/unit/pt/test_batch_pt24.py tests/unit/test_translation_integrity.py
python3 -m pytest -q tests/e2e/pt/test_batch_pt24_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt24.config.ts
```

Les sondes mGBA/Playwright utilisent les pointeurs livrés sur une copie temporaire, hors écran et sans sauvegarder en jeu. Elles ne constituent pas une validation du parcours complet. Captures hors dépôt.

## Bilan offset par offset

Détail machine : languages/pt/data/pt24_audit.json (anglais, comparaison FR, préimages, budgets et pointeurs).

| Offset | Statut | Pointeurs | Justification |
|---|---|---|---|
| `0x7a8d51` | Traduit / vérifié | 0x78d261 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a94e4` | Traduit / vérifié | 0x7a8a6b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a95bc` | Traduit / vérifié | 0x74b0a0 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a96e6` | Traduit / vérifié | 0x74b0bf | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a97de` | Traduit / vérifié | 0x74bb34 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a99c5` | Traduit / vérifié | 0x7a4485 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a9a75` | Traduit / vérifié | 0x74b0aa | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a9e8f` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7a9ea3, références 0x75c043. |
| `0x7a9ea3` | Traduit / vérifié | 0x75c043 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7a9f78` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7a9f79, références 0x75c0dd. |
| `0x7a9f79` | Traduit / vérifié | 0x75c0dd | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa251` | Traduit / vérifié | 0x78d265 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa277` | Traduit / vérifié | 0x78d26b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa2dc` | Traduit / vérifié | 0x7aa2d5 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa2fa` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7aa4de` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7aa4df, références 0x794212. |
| `0x7aa4df` | Traduit / vérifié | 0x794212 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa6a7` | Traduit / vérifié | 0x794225 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa6e9` | Traduit / vérifié | 0x78c0fe | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa7dc` | Traduit / vérifié | 0x7a82f1 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa853` | Traduit / vérifié | 0x7736cb | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa8ce` | Traduit / vérifié | 0x7a8337 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa8e5` | Traduit / vérifié | 0x7a832a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa94d` | Traduit / vérifié | 0x7aa917 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aa9bd` | Traduit / vérifié | 0x76511c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aab04` | Traduit / vérifié | 0x7a831c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aab4d` | Traduit / vérifié | 0x7736cf | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aab5e` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7aab5f, références 0x76512b. |
| `0x7aab5f` | Traduit / vérifié | 0x76512b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aac3a` | Traduit / vérifié | 0x7884f9 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aaca4` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7aadc3` | Traduit / vérifié | 0x7653d3 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aae6a` | Traduit / vérifié | 0x765cbc | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7aaeca` | Traduit / vérifié | 0x779521 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ab089` | Exception | 0x7538cb | Source corrompue : le script pointe au milieu du texte parent, produisant un fragment incomplet. Pas de traduction inventée ni de modification de cette référence. Préimage apparentée : 0x7aaeca, références 0x779521. |
| `0x7ab17d` | Traduit / vérifié | 0x78c07a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ab33c` | Traduit / vérifié | 0x78c091 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ab4ff` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7ab500, références 0x78c625. |
| `0x7ab500` | Traduit / vérifié | 0x78c625 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ab69d` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7ab6a5` | Traduit / vérifié | 0x78c677 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ab773` | Traduit / vérifié | 0x7736d5 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ac5d1` | Traduit / vérifié | 0x78c6ba | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ac678` | Traduit / vérifié | 0x78c79a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ac6f1` | Traduit / vérifié | 0x78c56e | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b1421` | Traduit / vérifié | 0x776040 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b1461` | Traduit / vérifié | 0x78038c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b14ab` | Traduit / vérifié | 0x780390 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b14d6` | Conservé / vérifié | 0x74ac37 | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b1503` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b1ce1` | Traduit / vérifié | 0x7a8d7b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b1d1e` | Traduit / vérifié | 0x7a8d7f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b1d45` | Traduit / vérifié | 0x7a8d85 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b1d65` | Traduit / vérifié | 0x7aa2b8 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b1d97` | Traduit / vérifié | 0x7aa2bc | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b223d` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b223e, références 0x78c7c1. |
| `0x7b223e` | Traduit / vérifié | 0x78c7c1 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2a11` | Traduit / vérifié | 0x76599f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2a38` | Traduit / vérifié | 0x789327 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2ace` | Traduit / vérifié | 0x7aa95a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2afc` | Traduit / vérifié | 0x7aa95e | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2b02` | Traduit / vérifié | 0x7aa964 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2b33` | Traduit / vérifié | 0x7aa972 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b2b58` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b2b59, références 0x7aa976. |
| `0x7b2cf4` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b2cf5, références 0x7b2cc2. |
| `0x7b2d02` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b2d0d` | Traduit / vérifié | 0x7b2cc8 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3381` | Traduit / vérifié | 0x7b2d45 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b33a1` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b350d` | Traduit / vérifié | 0x7b2d49 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3520` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b3521, références 0x7b2d4f. |
| `0x7b3521` | Traduit / vérifié | 0x7b2d4f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3543` | Traduit / vérifié | 0x7b2d5d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3568` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b3569, références 0x7b2d61. |
| `0x7b3577` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b3581` | Traduit / vérifié | 0x7b2d67 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3595` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b35d6` | Traduit / vérifié | 0x7b35a7 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b35e5` | Traduit / vérifié | 0x7b35ad | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b362c` | Traduit / vérifié | 0x7b360d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3639` | Traduit / vérifié | 0x7b3613 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b365a` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b36a2` | Traduit / vérifié | 0x7b366b, 0x9a534c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b36b5` | Traduit / vérifié | 0x7b3671 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3711` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b371c` | Traduit / vérifié | 0x7b36f0 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3728` | Traduit / vérifié | 0x7b36f6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b37a5` | Traduit / vérifié | 0x7b3762 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3822` | Traduit / vérifié | 0x7b376f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3834` | Traduit / vérifié | 0x7b3775 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b387a` | Traduit / vérifié | 0x7a99bc | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b38cc` | Traduit / vérifié | 0x78c7d3 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3979` | Traduit / vérifié | 0x78c7fa | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b39fa` | Traduit / vérifié | 0x780396 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3a3f` | Traduit / vérifié | 0x78a9a7 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3a8e` | Traduit / vérifié | 0x78a9ab | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3ac9` | Traduit / vérifié | 0x78a9b1 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3b28` | Traduit / vérifié | 0x78bea0 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3b91` | Traduit / vérifié | 0x78bea4 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b3be9` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b3bea, références 0x876b30. |
| `0x7b3c44` | Traduit / vérifié | 0x876b04 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3c6a` | Traduit / vérifié | 0x876b88 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3ccd` | Traduit / vérifié | 0x876bb4 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3d2b` | Traduit / vérifié | 0x876be0 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3d8e` | Traduit / vérifié | 0x876c0c | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3ded` | Traduit / vérifié | 0x876c64 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3e52` | Traduit / vérifié | 0x876c90 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3eb0` | Traduit / vérifié | 0x876cbc | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3f15` | Traduit / vérifié | 0x876e74 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3f80` | Traduit / vérifié | 0x87718c | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b3fe1` | Traduit / vérifié | 0x877318 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b403e` | Traduit / vérifié | 0x87739c | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4097` | Traduit / vérifié | 0x877554 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b40fa` | Traduit / vérifié | 0x8775ac | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4170` | Traduit / vérifié | 0x877604 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b41c1` | Traduit / vérifié | 0x877630 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4225` | Traduit / vérifié | 0x8775d8 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4273` | Traduit / vérifié | 0x878054 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b42d3` | Traduit / vérifié | 0x878080 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4336` | Traduit / vérifié | 0x8780ac | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4395` | Traduit / vérifié | 0x878918 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4406` | Traduit / vérifié | 0x878944 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b4468` | Traduit / vérifié | 0x878970 | Table des objets CFRU : cellule de pointeur fixe, texte relogeable ; aucune extension de cellule. |
| `0x7b44ca` | Traduit / vérifié | 0x78beaa | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b456b` | Traduit / vérifié | 0x761732 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b45a3` | Traduit / vérifié | 0x7a73a8 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b45f9` | Traduit / vérifié | 0x78bc6f, 0x7b4512 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b46b9` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b46ba, références 0x78bc87, 0x7b452a. |
| `0x7b46ba` | Traduit / vérifié | 0x78bc87, 0x7b452a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b46f3` | Traduit / vérifié | 0x794250 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4748` | Traduit / vérifié | 0x79427c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4772` | Traduit / vérifié | 0x7a449f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4787` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b4788, références 0x7b33aa. |
| `0x7b4788` | Traduit / vérifié | 0x7b33aa | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b47c7` | Traduit / vérifié | 0x7b47bf | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b47ec` | Traduit / vérifié | 0x7b47e4 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b484b` | Traduit / vérifié | 0x7b4843 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4882` | Conservé / vérifié | 0x7b4879 | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b489e` | Traduit / vérifié | 0x794289 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b48d5` | Traduit / vérifié | 0x794296 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b491c` | Traduit / vérifié | 0x7b4912 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b496f` | Traduit / vérifié | 0x7b4965 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4997` | Traduit / vérifié | 0x7611b2 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4a3b` | Traduit / vérifié | 0x753881 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4a4e` | Exception | 0xb50347 | Source corrompue : le script pointe au milieu du texte parent, produisant un fragment incomplet. Pas de traduction inventée ni de modification de cette référence. Préimage apparentée : 0x7b4a3b, références 0x753881. |
| `0x7b4aac` | Traduit / vérifié | 0x7a7077 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4ae1` | Traduit / vérifié | 0x7731ee, 0x78195a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b4d79` | Traduit / vérifié | 0x7aa2c2 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b51de` | Traduit / vérifié | 0x78bee0 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5222` | Traduit / vérifié | 0x78bee4 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b524d` | Traduit / vérifié | 0x78beea | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b52a1` | Traduit / vérifié | 0x78c3ef | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b52ec` | Traduit / vérifié | 0x78c3f3 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5303` | Traduit / vérifié | 0x78c3f9 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b533b` | Traduit / vérifié | 0x78c46f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5388` | Traduit / vérifié | 0x78c473 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b53a4` | Traduit / vérifié | 0x78c479 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b53ff` | Traduit / vérifié | 0x78c808 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b543e` | Traduit / vérifié | 0x78c80c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b545d` | Traduit / vérifié | 0x78c812 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b549a` | Traduit / vérifié | 0x78d5bb | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b54d4` | Traduit / vérifié | 0x78d5bf | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b55ca` | Traduit / vérifié | 0x74b16d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5860` | Conservé / vérifié | 0x7b584e | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b5a47` | Traduit / vérifié | 0x7b59ed | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5a8c` | Traduit / vérifié | 0x7b5a3f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5b4b` | Traduit / vérifié | 0x7b5abb | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5bd8` | Traduit / vérifié | 0x7b5ad7 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5c2f` | Traduit / vérifié | 0x7b5b01 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5c7c` | Traduit / vérifié | 0x7b5b0c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5ca4` | Traduit / vérifié | 0x7b5b25 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5ddc` | Traduit / vérifié | 0x7b5b39 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5ea4` | Traduit / vérifié | 0x7b5b43 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5ee6` | Traduit / vérifié | 0x7a6d9b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b5f6e` | Traduit / vérifié | 0x7a6dc2 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b609a` | Traduit / vérifié | 0x7a70bf | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b6105` | Traduit / vérifié | 0x7a70e6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b61bf` | Traduit / vérifié | 0x75b6c8 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b6216` | Traduit / vérifié | 0x78d5c5 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b625a` | Traduit / vérifié | 0x78d60c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b629c` | Traduit / vérifié | 0x78d612 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b62e2` | Traduit / vérifié | 0x78d68c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b632c` | Traduit / vérifié | 0x78d690 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b6357` | Traduit / vérifié | 0x78d696 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b6564` | Traduit / vérifié | 0x78bf43, 0x7b5563, 0x7b5595, 0x7b9492 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b659a` | Traduit / vérifié | 0x78bfdc | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b6c81` | Traduit / vérifié | 0x7b5579, 0x7b55ab, 0x7b65c6, 0x7b94a8 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b6d11` | Traduit / vérifié | 0x7b23fc | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b85b9` | Traduit / vérifié | 0x16d71d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b865e` | Traduit / vérifié | 0x7b8655 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b86b8` | Traduit / vérifié | 0x7b86af | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b870c` | Traduit / vérifié | 0x7611d3, 0x7a799b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8784` | Traduit / vérifié | 0x7b877c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b87ab` | Traduit / vérifié | 0x7b87a3 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b882f` | Conservé / vérifié | 0x7b8827 | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b8864` | Conservé / vérifié | 0x7b885c | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b88a4` | Conservé / vérifié | 0x7b889c | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b88e4` | Conservé / vérifié | 0x7b88dc | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b8908` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b896d` | Traduit / vérifié | 0x7b8966 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8989` | Conservé / vérifié | 0x78c724 | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b89db` | Conservé / vérifié | 0x7b89d3 | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b89fd` | Traduit / vérifié | 0x1a9a1b, 0x1a9a42 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8a54` | Traduit / vérifié | 0x77feff | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8b04` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b8b24` | Traduit / vérifié | 0x7a29d4 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8cff` | Traduit / vérifié | 0x7b8c60 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8d25` | Traduit / vérifié | 0x771bf5 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8e39` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7b8e3a, références 0x7a2a9d. |
| `0x7b8e3a` | Traduit / vérifié | 0x7a2a9d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8edd` | Exception | 0x7a8c9a | Source corrompue : le script pointe au milieu du texte parent, produisant un fragment incomplet. Pas de traduction inventée ni de modification de cette référence. Préimage apparentée : 0x7b8e3a, références 0x7a2a9d. |
| `0x7b8f1b` | Traduit / vérifié | 0x78d729 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8f4a` | Traduit / vérifié | 0x78d72d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b8f88` | Traduit / vérifié | 0x78d733 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b9435` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Aucun propriétaire textuel englobant prouvé ; aucun consommateur direct trouvé. |
| `0x7b97aa` | Conservé / vérifié | 0x744dac, 0x744ddc, 0x753856, 0x79237c, 0x7923aa, 0x7923da, 0x7b9785, 0x7c875b, 0x7d8cee | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7b97c1` | Traduit / vérifié | 0x7a6bec | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b97f1` | Traduit / vérifié | 0x7a6bf0 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b9882` | Traduit / vérifié | 0x78fe75 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b98e5` | Traduit / vérifié | 0x793f2e | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b992b` | Traduit / vérifié | 0x793f32 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b9956` | Traduit / vérifié | 0x793f38 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b998d` | Traduit / vérifié | 0x7a6bf6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b99bb` | Traduit / vérifié | 0x7ac755 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b99e7` | Traduit / vérifié | 0x7ac759 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b99f8` | Traduit / vérifié | 0x7ac75f | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b9a82` | Traduit / vérifié | 0x7b9a5b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b9b3d` | Traduit / vérifié | 0x7b2400 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7b9b5d` | Traduit / vérifié | 0x7b2406 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba1ec` | Traduit / vérifié | 0x7ba1bf | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba26a` | Traduit / vérifié | 0x7ba1e5 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba2cc` | Traduit / vérifié | 0x7ba2b3 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba2e4` | Traduit / vérifié | 0x1a9a1f, 0x1a9a46 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba306` | Traduit / vérifié | 0x7de66d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba36a` | Traduit / vérifié | 0x7de689 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba378` | Conservé / vérifié | 0x770f8e | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7ba408` | Traduit / vérifié | 0x7b897c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba41c` | Traduit / vérifié | 0x7ba415 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba42c` | Traduit / vérifié | 0x78075c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba466` | Traduit / vérifié | 0x7de6a6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba4c4` | Traduit / vérifié | 0x7de6c6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba59f` | Traduit / vérifié | 0x7de76e | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba5b2` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7ba5b3, références 0x7de6ea. |
| `0x7ba5b3` | Traduit / vérifié | 0x7de6ea | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba5bd` | Traduit / vérifié | 0x7de703 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba5d1` | Conservé / vérifié | 0x7de715 | Nom propre, panneau toponymique ou cri conservé selon F-759 ; octets vérifiés. |
| `0x7ba5de` | Traduit / vérifié | 0x7de6d8 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba5f5` | Traduit / vérifié | 0x7b9047 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba63d` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7ba63e, références 0x7de727. |
| `0x7ba63e` | Traduit / vérifié | 0x7de727 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba652` | Traduit / vérifié | 0x7de74a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba66f` | Exception | Aucun | Aucun pointeur 32 bits vers cet offset dans la ROM source ; entrée extraite parasite, non injectée. Préimage apparentée : 0x7ba670, références 0x7de75c. |
| `0x7ba670` | Traduit / vérifié | 0x7de75c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba6d0` | Traduit / vérifié | 0x7de791 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba731` | Traduit / vérifié | 0x7de7a7 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba777` | Traduit / vérifié | 0x7de7c6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba857` | Traduit / vérifié | 0x7ba18c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba8b4` | Traduit / vérifié | 0x771c2d | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba8e6` | Traduit / vérifié | 0x771c43 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7ba91f` | Traduit / vérifié | 0x771c67 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bac0a` | Traduit / vérifié | 0x7b9b2a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bac6b` | Traduit / vérifié | 0x7b46a7 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bace2` | Traduit / vérifié | 0x7b46ab | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bad0b` | Traduit / vérifié | 0x7b46b1 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bad86` | Traduit / vérifié | 0x7b482e | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7badd2` | Traduit / vérifié | 0x7b4832 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7badef` | Traduit / vérifié | 0x7b4838 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bae20` | Traduit / vérifié | 0x7b904b | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bae3e` | Traduit / vérifié | 0x7b9051 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7baee8` | Traduit / vérifié | 0x7bae8a | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7baf13` | Traduit / vérifié | 0x7bae90 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bafb8` | Traduit / vérifié | 0x7baf6c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bafed` | Traduit / vérifié | 0x7baf72 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb0b8` | Traduit / vérifié | 0x7bb05e | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb0d4` | Traduit / vérifié | 0x7bb064 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb173` | Traduit / vérifié | 0x7bb123 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb1b2` | Traduit / vérifié | 0x7bb129 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb2ac` | Traduit / vérifié | 0x7bb1f9 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb316` | Traduit / vérifié | 0x7bb211 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb332` | Traduit / vérifié | 0x7bb21c | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb35f` | Traduit / vérifié | 0x7bb248 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb372` | Traduit / vérifié | 0x7bb289 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb3b9` | Traduit / vérifié | 0x7bb290 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb3ff` | Traduit / vérifié | 0x7bb297 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb55c` | Traduit / vérifié | 0x7bb4a6 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb5c7` | Traduit / vérifié | 0x7bb4fb | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb651` | Traduit / vérifié | 0x7bb614 | Consommateurs référencés : texte complet, commandes et pages source conservées. |
| `0x7bb685` | Traduit / vérifié | 0x7bb61a | Consommateurs référencés : texte complet, commandes et pages source conservées. |

Le patch restaure les copies source des textes du lot avant leur relocation. Cela préserve les suffixes et les références internes hors lot, même après une écriture générique sur place. Tests négatif et ROM finale exigent les préimages intactes, notamment les trois exceptions pointées.
