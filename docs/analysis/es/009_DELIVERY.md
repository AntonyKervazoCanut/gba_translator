# ES-009 — décisions de traduction et contrats de livraison

F-859. Les 374 clés exactes du lot figurent dans
[009_DELIVERY.json](009_DELIVERY.json), avec préimage EN, texte communautaire,
correspondance ES, références binaires, décision, justification et valeur retenue.
La préparation reste un historique immuable ; le présent rapport la complète.

## Décisions

- 326 textes traduits ou corrigés et 11 valeurs conservées justifiées : 337 valeurs
  protégées exactement dans le même commit que leur ajout au combined.
- Six préfixes nuls exclus ; leur clé vivante est déjà traitée dans ce lot.
- Dix-huit choix de l'ancien consommateur contourné conservés sans injection, selon
  F-1040 et [009_FORMATTED.md](009_FORMATTED.md). Les huit noms de Médailles
  417FD9…41802F ont uniquement les pointeurs 3F5BCC…3F5BE8, lus par le
  même ancien littéral CBA68 contourné. Ils n’apparaissent pas dans les listes
  textuelles actives de 1FB196C. Les huit autres libellés, 417B3E…417B94,
  restent traités ; les préimages et pointeurs anciens sont gardés.
- Dix textes hérités sans pointeur direct conservés sans injection : 417322,
  4177DD, 417858, 41786B, 417920, 417CD1, 417CE6, 417CFF, 417D18, 417D32.
  Ils sont textuels : on ne les déclare pas « données non textuelles » pour
  masquer cette limite. Aucune route actuelle n'est attestée ; aucune
  inaccessibilité universelle n'est revendiquée.

Les trois anciens messages PC 4183F0/418408/418419 sont conservés sans
injection : leurs seuls pointeurs appartiennent au miroir 9A425C. Le lecteur
actif 8FBA4 emploie aux indices 25/26/27 les textes 1F21C3C/1F21C2A/1F21C0F,
hors lot. Les anciens miroirs ne deviennent pas des consommateurs inventés.

La rédaction EN vivante fait autorité. Les coquilles communautaires, omissions de
buffers, pertes de sens et noms étrangers au hack ne sont pas importés : Log
reste Log, Ayla reste Ayla, la Medalla et les états guéris gardent leur sens.
Les noms officiels d'espèces inchangés restent tels quels. Les interfaces sont
partagées ; aucun lieu géographique n'est attribué depuis une adresse de banque.
Les parcours naturels exhaustifs restent à distinguer de ces consommateurs.

## Acheminement et budgets

Les 26 contrats FC13/FC06/F7 de F-1040 sont réutilisés tels quels. Les 311 autres
valeurs ont des préimages et références explicites dans le même manifeste
SystemTextRoutes ; le builder existant reste l'unique réinserteur. Pas de nouveau
patch moteur, fallback, troncature ni alias. FC/FD/F8/F9/F7 et arguments, ainsi que
l'ordre des pages FA/FB, sont contrôlés à la normalisation et en ROM finale.

Les quatre textes 417200/417457/41778A/417D90 partagent des occurrences fortuites
avec les graphismes PT-12. Ils sont volontairement plus courts que leur cellule
source, avec fixed_capacity : aucune relocation ni modification des cinq faux
pointeurs graphiques. Le plafond de 512 octets et les voisins restent contrôlés.

Les neuf actions équipe emploient la police 2 et une enveloppe conservatrice de
48 px : fenêtre native minimale 7 tuiles, avec huit pixels réservés. Les trois
modèles 45A148/45A150/45A158 et la routine 121E5C sont épinglés. « Elegir »,
« Retirar » et « Cambiar » évitent de dépasser la petite fenêtre.

Les slots 45A32C et 402230 renvoient respectivement au message à nombre variable
A4E15D et à « Move to Cube » en 1F21C01, hors lot ; ils ne justifient pas une
injection dans les anciens textes 417322/4177DD.

Les 19 messages PC simples réutilisent aussi le lecteur 8FBA4 : fenêtre
144×16 px, police 1, tampon 80 octets. Leurs limites sont explicites, sans
activation d’un autre expanseur. Trois rédactions trop larges ont été corrigées
avant livraison : interdiction de libérer un Huevo, poursuite des opérations
et impossibilité de stocker une Carta.

Les six menus à prix gardent colonnes, polices, quantités et montants source.
L'unité « fich. » est une abréviation de budget de « fichas », pas un renommage
ou un changement de monnaie. SEM. MILAGRO et FL. AMARILLA sont les formes
historiques compactes ; les noms complets ne tiennent pas dans la colonne 80 px.
Le tampon PC réserve toujours 95 px aux objets et 60 px aux surnoms ; les trois
messages source qui débordent sont remplacés par des phrases espagnoles bornées,
sans modifier le nom runtime. « Eliges », « Lleva » et « Ahora » restent neutres
pour le genre des noms d'objets.

Références complémentaires de vocabulaire :
[Nintendo Esmeralda, objets](https://www.guiasnintendo.com/1_GAMEBOY_ADVANCE/Pokemon_Esmeralda/pok_esmeralda_SP/otros.html)
(SEM. MILAGRO, Carbón, Agua Mística, Bola Humo),
[Nintendo Esmeralda, soins](https://www.guiasnintendo.com/1_GAMEBOY_ADVANCE/Pokemon_Esmeralda/pok_esmeralda_SP/salud.html)
(nom complet Flauta Amarilla),
[relevé secondaire de la forme GBA Fl. Amarilla](https://www.pkmnstats.com/dex/tercera/objetos/110/fl-amarilla/).
Ce dernier est un relevé d'une localisation de jeu, pas une publication Nintendo.
Le glossaire D-849 partagé reste inchangé.

## Validation et limites

Les tests de livraison vérifient la sélection, les valeurs protégées, les
commandes, les références finales et l'isolation binaire. Les commandes et
résultats exécutés, les captures et le témoin FR sont consignés dans la résolution
du ticket. Aucun résultat du prérequis n'est présenté comme un test de la rédaction
finale. La certification ROM globale PT/DE signalée dans la préparation reste
séparée ; aucun attendu n'est neutralisé. Les dix textes sans consommateur
attesté, les consommateurs naturels des miroirs et les parcours géographiques
exhaustifs ne sont pas certifiés par une simple impression de sonde.

La vue complémentaire des 311 autres textes utilise le vrai expanseur FD à
8FCC et le printer natif. Elle vérifie les octets, glyphes, pages, largeurs
et canaris avec des sentinelles runtime. Les pauses FC08/FC09 et le son FC10
ne sont pas joués dans cette vue ; leurs octets et arguments sont vérifiés
séparément. Cette vue de glyphes ne revendique pas les fenêtres ni les
consommateurs naturels de chacun des scénarios.

## Rattachement aux consommateurs

Le rapport donne les IDs et cellules des 81 choix retrouvés dans les 65
premiers descripteurs natifs de 3E04B0 ; les IDs 32…37 désignent des listes RAM,
ils ne sont pas interprétés comme des listes de textes ROM. Il donne aussi
les indices actifs des 26 messages PC sélectionnés et les 28 IDs de chaînes
standard du lot. Les familles équipe, aide terrain, étages et actions PC sont
rattachées à leurs tables et lecteurs actuels, sans attribuer un lieu depuis
la banque ROM. Les autres références littérales restent explicitement partagées.

Le handler natif 6BED4 (dispatch 15FBC4, littéral 6BF10) copie les chaînes
standard via 8D84. Les buffers script sont à 2021CD0/2021CF0/2021D04 ; le
suivant commence à 2021D18 : capacité minimale 20 octets. Les 28 valeurs tiennent
avec FF. La sonde appelle ce vrai handler vers STR_VAR_3, compare les octets
copiés et place des canaris avant/après les vingt octets. Ces racines et la
capacité sont protégées avant/après les patches. Cette preuve de copie ne
prétend pas certifier chaque composition de texte parent qui utilise un buffer.
