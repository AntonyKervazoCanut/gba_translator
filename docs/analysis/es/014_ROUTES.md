# ES-014 — Contrats techniques de descriptions et textes système (F-1042)

Les 374 clés de `lots.json` restent inchangées. `014_ROUTES.json` consigne les
préimages EN propres, les références et une décision technique pour chacune.
Préparation parent : attachment://89a767a6-3e6f-4ee0-9191-0df9f1e49cd4.
Source SHA-256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Aucune traduction finale, aucun combined, protected_entries, glossaire ou cache
partagé n'est modifié. Les décisions linguistiques restent à F-864.

## Acheminement existant

`languages/es-maint/system_texts.json` étend `SystemTextRoutes` (B-1031/B-1032,
F-1035). Aucun nouveau réinserteur, patch ou changement du code partagé.
Le pipeline CSV → JSON est conservé. À partir du combined fourni, enrich_json
reconstruit les lignes manquantes ou obsolètes dans le JSON réellement transmis
au builder : préimage intégrale, capacité, références et fenêtre explicite.
Le cache partagé n'est jamais une autorité pour ces clés. Le test temporaire
retrouve notamment 0x482AA0 absent et remplace la préimage française de 0x482A53.

Les 339 descriptions actives sont ciblées par `0x99F190 + move_id*4`.
Les routines E541A et 137B88 utilisent `0x99F194+(move_id−1)*4`, chargée via
E5440/137BC8 ; 9F3B38 utilise la troisième racine 9F3B64 pour les CT/MO.
Toutes les références littérales sont figées, y compris les duplications des
anciennes tables. Les racines, routines, métriques et cellules non sélectionnées
de la table moteur sont gardées avant et après les patches.

- 270 descriptions : cinq lignes FE, 122 pixels par ligne, 512 octets maximum.
- 69 descriptions partagées avec gItems : intersection conservatrice des fenêtres,
  trois lignes FE et 122 pixels. Le Cube accepte 176 pixels, mais le résumé exige
  122 ; aucun rewrap différent selon le consommateur.
- La table de 128 CT/MO à 1A42B2A (racine 125A8C, 256 octets) atteint exactement
  ces mêmes 69 descriptions : 62 CT et sept MO du lot. Les accès dynamiques sont
  donc couverts en plus des pointeurs gItems explicites.
- Résumé : police 2 via 137B94 →12E5A4. Autre surface capacités : police 3 via
  E565E →12E5A4. La police 3 latine réutilise le décompresseur de police 2
  (67C0→65B8) et les largeurs 207300 via 67E0. Ces 256 métriques, comme celles
  de la police 1, sont exactement les GLYPH_WIDTHS du validateur existant.

FE reste explicite ; les capacités n'autorisent pas FA/FB. Le contrat existant
compare FC/FD/F8/F9/F7 avec tous leurs arguments et l'ordre des buffers, refuse
les terminateurs internes, les dépassements, le fallback et la troncature.
La vérification finale relit les octets à **chaque** consommateur après patches,
et refuse les entrées disparues ou dupliquées.

## Les 35 autres clés

Huit anciennes descriptions :

| Clé | Ancien move_id | Cible moteur actuelle hors lot |
|---|---:|---|
| 482A11 | 8 | A37C6F |
| 48371F | 58 | A37CB9 |
| 483760 | 59 | A37D02 |
| 483B57 | 74 | A37D4F |
| 4852B8 | 161 | A37D98 |
| 48581E | 181 | A37DE4 |
| 486532 | 229 | A37E33 |
| 4881E1 | 336 | A37E7C |

Elles n'ont aucune cible gItems actuelle. Les références appartiennent aux
anciennes tables 4886E8/904000 et, pour deux clés, gItems ancien 3DB028.
Ces bases n'ont pas de racine moteur ; les routines actuelles utilisent les
cibles ci-dessus. Conservation sans injection, sans déplacer la traduction vers
un autre lot. Les cellules anciennes de ces huit clés sont également gardées.

Les 18 textes 488CA2..4897EE réutilisent `preserve_control_flow` : neuf routines
copient/expandent le texte vers gStringVar4 et neuf scripts opcode BD le chargent.
Les préimages entières (265 octets au plus), les commandes et FA/FB sont conservées.
Les opcodes et segments de routine sont gardés sans figer les pointeurs destinés
à la relocation. Leur parcours naturel Mystery Gift n'est pas certifié ici.

Les neuf dernières clés sont exclues sur la preuve de leurs conteneurs :

| Clé(s) | Conteneur démontré |
|---|---|
| 4ABE2F | PCM, en-tête 4ABD24, racine instrument 48A0EC |
| 53D24F | Sample type 1, en-tête 53CE70, racines 19E9C5C/19ED904 |
| 59D2CC | Sample type 1, en-tête 59C97C, quatre racines dans le JSON |
| 5A19AF | Sample type 1, en-tête 5A05D8, racines 19EA070/19EDD18 |
| 69E06A | PCM, en-tête 69DEE0, racine 48EDD8 |
| 6B47F1 | PCM, en-tête 6B3540, racine 49B27C |
| 6C09CF / 6C0A84 | Image brute [6C0318,6C0B18), SpriteFrameImages 6C0148 |
| 6C0B90 | Image brute [6C0B18,6C1318), même table, racine 3A4B20 |

Les 17 exclusions sont refusées à l'import ; aucune conclusion n'est fondée
uniquement sur l'adresse ou l'absence de pointeur littéral.

## Vérification reproductible

- `tests/unit/test_es014_routes.py` : tranches ROM réelles, sélection exhaustive,
  préimages, récupération JSON, limites, commandes complètes, exclusions,
  disparition d'entrée, racines et comparaison intégrale des octets.
- `python3 tests/e2e-playwright/fixtures/prepare_es014_probe.py` : vrais CSV,
  convertisseur, builder et tous les patches, combined temporaire uniquement.
  Les écritures avant patches sont comparées à la ROM EN ; après patches elles
  sont comparées à un témoin subissant les mêmes patches sans traduction.
  Seules les cellules/pointeurs sélectionnés et leurs allocations sont permis.
- `npx playwright test -c tests/e2e-playwright/es014-routes.config.ts` : mGBA natif
  offscreen et navigateur headless. Assertions des octets livrés, des cinq lignes
  du résumé et des trois lignes du Cube, OCR et retour de navigation avant capture.
  La copie éphémère réaffecte les slots de la fixture à une description livrée ;
  elle certifie les fenêtres, pas une association capacité/nom de production.
- Captures dans le répertoire temporaire système, attachées au ticket, jamais
  dans le dépôt. Aucune sauvegarde en jeu.

La certification linguistique, les valeurs finales et les parcours naturels
complets restent au parent F-864. La comparaison intégrale couvre les sentinelles,
pas une certification globale de toutes les traductions historiques.
