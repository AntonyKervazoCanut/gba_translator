# PT-87 : livraison et validation finale de F-846

## Périmètre livré

Les 300 clés explicites de PT-87 sont décrites individuellement dans
`languages/pt/data/pt87_audit.json` : 282 traductions, 12 valeurs conservées
(noms propres, noms Pokémon et cris), six exceptions documentées. Les 294
valeurs vivantes possèdent leur protection exacte. Les zones comprennent
Tarmigan et ses cauchemars, les missions, les légendaires, les Miltank,
le voleur de nourriture et Lost Tunnel.

Le finaliseur `batch_87` contrôle 422 références textuelles et 295 groupes
canoniques : le groupe supplémentaire distingue le possessif féminin `sua`
du pronom objet `ela`. Les deux titres partageant un suffixe sont isolés.
Les exceptions ne revendiquent aucune injection : deux dialogues sans lecteur
textuel identifié, trois clés fantômes avant un titre vivant et le nom Bullo
sans référence. Les motifs PCM et Thumb restent des données binaires préservées.
L'absence de pointeur identifié ne prouve pas une inaccessibilité dynamique.

## Intégration de B-1034

Le commit `1179db62` est présent dans l'ascendance du worktree parent. Sa revue
confirme le routage canonique PT-83 à PT-88, les préimages et lecteurs stricts,
les écritures bornées sans padding, et le maintien de tous les finaliseurs.
Les limites de l'allocateur et les réservations moteur ne changent pas.
Voir `docs/92_PT_STRUCTURED_ALLOCATION.md` pour le diagnostic et les preuves
multilingues de l'enfant ; elles ne sont pas présentées comme des exécutions
supplémentaires du parent.

## Vérifications finales du parent

- `make build-pt` complet réussi sur les 88 lots ; 1 761 cellules canoniques,
  livraison intégrale contrôlée ; PT-87 : 295 groupes vérifiés, trois relocalisés.
- SHA256 PT : `dbd465155173ba676a2f5963ca742097c4860a755e567282bc2b498342d6b1eb`,
  identique aux deux builds de l'enfant.
- 311 tests unitaires PT-87 et routage réussis.
- 31 tests ROM PT-83, PT-85 à PT-88 et pression réussis, dont les sept
  tests officiels PT-87, sur la ROM fraîchement reconstruite.
- Playwright PT-87 : un test réussi, trois premières pages réelles lues aux
  pointeurs finaux, rendues par mGBA Qt offscreen et vérifiées par OCR dans
  Chromium headless. La copie de sauvegarde reste identique. Capture jointe
  au ticket F-846, hors dépôt.
- ROM FR présente inchangée au SHA256 de référence :
  `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.

## Non vérifié

Parcours naturel de toutes les scènes, toutes les pages à l'écran et toutes
les expansions de buffers en situation réelle. Les contrôles ROM couvrent
les valeurs intégrales, commandes, budgets des cinq polices, pointeurs,
exceptions binaires, atomicité et idempotence ; les sondes visuelles ne sont
pas un parcours naturel. Les trois skips préexistants de la suite standard
rapportés par B-1034 ne sont pas comptés comme réussis. La certification
PT globale et la release restent réservées à T-848. Aucun push ni pipeline
distant n'est autorisé par cette livraison.
