# PT-23 — Zones de Borrius (F-782)

Périmètre fermé : les 288 offsets explicites de `translation_batches.json`, après
intégration de F-758 et F-759. 262 textes qualifiés, 299 références directes,
26 exceptions sans pointeur direct. Aucune traduction existante supprimée.

Le domaine réel comprend Blizzard City, Tehl Town, Dehara City, Tarmigan Town,
Fallshore City, les itinéraires côtiers, Zygarde, les recherches saisonnières et
les scènes de The Shadows. La comparaison française est conservée à chaque offset
dans `languages/pt/data/pt23_audit.json`, avec l'anglais et la préimage binaire.
Elle sert de contexte ; les noms propres et mouvements suivent F-759.

## Livraison et limites

Le patch `languages/pt/patches/batch_23.py` utilise `StructuredTextPatch` après les
réparations et le repointage générique. Il ne réécrit aucune cellule source : il
alloue un texte complet et modifie uniquement les références auditées. Les tables
de pointeurs sont donc finalisées explicitement, y compris les suffixes vivants ;
aucune entrée ignorée par l'injecteur générique n'est revendiquée comme livrée.
Aucune table de noms à stride fixe n'a été identifiée dans ce lot.

Le contrat conserve exactement FC/FD, leurs arguments, FE/FA/FB et leur ordre.
Les ruptures ne sont pas recalculées. Maximum : 354 octets avec terminateur ;
chaque ligne visible reste dans 192 pixels selon la métrique du moteur partagée.
Les tests ROM vérifient aussi les cinq polices vivantes et une limite de 208 pixels
avec noms développés (10 caractères joueur/rival/espèce, saison Primavera).
Le champ `layout.max_width` mesure les lignes FE du validateur, qui concatène les
segments FA ; `line_widths` et `visible_line_limit` mesurent séparément chaque vraie
ligne FE/FA. Cette distinction conserve le défilement sans modifier le code partagé.

Les quatre fragments débutant par une espace utilisent `expected_raw` en plus de
`expected` (le lecteur historique de protection retire les espaces aux extrémités).
Le test métier vérifie la valeur brute et le test ROM vérifie les octets.
`0x78c45c` porte `9pidimy Town` dans la source vivante ; son nom propre est réparé
en `Epidimy Town`, attesté aux autres occurrences anglaises (notamment `0x7808dd`).

Les exceptions ont zéro référence directe, recherche sur les 32 Mio à tous les
alignements. Les préfixes parasites `9` précédant une cible vivante ne sont pas
injectés. Les copies/fragments autonomes sans consommateur ne sont pas traduits.
Le message Zygarde obsolète `0x7929a3` est remplacé par `0x792af0`, consommé depuis
`0x792740`. Les plages source et les éventuels consommateurs voisins sont consignés
individuellement dans l'audit JSON ; les offsets hors lot restent en lecture seule.

## Recette locale reproductible

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt23.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt23_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt23.config.ts
```

Playwright démarre mGBA avec `QT_QPA_PLATFORM=offscreen`, sans fenêtre ni sauvegarde.
Une copie temporaire de ROM reçoit seulement un script msgbox pointant vers les
consommateurs réels de deux dialogues marins. Les octets construits sont d'abord
comparés aux sources PT, puis les captures du moteur sont reconnues par OCR et
assertées dans Chromium headless. La preuve finale est écrite dans le répertoire
temporaire du système, hors dépôt. Ce contrôle est une sonde native de rendu ;
il ne certifie pas tous les parcours de Borrius ni les branches d'événements.

Validation exécutée : `make build-pt` réussi, 262 textes / 299 références finalisés
(dont 131 textes relocalisés par la passe finale), quatre tests ROM réussis et un
test Playwright réussi sur deux captures natives. Le test vérifie aussi les deux
rangées de pixels du tilde de « lição ». L'OCR Vision confond le O carré avec D et
parfois ç avec g ; ces seules ambiguïtés sont tolérées dans la lecture, tandis que
la comparaison intégrale du texte ROM et le contrôle pixel restent stricts.
TypeScript et Ruff ciblé passent. Hooks actifs : 5 775 tests Python et 71 tests
Vitest réussis, builds FR/IT/DE réussis ; un test Python ignoré par sa configuration
préexistante. Aucun script partagé ni source d'une autre langue modifié.

## Bilan offset par offset

Les références ci-dessous sont les sites source ; les cibles finales sont résolues
et comparées intégralement par le test ROM, sans supposer l'adresse de relocalisation.
Les noms anglais conservés sont des décisions de glossaire, pas des traductions oubliées.

| Offset | Décision | Pointeurs source / justification |
|---|---|---|
| `0x78c364` | Traduit / vérification ROM | `0x78bfa2`, `0x78c01f` |
| `0x78c40f` | Traduit / vérification ROM | `0x78bfa6`, `0x78c023` |
| `0x78c45c` | Traduit / vérification ROM | `0x78c3e0` |
| `0x78c4b3` | Traduit / vérification ROM | `0x78bfbc` |
| `0x78c4f0` | Traduit / vérification ROM | `0x74f8e3` |
| `0x78c62d` | Traduit / vérification ROM | `0x78c554`, `0x78c5b0` |
| `0x78c6c2` | Traduit / vérification ROM | `0x78c431` |
| `0x78c6ec` | Traduit / vérification ROM | `0x78c435` |
| `0x78c6f8` | Traduit / vérification ROM | `0x78c664` |
| `0x78c72c` | Traduit / vérification ROM | `0x78c5fe` |
| `0x78c889` | Traduit / vérification ROM | `0x78bb7c` |
| `0x78ce6a` | Traduit / vérification ROM | `0x778b26` |
| `0x78ced7` | Traduit / vérification ROM | `0x780a47` |
| `0x78d2ba` | Traduit / vérification ROM | `0x794696` |
| `0x78d31b` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x78d322` | Traduit / vérification ROM | `0x166cc7` |
| `0x78d43d` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x78d43e. Consommateurs voisins : 0x78d43e via 0x78a693 |
| `0x78d43e` | Traduit / vérification ROM | `0x78a693` |
| `0x78d4b8` | Traduit / vérification ROM | `0x78a6a6`, `0x78a6cc`, `0x7d058a`, `0x7d2cf5` |
| `0x78d4cd` | Traduit / vérification ROM | `0x7451ab` |
| `0x78d4f0` | Traduit / vérification ROM | `0x7451c8` |
| `0x78d50f` | Traduit / vérification ROM | `0x76d274` |
| `0x78d625` | Traduit / vérification ROM | `0x78d61d` |
| `0x78d662` | Traduit / vérification ROM | `0x78d65a` |
| `0x78d67b` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x78d6a9` | Traduit / vérification ROM | `0x78d6a1` |
| `0x78d6d7` | Traduit / vérification ROM | `0x78d6cf` |
| `0x78d6e6` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x78d6f8` | Traduit / vérification ROM | `0x78d6f0` |
| `0x78d717` | Traduit / vérification ROM | `0x78d70f` |
| `0x78d746` | Traduit / vérification ROM | `0x78d73e` |
| `0x78d764` | Traduit / vérification ROM | `0x78d75c` |
| `0x78d781` | Traduit / vérification ROM | `0x78d779` |
| `0x78d78d` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x78d7a6` | Traduit / vérification ROM | `0x78d79e` |
| `0x78d7ae` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x78d7c8` | Traduit / vérification ROM | `0x78d7c0` |
| `0x78d7ec` | Traduit / vérification ROM | `0x78d7e4` |
| `0x78d7f8` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x78d811` | Traduit / vérification ROM | `0x78d809` |
| `0x78d829` | Traduit / vérification ROM | `0x78d821` |
| `0x78d83d` | Traduit / vérification ROM | `0x78d835` |
| `0x78d851` | Traduit / vérification ROM | `0x78d849` |
| `0x78d86b` | Traduit / vérification ROM | `0x78d863` |
| `0x78d87f` | Traduit / vérification ROM | `0x78d877` |
| `0x78d889` | Traduit / vérification ROM | `0x78a8c5` |
| `0x78d90c` | Traduit / vérification ROM | `0x78a915` |
| `0x78d961` | Traduit / vérification ROM | `0x78dcca` |
| `0x78d96c` | Traduit / vérification ROM | `0x776aba` |
| `0x78d982` | Traduit / vérification ROM | `0x78dcdd` |
| `0x78d9c9` | Traduit / vérification ROM | `0x776ad7`, `0x77f58a`, `0x77f5da` |
| `0x78d9f4` | Traduit / vérification ROM | `0x77f64e`, `0x78a36b`, `0x78a3d0` |
| `0x78da32` | Traduit / vérification ROM | `0x78a43a`, `0x78a8a1`, `0x78a8f7` |
| `0x78da63` | Traduit / vérification ROM | `0x78a448`, `0x78a8af`, `0x78a905` |
| `0x78da85` | Traduit / vérification ROM | `0x77f5f0` |
| `0x78da8e` | Traduit / vérification ROM | `0x78a3e6` |
| `0x78da92` | Traduit / vérification ROM | `0x75ba71` |
| `0x78db0b` | Traduit / vérification ROM | `0x75ba93` |
| `0x78db32` | Traduit / vérification ROM | `0x74ed55` |
| `0x78dc12` | Traduit / vérification ROM | `0x78dcf8` |
| `0x78dc1a` | Traduit / vérification ROM | `0x7884b7`, `0x820b52` |
| `0x78dc2b` | Traduit / vérification ROM | `0x78dd1b`, `0x78dd52` |
| `0x78dc41` | Traduit / vérification ROM | `0x78dd81` |
| `0x78df49` | Traduit / vérification ROM | `0x78a1cd` |
| `0x78e02a` | Traduit / vérification ROM | `0x78a1fe` |
| `0x78e068` | Traduit / vérification ROM | `0x78a225` |
| `0x78e0c6` | Traduit / vérification ROM | `0x78a465` |
| `0x78e11a` | Traduit / vérification ROM | `0x7764a7` |
| `0x78e1c9` | Traduit / vérification ROM | `0x7764b3` |
| `0x78e287` | Traduit / vérification ROM | `0x7764c7` |
| `0x78e3d1` | Traduit / vérification ROM | `0x765572` |
| `0x78e468` | Traduit / vérification ROM | `0x765599` |
| `0x78e5dd` | Traduit / vérification ROM | `0x772db9` |
| `0x78e656` | Traduit / vérification ROM | `0x772de0` |
| `0x78e772` | Traduit / vérification ROM | `0x78e76a` |
| `0x78e789` | Traduit / vérification ROM | `0x78e704` |
| `0x78e7ac` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x78e7ad. Consommateurs voisins : 0x78e7ad via 0x78c5c6 |
| `0x78e7ad` | Traduit / vérification ROM | `0x78c5c6` |
| `0x78e7ba` | Traduit / vérification ROM | `0x78c6e4` |
| `0x78e7d3` | Traduit / vérification ROM | `0x78e757` |
| `0x78e984` | Traduit / vérification ROM | `0x78e816` |
| `0x78ea3a` | Traduit / vérification ROM | `0x78e82d` |
| `0x78ea78` | Traduit / vérification ROM | `0x78e854` |
| `0x78ead3` | Traduit / vérification ROM | `0x78e85f` |
| `0x78eafe` | Traduit / vérification ROM | `0x78e878` |
| `0x78eb95` | Traduit / vérification ROM | `0x78e88c` |
| `0x78ebd5` | Traduit / vérification ROM | `0x78e97c` |
| `0x78ec48` | Traduit / vérification ROM | `0x78e896` |
| `0x78ec4e` | Traduit / vérification ROM | `0x78e89d` |
| `0x78ec5d` | Traduit / vérification ROM | `0x75b6d7` |
| `0x78ed07` | Traduit / vérification ROM | `0x78c558`, `0x78c5b4` |
| `0x78f4de` | Traduit / vérification ROM | `0x750ff2` |
| `0x78f562` | Traduit / vérification ROM | `0x752041` |
| `0x78f5da` | Traduit / vérification ROM | `0x752833` |
| `0x78f61d` | Traduit / vérification ROM | `0x776036` |
| `0x78f7f2` | Traduit / vérification ROM | `0x772f50` |
| `0x78f87d` | Traduit / vérification ROM | `0x772f6c` |
| `0x78f9f2` | Traduit / vérification ROM | `0x78f98b` |
| `0x78fa39` | Traduit / vérification ROM | `0x77603a` |
| `0x78fa4a` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x78fa4b. Consommateurs voisins : 0x78fa4b via 0x745a14 |
| `0x78fa4b` | Traduit / vérification ROM | `0x745a14` |
| `0x78fbe3` | Traduit / vérification ROM | `0x745a1d` |
| `0x78fc07` | Traduit / vérification ROM | `0x78a6b9` |
| `0x78fd1d` | Traduit / vérification ROM | `0x78a6df` |
| `0x78fd42` | Traduit / vérification ROM | `0x750d51` |
| `0x78fe26` | Traduit / vérification ROM | `0x76d1c7` |
| `0x78fe3b` | Traduit / vérification ROM | `0x76d1fd` |
| `0x7916c1` | Traduit / vérification ROM | `0x781910` |
| `0x7917e7` | Traduit / vérification ROM | `0x166d17` |
| `0x7918d7` | Traduit / vérification ROM | `0x781086` |
| `0x791982` | Traduit / vérification ROM | `0x7814f3` |
| `0x791ad7` | Traduit / vérification ROM | `0x78d290` |
| `0x791b8b` | Traduit / vérification ROM | `0x791b6f`, `0x1eb08fb` |
| `0x791bba` | Traduit / vérification ROM | `0x791b82`, `0x1eb090f` |
| `0x791c3d` | Traduit / vérification ROM | `0x791bed` |
| `0x791c58` | Traduit / vérification ROM | `0x791c20` |
| `0x791db3` | Traduit / vérification ROM | `0x791ce8` |
| `0x791e5d` | Traduit / vérification ROM | `0x791d02` |
| `0x791f17` | Traduit / vérification ROM | `0x791d1c` |
| `0x792026` | Traduit / vérification ROM | `0x791d36` |
| `0x7920a9` | Traduit / vérification ROM | `0x791d9d` |
| `0x7920ea` | Traduit / vérification ROM | `0x791d5a` |
| `0x79223b` | Traduit / vérification ROM | `0x16a99c` |
| `0x7922d1` | Traduit / vérification ROM | `0x762a1e` |
| `0x792367` | Traduit / vérification ROM | `0x78fe6b` |
| `0x7924a2` | Traduit / vérification ROM | `0x792472` |
| `0x792504` | Traduit / vérification ROM | `0x79247c` |
| `0x79255c` | Traduit / vérification ROM | `0x792486` |
| `0x7925db` | Traduit / vérification ROM | `0x792490` |
| `0x792666` | Traduit / vérification ROM | `0x79249a` |
| `0x7927c1` | Traduit / vérification ROM | `0x792709` |
| `0x79283d` | Traduit / vérification ROM | `0x792717` |
| `0x79288d` | Traduit / vérification ROM | `0x79272a` |
| `0x792934` | Traduit / vérification ROM | `0x792768` |
| `0x7929a3` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Ancien message de réception Zygarde, remplacé par 0x792af0 (pointeur 0x792740). |
| `0x7929cd` | Traduit / vérification ROM | `0x792752` |
| `0x792a1d` | Traduit / vérification ROM | `0x79274a` |
| `0x792af0` | Traduit / vérification ROM | `0x792740` |
| `0x792c41` | Traduit / vérification ROM | `0x764e48` |
| `0x792c8b` | Traduit / vérification ROM | `0x792342`, `0x79241d` |
| `0x792d31` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x792d32. Consommateurs voisins : 0x792d32 via 0x792346,0x792421 |
| `0x792dff` | Traduit / vérification ROM | `0x792d51` |
| `0x792e51` | Traduit / vérification ROM | `0x79277c` |
| `0x792ec1` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x792ec9` | Traduit / vérification ROM | `0x7927aa` |
| `0x792f62` | Traduit / vérification ROM | `0x78fe6f` |
| `0x793779` | Traduit / vérification ROM | `0x771f23` |
| `0x79379e` | Traduit / vérification ROM | `0x78e3a6` |
| `0x7937b8` | Traduit / vérification ROM | `0x78e3b0` |
| `0x7937fa` | Traduit / vérification ROM | `0x78a13e` |
| `0x7938ed` | Traduit / vérification ROM | `0x78a160` |
| `0x79397a` | Traduit / vérification ROM | `0x78a16a` |
| `0x7939bc` | Traduit / vérification ROM | `0x78acc0` |
| `0x793a06` | Traduit / vérification ROM | `0x78ad03` |
| `0x793a67` | Traduit / vérification ROM | `0x78acd9` |
| `0x793aa1` | Traduit / vérification ROM | `0x78acf9` |
| `0x793b0c` | Traduit / vérification ROM | `0x78bc31` |
| `0x793c67` | Traduit / vérification ROM | `0x78bc52` |
| `0x793d11` | Traduit / vérification ROM | `0x78a15a`, `0x78a178` |
| `0x793d18` | Traduit / vérification ROM | `0x78a17e`, `0x78a192`, `0x79407d`, `0x7941d7` |
| `0x793d1f` | Traduit / vérification ROM | `0x78a198`, `0x78a1ac` |
| `0x793d26` | Traduit / vérification ROM | `0x78a1b2`, `0x78a477` |
| `0x793d32` | Traduit / vérification ROM | `0x78f998` |
| `0x793d6c` | Traduit / vérification ROM | `0x78f9af` |
| `0x793d9f` | Traduit / vérification ROM | `0x78f9e0` |
| `0x793de3` | Traduit / vérification ROM | `0x76d210` |
| `0x793edd` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x793ede. Consommateurs voisins : 0x793ede via 0x781067 |
| `0x793ede` | Traduit / vérification ROM | `0x781067` |
| `0x793ee8` | Traduit / vérification ROM | `0x76d22a` |
| `0x793f44` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x793f45. Consommateurs voisins : 0x793f45 via 0x7941a1 |
| `0x793f45` | Traduit / vérification ROM | `0x7941a1` |
| `0x793f7c` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x793f7d. Consommateurs voisins : 0x793f7d via 0x7941b6 |
| `0x793f8e` | Traduit / vérification ROM | `0x763972`, `0x76d288`, `0x79408c`, `0x7941e6` |
| `0x793fcb` | Traduit / vérification ROM | `0x76d292`, `0x7d98bf` |
| `0x793fcf` | Traduit / vérification ROM | `0x76d299`, `0x7d98cc` |
| `0x794343` | Traduit / vérification ROM | `0x7930c6` |
| `0x7944a4` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x7944bd` | Traduit / vérification ROM | `0x7930ce` |
| `0x7944d4` | Traduit / vérification ROM | `0x7930ef` |
| `0x7946d0` | Traduit / vérification ROM | `0x78c710` |
| `0x7963e9` | Traduit / vérification ROM | `0x770b17` |
| `0x796410` | Traduit / vérification ROM | `0x78c83b` |
| `0x796c75` | Traduit / vérification ROM | `0x772855`, `0x7aa84a` |
| `0x796ccf` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x7a2565` | Traduit / vérification ROM | `0x77ff4a` |
| `0x7a257f` | Traduit / vérification ROM | `0x7a2575` |
| `0x7a25ce` | Traduit / vérification ROM | `0x7a25bc` |
| `0x7a2622` | Traduit / vérification ROM | `0x7a2610` |
| `0x7a2766` | Traduit / vérification ROM | `0x7a2754` |
| `0x7a281f` | Traduit / vérification ROM | `0x770f49`, `0x7738dc`, `0x78beb6` |
| `0x7a2894` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x7a289c` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x7a28be` | Traduit / vérification ROM | `0x7a28b5` |
| `0x7a28d3` | Traduit / vérification ROM | `0x7a28ca` |
| `0x7a28f4` | Traduit / vérification ROM | `0x7a28eb` |
| `0x7a290c` | Traduit / vérification ROM | `0x7a2903` |
| `0x7a2926` | Traduit / vérification ROM | `0x7a2913` |
| `0x7a29f4` | Traduit / vérification ROM | `0x7a29eb` |
| `0x7a2aa7` | Traduit / vérification ROM | `0x79235c` |
| `0x7a3294` | Traduit / vérification ROM | `0x7937da` |
| `0x7a32b3` | Traduit / vérification ROM | `0x7937de` |
| `0x7a32c8` | Traduit / vérification ROM | `0x7937e4` |
| `0x7a3316` | Traduit / vérification ROM | `0x7a32f6` |
| `0x7a3326` | Traduit / vérification ROM | `0x7a32fc` |
| `0x7a3344` | Traduit / vérification ROM | `0x752331` |
| `0x7a3406` | Traduit / vérification ROM | `0x773810` |
| `0x7a34c5` | Traduit / vérification ROM | `0x77382f` |
| `0x7a352b` | Traduit / vérification ROM | `0x16effd` |
| `0x7a358f` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. |
| `0x7a35fc` | Traduit / vérification ROM | `0x7738c7` |
| `0x7a36ca` | Traduit / vérification ROM | `0x16eb42` |
| `0x7a3bdd` | Traduit / vérification ROM | `0x7ba7fb` |
| `0x7a3cf0` | Traduit / vérification ROM | `0x76290b`, `0x773842` |
| `0x7a3d04` | Traduit / vérification ROM | `0x7884c4` |
| `0x7a3d5d` | Traduit / vérification ROM | `0x7a3f10` |
| `0x7a3d66` | Traduit / vérification ROM | `0x7884d1` |
| `0x7a3d7e` | Traduit / vérification ROM | `0x773850` |
| `0x7a3d98` | Traduit / vérification ROM | `0x7a3f26` |
| `0x7a3dc5` | Traduit / vérification ROM | `0x7ba87f` |
| `0x7a3dfe` | Traduit / vérification ROM | `0x7a3f41` |
| `0x7a3f71` | Traduit / vérification ROM | `0x75389a` |
| `0x7a3fa7` | Traduit / vérification ROM | `0x7538a3` |
| `0x7a3fd3` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x7a3fd4. Consommateurs voisins : 0x7a3fd4 via 0x77275e, 0x7a3fe9 via 0x1e41b2d, 0x7a4018 via 0x909b1d |
| `0x7a3fd4` | Traduit / vérification ROM | `0x77275e` |
| `0x7a401f` | Traduit / vérification ROM | `0x78c0e4`, `0x78c238` |
| `0x7a4072` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x7a4073. Consommateurs voisins : 0x7a4073 via 0x744a6d, 0x7a40a8 via 0xb6d5f |
| `0x7a4073` | Traduit / vérification ROM | `0x744a6d` |
| `0x7a40f8` | Traduit / vérification ROM | `0x77277a` |
| `0x7a4133` | Traduit / vérification ROM | `0x772787` |
| `0x7a4188` | Traduit / vérification ROM | `0x7f0676` |
| `0x7a41cf` | Traduit / vérification ROM | `0x78bef6` |
| `0x7a41de` | Traduit / vérification ROM | `0x7727a3` |
| `0x7a4229` | Traduit / vérification ROM | `0x7727a7` |
| `0x7a4254` | Traduit / vérification ROM | `0x7727ad` |
| `0x7a42ae` | Traduit / vérification ROM | `0x7a4289` |
| `0x7a42c2` | Traduit / vérification ROM | `0x7a428f` |
| `0x7a4343` | Traduit / vérification ROM | `0x7a42f4` |
| `0x7a4365` | Traduit / vérification ROM | `0x7a42fa` |
| `0x7a4390` | Traduit / vérification ROM | `0x16b254` |
| `0x7a44d9` | Traduit / vérification ROM | `0x7a4429` |
| `0x7a5a40` | Traduit / vérification ROM | `0x7a59da` |
| `0x7a5a7d` | Traduit / vérification ROM | `0x7a59e6` |
| `0x7a6a12` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x7a6a13. Consommateurs voisins : 0x7a6a13 via 0x78e557 |
| `0x7a6a13` | Traduit / vérification ROM | `0x78e557` |
| `0x7a6b49` | Traduit / vérification ROM | `0x762ba5` |
| `0x7a6bb4` | Traduit / vérification ROM | `0x781706` |
| `0x7a6c49` | Traduit / vérification ROM | `0x78c43b` |
| `0x7a6d09` | Traduit / vérification ROM | `0x79325c` |
| `0x7a6d46` | Traduit / vérification ROM | `0x793266` |
| `0x7a6eed` | Traduit / vérification ROM | `0x78170a` |
| `0x7a6f09` | Traduit / vérification ROM | `0x7a4451` |
| `0x7a70f2` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x7a70f3. Consommateurs voisins : 0x7a70f3 via 0x793248 |
| `0x7a70f3` | Traduit / vérification ROM | `0x793248` |
| `0x7a712a` | Traduit / vérification ROM | `0x7a6cc7` |
| `0x7a7158` | Traduit / vérification ROM | `0x7a6ccb` |
| `0x7a7308` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x7a7309. Consommateurs voisins : 0x7a7309 via 0x7a6cd1 |
| `0x7a7309` | Traduit / vérification ROM | `0x7a6cd1` |
| `0x7a7336` | Traduit / vérification ROM | `0x7a72b3` |
| `0x7a7357` | Traduit / vérification ROM | `0x7a72b7` |
| `0x7a736d` | Traduit / vérification ROM | `0x7a72bd` |
| `0x7a753b` | Traduit / vérification ROM | `0x7a74e3` |
| `0x7a754d` | Traduit / vérification ROM | `0x7a74e9` |
| `0x7a7702` | Traduit / vérification ROM | `0x78c0e8`, `0x78c23c` |
| `0x7a78e5` | Traduit / vérification ROM | `0x74f855` |
| `0x7a7d18` | Traduit / vérification ROM | `0x7a7c4e` |
| `0x7a7df3` | Traduit / vérification ROM | `0x7a7c60` |
| `0x7a7e6a` | Exception | 0 référence ; Aucun pointeur direct dans les 32 Mio source (recherche sur tous les alignements). Fragment ou copie morte ; aucune injection pour ne pas corrompre une cellule voisine. Préfixe parasite 9 avant la cible vivante 0x7a7e6b. Consommateurs voisins : 0x7a7e6b via 0x7aa97c |
| `0x7a7e6b` | Traduit / vérification ROM | `0x7aa97c` |
| `0x7a7ed5` | Traduit / vérification ROM | `0x7a7c72` |
| `0x7a8053` | Traduit / vérification ROM | `0x7a7f74` |
| `0x7a805e` | Traduit / vérification ROM | `0x7a7fb9` |
| `0x7a80b1` | Traduit / vérification ROM | `0x7a7fcf` |
| `0x7a8133` | Traduit / vérification ROM | `0x7a7ff0` |
| `0x7a81da` | Traduit / vérification ROM | `0x78e57f` |
| `0x7a823b` | Traduit / vérification ROM | `0x76510d` |
| `0x7a8491` | Traduit / vérification ROM | `0x7a7c84` |
| `0x7a84b5` | Traduit / vérification ROM | `0x7a7c93` |
| `0x7a84d9` | Traduit / vérification ROM | `0x7a7ca0` |
| `0x7a84e6` | Traduit / vérification ROM | `0x7a7cbe` |
| `0x7a8589` | Traduit / vérification ROM | `0x7a4472` |
| `0x7a86ee` | Traduit / vérification ROM | `0x7a6fac` |
| `0x7a87b1` | Traduit / vérification ROM | `0x7a82c2` |
| `0x7a8951` | Traduit / vérification ROM | `0x78ce59` |
| `0x7a8971` | Traduit / vérification ROM | `0x78ce5d` |
| `0x7a89de` | Traduit / vérification ROM | `0x762bf9` |
| `0x7a89e3` | Traduit / vérification ROM | `0x762bf2` |
| `0x7a89ea` | Traduit / vérification ROM | `0x762bff` |
| `0x7a8ca4` | Traduit / vérification ROM | `0x78d608` |
