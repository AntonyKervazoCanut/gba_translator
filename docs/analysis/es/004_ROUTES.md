# ES-004 — contrats d’acheminement

F-1035. Ce document et `004_ROUTES.json` couvrent les 374 clés du lot :
167 descriptions actives, 88 mots Easy Chat, un nom de baie en cellule fixe,
118 clés conservées sans injection. Aucun texte final n’est certifié : F-854
reste responsable des traductions et de leur preuve d’affichage finale.
Les préimages sont relues dans la ROM EN, jamais dans la colonne EN française
de l’inventaire. Aucun combined, glossaire, protected_entries ou lots.json changé.

## Contrats consommés

`languages/es-maint/item_descriptions.json` conserve les 17 cas ES-003 et ajoute
167 descriptions ES-004 avec préimage entière, tous les référents (anciens doublons
inclus), IDs de compatibilité et fenêtre : trois lignes FE, 176 pixels par ligne,
512 octets maximum. Les commandes et arguments FC/FD/F8/F9/F7 restent inchangés ;
aucun FA/FB ajouté. L’ID de compatibilité vaut l’ID moteur +9 : même table,
base de compatibilité 0x876074 contre base moteur 0x876200, stride 44, champ+0x14.
Les littéraux et l’accesseur 0x9A96C sont gardés avant et après patches.

Les trois préimages absentes du cache (0x3D5934, 0x3D5968, 0x3D5AB8) et les
37 préimages obsolètes sont reconstruites dans le JSON réellement consommé par
le builder depuis le manifeste validé contre la ROM source. Pas de second
réinserteur. Les entrées sélectionnées sont enregistrées et contrôlées à nouveau
après les patches contre le combined ; perte, duplication, fallback et troncature
ne peuvent donner une certification verte.

`system_texts.json` réutilise ce chemin pour les 89 mots structurés. Les cinq
contrats système ES-002 restent inchangés. Une entrée peut déclarer une fenêtre
et une capacité fixe sans changer le comportement des dialogues existants.

## Easy Chat

Les groupes 1 et 2 ont pour base 0x3E7FE0 et 0x3E8504. Leurs descripteurs à
0x3ECEDC et 0x3ECEE4 valent respectivement `e07f3e081a001900` et
`04853e086d006d00` : pointeur, nombre, nombre disponible. L’accesseur 0xBD834
calcule groupe*8 puis mot*12, charge le premier champ, et copie la chaîne.
Les huit octets suivants sont ordre et disponibilité ; les gardes couvrent les
135 structures des deux groupes, même celles hors sélection. Ni IDs ni groupes
ne sont réordonnés. Ce n’est pas la table des talents CFRU.

Le consommateur 0x8B7CC calcule des slots de **13 octets** et appelle la copie
de mot à 0x8B7E0. Le sélecteur 0x1014FA emploie la police 1, colonnes x=24/128
(pas 104 pixels), lignes espacées de 16 pixels. Les métriques de police 1 à
0x1FB100 donnent au plus 6 pixels pour les glyphes latins/espagnols utilisés.
Le contrat conservateur est donc **12 octets de texte + FF, 72 pixels, une ligne**.
72 n’est pas présenté comme la largeur totale de colonne : c’est le plafond
commun sûr dérivé du buffer le plus contraignant. Les routines, racines et
métadonnées restent identiques après tous les patches.

## CHERI : base de table, jamais chaîne relogeable

À 0x3DF7E8 commence une table de baies, stride 28. Les références 0x9C77C et
0x14E294 sont des bases de table : 0x9C718 ajoute 0x498 et copie la structure 42 ;
0x14E210 calcule base+id*28 puis copie le nom, mesure et imprime en police 2.
Le nom occupe 7 octets (FF compris) ; firmness commence à +7. Contrat : en place,
**6 octets de texte + FF, 36 pixels, une ligne**. Les deux bases et les 21 octets
de métadonnées restent gelés. La chaîne ZREZA n’apparaît que dans les fixtures
sentinelles ; aucune décision linguistique finale n’est imposée à F-854.

## Anciennes tables, fragments et binaire

Les 54 descriptions sans consommateur gItems vivant gardent leurs anciens
pointeurs. Les comparaisons nominales par clé restent dans le rapport JSON.
Le moteur consulte 0x876200 ; les cibles des descriptions anciennes ne figurent
pas dans les 1000 entrées examinées. L’ancienne table 0x3DB028 n’a aucune racine
vers sa base, ni référence alignée dans le code bas (<0x1B0000) vers son intervalle
0x3DB028..0x3DF09C. Les coïncidences des banques de données ne sont pas des
consommateurs moteur démontrés. La conclusion combine routines, racines et
comparaison des cibles ; elle ne repose pas uniquement sur une recherche de pointeurs.
Ainsi X Attack pointe actuellement 0xEB23F0 : cette clé hors lot n’est pas modifiée.

Les 58 anciennes notices CT/MO sont également conservées sans injection.
Les routines 0xE541A et 0x137B88 utilisent 0x99F194+(move_id−1)*4, chargé depuis
0xE5440/0x137BC8 ; le pointeur précédent 0x99F190 n’est pas confondu avec la base.
Aucune des 892 cibles examinées ne correspond à ces notices. La coïncidence
non alignée 0x653C71 vers 0x3DA477 reste intacte. Les quatre fragments et deux
séquences binaires restent exclus ; aucune phrase n’est inventée.
Le manifeste refuse explicitement les 118 clés exclues si elles sont proposées
à l’injection. F-854 doit les documenter comme conservées/exclues, sans les
ajouter au combined pour les faire injecter.

## Validation reproductible

- `tests/unit/test_item_description_routes.py` : les 184 descriptions, préimages,
  trois absences et anciennes préimages du CSV, contrôles, budgets et ROM entière.
- `tests/unit/test_es004_routes.py` : 89 mots, relocations, glyphes espagnols,
  cellule baie, racines et métadonnées, refus d’overflow et comparaison ROM entière.
- `tests/e2e-playwright/fixtures/prepare_es004_system_probe.py` : vrai combined
  temporaire → CSV → JSON → builder → patches, comparaison intégrale avec témoin
  recevant les mêmes patches et aucune traduction.
- `tests/e2e-playwright/es004-routes.config.ts` : mGBA offscreen et Playwright
  headless, assertions avant capture temporaire. La sauvegarde fixture est copiée,
  jamais sauvegardée en jeu. Les détails de l’exposition temporaire du texte
  Moomoo Milk sont explicités dans la sonde ; ce n’est pas un parcours final F-854.

Les résultats complets, hashes, écarts des BPS historiques et limites de validation
sont consignés dans la résolution du ticket. Un BPS historique ne certifie pas
la ROM reconstruite depuis les sources courantes.

## Résultats locaux F-1035

Les builds `make build-es-maint`, `make build-it`, `make build-de` ont réussi
avec `BUILD_NUMBER=0`. Le témoin FR est reconstruit avant et après sur les mêmes
sources ; `cmp` confirme l’identité intégrale, SHA-256
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
ES maintenu reste à
`708c0d1cd5abdc3138cc4663204a6cc7fba704c8a7ea9149cf5ecc893311f0bc` :
les contrats seuls n’introduisent aucune nouvelle traduction de production.

Les sondes ont vérifié 184 descriptions (ES-003 et ES-004) et 89 mots structurés,
dont 80 relocations Easy Chat. La comparaison intégrale aux témoins avant/après
patches n’a détecté aucune écriture hors des plages autorisées. Les tests
négatifs vérifient aussi les FE en notation hexadécimale, glyphes hexadécimaux,
espaces répétés et terminateurs internes : la mesure stricte utilise les octets
encodés, sans compter les arguments de commandes comme glyphes ou ruptures.

Le typecheck Playwright passe. Ruff passe sur les autres fichiers Python touchés ;
le builder historique conserve 101 diagnostics préexistants, zéro nouveau
(comparaison des codes/messages avec HEAD avant modification). Aucun attendu de
lint ou de test n’est assoupli pour masquer ces diagnostics.

Les hashes reconstruits diffèrent du manifeste BPS historique (build 50),
sans modification des BPS ni de leurs attendus :

| Langue | Reconstruction BUILD_NUMBER=0 | Cible BPS historique |
|---|---|---|
| fr | `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863` | `c603198494cbee13c7e2ff8289763b9838644d11d50bf7c715c52bdf0360a7c4` |
| de | `fc1774fdd24ba441b2f5fc21fcbd0518a73bdd5f8b64ffc6a8753272c174c39f` | `f54046006f50e0596505e6028611825051262906e5659c9178557fccb49d3cb5` |
| it | `cb9cd80a36890e9d06e0140a33d9e2a128810ae72dc0f37c597a990952103279` | `ad71f26b57bb849f1147469916ca7592566b34e0c60df91b4eff1e4ebf020356` |

Cette divergence n’est pas imputée à ce ticket : la référence de non-régression
FR est le témoin reconstruit sur les mêmes sources, pas la release historique.

`make test-python` : **9 618 passed, 3 skipped, 4 419 deselected**, zéro échec
(822,77 s). Les trois skips sont des conditions préexistantes de tests de pont
émulateur, de séquences FD et de CSV dynamique ; aucun skip ajouté par ce ticket.
Les tests ROM ciblés sont exécutés séparément (la cible Make les désélectionne).
Playwright ES-004 final :1 passed ; régression B-1031 :1 passed. Les deux sondes
binaires finales passent également après le contrôle strict des octets.
