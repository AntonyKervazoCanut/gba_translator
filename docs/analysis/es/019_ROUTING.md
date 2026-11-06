# ES-019 — contrats mécaniques F-1049

Aucune traduction de production. Les quatre rapports historiques de préparation,
y compris la sonde négative, restent inchangés. Les résultats positifs sont dans
`019_ACHEMINEMENT_VALIDATION.json`.

## Stratégie canonique

Les clés 7CE3D9, 7CE573, 7D35E9 et 7E6C2E restent contractuelles dans le combined.
TextAliases enrichit le JSON réellement consommé avec leur début vivant à +1,
leur préimage complète et leurs seuls pointeurs qualifiés. AA reste une donnée.
Les correspondances ES sont vérifiées depuis la map et les préimages ES explicites,
sans présumer une égalité des adresses EN et ES.

Pour les paires 7DE55F/7DE560 et 7E6B88/7E6B89, le parent doit sélectionner
**uniquement 7DE560 et 7E6B89**. Les préfixes ne reçoivent aucune traduction.
Le garde existant `TextAliases.check_keys` refuse les deux clés simultanées,
même si leurs valeurs sont identiques ; chaque clé seule reste techniquement
acceptée. Aucun second réinserteur ni plafond global modifié.

## Consommateurs qualifiés

| Clé | Début vivant | Site | Grammaire |
|---|---|---|---|
| 7CE3D9 | 7CE3DA | 7763B2 | `0F 00 <ptr> 09 02`, message standard |
| 7CE573 | 7CE574 | 166DB1 | `0F 00 <ptr> 09 02`, message standard |
| 7D35E9 | 7D35EA | 7E70BE | introduction `trainerbattle` type 04, +6 |
| 7DE55F | 7DE560 | 7DE7E0 | `0F 00 <ptr> 09 06`, message standard |
| 7E6B88 | 7E6B89 | 78198D | `0F 00 <ptr> 09 03`, panneau |
| 7E6C2E | 7E6C2F | 78098B | `0F 00 <ptr> 09 05`, oui/non |

Le pari n'est pas une simple table de mots : à 7E70B8, la préimage
`5c041e000000ea357d084f907d0820e57f08` encode `trainerbattle` 04,
dresseur 001E, objet local 0000, introduction 087D35EA, défaite 087D904F,
suite 087FE520. Seul le champ d'introduction est repointé. La commande voisine
à 7E70D4 utilise le même format pour le dresseur 001F. Le contexte entier est
contrôlé au chargement et la différence binaire finale interdit toute écriture
sur les autres champs.

Les six surfaces utilisent la police normale, une fenêtre paginée de deux lignes
et 208 pixels par ligne. FA défile ; FB ouvre une page. Le buffer FD01 conserve
son argument et réserve 84 pixels. FC0108 reste complet ; les flèches 79/7A/7B
du panneau restent des glyphes. La limite par entrée reste 512 octets FF inclus ;
les préimages vivantes font respectivement 151, 271, 36, 97, 50 et 103 octets.
Le budget original exclut AA et tout padding. Il n'y a pas de cellule fixe à
agrandir ; la relocalisation est obligatoire, même pour une chaîne plus courte.

## Préservation

TextSourcePreservation, intégré par F-1046, conserve les six préimages complètes,
AA inclus, et les dix occurrences intérieures. Six sont les lecteurs ci-dessus.
Les quatre autres occurrences de 7CE573 (sites 80B6EB, 80D30D, 1D41C78, 8078EB)
restent `unproven_binary` : ni leur qualification textuelle ni leur repointage
ne sont autorisés. Leurs octets et les sources pointées restent intacts.

Les tests utilisent des tranches ROM réelles et vérifient les préimages, les
budgets, les commandes et arguments, les collisions, les refus atomiques,
l'idempotence et les allocations déterministes. La sonde complète compare le
builder puis les patches finaux à un témoin recevant les mêmes patches : seuls
les six champs qualifiés et les allocations peuvent différer. Les empreintes
des sources, protections et lots restent identiques.

## Preuve native et limites

Playwright headless lance mGBA avec `QT_QPA_PLATFORM=offscreen`. La sonde RAM
existante lit tous les pointeurs finaux, développe les buffers, mesure toutes
les lignes avec le moteur et rend les sept premières lignes de chaque sentinelle.
La capture est créée après les assertions dans le répertoire temporaire système.
Aucune sauvegarde en jeu, aucune fenêtre visible, aucune ROM sentinelle commitée.

Cette mire technique ne certifie ni les traductions, ni les zones, ni un parcours
de jeu. Les 393 décisions linguistiques, fragments/exclusions, les quatre sources
longues et la reconstruction de 7E6816 restent au parent F-869. Aucun combined,
protected_entries, glossaire, inventaire ou lots.json n'est modifié.

Les gardes ES-015 conservent leurs 67 préimages et 110 sites exacts : leur filtre
sélectionne leur rapport exact, y compris après intégration du lot ES-016. La fixture globale TextAliases
ajoute les six préimages réelles ; son total attendu passe de 102 à 108 après intégration du lot ES-016.
