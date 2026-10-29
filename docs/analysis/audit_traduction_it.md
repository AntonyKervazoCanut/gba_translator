# Audit de la traduction italienne — A-662

Date : 29 octobre 2026. Révision auditée : `43f2eddb8be77fd76ad308aa6c5fa73ea1b41175`.
Périmètre confirmé par C-660 : projet `gba_translator`, branche `unbound`.
Audit uniquement : aucune traduction, donnée métier, recette de build ou ROM versionnée modifiée.

## Résultat et méthode

Le statut `in_progress` doit être conservé. **10 544 offsets FR sont absents du fichier IT**, soit **43,63 % des 24 164 offsets FR**. Ce ratio mesure une présence dans les sources, pas un pourcentage de scènes anglaises visibles : les tables, doublons sémantiques et données non textuelles biaisent cette interprétation.

Lecture de `CLAUDE.md`, `AGENTS.md`, `docs/21_MULTILANGUE.md`, `docs/20_TRANSLATION_PRESERVATION.md`, `Makefile`, `scripts/check_de_parity.py`, `languages/de/parity.yaml` et du glossaire DE. Lecture des mémoires ciblées IT : contrôles, descriptions d'objets, tables figées et espace libre. Les souvenirs historiques ont été confrontés au code courant.

Parsing par `scripts.audit_translation_coverage.parse_combined` : offsets numériques, dernière occurrence gagnante. La référence retenue est **`languages/fr/combined_fr.txt`**, chemin vivant du dépôt. Inventaire exhaustif de l'union FR ∪ IT : **25 642 offsets**, chaque offset affecté exactement une fois. Les 15 098 entrées existantes sont également réparties en lots de relecture : les heuristiques ne prouvent pas leur qualité linguistique.

| Mesure | Résultat |
|---|---:|
| Offsets FR / EN / IT | 24 164 / 25 524 / 15 098 |
| Absents IT vs FR / vs EN | 10 544 / 10 508 |
| Présents IT hors FR / hors EN | 1 478 / 82 |
| Identiques à la référence EN versionnée | 555 |
| Entrées vides / offsets dupliqués IT | 0 / 0 |
| Entrées protégées | 2 (0,013 % des offsets IT) |

Le chiffre initial de **504 identiques EN n'est pas reproduit** : la comparaison exacte des valeurs last-wins aux sources EN versionnées donne 555 (391 dans l'intersection FR/IT/EN). Les 555 doivent être triés : noms propres, noms d'espèces inchangés et abréviations ne sont pas nécessairement des défauts. Le fichier EN conserve des valeurs historiques françaises (ex. noms d'espèces) ; il ne doit pas être assimilé à une extraction fraîche de la ROM propre. Les comparaisons de noms d'attaques et talents ci-dessous lisent donc les cellules de la ROM EN propre.

## Pièces d'audit et traçabilité

- [Inventaire des offsets](audit_traduction_it_offsets.csv) : offset, état, domaine, preuve du classement, lieu mentionné, dernière ligne IT, alertes, lot.
- [Alertes avec textes et exemples](audit_traduction_it_alertes.csv) : toutes les occurrences détectées, avec EN/IT et nom officiel lorsque disponible. Plusieurs alertes peuvent viser le même offset.
- [Manifeste exhaustif des lots](audit_traduction_it_lots.json) : listes exactes, bornes indicatives, taille et identifiant stable de chaque lot. **Une plage de bornes n'est jamais une autorisation de modifier toutes ses lignes.**
- [Mesures et empreintes](audit_traduction_it_mesures.json) : révision, SHA-256 des sources et des six CSV terminologiques figés.
- [Inventaire de parité](audit_traduction_it_parite.csv) : présence des fichiers et activation effective de chaque étape FR/DE/IT, deux notions distinctes.
- `audit_traduction_it_tickets.json` : correspondance lots → cartes créées, dépendances requises et limites de l'API disponible.

## Couverture par domaine

Les classements `candidats` sont des **files de qualification**, pas une identification certaine. Les vraies tables utilisent les pointeurs de la ROM EN : descriptions de capacités (`src/core/moves.py`), Pokédex (`src/core/pokedex.py`), talents (293 pointeurs à `0x96DE04`), objets (structs à `0x876074`, stride 44, pointeur +20, borne de scan 1 000 structs à revalider). Les autres domaines s'appuient sur les cibles explicites des patchs FR, puis les plages et mots-clés.

| Domaine | Absents IT vs FR | Existants à relire |
|---|---:|---:|
| attaques-descriptions | 0 | 804 |
| attaques-noms | 0 | 894 |
| autres-tables-candidats | 74 | 38 |
| carte-monde | 0 | 18 |
| classes-dresseurs | 0 | 106 |
| combat-candidats | 511 | 257 |
| dialogues | 4372 | 8343 |
| donnees-police-ne-pas-traduire | 23 | 0 |
| especes-noms | 0 | 1270 |
| menus-tables-candidats | 4008 | 2527 |
| missions | 48 | 3 |
| missions-candidats | 4 | 30 |
| objets-descriptions | 335 | 250 |
| pokedex | 890 | 5 |
| pokedex-categories-structs | 279 | 0 |
| talents-descriptions | 0 | 260 |
| talents-noms | 0 | 293 |

### Dialogues, zones et chapitres

Les lots de dialogues suivent l'ordre numérique des offsets dans chaque domaine pour conserver la proximité de scripts et limiter les conflits. La colonne `lieu_mentionne` relève notamment Frozen Heights, Bellin, Dresco, Crater, Blizzard, Fallshore, Tehl, Dehara, Antisis, Seaport, Polder, Redwood, Gurun, Cootes, Cinder Volcano, Thundercap, Crystal Peak, Victory Road, Vivill, Shadow Base, Cube Corp et Battle Frontier. **Mentionner un lieu ne prouve pas que le dialogue s'y déroule.**

Aucun index fiable offset → carte/chapitre n'est disponible dans les sources consultées. Chaque lot doit retrouver les referrers de scripts et noter carte, PNJ, séquence/chapitre avant édition. Le ticket d'outillage devra produire cet index. La présente cartographie des scènes est donc partielle et explicitement sans attribution inventée. Toutes les entrées non localisées restent couvertes par un lot.

### Tables à ne pas traduire aveuglément

**23 offsets absents tombent dans les polices `0x1EAF00–0x230000`**, région protégée par `src/core/fixed_tables.py`. Ce sont des candidats d'exclusion documentée, pas 23 textes à injecter. Les **279 offsets de catégories dans les structs Pokédex** passent par le patch de catégories ; aucune réinsertion générique dans une struct n'est autorisée. Les tickets correspondants doivent clôturer chaque offset par livraison vérifiée ou exclusion motivée.

Le répertoire des données IT existe : **653 catégories Pokédex**, **903 descriptions Pokédex d'override**, mais **zéro override de description d'attaque** (`move_descriptions_it_overrides.json` vaut `{}`). La présence des 903 textes ne comble pas automatiquement les 890 absences du combined : `pokedex` n'est pas actif ; `pokedex_rewrap` est actif. Vérifier consommateur, clés et pointeurs avant toute reprise.

## Terminologie et qualité linguistique

Source de comparaison figée : PokeAPI, révision `c0a9bc75af3a455cdfa27dde21e4ec95aedd3f25`, fichiers `move_names`, `ability_names`, `item_names`, `type_names`, `nature_names`, `stat_names`, langue IT **8**, EN **9**. Les téléchargements ont réussi ; leurs SHA-256 sont consignés. PokeAPI est un corpus secondaire des jeux, pas une publication de Nintendo. Une validation officielle doit compléter le glossaire, particulièrement les termes historiques et contenus propres à Unbound.

Les noms sont rapprochés par **nom anglais de la cellule propre**, jamais par égalité des indices CFRU/PokeAPI. Résultat : **350 noms d'attaques et 153 noms de talents différents** de ce corpus. Ce total inclut les abréviations volontaires et différences typographiques ; les 503 divergences ne sont pas toutes des contresens.

| Offset | IT actuel | Référence / problème |
|---|---|---|
| `0xA40A2A` | Colpo Karate | Colpokarate |
| `0xA40AC6` | Danza Spada | Danzaspada |
| `0xA40B21` | Sbattimento | Schianto (Slam) |
| `0xA40B3B` | Calpestio | Pestone (Stomp) |
| `0xA363DC` | Armatura da Battaglia | Lottascudo ; dépasse aussi 16 glyphes |
| `0xA3640F` | Flessibilità | Scioltezza |
| `0xA36475` | Nuvola Nove | Antimeteo : calque de Cloud Nine |
| `0xA364A8` | Mutatipo | Cambiacolore : confusion avec une autre capacité |
| `0x1F1687D` | La Medaglia Visione ti permetterà di obbedire ... ai Pokémon | Contresens : les Pokémon obéissent au joueur, pas l'inverse |
| `0x17D87F` | variable + la casa di + variable | Nom du joueur dupliqué ; contrôle de template nécessaire |
| `0xA4E08B` | piu | Accent manquant : più |

Le [Pokédex officiel italien](https://www.pokemon.com/it/pokedex?type=grass) confirme les types et les noms d'espèces affichés. Nomenclature attendue des types : Normale, Lotta, Volante, Veleno, Terra, Roccia, Coleottero, Spettro, Acciaio, Fuoco, Acqua, Erba, Elettro, Psico, Ghiaccio, Drago, Buio, Folletto. Le patch CFRU contient des formes contraintes (VOLA/ROCC/COL/SPETT/ACCIA/FUOC/GHI) et garde NORMAL pour sa cellule de six octets : distinguer nom officiel et forme d'affichage documentée.

`lang.yaml` déclare `PSN/SCT/CON/PAR/SON/KO`. Le commentaire « official IT localisation » ne suffit pas à certifier les six badges : le glossaire doit fournir une source et une décision par statut, vérifier en parallèle texte et image (`status_badges`). **Aucune modification de badge n'est prescrite sans cette preuve.**

Pour les objets, le patch contient déjà un dictionnaire de noms italiens et des exceptions de largeur. Il exclut volontairement plusieurs noms trop longs et garde alors la source. Le ticket de parité doit inventorier ces exclusions, figer les noms officiels et les abréviations par cellule, puis vérifier les pointeurs des descriptions (+0x14). Les catégories contiennent des formes contraintes telles que `TopoAcqua`, `UccelArmat` : leur existence ne prouve pas leur conformité officielle. Les lieux propres à Borrius doivent faire l'objet d'une convention IT ; ne pas importer les noms créatifs FR.

Relecture exhaustive à réaliser dans les lots existants : accords, sujet/objet, pluriels, tutoiement cohérent, registre des personnages, `un po'` et élisions, apostrophe droite/typographique normalisée par le codec, accents `à è é ì ò ù`, traduction des mécaniques et cohérence MT/MN/Abilità/PS. La présente passe linguistique repose sur les écarts terminologiques exhaustifs et un échantillonnage ciblé des textes signalés ; elle **ne certifie pas les 15 098 phrases**.

## Contraintes techniques

- **42 cellules alignées dépassent leur stride après encodage**, terminaison incluse. C'est une alerte source, pas une preuve de corruption en ROM : certains patchs tronquent, abrègent ou ignorent. Exemple : `0x166BB40`, `Uovo cattivo` dans une cellule d'espèce de 11 octets. Il faut lire la cellule finale et son voisin.
- Cellules de noms : attaques 13 octets (12 utiles), talents 17 (16 utiles), espèces 11 (10 utiles), classes 13 (12 utiles), objets 14 (13 utiles). Utiliser le pointeur vivant pour la base des attaques ; l'ancien `0x1B2980` ne remplace pas la table propre `0xA40A10`.
- **19 entrées à échappement suspect**, **12 macros résiduelles** (`[LV]`, etc.), **92 écarts de nombre de marqueurs FD**, **63 écarts lexicaux de placeholders**. Les représentations EN `<0xFD>À` et IT `<0xFD><0x01>` diffèrent ; le nombre de marqueurs détecte des pertes/duplications mais ne valide pas leurs arguments. Comparer les octets avec le parseur partagé avant correction.
- Le CSV expose aussi tous les caractères non directement encodables après les alias et tokens simples : `\.`, `\Lv`, `$`, `*`, macros et quelques caractères hébreux/devanagari. **2 094 chaînes ont notamment un antislash résiduel seul dans cette analyse**, souvent `\.`. Ne pas lancer de remplacement global : vérifier la normalisation réelle dans chaque consommateur. Le codec brut substitue les caractères inconnus par `?`.
- Les accents italiens demandés sont présents dans la charmap ; cela ne garantit pas le rendu dans toutes les polices. `font` vient après les réparations LZ77, ordre à préserver. Les formes `\pk/\mn/\sm/\sf` nécessitent leur convertisseur spécifique et ne sont pas des erreurs par simple présence d'antislash.
- `\n` = saut de ligne, `\l` = défilement FA, `\p` = effacement FB. **5 entrées en fenêtres fixes** possèdent du défilement/effacement à vérifier. Budgets existants : attaques 5 lignes × 122 px, Pokédex 3 × 232 px, missions 3 × environ 172 px sans défilement. Les dialogues utilisent le rewrap adapté ; une limite globale de caractères n'est pas une validation.
- Contrôles FC/FD/F7/F8/F9 multioctets, ordre et arguments à préserver ; la comparaison de chaînes visibles seule est insuffisante. Les noms dynamiques et variables peuvent allonger une ligne en jeu.
- Un build qui réussit peut conserver l'anglais après refus de relocalisation. La collision finale est actuellement report-only côté IT : exiger une porte bloquante ou des exceptions étroites et documentées.

## Parité FR / DE / IT

Inventaire complet dans le CSV de parité. Comptes actuels : **FR 55 modules / 35 étapes**, **DE 44 / 54**, **IT 30 / 37** ; les étapes partagées ne nécessitent pas toutes un wrapper local.

IT possède déjà les correctifs graphiques `status_badges`, `type_icons`, `hp_labels`, `dexnav_headers`, les tables de noms, la date et des restaurations structurelles. Ne pas recréer ces correctifs. À l'inverse, l'absence de `official_terminology.yaml`, d'un manifeste `parity.yaml`, d'un index de toponymes et d'un équivalent certifiant `audit-de` demeure un écart réel.

Les wrappers IT `dup_move_descriptions`, `meteorite_dialogue`, `mission_descriptions`, `move_descriptions`, `pokedex` existent **mais sont inactifs**. Le descripteur documente un conflit d'allocation d'espace avec le builder générique : les activer sans budget partagé serait dangereux. `pokedex_rewrap` est une stratégie alternative, à prouver sur pointeurs vivants. Missions, carte du monde, natures, labels de statistiques et autres étapes FR/DE sans équivalent actif IT nécessitent chacune une décision `équivalent`, `partagé` ou `exclusion motivée`, puis test de livraison ; l'absence d'homonyme seule n'est pas un bug.

## Outillage à créer dans les tickets

1. **Glossaire officiel IT**, premier préalable : `languages/it/data/official_terminology.yaml`, sources figées, noms complets et formes contraintes séparés ; types, statuts, objets, attaques, talents, natures, stats, lieux génériques et conventions Unbound. Pas de traduction massive pendant sa création.
2. **`make audit-it`** : adapter les briques DE sans duplication, couverture last-wins, exclusions explicites, parité des contrôles, largeur réelle, glyphes, collisions bloquantes, toponymes, tables et résultat JSON. Index carte/chapitre depuis les scripts, sans extrapoler à partir d'une mention.
3. **`scripts/check_it_parity.py` + `languages/it/parity.yaml`**, validation complète FR/DE→IT, fichiers/étapes/données/ordre, stratégie de relocalisation et preuve des alternatives. FR reste byte-perfect.
4. **Curation** : relire les 903 overrides Pokédex (3 lots de 301) et les 653 catégories (2 lots ≤327). Définir les consommateurs et la politique de vérité unique avant de changer les données. Le fichier vide d'overrides d'attaques ne doit être rempli que pour des cas qui en ont besoin.
5. **Certification finale** : zéro manque non justifié, tri des identiques EN et hors références, toutes les alertes clôturées, graphe de tickets soldé, source/ROM et pointeurs vivants concordants, build/test locaux et rendu headless. Seulement alors modifier `status: complete`.

## Découpage et règles communes

Les **88 lots d'offsets** couvrent sans chevauchement **10 544 absents + 15 098 existants**. Chaque lot contient au plus **350 entrées** ; les petites tables et corpus particuliers restent volontairement sous 150 pour préserver leur indépendance. Les gros domaines sont répartis en lots équilibrés. Les corrections de données de curation ont cinq lots supplémentaires, indépendants par clés.

Règles à rappeler dans chaque ticket :

- Éditions **chirurgicales de `combined_it.txt` uniquement pour les textes**, jamais de régénération, tri ou sed global ; éditer la **dernière occurrence** de l'offset. Pour les tickets d'infrastructure/curation, les fichiers techniques explicitement nommés sont autorisés ; ne pas déplacer des phrases hors de leur source de vérité.
- Toute ligne ajoutée/modifiée → valeur exacte dans `languages/it/protected_entries.yaml`, **même commit**, hook activé.
- Relire le fichier au moment d'éditer, committer immédiatement, relire le diff (**Pattern C**), chemins précis.
- Validation de chaque fix : **`make build-it` + `make test-python`** ; vérifier les pointeurs vivants et cellules voisines concernés. **Ne jamais toucher au hash de la ROM FR.**
- Commits en français **`type(scope): description`**. Aucun push ni démarrage de pipeline distant.
- Les lots de traduction dépendent du glossaire et de la validation de parité/outillage ; le dernier ticket dépend de **tous** les lots et préalables. Ne pas traiter un offset de police comme du texte.

## Non vérifié et limites de livraison

Pas de certification visuelle dans cet audit documentaire : aucun changement de rendu. Les hooks de commit imposent les builds locaux FR/IT/DE ; leurs résultats de reprise sont consignés ci-dessous. Les ROM déjà présentes dans le checkout principal datent d'août ; elles ne prouvent pas le rendu de la révision d'octobre. Leur présence sert uniquement à l'inventaire et à la lecture de la source propre. Le hash FR mesuré avant/après doit rester `74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.

Le catalogue MCP annonce `kanban-board`, mais **aucun outil `kanban_create_ticket` ni `kanban_update_ticket` n'est exposé dans `ALL_TOOLS`**. Le repli disponible est `orchestration_create_follow_up_ticket`, qui crée des cartes TODO mais **n'accepte pas `dependsOn`**. Les dépendances sont conservées dans les descriptions et le manifeste (`requiredDependsOnTicketIds`) ; leur application au graphe Kanban nécessite la capacité de mise à jour, suivie dans **C-1011**. Il ne faut pas confondre une dépendance textuelle avec un lien structurel effectif. Le ticket de raccordement dédié décrit précisément cette étape restante ; les cartes ne doivent pas être lancées en avance.

## Reproduction de la couverture et contrôle du découpage

```python
from pathlib import Path
from scripts.audit_translation_coverage import parse_combined
import csv, json
fr = parse_combined(Path('languages/fr/combined_fr.txt'))
it = parse_combined(Path('languages/it/combined_it.txt'))
en = parse_combined(Path('languages/en/combined_en.txt'))
assert len(fr.keys() - it.keys()) == 10544
assert sum(it[o] == en[o] for o in it.keys() & en.keys()) == 555
lots = json.loads(Path('docs/analysis/audit_traduction_it_lots.json').read_text())
flat = [int(o, 16) for lot in lots for o in lot['offsets']]
assert len(flat) == len(set(flat)) == len(fr.keys() | it.keys())
assert set(flat) == fr.keys() | it.keys()
assert all(0 < lot['nombre'] <= 350 for lot in lots)
rows = list(csv.DictReader(Path('docs/analysis/audit_traduction_it_offsets.csv').open()))
assert {int(r['offset'], 16) for r in rows if r['etat'] == 'manquant'} == fr.keys() - it.keys()
```

Pour reproduire la classification : priorité aux plages de police/structs protégées, puis aux cinq tables de noms documentées ci-dessus, aux pointeurs de descriptions EN, aux cibles des patchs FR, puis aux candidats. Les candidats combat utilisent la plage `0xA4B000–0xA4F000` ou `foe/wild/fainted/critical hit/super effective` ; missions `mission/bounty/quest` ; menus `0x3D0000–0x420000` ou texte de moins de 38 caractères sous `0x1E00000` ; dialogues à partir de `0x1EE0000` ou prose de plus de 38 caractères. Tout le reste reste à qualifier. Les groupes `(état, domaine)` sont triés par offset puis partagés en `ceil(n/350)` lots équilibrés. Cette règle est un classement d'audit et ne doit jamais devenir un filtre de réinsertion.

## Vérifications à la reprise

- Les quatre tests de `tests/unit/it/test_audit_translation_it_plan.py` passent ; la couverture a également été recalculée depuis les sources courantes (10 544 absents, 555 identiques EN, union de 25 642 offsets). Les empreintes des trois sources correspondent au snapshot.
- Premier hook : 2 031 tests Python réussis, un test préexistant ignoré et 425 désélectionnés ; 68 tests Vitest réussis. Le build FR a ensuite révélé un JSON de traduction d'août périmé, copié avec une date récente. `make prepare-fr` puis `make build-fr` réussissent avec les sources actuelles, sans modification de code ou de traduction. Les artefacts reconstruits restent locaux au worktree ; la ROM FR de référence du checkout principal est inchangée.
- Ruff n'est pas installé dans le Python système ; le lint Ruff n'est pas vérifié. Aucun pipeline distant lancé.

## Cartes créées

Les 98 cartes ont été relues dans le Kanban : **A-757** (glossaire existant réutilisé), **A-916** (outillage), **A-917** (parité), **A-918 à A-1005** (88 lots d'offsets), **A-1006 à A-1010** (curation), **C-1011** (raccordement structurel) et **A-1012** (certification finale). Le manifeste contient leur UUID, référence et liste exacte des UUID préalables requis. Toutes sont TODO à la création ; aucune correction n'a été exécutée par cet audit.

**Limite restante :** les liens `dependsOn` ne sont pas appliqués par l'API de repli. C-1011 porte exclusivement leur raccordement via une capacité Kanban effective ou l'interface humaine. Le plan ne doit pas être exécuté comme si ces liens existaient déjà.

Le commit du rapport a passé les hooks activés : suites Python/Vitest et builds locaux FR, IT, DE réussis. Après intégration de l'audit ES concurrent, les sept tests des plans IT/ES passent également. Aucune ROM ni traduction versionnée n'a été modifiée ; aucun push effectué.

À la nouvelle reprise du 29 octobre, la lecture du graphe confirme les 98 UUID : 19 cartes portent déjà des dépendances, mais 77 cartes ont encore des préalables requis manquants, dont A-1012. Le manifeste conserve les liens observés séparément des liens requis. C-1011 reste le préalable bloquant de clôture de cet audit ; aucune carte supplémentaire n’a été créée.
