# ES-011 — 374 décisions contractuelles

F-861, après revue du routage F-1041 (`c4dc8c3f`) et des prérequis terminés
D-849/F-850. Le relevé de préparation reste une préimage historique, pas une
certification. Le traitement final est dans [011_TRAITEMENT.json](011_TRAITEMENT.json).

## Traduction et conservation

| Décision | Nombre |
|---|---:|
| Traduit ou corrigé depuis la ROM EN canonique | 297 |
| Nom ou libellé identique conservé et injecté | 5 |
| Doublon canonique, injecté par sa clé contractuelle | 4 |
| Ancien crédit conservé, sans injection | 60 |
| Texte conservé faute de lecteur identifié | 4 |
| Donnée binaire exclue | 4 |
| Total | 374 |

Les 302 valeurs ont leurs protections exactes. Elles sont ajoutées à la fin du
combined, sans réécrire les anciennes lignes, leurs doublons ou leurs fins de ligne.
Les cinq valeurs identiques sont BILL (deux occurrences), FUJI, Pokémon et
Pokémon2 (catégorie technique). Elles ne sont pas comptées comme traductions.
Aucun offset d'un autre lot n'est ajouté ni changé. Aucun combined EN, ES référence
ou FR, glossaire, lots.json, code partagé ou statut de langue n'est modifié.

Les 90 notices Pokédex sont retraduites depuis la ROM EN vivante : le corpus
historique contient des notices françaises et l'ES décrit souvent une autre version.
Les caractéristiques EN sont conservées, y compris la queue fourrée de Wartortle,
les durées, quantités, conditions, négations et noms scientifiques. Les unités
rédactionnelles sont métriques : dix onces liquides sont arrondies à environ 300 ml et
mille pieds à environ 300 m. Les noms d'espèces restent identiques. Les tutoriels
emploient MT, Hidropulso, Recurrente et Puño Certero ; le nom EN Poké Dude est
conservé, sans adaptation présentée comme officielle. Les événements deviennent
Regalo Misterioso, tarjetas/noticias misteriosas et sellos, sans publicité.

## Référents et limites d'attribution

Les 302 valeurs atteignent 376 sites recensés dans la ROM. Le rapport donne les
préimages, sites, tables et consommateurs sélectionnés, sans attribuer une carte
à partir de l'adresse du texte. Les surfaces sont les tutoriels Teachy TV/Poké
Dude, Pokémon Jump, Dodrio Berry Picking, Berry Crush, la pêche, les catégories
Easy Chat, échanges, reproduction, apprentissage de mouvements, communications,
Regalo Misterioso, clavier et 90 notices de la table Pokédex de stride 36.
La table est `0x1A357CC`, champ description à `+0x10`, stride 36. Le littéral
`0x105D44` charge sa racine ; les instructions `0x105CDC–0x105CE8` calculent
l'index × 36 et lisent la description. Le premier pointeur sélectionné est
`0x1A357DC` (notice inconnue, ID 0), puis `0x1A35800` (Bulbasaur, ID 1).

Les correspondances ES sont vérifiées à la cible textuelle vivante, via l'offset
map et les pointeurs homologues EN/ES. Vingt et une absences de map sont
reconstruites par ces pointeurs et leurs préimages, jamais depuis le français.
Pour les alias, la map est consultée à la cible vivante, pas au préfixe nul.

Les quatre paires actives utilisent seulement les clés contractuelles `41CE3B`,
`41CEA7`, `41CF13`, `41CF4F`. Les clés `41CE3C`, `41CEA8`, `41CF14`, `41CF50`
sont des doublons documentés, sans seconde saisie. Les deux clés `41DC45` et
`41DC48` appartiennent aux crédits historiques exclus. Les 60 anciens crédits
restent intacts : l'ancienne table `0x4145BC` est remplacée par `0x1FB0DB0` et
le script `0x1FB12D8`, comme établi par F-1041. Noms, lignes vides et FC13 ne
sont pas modifiés. Les occurrences binaires ne sont pas toutes des lecteurs actifs.

`41CC7B`, `41D195`, `41E2EC`, `41E76B` sont conservés sans injection : aucun
pointeur direct ni route active retrouvé. Cela ne démontre pas leur inaccessibilité
dynamique. Un balayage du corps complet et de ses limites ne trouve aucun
lecteur intérieur. À `41E76B`, le lecteur suivant `0x1430F8` cible
`0x41E794` (« Communicating... »), hors contrat ; ce voisin reste intact.
`41CC7B` est distinct du SAVING vivant `41CC42` ; `41E2EC` est une
variante B/Cancel distincte du Cancel vivant `41E0B9`.
`41EFB8`, `41F0A8`, `41F0BD`, `41F160` sont des motifs binaires sans
texte intelligible ni consommateur textuel identifié ; aucune phrase n'est inventée.

## Insertion, commandes et budgets

Les quinze alias réutilisent TextAliases. Les 287 autres valeurs réutilisent le
contrat existant SystemTextRoutes, par ajout de données propres à es-maint :
préimage complète, références exhaustives, refus de fallback et de troncature,
conservation des commandes et de la mise en page. Aucun second réinserteur ni
correctif de code partagé. Les anciennes entrées du manifeste sont préservées.

Cette déclaration est nécessaire : le normaliseur générique remanierait certains
textes paginés comme des blocs plein écran. La garde exécute le vrai normaliseur
sur les 302 valeurs et exige l'identité de chaque page relue. Elle compare les
séquences FC/FD/F8/F9/F7 avec tous leurs arguments et l'ordre des buffers, ainsi
que FA/FB. Le plafond 512 inclut le terminateur FF. Les lignes souples sont adaptées
au texte espagnol ; aucune commande structurelle n'est ajoutée ou supprimée.

Les budgets des alias sont ceux des fenêtres/routines gardées par F-1041.
`41CF13` tient maintenant sur deux lignes, corrigeant la disposition EN native
sur trois lignes dans une fenêtre de deux. Le suffixe « times » devient « v. »
avec son espace initial, variante de budget de 32 px, distincte du rythme
« veces/s ». GHOST devient FANTASMA aux trois consommateurs, comparaison et
surnom compris ; le surnom respecte dix octets utiles maximum.

Les prix F7 ont des réserves explicites : 108 px / 18 octets pour le nom
d’objet, 30 px / 5 octets pour la quantité, tampon expansé borné à 256 octets pour Jump et 64 pour Dodrio.
Le prix Dodrio utilise la police 0 (`0x1555512`), distincte de celle de Jump.
Le message Pokémon Jump est borné à 176 px sur deux lignes ; les instructions
`0x14A4E6–0x14A50C` confirment la fenêtre 22 × 4 tuiles et la police 2, et
`0x14A4C8–0x14A4E2` les variables F7. Leur préimage de code est gardée.
Les autres textes FD sont aussi contrôlés avec douze lettres larges par buffer
(72 px), avec des ruptures dédiées aux échanges et à l’apprentissage.
Le fragment BERRY devient « Baya {buffer} », en conservant sa commande et
les espaces textuels sans toucher au préfixe nul.

Les notices restent sur trois lignes sans pagination, 232 px maximum. Les
textes système ont une garde conservatrice de 208 px par ligne (176 pour les
titres Berry Crush, 88 pour les catégories Easy Chat). Ces plafonds ne sont pas
présentés comme une reconstitution exhaustive des fenêtres de chaque menu ;
les mesures natives utilisent la police normale et une mire RAM contrôlée.

## Reproduction des contrôles

L'extraction EN locale a été reconstruite depuis la ROM canonique de SHA-256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Le cache du checkout principal n'a pas été modifié. Les caches non liés au hash
de ROM restent une limite préexistante du driver, pas une nouvelle garantie.

```sh
make build-es-maint BUILD_NUMBER=0
make test-python
python3 -m pytest -q tests/unit/test_es011_translation.py -m rom
python3 -m pytest -q tests/e2e/es/test_es011_translation_pipeline.py -m rom
python3 tests/e2e-playwright/fixtures/prepare_es011_production.py
ES011_PRODUCTION=1 npx playwright test -c tests/e2e-playwright/es011.config.ts
ES_NATIVE_REPORT=output/reports/es011-native.json ES_NATIVE_COUNT=244 \
 ES_NATIVE_KEYS=0x41CB63,0x41CC42,0x41CF13,0x41D18D,0x41DF05,0x41DFE6,0x41E0C0,0x41E3A8,0x41EDBD,0x41E823,0x444CB2,0x445D35 \
 ES_NATIVE_OCR_WORDS=Pokésalto,Oddium,Wanderus \
 ES_NATIVE_LABEL=ES-011 ES_NATIVE_PROOF=f861-es011-proof.png \
 ES_NATIVE_METRICS=output/reports/es011-native-widths.json \
 npx playwright test -c tests/e2e-playwright/es012.config.ts
```

La seconde sonde réutilise le test ES-012 par paramètres optionnels ; son
comportement ES-012 par défaut est conservé. Les 244 chaînes sans commandes
sont lues aux vrais pointeurs et mesurées par GetStringWidth ; douze sont
imprimées par le moteur et relues par OCR. L'analyse OCR recadre les traits
noirs sans l'ombre grise et lit aussi la vue originale ; un résultat doit
reconnaître le paragraphe entier dans l'ordre, sans recomposer des lettres entre
les vues. Un lexique OCR explicite couvre Pokésalto et les noms scientifiques EN
Oddium/Wanderus ; les octets ont leur garde indépendante. Les captures publiées
restent les PNG natifs intacts.
La mesure choisit un site de table aligné, tandis que les contrôles binaires
conservent aussi tous les opérandes de scripts non alignés. Le test des alias vérifie leurs 18
lecteurs et sept impressions, commandes, préfixes et racines des crédits.
Les captures suivent les assertions, restent hors dépôt et sont jointes au ticket.
Aucune sauvegarde en jeu, aucun texte sentinelle dans la production.

Le test du pipeline isolé utilise un combined temporaire limité aux 302 valeurs,
le vrai CSV, JSON, builder et patches. Il compare intégralement les ROMs à un
témoin portant les mêmes patches, en n'autorisant que les sites et allocations
sélectionnés. Le test de ROM finale contrôle aussi les 72 décisions sans seconde
saisie et les préfixes des alias. Les résultats d'exécution sont consignés dans
la résolution du ticket ; cette section décrit les assertions, pas leur succès.

## Non vérifié

Parcours naturels complets des minijeux, du combat GHOST, des échanges et de
toutes les notices ; accessibilité naturelle des tutoriels hérités ; expansion
exhaustive des buffers en situation ; fenêtres et polices effectives de chaque
menu système hors contrats gardés des alias. Les 58 textes portant des commandes
n'ont pas tous une impression complète individuelle ; commandes et arguments
ont des contrôles binaires distincts. Les quatre textes sans lecteur identifié
restent conservés, sans certification d'inaccessibilité. Certification globale,
statut complete et artefacts de distribution restent réservés à T-914.
Aucun push ni déclenchement de pipeline distant.

Repère de lecture du code historique, recoupé contre les instructions ROM :
[PrintPrizeMessage dans pokefirered](https://github.com/pret/pokefirered/blob/master/src/pokemon_jump.c).
La ROM actuelle reste l’autorité ; aucune accessibilité naturelle n’est déduite du dépôt.
