# ES-008 — Qualification des trois fragments grammaticaux (B-1038)

## Décision

**Aucun patch de production nécessaire.** Les trois clés restent dans le bilan
contractuel de F-858, avec les justifications ci-dessous. Ce ticket ne traduit
aucune entrée : aucun combined, manifeste de protection, glossaire ou lots.json
n'est modifié. Il ne réutilise pas implicitement B-1033 (PT-BR, encore à faire).

| Clé | Consommateur vérifié | Conclusion pour F-858 |
|---|---|---|
| `0x3FE865` | Début réel `0x3FE864`, littéral `0xE674C`, appel `0xE6744` à `0x8DA4`, tampon `0x02021CD0` | Ancienne liste d'éligibilité d'équipe, routine sans racine exécutable. Exclusion documentée, pas un texte de combat à traduire. |
| `0x3FE88C` | Début réel `0x3FE88B`, littéral `0xD8704`, appel `0xD86F4` à `0x8D84` | Copie vivante de `00 DD E7 FF` dans le buffer 0 pour les groupes 0–2 ; ce buffer n'est pas consommé dans la phrase produite. Aucun alias d'injection à ajouter. |
| `0x3FE88F` | Littéral direct `0xD871C`, appel `0xD8710` à `0x8D84` | Copie vivante de `B4 E7 FF` dans le même buffer pour les groupes 3–4 ; aucune construction possessive affichée. Ne pas traduire en « de » ni réordonner les buffers. |

Les octets des deux dernières branches sont bien exécutés ; **seul leur résultat
est inutilisé par le message**. Les qualifier de routines mortes serait faux.
La preuve de la première clé est détaillée dans [008_GRAMMAIRE_RACINES.md](008_GRAMMAIRE_RACINES.md).

## Chemin réel des deux fragments de combat

Le point d'entrée public `0xD7274` est un trampoline (`00 49 08 47 89 DA 9B 08`)
vers `0x9BDA88`. Le sélecteur du message 4 à `0x9BDB86–0x9BDB8E` rejoint
`0x9BDF06`. Il appelle `0xD86C8` via le littéral `0x9BE0D0` et le veneer
`0x9BE3A2` (`bx r3`). L'ancien appel direct à `0xD75F2` appartient au corps
historique ; son message final utilise lui aussi `0x3FD57B`.

Correction du relevé initial : **`0x8D84` est StringCopy**, avec retour du pointeur
sur le FF ; **`0x8DA4` est StringAppend**, qui cherche d'abord le FF puis appelle
StringCopy. Le fragment ne s'ajoute donc pas au nom du Pokémon : il remplace le
contenu du premier tampon.

`0xD86C8` parcourt les numéros d'attaques de `0x3FEA70`, séparés par quatre
valeurs zéro. Les groupes contiennent respectivement 42, 7, 18 et 47 numéros ;
le groupe 4 est le repli pour les autres numéros. La comparaison `r2 <= 2`
choisit « is » ; les groupes 3 et 4 choisissent apostrophe-s.

| Groupe | Cas exécuté | Buffer 0 après sélection | Phrase source complète |
|---|---|---|---|
| 0 | 14 / Swords Dance | `00 DD E7 FF` | `ABCDEFGHIJ used\nSwords Dance!` |
| 1 | 100 / Teleport | `00 DD E7 FF` | `ABCDEFGHIJ used\nTeleport!` |
| 2 | 96 / Meditate | `00 DD E7 FF` | `ABCDEFGHIJ used\nMeditate!` |
| 3 | 1 / Pound | `B4 E7 FF` | `ABCDEFGHIJ used\nPound!` |
| 4 | 2 / Karate Chop | `B4 E7 FF` | `ABCDEFGHIJ used\nKarate Chop!` |

Le nom de l'attaque est préparé séparément à `0x9BDF60–0x9BDF68`, via
`0x9BCFCC`, dans le buffer 1. Le repli pour un numéro supérieur au plafond passe
par `0x9BDF1A–0x9BDF2E` et la table de types. Puis `0x9BDF32–0x9BDF36` appelle
`0xD8720` via `0x9BE0E0` : les cinq branches ajoutent toutes `AB FF` (« ! »).

La phrase ordinaire est sélectionnée via `0x9BE13C → 0x3FD57B` :
`FD 0F 00 E9 E7 D9 D8 FE FD 01 FF` = attaquant + « used » + saut + **buffer 1**.
La variante Z de statut passe par `0x9BE0EC → 0xA4C42B` :
`FD 0F 00 E9 E7 D9 D8 FE D4 AE FD 01 FF`, avec le préfixe Z-.
**Aucune des deux ne contient FD 00.** La routine d'expansion publique
`0xD77F4` rejoint le moteur CFRU via `0xD7868`. Les tests exécutent ce chemin
entier et surveillent les lectures mémoire : zéro lecture du buffer 0 pendant
l'expansion, pour les cinq groupes, Z et le repli par type.

Chaque appel public recharge les trois buffers depuis le paquet de commande
(`0x9BDAF2–0x9BDB24`) avant la sélection du message. Le suffixe local n'est pas
écrit dans le paquet : il ne devient pas une traduction implicite d'un message
suivant. Les autres messages FD 00 ne doivent donc pas être modifiés globalement.

## Buffers, commandes et budgets

- Buffer 0 : `0x02022AB8`, buffer 1 : `0x02022AC8`, buffer 2 : `0x02022AD8`.
  Espacement 16 octets. La copie initiale historique parcourt 17 octets par
  buffer (indice 0 à 16 inclus) ; cette particularité existante est conservée.
- Sélecteur grammatical : écrit exactement 4 ou 3 octets, FF compris.
  Le test sur tranche binaire réelle garde des sentinelles jusqu'au voisin.
- Ajout de ponctuation : un nom temporaire de 14 octets produit exactement
  16 octets avec `!` et FF, sans écriture dans le buffer suivant.
- Nom du Pokémon testé : 10 caractères, limite du surnom. Nom d'attaque en
  table native : cellule de 13 octets ; la fixture longue a 12 caractères + FF.
- Phrase finale : `0x0202298C`. Les 256 octets de sonde sont initialisés à A5 ;
  les tests exigent la phrase entière, son unique FF terminal et le reste A5.
- Les templates temporaires conservent **FD 0F puis FD 01**, FE et FF. Aucun
  échange global de tokens, aucune modification de FC/F8/F9/F7, aucun nouvel
  offset contractuel. Les traductions de fixture (« ha usado », « Danza Espada »,
  etc.) ne sont pas importées dans les sources.

## Empreintes de cette qualification

- Source EN : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
- Build ES maintenu (`BUILD_NUMBER=0`) : `c415e3913a23dfc296746ebfe9dcafabd81efe05023e2c4b56967960999e141b`.
- Les tranches de routine de la fixture portent également le SHA-256 de leur ROM source.

## Validation reproductible

- `make build-es-maint BUILD_NUMBER=0` : build réel réussi, puis contrôle des
  lecteurs et préimages sur la ROM produite, pas seulement sur la source.
- `python -m pytest -q tests/unit/test_es008_grammar.py tests/unit/test_es008_dead_party_routine.py` :
  32 tests réussis, dont exécution Thumb sous Unicorn et scans de racines sur les
  deux ROMs. Unicorn est requis seulement pour les cas marqués `emulator` ;
  les gardes de fixture restent exécutables dans la suite Python normale.
- `npx playwright test --config tests/e2e-playwright/es008-grammar.config.ts` :
  réussi en headless, mGBA avec `QT_QPA_PLATFORM=offscreen`. La sonde appelle le
  vrai point d'entrée public pour sept cas, compare les 256 octets de chaque
  sortie, puis affiche les cinq groupes avec le décompresseur natif de police.
  Les pixels de toute la mire sont comparés aux glyphes ROM, y compris le
  point d'exclamation final et l'absence de texte parasite. Capture hors dépôt
  jointe au ticket : `attachment://d9a6b238-383d-449e-8bbe-5e0b535acee4`.
- Ruff ciblé, typecheck TypeScript et suite Python complète : résultats finaux
  consignés dans la résolution du ticket.

## Non vérifié / limites

La mire est une sonde moteur, pas un parcours de combat depuis une sauvegarde.
Aucune sauvegarde en jeu. Aucun texte définitif ES-008 n'est certifié ici : F-858
reste responsable de `0x3FD57B` et des autres phrases de son lot, de leur import
et de leurs protections. La phrase Z est hors de ces trois clés ; son texte de
fixture ne constitue pas une livraison linguistique. Le repli par type conserve
son nom source dans les tests afin de ne pas simuler une traduction livrée.

Aucun code partagé, descripteur, patch de langue ou binaire distribué n'est changé.
La matrice FR/IT/DE avec témoin avant/après n'est donc pas déclenchée par un
changement d'infrastructure ; les builds imposés par les hooks restent actifs.
Les gardes échoueront si une future ROM réintroduit une racine ou consomme le
buffer grammatical : cette exclusion doit alors être réévaluée.
