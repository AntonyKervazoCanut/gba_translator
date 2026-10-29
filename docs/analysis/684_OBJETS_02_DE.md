# B-684 — Qualification DE objets-02

Qualification limitée aux **300 offsets exclusifs** du ticket, le 29 octobre 2026.
Aucun audit global, aucune modification de traduction, de patch ou de ressource de jeu.

## Résultat

- **101 noms déjà patchés** et vérifiés dans le build DE.
- **95 termes légitimes** : 93 TM numérotées, ADM (identifiant Unbound), Gracidea.
- **104 besoins de patch séparé** : 103 noms encore anglais et Beerentasche, à remplacer par le nom officiel Beerentüte.
- Le ticket autonome **B-1027** porte ces 104 corrections et le raccordement
  dédié ; B-1026 couvre le lot objets-01, sans chevauchement.
- **0 fragment mort** : les 300 noms sont des cellules de la table vivante.
- Les 300 valeurs EN du corpus correspondent aux noms de la ROM canonique.
  Les 300 offsets sont absents des deux combined FR/DE, de l’extraction EN
  et du JSON DE d’injection. Il n’existe donc aucune dernière occurrence DE à corriger.
  Ajouter des lignes au combined seul ne raccorde pas ces noms au build.

Le fichier JSON associé donne, pour **chaque offset**, la décision, les trois
corpus, les noms EN et DE réellement décodés, les cellules binaires complètes,
les références brutes, les pointeurs de description avant/après build, le nom
DE officiel ou une proposition explicitement non officielle, et les budgets.
Les propositions du rapport ne sont pas des traductions injectées.

## Preuves techniques et exclusions

ROM EN canonique vérifiée par SHA256 :
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

La routine à `0x9A8CA` multiplie l’index par `0x2C` et charge la base
`0x876200` via le littéral `0x9A8D8` ; mêmes octets dans le build DE.
Chaque offset du lot est `base + index * 44`. Le nom occupe 14 octets,
terminateur FF inclus, suivi des métadonnées ; la description est pointée à +20.
La base historique `0x876074` des commentaires du patch est décalée de neuf
structs, mais appartient à la même grille : son balayage atteint ces cellules.
L’absence de pointeur direct vers chaque nom ne les rend pas morts.
Les occurrences brutes d’une adresse dans la ROM sont consignées sans les
présenter comme des appels prouvés ; la preuve de lecture est la routine indexée.

Les 300 cellules EN et DE ont leur terminateur dans les 14 octets.
Aucun placeholder ni contrôle de nom, donc aucun ordre de variables à restaurer,
aucun alias brut/accolade, aucune commande `\n`, `\l` ou `\p` omise.
Largeur maximale mesurée : **74 pixels** avec les avances de police normale du
projet. Cette mesure n’est pas une validation de toutes les phrases dynamiques
contenant un nom d’objet. Les métadonnées hors pointeur de description sont
identiques à EN pour les 300 structs ; les 300 pointeurs de description restent
dans la ROM. Aucune relocalisation de nom par ce ticket.

Pas de dialogues ni de Pokédex dans le lot : scène, registre du personnage,
Sohn/Tochter et fidélité d’espèce sont sans objet. `0x7A823B` est hors périmètre.
Les noms de Méga-Gemmes sont des noms d’objets officiels : la conservation des
noms anglais d’espèces par le build ne justifie pas de conserver Venusaurite.

`Mitgl.Karte` est accepté : abréviation officielle historique, explicitement
versionnée dans le glossaire. Les traductions Unbound existantes Paket, Sendung,
Kostümbox et Mobil-PC sont cohérentes avec leur fonction. Les propositions
Grimy Socks, Key Card: 1, Time Turner, Baby Monitor, Motorcycle et Notebook
ont été confrontées aux descriptions canoniques consignées dans le JSON.
ADM reste le sigle propre du dispositif Unbound. Mega Earing nécessite une
localisation cohérente malgré sa description générique de bague.

Six noms officiels proposés dépassent la cellule de 14 octets (FF inclus) :
Ultranecronium Z, Aerodactylonit, Illumina-Galette, Feldbeschichtung,
Silberkronkorken et Purpurner Nektar. Le ticket technique devra choisir des
abréviations versionnées ou une relocalisation d’union sûre, puis vérifier le
sac et les messages de ramassage. Les autres propositions tiennent en octets ;
leur rendu reste à valider après raccordement.

## Sources

- `languages/de/data/official_terminology.yaml`, dont les abréviations contraintes.
- [PokeAPI item_names.csv, révision figée du glossaire](https://raw.githubusercontent.com/PokeAPI/pokeapi/c0a9bc75af3a455cdfa27dde21e4ec95aedd3f25/data/v2/csv/item_names.csv), colonnes langues 9/6/5.
- ROM canonique EN, routine de lecture et descriptions des objets.
- `languages/de/patches/item_names.py` et `fixed_table_names.py`, vérifiés contre le résultat binaire.

Les alias CFRU abrégés sont résolus explicitement (Charizite, Blastoisite,
Kangaskhite, Aerodactite, Houndoomite, Necrozium Z, Lumiose Gale, Ragecandybar,
Protect Pads, Terrain Ext., Purp Nectar, Adrenal Orb, Marang Berry, VS Seeker).
Les anciens noms Wing correspondent aux noms Feather de la source récente.
Necrozium Z est identifié par sa description : permet Ultra Burst à Necrozma.

## Validation locale

- `make build-de` : réussi ; contrôle sur la ROM finale, pas simulation du patch.
- `make test-python` : 3508 réussis, 97 ignorés, 1977 désélectionnés ; aucun échec.
  Les ignorés ne sont pas comptés comme des vérifications réussies.
- Hash FR principal avant travail :
  `74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
- Tests unitaires associés : intégrité de la liste exclusive, décodage des
  preuves binaires, bornes de cellule, classification et budgets des propositions.

## Non vérifié

Aucun écran de gameplay n’est modifié par ce ticket documentaire ; aucun test
Playwright ni capture ne prétend valider les 104 corrections futures.
Le parcours manuel de tous les objets, les usages scriptés de chaque objet et
les largeurs de phrases avec variables restent à vérifier dans le ticket de patch.
Les chaînes de description sont utilisées comme contexte, sans audit ni correction
hors des 300 noms autorisés. Aucune nouvelle protection combined n’est nécessaire
puisqu’aucune ligne de traduction n’est ajoutée ou modifiée.

## Décisions exhaustives

« Patch séparé » signifie besoin confirmé, **pas correction effectuée**.

| Offset | EN canonique | DE injecté | Décision | DE proposé / retenu |
|---|---|---|---|---|
| 0x879850 | TM28 | TM28 | Terme légitime | TM28 |
| 0x87987C | TM29 | TM29 | Terme légitime | TM29 |
| 0x8798A8 | TM30 | TM30 | Terme légitime | TM30 |
| 0x8798D4 | TM31 | TM31 | Terme légitime | TM31 |
| 0x879900 | TM32 | TM32 | Terme légitime | TM32 |
| 0x87992C | TM33 | TM33 | Terme légitime | TM33 |
| 0x879958 | TM34 | TM34 | Terme légitime | TM34 |
| 0x879984 | TM35 | TM35 | Terme légitime | TM35 |
| 0x8799B0 | TM36 | TM36 | Terme légitime | TM36 |
| 0x8799DC | TM37 | TM37 | Terme légitime | TM37 |
| 0x879A08 | TM38 | TM38 | Terme légitime | TM38 |
| 0x879A34 | TM39 | TM39 | Terme légitime | TM39 |
| 0x879A60 | TM40 | TM40 | Terme légitime | TM40 |
| 0x879A8C | TM41 | TM41 | Terme légitime | TM41 |
| 0x879AB8 | TM42 | TM42 | Terme légitime | TM42 |
| 0x879AE4 | TM43 | TM43 | Terme légitime | TM43 |
| 0x879B10 | TM44 | TM44 | Terme légitime | TM44 |
| 0x879B3C | TM45 | TM45 | Terme légitime | TM45 |
| 0x879B68 | TM46 | TM46 | Terme légitime | TM46 |
| 0x879B94 | TM47 | TM47 | Terme légitime | TM47 |
| 0x879BC0 | TM48 | TM48 | Terme légitime | TM48 |
| 0x879BEC | TM49 | TM49 | Terme légitime | TM49 |
| 0x879C18 | TM50 | TM50 | Terme légitime | TM50 |
| 0x879C44 | TM51 | TM51 | Terme légitime | TM51 |
| 0x879C70 | TM52 | TM52 | Terme légitime | TM52 |
| 0x879C9C | TM53 | TM53 | Terme légitime | TM53 |
| 0x879CC8 | TM54 | TM54 | Terme légitime | TM54 |
| 0x879CF4 | TM55 | TM55 | Terme légitime | TM55 |
| 0x879D20 | TM56 | TM56 | Terme légitime | TM56 |
| 0x879D4C | TM57 | TM57 | Terme légitime | TM57 |
| 0x879D78 | TM58 | TM58 | Terme légitime | TM58 |
| 0x879DD0 | Costume Box | Kostümbox | Déjà patché | Kostümbox |
| 0x879DFC | Parcel | Paket | Déjà patché | Paket |
| 0x879E28 | Jade Orb | Jade Orb | Patch séparé | Grüne Kugel |
| 0x879E54 | Grimy Socks | Grimy Socks | Patch séparé | Drecksocken |
| 0x879E80 | Package | Sendung | Déjà patché | Sendung |
| 0x879EAC | Mega Ring | Mega Ring | Patch séparé | Mega-Ring |
| 0x879ED8 | Old Amber | Altbernstein | Déjà patché | Altbernstein |
| 0x879F04 | Key Card: 1 | Key Card: 1 | Patch séparé | Schlüssel 1 |
| 0x879F30 | Time Turner | Time Turner | Patch séparé | Zeitwender |
| 0x879F5C | Helix Fossil | Helixfossil | Déjà patché | Helixfossil |
| 0x879F88 | Dome Fossil | Domfossil | Déjà patché | Domfossil |
| 0x879FB4 | Baby Monitor | Baby Monitor | Patch séparé | Pensionsgerät |
| 0x879FE0 | Motorcycle | Motorcycle | Patch séparé | Motorrad |
| 0x87A00C | Town Map | Karte | Déjà patché | Karte |
| 0x87A038 | VS Seeker | Kampffahnder | Déjà patché | Kampffahnder |
| 0x87A090 | TM Case | TM-Box | Déjà patché | TM-Box |
| 0x87A0BC | Berry Pouch | Beerentasche | Patch séparé | Beerentüte |
| 0x87A0E8 | ADM | ADM | Terme légitime | ADM |
| 0x87A114 | Notebook | Notebook | Patch séparé | Notizbuch |
| 0x87A140 | Porta-PC | Mobil-PC | Déjà patché | Mobil-PC |
| 0x87A1F0 | Powder Jar | Puderdöschen | Déjà patché | Puderdöschen |
| 0x87A21C | Lunar Wing | Lunarfeder | Déjà patché | Lunarfeder |
| 0x87A248 | Member Card | Mitgl.Karte | Déjà patché | Mitgl.Karte |
| 0x87A274 | TM59 | TM59 | Terme légitime | TM59 |
| 0x87A2A0 | TM60 | TM60 | Terme légitime | TM60 |
| 0x87A2CC | TM61 | TM61 | Terme légitime | TM61 |
| 0x87A2F8 | TM62 | TM62 | Terme légitime | TM62 |
| 0x87A324 | TM63 | TM63 | Terme légitime | TM63 |
| 0x87A350 | TM64 | TM64 | Terme légitime | TM64 |
| 0x87A37C | TM65 | TM65 | Terme légitime | TM65 |
| 0x87A3A8 | TM66 | TM66 | Terme légitime | TM66 |
| 0x87A3D4 | TM67 | TM67 | Terme légitime | TM67 |
| 0x87A400 | TM68 | TM68 | Terme légitime | TM68 |
| 0x87A42C | TM69 | TM69 | Terme légitime | TM69 |
| 0x87A458 | TM70 | TM70 | Terme légitime | TM70 |
| 0x87A484 | TM71 | TM71 | Terme légitime | TM71 |
| 0x87A4B0 | TM72 | TM72 | Terme légitime | TM72 |
| 0x87A4DC | TM73 | TM73 | Terme légitime | TM73 |
| 0x87A508 | TM74 | TM74 | Terme légitime | TM74 |
| 0x87A534 | TM75 | TM75 | Terme légitime | TM75 |
| 0x87A560 | TM76 | TM76 | Terme légitime | TM76 |
| 0x87A58C | TM77 | TM77 | Terme légitime | TM77 |
| 0x87A5B8 | TM78 | TM78 | Terme légitime | TM78 |
| 0x87A5E4 | TM79 | TM79 | Terme légitime | TM79 |
| 0x87A610 | TM80 | TM80 | Terme légitime | TM80 |
| 0x87A63C | TM81 | TM81 | Terme légitime | TM81 |
| 0x87A668 | TM82 | TM82 | Terme légitime | TM82 |
| 0x87A694 | TM83 | TM83 | Terme légitime | TM83 |
| 0x87A6C0 | TM84 | TM84 | Terme légitime | TM84 |
| 0x87A6EC | TM85 | TM85 | Terme légitime | TM85 |
| 0x87A718 | TM86 | TM86 | Terme légitime | TM86 |
| 0x87A744 | TM87 | TM87 | Terme légitime | TM87 |
| 0x87A770 | TM88 | TM88 | Terme légitime | TM88 |
| 0x87A79C | TM89 | TM89 | Terme légitime | TM89 |
| 0x87A7C8 | TM90 | TM90 | Terme légitime | TM90 |
| 0x87A7F4 | TM91 | TM91 | Terme légitime | TM91 |
| 0x87A820 | TM92 | TM92 | Terme légitime | TM92 |
| 0x87A84C | TM93 | TM93 | Terme légitime | TM93 |
| 0x87A878 | TM94 | TM94 | Terme légitime | TM94 |
| 0x87A8A4 | TM95 | TM95 | Terme légitime | TM95 |
| 0x87A8D0 | TM96 | TM96 | Terme légitime | TM96 |
| 0x87A8FC | TM97 | TM97 | Terme légitime | TM97 |
| 0x87A928 | TM98 | TM98 | Terme légitime | TM98 |
| 0x87A954 | TM99 | TM99 | Terme légitime | TM99 |
| 0x87A980 | TM100 | TM100 | Terme légitime | TM100 |
| 0x87A9AC | TM101 | TM101 | Terme légitime | TM101 |
| 0x87A9D8 | TM102 | TM102 | Terme légitime | TM102 |
| 0x87AA04 | TM103 | TM103 | Terme légitime | TM103 |
| 0x87AA30 | TM104 | TM104 | Terme légitime | TM104 |
| 0x87AA5C | TM105 | TM105 | Terme légitime | TM105 |
| 0x87AA88 | TM106 | TM106 | Terme légitime | TM106 |
| 0x87AAB4 | TM107 | TM107 | Terme légitime | TM107 |
| 0x87AAE0 | TM108 | TM108 | Terme légitime | TM108 |
| 0x87AB0C | TM109 | TM109 | Terme légitime | TM109 |
| 0x87AB38 | TM110 | TM110 | Terme légitime | TM110 |
| 0x87AB64 | TM111 | TM111 | Terme légitime | TM111 |
| 0x87AB90 | TM112 | TM112 | Terme légitime | TM112 |
| 0x87ABBC | TM113 | TM113 | Terme légitime | TM113 |
| 0x87ABE8 | TM114 | TM114 | Terme légitime | TM114 |
| 0x87AC14 | TM115 | TM115 | Terme légitime | TM115 |
| 0x87AC40 | TM116 | TM116 | Terme légitime | TM116 |
| 0x87AC6C | TM117 | TM117 | Terme légitime | TM117 |
| 0x87AC98 | TM118 | TM118 | Terme légitime | TM118 |
| 0x87ACC4 | TM119 | TM119 | Terme légitime | TM119 |
| 0x87ACF0 | TM120 | TM120 | Terme légitime | TM120 |
| 0x87AD1C | HM01 | VM01 | Déjà patché | VM01 |
| 0x87AD48 | HM02 | VM02 | Déjà patché | VM02 |
| 0x87AD74 | HM03 | VM03 | Déjà patché | VM03 |
| 0x87ADA0 | HM04 | VM04 | Déjà patché | VM04 |
| 0x87ADCC | HM05 | VM05 | Déjà patché | VM05 |
| 0x87ADF8 | HM06 | VM06 | Déjà patché | VM06 |
| 0x87AE24 | HM07 | VM07 | Déjà patché | VM07 |
| 0x87AE50 | HM08 | VM08 | Déjà patché | VM08 |
| 0x87AE7C | Necrozium Z | Necrozium Z | Patch séparé | Ultranecronium Z |
| 0x87AEA8 | Venusaurite | Venusaurite | Patch séparé | Bisaflornit |
| 0x87AED4 | Charizite X | Charizite X | Patch séparé | Gluraknit X |
| 0x87AF00 | Charizite Y | Charizite Y | Patch séparé | Gluraknit Y |
| 0x87AF2C | Blastoisite | Blastoisite | Patch séparé | Turtoknit |
| 0x87AF58 | Beedrillite | Beedrillite | Patch séparé | Bibornit |
| 0x87AF84 | Pidgeotite | Pidgeotite | Patch séparé | Taubossnit |
| 0x87AFB0 | Alakazite | Alakazite | Patch séparé | Simsalanit |
| 0x87AFDC | Slowbronite | Slowbronite | Patch séparé | Lahmusnit |
| 0x87B008 | Gengarite | Gengarite | Patch séparé | Gengarnit |
| 0x87B034 | Kangaskhite | Kangaskhite | Patch séparé | Kangamanit |
| 0x87B060 | Pinsirite | Pinsirite | Patch séparé | Pinsirnit |
| 0x87B08C | Gyaradosite | Gyaradosite | Patch séparé | Garadosnit |
| 0x87B0B8 | Aerodactite | Aerodactite | Patch séparé | Aerodactylonit |
| 0x87B0E4 | Mewtwonite X | Mewtwonite X | Patch séparé | Mewtunit X |
| 0x87B110 | Mewtwonite Y | Mewtwonite Y | Patch séparé | Mewtunit Y |
| 0x87B13C | Ampharosite | Ampharosite | Patch séparé | Ampharosnit |
| 0x87B168 | Steelixite | Steelixite | Patch séparé | Stahlosnit |
| 0x87B194 | Scizorite | Scizorite | Patch séparé | Scheroxnit |
| 0x87B1C0 | Heracronite | Heracronite | Patch séparé | Skarabornit |
| 0x87B1EC | Houndoomite | Houndoomite | Patch séparé | Hundemonit |
| 0x87B218 | Tyranitarite | Tyranitarite | Patch séparé | Despotarnit |
| 0x87B244 | Sceptilite | Sceptilite | Patch séparé | Gewaldronit |
| 0x87B270 | Blazikenite | Blazikenite | Patch séparé | Lohgocknit |
| 0x87B29C | Swampertite | Swampertite | Patch séparé | Sumpexnit |
| 0x87B2C8 | Gardevoirite | Gardevoirite | Patch séparé | Guardevoirnit |
| 0x87B2F4 | Sablenite | Sablenite | Patch séparé | Zobirisnit |
| 0x87B320 | Mawilite | Mawilite | Patch séparé | Flunkifernit |
| 0x87B34C | Aggronite | Aggronite | Patch séparé | Stollossnit |
| 0x87B378 | Medichamite | Medichamite | Patch séparé | Meditalisnit |
| 0x87B3A4 | Manectite | Manectite | Patch séparé | Voltensonit |
| 0x87B3D0 | Sharpedonite | Sharpedonite | Patch séparé | Tohaidonit |
| 0x87B3FC | Cameruptite | Cameruptite | Patch séparé | Cameruptnit |
| 0x87B428 | Altarianite | Altarianite | Patch séparé | Altarianit |
| 0x87B454 | Banettite | Banettite | Patch séparé | Banetteonit |
| 0x87B480 | Absolite | Absolite | Patch séparé | Absolnit |
| 0x87B4AC | Glalitite | Glalitite | Patch séparé | Firnontornit |
| 0x87B4D8 | Salamencite | Salamencite | Patch séparé | Brutalandanit |
| 0x87B504 | Metagrossite | Metagrossite | Patch séparé | Metagrossnit |
| 0x87B530 | Latiasite | Latiasite | Patch séparé | Latiasnit |
| 0x87B55C | Latiosite | Latiosite | Patch séparé | Latiosnit |
| 0x87B588 | Lopunnite | Lopunnite | Patch séparé | Schlapornit |
| 0x87B5B4 | Garchompite | Garchompite | Patch séparé | Knakracknit |
| 0x87B5E0 | Lucarionite | Lucarionite | Patch séparé | Lucarionit |
| 0x87B60C | Abomasite | Abomasite | Patch séparé | Rexblisarnit |
| 0x87B638 | Galladite | Galladite | Patch séparé | Galagladinit |
| 0x87B664 | Audinite | Audinite | Patch séparé | Ohrdochnit |
| 0x87B690 | Diancite | Diancite | Patch séparé | Diancienit |
| 0x87B6E8 | Assault Vest | Assault Vest | Patch séparé | Offensivweste |
| 0x87B714 | Eviolite | Evolith | Déjà patché | Evolith |
| 0x87B740 | Fist Plate | Fist Plate | Patch séparé | Fausttafel |
| 0x87B76C | Sky Plate | Sky Plate | Patch séparé | Wolkentafel |
| 0x87B798 | Toxic Plate | Toxic Plate | Patch séparé | Gifttafel |
| 0x87B7C4 | Earth Plate | Earth Plate | Patch séparé | Erdtafel |
| 0x87B7F0 | Stone Plate | Stone Plate | Patch séparé | Steintafel |
| 0x87B81C | Insect Plate | Insect Plate | Patch séparé | Käfertafel |
| 0x87B848 | Spooky Plate | Spooky Plate | Patch séparé | Spuktafel |
| 0x87B874 | Iron Plate | Iron Plate | Patch séparé | Eisentafel |
| 0x87B8A0 | Flame Plate | Flame Plate | Patch séparé | Feuertafel |
| 0x87B8CC | Splash Plate | Splash Plate | Patch séparé | Wassertafel |
| 0x87B8F8 | Meadow Plate | Meadow Plate | Patch séparé | Wiesentafel |
| 0x87B924 | Zap Plate | Zap Plate | Patch séparé | Blitztafel |
| 0x87B950 | Mind Plate | Mind Plate | Patch séparé | Hirntafel |
| 0x87B97C | Icicle Plate | Icicle Plate | Patch séparé | Frosttafel |
| 0x87B9A8 | Draco Plate | Draco Plate | Patch séparé | Dracotafel |
| 0x87B9D4 | Dread Plate | Dread Plate | Patch séparé | Furchttafel |
| 0x87BA00 | Pixie Plate | Pixie Plate | Patch séparé | Feentafel |
| 0x87BA2C | Comet Shard | Comet Shard | Patch séparé | Kometstück |
| 0x87BA84 | Big Malasada | Maxi-Malasada | Déjà patché | Maxi-Malasada |
| 0x87BAB0 | Casteliacone | Casteliacone | Patch séparé | Stratos-Eis |
| 0x87BADC | Lumiose Gale | Lumiose Gale | Patch séparé | Illumina-Galette |
| 0x87BB08 | Ragecandybar | Ragecandybar | Patch séparé | Wutkeks |
| 0x87BB60 | Old Gateau | Old Gateau | Patch séparé | Spezialität |
| 0x87BB8C | Skull Fossil | Kopffossil | Déjà patché | Kopffossil |
| 0x87BBB8 | Armor Fossil | Armor Fossil | Patch séparé | Panzerfossil |
| 0x87BBE4 | Cover Fossil | Cover Fossil | Patch séparé | Schildfossil |
| 0x87BC10 | Plume Fossil | Federfossil | Déjà patché | Federfossil |
| 0x87BC3C | Jaw Fossil | Jaw Fossil | Patch séparé | Kieferfossil |
| 0x87BC68 | Sail Fossil | Flossenfossil | Déjà patché | Flossenfossil |
| 0x87BC94 | Mega Earing | Mega Earing | Patch séparé | Mega-Ohrring |
| 0x87BCC0 | Mega Charm | Mega Charm | Patch séparé | Megaillon |
| 0x87BD18 | Mega Anklet | Mega Anklet | Patch séparé | Mega-Beinreif |
| 0x87BD44 | Mega Pendant | Mega Pendant | Patch séparé | Mega-Anhänger |
| 0x87BD70 | Adamant Orb | Adamant Orb | Patch séparé | Adamant-Orb |
| 0x87BD9C | Lustrous Orb | Lustrous Orb | Patch séparé | Weiß-Orb |
| 0x87BDC8 | Griseous Orb | Griseous Orb | Patch séparé | Platinum-Orb |
| 0x87BDF4 | Gracidea | Gracidea | Terme légitime | Gracidea |
| 0x87BE20 | DNA Splicers | DNA Splicers | Patch séparé | DNS-Keil |
| 0x87BE4C | Reveal Glass | Reveal Glass | Patch séparé | Wahrspiegel |
| 0x87BEA4 | Occa Berry | Koakobeere | Déjà patché | Koakobeere |
| 0x87BED0 | Passho Berry | Foepasbeere | Déjà patché | Foepasbeere |
| 0x87BEFC | Wacan Berry | Kerzalbeere | Déjà patché | Kerzalbeere |
| 0x87BF28 | Rindo Berry | Grindobeere | Déjà patché | Grindobeere |
| 0x87BF54 | Yache Berry | Kiroyabeere | Déjà patché | Kiroyabeere |
| 0x87BF80 | Chople Berry | Rospelbeere | Déjà patché | Rospelbeere |
| 0x87BFAC | Kebia Berry | Grarzbeere | Déjà patché | Grarzbeere |
| 0x87BFD8 | Shuca Berry | Schukebeere | Déjà patché | Schukebeere |
| 0x87C004 | Coba Berry | Kobabeere | Déjà patché | Kobabeere |
| 0x87C030 | Payapa Berry | Pyapabeere | Déjà patché | Pyapabeere |
| 0x87C05C | Tanga Berry | Tanigabeere | Déjà patché | Tanigabeere |
| 0x87C088 | Charti Berry | Chiaribeere | Déjà patché | Chiaribeere |
| 0x87C0B4 | Kasib Berry | Zitarzbeere | Déjà patché | Zitarzbeere |
| 0x87C0E0 | Haban Berry | Terirobeere | Déjà patché | Terirobeere |
| 0x87C10C | Colbur Berry | Burleobeere | Déjà patché | Burleobeere |
| 0x87C138 | Babiri Berry | Babiribeere | Déjà patché | Babiribeere |
| 0x87C164 | Chilan Berry | Latchibeere | Déjà patché | Latchibeere |
| 0x87C190 | Micle Berry | Wunfrubeere | Déjà patché | Wunfrubeere |
| 0x87C1BC | Custap Berry | Eipfelbeere | Déjà patché | Eipfelbeere |
| 0x87C1E8 | Jaboca Berry | Jabocabeere | Déjà patché | Jabocabeere |
| 0x87C214 | Rowap Berry | Roselbeere | Déjà patché | Roselbeere |
| 0x87C240 | Roseli Berry | Hibisbeere | Déjà patché | Hibisbeere |
| 0x87C26C | Kee Berry | Akibeere | Déjà patché | Akibeere |
| 0x87C298 | Marang Berry | Tarabeere | Déjà patché | Tarabeere |
| 0x87C2C4 | Absorb Bulb | Knolle | Déjà patché | Knolle |
| 0x87C2F0 | Air Balloon | Luftballon | Déjà patché | Luftballon |
| 0x87C31C | Adrenal Orb | Zitterorb | Déjà patché | Zitterorb |
| 0x87C348 | Binding Band | Klammerband | Déjà patché | Klammerband |
| 0x87C374 | Cell Battery | Akku | Déjà patché | Akku |
| 0x87C3A0 | Eject Button | Fluchtknopf | Déjà patché | Fluchtknopf |
| 0x87C3CC | Float Stone | Leichtstein | Déjà patché | Leichtstein |
| 0x87C3F8 | Focus Sash | Focus Sash | Patch séparé | Fokusgurt |
| 0x87C424 | Grip Claw | Griffklaue | Déjà patché | Griffklaue |
| 0x87C450 | Iron Ball | Eisenkugel | Déjà patché | Eisenkugel |
| 0x87C47C | Lagging Tail | Schwerschweif | Déjà patché | Schwerschweif |
| 0x87C4D4 | Quick Powder | Flottstaub | Déjà patché | Flottstaub |
| 0x87C500 | Metronome | Metronom | Déjà patché | Metronom |
| 0x87C52C | Muscle Band | Muskelband | Déjà patché | Muskelband |
| 0x87C558 | Protect Pads | Protect Pads | Patch séparé | Schutzpolster |
| 0x87C584 | Red Card | Rote Karte | Déjà patché | Rote Karte |
| 0x87C5B0 | Ring Target | Zielscheibe | Déjà patché | Zielscheibe |
| 0x87C5DC | Shed Shell | Wechselhülle | Déjà patché | Wechselhülle |
| 0x87C608 | Snowball | Schneeball | Déjà patché | Schneeball |
| 0x87C634 | Sticky Barb | Klettdorn | Déjà patché | Klettdorn |
| 0x87C660 | Terrain Ext. | Terrain Ext. | Patch séparé | Feldbeschichtung |
| 0x87C68C | Wise Glasses | Wise Glasses | Patch séparé | Schlaubrille |
| 0x87C6E4 | Grassy Seed | Grassy Seed | Patch séparé | Gras-Samen |
| 0x87C710 | Misty Seed | Misty Seed | Patch séparé | Nebel-Samen |
| 0x87C73C | Psychic Seed | Psychic Seed | Patch séparé | Psycho-Samen |
| 0x87C768 | Normal Gem | Normaljuwel | Déjà patché | Normaljuwel |
| 0x87C794 | Fighting Gem | Kampfjuwel | Déjà patché | Kampfjuwel |
| 0x87C7C0 | Flying Gem | Flugjuwel | Déjà patché | Flugjuwel |
| 0x87C7EC | Poison Gem | Giftjuwel | Déjà patché | Giftjuwel |
| 0x87C818 | Ground Gem | Bodenjuwel | Déjà patché | Bodenjuwel |
| 0x87C844 | Rock Gem | Gesteinsjuwel | Déjà patché | Gesteinsjuwel |
| 0x87C870 | Bug Gem | Käferjuwel | Déjà patché | Käferjuwel |
| 0x87C89C | Ghost Gem | Geisterjuwel | Déjà patché | Geisterjuwel |
| 0x87C8C8 | Steel Gem | Stahljuwel | Déjà patché | Stahljuwel |
| 0x87C8F4 | Fire Gem | Feuerjuwel | Déjà patché | Feuerjuwel |
| 0x87C920 | Water Gem | Wasserjuwel | Déjà patché | Wasserjuwel |
| 0x87C94C | Grass Gem | Pflanzenjuwel | Déjà patché | Pflanzenjuwel |
| 0x87C978 | Electric Gem | Electric Gem | Patch séparé | Elektrojuwel |
| 0x87C9A4 | Psychic Gem | Psychojuwel | Déjà patché | Psychojuwel |
| 0x87C9D0 | Ice Gem | Eisjuwel | Déjà patché | Eisjuwel |
| 0x87C9FC | Dragon Gem | Drakojuwel | Déjà patché | Drakojuwel |
| 0x87CA28 | Dark Gem | Dark Gem | Patch séparé | Unlichtjuwel |
| 0x87CA54 | Fairy Gem | Feenjuwel | Déjà patché | Feenjuwel |
| 0x87CAAC | Health Wing | Heilfeder | Déjà patché | Heilfeder |
| 0x87CAD8 | Muscle Wing | Kraftfeder | Déjà patché | Kraftfeder |
| 0x87CB04 | Resist Wing | Abwehrfeder | Déjà patché | Abwehrfeder |
| 0x87CB30 | Genius Wing | Geniefeder | Déjà patché | Geniefeder |
| 0x87CB5C | Clever Wing | Espritfeder | Déjà patché | Espritfeder |
| 0x87CB88 | Swift Wing | Flinkfeder | Déjà patché | Flinkfeder |
| 0x87CBB4 | Pretty Wing | Prachtfeder | Déjà patché | Prachtfeder |
| 0x87CBE0 | Bottle Cap | Bottle Cap | Patch séparé | Silberkronkorken |
| 0x87CC38 | Red Nectar | Roter Nektar | Déjà patché | Roter Nektar |
| 0x87CC90 | Pink Nectar | Rosa Nektar | Déjà patché | Rosa Nektar |
| 0x87CCBC | Purp Nectar | Purp Nectar | Patch séparé | Purpurner Nektar |
| 0x87CCE8 | Fast Ball | Turboball | Déjà patché | Turboball |
| 0x87CD14 | Level Ball | Levelball | Déjà patché | Levelball |
| 0x87CD40 | Lure Ball | Köderball | Déjà patché | Köderball |
| 0x87CD6C | Heavy Ball | Schwerball | Déjà patché | Schwerball |
| 0x87CD98 | Love Ball | Love Ball | Patch séparé | Sympaball |
| 0x87CDC4 | Friend Ball | Freundesball | Déjà patché | Freundesball |
| 0x87CDF0 | Moon Ball | Mondball | Déjà patché | Mondball |
| 0x87CE1C | Sport Ball | Turnierball | Déjà patché | Turnierball |
| 0x87CE48 | Beast Ball | Ultraball | Déjà patché | Ultraball |
