# ES-004 — traitement final des 374 clés

F-854. D-849/F-850 terminés et intégrés avant traduction ; F-1035 intégré au
commit `b8a735f4`, relu avant reprise. La préparation `004_PREPARATION.json`
reste un état historique, sans certification de traduction. Les contrats
techniques et conclusions sur les anciennes tables sont dans `004_ROUTES.md`.

[004_TRAITEMENT.json](004_TRAITEMENT.json) donne une décision pour chacune des
374 clés exactes de `lots.json` : **256 valeurs actives** (167 descriptions
objets, 88 mots Easy Chat, ZREZA) et **118 exclusions sans injection**
(54 anciennes descriptions objets, 58 anciennes notices CT/MO, quatre fragments,
deux séquences binaires). Quatre valeurs restent identiques pour une raison
lexicale : Pokémon, Pokédex, POKéNAV et COLOR. Les 252 autres sont traduites ou
corrigées depuis les préimages EN complètes, pas depuis l’ancien inventaire EN
partiellement français. Aucun import communautaire n’est accepté sans relecture.

## Fidélité et terminologie

La relecture rétablit notamment les 10 PP de l’Éther, tous les PP de l’Élixir Max,
la résurrection de tous les Pokémon pour Sacred Ash, le niveau des Pokémon
sauvages pour les flûtes noire/blanche, les statistiques de base des boissons,
le prix élevé du Morceau d’Étoile et la teinte rougeâtre de l’ambre. Le Magnetime
communautaire redevient Magnemite. Les références au Cubo et aux secteurs restent
fidèles à Unbound ; Shadows, Monte Thundercap, Profesor Log, Pueblo Bellin et
Ciudad Antisis suivent D-849, sans reprendre les substitutions FR/communautaires.
The Shadow reste le nom EN propre du vaisseau, distinct de la faction Shadows.

Les mots sont des lexèmes combinables Easy Chat, pas une nouvelle table de noms
de talents CFRU. Les types suivent D-849. Les noms des habilités et les compactes
ARMAD. BAT., ELEC. ESTÁT., ABSOR. ELEC. et ABSOR. AGUA sont attestés par le
[guide Nintendo Platine](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/habilidades.html).
SOMBRATRAMPA est la forme officielle en un mot, qui tient dans les 12 octets.
ZREZA est le nom seul de la baie, dans sa cellule fixe, selon les
[baies du guide Nintendo](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/objetos_bayas.html).
Les lieux empruntés à Hoenn emploient Pueblo Lavacalda, Malvalanova et Nao
Abandonada, noms du [guide Nintendo Esmeralda](https://www.guiasnintendo.com/1_GAMEBOY_ADVANCE/Pokemon_Esmeralda/pok_esmeralda_SP/otros.html).
Les autres noms du hack gardent leur noyau EN. Les mots des versions sont
localisés RUBÍ/ZAFIRO/ORO/PLATA/VERDE/FUEGO/HOJA ; les noms d’espèces restent
inchangés. Aucune substitution promotionnelle, URL ou date ajoutée au texte.

## Consommateurs et limites

Les descriptions sont globales au Cube ; aucune carte n’est déduite de leur
adresse. Les 167 descriptions utilisent gItems `0x876200`, stride 44, champ +20,
et tous leurs anciens référents directs restent cohérents. Les trois absences et
les anciennes préimages du cache passent par les contrats canoniques existants.
Trois lignes FE maximum, 176 pixels par ligne, 512 octets maximum. Aucun FA/FB,
fallback ni troncature. Les commandes complètes FC/FD/F8/F9/F7 et leurs arguments
sont comparés : les préimages actives n’en contiennent aucun, les valeurs finales
non plus. Les octets FE sont distingués des arguments et FF termine chaque chaîne.

Les groupes Easy Chat 1 et 2 conservent leurs bases, ID, index, ordres et
disponibilités : une ligne, 12 octets + FF, 72 pixels. ZREZA tient dans six
caractères + FF et 36 pixels ; aucune des deux bases de la table de baies n’est
repointée vers une chaîne isolée. Les métadonnées voisines restent gelées.

Les exclusions suivent l’analyse des routines/racines de F-1035, pas la seule
absence de pointeur. Aucun texte n’est déplacé vers un consommateur hors lot.
L’ancienne coïncidence non alignée `0x653C71` n’est pas repointée. Les fragments
et données binaires ne deviennent pas des phrases. Aucune des 118 clés n’est
ajoutée au combined ; le manifeste technique les refuse explicitement.

## Vérifications reproductibles

```sh
make build-es-maint BUILD_NUMBER=0
python3 -m pytest tests/unit/test_es004_contract.py tests/unit/test_es004_preparation.py tests/unit/test_es004_routes.py -q
python3 -m pytest tests/e2e/es/test_es004_delivery.py -q
make test-python
npx playwright test --config tests/e2e-playwright/es004-delivery.config.ts
```

Le test de recette utilise aussi un combined temporaire contenant uniquement
les 256 valeurs finales, le vrai CSV → JSON → builder et tous les patches.
Il compare la ROM entière à un témoin recevant les mêmes patches et aucune
traduction : seules les cibles et cellules de pointeurs déclarées sont autorisées.
Le build complet est vérifié séparément aux consommateurs réels de production.
La recette ES-005 vérifie désormais chaque mot traduit des groupes partagés
contre sa valeur maintenue, y compris ES-004, au lieu de supposer que toute
cellule hors ES-005 reste anglaise. Les huit octets de métadonnées sont vérifiés
pour toutes les cellules ; les cellules non traduites restent inchangées.
Les largeurs sont contrôlées depuis les octets encodés et les tables de métriques
vivantes des cinq polices latines. Aucun attendu BPS historique n’est modifié.

## Résultats du checkpoint de livraison

`make build-es-maint BUILD_NUMBER=0` réussi, SHA-256
`ca93c3bae49749fe114574bb7a4f68e80d6199e09f6c200984a77a0864f5e533`.
Les 256 valeurs sont relues aux consommateurs après tous les patches ; les
118 préimages et leurs références restent identiques. Le pipeline isolé des
valeurs finales ne modifie aucun octet hors des plages autorisées, avant ou
après patches. Les contrôles ES-004 passent, puis les quatre contrôles ROM
ES-005 passent après l’adaptation des groupes partagés décrite ci-dessus.

`make test-python` sous Python 3.14.10 : **9 626 passed, 7 skipped,
4 432 deselected**, aucun échec (624,54 s). Quatre skips provenaient de
l’absence d’Unicorn dans cet environnement : les deux fichiers concernés sont
rejoués dans un environnement temporaire Python 3.14 avec Unicorn 2.1.4,
avec succès. Il reste les trois conditions préexistantes du pont émulateur,
des séquences FD et du CSV dynamique ; aucun skip ajouté ou test assoupli.
Les hooks du premier commit ont aussi passé **9 489 tests Python**, un skip
préexistant, **80 tests Vitest** et les builds FR/IT/DE. La consolidation finale
repasse ces hooks avec Unicorn disponible. Les résultats après rebase sont
consignés dans la résolution du ticket.

Playwright headless/mGBA offscreen : **7 passed**, captures attachées après
assertions. Trois descriptions dans le Cube (lait, Éther, clé Shadows), trois
mots Easy Chat (INTIMIDACIÓN, ELEC. ESTÁT., ABSOR. ELEC.) et ZREZA en cellule
fixe. Ruff ciblé et typecheck Playwright passent. Aucune sauvegarde en jeu.
Le témoin FR reconstruit avant/après avec `BUILD_NUMBER=0` est intégralement
identique (`cmp`), SHA-256
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Les sources FR, ES référence, glossaire et liste des lots restent inchangés.

## Non vérifié

Les sondes courtes ne certifient pas toutes les combinaisons Easy Chat ni le
parcours naturel de chaque mot dans le sélecteur : les mots et ZREZA sont rendus
par l’imprimante native de msgbox à leur cible livrée. Les captures comparent
exactement les pixels des glyphes natifs, accents et ponctuation compris.
Les descriptions sont
exposées dans la fenêtre native du Cube avec le Repel de la fixture : seuls son
nom et son pointeur sont adaptés dans une copie temporaire ; les consommateurs
livrés sont vérifiés séparément octet par octet. Ces copies ne sont pas livrées.
Les index de tri EN restent conservés ; aucun tri alphabétique espagnol partagé
n’est introduit par ce lot. Aucune sauvegarde en jeu. La certification globale et le statut complete restent
à T-914. Aucun push ni lancement/retry de pipeline distant.
