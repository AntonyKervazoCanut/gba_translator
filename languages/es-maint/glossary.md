# Glossaire et politique de localisation — es-maint

Référence D-849, 2026-10-29. Applicable aux **63 lots ES-001 à ES-063**
de `docs/analysis/es/lots.json`, à F-850 et à la certification T-914.
Prérequis réutilisé : audit A-663 intégré par `6988ec86`.

## Portée et autorité

La langue cible est **l’espagnol d’Espagne (es-ES)** : tutoiement courant,
`vosotros` au pluriel lorsque le registre le demande, ponctuation `¡…!` et `¿…?`,
accents sur les majuscules, `Pokémon` invariable. Préserver le registre de chaque
personnage ; ne pas ajouter d’argot régional, de références françaises ou de memes.
Les accents ne sont pas des caractères facultatifs pour gagner de la place.

Le mot « officiel » désigne la localisation des jeux Pokémon, **pas une
localisation officielle d’Unbound**. Le scénario et les mécaniques du hack restent
l’autorité sémantique : un nom officiel ne justifie jamais de remplacer un effet
modifié par l’effet du jeu commercial. Les traductions communautaires ES et FR
servent à la comparaison, jamais de source unique du scénario.

Ordre de décision : identifier l’entité EN par son ID et son contexte vivant →
appellation es-ES du jeu où elle existe → forme complète ci-dessous → variante
courte attestée ou décision de budget explicitement consignée. Pour les entités
postérieures à Platine, consulter la localisation es-ES de leur génération ; ne
pas les rétrotraduire depuis le français. Si plusieurs générations ont renommé
une entité, retenir le nom de la génération de référence de sa mécanique dans
Unbound et consigner cette exception dans le rapport du lot. À défaut de preuve,
conserver provisoirement le nom EN comme exception non certifiée, sans inventer
une appellation « officielle » ; T-914 doit résoudre ces exceptions.

Ce document fixe le vocabulaire commun et la procédure pour les milliers de noms,
pas une copie exhaustive des bases de données commerciales. Chaque lot fournit
pour les noms non listés : ID EN, nom ES exact, jeu/génération, URL ou écran de
référence et éventuelle forme courte. Les lots ne modifient pas ce glossaire partagé.

## Sources et générations

Sources consultées le 2026-10-29. Les liens sont des références de vocabulaire ;
leurs descriptions ne doivent pas être copiées en masse.

- **S1 — Nintendo, Pokémon X, version européenne espagnole, génération VI (2013)** :
  [manuel électronique CTR-P-EKJA-EUR_es](https://www.nintendo.com/eu/media/downloads/games_8/emanuals/nintendo_3ds_2/pok_mon_x/ElectronicManual_Nintendo3DS_PokemonX_es.pdf),
  rubrique 9 « Pantalla de combate », pages PDF 28–30 : PS, PP, mouvements,
  affaiblissement, Luchar, Bolsa, Huir, Pokémon. Rubrique 7 : menus.
  Ce manuel confirme les mots, **pas les six badges abrégés**.
- **S2 — Nintendo, guide espagnol de Pokémon Platine, génération IV (2009)** :
  [mouvements](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/ataques.html),
  [habilidades](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/habilidades.html),
  [objets de soin](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/objetos_medicinas.html).
  Référence des noms et des formes compactes historiques ; ne pas reproduire les
  coquilles rédactionnelles ou appliquer ses valeurs d’effets à CFRU.
- **S3 — The Pokémon Company, [Pokédex en espagnol](https://www.pokemon.com/el/pokedex)** :
  noms d’espèces, types et liens vers les fiches d’habilités. Catalogue web évolutif
  allant jusqu’à la génération IX à la consultation, sans numéro de version ROM.
  Ce n’est pas une preuve des abréviations GBA ni des mécaniques d’Unbound.
- **S4 — Pokémon Rubí/Zafiro, localisation espagnole, GBA, génération III (2003)** :
  lecture visuelle des six sprites de statut reproduits dans
  [la table comparative de WikiDex](https://www.wikidex.net/wiki/Estado#Sprites).
  Œuvre source : Nintendo/Creatures/GAME FREAK ; **hébergeur secondaire non officiel**.
  Les liens de fichiers et SHA-256 ci-dessous identifient exactement les reproductions
  lues. Ce contrôle porte sur les libellés des sprites, pas sur une ROM commerciale
  locale authentifiée ou un parcours en émulateur. Ne pas présenter WikiDex comme
  une publication Nintendo. Ni JCC ni ROM communautaire Unbound utilisés comme preuve.

- **S5 — The Pokémon Company, stratégie de Soleil/Lune, génération VII** :
  [Eevee et ses évolutions](https://www.pokemon.com/es/estrategia/evoluciona-tu-estrategia-con-eevee)
  confirme notamment Miedosa et Absorbe Elec ;
  [Pokémon singuliers, deuxième partie](https://www.pokemon.com/es/estrategia/lo-que-debes-saber-sobre-los-pokemon-singulares-de-las-distribuciones-2a-parte),
  contexte génération VI, confirme Miedosa, Modesta, Mansa, Alegre, Ingenua et
  Activa avec leurs effets. Ces exemples n’attestent pas les 25 noms à eux seuls.

## Statuts : décision pour F-850

| Clé du descripteur | EN | Forme ES | Badge (3 lettres) | Preuve |
|---|---|---|---|---|
| poison | poisoned | envenenado | ENV | S4, sprite Rubí/Zafiro |
| burn | burned | quemado | QUE | S4, sprite Rubí/Zafiro |
| freeze | frozen | congelado | CON | S4, sprite Rubí/Zafiro |
| paralysis | paralyzed | paralizado | PAR | S4, sprite Rubí/Zafiro |
| sleep | asleep | dormido | DOR | S4, sprite Rubí/Zafiro |
| faint | fainted | debilitado | **DEB** | S4, sprite Rubí/Zafiro ; sens confirmé S1 |

DEB est donc retenu, sans point ni quatrième caractère. Les six formes ont été
lues sur des reproductions des graphismes d’une localisation officielle de jeu
vidéo ; elles ne sont pas déduites des initiales ni des règles JCC. En dialogue,
accorder le participe au référent quand celui-ci est connu. `fainted` → `se ha
debilitado` selon le temps EN, jamais « muerto ». L’empoisonnement grave reste
`gravemente envenenado` ; le badge partagé ENV est une limite d’affichage, pas une
fusion des effets. La confusion n’est pas la congélation : réserver CON à frozen.
Ne pas importer `helado`/`somnoliento` de Légendes si la mécanique EN est freeze/sleep.

Reproductions S4 inspectées (fichiers originaux, pas miniatures) :

| État | Fichier | SHA-256 |
|---|---|---|
| Paralizado | [Paralizado_RZ.png](https://images.wikidexcdn.net/mwuploads/wikidex/d/d0/latest/20230313101134/Paralizado_RZ.png) | `1463ca4c99c384a0a08f7202c8e13a0ee5caeaf37ddab4e683fc4a9d846d9dd4` |
| Quemado | [Quemado_RZ.png](https://images.wikidexcdn.net/mwuploads/wikidex/7/79/latest/20230312213858/Quemado_RZ.png) | `5bd08a9b1a6cf95851f569c127c9a5a3bfe47f9b1a51ecd21f826a8da284b9c0` |
| Envenenado | [Envenenado_RZ.png](https://images.wikidexcdn.net/mwuploads/wikidex/f/f2/latest/20230313101104/Envenenado_RZ.png) | `1c876575ed37836db42e697d3286de303a9b54f46271b1657af868f8383b4014` |
| Dormido | [Dormido_RZ.png](https://images.wikidexcdn.net/mwuploads/wikidex/4/4a/latest/20230313101036/Dormido_RZ.png) | `63db2a5f12b16cf5e4d81102960017a974a3377fa68cd3830910a67f8ea294f5` |
| Congelado | [Congelado_RZ.png](https://images.wikidexcdn.net/mwuploads/wikidex/f/f8/latest/20230313100904/Congelado_RZ.png) | `44683862447e4bf3e08321dab15260f11777575e04de463bdd36ef6879f2a3aa` |
| Debilitado | [Debilitado_RZ.png](https://images.wikidexcdn.net/mwuploads/wikidex/5/51/latest/20230313100949/Debilitado_RZ.png) | `b92ff87325b0402061efa7c5dc0a73be21531a8e0e1521e3f8359fc0cf81e534` |

F-850 devra encore vérifier les badges **réellement rendus dans Unbound**, toutes
les polices et les six clés du descripteur. La vérification documentaire ne remplace
pas les assertions d’émulateur, ni une authentification binaire du jeu source.

## Noms d’espèces et formes (ES-060 à ES-063)

Conserver les noms es-ES officiels par ID national (S3) : Bulbasaur, Pikachu,
Charizard, etc. Ne pas utiliser les noms FR (`Dracaufeu`, `Évoli`) ou traduire les
étymologies (`Pikachu` ne devient pas un nom descriptif). Préserver chiffres,
traits d’union, points, accents et symboles des noms concernés : Nidoran♀/Nidoran♂,
Mr. Mime, Mime Jr., Porygon-Z, Flabébé, Type: Null → **Código Cero**.
La capitalisation de la table est une convention d’interface ; elle ne change pas
le nom. Distinguer espèce, surnom du joueur, forme régionale et identifiant interne.

Les 1 261 cellules auditées incluent des formes et entrées internes ; ne pas les
traiter comme 1 261 espèces officielles distinctes. Pour une forme propre au hack,
conserver le nom d’espèce officiel et le qualificatif EN du hack tant qu’aucun
équivalent n’est documenté. Aucun raccourci nouveau d’espèce autorisé : si le nom
ne tient pas, résoudre le budget avec l’infrastructure et vérifier tous les usages.

## Types

Appellations es-ES ; Bicho est retenu (usage du jeu vidéo S2), et non le libellé
web « Insecto » que peut afficher S3. Cette différence de support est explicite.

| EN | ES | EN | ES | EN | ES |
|---|---|---|---|---|---|
| Normal | Normal | Fire | Fuego | Water | Agua |
| Grass | Planta | Electric | Eléctrico | Ice | Hielo |
| Fighting | Lucha | Poison | Veneno | Ground | Tierra |
| Flying | Volador | Psychic | Psíquico | Bug | Bicho |
| Rock | Roca | Ghost | Fantasma | Dragon | Dragón |
| Dark | Siniestro | Steel | Acero | Fairy | Hada |

Pas de `Hierba`, `Oscuro`, `Insecto` ou `Tierra` pour Rock. Les formes complètes
restent prioritaires dans les badges. Pas de sigles inventés pour les types ; un
budget graphique insuffisant est un problème d’infrastructure.

## Mouvements, habilités et objets

Le terme générique est **movimiento** (move), **habilidad** (ability), **objeto**
(item). `Ataque` reste le nom de la statistique Attack et le verbe d’action selon
la phrase. Jamais `talento` calqué sur le français. Tables de départ : S2 ; pour
les générations suivantes, vérifier le jeu es-ES correspondant avant import.

| EN / identité | Nom ES de référence | Variante compacte | Statut |
|---|---|---|---|
| Quick Attack | Ataque Rápido | At. Rápido | compacte attestée S2, gen IV |
| Acid Armor | Armadura Ácida | Armad. Ácida | compacte attestée S2, gen IV |
| Thunderbolt | Rayo | identique | S2, gen IV |
| Flamethrower | Lanzallamas | identique | S2, gen IV |
| Ice Beam | Rayo Hielo | identique | S2, gen IV |
| Surf | Surf | identique | S2, gen IV |
| Water Absorb | Absorbe Agua | Absor. Agua | compacte S2, gen IV |
| Volt Absorb | Absorbe Elec | Absor. Elec. | compacte S2, gen IV |
| Battle Armor | Armadura Batalla | Armad. Bat. | compacte S2, gen IV |
| Static | Electricidad Estática | Elec. Estát. | compacte S2, gen IV |
| Overgrow | Espesura | identique | S2, gen IV |
| Blaze | Mar Llamas | identique | S2, gen IV |
| Torrent | Torrente | identique | S2, gen IV |
| Potion | Poción | identique | nom es-ES, soin |
| Antidote | Antídoto | identique | S2, gen IV |
| Burn Heal | Antiquemar | identique | S2, gen IV |
| Ice Heal | Antihielo | identique | S2, gen IV |
| Paralyze Heal | Antiparalizador | Antiparaliz | compacte S2, gen IV |
| Full Heal | Cura Total | identique | S2, gen IV |
| Awakening | Despertar | identique | S2, gen IV |
| Rare Candy | Caramelo Raro | Carameloraro | compacte historique S2, gen IV |

Les formes complètes développées à partir des formes compactes ne sont pas une
preuve de leur présence dans l’UI de Platine. Elles constituent la forme rédactionnelle
retenue ici ; la forme compacte S2 est la référence attestée pour une cellule étroite.
Une variante « identique » n’est pas une garantie de place. Préserver les distinctions
Full Heal / Full Restore, Potion / Super Potion et objet / habilité Antídoto.
`Poké Ball`, `Super Ball`, `Ultra Ball`, `Master Ball`, `MT`, `MO`, `Baya` sont les
termes retenus. Ne pas traduire Poké Ball par « bola » dans un nom d’objet.
Les objets et habilités exclusifs au hack gardent leur nom EN en attendant une
entrée d’exception argumentée ; décrire fidèlement leur effet CFRU.

## Natures

Table de correspondance es-ES de la série principale depuis la génération III.
S5 confirme les cas compétitifs cités ; la table complète est la référence
normative du projet, à contrôler par ID dans le jeu lors de son injection. Ne pas déduire les noms d’un adjectif EN
ou FR. Vérifier l’ID de nature, pas la position d’une liste alphabétique. Une menthe
ou un mécanisme du hack peut modifier les statistiques sans changer la nature affichée.

| EN | ES | EN | ES |
|---|---|---|---|
| Hardy | Fuerte | Lonely | Huraña |
| Brave | Audaz | Adamant | Firme |
| Naughty | Pícara | Bold | Osada |
| Docile | Dócil | Relaxed | Plácida |
| Impish | Agitada | Lax | Floja |
| Timid | Miedosa | Hasty | Activa |
| Serious | Seria | Jolly | Alegre |
| Naive | Ingenua | Modest | Modesta |
| Mild | Afable | Quiet | Mansa |
| Bashful | Tímida | Rash | Alocada |
| Calm | Serena | Gentle | Amable |
| Sassy | Grosera | Careful | Cauta |
| Quirky | Rara | — | — |

Aucune forme courte nouvelle : la plus longue fait 7 lettres. Attention à
**Timid → Miedosa**, **Bashful → Tímida**, **Quiet → Mansa**. Ces trois faux amis
sont des critères bloquants de revue. Le lot consigne un écran du jeu es-ES choisi
pour toute divergence ; S1/S2 ne constituent pas une liste sourcée des 25 natures.

## Statistiques, combat, menus et Pokédex

Formes rédactionnelles retenues ; les compactes marquées « projet » sont des
choix de budget du hack, pas des appellations prétendument officielles.

| EN / contexte | ES complet | Compact autorisé | Provenance / règle |
|---|---|---|---|
| HP | puntos de salud | PS | S1, gen VI |
| PP | puntos de poder | PP | S1, gen VI |
| Attack | Ataque | At. | projet ; préserver distinction avec mouvement |
| Defense | Defensa | Def. | projet |
| Sp. Atk | Ataque Especial | At. Esp. | S2, gen IV |
| Sp. Def | Defensa Especial | Def. Esp. | projet |
| Speed | Velocidad | Vel. | projet |
| Accuracy | Precisión | Precis. | projet |
| Evasion | Evasión | Evas. | projet |
| Level | Nivel | Nv. | projet ; vérifier aussi le glyphe runtime |
| Experience | experiencia | Exp. | projet ; S1 confirme le terme complet |
| Fight / Bag / Run | Luchar / Bolsa / Huir | identiques | S1, gen VI |
| Pokémon / Pokédex | Pokémon / Pokédex | identiques | S1 / S3 |
| Save / Options / Exit | Guardar / Opciones / Salir | identiques | lexique de projet |
| Yes / No / Cancel | Sí / No / Cancelar | identiques | lexique de projet |
| Summary / Switch | Datos / Cambiar | identiques | lexique de projet, selon action réelle |
| Use / Give / Toss | Usar / Dar / Tirar | identiques | lexique de projet, selon action réelle |
| Move (PC action) | Mover | identique | ne pas traduire par Movimiento |
| Move (combat data) | Movimiento | Mov. | compacte de projet |
| Seen / Caught | Vistos / Atrapados | identiques | compteurs Pokédex, choix de projet |
| Height / Weight | Altura / Peso | identiques | S3 |
| Species / Category | Especie / Categoría | identiques | selon intitulé EN réel |
| Trainer / Gym / Badge | Entrenador / Gimnasio / Medalla | identiques | lexique de projet |
| Missions / Cube | Misiones / Cubo | identiques | interface propre au hack |

ES-059 : identifier les 279 **catégories** par l’espèce référente ; ne pas traduire
littéralement le nom EN si la catégorie es-ES existe. Exemple S3 : Bulbasaur →
`Semilla` ; ne pas confondre catégorie et type Planta. Respecter l’ajout runtime de
« Pokémon » : ne pas l’écrire deux fois. Pour un texte Pokédex modifié par Unbound,
traduire le texte EN du hack, sans lui substituer une notice d’un autre jeu.
Unités métriques, virgule décimale dans la prose espagnole ; ne pas réécrire un
nombre ou un format contrôlé par le moteur sans vérifier ses arguments.

## Noms propres d’Unbound — décisions du hack

**Choix stable : conserver les noms propres EN du hack**, traduire seulement leurs
désignateurs génériques. Cette règle vaut dans les dialogues, panneaux, carte,
missions, menus et tables de noms : aucune adaptation phonétique ou traduction
étymologique improvisée. Ce ne sont pas des noms officiels Pokémon espagnols.

| EN | Forme es-maint | Nature de la décision |
|---|---|---|
| Borrius | Borrius | région inchangée |
| Frozen Heights | Frozen Heights | nom composé conservé, pas « Alturas Heladas » |
| Bellin Town | Pueblo Bellin | désignateur traduit |
| Dresco Town | Pueblo Dresco | désignateur traduit |
| Crater Town | Pueblo Crater | pas d’accent ajouté au nom propre Crater |
| Fallshore City | Ciudad Fallshore | pas « Cascada » |
| Dehara City | Ciudad Dehara | nom inchangé |
| Mt. Thundercap | Monte Thundercap | pas de reprise du toponyme FR |
| Route + numéro | Ruta + numéro | conserver numéro et destination |
| KBT Expressway | Autovía KBT | sigle intact |
| SES Expressway | Autovía SES | distinct de KBT |
| Professor Log | Profesor Log | titre traduit, nom conservé |
| Jax, Marlon, Zeph, Skeli | Jax, Marlon, Zeph, Skeli | noms conservés |
| Shadows (faction) | Shadows | nom de faction conservé ; ombres ordinaires → sombras |
| Light of Ruin (faction) | Light of Ruin | ne pas confondre avec un mouvement officiel |

Pour tout autre nom : conserver exactement le noyau EN ; Town → Pueblo,
City → Ciudad, Mountain/Mt. → Monte, Forest → Bosque, Cave → Cueva,
Island → Isla, Lake → Lago si ces mots sont des désignateurs séparables.
Un nom composé indivisible (comme Frozen Heights) reste intégralement EN.
Les personnages et lieux **empruntés à un jeu officiel** utilisent en revanche
leur nom es-ES attesté (ex. Kanto, Professor Oak → Profesor Oak), avec preuve
par identité ; ne pas rebaptiser un homonyme original d’Unbound par analogie.
Les noms du joueur et surnoms restent des buffers, jamais un texte littéral.

Exceptions du hack : `Cubo`, `Misiones`, désignateurs ci-dessus, noms de factions
conservés et compactes marquées projet. Aucun autre régionalisme ou renommage
communautaire n’est implicitement autorisé. Un nom trop long exige une décision
centralisée documentée, pas un second nom concurrent dans un lot.

## Fidélité au scénario et termes interdits

Revoir aussi les textes ES différents d’EN, pas seulement les égalités de l’audit.

| Offset audité | Prescription pour le lot |
|---|---|
| 0x0018D43D | Rétablir la scène EN des quatre garçons devant la télévision ; supprimer la publicité YOSOYKIKE étrangère au dialogue. |
| 0x0018D53B | Rétablir la notice EN ; supprimer l’annonce datée du 24 décembre 2024. |
| 0x00190687 | Retrouver la chaîne EN vivante complète avant de traduire ; ne pas conserver « EEjust don't know... » comme début de phrase. |
| 0x00196A82 | Corriger « esta máquinas » en « estas máquinas » seulement après confirmation du référent et du budget. |
| 0x0018D3F8 | Identifier le vrai code de ponctuation et la police ; ne pas remplacer globalement `<0x52>`. |

Conserver les crédits légitimes du hack à leur emplacement réel. Aucune publicité,
URL communautaire, nouvelle date, blague de traducteur ou message promotionnel ne
remplace une notice ou un dialogue EN. Ne pas inventer des événements pour rendre
une phrase tronquée plausible. Respecter négations, modalités, temps, protagonistes,
conditions de mission, quantités et récompenses.

Interdits terminologiques : `talento` pour ability ; HP/PV pour PS en texte ES ;
BRN/FRZ/SLP/PSN/FNT pour les six badges localisés ; « muerto », « KO » ou
« fuera de combate » comme remplacement systématique de fainted ; `Hierba` pour
le type Grass ; `Oscuro` pour Dark ; noms d’espèces FR ; faux amis de natures
ci-dessus ; `guardar` pour conserver un objet quand l’action est une sauvegarde
ou inversement ; `Movimiento` pour le bouton PC Mover. Les mots restent permis
lorsque leur sens ordinaire est réellement celui de la phrase EN.

## Repères de cellules et choix des compactes

Repères du code actuel (`src/core/fixed_tables.py`, patches FR `move_names.py`
et `ability_names.py`) ; F-850 doit confirmer la table **vivante EN** avant emploi.
Ce sont des limites en octets, pas une autorisation de copier les patches FR.

| Surface | Cellule connue | Charge utile maximale hors terminateur | Exemple de choix |
|---|---:|---:|---|
| Espèce | 11 octets | 10 | `Código Cero` compte 11 caractères encodables : ne tient pas dans cette cellule ; adaptation technique requise, pas de nom inventé. |
| Mouvement | 13 octets | 12 | `Ataque Rápido` = 13 caractères ; `At. Rápido` = 10 : préférer la compacte attestée. |
| Habilité | 17 octets | 16 | `Electricidad Estática` = 21 caractères ; `Elec. Estát.` = 12 : compacte attestée. |
| Badge statut | 3 lettres dessinées | dépend du sprite | `DEB` est un graphisme à vérifier, pas une cellule texte supposée de 3 octets. |

Les comptages des exemples sont des repères textuels pour des glyphes simples ;
le lot mesure encore les octets du profil ES et la largeur rendue. Aucune limite
d’objet, menu, lieu ou catégorie Pokédex n’est déduite de ces trois tables.
Une même compacte doit être utilisée dans tous les consommateurs de la même table ;
le dialogue peut employer le nom complet si son propre budget le permet.

## Budgets et critères de revue par lot

1. Utiliser la liste exacte du lot, jamais sa plage d’adresses ni `--skip-existing`.
   Pour chaque offset : traduit/importé, conservé avec justification, ou exclu
   comme non textuel avec preuve. Identifier ID, référents et zone par les scripts.
2. Lire l’EN au **pointeur vivant**, contrôler l’alignement ES par l’offset map.
   Une absence EN ou une donnée de police n’autorise pas une traduction depuis FR.
3. Appliquer le nom complet ; ne choisir une compacte que si nécessaire au budget.
   Mesurer avec le profil ES réel : octets encodés **plus 0xFF**, stride/voisins des
   cellules fixes, largeur en pixels avec la police effective, lignes et pagination.
   Les nombres de caractères seuls ne prouvent rien. Ne pas couper un nom à l’aveugle.
4. Préserver les commandes FC/FD/F8/F9/F7 avec **tous leurs arguments**, ordre des
   buffers, couleurs et contrôles FA/FB. Un argument décodé comme lettre n’est pas
   du texte. Ne pas permuter les placeholders pour calquer la syntaxe espagnole.
5. Éditer chirurgicalement la dernière occurrence gagnante du combined es-maint ;
   conserver doublons, ordre et encodage. Chaque valeur ajoutée/modifiée doit être
   exactement protégée dans `protected_entries.yaml`, **dans le même commit**.
   Aucune régénération, tri ou substitution globale ; ne jamais toucher ES référence/FR.
6. Vérifier fidélité EN, cohérence de tous les usages du nom, accords, accents,
   `ñ/ü/¡/¿`, variantes de genre et buffers longs. Consigner source et génération,
   compacte retenue, budget mesuré, pointeur et résultat de décodage ROM par entrée.
7. Après F-850 : `make build-es-maint`, `make test-python`, contrôles disponibles
   d’intégrité et de ROM, lecture des octets aux pointeurs vivants. Vérifier que
   les entrées ne sont ni ignorées, ni remplacées par fallback EN.
8. Toute modification d’affichage nécessite assertions Playwright headless en
   émulateur puis capture attachée au ticket ; ne jamais sauvegarder en jeu.
   Comparer le témoin FR avant/après sur les mêmes sources et paramètres.
   Commits français `type(scope): description`, hooks actifs ; aucun push ni
   déclenchement de pipeline distant.

Rejet bloquant : scénario altéré, nom inventé présenté comme officiel, statut
incohérent, perte de commande/argument, dépassement, fallback non justifié,
protection absente ou offset non traité. Les exceptions non certifiées doivent
être visibles dans le rapport et résolues avant T-914 ; un build vert seul ne
certifie pas la traduction.

## Validation de ce livrable documentaire

Aucun descripteur ni combined créé ici. Le build attend **F-850**, qui dépend de
ce glossaire : `make build-es-maint` retourne actuellement « No rule to make
target ». Aucun texte ROM, code, police ou source ES/FR n’est modifié ; aucun
nouvel affichage n’est produit. Les contrôles d’octets/pointeurs, budgets réels et
preuves Playwright des futurs textes appartiennent à l’infrastructure et aux lots.
Les résultats locaux, empreintes témoins et limites de vérification sont consignés
dans la résolution D-849. Ne pas interpréter ce document comme une certification
complète de es-maint.
