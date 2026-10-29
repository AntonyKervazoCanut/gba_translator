# B-686 — Qualification du lot pokedex-01

Périmètre fermé : 97 offsets, aucun audit global relancé. Le nom du lot ne
reflète pas tout son contenu : 7 fiches Pokédex, 60 descriptions de décorations,
10 fragments binaires et 20 textes/prefixes de communication.

## Sources et décisions

La ROM EN canonique est validée par `scripts/verify_roms.py`, SHA-256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Le JSON associé donne, pour chaque offset, les dernières valeurs EN/FR/DE,
la préimage brute canonique, les commandes et les références de pointeurs.
Le corpus nommé EN contient du français : la ROM prime sur ce corpus.

Les 7 fiches concernent Weezing, Shuckle, Makuhita, Aggron, Carvanha,
Banette et Spheal. Sens confronté à la ROM : gaz **toxiques**, fermentation
des Baies, endurcissement contre les arbres, montagne et blessures de combat,
coques percées, rancune de la poupée et déplacement en roulant.
Deux fiches corrigées à l’écran, trois sources alignées sur la curation déjà
injectée (Makuhita, Aggron, Banette), deux conformes conservées. La version
courte d’Aggron exprime son expérience par ses blessures sans reprendre
l’avertissement rhétorique final ; ce choix de curation est conservé.

Les décorations emploient un registre nominal cohérent. Les espèces restent
anglaises selon la convention du build : Smoochum, Duskull, Wynaut, Baltoy,
Skitty, Seedot et Sableye remplacent notamment les espèces erronées.
Le motif aquatique remplace le contresens « Filigranmuster ».
Surfer, Donner, Feuersturm, Pulverschnee, Anziehung, Geofissur et Stachler
sont vérifiés dans `languages/de/data/move_names_de_official.json`, référencé
par `official_terminology.yaml`. Aucun talent, statut, Sohn/Tochter ou dialogue
de personnage n’apparaît dans ces corrections. `0x7A823B` est hors lot.

Les 60 descriptions de décorations restent sur 2 ou 3 lignes, au plus 107 px
par ligne (garde conservatrice 110 px). Les fiches restent sur 3 lignes de
232 px maximum. L’échange garde ses deux changements de page et ses quatre
buffers ordonnés. L’en-tête conserve les trois commandes de positionnement.
Les pauses des deux chaînes d’attente sont conservées sans changement.
Les pages de l’offre d’échange tiennent en 187/188 px même si le build fusionne
leurs lignes, avec niveau 100 et nom d’espèce de douze glyphes larges.

## Qualification exhaustive

| Offset | Décision | Motif | Références EN |
|---|---|---|---|
| `0x447800` | corrigé | Fidélité et budget Pokédex (3 × 232 px). | 0x1a36754 |
| `0x44a0c1` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x1a375d0 |
| `0x44c1f5` | corrigé | Source alignée sur la curation DE prioritaire déjà injectée, sans modifier cette ressource. | 0x1a3817c |
| `0x44c5fd` | corrigé | Source alignée sur la curation DE prioritaire déjà injectée, sans modifier cette ressource. | 0x1a382e4 |
| `0x44cad6` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x1a38494 |
| `0x44d92a` | corrigé | Source alignée sur la curation DE prioritaire déjà injectée, sans modifier cette ressource. | 0x1a389a4 |
| `0x44dcc3` | corrigé | Fidélité et budget Pokédex (3 × 232 px). | 0x1a38ae8 |
| `0x452fcb` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x453010` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x454284` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455770 |
| `0x4542bc` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455790 |
| `0x4542f3` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4557b0 |
| `0x454398` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455810 |
| `0x454625` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455a50 |
| `0x45465a` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455a70 |
| `0x454789` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455b30 |
| `0x4547b7` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455b50 |
| `0x454bfd` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455e70 |
| `0x454c31` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455e90 |
| `0x454c68` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455eb0 |
| `0x454ca2` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455ed0 |
| `0x454cdb` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455ef0 |
| `0x454d13` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455f10 |
| `0x454d4a` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x455f30 |
| `0x454f02` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456090 |
| `0x454f2d` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4560b0 |
| `0x454f5a` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4560d0 |
| `0x454f86` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4560f0 |
| `0x454fb2` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456110 |
| `0x454fe1` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456130 |
| `0x455010` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456150 |
| `0x45503e` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456170 |
| `0x45506e` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456190 |
| `0x45509a` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4561b0 |
| `0x4550c8` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4561d0 |
| `0x4550f3` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4561f0 |
| `0x455121` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456210 |
| `0x45514e` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456230 |
| `0x45517b` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456250 |
| `0x4551a7` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456270 |
| `0x4551d4` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456290 |
| `0x455200` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4562b0 |
| `0x45522c` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4562d0 |
| `0x455259` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4562f0 |
| `0x455287` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456310 |
| `0x4552b3` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456330 |
| `0x4552df` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456350 |
| `0x45530b` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456370 |
| `0x455336` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456390 |
| `0x455362` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4563b0 |
| `0x455392` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4563d0 |
| `0x4553c1` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4563f0 |
| `0x4553f2` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456410 |
| `0x455424` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456430 |
| `0x455453` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456450 |
| `0x455483` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456470 |
| `0x4554b0` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456490 |
| `0x4554e3` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4564b0 |
| `0x455515` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4564d0 |
| `0x455548` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4564f0 |
| `0x455573` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456510 |
| `0x45559e` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456530 |
| `0x4555c9` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456550 |
| `0x4555f4` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456570 |
| `0x45561f` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456590 |
| `0x45564a` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4565b0 |
| `0x455675` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4565d0 |
| `0x4556a0` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x4565f0 |
| `0x4556cb` | corrigé | Décoration : sens, espèce EN conservée, registre nominal et 3 lignes courtes. | 0x456610 |
| `0x4566c8` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x4566e8` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x456708` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x456728` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x45687c` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x45689c` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x4568bc` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x4568dc` | fragment sans pointeur direct | Données graphiques répétitives, pas une phrase : ne pas injecter. | aucune |
| `0x4571b7` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x45749d` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x4574c1` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x4574e9` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x4577b9` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x4577f5` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x457950` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x457a38 |
| `0x4579bc` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x457a3c |
| `0x457a70` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x457b08 |
| `0x457b2a` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x457b4c` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x457b88, 0x457b8c |
| `0x457d44` | corrigé | Échange Salle Union : quatre buffers F7 00/01/02/03 ordonnés ; pages de 187/188 px même après fusion avec niveau 100 et nom de 12 glyphes larges. | 0x11b074, 0x457e84 |
| `0x457e28` | déjà correct | Sens conforme à la ROM EN, aucun ajout requis ; contrôles comparés en octets. | 0x116308 |
| `0x457e41` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x458fc6` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. Aide de touches vivante hors lot : besoin de correction distincte à qualifier, aucun patch ici. | aucune |
| `0x45934b` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. Chat est un terme courant allemand légitime. | aucune |
| `0x459378` | corrigé | En-tête de liste Salle Union absent : Name/Gesucht/Angebot/Lv., positions FC 13 3C/6E/C6 conservées. | 0x11a1f8 |
| `0x4593d3` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. Chat est un terme courant allemand légitime. | aucune |
| `0x459541` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |
| `0x459561` | fragment sans pointeur direct | Préfixe de remplissage avant la chaîne réellement référencée : ne pas écrire ici. | aucune |

## Exclusions et limites

Deux coïncidences binaires sont exclues des références vivantes : 0x146B64
(instructions Thumb au milieu d’une fonction) et 0xCBA129 (bloc de données).
Leurs quatre octets restent identiques à la ROM source. Seules les tables
Pokédex (pas 36), décorations (pas 32) et les références de communication
sont retenues : 76 sites structurés pour 74 entrées vivantes.

Les dix fragments graphiques à 0x452FCB/0x453010 et 0x4566C8–0x4568DC
restent absents du combined. Une absence de pointeur direct ne démontre pas
une inaccessibilité absolue ; leur contenu binaire ne justifie aucune traduction.
Treize offsets de remplissage précèdent des chaînes référencées à +1, +2 ou +3 :
les adresses et sources des voisins sont détaillées dans le JSON. Modifier ces
préfixes risquerait de tronquer la chaîne voisine. Les deux occurrences de Chat
sont légitimes en allemand. L’aide à 0x458FC8 est hors lot et nécessite une
qualification distincte ; aucune modification à un voisin n’est incluse.

La sonde visuelle vérifie six chaînes réellement lues via leurs pointeurs
finaux et imprimées par mGBA, avec assertions OCR Playwright. Elle utilise une
boîte native de dialogue : elle ne certifie pas le parcours du menu de
décorations, du Pokédex ou de la Salle Union. Ces parcours exhaustifs ne sont
pas vérifiés ; les budgets des chaînes finales sont contrôlés séparément.

Aucun patch de jeu ni ressource de données de jeu modifié. La matrice de tests
DE est seulement complétée pour déclarer le nouveau fichier de tests.
Les boîtes de communication existantes emploient aussi le vouvoiement : ce sont
des messages système, sans personnage ni accord de genre à reconstruire.

## Résultats locaux

Validation sur les sources du commit `0ca665da` (instantané JSON avant rebase).
Les tests ROM recalculent les pointeurs du build courant ; les adresses du JSON
ne sont pas des constantes d’injection.

- `make build-de` : succès ; les hooks ont également reconstruit FR/IT/DE dans
  le worktree isolé, sans changer leurs sources ni les ROMs du dépôt principal.
- `make test-python` : **4 041 réussis, 3 ignorés préexistants, 2 280 désélectionnés**.
- Hook : **3 900 tests Python rapides et 68 tests Vitest réussis**.
- `python3 -m pytest tests/unit/de/test_pokedex_01.py -q` : **4 réussis**, dont
  les octets finaux, les commandes ordonnées, les boîtes et les faux pointeurs.
- `npx playwright test --config tests/e2e-playwright/playwright.pokedex-01-de.config.ts` :
  **1 réussi**, six rendus natifs mGBA avec assertions OCR. Capture PNG hors dépôt,
  jointe à B-686. Seule ambiguïté OCR tolérée : le glyphe `l` lu comme `1` ; les
  octets du nom sont vérifiés indépendamment.
- `make lint` et ruff sur le test ajouté : succès.
- 76 références structurées : commandes finales identiques à la ROM EN ;
  67 valeurs corrigées/alignées livrées exactement, à repli des lignes près.
- Budgets finaux : Pokédex au plus **212/232 px**, décorations **107/110 px**,
  au plus 3 lignes. Offre d’échange : **187/188 px** en expansion maximale.
- `scripts/verify_roms.py` : les trois entrées privées correspondent au baseline.
  SHA-256 de la ROM FR principale inchangé :
  `74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
- Préservation vérifiée byte à byte : 66 dernières occurrences modifiées,
  un ajout (`0x459378`), toutes les autres lignes et fins de ligne identiques.
  Les 67 valeurs ont leur protection exacte dans le même commit que leur texte.

Les premiers essais ont exposé deux problèmes de préparation, résolus sans
modifier le produit : déclaration du test dans la matrice DE et présence des
artefacts locaux attendus par le dry-run Make. Un essai Python lancé pendant
le rebuild IT a été entièrement rejoué après stabilisation (résultat ci-dessus).
La sonde écrit le contexte du script GBA atomiquement pour éviter qu’une frame
ne consomme un pointeur encore ancien entre deux commandes du pont.

Aucun audit qualitatif global relancé, aucun push ni pipeline distant démarré.
L’aide de touches vivante `0x458FC8`, appelée par `0x1168F8`, reste anglaise
(`Choose / Join / Cancel`) : correction distincte hors lot requise à cette
adresse, pas au préfixe `0x458FC6`. Aucun autre besoin de patch de jeu n’est
nécessaire pour livrer les 67 valeurs de ce lot.
