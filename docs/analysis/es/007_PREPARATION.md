# ES-007 — traitement du lot et composition des statistiques

F-857, 6 novembre 2026. D-849 et F-850 ont été consultés, terminés et intégrés
avant traduction. Le glossaire et le code partagé restent inchangés.

## Couverture de préparation

Les 374 clés sont exactement celles de `lots.json`, sans `--skip-existing`.
`007_TRAITEMENT.json` consigne chaque préimage EN reconstruite depuis la ROM,
la correspondance de l'offset map lorsqu'elle existe, les références brutes et
plausibles, les arguments des commandes, la décision et les traductions préparées.
Il distingue 332 traductions, neuf noms ou identifiants conservés, quatre buffers
sans texte littéral, dix fragments résiduels, dix-neuf préimages sans pointeur
plausible. Les neuf entrées statistiques sont composées sans patch moteur.

Les noms de lieux sont des consommateurs des tables globales de carte et de noms,
les mots courts appartiennent à Easy Chat, et les autres textes au moteur de combat.
Ces attributions viennent des tables référentes, pas d'une adresse supposée de scène.
L'absence de pointeur direct des dix-neuf préimages ne démontre pas une absence
d'accès calculé ; aucune injection de ces préimages n'est revendiquée.

Les ajouts dans `combined_es-maint.txt` et les protections exactes sont limités aux
332 clés du lot. Les nouvelles données de `system_texts.json` déclarent les
préimages et pointeurs pour le routeur existant ; aucun mécanisme partagé n'est
modifié. Le faux pointeur non aligné de FLATTEN dans les données audio à
`0x54482E` n'est pas un consommateur textuel ; ses octets sont gardés en test ROM.

La politique D-849 conserve les noyaux propres Grim, Vivill, Autl, Valley, Rift,
Icicle, Cliff et les noms composés du hack. Elle rétablit Pueblo Bellin, Pueblo
Crater et Pueblo Tarmigan. Les noms empruntés aux jeux utilisent les formes es-ES,
notamment [Calle Victoria](https://www.wikidex.net/wiki/Ruta_de_la_Victoria/Calle_Victoria),
[Cueva Psique](https://www.wikidex.net/wiki/Cueva_Psique) et
[Ruinas Sete](https://www.wikidex.net/wiki/Ruinas_Sete).
Ces pages secondaires décrivent les localisations officielles ; ce ne sont pas
des captures authentifiées d'une ROM commerciale.

## Statistiques : solution par les données

La preuve `007_PREUVE_ASSEMBLAGE_STATS.json` consigne les préimages et le
désassemblage EN. Le constructeur préfixe bien l'intensité au suffixe. Le premier
diagnostic d'un patch moteur obligatoire était trop fort : B-35 et B-363 ont
déjà démontré la solution par les textes. Les gabarits portent `subió` ou `bajó`,
les suffixes portent `!` et les intensités portent `<0x00>mucho`. On obtient
`subió!`, `subió mucho!`, `bajó!`, `bajó mucho!`, dans l'ordre original des FD.
Le gabarit objet est consommé par la table de hausse, pas celle de baisse.

Les ID CFRU 185/186 sont résolus par la routine 0x9A32C0 vers 0xA4C610/0xA4C603,
et non dans la table originale. Ces deux textes sont la propriété d'ES-031 : leur
traduction future doit être un intensificateur à espace initial, comme
`<0x00>muchísimo`. Ils ne sont pas modifiés ici. La certification des phrases
complètes à ±3 et plus attend donc ES-031 et T-914, comme les noms de statistiques
et autres buffers appartenant aux lots suivants. Aucune modification du moteur
ou de ses tables n'est nécessaire pour les neuf entrées d'ES-007.

## Validation et limites

Le témoin FR a été reconstruit avec `make prepare-fr` puis `make build-fr` avant
les traductions : SHA-256
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Le premier essai avec un JSON historique copié échouait sur un préfixe FR ; la
reconstruction depuis les sources actuelles a résolu cet artefact périmé sans
modification du code ni du français.

Les tests comparent les séquences FC/FD/F8/F9/F7 complètes, FA/FB et leurs arguments,
le plafond de 512 octets et les largeurs. Dix `W` par buffer constituent une borne
de sonde, pas une certification des noms ennemis préfixés ou des mouvements,
objets et habilités dynamiques les plus longs.

Le test Playwright contrôle les octets aux pointeurs finaux, puis utilise
une copie temporaire et l'imprimante native mGBA offscreen. Les FD combat sont
développés seulement dans cette copie. Ses captures et OCR ne certifient pas le
déclenchement naturel en combat ni les fenêtres natives Easy Chat/carte.
Les résultats d'exécution seront consignés après validation. La certification complète de la langue reste réservée à T-914.


## Relecture sémantique et validation intermédiaire

La relecture finale distingue Rabia (Grudge : tous les PP perdus) de Rencor
(Spite : retrait partiel de PP), et nomme le compteur de Canto Mortal. Les trois
valeurs corrigées et leurs protections exactes sont couvertes par la garde
unitaire. Référence primaire : [guide Nintendo Platino, mouvements](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/ataques.html).
La ligne du compteur reste sous 192 px avec les deux buffers élargis à dix W.

Avant cette dernière correction lexicale, les 332 traductions avaient été
vérifiées à leurs 364 pointeurs ; les 336 états natifs (332 textes et quatre
compositions) et dix OCR avaient passé Playwright. La ROM FR conservait le
témoin ci-dessus. `make test-python` a donné 9673 réussis, six skips préexistants,
zéro échec ; TypeScript et les 416 gardes ciblées passent. Les nouveaux termes
font l'objet d'un nouveau build et d'une nouvelle preuve, à consigner au ticket.

Le profil ROM local sur les six reconstructions fraîches
(`make -o materialize-test-roms test-rom`) a donné 4158 réussis, 51 skips et douze
échecs hors ES-007. Ils concernent PT-04/22/48/57/69/72, la réplique du rival DE,
les gardes F-601 et dialogues-09 DE, et la garde de hash historique FR Corps Gel.
Aucun de ces fichiers de données ou mécanismes n'est modifié dans ES-007 ; les
attendus ne sont pas neutralisés. La certification globale n'est pas revendiquée.
Les résultats complets sont conservés dans les pièces jointes du ticket.

**Prérequis de clôture F-881 / ES-031 :** traduire les deux intensificateurs
0xA4C603 et 0xA4C610 avec un séparateur initial compatible, puis vérifier les
phrases complètes à ±3, ±6 et les effets doublés. Les formes actuelles produisent
encore une jonction hybride à ces degrés. Le lot ES-007 reste en attente de ce
prérequis après livraison et vérification du travail indépendant ; aucun nouvel
offset n'est pris à ES-031 et aucun patch moteur n'est introduit ici.
