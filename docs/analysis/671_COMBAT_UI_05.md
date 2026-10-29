# 671 — Qualification DE combat_ui-05 (B-671)

Périmètre : exactement les 300 offsets exclusifs du ticket, sans nouvel audit global.
Une seule traduction ajoutée, à `0xA438F0` : `Flag setzen` ; protection exacte dans
`languages/de/protected_entries.yaml`, contrôlée par `tests/unit/test_translation_integrity.py`.
Les autres absences ne justifient pas une insertion artificielle dans le fichier DE.

## Méthode et décisions

Lecture des dernières occurrences EN/DE/FR, puis décodage de la ROM EN canonique.
Recherche exhaustive des pointeurs absolus little-endian dans la ROM EN ; lecture
à chaque même site dans la ROM DE reconstruite. Pour les attaques, résolution de
la base indexée via `0x0308A4`, pas seulement recherche de pointeurs par entrée.
Les sites indiqués sont des références binaires, pas une preuve d'exécution de
chaque branche en jeu. Tous leurs textes cibles ont été comparés octet par octet
aux formes attendues (terminateur compris) et leurs lectures décodées contrôlées.

- Les 96 attaques sont déjà produites par `languages/de/patches/move_names.py`
  à partir de `languages/de/data/move_names_de_official.json`, conformément à
  `official_terminology.yaml`. Les cellules font 13 octets, terminateur compris.
  Les faux fragments français du corpus EN sont périmés : ils ne décrivent pas
  les octets de la ROM EN actuelle. Aucun ajout DE ni modification de ces ressources.
- `Finale`, `Land`, `Magma`, `Sand`, `Standard` et `Level 5/50/100` sont des
  termes allemands corrects dans leurs menus. `Wasser` traduit déjà `Water`.
  Les deux `Finale` n'ont pas de pointeur direct ; leurs octets sont conservés,
  sans conclure abusivement qu'une table indexée serait morte.
- Les noms Smogon, les coupes et formats (`Mega Brawl`, `Dynamax Standard`, etc.)
  sont des identifiants propres de règles, conservés comme dans la référence EN.
  `Smogon Benjamin Butterfree` reste entier : le nom du format n'est pas un nom
  d'espèce à remplacer isolément par `Smettbo`.
- Les prénoms du groupe `0xA44C9F–0xA45153` restent intentionnellement en anglais.
  `0xA44C9F` est l'espace précédant `Liam` : la table pointe à `0xA44CA0`.
  Ce fragment ne doit pas recevoir une traduction décalée.
- Le menu debug pointe à `0xA438F0` depuis `0x9A51C8`. L'ancienne entrée voisine
  `0xA438EF: Flag setzen` ne corrige pas ce pointeur. Elle est hors lot et reste
  intacte. La nouvelle entrée est repointable ; aucune écriture de 12 octets
  dans la cellule anglaise de 9 octets n'est autorisée.

Aucun dialogue scénarisé, pronom de personne, tutoiement/vouvoiement ni buffer
Sohn/Tochter dans ces 300 chaînes canoniques. Contexte : noms d'attaques, menu debug,
terrains DexNav, réglages/formats de combat et tables de prénoms de dresseurs.
Les chaînes contrôlées n'ont ni placeholders ni `\n`, `\l`, `\p` ni commandes
FC/FD/F7/F8/F9 ; leur séquence vide est préservée. Les umlauts des noms officiels
sont encodés en caractères réels. Les colonnes octets incluent FF ; les pixels
sont les avances de police normale fournies par `dialogue_linewrap.word_width`.
Aucune géométrie de boîte, aucun patch ni fichier FR/IT n'est modifié.

## Résultats

- Déjà patché : nom officiel : 96.
- Déjà correct : terme allemand : 10.
- Corrigé : oubli du menu debug : 1.
- Nom propre légitime : format de combat : 23.
- Fragment non vivant : espace avant Liam : 1.
- Nom propre légitime : prénom : 169.

SHA-256 ROM EN : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

SHA-256 ROM DE vérifiée : `0a4fa063cd55127da95bb93d7d30670a459e704bea7ab9ccb6354d40704adf92`.

## Décision exhaustive par offset

`∅` = absent du fichier ; `vide` = entrée présente mais vide. DE final désigne
le texte effectivement lu dans la ROM, y compris le patch officiel.

| Offset | EN fichier | DE fichier | FR fichier | EN ROM | DE final | Sites de pointeurs EN | Cibles DE | Octets | Pixels | Décision |
|---|---|---|---|---|---|---|---|---:|---:|---|
| 0xA411C8 | vide | ∅ | `Pince-Masse` | `Crabhammer` | `Krabbhammer` | table via 0x0308A4 | 0xA411C8 | 12 | 64 | Déjà patché : nom officiel |
| 0xA411D5 | vide | ∅ | `Explosion` | `Explosion` | `Explosion` | table via 0x0308A4 | 0xA411D5 | 10 | 49 | Déjà patché : nom officiel |
| 0xA411E2 | vide | ∅ | `Combo-Griffe` | `Fury Swipes` | `Kratzfurie` | table via 0x0308A4 | 0xA411E2 | 11 | 54 | Déjà patché : nom officiel |
| 0xA411EF | vide | ∅ | `Osmerang` | `Bonemerang` | `Knochmerang` | table via 0x0308A4 | 0xA411EF | 12 | 63 | Déjà patché : nom officiel |
| 0xA411FC | vide | ∅ | `Repos` | `Rest` | `Erholung` | table via 0x0308A4 | 0xA411FC | 9 | 45 | Déjà patché : nom officiel |
| 0xA41209 | `e rêver de pouvoir voler, sa\nstructure cellulaire a évolué et il\ns'est vu pousser des ailes.` | ∅ | `Éboulement` | `Rock Slide` | `Steinhagel` | table via 0x0308A4 | 0xA41209 | 11 | 55 | Déjà patché : nom officiel |
| 0xA41216 | `uvoir voler, sa\nstructure cellulaire a évolué et il\ns'est vu pousser des ailes.` | ∅ | `Croc de Mort` | `Hyper Fang` | `Hyperzahn` | table via 0x0308A4 | 0xA41216 | 10 | 52 | Déjà patché : nom officiel |
| 0xA41223 | `sa\nstructure cellulaire a évolué et il\ns'est vu pousser des ailes.` | ∅ | `Affûtage` | `Sharpen` | `Schärfer` | table via 0x0308A4 | 0xA41223 | 9 | 45 | Déjà patché : nom officiel |
| 0xA41230 | `cellulaire a évolué et il\ns'est vu pousser des ailes.` | ∅ | `Conversion` | `Conversion` | `Umwandlung` | table via 0x0308A4 | 0xA41230 | 11 | 57 | Déjà patché : nom officiel |
| 0xA4123D | `évolué et il\ns'est vu pousser des ailes.` | ∅ | `Triplattaque` | `Tri Attack` | `Triplette` | table via 0x0308A4 | 0xA4123D | 10 | 48 | Déjà patché : nom officiel |
| 0xA4124A | `s'est vu pousser des ailes.` | ∅ | `Croc Fatal` | `Super Fang` | `Superzahn` | table via 0x0308A4 | 0xA4124A | 10 | 52 | Déjà patché : nom officiel |
| 0xA41257 | `ser des ailes.` | ∅ | `Tranche` | `Slash` | `Schlitzer` | table via 0x0308A4 | 0xA41257 | 10 | 49 | Déjà patché : nom officiel |
| 0xA41264 | `.` | ∅ | `Clonage` | `Substitute` | `Delegator` | table via 0x0308A4 | 0xA41264 | 10 | 51 | Déjà patché : nom officiel |
| 0xA41271 | vide | ∅ | `Lutte` | `Struggle` | `Verzweifler` | table via 0x0308A4 | 0xA41271 | 12 | 60 | Déjà patché : nom officiel |
| 0xA4127E | vide | ∅ | `Gribouille` | `Sketch` | `Nachahmer` | table via 0x0308A4 | 0xA4127E | 10 | 53 | Déjà patché : nom officiel |
| 0xA4128B | vide | ∅ | `Triple Pied` | `Triple Kick` | `Dreifachkick` | table via 0x0308A4 | 0xA4128B | 13 | 64 | Déjà patché : nom officiel |
| 0xA41298 | vide | ∅ | `Larcin` | `Thief` | `Raub` | table via 0x0308A4 | 0xA41298 | 5 | 24 | Déjà patché : nom officiel |
| 0xA412A5 | vide | ∅ | `Toile` | `Spider Web` | `Spinnennetz` | table via 0x0308A4 | 0xA412A5 | 12 | 59 | Déjà patché : nom officiel |
| 0xA412B2 | vide | ∅ | `Lire-Esprit` | `Mind Reader` | `Willensleser` | table via 0x0308A4 | 0xA412B2 | 13 | 63 | Déjà patché : nom officiel |
| 0xA412BF | vide | ∅ | `Cauchemar` | `Nightmare` | `Nachtmahr` | table via 0x0308A4 | 0xA412BF | 10 | 52 | Déjà patché : nom officiel |
| 0xA412CC | `avec les siens par\nimpulsions magnétiques. En bande, ils se\ndéplacent à l'unisson.` | ∅ | `Roue de Feu` | `Flame Wheel` | `Flammenrad` | table via 0x0308A4 | 0xA412CC | 11 | 57 | Déjà patché : nom officiel |
| 0xA412D9 | `s par\nimpulsions magnétiques. En bande, ils se\ndéplacent à l'unisson.` | ∅ | `Ronflement` | `Snore` | `Schnarcher` | table via 0x0308A4 | 0xA412D9 | 11 | 57 | Déjà patché : nom officiel |
| 0xA412E6 | `ons magnétiques. En bande, ils se\ndéplacent à l'unisson.` | ∅ | `Malédiction` | `Curse` | `Fluch` | table via 0x0308A4 | 0xA412E6 | 6 | 29 | Déjà patché : nom officiel |
| 0xA412F3 | `es. En bande, ils se\ndéplacent à l'unisson.` | ∅ | `Gigotage` | `Flail` | `Dreschflegel` | table via 0x0308A4 | 0xA412F3 | 13 | 67 | Déjà patché : nom officiel |
| 0xA41300 | ` ils se\ndéplacent à l'unisson.` | ∅ | `Conversion 2` | `Conversion 2` | `Umwandlung2` | table via 0x0308A4 | 0xA41300 | 12 | 63 | Déjà patché : nom officiel |
| 0xA4130D | `cent à l'unisson.` | ∅ | `Aéroblast` | `Aeroblast` | `Luftstoß` | table via 0x0308A4 | 0xA4130D | 9 | 44 | Déjà patché : nom officiel |
| 0xA4131A | `son.` | ∅ | `Spore Coton` | `Cotton Spore` | `Baumwollsaat` | table via 0x0308A4 | 0xA4131A | 13 | 68 | Déjà patché : nom officiel |
| 0xA41327 | vide | ∅ | `Contre` | `Reversal` | `Gegenschlag` | table via 0x0308A4 | 0xA41327 | 12 | 63 | Déjà patché : nom officiel |
| 0xA41334 | vide | ∅ | `Dépit` | `Spite` | `Groll` | table via 0x0308A4 | 0xA41334 | 6 | 27 | Déjà patché : nom officiel |
| 0xA41341 | vide | ∅ | `Poudreuse` | `Powder Snow` | `Pulverschnee` | table via 0x0308A4 | 0xA41341 | 13 | 68 | Déjà patché : nom officiel |
| 0xA4134E | vide | ∅ | `Abri` | `Protect` | `Schutzschild` | table via 0x0308A4 | 0xA4134E | 13 | 67 | Déjà patché : nom officiel |
| 0xA4135B | vide | ∅ | `Mach Punch` | `Mach Punch` | `Tempohieb` | table via 0x0308A4 | 0xA4135B | 10 | 52 | Déjà patché : nom officiel |
| 0xA41368 | vide | ∅ | `Grimace` | `Scary Face` | `Grimasse` | table via 0x0308A4 | 0xA41368 | 9 | 43 | Déjà patché : nom officiel |
| 0xA41375 | vide | ∅ | `Feinte` | `Feint Attack` | `Finte` | table via 0x0308A4 | 0xA41375 | 6 | 26 | Déjà patché : nom officiel |
| 0xA41382 | ` est formé de deux Terhal soudés. Son\ncorps de fer résiste à un choc avec un\navion à réaction.` | ∅ | `Doux Baiser` | `Sweet Kiss` | `Bitterkuss` | table via 0x0308A4 | 0xA41382 | 11 | 52 | Déjà patché : nom officiel |
| 0xA4138F | ` deux Terhal soudés. Son\ncorps de fer résiste à un choc avec un\navion à réaction.` | ∅ | `Cognobidon` | `Belly Drum` | `Bauchtrommel` | table via 0x0308A4 | 0xA4138F | 13 | 69 | Déjà patché : nom officiel |
| 0xA4139C | `soudés. Son\ncorps de fer résiste à un choc avec un\navion à réaction.` | ∅ | `Bombe Beurk` | `Sludge Bomb` | `Matschbombe` | table via 0x0308A4 | 0xA4139C | 12 | 64 | Déjà patché : nom officiel |
| 0xA413A9 | `orps de fer résiste à un choc avec un\navion à réaction.` | ∅ | `Coud’Boue` | `Mud-Slap` | `Lehmschelle` | table via 0x0308A4 | 0xA413A9 | 12 | 63 | Déjà patché : nom officiel |
| 0xA413B6 | `ésiste à un choc avec un\navion à réaction.` | ∅ | `Octazooka` | `Octazooka` | `Octazooka` | table via 0x0308A4 | 0xA413B6 | 10 | 52 | Déjà patché : nom officiel |
| 0xA413C3 | `hoc avec un\navion à réaction.` | ∅ | `Picots` | `Spikes` | `Stachler` | table via 0x0308A4 | 0xA413C3 | 9 | 45 | Déjà patché : nom officiel |
| 0xA413D0 | `vion à réaction.` | ∅ | `Élecanon` | `Zap Cannon` | `Blitzkanone` | table via 0x0308A4 | 0xA413D0 | 12 | 59 | Déjà patché : nom officiel |
| 0xA413DD | `on.` | ∅ | `Clairvoyance` | `Foresight` | `Scharfblick` | table via 0x0308A4 | 0xA413DD | 12 | 60 | Déjà patché : nom officiel |
| 0xA413EA | vide | ∅ | `Prlvt Destin` | `Destiny Bond` | `Abgangsbund` | table via 0x0308A4 | 0xA413EA | 12 | 63 | Déjà patché : nom officiel |
| 0xA413F7 | vide | ∅ | `Requiem` | `Perish Song` | `Abgesang` | table via 0x0308A4 | 0xA413F7 | 9 | 46 | Déjà patché : nom officiel |
| 0xA41404 | vide | ∅ | `Vent Glace` | `Icy Wind` | `Eissturm` | table via 0x0308A4 | 0xA41404 | 9 | 42 | Déjà patché : nom officiel |
| 0xA41411 | vide | ∅ | `Détection` | `Detect` | `Scanner` | table via 0x0308A4 | 0xA41411 | 8 | 39 | Déjà patché : nom officiel |
| 0xA4141E | vide | ∅ | `Charge Os` | `Bone Rush` | `Knochenhatz` | table via 0x0308A4 | 0xA4141E | 12 | 63 | Déjà patché : nom officiel |
| 0xA4142B | vide | ∅ | `Verrouillage` | `Lock-On` | `Zielschuss` | table via 0x0308A4 | 0xA4142B | 11 | 54 | Déjà patché : nom officiel |
| 0xA41438 | vide | ∅ | `Colère` | `Outrage` | `Wutanfall` | table via 0x0308A4 | 0xA41438 | 10 | 49 | Déjà patché : nom officiel |
| 0xA41445 | `t qu'il a fait monter les eaux en\ncausant des pluies diluviennes. Il\nsomnolait dans une fosse marine.` | ∅ | `Tempêtesable` | `Sandstorm` | `Sandsturm` | table via 0x0308A4 | 0xA41445 | 10 | 50 | Déjà patché : nom officiel |
| 0xA41452 | `t monter les eaux en\ncausant des pluies diluviennes. Il\nsomnolait dans une fosse marine.` | ∅ | `Giga-Sangsue` | `Giga Drain` | `Gigasauger` | table via 0x0308A4 | 0xA41452 | 11 | 56 | Déjà patché : nom officiel |
| 0xA4145F | `eaux en\ncausant des pluies diluviennes. Il\nsomnolait dans une fosse marine.` | ∅ | `Ténacité` | `Endure` | `Ausdauer` | table via 0x0308A4 | 0xA4145F | 9 | 46 | Déjà patché : nom officiel |
| 0xA4146C | `nt des pluies diluviennes. Il\nsomnolait dans une fosse marine.` | ∅ | `Charme` | `Charm` | `Charme` | table via 0x0308A4 | 0xA4146C | 7 | 35 | Déjà patché : nom officiel |
| 0xA41479 | ` diluviennes. Il\nsomnolait dans une fosse marine.` | ∅ | `Roulade` | `Rollout` | `Walzer` | table via 0x0308A4 | 0xA41479 | 7 | 34 | Déjà patché : nom officiel |
| 0xA41486 | ` Il\nsomnolait dans une fosse marine.` | ∅ | `Faux-Chage` | `False Swipe` | `Trugschlag` | table via 0x0308A4 | 0xA41486 | 11 | 57 | Déjà patché : nom officiel |
| 0xA41493 | ` dans une fosse marine.` | ∅ | `Vantardise` | `Swagger` | `Angeberei` | table via 0x0308A4 | 0xA41493 | 10 | 50 | Déjà patché : nom officiel |
| 0xA414A0 | `se marine.` | ∅ | `Lait à Boire` | `Milk Drink` | `Milchgetränk` | table via 0x0308A4 ; 0xA6CAFC | 0xA414A0 / 0xA414A0 | 13 | 65 | Déjà patché : nom officiel |
| 0xA414AD | vide | ∅ | `Étincelle` | `Spark` | `Funkensprung` | table via 0x0308A4 | 0xA414AD | 13 | 66 | Déjà patché : nom officiel |
| 0xA414BA | vide | ∅ | `Taillade` | `Fury Cutter` | `Zornklinge` | table via 0x0308A4 | 0xA414BA | 11 | 53 | Déjà patché : nom officiel |
| 0xA414C7 | vide | ∅ | `AilesD’Acier` | `Steel Wing` | `Stahlflügel` | table via 0x0308A4 | 0xA414C7 | 12 | 61 | Déjà patché : nom officiel |
| 0xA414D4 | vide | ∅ | `Regard Noir` | `Mean Look` | `Horrorblick` | table via 0x0308A4 | 0xA414D4 | 12 | 59 | Déjà patché : nom officiel |
| 0xA414E1 | vide | ∅ | `Attraction` | `Attract` | `Anziehung` | table via 0x0308A4 | 0xA414E1 | 10 | 50 | Déjà patché : nom officiel |
| 0xA414EE | vide | ∅ | `Blabla Dodo` | `Sleep Talk` | `Schlafrede` | table via 0x0308A4 | 0xA414EE | 11 | 57 | Déjà patché : nom officiel |
| 0xA414FB | vide | ∅ | `Glas de Soin` | `Heal Bell` | `Vitalglocke` | table via 0x0308A4 | 0xA414FB | 12 | 60 | Déjà patché : nom officiel |
| 0xA41508 | `it dans le magma souterrain\ndepuis sa lutte féroce contre Kyogre, il\ny a longtemps de cela.` | ∅ | `Retour` | `Return` | `Rückkehr` | table via 0x0308A4 | 0xA41508 | 9 | 45 | Déjà patché : nom officiel |
| 0xA41515 | `gma souterrain\ndepuis sa lutte féroce contre Kyogre, il\ny a longtemps de cela.` | ∅ | `Cadeau` | `Present` | `Geschenk` | table via 0x0308A4 | 0xA41515 | 9 | 45 | Déjà patché : nom officiel |
| 0xA41522 | `n\ndepuis sa lutte féroce contre Kyogre, il\ny a longtemps de cela.` | ∅ | `Frustration` | `Frustration` | `Frustration` | table via 0x0308A4 | 0xA41522 | 12 | 58 | Déjà patché : nom officiel |
| 0xA4152F | `utte féroce contre Kyogre, il\ny a longtemps de cela.` | ∅ | `Rune Protect` | `Safeguard` | `Bodyguard` | table via 0x0308A4 | 0xA4152F | 10 | 53 | Déjà patché : nom officiel |
| 0xA4153C | `ontre Kyogre, il\ny a longtemps de cela.` | ∅ | `Balance` | `Pain Split` | `Leidteiler` | table via 0x0308A4 | 0xA4153C | 11 | 53 | Déjà patché : nom officiel |
| 0xA41549 | ` il\ny a longtemps de cela.` | ∅ | `Feu Sacré` | `Sacred Fire` | `Läuterfeuer` | table via 0x0308A4 | 0xA41549 | 12 | 62 | Déjà patché : nom officiel |
| 0xA41556 | `emps de cela.` | ∅ | `Ampleur` | `Magnitude` | `Intensität` | table via 0x0308A4 | 0xA41556 | 11 | 52 | Déjà patché : nom officiel |
| 0xA41563 | vide | ∅ | `Dynamo-Poing` | `DynamicPunch` | `Wuchtschlag` | table via 0x0308A4 | 0xA41563 | 12 | 63 | Déjà patché : nom officiel |
| 0xA41570 | vide | ∅ | `Mégacorne` | `Megahorn` | `Vielender` | table via 0x0308A4 | 0xA41570 | 10 | 49 | Déjà patché : nom officiel |
| 0xA4157D | vide | ∅ | `DracoSouffle` | `DragonBreath` | `Feuerodem` | table via 0x0308A4 | 0xA4157D | 10 | 53 | Déjà patché : nom officiel |
| 0xA4158A | vide | ∅ | `Relais` | `Baton Pass` | `Stafette` | table via 0x0308A4 | 0xA4158A | 9 | 44 | Déjà patché : nom officiel |
| 0xA41597 | vide | ∅ | `Encore` | `Encore` | `Zugabe` | table via 0x0308A4 | 0xA41597 | 7 | 36 | Déjà patché : nom officiel |
| 0xA415A4 | vide | ∅ | `Poursuite` | `Pursuit` | `Verfolgung` | table via 0x0308A4 | 0xA415A4 | 11 | 56 | Déjà patché : nom officiel |
| 0xA415B1 | vide | ∅ | `Tour Rapide` | `Rapid Spin` | `Turbodreher` | table via 0x0308A4 | 0xA415B1 | 12 | 63 | Déjà patché : nom officiel |
| 0xA415BE | vide | ∅ | `Doux Parfum` | `Sweet Scent` | `Lockduft` | table via 0x0308A4 ; 0xA6CB0C | 0xA415BE / 0xA415BE | 9 | 45 | Déjà patché : nom officiel |
| 0xA415CB | `qu'une fois tous les mille\nans, il a la capacité d'exaucer tous les\nvœux durant une semaine.` | ∅ | `Queue de Fer` | `Iron Tail` | `Eisenschweif` | table via 0x0308A4 | 0xA415CB | 13 | 64 | Déjà patché : nom officiel |
| 0xA415D8 | `ous les mille\nans, il a la capacité d'exaucer tous les\nvœux durant une semaine.` | ∅ | `Griffe Acier` | `Metal Claw` | `Metallklaue` | table via 0x0308A4 | 0xA415D8 | 12 | 61 | Déjà patché : nom officiel |
| 0xA415E5 | `\nans, il a la capacité d'exaucer tous les\nvœux durant une semaine.` | ∅ | `Corps Perdu` | `Vital Throw` | `Überwurf` | table via 0x0308A4 | 0xA415E5 | 9 | 45 | Déjà patché : nom officiel |
| 0xA415F2 | ` capacité d'exaucer tous les\nvœux durant une semaine.` | ∅ | `Aurore` | `Morning Sun` | `Morgengrauen` | table via 0x0308A4 | 0xA415F2 | 13 | 68 | Déjà patché : nom officiel |
| 0xA415FF | `xaucer tous les\nvœux durant une semaine.` | ∅ | `Synthèse` | `Synthesis` | `Synthese` | table via 0x0308A4 | 0xA415FF | 9 | 45 | Déjà patché : nom officiel |
| 0xA4160C | `es\nvœux durant une semaine.` | ∅ | `Rayon Lune` | `Moonlight` | `Mondschein` | table via 0x0308A4 | 0xA4160C | 11 | 55 | Déjà patché : nom officiel |
| 0xA41619 | `t une semaine.` | ∅ | `Puis. Cachée` | `Hidden Power` | `Kraftreserve` | table via 0x0308A4 | 0xA41619 | 13 | 66 | Déjà patché : nom officiel |
| 0xA41626 | `.` | ∅ | `Coup Croix` | `Cross Chop` | `Kreuzhieb` | table via 0x0308A4 | 0xA41626 | 10 | 51 | Déjà patché : nom officiel |
| 0xA41633 | vide | ∅ | `Ouragan` | `Twister` | `Windhose` | table via 0x0308A4 | 0xA41633 | 9 | 44 | Déjà patché : nom officiel |
| 0xA41640 | vide | ∅ | `Danse Pluie` | `Rain Dance` | `Regentanz` | table via 0x0308A4 | 0xA41640 | 10 | 51 | Déjà patché : nom officiel |
| 0xA4164D | vide | ∅ | `Zénith` | `Sunny Day` | `Sonnentag` | table via 0x0308A4 | 0xA4164D | 10 | 50 | Déjà patché : nom officiel |
| 0xA4165A | vide | ∅ | `Mâchouille` | `Crunch` | `Knirscher` | table via 0x0308A4 | 0xA4165A | 10 | 48 | Déjà patché : nom officiel |
| 0xA41667 | vide | ∅ | `Voile Miroir` | `Mirror Coat` | `Spiegelcape` | table via 0x0308A4 | 0xA41667 | 12 | 63 | Déjà patché : nom officiel |
| 0xA41674 | vide | ∅ | `Boost` | `Psych Up` | `Psycho-Plus` | table via 0x0308A4 | 0xA41674 | 12 | 63 | Déjà patché : nom officiel |
| 0xA41681 | `l vient d'un virus extraterrestre\narrivé avec une météorite et ayant subi\nune mutation génétique.` | ∅ | `Vit.Extrême` | `ExtremeSpeed` | `Turbotempo` | table via 0x0308A4 | 0xA41681 | 11 | 58 | Déjà patché : nom officiel |
| 0xA4168E | `virus extraterrestre\narrivé avec une météorite et ayant subi\nune mutation génétique.` | ∅ | `Pouv.Antique` | `AncientPower` | `Antik-Kraft` | table via 0x0308A4 | 0xA4168E | 12 | 58 | Déjà patché : nom officiel |
| 0xA41F71 | vide | ∅ | `Yama Arashi` | `Storm Throw` | `Bergsturm` | table via 0x0308A4 | 0xA41F71 | 10 | 50 | Déjà patché : nom officiel |
| 0xA4386D | `Finale` | `Finale` | `Finale` | `Finale` | `Finale` | aucun pointeur direct ; octets en place (accès indexé non tracé) | 0xA4386D | 7 | 32 | Déjà correct : terme allemand |
| 0xA4387A | `Finale` | `Finale` | `Finale` | `Finale` | `Finale` | aucun pointeur direct ; octets en place (accès indexé non tracé) | 0xA4387A | 7 | 32 | Déjà correct : terme allemand |
| 0xA438F0 | `Set Flag` | `Flag setzen` | ∅ | `Set Flag` | `Flag setzen` | 0x9A51C8 | 0x7B21F8 | 12 | 62 | Corrigé : oubli du menu debug |
| 0xA439B0 | ∅ | `Wasser` | `Eau` | `Water` | `Wasser` | 0x9D7320, 0x9D7614 | 0xE58FA9 / 0xE58FA9 | 7 | 33 | Déjà correct : terme allemand |
| 0xA439B6 | `Land` | `Land` | `Terre` | `Land` | `Land` | 0x9D761C | 0xA439B6 | 5 | 23 | Déjà correct : terme allemand |
| 0xA43A18 | `Magma` | `Magma` | `Magma` | `Magma` | `Magma` | 0x9D7318 | 0xA43A18 | 6 | 30 | Déjà correct : terme allemand |
| 0xA43A1E | `Sand` | `Sand` | `Sable` | `Sand` | `Sand` | 0x9D7618 | 0xA43A1E | 5 | 23 | Déjà correct : terme allemand |
| 0xA440D0 | `Level 5` | `Level 5` | `Level 5` | `Level 5` | `Level 5` | 0x9E97F4 | 0xA440D0 | 8 | 41 | Déjà correct : terme allemand |
| 0xA440D8 | `Level 50` | `Level 50` | `Level 50` | `Level 50` | `Level 50` | 0x9E97FC | 0xA440D8 | 9 | 47 | Déjà correct : terme allemand |
| 0xA440E1 | `Level 100` | `Level 100` | `Level 100` | `Level 100` | `Level 100` | 0x9E97F8 | 0xA440E1 | 10 | 53 | Déjà correct : terme allemand |
| 0xA4412B | `Standard` | `Standard` | `Standard` | `Standard` | `Standard` | 0xA6B700 | 0xA4412B | 9 | 45 | Déjà correct : terme allemand |
| 0xA44144 | `Smogon OU` | `Smogon OU` | `Smogon OU` | `Smogon OU` | `Smogon OU` | 0xA6B708 | 0xA44144 | 10 | 53 | Nom propre légitime : format de combat |
| 0xA4414E | `Smogon Doubles OU` | `Smogon Doubles OU` | `Smogon Doubles OU` | `Smogon Doubles OU` | `Smogon Doubles OU` | 0x9E6DBC | 0xA4414E | 18 | 99 | Nom propre légitime : format de combat |
| 0xA44160 | `Smogon Ubers` | `Smogon Ubers` | `Smogon Ubers` | `Smogon Ubers` | `Smogon Ubers` | 0xA6B70C | 0xA44160 | 13 | 69 | Nom propre légitime : format de combat |
| 0xA4416D | `Smogon Little Cup` | `Smogon Little Cup` | `Smogon Little Cup` | `Smogon Little Cup` | `Smogon Little Cup` | 0xA6B710 | 0xA4416D | 18 | 96 | Nom propre légitime : format de combat |
| 0xA4417F | `Middle Cup` | `Middle Cup` | `Middle Cup` | `Middle Cup` | `Middle Cup` | 0xA6B714 | 0xA4417F | 11 | 57 | Nom propre légitime : format de combat |
| 0xA4418A | `Smogon Monotype` | `Smogon Monotype` | `Smogon Monotype` | `Smogon Monotype` | `Smogon Monotype` | 0xA6B718 | 0xA4418A | 16 | 87 | Nom propre légitime : format de combat |
| 0xA4419A | `GS Cup` | `GS Cup` | `GS Cup` | `GS Cup` | `GS Cup` | 0x9E6DC0 | 0xA4419A | 7 | 36 | Nom propre légitime : format de combat |
| 0xA441A1 | `Smogon Camomons` | `Smogon Camomons` | `Smogon Camomons` | `Smogon Camomons` | `Smogon Camomons` | 0xA6B71C | 0xA441A1 | 16 | 87 | Nom propre légitime : format de combat |
| 0xA441B1 | `Uber Camomons` | `Uber Camomons` | `Uber Camomons` | `Uber Camomons` | `Uber Camomons` | 0xA6B720 | 0xA441B1 | 14 | 75 | Nom propre légitime : format de combat |
| 0xA441BF | `Little Cup Camomons` | `Little Cup Camomons` | `Little Cup Camomons` | `Little Cup Camomons` | `Little Cup Camomons` | 0xA6B724 | 0xA441BF | 20 | 107 | Nom propre légitime : format de combat |
| 0xA441D3 | `Middle Cup Camomons` | `Middle Cup Camomons` | `Middle Cup Camomons` | `Middle Cup Camomons` | `Middle Cup Camomons` | 0xA6B728 | 0xA441D3 | 20 | 109 | Nom propre légitime : format de combat |
| 0xA441E7 | `GS Cup Camomons` | `GS Cup Camomons` | `GS Cup Camomons` | `GS Cup Camomons` | `GS Cup Camomons` | 0x9E6DB8 | 0xA441E7 | 16 | 88 | Nom propre légitime : format de combat |
| 0xA441F7 | `Smogon Scalemons` | `Smogon Scalemons` | `Smogon Scalemons` | `Smogon Scalemons` | `Smogon Scalemons` | 0xA6B72C | 0xA441F7 | 17 | 92 | Nom propre légitime : format de combat |
| 0xA44208 | `Smogon 350 Cup` | `Smogon 350 Cup` | `Smogon 350 Cup` | `Smogon 350 Cup` | `Smogon 350 Cup` | 0xA6B730 | 0xA44208 | 15 | 83 | Nom propre légitime : format de combat |
| 0xA44217 | `Smogon Averagemons` | `Smogon Averagemons` | `Smogon Averagemons` | `Smogon Averagemons` | `Smogon Averagemons` | 0xA6B734 | 0xA44217 | 19 | 104 | Nom propre légitime : format de combat |
| 0xA4422A | `Smogon Benjamin Butterfree` | `Smogon Benjamin Butterfree` | `Smogon Benjamin Papilusion` | `Smogon Benjamin Butterfree` | `Smogon Benjamin Butterfree` | 0xA6B738 | 0xA4422A | 27 | 146 | Nom propre légitime : format de combat |
| 0xA44245 | `Mega Brawl` | `Mega Brawl` | `Mega Brawl` | `Mega Brawl` | `Mega Brawl` | 0xA6B73C | 0xA44245 | 11 | 58 | Nom propre légitime : format de combat |
| 0xA44250 | `Dynamax Standard` | `Dynamax Standard` | `Dynamax Standard` | `Dynamax Standard` | `Dynamax Standard` | 0xA6B740 | 0xA44250 | 17 | 92 | Nom propre légitime : format de combat |
| 0xA44261 | `Smogon National Dex OU` | `Smogon National Dex OU` | `Smogon National Dex OU` | `Smogon National Dex OU` | `Smogon National Dex OU` | 0xA6B744 | 0xA44261 | 23 | 126 | Nom propre légitime : format de combat |
| 0xA44278 | `Smogon Metronome` | `Smogon Metronome` | `Smogon Metronome` | `Smogon Metronome` | `Smogon Metronome` | 0xA6B748 | 0xA44278 | 17 | 92 | Nom propre légitime : format de combat |
| 0xA44289 | `Smogon Gen 7 UU` | `Smogon Gen 7 UU` | `Smogon Gen 7 UU` | `Smogon Gen 7 UU` | `Smogon Gen 7 UU` | 0xA6B74C | 0xA44289 | 16 | 88 | Nom propre légitime : format de combat |
| 0xA44299 | `Smogon Gen 7 RU` | `Smogon Gen 7 RU` | `Smogon Gen 7 RU` | `Smogon Gen 7 RU` | `Smogon Gen 7 RU` | 0xA6B754 | 0xA44299 | 16 | 88 | Nom propre légitime : format de combat |
| 0xA442A9 | `Smogon Gen 7 NU` | `Smogon Gen 7 NU` | `Smogon Gen 7 NU` | `Smogon Gen 7 NU` | `Smogon Gen 7 NU` | 0xA6B750 | 0xA442A9 | 16 | 88 | Nom propre légitime : format de combat |
| 0xA44C9F | ` Liam` | ∅ | `Liam` | ` Liam` | `Liam` | début réel 0xA44CA0 via 0xA76484 | 0xA44CA0 | 5 | 22 | Fragment non vivant : espace avant Liam |
| 0xA44CA5 | `Noah` | ∅ | `Noah` | `Noah` | `Noah` | 0xA76488 | 0xA44CA5 | 5 | 24 | Nom propre légitime : prénom |
| 0xA44CAA | `William` | ∅ | `William` | `William` | `William` | 0xA7648C | 0xA44CAA | 8 | 36 | Nom propre légitime : prénom |
| 0xA44CB2 | `James` | ∅ | `James` | `James` | `James` | 0xA76490 | 0xA44CB2 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44CB8 | `Logan` | ∅ | `Logan` | `Logan` | `Logan` | 0xA76494 | 0xA44CB8 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44CBE | `Benjamin` | ∅ | `Benjamin` | `Benjamin` | `Benjamin` | 0xA76498 | 0xA44CBE | 9 | 44 | Nom propre légitime : prénom |
| 0xA44CC7 | `Mason` | ∅ | `Mason` | `Mason` | `Mason` | 0xA7649C | 0xA44CC7 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44CCD | `Elijah` | ∅ | `Elijah` | `Elijah` | `Elijah` | 0xA764A0 | 0xA44CCD | 7 | 33 | Nom propre légitime : prénom |
| 0xA44CD4 | `Oliver` | ∅ | `Oliver` | `Oliver` | `Oliver` | 0xA764A4 | 0xA44CD4 | 7 | 32 | Nom propre légitime : prénom |
| 0xA44CDB | `Jacob` | ∅ | `Jacob` | `Jacob` | `Jacob` | 0xA764A8 | 0xA44CDB | 6 | 30 | Nom propre légitime : prénom |
| 0xA44CE1 | `Lucas` | ∅ | `Lucas` | `Lucas` | `Lucas` | 0xA764AC | 0xA44CE1 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44CE7 | `Michael` | ∅ | `Michael` | `Michael` | `Michael` | 0xA764B0 | 0xA44CE7 | 8 | 39 | Nom propre légitime : prénom |
| 0xA44CEF | `Alexander` | ∅ | `Alexander` | `Alexander` | `Alexander` | 0xA764B4 | 0xA44CEF | 10 | 51 | Nom propre légitime : prénom |
| 0xA44CF9 | `Ethan` | ∅ | `Ethan` | `Ethan` | `Ethan` | 0xA764B8 | 0xA44CF9 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44CFF | `Daniel` | ∅ | `Daniel` | `Daniel` | `Daniel` | 0xA764BC | 0xA44CFF | 7 | 32 | Nom propre légitime : prénom |
| 0xA44D06 | `Matthew` | ∅ | `Matthew` | `Matthew` | `Matthew` | 0xA764C0 | 0xA44D06 | 8 | 40 | Nom propre légitime : prénom |
| 0xA44D0E | `Aiden` | ∅ | `Aiden` | `Aiden` | `Aiden` | 0xA764C4 | 0xA44D0E | 6 | 27 | Nom propre légitime : prénom |
| 0xA44D14 | `Henry` | ∅ | `Henry` | `Henry` | `Henry` | 0xA764C8 | 0xA44D14 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44D1A | `Joseph` | ∅ | `Joseph` | `Joseph` | `Joseph` | 0xA764CC | 0xA44D1A | 7 | 35 | Nom propre légitime : prénom |
| 0xA44D21 | `Jackson` | ∅ | `Jackson` | `Jackson` | `Jackson` | 0xA764D0 | 0xA44D21 | 8 | 39 | Nom propre légitime : prénom |
| 0xA44D29 | `Samuel` | ∅ | `Samuel` | `Samuel` | `Samuel` | 0xA764D4 | 0xA44D29 | 7 | 35 | Nom propre légitime : prénom |
| 0xA44D30 | `Sebastian` | ∅ | `Sebastian` | `Sebastian` | `Sebastian` | 0xA764D8 | 0xA44D30 | 10 | 49 | Nom propre légitime : prénom |
| 0xA44D3A | `David` | ∅ | `David` | `David` | `David` | 0xA764DC | 0xA44D3A | 6 | 28 | Nom propre légitime : prénom |
| 0xA44D40 | `Carter` | ∅ | `Carter` | `Carter` | `Carter` | 0xA764E0 | 0xA44D40 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44D47 | `Wyatt` | ∅ | `Wyatt` | `Wyatt` | `Wyatt` | 0xA764E4 | 0xA44D47 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44D4D | `Jayden` | ∅ | `Jayden` | `Jayden` | `Jayden` | 0xA764E8 | 0xA44D4D | 7 | 35 | Nom propre légitime : prénom |
| 0xA44D54 | `John` | ∅ | `John` | `John` | `John` | 0xA764EC | 0xA44D54 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44D59 | `Owen` | ∅ | `Owen` | `Owen` | `Owen` | 0xA764F0 | 0xA44D59 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44D5E | `Dylan` | ∅ | `Dylan` | `Dylan` | `Dylan` | 0xA764F4 | 0xA44D5E | 6 | 28 | Nom propre légitime : prénom |
| 0xA44D64 | `Luke` | ∅ | `Luke` | `Luke` | `Luke` | 0xA764F8 | 0xA44D64 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44D69 | `Gabriel` | ∅ | `Gabriel` | `Gabriel` | `Gabriel` | 0xA764FC | 0xA44D69 | 8 | 38 | Nom propre légitime : prénom |
| 0xA44D71 | `Anthony` | ∅ | `Anthony` | `Anthony` | `Anthony` | 0xA76500 | 0xA44D71 | 8 | 39 | Nom propre légitime : prénom |
| 0xA44D79 | `Isaac` | ∅ | `Isaac` | `Isaac` | `Isaac` | 0xA76504 | 0xA44D79 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44D7F | `Grayson` | ∅ | `Grayson` | `Grayson` | `Grayson` | 0xA76508 | 0xA44D7F | 8 | 39 | Nom propre légitime : prénom |
| 0xA44D87 | `Jack` | ∅ | `Jack` | `Jack` | `Jack` | 0xA7650C | 0xA44D87 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44D8C | `Julian` | ∅ | `Julian` | `Julian` | `Julian` | 0xA76510 | 0xA44D8C | 7 | 32 | Nom propre légitime : prénom |
| 0xA44D93 | `Levi` | ∅ | `Levi` | `Levi` | `Levi` | 0xA76514 | 0xA44D93 | 5 | 22 | Nom propre légitime : prénom |
| 0xA44D98 | `Christopher` | ∅ | `Christopher` | `Christopher` | `Christopher` | 0xA76518 | 0xA44D98 | 12 | 60 | Nom propre légitime : prénom |
| 0xA44DA4 | `Joshua` | ∅ | `Joshua` | `Joshua` | `Joshua` | 0xA7651C | 0xA44DA4 | 7 | 35 | Nom propre légitime : prénom |
| 0xA44DAB | `Andrew` | ∅ | `Andrew` | `Andrew` | `Andrew` | 0xA76520 | 0xA44DAB | 7 | 34 | Nom propre légitime : prénom |
| 0xA44DB2 | `Lincoln` | ∅ | `Lincoln` | `Lincoln` | `Lincoln` | 0xA76524 | 0xA44DB2 | 8 | 37 | Nom propre légitime : prénom |
| 0xA44DBA | `Mateo` | ∅ | `Mateo` | `Mateo` | `Mateo` | 0xA76528 | 0xA44DBA | 6 | 29 | Nom propre légitime : prénom |
| 0xA44DC0 | `Ryan` | ∅ | `Ryan` | `Ryan` | `Ryan` | 0xA7652C | 0xA44DC0 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44DC5 | `Jaxon` | ∅ | `Jaxon` | `Jaxon` | `Jaxon` | 0xA76530 | 0xA44DC5 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44DCB | `Nathan` | ∅ | `Nathan` | `Nathan` | `Nathan` | 0xA76534 | 0xA44DCB | 7 | 34 | Nom propre légitime : prénom |
| 0xA44DD2 | `Aaron` | ∅ | `Aaron` | `Aaron` | `Aaron` | 0xA76538 | 0xA44DD2 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44DD8 | `Isaiah` | ∅ | `Isaiah` | `Isaiah` | `Isaiah` | 0xA7653C | 0xA44DD8 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44DDF | `Thomas` | ∅ | `Thomas` | `Thomas` | `Thomas` | 0xA76540 | 0xA44DDF | 7 | 35 | Nom propre légitime : prénom |
| 0xA44DE6 | `Charles` | ∅ | `Charles` | `Charles` | `Charles` | 0xA76544 | 0xA44DE6 | 8 | 39 | Nom propre légitime : prénom |
| 0xA44DEE | `Caleb` | ∅ | `Caleb` | `Caleb` | `Caleb` | 0xA76548 | 0xA44DEE | 6 | 29 | Nom propre légitime : prénom |
| 0xA44DF4 | `Josiah` | ∅ | `Josiah` | `Josiah` | `Josiah` | 0xA7654C | 0xA44DF4 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44DFB | `Christian` | ∅ | `Christian` | `Christian` | `Christian` | 0xA76550 | 0xA44DFB | 10 | 46 | Nom propre légitime : prénom |
| 0xA44E05 | `Hunter` | ∅ | `Hunter` | `Hunter` | `Hunter` | 0xA76554 | 0xA44E05 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44E10 | `Jonathan` | ∅ | `Jonathan` | `Jonathan` | `Jonathan` | 0xA7655C | 0xA44E10 | 9 | 45 | Nom propre légitime : prénom |
| 0xA44E19 | `Connor` | ∅ | `Connor` | `Connor` | `Connor` | 0xA76560 | 0xA44E19 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44E20 | `Landon` | ∅ | `Landon` | `Landon` | `Landon` | 0xA76564 | 0xA44E20 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44E27 | `Adrian` | ∅ | `Adrian` | `Adrian` | `Adrian` | 0xA76568 | 0xA44E27 | 7 | 32 | Nom propre légitime : prénom |
| 0xA44E2E | `Asher` | ∅ | `Asher` | `Asher` | `Asher` | 0xA7656C | 0xA44E2E | 6 | 28 | Nom propre légitime : prénom |
| 0xA44E34 | `Cameron` | ∅ | `Cameron` | `Cameron` | `Cameron` | 0xA76570 | 0xA44E34 | 8 | 40 | Nom propre légitime : prénom |
| 0xA44E40 | `Theodore` | ∅ | `Theodore` | `Theodore` | `Theodore` | 0xA76578 | 0xA44E40 | 9 | 47 | Nom propre légitime : prénom |
| 0xA44E49 | `Jeremiah` | ∅ | `Jeremiah` | `Jeremiah` | `Jeremiah` | 0xA7657C | 0xA44E49 | 9 | 45 | Nom propre légitime : prénom |
| 0xA44E52 | `Hudson` | ∅ | `Hudson` | `Hudson` | `Hudson` | 0xA76580 | 0xA44E52 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44E59 | `Robert` | ∅ | `Robert` | `Robert` | `Robert` | 0xA76584 | 0xA44E59 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44E60 | `Easton` | ∅ | `Easton` | `Easton` | `Easton` | 0xA76588 | 0xA44E60 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44E67 | `Nolan` | ∅ | `Nolan` | `Nolan` | `Nolan` | 0xA7658C | 0xA44E67 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44E6D | `Nicholas` | ∅ | `Nicholas` | `Nicholas` | `Nicholas` | 0xA76590 | 0xA44E6D | 9 | 44 | Nom propre légitime : prénom |
| 0xA44E76 | `Ezra` | ∅ | `Ezra` | `Ezra` | `Ezra` | 0xA76594 | 0xA44E76 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44E7B | `Colton` | ∅ | `Colton` | `Colton` | `Colton` | 0xA76598 | 0xA44E7B | 7 | 33 | Nom propre légitime : prénom |
| 0xA44E82 | `Angel` | ∅ | `Angel` | `Angel` | `Angel` | 0xA7659C | 0xA44E82 | 6 | 28 | Nom propre légitime : prénom |
| 0xA44E88 | `Brayden` | ∅ | `Brayden` | `Brayden` | `Brayden` | 0xA765A0 | 0xA44E88 | 8 | 40 | Nom propre légitime : prénom |
| 0xA44E90 | `Jordan` | ∅ | `Jordan` | `Jordan` | `Jordan` | 0xA765A4 | 0xA44E90 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44E97 | `Dominic` | ∅ | `Dominic` | `Dominic` | `Dominic` | 0xA765A8 | 0xA44E97 | 8 | 37 | Nom propre légitime : prénom |
| 0xA44E9F | `Austin` | ∅ | `Austin` | `Austin` | `Austin` | 0xA765AC | 0xA44E9F | 7 | 31 | Nom propre légitime : prénom |
| 0xA44EAA | `Adam` | ∅ | `Adam` | `Adam` | `Adam` | 0xA765B4 | 0xA44EAA | 5 | 24 | Nom propre légitime : prénom |
| 0xA44EAF | `Elias` | ∅ | `Elias` | `Elias` | `Elias` | 0xA765B8 | 0xA44EAF | 6 | 26 | Nom propre légitime : prénom |
| 0xA44EB5 | `Jaxson` | ∅ | `Jaxson` | `Jaxson` | `Jaxson` | 0xA765BC | 0xA44EB5 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44EBC | `Greyson` | ∅ | `Greyson` | `Greyson` | `Greyson` | 0xA765C0 | 0xA44EBC | 8 | 39 | Nom propre légitime : prénom |
| 0xA44EC4 | `Jose` | ∅ | `Jose` | `Jose` | `Jose` | 0xA765C4 | 0xA44EC4 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44EC9 | `Ezekiel` | ∅ | `Ezekiel` | `Ezekiel` | `Ezekiel` | 0xA765C8 | 0xA44EC9 | 8 | 38 | Nom propre légitime : prénom |
| 0xA44ED1 | `Carson` | ∅ | `Carson` | `Carson` | `Carson` | 0xA765CC | 0xA44ED1 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44ED8 | `Evan` | ∅ | `Evan` | `Evan` | `Evan` | 0xA765D0 | 0xA44ED8 | 5 | 23 | Nom propre légitime : prénom |
| 0xA44EDD | `Maverick` | ∅ | `Maverick` | `Maverick` | `Maverick` | 0xA765D4 | 0xA44EDD | 9 | 44 | Nom propre légitime : prénom |
| 0xA44EE6 | `Bryson` | ∅ | `Bryson` | `Bryson` | `Bryson` | 0xA765D8 | 0xA44EE6 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44EED | `Jace` | ∅ | `Jace` | `Jace` | `Jace` | 0xA765DC | 0xA44EED | 5 | 24 | Nom propre légitime : prénom |
| 0xA44EF2 | `Cooper` | ∅ | `Cooper` | `Cooper` | `Cooper` | 0xA765E0 | 0xA44EF2 | 7 | 35 | Nom propre légitime : prénom |
| 0xA44EF9 | `Xavier` | ∅ | `Xavier` | `Xavier` | `Xavier` | 0xA765E4 | 0xA44EF9 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44F00 | `Parker` | ∅ | `Parker` | `Parker` | `Parker` | 0xA765E8 | 0xA44F00 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44F07 | `Roman` | ∅ | `Roman` | `Roman` | `Roman` | 0xA765EC | 0xA44F07 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44F0D | `Jason` | ∅ | `Jason` | `Jason` | `Jason` | 0xA765F0 | 0xA44F0D | 6 | 28 | Nom propre légitime : prénom |
| 0xA44F13 | `Santiago` | ∅ | `Santiago` | `Santiago` | `Santiago` | 0xA765F4 | 0xA44F13 | 9 | 44 | Nom propre légitime : prénom |
| 0xA44F1C | `Chase` | ∅ | `Chase` | `Chase` | `Chase` | 0xA765F8 | 0xA44F1C | 6 | 29 | Nom propre légitime : prénom |
| 0xA44F22 | `Sawyer` | ∅ | `Sawyer` | `Sawyer` | `Sawyer` | 0xA765FC | 0xA44F22 | 7 | 35 | Nom propre légitime : prénom |
| 0xA44F29 | `Gavin` | ∅ | `Gavin` | `Gavin` | `Gavin` | 0xA76600 | 0xA44F29 | 6 | 27 | Nom propre légitime : prénom |
| 0xA44F2F | `Leonardo` | ∅ | `Leonardo` | `Leonardo` | `Leonardo` | 0xA76604 | 0xA44F2F | 9 | 46 | Nom propre légitime : prénom |
| 0xA44F38 | `Kayden` | ∅ | `Kayden` | `Kayden` | `Kayden` | 0xA76608 | 0xA44F38 | 7 | 35 | Nom propre légitime : prénom |
| 0xA44F3F | `Ayden` | ∅ | `Ayden` | `Ayden` | `Ayden` | 0xA7660C | 0xA44F3F | 6 | 29 | Nom propre légitime : prénom |
| 0xA44F45 | `Jameson` | ∅ | `Jameson` | `Jameson` | `Jameson` | 0xA76610 | 0xA44F45 | 8 | 40 | Nom propre légitime : prénom |
| 0xA44F4D | `Emma` | ∅ | `Emma` | `Emma` | `Emma` | 0xA762F4 | 0xA44F4D | 5 | 24 | Nom propre légitime : prénom |
| 0xA44F52 | `Olivia` | ∅ | `Olivia` | `Olivia` | `Olivia` | 0xA762F8 | 0xA44F52 | 7 | 31 | Nom propre légitime : prénom |
| 0xA44F5D | `Isabella` | ∅ | `Isabella` | `Isabella` | `Isabella` | 0xA76300 | 0xA44F5D | 9 | 45 | Nom propre légitime : prénom |
| 0xA44F66 | `Sophia` | ∅ | `Sophia` | `Sophia` | `Sophia` | 0xA76304 | 0xA44F66 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44F71 | `Charlotte` | ∅ | `Charlotte` | `Charlotte` | `Charlotte` | 0xA7630C | 0xA44F71 | 10 | 50 | Nom propre légitime : prénom |
| 0xA44F7B | `Amelia` | ∅ | `Amelia` | `Amelia` | `Amelia` | 0xA76310 | 0xA44F7B | 7 | 33 | Nom propre légitime : prénom |
| 0xA44F82 | `Evelyn` | ∅ | `Evelyn` | `Evelyn` | `Evelyn` | 0xA76314 | 0xA44F82 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44F89 | `Abigail` | ∅ | `Abigail` | `Abigail` | `Abigail` | 0xA76318 | 0xA44F89 | 8 | 37 | Nom propre légitime : prénom |
| 0xA44F91 | `Harper` | ∅ | `Harper` | `Harper` | `Harper` | 0xA7631C | 0xA44F91 | 7 | 34 | Nom propre légitime : prénom |
| 0xA44F98 | `Emily` | ∅ | `Emily` | `Emily` | `Emily` | 0xA76320 | 0xA44F98 | 6 | 27 | Nom propre légitime : prénom |
| 0xA44F9E | `Elizabeth` | ∅ | `Elizabeth` | `Elizabeth` | `Elizabeth` | 0xA76324 | 0xA44F9E | 10 | 50 | Nom propre légitime : prénom |
| 0xA44FA8 | `Avery` | ∅ | `Avery` | `Avery` | `Avery` | 0xA76328 | 0xA44FA8 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44FAE | `Sofia` | ∅ | `Sofia` | `Sofia` | `Sofia` | 0xA7632C | 0xA44FAE | 6 | 27 | Nom propre légitime : prénom |
| 0xA44FB4 | `Ella` | ∅ | `Ella` | `Ella` | `Ella` | 0xA76330 | 0xA44FB4 | 5 | 22 | Nom propre légitime : prénom |
| 0xA44FB9 | `Madison` | ∅ | `Madison` | `Madison` | `Madison` | 0xA76334 | 0xA44FB9 | 8 | 38 | Nom propre légitime : prénom |
| 0xA44FC1 | `Scarlett` | ∅ | `Scarlett` | `Scarlett` | `Scarlett` | 0xA76338 | 0xA44FC1 | 9 | 44 | Nom propre légitime : prénom |
| 0xA44FCA | `Victoria` | ∅ | `Victoria` | `Victoria` | `Victoria` | 0xA7633C | 0xA44FCA | 9 | 42 | Nom propre légitime : prénom |
| 0xA44FD3 | `Aria` | ∅ | `Aria` | `Aria` | `Aria` | 0xA76340 | 0xA44FD3 | 5 | 21 | Nom propre légitime : prénom |
| 0xA44FD8 | `Grace` | ∅ | `Grace` | `Grace` | `Grace` | 0xA76344 | 0xA44FD8 | 6 | 29 | Nom propre légitime : prénom |
| 0xA44FDE | `Chloe` | ∅ | `Chloe` | `Chloe` | `Chloe` | 0xA76348 | 0xA44FDE | 6 | 29 | Nom propre légitime : prénom |
| 0xA44FE4 | `Camila` | ∅ | `Camila` | `Camila` | `Camila` | 0xA7634C | 0xA44FE4 | 7 | 33 | Nom propre légitime : prénom |
| 0xA44FEB | `Penelope` | ∅ | `Penelope` | `Penelope` | `Penelope` | 0xA76350 | 0xA44FEB | 9 | 46 | Nom propre légitime : prénom |
| 0xA44FF4 | `Riley` | ∅ | `Riley` | `Riley` | `Riley` | 0xA76354 | 0xA44FF4 | 6 | 27 | Nom propre légitime : prénom |
| 0xA44FFA | `Layla` | ∅ | `Layla` | `Layla` | `Layla` | 0xA76358 | 0xA44FFA | 6 | 29 | Nom propre légitime : prénom |
| 0xA45000 | `Lillian` | ∅ | `Lillian` | `Lillian` | `Lillian` | 0xA7635C, 0x16D31ED | 0xA45000 / 0xA45000 | 8 | 35 | Nom propre légitime : prénom |
| 0xA45008 | `Nora` | ∅ | `Nora` | `Nora` | `Nora` | 0xA76360 | 0xA45008 | 5 | 23 | Nom propre légitime : prénom |
| 0xA4500D | `Zoey` | ∅ | `Zoey` | `Zoey` | `Zoey` | 0xA76364 | 0xA4500D | 5 | 24 | Nom propre légitime : prénom |
| 0xA45012 | `Mila` | ∅ | `Mila` | `Mila` | `Mila` | 0xA76368 | 0xA45012 | 5 | 21 | Nom propre légitime : prénom |
| 0xA45017 | `Aubrey` | ∅ | `Aubrey` | `Aubrey` | `Aubrey` | 0xA7636C | 0xA45017 | 7 | 35 | Nom propre légitime : prénom |
| 0xA4501E | `Hannah` | ∅ | `Hannah` | `Hannah` | `Hannah` | 0xA76370 | 0xA4501E | 7 | 34 | Nom propre légitime : prénom |
| 0xA45025 | `Lily` | ∅ | `Lily` | `Lily` | `Lily` | 0xA76374 | 0xA45025 | 5 | 21 | Nom propre légitime : prénom |
| 0xA4502A | `Addison` | ∅ | `Addison` | `Addison` | `Addison` | 0xA76378 | 0xA4502A | 8 | 38 | Nom propre légitime : prénom |
| 0xA45032 | `Eleanor` | ∅ | `Eleanor` | `Eleanor` | `Eleanor` | 0xA7637C | 0xA45032 | 8 | 39 | Nom propre légitime : prénom |
| 0xA4503A | `Natalie` | ∅ | `Natalie` | `Natalie` | `Natalie` | 0xA76380 | 0xA4503A | 8 | 38 | Nom propre légitime : prénom |
| 0xA45042 | `Luna` | ∅ | `Luna` | `Luna` | `Luna` | 0xA76384 | 0xA45042 | 5 | 23 | Nom propre légitime : prénom |
| 0xA45047 | `Savannah` | ∅ | `Savannah` | `Savannah` | `Savannah` | 0xA76388 | 0xA45047 | 9 | 46 | Nom propre légitime : prénom |
| 0xA45050 | `Brooklyn` | ∅ | `Brooklyn` | `Brooklyn` | `Brooklyn` | 0xA7638C | 0xA45050 | 9 | 44 | Nom propre légitime : prénom |
| 0xA45059 | `Leah` | ∅ | `Leah` | `Leah` | `Leah` | 0xA76390 | 0xA45059 | 5 | 24 | Nom propre légitime : prénom |
| 0xA45062 | `Stella` | ∅ | `Stella` | `Stella` | `Stella` | 0xA76398 | 0xA45062 | 7 | 33 | Nom propre légitime : prénom |
| 0xA45069 | `Hazel` | ∅ | `Hazel` | `Hazel` | `Hazel` | 0xA7639C | 0xA45069 | 6 | 29 | Nom propre légitime : prénom |
| 0xA4506F | `Ellie` | ∅ | `Ellie` | `Ellie` | `Ellie` | 0xA763A0 | 0xA4506F | 6 | 26 | Nom propre légitime : prénom |
| 0xA45075 | `Paisley` | ∅ | `Paisley` | `Paisley` | `Paisley` | 0xA763A4 | 0xA45075 | 8 | 38 | Nom propre légitime : prénom |
| 0xA4507D | `Audrey` | ∅ | `Audrey` | `Audrey` | `Audrey` | 0xA763A8 | 0xA4507D | 7 | 35 | Nom propre légitime : prénom |
| 0xA45084 | `Skylar` | ∅ | `Skylar` | `Skylar` | `Skylar` | 0xA763AC | 0xA45084 | 7 | 33 | Nom propre légitime : prénom |
| 0xA4508B | `Violet` | ∅ | `Violet` | `Violet` | `Violet` | 0xA763B0 | 0xA4508B | 7 | 32 | Nom propre légitime : prénom |
| 0xA45092 | `Claire` | ∅ | `Claire` | `Claire` | `Claire` | 0xA763B4 | 0xA45092 | 7 | 32 | Nom propre légitime : prénom |
| 0xA45099 | `Bella` | ∅ | `Bella` | `Bella` | `Bella` | 0xA763B8 | 0xA45099 | 6 | 28 | Nom propre légitime : prénom |
| 0xA4509F | `Aurora` | ∅ | `Aurora` | `Aurora` | `Aurora` | 0xA763BC | 0xA4509F | 7 | 34 | Nom propre légitime : prénom |
| 0xA450A6 | `Lucy` | ∅ | `Lucy` | `Lucy` | `Lucy` | 0xA763C0 | 0xA450A6 | 5 | 24 | Nom propre légitime : prénom |
| 0xA450AB | `Anna` | ∅ | `Anna` | `Anna` | `Anna` | 0xA763C4 | 0xA450AB | 5 | 22 | Nom propre légitime : prénom |
| 0xA450B0 | `Samantha` | ∅ | `Samantha` | `Samantha` | `Samantha` | 0xA763C8 | 0xA450B0 | 9 | 46 | Nom propre légitime : prénom |
| 0xA450B9 | `Caroline` | ∅ | `Caroline` | `Caroline` | `Caroline` | 0xA763CC | 0xA450B9 | 9 | 43 | Nom propre légitime : prénom |
| 0xA450C2 | `Genesis` | ∅ | `Genesis` | `Genesis` | `Genesis` | 0xA763D0 | 0xA450C2 | 8 | 37 | Nom propre légitime : prénom |
| 0xA450CA | `Aaliyah` | ∅ | `Aaliyah` | `Aaliyah` | `Aaliyah` | 0xA763D4 | 0xA450CA | 8 | 39 | Nom propre légitime : prénom |
| 0xA450D2 | `Kennedy` | ∅ | `Kennedy` | `Kennedy` | `Kennedy` | 0xA763D8 | 0xA450D2 | 8 | 40 | Nom propre légitime : prénom |
| 0xA450DA | `Kinsley` | ∅ | `Kinsley` | `Kinsley` | `Kinsley` | 0xA763DC | 0xA450DA | 8 | 37 | Nom propre légitime : prénom |
| 0xA450E2 | `Allison` | ∅ | `Allison` | `Allison` | `Allison` | 0xA763E0 | 0xA450E2 | 8 | 36 | Nom propre légitime : prénom |
| 0xA450EA | `Maya` | ∅ | `Maya` | `Maya` | `Maya` | 0xA763E4 | 0xA450EA | 5 | 24 | Nom propre légitime : prénom |
| 0xA450EF | `Sarah` | ∅ | `Sarah` | `Sarah` | `Sarah` | 0xA763E8 | 0xA450EF | 6 | 29 | Nom propre légitime : prénom |
| 0xA450F5 | `Madelyn` | ∅ | `Madelyn` | `Madelyn` | `Madelyn` | 0xA763EC | 0xA450F5 | 8 | 40 | Nom propre légitime : prénom |
| 0xA450FD | `Adeline` | ∅ | `Adeline` | `Adeline` | `Adeline` | 0xA763F0 | 0xA450FD | 8 | 38 | Nom propre légitime : prénom |
| 0xA45105 | `Alexa` | ∅ | `Alexa` | `Alexa` | `Alexa` | 0xA763F4 | 0xA45105 | 6 | 29 | Nom propre légitime : prénom |
| 0xA4510B | `Ariana` | ∅ | `Ariana` | `Ariana` | `Ariana` | 0xA763F8 | 0xA4510B | 7 | 32 | Nom propre légitime : prénom |
| 0xA45112 | `Elena` | ∅ | `Elena` | `Elena` | `Elena` | 0xA763FC | 0xA45112 | 6 | 28 | Nom propre légitime : prénom |
| 0xA45118 | `Gabriella` | ∅ | `Gabriella` | `Gabriella` | `Gabriella` | 0xA76400 | 0xA45118 | 10 | 49 | Nom propre légitime : prénom |
| 0xA45122 | `Naomi` | ∅ | `Naomi` | `Naomi` | `Naomi` | 0xA76404 | 0xA45122 | 6 | 28 | Nom propre légitime : prénom |
| 0xA45128 | `Alice` | ∅ | `Alice` | `Alice` | `Alice` | 0xA50CE8, 0xA76408 | 0xA45128 / 0xA45128 | 6 | 27 | Nom propre légitime : prénom |
| 0xA4512E | `Sadie` | ∅ | `Sadie` | `Sadie` | `Sadie` | 0xA7640C | 0xA4512E | 6 | 28 | Nom propre légitime : prénom |
| 0xA45134 | `Hailey` | ∅ | `Hailey` | `Hailey` | `Hailey` | 0xA76410 | 0xA45134 | 7 | 33 | Nom propre légitime : prénom |
| 0xA4513F | `Emilia` | ∅ | `Emilia` | `Emilia` | `Emilia` | 0xA76418 | 0xA4513F | 7 | 31 | Nom propre légitime : prénom |
| 0xA45146 | `Autumn` | ∅ | `Autumn` | `Autumn` | `Autumn` | 0xA7641C | 0xA45146 | 7 | 34 | Nom propre légitime : prénom |
| 0xA4514D | `Quinn` | ∅ | `Quinn` | `Quinn` | `Quinn` | 0xA76420 | 0xA4514D | 6 | 26 | Nom propre légitime : prénom |
| 0xA45153 | `Nevaeh` | ∅ | `Nevaeh` | `Nevaeh` | `Nevaeh` | 0xA76424 | 0xA45153 | 7 | 36 | Nom propre légitime : prénom |

## Validation locale

- `make build-de` : réussi via le hook actif ; le hook impose également les
  builds FR/IT, exécutés uniquement dans le worktree. Aucun fichier source FR/IT
  ni référence de hash FR modifié.
- `make test-python` : **2171 réussis, 93 sous-tests réussis, 7 ignorés existants,
  742 désélectionnés** par la cible standard ; aucune exclusion ajoutée.
- Premier hook : **2029 tests Python rapides** et **68 tests Vitest** réussis.
- Garde supplémentaire `tests/unit/de/test_combat_ui_05_qualification.py` :
  **1 réussi** ; empreinte de la liste exacte du ticket, décisions et cibles
  obligatoires pour les 300 offsets. Test déclaré dans la matrice de tests
  `languages/de/parity.yaml`, sans modifier les données de traduction des patches.
- Contrôle ciblé : **300 offsets uniques**, ensemble exactement égal au ticket ;
  toutes les cibles décodées et leurs octets encodés + FF sont conformes.
  Toutes les cellules d'attaques respectent les 13 octets. Aucun contrôle perdu.
- Le pointeur `0x9A51C8` vaut désormais `0x087B21F8` ; sa cible contient
  `c0 e0 d5 db 00 e7 d9 e8 ee d9 e2 ff` (`Flag setzen`, 12 octets, 62 pixels).
  Les octets `0xA438EF–0xA438F8` restent strictement identiques à la ROM EN :
  aucune écriture en débordement dans l'ancienne cellule ou son voisin.
- `npx playwright test --config tests/e2e-playwright/playwright.combat-ui-05-de.config.ts` :
  **1 réussi**. mGBA avec `QT_QPA_PLATFORM=offscreen`, Chromium headless,
  assertions sur pointeur/octets et OCR `Flag setzen`, rejet de `Set Flag`.
  Le texte du pointeur réel est présenté par la boîte standard du jeu dans une
  copie temporaire de ROM ; aucune sauvegarde en jeu, aucun changement des fixtures.
- Capture vérifiée attachée au ticket :
  `attachment://c7399535-caab-4747-a2ea-19627dbae757` ; fichier dans le répertoire
  temporaire du système, aucune image de preuve dans Git.
- Diff de `605f02f5` relu après commit : un seul offset ajouté et sa protection,
  aucun autre texte modifié. Hooks conservés ; aucun push ni pipeline distant.

## Non vérifié

Le parcours utilisateur jusqu'au menu de débogage original n'a pas été rejoué.
La preuve visuelle couvre le texte réellement pointé et son rendu par le moteur
avec la police DE dans une boîte standard, pas la géométrie de ce menu debug.
Les accès calculés aux deux cellules `Finale` n'ont pas été tracés en exécution ;
leur contenu, déjà correct en allemand, est inchangé. Aucun besoin de patch
séparé n'a été établi pour ce lot.
