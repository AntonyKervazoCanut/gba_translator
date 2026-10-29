# B-678 — Qualification et corrections DE, dialogues-06

Périmètre strict : les 300 offsets du ticket, sans nouvel audit global.
Le [relevé individuel](678_DIALOGUES_06_DE.json) conserve pour chacun la dernière
valeur EN/FR/DE avant correction, les octets EN canoniques, les références directes,
la décision et sa justification. La source EN a pour SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

## Décisions

| Décision | Nombre | Motif |
|---|---:|---|
| Fragments non vivants comme texte | 272 | 211 fragments d'icônes 4bpp et 61 fragments audio DPCM |
| Corrigés | 12 | Fidélité, registre, genre, terminologie et commandes conservées |
| Déjà corrects | 4 | Garde du port, garde de Bellin, installations, anniversaire |
| Noms propres légitimes | 8 | Antisis, Bellin, Battleground, Frontier, Pokémon Center |
| Onomatopées légitimes | 4 | Cris et exclamation, sans traduction arbitraire |

Les 272 exclusions sont absentes de DE et doivent le rester. Le scan complet de la
ROM, à tous les alignements, ne trouve aucune référence 32 bits vers ces offsets
précis. Ce constat seul ne prouverait pas leur nature : la classification s'appuie
aussi sur les limites des ressources auxquelles ils appartiennent.

- Icônes : `gMonIconTable` à `0x1A217FC`, blocs bruts de `0x420` octets,
  région `[0x189C054, 0x19DCFF4)`. Voir
  `languages/fr/patches/mon_icon_repair.py` (lecture seule). Les pointeurs des
  ressources, leurs bornes et l'index de chaque icône figurent dans le relevé.
- Audio : en-têtes `WaveData`, format 1, longueur physique
  `16 + ceil(nombre_échantillons / 64) * 33`. Les 61 offsets se trouvent dans
  ces blocs DPCM ; leurs en-têtes et références de tables sont consignés.
  Structure et format confirmés par
  [m4a_internal.h](https://raw.githubusercontent.com/pret/pokefirered/master/include/gba/m4a_internal.h)
  et [wav2agb/converter.cpp](https://raw.githubusercontent.com/pret/pokefirered/master/tools/wav2agb/converter.cpp).

Les pseudo-commandes FC/FD/FA/FB et les caractères accentués observés dans ces
fragments sont des valeurs binaires accidentelles, pas des placeholders à traduire.
Aucun patch de ressources n'est nécessaire pour ce lot. Aucune modification FR/IT,
de police, de charmap, de patch ou de bundle distribué.

## Relecture des textes vivants

Les 28 entrées restantes ont des consommateurs identifiés dans la ROM canonique.
Les scènes sont Antisis City/Port, le Battleground et Bellin Town. Aucune entrée
n'est une fiche Pokédex ; `0x7A823B` est hors lot. Aucun buffer Sohn/Tochter n'est
présent. Les noms de lieux et d'espèces EN restent intentionnels.

Les 12 corrections portent exclusivement sur les dernières occurrences de
`combined_de.txt`, accompagnées des protections exactes dans le même commit :

- `0x1EDD5D5` : ancien policier d'Antisis, allemand naturel et deux pauses conservées.
- `0x1EDE63B` : Spezialität est bien le nom officiel d'Old Gateau ; maintien du
  français volontaire « Oui, oui » dans la caractérisation du personnage.
- `0x1EDFB75` : défi des Arenaleiter, et non des Champions.
- `0x1EE02B5` : choix des Pokémon de départ, et non de l'ordre complet de l'équipe ;
  texte complet lu en ROM au-delà de la coupure du corpus EN.
- `0x1EE118A` : Vega est un Arenaleiter/Agent masculin ; lieu Cinder Volcano en EN,
  motivations et trois pauses restaurées. Contexte recoupé avec
  [la scène de Cinder Volcano](https://unboundwiki.com/walkthrough/part-19/).
- `0x1EE1904` : aptitude au renseignement, sans genre féminin imposé au joueur.
- `0x1EE29F6` : Galavan garde le ton familier, le chapeau et l'ancienne relation.
- `0x1EE2F9F` : Metallium Z, Voltium Z, Turbo-Spiralkombo et Gigavolt-Funkensalve ;
  types Stahl/Elektro, couleurs et ordre des commandes conservés.
- `0x1EE3C49` : Tessy emploie Schätzchen sans genre imposé ; référence au Badge
  et invitation finale rétablies, à partir de la ROM complète.
- `0x1EE563C` : Victini est le Mysteriöse Triumph-Pokémon ; condition des huit
  Arenaleiter et partage volontaire du pouvoir conservés. La catégorie est
  confirmée par [Nintendo DE](https://www.nintendo.com/de-de/News/2011/Veni-vidi-Victini--253433.html).
- `0x1EE6834` : PC dans le coin, pas simplement un PC local.
- `0x1EE692E` : Chansey en EN selon la politique du build, sans changer le sens.

Terminologie : référentiel local `languages/de/data/official_terminology.yaml`,
[noms des attaques](https://bulbapedia.bulbagarden.net/wiki/List_of_moves_in_other_languages),
[Metallium Z](https://bulbapedia.bulbagarden.net/wiki/Steelium_Z),
[Voltium Z](https://www.wikidex.net/wiki/Electrostal_Z).
Le nom Gigavolt-Funkensalve est également attesté par
[Pokémon DE](https://www.pokemon.com/de/zeichentrick/staffeln/20/folge-2-die-herausforderung-des-schutzpatrons).

Les codes sont comparés après décodage de leurs arguments, pas par comparaison
textuelle des alias. À `0x1EE6B13`, `{VERSION}` représente bien le buffer âge
FD07 ; les quatre variables FD02/03/04/07 restent dans l'ordre canonique.
Les retours mécaniques sont rééquilibrés selon les métriques de la police ; les
pages et les pauses de la ROM source restent conservées.

## Validation locale

Le relevé JSON contient aussi les octets DE, les cibles des pointeurs et les
largeurs du build du commit `e807390b`. Les adresses de relocalisation sont une
observation de ce build, pas des adresses à coder en dur : les tests résolvent
toujours les consommateurs EN dans la ROM reconstruite.

- `make build-de` exécuté après le commit : réussi.
- `make test-python` : 2 950 réussis, 3 ignorés préexistants, 1 340 désélectionnés
  par le profil standard ; aucun échec (218,84 secondes).
- `tests/unit/test_translation_integrity.py` : 30 tests réussis ; protections
  exactes des 12 dernières valeurs. Matrice DE et garde de périmètre conformes.
- Hooks activés : 2 809 tests Python rapides réussis (1 exclusion existante),
  68 tests Vitest réussis ; builds FR/IT/DE réussis dans le worktree isolé.
- `tests/unit/de/test_dialogues_06.py` : 2 tests réussis, dont le contrôle ROM
  des 28 chaînes et de leurs 34 références. Octets exacts, placeholders et
  commandes dans l'ordre, nombre de pages EN conservé, largeurs ≤ 192 pixels.
- 272/272 fragments exclus : octets DE identiques aux octets EN à ces offsets.
- Playwright headless + mGBA `QT_QPA_PLATFORM=offscreen` : 5 tests réussis en
  29 secondes, assertions OCR sur Vega, les cristaux Z, Turbo-Spiralkombo,
  Gigavolt-Funkensalve et Victini. Captures enregistrées dans le répertoire
  temporaire système puis jointes au ticket, jamais dans Git.
- `ruff check tests/unit/de/test_dialogues_06.py` et `git diff --check` : conformes.
- Hash de la ROM FR du checkout principal comparé avant/après : identique.

| Offset corrigé | Octets DE, terminateur inclus | Largeur maximale |
|---|---:|---:|
| 0x1EDD5D5 | 293 | 187 px |
| 0x1EDE63B | 81 | 167 px |
| 0x1EDFB75 | 365 | 192 px |
| 0x1EE02B5 | 493 | 188 px |
| 0x1EE118A | 567 | 191 px |
| 0x1EE1904 | 321 | 187 px |
| 0x1EE29F6 | 355 | 189 px |
| 0x1EE2F9F | 448 | 191 px |
| 0x1EE3C49 | 613 | 189 px |
| 0x1EE563C | 616 | 192 px |
| 0x1EE6834 | 250 | 191 px |
| 0x1EE692E | 270 | 177 px |

Huit textes ont été relocalisés par le pipeline, quatre écrits en place.
Les textes relocalisés sont vérifiés à destination, pas dans leur ancien slot.

## Non vérifié

Pas de parcours narratif complet des trois zones ni d'écoute des échantillons DPCM.
Les sondes visuelles invoquent des pages des textes réellement injectés par leurs
pointeurs vivants, dans une copie temporaire de la ROM, sans sauvegarde en jeu.
Elles ne simulent pas le parcours d'accès à chaque PNJ.
