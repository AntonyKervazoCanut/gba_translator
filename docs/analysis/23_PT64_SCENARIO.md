# PT-64 — Fallshore City et scénario étendu (F-823)

## Périmètre et méthode

Les 300 clés du manifeste PT-64 font autorité. F-758 et F-759 sont intégrés.
292 textes traduits, 8 noms propres/cri conservés ; aucune exception sans lecteur.
Aucun offset hors lot ni aucune traduction préexistante ne sont modifiés.
L’anglais de `languages/en/combined_en.txt` et le français au même offset sont
consignés avec l’anglais intégral lu dans la ROM, dans `languages/pt/data/pt64_audit.json`.
Les extraits plafonnés des dialogues 0x1f06c7f et 0x1f0be99 ne suffisent pas :
leurs fins sont traduites depuis les octets complets, terminateur compris.

## Livraison et budgets

Le finaliseur `batch_64` réutilise `BorriusTextPatch` après les réparations et la
police. Il vérifie les préimages, chaque pointeur source, les commandes et les
budgets avant toute écriture. Relocalisation atomique, idempotente, sans réécriture
des voisins. Les tables d’évolution 0x1fb5e70–0x1fb5f0b et les tables du guide sont
des tables de pointeurs : leurs cellules restent en place, seuls les pointeurs
sont actualisés. La note d’Œuf est référencée à 0x463edc. Aucune cellule texte brute
à pas fixe nécessitant un autre patch n’a été identifiée dans ce lot.

Les commandes FC/FD/F8 et leurs paramètres, pages FB et défilements FA conservent
leur ordre exact. Les FE sont adaptés au portugais ; les descriptions de missions
ont au plus trois lignes de 172 px. La lettre 0x1f0c2cc conserve ses lignes vides.
Le budget dialogue est 208 px. Les cinq tables de largeurs réelles sont mesurées
avec les tildes PT, les noms de dix W, les compteurs, dates, objets et suffixes
explicités par entrée dans l’audit. Les estimations statiques de 54 px par FD
surestiment notamment les chiffres et les suffixes ; `max_width` contient ce
plafond estimé, distinct du vrai `pixel_budget` vérifié dans les cinq polices.
Les mots terminés par FD07/FD08 utilisent des pluriels en s (uso, compra, objeto,
Ponto), jamais vez+s. Les noms d’objets, mouvements et lieux sans équivalent
attesté restent anglais selon F-759. Les conditions d’évolution (statistiques,
genre, horaire, météo hors combat, objet tenu) et seuils des missions sont testés.

## Validation reproductible

- `python3 -m pytest tests/unit/pt/test_batch_pt64.py tests/unit/test_translation_integrity.py -q`
- `make build-pt`
- `python3 -m pytest tests/e2e/pt/test_batch_pt64_rom.py -m rom -q`
- `npx playwright test --config tests/e2e-playwright/playwright.pt64.config.ts`

Le test Playwright lance mGBA hors écran sur une copie temporaire de la ROM finale,
suit deux pointeurs audités, invoque le msgbox natif, puis vérifie les deux premières
lignes par OCR avant capture (mots normalisés sans accents ni ponctuation ;
valeurs exactes contrôlées en binaire). Le compteur FD02 est initialisé comme
dans le script de mission, car le moteur développe toutes les pages à l’ouverture. Il n’altère ni les glyphes ni les textes. Il ne
prétend pas parcourir naturellement les 300 scènes. Toutes les chaînes complètes
et tous leurs lecteurs sont contrôlés en binaire dans la ROM finale. Les captures
restent dans le répertoire temporaire système et sont jointes au ticket.

Validation de reprise : build PT réussi ; 37 tests ciblés (intégrité, domaine,
pointeurs et budgets des cinq polices) réussis, aucun skip. Lint Python ciblé
et `npx tsc --noEmit` réussis. Playwright : 1 test réussi, deux dialogues
affichés, sauvegarde temporaire inchangée et capture jointe au ticket.
Aucun code partagé modifié.

## Bilan par offset

Les références ci-dessous sont les emplacements ROM des pointeurs, pas les cibles
après relocalisation. Le JSON précise préimage, sources EN/FR, valeur PT exacte,
octets encodés et largeurs développées dans les cinq polices.

| Offset | Décision | Scène | Pointeurs source | Octets PT | Pixels max / budget |
|---|---|---|---|---:|---:|
| `0x1f052dc` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a671 | 159 | 174 / 208 |
| `0x1f05393` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a690 | 63 | 148 / 208 |
| `0x1f053d0` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6a9, 0x1e7b39c, 0x1e7b415, 0x1e7b482 | 41 | 149 / 208 |
| `0x1f05401` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6b6 | 83 | 140 / 208 |
| `0x1f05459` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6c3 | 77 | 172 / 208 |
| `0x1f054b3` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6d0 | 60 | 173 / 208 |
| `0x1f054ee` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x463edc | 46 | 132 / 208 |
| `0x1f05515` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6de | 140 | 191 / 208 |
| `0x1f055ad` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6ec | 296 | 184 / 208 |
| `0x1f056c9` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a6f6 | 76 | 109 / 208 |
| `0x1f0572f` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a704 | 74 | 180 / 208 |
| `0x1f05779` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a712 | 110 | 174 / 208 |
| `0x1f057f0` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a729 | 186 | 154 / 208 |
| `0x1f058bd` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a74b | 84 | 170 / 208 |
| `0x1f0591e` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a914 | 439 | 178 / 208 |
| `0x1f05afd` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a927 | 16 | 87 / 208 |
| `0x1f05b12` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a95c | 96 | 188 / 208 |
| `0x1f05b72` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a97e | 285 | 182 / 208 |
| `0x1f05cad` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a98b | 48 | 149 / 208 |
| `0x1f05cf2` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a998 | 97 | 190 / 208 |
| `0x1f05d58` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a9a5 | 107 | 151 / 208 |
| `0x1f05dd1` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a759 | 174 | 183 / 208 |
| `0x1f05e90` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a87f | 36 | 142 / 208 |
| `0x1f05eb5` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a8c4 | 77 | 144 / 208 |
| `0x1f05f04` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a8e7 | 62 | 177 / 208 |
| `0x1f05f4d` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a8f4 | 31 | 142 / 208 |
| `0x1f05f6d` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a901 | 55 | 147 / 208 |
| `0x1f05fa4` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a767 | 118 | 139 / 208 |
| `0x1f06025` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a840 | 57 | 159 / 208 |
| `0x1f06062` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a77a | 31 | 104 / 208 |
| `0x1f0608b` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a849 | 22 | 63 / 208 |
| `0x1f060a3` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a856 | 18 | 75 / 208 |
| `0x1f060b7` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a7d7 | 106 | 168 / 208 |
| `0x1f06137` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a7e5 | 19 | 99 / 208 |
| `0x1f06153` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a863 | 62 | 158 / 208 |
| `0x1f0618a` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1e6a837 | 21 | 142 / 208 |
| `0x1f061a0` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e7c, 0x1fb5e98, 0x1fb5e9c, 0x1fb5ea0, 0x1fb5ee8, 0x1fb5eec | 19 | 114 / 208 |
| `0x1f061b6` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e8c | 47 | 138 / 208 |
| `0x1f061f8` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e90 | 45 | 132 / 208 |
| `0x1f06231` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e94 | 47 | 139 / 208 |
| `0x1f06270` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ea4 | 56 | 162 / 208 |
| `0x1f062b0` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ebc | 31 | 142 / 208 |
| `0x1f062d4` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ec0 | 31 | 142 / 208 |
| `0x1f062fa` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ec4 | 27 | 158 / 208 |
| `0x1f06319` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ec8 | 33 | 153 / 208 |
| `0x1f0633e` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e70 | 112 | 158 / 208 |
| `0x1f063b9` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e74 | 126 | 158 / 208 |
| `0x1f06443` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e78 | 120 | 158 / 208 |
| `0x1f064c7` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5eb0 | 139 | 178 / 208 |
| `0x1f0655b` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e80 | 13 | 69 / 208 |
| `0x1f06568` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e84 | 26 | 120 / 208 |
| `0x1f0658a` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5e88 | 14 | 148 / 208 |
| `0x1f065a0` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ea8 | 41 | 167 / 208 |
| `0x1f065cb` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5eac | 56 | 189 / 208 |
| `0x1f0660e` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5eb4 | 52 | 179 / 208 |
| `0x1f06649` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5eb8 | 22 | 185 / 208 |
| `0x1f0665d` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ecc | 37 | 149 / 208 |
| `0x1f06689` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ed0 | 36 | 149 / 208 |
| `0x1f066bb` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ed4 | 30 | 143 / 208 |
| `0x1f066da` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ed8 | 33 | 176 / 208 |
| `0x1f06702` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5edc | 33 | 141 / 208 |
| `0x1f0672a` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ee4 | 43 | 140 / 208 |
| `0x1f06757` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ef0 | 25 | 125 / 208 |
| `0x1f06771` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ef4 | 28 | 187 / 208 |
| `0x1f0679c` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5ef8 | 32 | 149 / 208 |
| `0x1f067c7` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5efc | 27 | 149 / 208 |
| `0x1f067f2` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5f08 | 22 | 142 / 208 |
| `0x1f06811` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5f00 | 44 | 160 / 208 |
| `0x1f0683c` | traduit / vérifié en ROM | Evolution House : méthodes d’évolution | 0x1fb5f04 | 44 | 159 / 208 |
| `0x1f06869` | traduit / vérifié en ROM | Fallshore City : œuf, Mel et Evolution House | 0x1ecc280 | 22 | 119 / 208 |
| `0x1f06885` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6a9e7 | 192 | 172 / 208 |
| `0x1f0694f` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aa79 | 214 | 172 / 208 |
| `0x1f06a4c` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aa8a | 40 | 134 / 208 |
| `0x1f06a77` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1d77c2f, 0x1e6aa8e | 6 | 28 / 208 |
| `0x1f06a82` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aaa1 | 21 | 119 / 208 |
| `0x1f06a9d` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aaa5 | 17 | 92 / 208 |
| `0x1f06aa6` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aab8 | 33 | 178 / 208 |
| `0x1f06ac3` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aabc | 27 | 147 / 208 |
| `0x1f06ad9` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aacf | 27 | 148 / 208 |
| `0x1f06af1` | traduit / vérifié en ROM | Fallshore City : Inverse Battle House | 0x1e6aad3 | 31 | 174 / 208 |
| `0x1f06b10` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6afb4, 0x1e6afe8, 0x1e6b058 | 18 | 96 / 208 |
| `0x1f06b1d` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6afcc | 73 | 170 / 172 |
| `0x1f06b65` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ac93 | 112 | 164 / 208 |
| `0x1f06bd9` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6acc6 | 88 | 160 / 208 |
| `0x1f06c38` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6aca6 | 61 | 152 / 208 |
| `0x1f06c7f` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6acb1 | 658 | 190 / 208 |
| `0x1f06f5c` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6af93 | 101 | 160 / 208 |
| `0x1f06fc6` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ac31, 0x1e6ad00, 0x1e6ad32, 0x1e6ad83, 0x1e6ae82, 0x1e6aeb1, 0x1e6af33, 0x1e6af66 | 83 | 139 / 208 |
| `0x1f07015` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ae63 | 108 | 168 / 208 |
| `0x1f07090` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ac86 | 113 | 187 / 208 |
| `0x1f07111` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ae2f | 52 | 144 / 208 |
| `0x1f0714f` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6afdb | 207 | 177 / 208 |
| `0x1f07244` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b028 | 86 | 162 / 208 |
| `0x1f0729e` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b04b | 143 | 176 / 208 |
| `0x1f0734a` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ad2c | 11 | 59 / 208 |
| `0x1f07353` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ac2b, 0x1e6acdf | 27 | 148 / 208 |
| `0x1f07367` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ad72 | 16 | 86 / 208 |
| `0x1f07376` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ae7c, 0x1e6b092 | 14 | 71 / 208 |
| `0x1f07382` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6aeab, 0x1e6b086 | 14 | 71 / 208 |
| `0x1f0738e` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6af2d | 15 | 80 / 208 |
| `0x1f0739c` | conservé / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6af60 | 15 | 80 / 208 |
| `0x1f073ab` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b0a8, 0x1e6b142, 0x1e6b1ff, 0x1e6b24d | 13 | 68 / 208 |
| `0x1f073b6` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b0b8 | 76 | 142 / 172 |
| `0x1f07406` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b0bc | 65 | 142 / 172 |
| `0x1f0744b` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b0c0 | 66 | 142 / 172 |
| `0x1f07491` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b0c4 | 64 | 142 / 172 |
| `0x1f074d5` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b0c8 | 79 | 148 / 172 |
| `0x1f07524` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b11e | 175 | 190 / 208 |
| `0x1f075cb` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b135 | 62 | 163 / 208 |
| `0x1f07615` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b152 | 10 | 52 / 208 |
| `0x1f07621` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b1c0 | 60 | 119 / 208 |
| `0x1f0765b` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b1dc | 26 | 137 / 208 |
| `0x1f0767d` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b21c | 67 | 167 / 208 |
| `0x1f076b9` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b20f | 95 | 164 / 208 |
| `0x1f0771d` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b1f7 | 95 | 164 / 208 |
| `0x1f07781` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b229 | 119 | 161 / 208 |
| `0x1f077fa` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b111 | 58 | 160 / 208 |
| `0x1f0784d` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b25c, 0x1e6b2bb, 0x1e6b37f | 18 | 95 / 208 |
| `0x1f07861` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b268 | 83 | 158 / 172 |
| `0x1f078cb` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b28e | 96 | 190 / 208 |
| `0x1f07929` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b29b | 117 | 148 / 208 |
| `0x1f079b1` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b2ae | 200 | 161 / 208 |
| `0x1f07a82` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b2cb | 45 | 126 / 208 |
| `0x1f07ab1` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b2d8 | 49 | 121 / 208 |
| `0x1f07ae2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b31a | 99 | 147 / 208 |
| `0x1f07b4f` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b331 | 28 | 119 / 208 |
| `0x1f07b70` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b339 | 87 | 191 / 208 |
| `0x1f07bc4` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b344 | 86 | 170 / 208 |
| `0x1f07c20` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b372, 0x1e6b38f | 123 | 165 / 208 |
| `0x1f07cad` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b39c | 72 | 180 / 208 |
| `0x1f07d00` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b3a9 | 115 | 180 / 208 |
| `0x1f07d7b` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b3b6 | 145 | 180 / 208 |
| `0x1f07e1e` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b3c3 | 63 | 163 / 208 |
| `0x1f07e65` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b3d0, 0x1e6b42e, 0x1e6b487 | 22 | 120 / 208 |
| `0x1f07e7e` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b3e8 | 74 | 159 / 172 |
| `0x1f07ec2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b40e | 320 | 190 / 208 |
| `0x1f08005` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b421 | 150 | 184 / 208 |
| `0x1f080a8` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b4d1 | 56 | 161 / 208 |
| `0x1f080ee` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b4c7 | 125 | 149 / 208 |
| `0x1f08182` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b462 | 179 | 178 / 208 |
| `0x1f08242` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b4db | 61 | 143 / 208 |
| `0x1f08287` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b4e4, 0x1e6b542, 0x1e6b59b | 24 | 129 / 208 |
| `0x1f082a1` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b4fc | 55 | 157 / 172 |
| `0x1f082e2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b522 | 266 | 176 / 208 |
| `0x1f083f2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b535 | 133 | 171 / 208 |
| `0x1f08489` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b5e5 | 49 | 138 / 208 |
| `0x1f084bc` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b5db | 123 | 183 / 208 |
| `0x1f08541` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b576 | 187 | 188 / 208 |
| `0x1f085f2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b5ef | 81 | 186 / 208 |
| `0x1f08646` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b5f8, 0x1e6b656, 0x1e6b6af | 22 | 117 / 208 |
| `0x1f08659` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b610 | 57 | 166 / 172 |
| `0x1f08691` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b636 | 292 | 190 / 208 |
| `0x1f087c3` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b649 | 64 | 150 / 208 |
| `0x1f0880b` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b6ff | 64 | 184 / 208 |
| `0x1f08849` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b6f2 | 159 | 169 / 208 |
| `0x1f08909` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b68d | 228 | 171 / 208 |
| `0x1f08a06` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b6a1 | 59 | 161 / 208 |
| `0x1f08a3f` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b70c | 57 | 160 / 208 |
| `0x1f08a72` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b718, 0x1e6b776, 0x1e6b83d | 16 | 88 / 208 |
| `0x1f08a80` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b730 | 53 | 151 / 172 |
| `0x1f08ac4` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b756 | 285 | 183 / 208 |
| `0x1f08be6` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b769 | 43 | 116 / 208 |
| `0x1f08c1e` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b88d | 72 | 142 / 208 |
| `0x1f08c72` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b880 | 142 | 169 / 208 |
| `0x1f08d0a` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b7ad | 82 | 147 / 208 |
| `0x1f08d69` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b8a7 | 53 | 150 / 208 |
| `0x1f08da1` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b89a | 60 | 173 / 208 |
| `0x1f08de6` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b8b4, 0x1e6b912, 0x1e6b9d3 | 19 | 101 / 208 |
| `0x1f08df7` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b8cc | 52 | 157 / 172 |
| `0x1f08e36` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b8f2 | 245 | 179 / 208 |
| `0x1f08f28` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b905 | 89 | 158 / 208 |
| `0x1f08f8a` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba23 | 62 | 128 / 208 |
| `0x1f08fe2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba16 | 84 | 163 / 208 |
| `0x1f09045` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6b949 | 216 | 154 / 208 |
| `0x1f0912a` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba3d | 40 | 127 / 208 |
| `0x1f09154` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba30 | 163 | 168 / 208 |
| `0x1f0920d` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba48, 0x1e6baa2, 0x1e6bb66 | 19 | 98 / 208 |
| `0x1f0921e` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba60 | 50 | 152 / 172 |
| `0x1f0925a` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba82 | 243 | 190 / 208 |
| `0x1f0935a` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6ba95 | 133 | 163 / 208 |
| `0x1f093f2` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bb83 | 56 | 157 / 208 |
| `0x1f09434` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bb76 | 155 | 161 / 208 |
| `0x1f094ea` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bac2 | 184 | 159 / 208 |
| `0x1f095a6` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bb04 | 244 | 158 / 208 |
| `0x1f09699` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bb2e | 52 | 165 / 208 |
| `0x1f096d7` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bb4c, 0x1e6bbeb | 94 | 136 / 208 |
| `0x1f0974f` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bb59 | 219 | 175 / 208 |
| `0x1f09838` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bba0 | 101 | 201 / 208 |
| `0x1f098b9` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bc00 | 47 | 130 / 208 |
| `0x1f098ef` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bc0d | 97 | 145 / 208 |
| `0x1f0994c` | traduit / vérifié en ROM | Fallshore City : Mission HQ et récompenses | 0x1e6bc24 | 111 | 178 / 208 |
| `0x1f099c2` | traduit / vérifié en ROM | Fallshore City : PNJ et boutique | 0x1e6bc92 | 119 | 170 / 208 |
| `0x1f09a3c` | traduit / vérifié en ROM | Fallshore City : PNJ et boutique | 0x1e6bca0 | 108 | 192 / 208 |
| `0x1f09abc` | traduit / vérifié en ROM | Fallshore City : PNJ et boutique | 0x1e6bcb7 | 52 | 128 / 208 |
| `0x1f09aff` | traduit / vérifié en ROM | Fallshore City : PNJ et boutique | 0x1e6bcc4 | 69 | 142 / 208 |
| `0x1f09b40` | traduit / vérifié en ROM | Fallshore City : PNJ et boutique | 0x1e6bcd2 | 177 | 172 / 208 |
| `0x1f09bfc` | traduit / vérifié en ROM | Fallshore City : PNJ et boutique | 0x1e6bce0 | 122 | 192 / 208 |
| `0x1f09c88` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1fb469c | 89 | 144 / 208 |
| `0x1f09cf0` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bde6 | 101 | 159 / 208 |
| `0x1f09d6c` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6be33 | 120 | 135 / 208 |
| `0x1f09e0d` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6be15 | 124 | 170 / 208 |
| `0x1f09e94` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6be2a | 214 | 163 / 208 |
| `0x1f09f94` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6be6b | 140 | 154 / 208 |
| `0x1f0a03c` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6be82 | 45 | 125 / 208 |
| `0x1f0a079` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bcf8, 0x1e6bd50, 0x1e6bdb3 | 16 | 87 / 208 |
| `0x1f0a086` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bd04 | 80 | 161 / 172 |
| `0x1f0a0e6` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bd30 | 355 | 178 / 208 |
| `0x1f0a273` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bd43 | 263 | 159 / 208 |
| `0x1f0a3b5` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bd6d | 55 | 156 / 208 |
| `0x1f0a3f7` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bd8f | 46 | 144 / 208 |
| `0x1f0a436` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bdd1 | 221 | 171 / 208 |
| `0x1f0a526` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bddb | 50 | 106 / 208 |
| `0x1f0a55e` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bdc3 | 152 | 185 / 208 |
| `0x1f0a5f5` | conservé / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bed7 | 14 | 58 / 208 |
| `0x1f0a603` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bf2c | 36 | 134 / 208 |
| `0x1f0a62d` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bf55 | 103 | 154 / 208 |
| `0x1f0a694` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bf62 | 99 | 154 / 208 |
| `0x1f0a6f7` | traduit / vérifié en ROM | Flower Paradise : Shaymin et collecte de Honey | 0x1e6bf83 | 13 | 68 / 208 |
| `0x1f0a717` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1fb46d8 | 94 | 143 / 208 |
| `0x1f0a789` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6cb25 | 87 | 162 / 208 |
| `0x1f0a81d` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6ce95 | 28 | 66 / 208 |
| `0x1f0a83e` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6cf31, 0x1e6cf57, 0x1e6cf82, 0x1e6cfa8 | 49 | 128 / 208 |
| `0x1f0a86e` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6cee6 | 33 | 158 / 208 |
| `0x1f0a892` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d109 | 108 | 137 / 208 |
| `0x1f0a912` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d133, 0x1e6d1bd | 42 | 116 / 208 |
| `0x1f0a939` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d139 | 80 | 153 / 208 |
| `0x1f0a991` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d15b | 92 | 165 / 208 |
| `0x1f0a9fd` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d164 | 190 | 188 / 208 |
| `0x1f0aabd` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d16d | 216 | 188 / 208 |
| `0x1f0aba6` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d1ad | 118 | 164 / 208 |
| `0x1f0ac39` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d119, 0x1e6d1d7 | 31 | 169 / 208 |
| `0x1f0ac54` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d1dd | 76 | 150 / 208 |
| `0x1f0aca3` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d1ff | 110 | 186 / 208 |
| `0x1f0ad1c` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d208 | 143 | 161 / 208 |
| `0x1f0adcc` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d211 | 195 | 161 / 208 |
| `0x1f0aece` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d003 | 60 | 173 / 208 |
| `0x1f0af03` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d007 | 51 | 168 / 208 |
| `0x1f0af31` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d00d | 219 | 188 / 208 |
| `0x1f0b026` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d01a | 10 | 50 / 208 |
| `0x1f0b02c` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d01e | 15 | 78 / 208 |
| `0x1f0b03d` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d024 | 57 | 163 / 208 |
| `0x1f0b076` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d031 | 48 | 169 / 208 |
| `0x1f0b0a8` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d035 | 53 | 144 / 208 |
| `0x1f0b0e2` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d03b | 56 | 152 / 208 |
| `0x1f0b11c` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d048 | 44 | 124 / 208 |
| `0x1f0b151` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d04c | 58 | 170 / 208 |
| `0x1f0b194` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d052 | 48 | 157 / 208 |
| `0x1f0b1d7` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d05f | 26 | 145 / 208 |
| `0x1f0b1f2` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d063 | 18 | 99 / 208 |
| `0x1f0b209` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d069 | 117 | 156 / 208 |
| `0x1f0b284` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d076 | 60 | 129 / 208 |
| `0x1f0b2bc` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d07a | 36 | 129 / 208 |
| `0x1f0b2db` | traduit / vérifié en ROM | Frost Mountain : Aggron, Devil Duo et randonneurs | 0x1e6d080 | 174 | 148 / 208 |
| `0x1f0b3b0` | conservé / vérifié en ROM | Frozen Forest / Frozen Heights : libellés et guide | 0x1eafa94, 0x1fb3e3c, 0x1fb46e0 | 14 | 73 / 208 |
| `0x1f0b3be` | traduit / vérifié en ROM | Frozen Forest / Frozen Heights : libellés et guide | 0x1fb46e4 | 105 | 168 / 208 |
| `0x1f0b428` | conservé / vérifié en ROM | Frozen Forest / Frozen Heights : libellés et guide | 0x1e9399c, 0x1eaf8c4 | 15 | 78 / 208 |
| `0x1f0b437` | conservé / vérifié en ROM | Frozen Forest / Frozen Heights : libellés et guide | 0x1fb3ccc | 17 | 90 / 208 |
| `0x1f0b448` | conservé / vérifié en ROM | Frozen Forest / Frozen Heights : libellés et guide | 0x1fb3cd4 | 17 | 90 / 208 |
| `0x1f0b460` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6d582 | 43 | 154 / 208 |
| `0x1f0b48a` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e9305e | 24 | 113 / 208 |
| `0x1f0b4a6` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6dca0 | 39 | 109 / 208 |
| `0x1f0b4d6` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6dcd3 | 19 | 100 / 208 |
| `0x1f0b4e9` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e1c1 | 146 | 181 / 208 |
| `0x1f0b584` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e1ca | 157 | 165 / 208 |
| `0x1f0b632` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e1ef | 94 | 175 / 208 |
| `0x1f0b699` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e1e6 | 85 | 176 / 208 |
| `0x1f0b6ea` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e1f8 | 95 | 184 / 208 |
| `0x1f0b749` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e212 | 85 | 178 / 208 |
| `0x1f0b7a3` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e229 | 394 | 173 / 208 |
| `0x1f0b934` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e253 | 106 | 146 / 208 |
| `0x1f0b9b3` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e261 | 94 | 178 / 208 |
| `0x1f0ba1f` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e411, 0x1e6e432, 0x1e6e44b, 0x1e6e47a, 0x1e6e4b1, 0x1e6e4d6, 0x1e6e4f8, 0x1e6e523, 0x1e6e544, 0x1e6e568, 0x1e8d6ed, 0x1e8d70f | 6 | 30 / 208 |
| `0x1f0ba23` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e41c | 184 | 181 / 208 |
| `0x1f0bae5` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e43d | 94 | 173 / 208 |
| `0x1f0bb4b` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e456 | 214 | 179 / 208 |
| `0x1f0bc27` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e471 | 60 | 193 / 208 |
| `0x1f0bc67` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e485 | 219 | 168 / 208 |
| `0x1f0bd67` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e4bc | 230 | 187 / 208 |
| `0x1f0be5e` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e4cd | 58 | 188 / 208 |
| `0x1f0be99` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e4e1 | 528 | 189 / 208 |
| `0x1f0c11c` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e503 | 239 | 173 / 208 |
| `0x1f0c237` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e52e | 23 | 104 / 208 |
| `0x1f0c259` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e573 | 42 | 168 / 208 |
| `0x1f0c28b` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e54f | 56 | 149 / 208 |
| `0x1f0c2cc` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e599 | 119 | 164 / 208 |
| `0x1f0c34f` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e5b3 | 89 | 166 / 208 |
| `0x1f0c3af` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e5be | 84 | 166 / 208 |
| `0x1f0c40f` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e5c9 | 84 | 166 / 208 |
| `0x1f0c46e` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e6bb | 166 | 166 / 208 |
| `0x1f0c52e` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e6d6 | 208 | 168 / 208 |
| `0x1f0c615` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e7d0 | 61 | 128 / 208 |
| `0x1f0c663` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e6f2 | 92 | 194 / 208 |
| `0x1f0c6c4` | conservé / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e5e434, 0x1e5e44b, 0x1e6e5ee, 0x1e6e605, 0x1e6e61c, 0x1e6e63c, 0x1e6e657, 0x1e6e677 | 7 | 34 / 208 |
| `0x1f0c6cb` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e5f9 | 157 | 153 / 208 |
| `0x1f0c779` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e610 | 139 | 182 / 208 |
| `0x1f0c816` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e627 | 110 | 176 / 208 |
| `0x1f0c886` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e647 | 154 | 169 / 208 |
| `0x1f0c92a` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e662 | 218 | 176 / 208 |
| `0x1f0ca0d` | traduit / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e6e682 | 58 | 195 / 208 |
| `0x1f0ca42` | conservé / vérifié en ROM | Frozen Heights : village, mère, lettre et famille du rival | 0x1e604a2, 0x1e6e68f, 0x1e93022, 0x1e93039 | 9 | 46 / 208 |
