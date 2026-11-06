# Hindi romanisé — référence HI-LATIN-1

Version **1.1.0**, 6 novembre 2026, extension HI-02 de D-692, suite de [A-665](audit_langue_indie.md).
La version 1.1.0 ajoute les termes de HI-02 sans changer les graphies 1.0.0.
Les noms de modes de liaison, classes Agent/Idol/ACE TRAINER/Nurse/Skier et
formes électroménagères de Rotom sont conservés comme libellés EN éditoriaux.

Applicable à **HI-01 à HI-64**, code technique `indie`. Cette convention éditoriale
unique prime sur les anciennes seeds ; elle ne revendique aucune homologation.
Le [glossaire machine versionné](../../languages/indie/data/glossary_v1.json)
contient les entrées EN → HI, leur domaine, forme courte et provenance. Il n'est
pas injecté automatiquement dans le jeu. Aucun `combined_*`, manifeste de
protection, patch, police ou rendu n'est modifié par ce ticket.

## Sources et niveau de preuve

Consultation le 29 octobre 2026. Les identifiants ci-dessous sont ceux du JSON.

| Identifiant | Source primaire | Ce qu'elle établit ; limites |
|---|---|---|
| official-names | [Pokémon India, annonce du 25/09/2025](https://in.portal-pokemon.com/topics/pokemon_names_unified_across_india/) | Les noms hindi des Pokémon sont alignés sur leurs noms anglais. Cela ne localise pas les villes d'Unbound. |
| official-go | [Pokémon GO, lancement hindi, septembre 2023](https://pokemongo.com/news/hindi-availability-september-2023) | Une localisation officielle hindi existe. La page consultée en anglais ne fournit pas un lexique HI romanisé des mécaniques GBA. |
| official-types | [Pokédex officiel](https://www.pokemon.com/pokedex/) | Référence des 18 noms de types EN. Les équivalents HI du JSON sont nos choix. |
| official-stats | [Pokédex officiel indien, Pikachu](https://in.portal-pokemon.com/pokedex/0025/) | Six statistiques EN, Electric et Static ; ne prouve pas leurs traductions hindi. |
| ala-lc | [Library of Congress, table hindi 2025](https://www.loc.gov/catdir/cpso/romanization/hindi.pdf) | Référence bibliographique utilisant notamment des diacritiques. Notre romanisation simplifiée n'est pas ALA-LC. |
| live-en | `languages/en/combined_en.txt` et ROM EN locale | Référence du sens et des noms propres du fan-game, pas une publication officielle Pokémon. Snapshot SHA-256 dans le JSON. |

Les recherches sur les sites officiels Pokémon, Pokémon India et Pokémon GO
n'ont pas fourni de glossaire complet et vérifiable HI romanisé pour Unbound.
Cela **ne prouve pas l'absence** de termes officiels dans leurs applications ou
doublages. Aucun équivalent hindi de ce livrable n'est étiqueté « officiel ».
`source` atteste l'ancrage EN ou le contexte ; `status: editorial-hi` distingue
une traduction du projet, `editorial-retained-en` une conservation décidée par le
projet. Un mot EN attesté officiellement reste un **choix éditorial** lorsqu'on
le conserve dans une phrase hindi. Pas de transposition des règles du JCC ou de
GO vers celles d'Unbound. Pour un terme nouvellement attesté : conserver URL,
date, produit, langue, libellé exact et contexte avant de réviser la référence.

Le commentaire historique « Hunterian » de `combined_indie.txt` explique
l'intention de romaniser ; il ne valide ni conformité ni norme. **Ne pas le citer
comme autorité.** HI-LATIN-1 est une convention de lecture pratique et avec perte,
non une translittération réversible ou scientifique.

## Écriture et grammaire communes

- Texte nouveau : lettres `A-Z a-z`, chiffres, espace simple, ponctuation
  `. , ! ? ' - ( ) : /` si nécessaire et contrôlée par le codec. Pas de
  devanagari, macrons, points souscrits, guillemets typographiques ou espace
  insécable. ASCII dans le fichier ne signifie pas ASCII dans la ROM : encoder
  avec `TextEncoder.encode_pokemon`, alphabet CFRU.
- Voyelles : `a i u` brèves, `aa` longue, `ee` longue, `oo` longue ; `e o ai au`.
  Écrire `bataa`, `rahaa`, `jeet`, `door`.
  Exceptions lexicales fermées, pour la lisibilité : `ki`, `bhi`, `hi`, `ji`,
  finales longues `-i` (`paani`, `bijli`, `saathi`, `gayi`, `-ungi`), `nahin`.
  Ne pas alterner `paani/paanee`, `hoon/hun`, `nahin/nahi` entre lots.
- Nasalisation : `main` (je), `mein` (dans), `hain`, `hoon`, `haan`, `nahin`,
  `tumhein`, `vahaan` ; `Maa` (mère) est une exception lexicale sans `n`. Pas de tilde. Consonnes aspirées : `kh gh ch chh j jh
  th dh ph bh` ; `sh` pour les deux sifflantes savantes, `v` par défaut,
  `y` pour la semi-voyelle. `t d n` sans distinction rétroflexe, `ri` pour la
  voyelle syllabique. Retirer le schwa final non prononcé (`naam`, `dost`).
  Les noms propres conservés restent orthographiés EN, sans ces substitutions.
- Négation : `nahin` dans une assertion ; `mat` dans une interdiction ; `na`
  uniquement dans une construction idiomatique identifiée, pas pour gagner des
  octets. `Abhi tak nahin!` = pas encore ; `Vahaan mat jaao!` = n'y va pas.
- Tutoiement de référence : `tum`, accord `ho`, possessifs
  `tumhaaraa/tumhaari/tumhaare`. Impératifs : `jaao`, `dekho`, `chuno`, `karo`.
  Pas d'alternance gratuite avec `tu` ou `aap`. Un registre honorifique essentiel
  à une scène exige une justification dans l'inventaire du lot, sans changer la
  convention globale. Les boutons du glossaire priment sur la prose.
- Genre : accorder au référent connu, pas au sexe supposé du joueur. `Main ...
  rahaa hoon` masculin / `Main ... rahi hoon` féminin. Pour un joueur variable,
  reformuler sans accord variable : `Tumne mujhe haraa diyaa.` ou `Tumhaari jeet
  hui.` (`jeet` féminin). Ne pas ajouter un masculin absent de la source.
  Une forme du glossaire comme `Hichkichaa gayaa` est une base à accorder, pas
  un message prêt à injecter pour tous les sujets.
- Pluriel : noms hindi selon leur fonction (`ladkaa/ladke/ladkon`), accord
  `hai/hain` ; après un nombre, pas de `-s` anglais ajouté. Les noms d'espèces et
  les noms EN conservés sont invariants : `do Pikachu`, `teen Potion`.
  Après postposition, adapter les seuls mots hindi. Les noms EN variables ne
  doivent pas provoquer de variantes ad hoc dans chaque lot.
- Ton : hindi parlé clair, sans caricature ni mélange gratuit. Les emprunts
  techniques fixés au glossaire sont autorisés. Traduire le sens EN vivant,
  jamais une traduction FR intermédiaire.

## Terminologie et portée

Les domaines du JSON sont types, statuts, statistiques, menus, combat, objets,
attaques, talents, narration. Une clé est **(domaine, EN)** : `menus/Move` =
`Khiskaao` (déplacer), `combat/move` = `Chaal` (capacité de combat), `Attack` =
`Hamlaa` (statistique), `Ability` = `Kshamtaa` (talent). Une attaque de statut
reste une `Chaal` ; ne pas appeler tout mouvement une attaque infligeant des dégâts.
`Ground/Zameen` et `Rock/Chattaan`, `poisoned/Zahar lagaa` et `Poison/Zahar`,
`fainted/Behosh` et `asleep/Neend` restent distincts. « Fainted » ne signifie pas mort.

**Politique exhaustive des noms** : conserver les noms EN de chaque espèce,
personnage, faction et toponyme, même non présent dans le JSON (Borrius, Dresco
Town, Frozen Heights, Shadows...). Conserver aussi les noms d'objets, attaques et
talents EN, y compris ceux non listés ; traduire leur catégorie et leur description.
Les exemples Tackle, Surf, Static, Potion ne constituent pas une liste exhaustive
ni une permission de traduire autrement les noms absents. Garder TM/HM et les
numéros, HP/PP, PC, ID. Les noms `Pokémon`, `Pokédex`, `Poké Ball` deviennent
`Pokemon`, `Pokedex`, `Poke Ball` dans le texte HI nouveau : seule suppression
éditoriale des accents, pas renommage des espèces. Préserver la ponctuation
significative des noms EN, après vérification codec ; ne jamais écraser un nom
fourni par un buffer. « route » générique = `Raastaa`, mais `Route 3` reste EN.

Un nom inédit dans le fan-game est conservé tel quel et consigné dans le lot.
Un **terme commun** absent doit être ajouté au glossaire central avec son domaine,
sa provenance et son statut avant réemploi ; pas de dictionnaire divergent par lot.
Changer une graphie approuvée implique une nouvelle version et l'inventaire des
lots affectés, jamais une substitution globale des fichiers `combined_*`.

## Formes courtes et budgets

Le champ `hi` est la forme développée ; `short` la seule forme courte permise.
Les sigles techniques EN `ATK`, `DEF`, `Sp. ATK`, `Sp. DEF`, `SPE`, `ACC`, `EVA`,
`EXP`, `PWR`, `Lv` sont des choix de lisibilité, pas de l'hindi officiel.
Statuts en trois lettres : `ZHR JAL JAM LKV NND BHS` ; le poison aggravé utilise
le même sigle que le poison mais sa description conserve la distinction. Les
badges graphiques ne sont pas localisés par ces mots ; F-691 et les lots doivent
vérifier les surfaces et les métadonnées au moment de leur application.
`Use` et `Save` sont les replis courts fixés ; pas de troncature automatique.

**Aucun budget universel de caractères ne garantit l'injection.**

| Support | Budget à vérifier dans le lot |
|---|---|
| Cellule fixe de N octets | texte encodé + terminateur `FF` ≤ N, sans toucher le voisin ni déplacer la cellule |
| Texte sans pointeur relogeable | longueur encodée ≤ espace EN vivant démontré, pas le vide apparent après un `FF` |
| Dialogue relogeable | allocation et tous les pointeurs validés ; largeur normale indicative ≤192 px/ligne (`dialogue_linewrap.py`) |
| Menu, intro, résumé, mission | largeur/hauteur propre à la surface ; 192 px n'est pas une garantie pour ces fenêtres |
| Buffer | coût ROM du contrôle ET largeur maximale de sa valeur runtime, jamais la longueur du nom du token |

Les tables recensées dans `fixed_tables.py` ont notamment des cellules de 13
octets pour les attaques et 11 pour les espèces : 12/10 octets utiles au plus,
**à confirmer dans la base EN du lot**, sans appliquer aveuglément les anciennes
annotations « déjà français ». Un nom EN non conforme à une cellule identifiée
signale une mauvaise table ou un cas spécial à examiner, pas un droit à tronquer.
Les exemples du JSON ont un `max_bytes` explicite, terminateur compris : ce sont
des budgets de test, **pas les budgets des offsets des seeds**. Le test mesure
ces budgets sans fallback. Formes illustratives : `Koi asar nahin.` court ;
`Gufaa mein jaao.\nTumhaaraa dost vahaan\nintzaar kar rahaa hai.` long, trois
lignes. Ce dernier illustre la grammaire et l'encodage ; choisir les pages selon
la fenêtre réelle, ne pas coller trois lignes dans une boîte à deux lignes.
Si aucune forme ne tient : reformuler le contexte, ou consigner le blocage de
surface. Ne pas supprimer négation, cible, quantité ou condition pour raccourcir.

## Tokens : contrat commun sans permutation

Conserver la séquence, la multiplicité, les arguments et le rôle des tokens EN
vivants. Ne pas traduire leur contenu : `{0}`, `{1}`, `{PLAYER}`, `{RIVAL}`,
`{STR_VAR_1}`, `{STR_VAR_2}`, `{STR_VAR_3}`, `{UNKNOWN_STR}`, tous les `{B_*}`,
`{COLOR}` et son argument, `{LV}`, boutons et `<0xNN>` bruts.
La liste exacte dépend de l'entrée : ce n'est pas une allowlist exhaustive.

Le builder reconnaît certains noms via `FD_VARIABLE_CODES` mais utilise encore
une FIFO pour les noms inconnus. HI-LATIN-1 impose donc de **préserver l'ordre
même pour les noms connus**, et de reformuler autour. Exemple : ordre joueur,
objet → `<0xFD><0x01> ko <0xFD><0x02> milaa.`. Ne pas inverser `{0}` et `{1}`
pour satisfaire l'ordre hindi ; pas de renommage d'un buffer de genre.

Lire `FC/FD/F8/F9/F7` comme séquences multi-octets avec leurs paramètres ; un
argument n'est pas une lettre. Préserver pauses, couleurs, retours et frontières
sémantiques de pages. `\n` correspond à FE, `\l` à FA et `\p` à FB dans le
format source ; FA/FB sont hors FIFO des placeholders, **pas du texte libre**.
Ne pas en inventer pour réparer une cellule de menu. Tout déplacement de saut
exige validation de la fenêtre et de la séquence binaire. `{LV}` est un glyphe
particulier ; le `Lv` du glossaire est un libellé, pas un remplacement de token.
Passer par la normalisation/résolution du pipeline avant de mesurer les octets ;
`TextEncoder` seul ne résout pas les placeholders nommés ou positionnels.

## Relecture des trois seeds sur l'anglais vivant

Lecture seule de `input/roms/englishrom.gba` du checkout principal : SHA-256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Les textes lus jusqu'à FF sont identiques au snapshot EN. Les pointeurs sont
32 bits little-endian (`0x08000000 + offset`). Leur site et leur opcode, pas
seulement une recherche de texte, donnent les preuves suivantes.

| Offset | EN / seed actuelle | Contexte binaire vérifié et décision |
|---|---|---|
| `0x1773FD` | `I'll tell you.` / `Main tumhein bata raha hoon.` | Pointeur `0x162247`, second texte à +10 d'un `trainerbattle` (`5C 00 F3 01 00 00`). Futur/promesse après défaite, pas « je suis en train de te dire ». Proposition masculine `Main tumhein bataaungaa.`, féminine `Main tumhein bataaungi.` ; identifier le locuteur avant application, ne pas deviner son genre à partir de `raha`. |
| `0x177489` | `Not quite yet!` / `Abhi tak nahin!` | `loadpointer` (`0F 00`) aux sites de pointeur `0x78BF7F`, `0x7C7B95`, `0x7C7C87`. La seed exprime bien « pas encore » ; la conserver, sans transformer en « jamais » ou « pas tout à fait » hors contexte. |
| `0x183509` | `You beat me.` / `Tum mujhe peet dete ho.` | Deux pointeurs `0x1A944F`, `0x1A9476`, second texte de `trainerbattle` (`5C 00 69 00 00 00` et `5C 05 69 00 00 00`). Défaite de combat, pas coups physiques habituels. Recommandation `Tumne mujhe haraa diyaa.` (tu m'as vaincu), sans accord dépendant du genre du joueur. |

Les scripts référencent effectivement ces textes ; cela ne constitue pas un
replay de toutes leurs branches. Les textes EN occupent respectivement 14, 15,
12 octets avec FF. Les deux corrections proposées dépassent ces espaces : elles
ne sont **pas** à écrire en place aveuglément. Les trois seeds restent inchangées
ici ; leur application nécessite protections exactes, relocation validée et
preuve visuelle dans un ticket de rendu. Leur relecture sémantique est livrée,
pas une correction affichée prétendument testée.

## Validation, exploitation et limites

Commande : `python3 -m pytest tests/unit/test_hindi_reference.py -v`, puis
`make test-python` complet. La garde vérifie les domaines, les clés uniques,
les provenances, les deux formes, les exemples, les budgets et les tokens bruts.
Elle impose un alphabet encodable et compare les octets attendus directement à
la charmap, sans alias ni remplacement silencieux par `?` ; un vrai `?` est admis.

Pour chaque lot : citer HI-LATIN-1 v1.0.0, lire EN et pointeurs vivants, classer
les surfaces, préserver tokens, vérifier budgets et codec, modifier seulement
les dernières occurrences visées, ajouter chaque traduction à
`protected_entries.yaml` dans le même commit, builder Hindi et redécoder la ROM,
puis tester le rendu headless avec assertions et capture. Les termes conservés
EN doivent être comptés comme conservés selon glossaire, pas traduits en hindi.

Non vérifié ici : validation linguistique par un relecteur natif, couverture de
la totalité des noms/expressions d'Unbound, rendu de ces propositions en jeu,
branches complètes des scripts des seeds. Aucun support devanagari n'est fourni.
Les données de référence et leurs tests ne modifient aucun rendu ; Playwright
n'est donc pas applicable à ce ticket documentaire. Aucun build/release n'est
nécessaire pour injecter ces données puisqu'elles ne sont pas consommées par le
builder. L'infrastructure F-691 reste un préalable distinct des lots.

Validation locale D-692 : `make test-python` terminé avec **2336 passed,
3 skipped, 831 deselected** (profil Makefile, aucun test désactivé par ce ticket).
Les 149 cas du référentiel sont inclus. La première exécution avait signalé
l'absence des artefacts privés EN/DE dans le worktree neuf ; après mise à
disposition des artefacts locaux, la suite complète ci-dessus est verte.
SHA-256 de la ROM FR de référence, inchangé avant/après les travaux :
`74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
