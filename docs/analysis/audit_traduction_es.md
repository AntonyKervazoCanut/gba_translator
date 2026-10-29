# Audit de la traduction espagnole — A-663

Date : 2026-10-29. Périmètre : `gba_translator`, tranche du parent C-660.
Audit et préparation du travail ; aucune traduction de masse ni modification de ROM.

## Décision d’architecture

Conserver **`es` comme référence communautaire**, avec `status: reference`, `build: none`,
`languages/es/combined_es.txt` inchangé. Conserver `make build-es`, `pipeline`, les
extractions EN/ES et l’offset map : ils servent à reproduire la ROM communautaire,
et ne constituent pas un build maintenu depuis les fichiers `combined`.

La nouvelle cible sera **`es-maint`**, avec `status: in_progress`, `build: generic`,
`builder_language: spanish`, `combined: languages/es-maint/combined_es-maint.txt`,
`output_rom: GenedRom-es-maint.gba`, `patch_source: input/roms/englishrom.gba`.
L’infrastructure est confiée à un ticket dédié : ne pas annoncer cette cible comme
actuellement disponible. `make build-es-maint` s’ajoutera à `build-all` et donc à
`release-all`, sans réaffecter `build-es` et sans changer la recette FR.

**Ne pas copier aveuglément l’extraction ES dans le nouveau combined.** Elle contient
des fragments de chaînes, des arguments de contrôle décodés comme lettres, des données
binaires et des substitutions communautaires hors scénario. L’infrastructure créera
initialement un fichier vide commenté et `protected_entries.yaml` vide, puis les lots
importeront chirurgicalement les seules traductions vérifiées. C’est une création
initiale explicite, pas une régénération d’une source existante. À chaque import :
contrôler le texte anglais à l’offset canonique, son pointeur vivant et la correspondance
ES via l’offset map ; ne pas supposer que les adresses sont identiques entre ROMs.

Aucun changement de charmap partagé ne devra modifier les octets FR : introduire le
profil d’encodage ES nécessaire plutôt que modifier les alias par défaut. Préserver
les étapes mécaniques génériques (`repair_lz77`, `repair_localized_lz77`,
`repoint_stale`, `legendary_ritual`) ; appliquer la police après les réparations LZ77.
Les patches spécifiques FR ne doivent pas être copiés en bloc.

## Mesures reproductibles

Les valeurs sont résolues par **dernière occurrence gagnante**, via le parseur existant
`scripts.audit_translation_coverage.parse_combined`. Il ne s’agit pas d’un comptage de
lignes. Provenance, listes exhaustives et empreintes : [mesures.json](es/mesures.json).
Programme exact d’analyse : [methode.md](es/methode.md).

| Mesure | Résultat |
|---|---:|
| Offsets uniques ES | 23 873 |
| Offsets uniques EN | 25 524 |
| Offsets uniques FR | 24 164 |
| ES strictement identique à EN | 9 687 (40,58 %) |
| ES différent de EN, sans présumer de la qualité | 14 186 |
| Offsets FR absents de ES | 308 |
| Offsets ES absents de FR | 17 |
| Offsets EN absents de ES | 1 651 |
| Union FR ∪ ES | 24 181 |
| Données de police exclues de la traduction | 23 |
| Entrées réparties dans les lots | 24 158 |

La mesure du ticket (9 627) diffère de 60 entrées : le présent chiffre correspond aux
sources identifiées par SHA-256, pas à une reconstitution non vérifiable de l’état du
28 octobre. L’égalité à EN est un **signal de triage**, pas la preuve d’un défaut :
noms d’espèces, acronymes ou textes techniques peuvent rester identiques. À l’inverse,
un texte différent peut être encore anglais, corrompu ou non textuel.

Les 1 651 absences par rapport à EN ne sont pas interchangeables avec les 308 absences
par rapport à FR. Le présent plan couvre FR ∪ ES ; l’exhaustivité du jeu demandera
également l’examen des extractions par pointeurs et des surfaces graphiques au ticket
final. Les 54 offsets de cette union sans référence EN doivent être reconstruits depuis
la ROM et les pointeurs avant toute traduction ; pas de traduction à partir du FR seul.

Le test existant `tests/e2e/es/test_extraction_coverage.py` dépassait son plafond
de 300 et recommandait une régénération interdite. Il utilise désormais la liste des
308 lacunes auditées : toute absence supplémentaire échoue, même si une autre lacune
est comblée en parallèle. Un cas de régression vérifie explicitement cet échange à
nombre constant ; aucune entrée ES ou FR n’est modifiée pour faire passer le test.

## Qualité communautaire : exemples vérifiés dans les sources

| Offset | Constat | Travail attendu |
|---|---|---|
| `0x0018D43D` | La scène des quatre garçons devant la télévision devient une publicité « YOSOYKIKE » | Rétablir le sens du scénario EN en espagnol |
| `0x0018D53B` | Une notice devient une annonce datée du 24 décembre 2024 | Rétablir la notice, conserver séparément les crédits légitimes |
| `0x00190687` | Début `EEjust don't know...`, reste anglais | Retrouver le texte vivant complet avant traduction |
| `0x00196A82` | `esta máquinas` | Accord `estas máquinas`, après contrôle du contexte et du budget |
| `0x0018D3F8` | Ponctuation inversée extraite sous forme `<0x52>` | Vérifier le codepoint et la police, pas un remplacement global |

Il ne s’agit pas d’une validation linguistique exhaustive des 14 186 différences.
Les lots incluent leur relecture : fidélité, accords, accents, ponctuation et cohérence
terminologique. Les noms d’espèces restent ceux de la localisation espagnole officielle
(ex. Pikachu), avec exceptions/formes propres au hack documentées. Les noms de lieux
propres à Unbound doivent suivre une politique unique, sans traductions improvisées.

Le glossaire doit fixer les types, objets, attaques, talents, natures, statistiques,
termes du Pokédex, menus et toponymes, avec variantes courtes justifiées par les cellules.
Sources officielles de départ : [Pokédex Pokémon](https://www.pokemon.com/el/pokedex)
pour les noms/types/habilités ; [règles Pokémon en espagnol](https://assets.pokemon.com/assets/cms2-es-es/pdf/trading-card-game/rulebook/sm12-rulebook-es.pdf)
pour les termes Envenenado, Quemado, Paralizado, Dormido. Ces règles JCC ne prouvent
ni les abréviations du jeu vidéo ni la terminologie propre aux générations récentes :
les vérifier sur une localisation officielle du jeu vidéo et consigner la provenance.

## Contraintes techniques et faux positifs

[inventaire.csv](es/inventaire.csv) contient chaque offset de FR ∪ ES, les trois textes,
le domaine, le lot, les longueurs et les alertes, sans réécrire les sources.

| Signal statique | Nombre | Interprétation |
|---|---:|---|
| ES plus long que EN, en octets réencodés hors terminateur | 2 572 | Budget à vérifier ; relocalisation possible, pas automatiquement un overflow |
| Séquence de marqueurs différente | 2 462 | Contrôle nécessaire, pas une preuve de placeholder cassé |
| Longueur réencodée ≥ 512 | 118 | Plafond de l’extracteur à examiner ; pas une preuve de troncature seule |
| Ajout promotionnel/date repéré par motif | 4 | Échantillon de substitutions à relire |

Les longueurs emploient `TextEncoder.encode_pokemon` après conversion de `\n`,
`\l`, `\p`, hors `0xFF`. Elles restent indicatives : les alias peuvent perdre des
caractères et les macros nommées doivent être résolues par le pipeline réel.
Le comparateur de marqueurs relève les `<0xFC/FD/F8/F9/F7/FA/FB>` et `{...}` dans
l’ordre ; il ne valide pas leurs arguments, ni la sémantique des codes. Il ignore les
simples changements de `\n` pour éviter de confondre rewrap et perte de contrôle.
Pour chaque correction, comparer les **octets de contrôle complets** (arguments inclus),
les buffers positionnels et la pagination ; ne jamais permuter `{0}` et `{1}`.

`scripts/extract_combined_rom.py` lit au même offset dans la ROM ES, avec une limite
de 512 octets. Son décodage peut transformer un argument de commande en lettre :
`<0xFD>À` n’est pas nécessairement du texte espagnol. La comparaison textuelle ne
remplace donc ni l’alignement EN→ES ni la lecture au pointeur vivant de la ROM produite.

Les plages fixes connues contiennent 1 261 noms d’espèces et 279 catégories Pokédex.
Les 23 entrées dans `0x1EAF00–0x230000` appartiennent aux polices : **à exclure**,
jamais à traduire ni injecter. Les autres banques sont nommées par leur position ROM,
pas par une carte supposée : l’attribution à une zone doit être confirmée via les
référents de scripts. Les tables d’attaques connues n’ont aucun offset dans cette
extraction ES ; leur absence ici ne garantit pas leur traduction dans le jeu.

Budgets : taille encodée + terminateur, stride et voisins pour les cellules fixes,
largeur en pixels et police effective pour l’interface, pagination pour les dialogues.
Une entrée présente dans le combined ou un build réussi ne prouve pas son injection.

## Charmap et police

Résultat réel de l’encodeur actuel, hexadécimal hors terminateur :

| Caractères | Octets |
|---|---|
| á é í ó ú ñ | 17 1B 6F 23 27 29 |
| Á É Í Ó Ú Ñ | 02 06 5A 0E 12 14 |
| ü Ü | E9 CF : perte des trémas, u/U |
| ¡ ¿ | AB AC : perte de l’inversion, !/? |

`font_glyphs` seul ne règle pas ces pertes. `ü/Ü` ont des slots allemands mais sont
rabattus par les alias du profil générique. `¡/¿` sont absents de `POKEMON_TABLE` et
rabattus par `SPANISH_ALIASES`. Le ticket d’infrastructure doit préserver les glyphes
sans modifier le profil FR et synchroniser la charmap TypeScript si nécessaire.

Contrôle binaire en lecture seule : dans la police brute FONT_SMALL à `0x1EAF00`,
les cellules de 32 octets pour ñ/á/í/ó/ú sont non vides (respectivement 24/24/12/24/24
octets non nuls) et identiques entre les ROMs EN et ES épinglées. Cela vérifie leur
présence, **pas leur rendu** : toutes les polices (dialogue, petite, intro, graphismes)
demandent une preuve visuelle lors de l’infrastructure.

Descripteur attendu : `font_glyphs: "áéíóúüñÁÉÍÓÚÜÑ¡¿"`, statuts `poison: ENV`,
`burn: QUE`, `freeze: CON`, `paralysis: PAR`, `sleep: DOR`, `faint: DEB` (forme courte
à confirmer dans le glossaire avec la contrainte de trois caractères). Prévoir les
badges graphiques autant que les chaînes de texte.

## Plan de tickets et préservation

[lots.json](es/lots.json) fige **63 lots indépendants de 279 à 397 entrées**.
Ils couvrent exactement les 24 158 offsets traduisibles de FR ∪ ES, sans chevauchement.
Les 23 offsets de police sont exclus explicitement dans l’inventaire. Les lots sont
regroupés par tables connues ou banques ROM ; chaque ticket possède ses offsets exacts,
jamais une fenêtre recalculée avec `--skip-existing`.

Ordre : glossaire officiel → infrastructure `es-maint` → lots de traduction/relecture
(en parallèle une fois les deux prérequis livrés) → certification finale → `complete`.
Les dépendances précises et références de cartes sont dans [tickets.json](es/tickets.json).
Le statut `complete` est interdit avant résolution des alertes et justifications des
exceptions EN, contrôle des offsets manquants et des graphismes, builds déterministes,
tests ROM et parcours en émulateur, puis non-régression FR.

Règles à reprendre dans **chaque** ticket :

- `combined_*.txt` : éditions chirurgicales, dernière occurrence gagnante, jamais de
  régénération, tri ou sed global ; seule la création initiale décrite plus haut est autorisée.
- Toute ligne ajoutée ou modifiée : valeur exacte dans `protected_entries.yaml`, même commit.
- Validation : build de la langue + `make test-python` ; hash de la ROM FR inchangé.
- Commits français `type(scope): description`, hooks actifs ; aucun push ni pipeline distant.

## Non vérifié / limites

L’infrastructure, la relecture intégrale et les traductions sont les livrables des
tickets de suite. Aucune nouvelle UI n’est produite ici ; aucune validation visuelle
ni qualité linguistique exhaustive n’est revendiquée. Les mesures sont celles des
fichiers de référence, pas un taux de couverture garanti des textes visibles en jeu.

ROM FR témoin au début de l’audit :
`74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
À la reprise de session, le témoin local vaut
`c603198494cbee13c7e2ff8289763b9838644d11d50bf7c715c52bdf0360a7c4`.
Cette divergence avec le témoin initial est antérieure à la reprise ; elle interdit
de revendiquer une identité binaire sur toute la session précédente. Les trois
sources combined correspondent toujours exactement aux empreintes de l’inventaire.
Aucun code de production ni source de traduction n’est modifié par cet audit.
Les empreintes des ROMs source correspondent à `docs/roms_baseline.json`.
La vérification des tests, des hooks et du témoin FR est consignée dans la résolution
finale du ticket. Aucun changement aux sources FR, au Makefile ou aux descripteurs.

Le catalogue MCP annonce `kanban_create_ticket`, mais aucun outil kanban n’est
appelable dans cette session. Les cartes sont donc créées via
`orchestration_create_follow_up_ticket`. Les prérequis sont consignés dans chaque
description et dans `tickets.json` ; les arêtes automatiques `dependsOn` ne peuvent
pas être écrites avec cet outil et ne sont pas revendiquées comme configurées.
Ne pas lancer un lot tant que son glossaire et son infrastructure ne sont pas livrés.
