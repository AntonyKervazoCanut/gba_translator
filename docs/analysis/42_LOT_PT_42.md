# PT-42 — mouvements, menus techniques et DexNav

## Périmètre et sources

F-801 ; prérequis F-758 et F-759 intégrés. Le manifeste PT-42 fait foi :
283 offsets, aucun ajout hors lot. L’audit `languages/pt/data/pt42_audit.json`
consigne chaque offset, sa préimage binaire, l’extraction EN, la comparaison FR,
les références exhaustives, le statut et les valeurs/budgets livrés.

L’étiquette provisoire « Combat et descriptions » est trompeuse : les fragments
français du fichier EN sont des reliquats de la base historiquement contaminée.
La ROM EN propre, dont le SHA256 est figé dans l’audit, contient ici 221 noms
de mouvements (indices 702–922, cellules fixes de 13 octets), 16 libellés de
menus techniques et 44 textes DexNav. Aucun texte Pokédex n’est traduit à ces
adresses. Les noms de mouvements non attestés restent exactement en anglais,
y compris les abréviations natives ; même politique pour Surf, Poké Balls et les cannes.
Au total : 50 traductions, 231 valeurs conservées, 2 exceptions.

`0xa439b0` est absent de l’extraction EN (la valeur Python affichée « None »
n’est pas une chaîne source). La ROM contient Water, la FR Eau, et les
consommateurs 0x9d7320/0x9d7614 prouvent le libellé d’habitat : traduction Água.
Le guillemet parasite de la source à 0xa43b3d est corrigé dans le texte PT,
sans changer sa commande finale FC 09. Les tampons FD 02/FD 03 et l’icône
F8 03 sont conservés en octets, dans le même ordre. Aucune page FA/FB supprimée. L’espace final de Chain: est encodé explicitement
par `<0x00>` pour survivre aux lecteurs combined qui retirent les blancs finaux.

## Injection et tables fixes

Le patch PT `batch_42` réutilise le repointage atomique partagé existant.
Il finalise les 60 textes référencés après les passes génériques et contrôle
les 221 cellules de noms via les 41 pointeurs de base de la table réelle.
Il prend en charge une table relocalisée et restaure seulement les cellules
du lot si une passe intermédiaire les a altérées ; aucune cellule voisine
n’est écrite. Les préimages, budgets, terminateurs et références sont contrôlés
avant publication de la copie modifiée. Un second passage est idempotent.
Chaque nouvelle ligne de combined possède sa protection exacte dans le même commit.

Budgets : noms ≤13 octets avec terminateur ; textes repointés sans limite
artificielle de longueur de l’ancienne chaîne. Les libellés de menus techniques
mesurent au plus 98 pixels. Les messages DexNav tiennent sur deux lignes,
avec une limite statique de 196 pixels avant expansion des tampons runtime.
Les largeurs exactes et longueurs encodées figurent dans l’audit. Les noms
dynamiques restent soumis aux limites du moteur ; la preuve native utilise
les messages sans tampon pour éviter de substituer une valeur inventée.

## Exceptions, offset et pointeur

- `0xa438ef` : octet séparateur après la dernière cellule de mouvements,
  immédiatement suivi de Set Flag à 0xa438f0. Aucun pointeur vers 0xa438ef ;
  le consommateur réel est 0x9a51c8 → 0xa438f0. Traduire le préfixe chevauchant
  créerait une fausse entrée et risquerait d’écraser la chaîne vivante.
- `0xa43bc5` : ancien texte d’aide DexNav, aucun pointeur 32 bits direct dans
  les 32 Mio de source. Les messages actifs voisins sont référencés depuis
  0xa69808–0xa69820 et 0x9d58e4–0x9d595c. Aucun consommateur identifié :
  texte conservé inchangé, aucune injection revendiquée. L’absence de pointeur
  direct n’exclut pas théoriquement un adressage calculé ; certification T-848
  pourra réexaminer ce texte si un tel consommateur est découvert.

## Vérification reproductible

- `make build-pt` puis `pytest tests/e2e/pt/test_batch_pt42_rom.py` :
  SHA256 source, tous les pointeurs, toutes les préimages, 281 valeurs vivantes
  dans la ROM livrée, et conservation binaire des deux exceptions.
- `pytest tests/unit/pt/test_batch_pt42.py tests/unit/test_translation_integrity.py` :
  périmètre, glossaire, commandes binaires, budgets, injection atomique bornée,
  table fixe relocalisée, copie morte intacte et idempotence.
- `npx playwright test --config tests/e2e-playwright/playwright.pt42.config.ts` :
  trois messages DexNav réels lus via leurs pointeurs finaux, sonde msgbox native
  dans une copie temporaire de ROM, OCR des deux lignes et sauvegarde inchangée.
  mGBA Qt offscreen, Chromium headless ; capture après assertions dans `/tmp`.

## Non vérifié

La sonde de rendu ne revendique ni une navigation naturelle dans le DexNav,
ni un parcours des menus de débogage, ni les 221 mouvements en combat.
Les libellés graphiques DexNav hors manifeste restent hors périmètre.
Aucun code partagé, ROM source ou artefact de distribution modifié.

Résultats locaux : build PT réussi, 33 tests ciblés (ROM réelle, patch et
intégrité) réussis, lint ciblé réussi ; Playwright : 1 test réussi sur trois
messages natifs. L’OCR vérifie exactement les fragments portugais ; le nom
Pokémon, lu Pakemon par Vision malgré un rendu correct, est vérifié en octets.
La capture est jointe au ticket, hors dépôt.
