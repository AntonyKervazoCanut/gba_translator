# B-683 — Qualification DE objets-01

Qualification des **300 offsets exclusifs** du ticket, le 29 octobre 2026. Aucun audit global.

## Clôture après intégration de B-1026

Les 122 besoins de patch séparé décrits ci-dessous sont désormais résolus par
B-1026, intégré dans les commits `2630ebcf`, `c7ddb7d9` et `a00074bb`.
La comparaison des ensembles d'offsets confirme une correspondance exacte entre
les 122 besoins du présent relevé et les 122 corrections du rapport enfant.
Le bilan final est donc **122 noms corrigés, 145 déjà correctement patchés et
33 termes légitimes conservés**, soit 300 décisions sur 300.

Le rapport et le JSON B-683 restent un relevé historique avant correction : les
mentions « absent du corpus », « patch séparé requis » et les octets observés
ci-dessous ne décrivent pas la ROM finale. Les valeurs définitives, les six
abréviations et les neuf décisions spécifiques Unbound sont documentées dans
[1026_OBJETS_01_DE.md](1026_OBJETS_01_DE.md) et son JSON associé. En particulier,
les propositions « Schlüssel: 2/3 » ont été remplacées par « Codekarte: 2/3 »
après confrontation aux descriptions ; Hard Stone est désormais Granitstein.

Vérification parent après intégration : `make build-de` réussi, puis **315 tests
ciblés réussis**, dont le contrôle ROM des 300 cellules, de la base vivante et
de la préservation des métadonnées et pointeurs pendant le patch des noms.
L'absence initiale de la sauvegarde `.item-names.bak` dans l'ancien build parent
a été résolue par cette reconstruction, sans désactiver le test.
La reprise confirme `make test-python` : **4 341 réussis, trois skips préexistants**,
sans échec ; Ruff et le contrôle du diff passent également.

Preuve visuelle fournie par B-1026 : 122 résolutions `bufferitemname` dans mGBA,
douze noms rendus avec OCR et assertions de pixels ; capture finale attachée
au ticket enfant : `d0f9264e-d776-4f2f-b8ff-4b5ed6caaec8`.
Non vérifié : capture individuelle des 122 lignes du sac et accessibilité de
chaque objet en partie ; les budgets pixels sont contrôlés automatiquement.

## Résultat

| Décision | Nombre |
| --- | ---: |
| Déjà correctement patché dans la ROM reconstruite | 145 |
| Terme allemand légitime identique à EN | 33 |
| Patch séparé requis (B-1026) | 122 |
| Texte corrigé dans ce ticket | 0 |

Les 122 besoins sont **121 noms anglais vivants** et **un contresens du patch existant** :
`Hard Stone` → `Harter Stein`, alors que le nom officiel est **Granitstein**.
Le ticket distinct **B-1026** porte leur raccordement et correction. Il ne bloque pas
cette qualification : le critère du lot autorise expressément les besoins de patch séparé.
Aucun nom manquant n'est déclaré corrigé ; aucun fragment n'est déclaré mort.

Les 300 valeurs DE et FR sont absentes des corpus, après lecture avec résolution
par dernière occurrence. Le JSON associé consigne chaque absence (`null`), la dernière
valeur du corpus EN (avec numéro de ligne), les deux préimages ROM, le résultat DE,
la cible terminologique et le motif individuel. Les noms du corpus EN contenant du
français ne sont pas employés comme préimages de la ROM anglaise propre.

## Pourquoi aucune insertion dans combined_de.txt

Ces offsets désignent des champs `name[14]` dans des structures de 44 octets.
La **base vivante est 0x876200** : premier objet (Meisterball) à base + 1 × 44.
La constante historique 0x876074 utilisée par le patch est neuf cellules avant la
base, avec le même alignement ; ce n'est pas la base réelle du moteur.

Le code Thumb à 0x9A8CA charge 0x2C, multiplie l'index, charge le pointeur à
0x9A8D8 (= 0x08876200) puis additionne la base. Les 18 occurrences brutes de cette
base sont identiques avant/après build ; 14 se trouvent dans les lecteurs indexés
entre 0x9A8D8 et 0x9AAAC. Ce chemin rend les noms accessibles même sans pointeur
individuel. Ne pas qualifier ces noms de fragments non vivants.

L'extraction locale réutilisée par le build ne contient que quatre des 300 offsets :
0x876284, 0x876678, 0x877438, 0x877800. Les deux premiers y portent encore les
préimages françaises `Super Ball` et `Eau Fraîche`, différentes de la ROM canonique
`Great Ball` et `Fresh Water`. Les deux autres sont déjà traduits par le patch.
`apply_combined_fr.py --extend` ignore les offsets absents de cette extraction.
Une correction limitée au corpus n'est donc pas un raccordement fiable de cette table.
Les sept références brutes à ces quatre cellules sont consignées et inchangées ; leur
présence dans les données ne démontre pas à elle seule un appel moteur valide.

Le patch `item_names` utilise encore des clés françaises pour plusieurs balles.
Il manque aussi de nombreuses clés anglaises (médicaments, objets tenus, etc.).
Le ticket interdit de modifier les patchs ou ressources sans ticket distinct :
aucun patch, aucune ressource de jeu, aucun combined ni manifeste de protection n'est modifié.
Ajouter des protections sur des traductions non injectées aurait donné une fausse assurance.

## Terminologie, sens et contraintes

Comparaison individuelle avec le [catalogue des noms localisés PokeAPI figé](https://raw.githubusercontent.com/PokeAPI/pokeapi/c0a9bc75af3a455cdfa27dde21e4ec95aedd3f25/data/v2/csv/item_names.csv),
révision du glossaire `languages/de/data/official_terminology.yaml` ; SHA256 du CSV
consigné dans le JSON. Les équivalences CFRU sont explicites : `Parlyz Heal`,
`EnergyPowder`, `Thunderstone`, `TinyMushroom`, `Whip Dream`, `King's Rock`,
`Weak Policy`, `SS. Ticket` correspondent aux noms complets du catalogue.

- `Spitz.Schnab.` est l'abréviation validée de Spitzer Schnabel dans le glossaire.
- `Up-Grade` conserve la graphie historique (catalogue moderne : Upgrade).
- TM01 à TM27 sont allemands : Technische Maschine. Protein, Nugget, Magnet,
  Lucky Punch et Uniform sont également légitimes ; pas de traduction automatique.
- Les neuf noms spécifiques Unbound portent une **proposition éditoriale**, pas un
  nom officiel : Meersalz, Seemuschel, Dyna-Pulver, Traumnebel, Tauschstein,
  Werte-Scanner, Barrierenpass, Schlüssel: 2 et Schlüssel: 3. B-1026 devra confronter
  leurs descriptions avant de les insérer.
- Red Orb / Blue Orb : Roter Edelstein / Blauer Edelstein dépassent la cellule ;
  B-1026 doit définir une abréviation ou un raccordement pointeur sûr.
- Chaque nom reconstruit possède son terminateur dans les 14 octets, au plus
  13 glyphes. Largeur calculée avec les avances normales CFRU : maximum **76 px**.
  Cette mesure n'est pas un test de toutes les boîtes avec substitution d'objet.
- Aucun placeholder, contrôle FC/FD/F8/F9/F7, saut de ligne FE, défilement FA ou
  paragraphe FB dans ces 300 noms. Les umlauts et ß sont encodés exactement ;
  aller-retour octets/texte vérifié pour chaque cellule.
- Registre et genre : noms isolés, aucun dialogue ou accord Sohn/Tochter.
  Aucun Pokédex, espèce ou lieu ; 0x7A823B est hors lot et reste intact.

## Contrôles binaires et résultats locaux

- ROM EN canonique : SHA256 `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
- `make build-de` : succès (code 0), ROM de 33 554 432 octets, hash dans le JSON.
- `make test-python` : **3207 réussis, 97 ignorés, 1677 désélectionnés**, aucun échec.
  Les ignorés sont ceux de la suite existante, notamment faute d'artefacts ROM FR/IT
  dans le worktree isolé au moment du lancement ; aucun test modifié ou désactivé.
- Vérification dédiée exécutée : 300 cellules, round-trip exact, portée exclusive,
  métadonnées +14..+19 et +24..+43 préservées, 300 pointeurs de description valides,
  18 références de base et sept références brutes individuelles préservées.
  Les descriptions peuvent être relocalisées par le build existant ; leurs valeurs
  EN/DE sont enregistrées, sans prétendre auditer leur traduction hors lot.
- L'index 102 (Oval Stone) a déjà un champ itemId à zéro dans EN : conservé exactement,
  distinct de l'index utilisé pour l'accès au nom ; aucune réparation structurelle.
- Aucun fichier FR/IT ni baseline modifié. Aucun push ni pipeline distant.

## Non vérifié

Aucun affichage n'est modifié par ce ticket de qualification. Pas de test Playwright
ni de capture de gameplay revendiqués ; la preuve visuelle des 122 corrections est
requise dans B-1026. L'accessibilité de chaque objet au cours d'une partie et le
rendu de chaque phrase qui substitue son nom ne sont pas testés ici. Les données
extraites historiques ne sont pas régénérées ; les conclusions sur le lot reposent
sur la ROM canonique et la ROM réellement construite, pas sur ces préimages périmées.

## Décision par offset

FR/DE corpus : absents pour les 300 lignes. Détails et octets :
[683_OBJETS_01_DE.json](683_OBJETS_01_DE.json).
La colonne cible décrit la décision ; elle ne représente pas une correction injectée.

| Offset | ROM EN canonique | ROM DE construite | Cible / terme retenu | Décision |
| --- | --- | --- | --- | --- |
| 0x87622C | Master Ball | Meisterball | Meisterball | déjà patché |
| 0x876258 | Ultra Ball | Ultra Ball | Hyperball | patch séparé requis |
| 0x876284 | Great Ball | Great Ball | Superball | patch séparé requis |
| 0x8762B0 | Poké Ball | Pokéball | Pokéball | déjà patché |
| 0x8762DC | Safari Ball | Safariball | Safariball | déjà patché |
| 0x876308 | Net Ball | Net Ball | Netzball | patch séparé requis |
| 0x876334 | Dive Ball | Dive Ball | Tauchball | patch séparé requis |
| 0x876360 | Nest Ball | Nest Ball | Nestball | patch séparé requis |
| 0x87638C | Repeat Ball | Repeat Ball | Wiederball | patch séparé requis |
| 0x8763B8 | Timer Ball | Timer Ball | Timerball | patch séparé requis |
| 0x8763E4 | Luxury Ball | Luxury Ball | Luxusball | patch séparé requis |
| 0x876410 | Premier Ball | Premier Ball | Premierball | patch séparé requis |
| 0x87643C | Potion | Potion | Trank | patch séparé requis |
| 0x876468 | Antidote | Antidote | Gegengift | patch séparé requis |
| 0x876494 | Burn Heal | Burn Heal | Feuerheiler | patch séparé requis |
| 0x8764C0 | Ice Heal | Ice Heal | Eisheiler | patch séparé requis |
| 0x8764EC | Awakening | Awakening | Aufwecker | patch séparé requis |
| 0x876518 | Parlyz Heal | Parlyz Heal | Para-Heiler | patch séparé requis |
| 0x876544 | Full Restore | Full Restore | Top-Genesung | patch séparé requis |
| 0x876570 | Max Potion | Max Potion | Top-Trank | patch séparé requis |
| 0x87659C | Hyper Potion | Hyper Potion | Hypertrank | patch séparé requis |
| 0x8765C8 | Super Potion | Super Potion | Supertrank | patch séparé requis |
| 0x8765F4 | Full Heal | Full Heal | Hyperheiler | patch séparé requis |
| 0x876620 | Revive | Revive | Beleber | patch séparé requis |
| 0x87664C | Max Revive | Max Revive | Top-Beleber | patch séparé requis |
| 0x876678 | Fresh Water | Fresh Water | Tafelwasser | patch séparé requis |
| 0x8766A4 | Soda Pop | Soda Pop | Sprudel | patch séparé requis |
| 0x8766D0 | Lemonade | Lemonade | Limonade | patch séparé requis |
| 0x8766FC | Moomoo Milk | Moomoo Milk | Kuhmuh-Milch | patch séparé requis |
| 0x876728 | EnergyPowder | EnergyPowder | Energiestaub | patch séparé requis |
| 0x876754 | Energy Root | Energy Root | Kraftwurzel | patch séparé requis |
| 0x876780 | Heal Powder | Heal Powder | Heilpuder | patch séparé requis |
| 0x8767AC | Revival Herb | Revival Herb | Vitalkraut | patch séparé requis |
| 0x8767D8 | Ether | Ether | Äther | patch séparé requis |
| 0x876804 | Max Ether | Max Ether | Top-Äther | patch séparé requis |
| 0x876830 | Elixir | Elixir | Elixier | patch séparé requis |
| 0x87685C | Max Elixir | Max Elixir | Top-Elixier | patch séparé requis |
| 0x876888 | Lava Cookie | Lava Cookie | Lavakeks | patch séparé requis |
| 0x8768B4 | Blue Flute | Blue Flute | Blaue Flöte | patch séparé requis |
| 0x8768E0 | Yellow Flute | Yellow Flute | Gelbe Flöte | patch séparé requis |
| 0x87690C | Red Flute | Red Flute | Rote Flöte | patch séparé requis |
| 0x876938 | Black Flute | Black Flute | Schwarze Flöte | patch séparé requis |
| 0x876964 | White Flute | White Flute | Weiße Flöte | patch séparé requis |
| 0x876990 | Berry Juice | Berry Juice | Beerensaft | patch séparé requis |
| 0x8769BC | Sacred Ash | Sacred Ash | Zauberasche | patch séparé requis |
| 0x8769E8 | Sea Salt | Sea Salt | Meersalz | patch séparé requis |
| 0x876A14 | Sea Shell | Sea Shell | Seemuschel | patch séparé requis |
| 0x876A40 | Red Shard | Red Shard | Purpurstück | patch séparé requis |
| 0x876A6C | Blue Shard | Blue Shard | Indigostück | patch séparé requis |
| 0x876A98 | Yellow Shard | Yellow Shard | Gelbstück | patch séparé requis |
| 0x876AC4 | Green Shard | Green Shard | Grünstück | patch séparé requis |
| 0x876AF0 | Park Ball | Park Ball | Parkball | patch séparé requis |
| 0x876B1C | Cherish Ball | Cherish Ball | Jubelball | patch séparé requis |
| 0x876B74 | Life Orb | Life Orb | Leben-Orb | patch séparé requis |
| 0x876BA0 | Toxic Orb | Toxic Orb | Toxik-Orb | patch séparé requis |
| 0x876BCC | Flame Orb | Flame Orb | Heiß-Orb | patch séparé requis |
| 0x876BF8 | Black Sludge | Black Sludge | Giftschleim | patch séparé requis |
| 0x876C24 | Max Powder | Max Powder | Dyna-Pulver | patch séparé requis |
| 0x876C50 | Dusk Ball | Dusk Ball | Finsterball | patch séparé requis |
| 0x876C7C | Heal Ball | Heal Ball | Heilball | patch séparé requis |
| 0x876CA8 | Quick Ball | Quick Ball | Flottball | patch séparé requis |
| 0x876CD4 | HP Up | KP-Plus | KP-Plus | déjà patché |
| 0x876D00 | Protein | Protein | Protein | terme légitime |
| 0x876D2C | Iron | Iron | Eisen | patch séparé requis |
| 0x876D58 | Carbos | Carbos | Carbon | patch séparé requis |
| 0x876D84 | Calcium | Calcium | Kalzium | patch séparé requis |
| 0x876DB0 | Rare Candy | Rare Candy | Sonderbonbon | patch séparé requis |
| 0x876DDC | PP Up | PP Up | AP-Plus | patch séparé requis |
| 0x876E08 | Zinc | Zinc | Zink | patch séparé requis |
| 0x876E34 | PP Max | PP Max | AP-Top | patch séparé requis |
| 0x876E60 | Honey | Honey | Honig | patch séparé requis |
| 0x876E8C | Guard Spec. | Guard Spec. | Megablock | patch séparé requis |
| 0x876EB8 | Dire Hit | Dire Hit | Angriffplus | patch séparé requis |
| 0x876EE4 | X Attack | X Attack | X-Angriff | patch séparé requis |
| 0x876F10 | X Defense | X Defense | X-Verteidigung | patch séparé requis |
| 0x876F3C | X Speed | X Speed | X-Initiative | patch séparé requis |
| 0x876F68 | X Accuracy | X Accuracy | X-Genauigkeit | patch séparé requis |
| 0x876F94 | X Sp. Atk | X Sp. Atk | X-Sp.-Ang. | patch séparé requis |
| 0x876FC0 | Poké Doll | Poké Doll | Poképuppe | patch séparé requis |
| 0x876FEC | Fluffy Tail | Fluffy Tail | Eneco-Rute | patch séparé requis |
| 0x877018 | X Sp. Def | X Sp. Def | X-Sp.-Vert. | patch séparé requis |
| 0x877044 | Super Repel | Super Repel | Superschutz | patch séparé requis |
| 0x877070 | Max Repel | Max Repel | Top-Schutz | patch séparé requis |
| 0x87709C | Escape Rope | Escape Rope | Fluchtseil | patch séparé requis |
| 0x8770C8 | Repel | Repel | Schutz | patch séparé requis |
| 0x87714C | Dream Mist | Dream Mist | Traumnebel | patch séparé requis |
| 0x877178 | Light Clay | Lichtlehm | Lichtlehm | déjà patché |
| 0x8771A4 | Link Stone | Link Stone | Tauschstein | patch séparé requis |
| 0x8771D0 | Magma Stone | Magma Stone | Magmastein | patch séparé requis |
| 0x8771FC | Sun Stone | Sonnenstein | Sonnenstein | déjà patché |
| 0x877228 | Moon Stone | Mondstein | Mondstein | déjà patché |
| 0x877254 | Fire Stone | Feuerstein | Feuerstein | déjà patché |
| 0x877280 | Thunderstone | Donnerstein | Donnerstein | déjà patché |
| 0x8772AC | Water Stone | Wasserstein | Wasserstein | déjà patché |
| 0x8772D8 | Leaf Stone | Blattstein | Blattstein | déjà patché |
| 0x877304 | Dusk Stone | Finsterstein | Finsterstein | déjà patché |
| 0x877330 | Dawn Stone | Funkelstein | Funkelstein | déjà patché |
| 0x87735C | Shiny Stone | Leuchtstein | Leuchtstein | déjà patché |
| 0x877388 | Oval Stone | Ovaler Stein | Ovaler Stein | déjà patché |
| 0x8773B4 | TinyMushroom | Minipilz | Minipilz | déjà patché |
| 0x8773E0 | Big Mushroom | Riesenpilz | Riesenpilz | déjà patché |
| 0x87740C | Ice Stone | Eisstein | Eisstein | déjà patché |
| 0x877438 | Pearl | Perle | Perle | déjà patché |
| 0x877464 | Big Pearl | Riesenperle | Riesenperle | déjà patché |
| 0x877490 | Stardust | Sternenstaub | Sternenstaub | déjà patché |
| 0x8774BC | Star Piece | Star Piece | Sternenstück | patch séparé requis |
| 0x8774E8 | Nugget | Nugget | Nugget | terme légitime |
| 0x877514 | Heart Scale | Herzschuppe | Herzschuppe | déjà patché |
| 0x877540 | Protector | Schützer | Schützer | déjà patché |
| 0x87756C | Magmarizer | Magmaisierer | Magmaisierer | déjà patché |
| 0x877598 | Rare Bone | Steinknochen | Steinknochen | déjà patché |
| 0x8775C4 | Prism Scale | Schönschuppe | Schönschuppe | déjà patché |
| 0x8775F0 | Sachet | Sachet | Duftbeutel | patch séparé requis |
| 0x87761C | Whip Dream | Sahnehäubchen | Sahnehäubchen | déjà patché |
| 0x877648 | Enigma Berry | Enigmabeere | Enigmabeere | déjà patché |
| 0x877674 | Mega Cuff | Mega Cuff | Mega-Armband | patch séparé requis |
| 0x8776A0 | Mega Tiara | Mega Tiara | Mega-Diadem | patch séparé requis |
| 0x8776CC | Orange Mail | Zigzagbrief | Zigzagbrief | déjà patché |
| 0x8776F8 | Harbor Mail | Hafenbrief | Hafenbrief | déjà patché |
| 0x877724 | Glitter Mail | Glitter Mail | Glitzerbrief | patch séparé requis |
| 0x877750 | Mech Mail | Eilbrief | Eilbrief | déjà patché |
| 0x87777C | Wood Mail | Waldbrief | Waldbrief | déjà patché |
| 0x8777A8 | Wave Mail | Wellenbrief | Wellenbrief | déjà patché |
| 0x8777D4 | Bead Mail | Perlenbrief | Perlenbrief | déjà patché |
| 0x877800 | Shadow Mail | Dunkelbrief | Dunkelbrief | déjà patché |
| 0x87782C | Tropic Mail | Tropenbrief | Tropenbrief | déjà patché |
| 0x877858 | Dream Mail | Traumbrief | Traumbrief | déjà patché |
| 0x877884 | Fab Mail | Fab Mail | Edelbrief | patch séparé requis |
| 0x8778B0 | Retro Mail | Retrobrief | Retrobrief | déjà patché |
| 0x8778DC | Cheri Berry | Amrenabeere | Amrenabeere | déjà patché |
| 0x877908 | Chesto Berry | Maronbeere | Maronbeere | déjà patché |
| 0x877934 | Pecha Berry | Pirsifbeere | Pirsifbeere | déjà patché |
| 0x877960 | Rawst Berry | Fragiabeere | Fragiabeere | déjà patché |
| 0x87798C | Aspear Berry | Wilbirbeere | Wilbirbeere | déjà patché |
| 0x8779B8 | Leppa Berry | Jonagobeere | Jonagobeere | déjà patché |
| 0x8779E4 | Oran Berry | Sinelbeere | Sinelbeere | déjà patché |
| 0x877A10 | Persim Berry | Persimbeere | Persimbeere | déjà patché |
| 0x877A3C | Lum Berry | Prunusbeere | Prunusbeere | déjà patché |
| 0x877A68 | Sitrus Berry | Tsitrubeere | Tsitrubeere | déjà patché |
| 0x877A94 | Figy Berry | Giefebeere | Giefebeere | déjà patché |
| 0x877AC0 | Wiki Berry | Wikibeere | Wikibeere | déjà patché |
| 0x877AEC | Mago Berry | Magobeere | Magobeere | déjà patché |
| 0x877B18 | Aguav Berry | Gauvebeere | Gauvebeere | déjà patché |
| 0x877B44 | Iapapa Berry | Yapabeere | Yapabeere | déjà patché |
| 0x877B70 | Razz Berry | Himmihbeere | Himmihbeere | déjà patché |
| 0x877B9C | Bluk Berry | Morbbeere | Morbbeere | déjà patché |
| 0x877BC8 | Nanab Berry | Nanabbeere | Nanabbeere | déjà patché |
| 0x877BF4 | Wepear Berry | Nirbebeere | Nirbebeere | déjà patché |
| 0x877C20 | Pinap Berry | Sananabeere | Sananabeere | déjà patché |
| 0x877C4C | Pomeg Berry | Granabeere | Granabeere | déjà patché |
| 0x877C78 | Kelpsy Berry | Setangbeere | Setangbeere | déjà patché |
| 0x877CA4 | Qualot Berry | Qualotbeere | Qualotbeere | déjà patché |
| 0x877CD0 | Hondew Berry | Honmelbeere | Honmelbeere | déjà patché |
| 0x877CFC | Grepa Berry | Labrusbeere | Labrusbeere | déjà patché |
| 0x877D28 | Tamato Berry | Tamotbeere | Tamotbeere | déjà patché |
| 0x877D54 | Cornn Berry | Saimbeere | Saimbeere | déjà patché |
| 0x877D80 | Magost Berry | Magostbeere | Magostbeere | déjà patché |
| 0x877DAC | Rabuta Berry | Rabutabeere | Rabutabeere | déjà patché |
| 0x877DD8 | Nomel Berry | Tronzibeere | Tronzibeere | déjà patché |
| 0x877E04 | Spelon Berry | Kiwanbeere | Kiwanbeere | déjà patché |
| 0x877E30 | Pamtre Berry | Pallmbeere | Pallmbeere | déjà patché |
| 0x877E5C | Watmel Berry | Wasmelbeere | Wasmelbeere | déjà patché |
| 0x877E88 | Durin Berry | Durinbeere | Durinbeere | déjà patché |
| 0x877EB4 | Belue Berry | Myrtilbeere | Myrtilbeere | déjà patché |
| 0x877EE0 | Liechi Berry | Lydzibeere | Lydzibeere | déjà patché |
| 0x877F0C | Ganlon Berry | Linganbeere | Linganbeere | déjà patché |
| 0x877F38 | Salac Berry | Salkabeere | Salkabeere | déjà patché |
| 0x877F64 | Petaya Berry | Tahaybeere | Tahaybeere | déjà patché |
| 0x877F90 | Apicot Berry | Apikobeere | Apikobeere | déjà patché |
| 0x877FBC | Lansat Berry | Lansatbeere | Lansatbeere | déjà patché |
| 0x877FE8 | Starf Berry | Krambobeere | Krambobeere | déjà patché |
| 0x878040 | Choice Band | Wahlband | Wahlband | déjà patché |
| 0x87806C | Choice Specs | Choice Specs | Wahlbrille | patch séparé requis |
| 0x878098 | Choice Scarf | Choice Scarf | Wahlschal | patch séparé requis |
| 0x8780F0 | White Herb | Schlohkraut | Schlohkraut | déjà patché |
| 0x87811C | Macho Brace | Machoband | Machoband | déjà patché |
| 0x878148 | Exp. Share | EP-Teiler | EP-Teiler | déjà patché |
| 0x878174 | Quick Claw | Flinkklaue | Flinkklaue | déjà patché |
| 0x8781A0 | Soothe Bell | Sanftglocke | Sanftglocke | déjà patché |
| 0x8781CC | Mental Herb | Mentalkraut | Mentalkraut | déjà patché |
| 0x878224 | King's Rock | King-Stein | King-Stein | déjà patché |
| 0x87827C | Amulet Coin | Münzamulett | Münzamulett | déjà patché |
| 0x8782A8 | Cleanse Tag | Schutzband | Schutzband | déjà patché |
| 0x8782D4 | Soul Dew | Soul Dew | Seelentau | patch séparé requis |
| 0x878358 | Smoke Ball | Rauchball | Rauchball | déjà patché |
| 0x878384 | Everstone | Ewigstein | Ewigstein | déjà patché |
| 0x8783B0 | Focus Band | Fokusband | Fokusband | déjà patché |
| 0x8783DC | Lucky Egg | Lucky Egg | Glücks-Ei | patch séparé requis |
| 0x878408 | Scope Lens | Scope-Linse | Scope-Linse | déjà patché |
| 0x878434 | Metal Coat | Metallmantel | Metallmantel | déjà patché |
| 0x878460 | Leftovers | Leftovers | Überreste | patch séparé requis |
| 0x87848C | Dragon Scale | Drachenhaut | Drachenhaut | déjà patché |
| 0x8784B8 | Light Ball | Light Ball | Kugelblitz | patch séparé requis |
| 0x8784E4 | Soft Sand | Pudersand | Pudersand | déjà patché |
| 0x878510 | Hard Stone | Harter Stein | Granitstein | patch séparé requis |
| 0x87853C | Miracle Seed | Wundersaat | Wundersaat | déjà patché |
| 0x878594 | Black Belt | Schwarzgurt | Schwarzgurt | déjà patché |
| 0x8785C0 | Magnet | Magnet | Magnet | terme légitime |
| 0x8785EC | Mystic Water | Zauberwasser | Zauberwasser | déjà patché |
| 0x878618 | Sharp Beak | Spitz.Schnab. | Spitz.Schnab. | déjà patché |
| 0x878644 | Poison Barb | Giftstich | Giftstich | déjà patché |
| 0x87869C | Spell Tag | Bannsticker | Bannsticker | déjà patché |
| 0x8786F4 | Charcoal | Holzkohle | Holzkohle | déjà patché |
| 0x878720 | Dragon Fang | Drachenzahn | Drachenzahn | déjà patché |
| 0x87874C | Silk Scarf | Seidenschal | Seidenschal | déjà patché |
| 0x878778 | Up-Grade | Up-Grade | Up-Grade | terme légitime |
| 0x8787A4 | Shell Bell | Muschelglocke | Muschelglocke | déjà patché |
| 0x8787D0 | Sea Incense | Seerauch | Seerauch | déjà patché |
| 0x8787FC | Lax Incense | Laxrauch | Laxrauch | déjà patché |
| 0x878828 | Lucky Punch | Lucky Punch | Lucky Punch | terme légitime |
| 0x878854 | Metal Powder | Metallstaub | Metallstaub | déjà patché |
| 0x878880 | Thick Club | Kampfknochen | Kampfknochen | déjà patché |
| 0x8788AC | Leek | Lauchstange | Lauchstange | déjà patché |
| 0x8788D8 | Rocky Helmet | Beulenhelm | Beulenhelm | déjà patché |
| 0x878904 | Weak Policy | Weak Policy | Schwächenschutz | patch séparé requis |
| 0x878930 | Pearl String | Pearl String | Triperle | patch séparé requis |
| 0x87895C | Big Nugget | Riesennugget | Riesennugget | déjà patché |
| 0x878988 | Razor Claw | Scharfklaue | Scharfklaue | déjà patché |
| 0x8789B4 | Razor Fang | Scharfzahn | Scharfzahn | déjà patché |
| 0x8789E0 | Reaper Cloth | Düsterumhang | Düsterumhang | déjà patché |
| 0x878A0C | Dubious Disc | Dubious Disc | Dubiosdisc | patch séparé requis |
| 0x878A38 | Electirizer | Stromisierer | Stromisierer | déjà patché |
| 0x878A64 | Expert Belt | Expertengurt | Expertengurt | déjà patché |
| 0x878A90 | Power Herb | Energiekraut | Energiekraut | déjà patché |
| 0x878ABC | Wide Lens | Großlinse | Großlinse | déjà patché |
| 0x878AE8 | Zoom Lens | Zoomlinse | Zoomlinse | déjà patché |
| 0x878B14 | Destiny Knot | Fatumknoten | Fatumknoten | déjà patché |
| 0x878B40 | Smooth Rock | Glattbrocken | Glattbrocken | déjà patché |
| 0x878B6C | Damp Rock | Nassbrocken | Nassbrocken | déjà patché |
| 0x878B98 | Heat Rock | Heißbrocken | Heißbrocken | déjà patché |
| 0x878BC4 | Icy Rock | Eisbrocken | Eisbrocken | déjà patché |
| 0x878BF0 | Power Bracer | Power Bracer | Machtreif | patch séparé requis |
| 0x878C1C | Power Belt | Machtgurt | Machtgurt | déjà patché |
| 0x878C48 | Power Lens | Power Lens | Machtlinse | patch séparé requis |
| 0x878C74 | Power Band | Power Band | Machtband | patch séparé requis |
| 0x878CA0 | Power Anklet | Power Anklet | Machtkette | patch séparé requis |
| 0x878CCC | Power Weight | Power Weight | Machtgewicht | patch séparé requis |
| 0x878CF8 | Big Root | Großwurzel | Großwurzel | déjà patché |
| 0x878D24 | Odd Keystone | Odd Keystone | Spiritkern | patch séparé requis |
| 0x878D50 | Luck Incense | Glücksrauch | Glücksrauch | déjà patché |
| 0x878D7C | Full Incense | Lahmrauch | Lahmrauch | déjà patché |
| 0x878DA8 | Odd Incense | Odd Incense | Schrägrauch | patch séparé requis |
| 0x878DD4 | Pure Incense | Scheuchrauch | Scheuchrauch | déjà patché |
| 0x878E00 | Rock Incense | Steinrauch | Steinrauch | déjà patché |
| 0x878E2C | Rose Incense | Rosenrauch | Rosenrauch | déjà patché |
| 0x878E58 | Wave Incense | Wellenrauch | Wellenrauch | déjà patché |
| 0x878E84 | Mach Bike | Eilrad | Eilrad | déjà patché |
| 0x878EB0 | Coin Case | Münzkorb | Münzkorb | déjà patché |
| 0x878F08 | Old Rod | Angel | Angel | déjà patché |
| 0x878F34 | Good Rod | Profiangel | Profiangel | déjà patché |
| 0x878F60 | Super Rod | Superangel | Superangel | déjà patché |
| 0x878F8C | SS. Ticket | SS. Ticket | Bootsticket | patch séparé requis |
| 0x878FB8 | Grubby Hanky | Grubby Hanky | Schnäuztuch | patch séparé requis |
| 0x878FE4 | Uniform | Uniform | Uniform | terme légitime |
| 0x879010 | Dynamax Band | Dynamax Band | Dynamax-Band | patch séparé requis |
| 0x879068 | Fashion Case | Fashion Case | Modekoffer | patch séparé requis |
| 0x879094 | Basement Key | Basement Key | Kelleröffner | patch séparé requis |
| 0x8790EC | Poké Ball | Pokéball | Pokéball | déjà patché |
| 0x879118 | Letter | Brief an Troy | Brief an Troy | déjà patché |
| 0x879144 | Eon Ticket | Äon-Ticket | Äon-Ticket | déjà patché |
| 0x879170 | Red Orb | Red Orb | Roter Edelstein | patch séparé requis |
| 0x87919C | Blue Orb | Blue Orb | Blauer Edelstein | patch séparé requis |
| 0x8791C8 | Stat Scanner | Stat Scanner | Werte-Scanner | patch séparé requis |
| 0x8791F4 | Go-Goggles | Go-Goggles | Wüstenbrille | patch séparé requis |
| 0x879220 | Meteorite | Meteorit | Meteorit | déjà patché |
| 0x87924C | Barrier Key | Barrier Key | Barrierenpass | patch séparé requis |
| 0x879278 | Key Card: 2 | Key Card: 2 | Schlüssel: 2 | patch séparé requis |
| 0x8792A4 | Key Card: 3 | Key Card: 3 | Schlüssel: 3 | patch séparé requis |
| 0x8792D0 | Rm. 6 Key | Rm. 6 Key | K6-Schlüssel | patch séparé requis |
| 0x8792FC | Storage Key | Storage Key | Lagerschlüssel | patch séparé requis |
| 0x879328 | Root Fossil | Root Fossil | Wurzelfossil | patch séparé requis |
| 0x879354 | Claw Fossil | Claw Fossil | Klauenfossil | patch séparé requis |
| 0x879380 | Devon Scope | Devon-Scope | Devon-Scope | déjà patché |
| 0x8793AC | TM01 | TM01 | TM01 | terme légitime |
| 0x8793D8 | TM02 | TM02 | TM02 | terme légitime |
| 0x879404 | TM03 | TM03 | TM03 | terme légitime |
| 0x879430 | TM04 | TM04 | TM04 | terme légitime |
| 0x87945C | TM05 | TM05 | TM05 | terme légitime |
| 0x879488 | TM06 | TM06 | TM06 | terme légitime |
| 0x8794B4 | TM07 | TM07 | TM07 | terme légitime |
| 0x8794E0 | TM08 | TM08 | TM08 | terme légitime |
| 0x87950C | TM09 | TM09 | TM09 | terme légitime |
| 0x879538 | TM10 | TM10 | TM10 | terme légitime |
| 0x879564 | TM11 | TM11 | TM11 | terme légitime |
| 0x879590 | TM12 | TM12 | TM12 | terme légitime |
| 0x8795BC | TM13 | TM13 | TM13 | terme légitime |
| 0x8795E8 | TM14 | TM14 | TM14 | terme légitime |
| 0x879614 | TM15 | TM15 | TM15 | terme légitime |
| 0x879640 | TM16 | TM16 | TM16 | terme légitime |
| 0x87966C | TM17 | TM17 | TM17 | terme légitime |
| 0x879698 | TM18 | TM18 | TM18 | terme légitime |
| 0x8796C4 | TM19 | TM19 | TM19 | terme légitime |
| 0x8796F0 | TM20 | TM20 | TM20 | terme légitime |
| 0x87971C | TM21 | TM21 | TM21 | terme légitime |
| 0x879748 | TM22 | TM22 | TM22 | terme légitime |
| 0x879774 | TM23 | TM23 | TM23 | terme légitime |
| 0x8797A0 | TM24 | TM24 | TM24 | terme légitime |
| 0x8797CC | TM25 | TM25 | TM25 | terme légitime |
| 0x8797F8 | TM26 | TM26 | TM26 | terme légitime |
| 0x879824 | TM27 | TM27 | TM27 | terme légitime |
