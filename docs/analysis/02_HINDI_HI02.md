# HI-02 — corpus EN 0x1A532F–0x23E635

F-694, suite de A-665 ; préalables F-691 et D-692 livrés et intégrés.
Convention HI-LATIN-1, glossaire 1.1.0 (ajouts propres aux surfaces de ce lot,
aucune modification des graphies déjà approuvées).

## Inventaire fermé

Le [manifeste des 400 offsets](../../languages/indie/data/hi02_audit.json)
enregistre pour chaque entrée le texte EN, le statut, le motif, le domaine,
les octets source terminés par FF et les lecteurs avec leur contexte binaire.
Il est l'inventaire exhaustif du lot, y compris les exclusions.

- Snapshot EN SHA-256 : `65e93f43b9f92f19ba011fb4971aea6f44d9cd419363d7b51d9dbe094235af19`.
- 447 lignes dans l'intervalle, **400 offsets uniques** après résolution last-wins.
- ROM EN SHA-256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
- **280 traductions** : 271 chaînes avec lecteurs absolus et neuf cellules fixes.
- **78 conservations** : noms propres, objets, formes de Rotom, classes retenues
  explicitement au glossaire et cri `Gyaoo!`. Elles ne sont pas réinjectées.
- **42 exclusions** motivées individuellement, sans ajout au combined.

Les adresses ne sont pas une cartographie géographique. Les dialogues de services,
menus de liaison, aide initiale, descriptions d'objets et classes sont identifiés
par leur contenu anglais et leurs consommateurs binaires.

## Exclusions et consommateurs

Les 23 entrées dans `0x1EAF00–0x230000` sont des données de police, protégées
dans `fixed_tables.py`, pas des chaînes à traduire. Les préfixes parasites `9`,
fragments internes et extractions tronquées ne sont pas injectés. Lorsqu'aucun
lecteur absolu n'est démontré, le motif précise cette limite : l'absence d'un
pointeur ne constitue pas à elle seule une preuve de code mort.

La page monétaire `0x1A6197` reste EN : préserver la panique, le montant et les
deux buffers exige une adaptation des sauts non validée dans ce lot. Aucun sens
n'a été supprimé pour faire tenir cette page. Les extractions mal formées des
cellules `0x23E572` et `0x23E610` restent également exclues.

Les occurrences `0x10C2A7` et `0x10C333` ressemblent à des pointeurs vers
`0x1C0DB0`, mais traversent des instructions Thumb (`30 b5 85 b0 0d 1c 08 99`).
Les collisions `0x133F573` et `0x1FC5A9F` sont dans des données non textuelles.
Ces quatre sites restent intacts. Les vrais lecteurs sont des commandes
`loadpointer`/message/`0x9B`, des pools littéraux Thumb ou des tables de pointeurs.
Les descriptions d'objets sont atteintes par les structures actives à `0x87Bxxx`.

Les classes utilisent des cellules de 13 octets à `0x23E558`, base référencée
par `0xD80A0` et `0x11B4B4`. Seules neuf cellules alignées sont écrites ; les
cellules voisines restent inchangées. Les noms non traduits sont comptés comme
conservés, jamais comme localisation hindi.

## Injection et contrôles

Le finaliseur Indie `batch_02` réutilise l'allocateur transactionnel partagé.
Les routes structurées fournissent directement les octets validés au builder :
aucune normalisation implicite des pages, couleurs ou variables. Le finaliseur
contrôle chaque lecteur après les réparations génériques du build. Il refuse
une préimage différente, un contrôle ou saut modifié, une largeur supérieure à
192 px ou une cellule dépassant 13 octets avec FF. Les buffers utilisent
l'estimation conservatrice de 54 px du moteur de mesure existant.

Les arguments autrefois affichés comme `À/Á/Â` sont écrits en tokens hexadécimaux
explicites : ils ne passent jamais par les alias de lettres. Les nouvelles
phrases sont latines simples et l'encodage strict n'autorise aucun fallback.
Chaque traduction possède sa valeur exacte dans `protected_entries.yaml`.
Les trois seeds et tous les offsets hors lot restent inchangés dans le combined.

## Validation reproductible

`make build-indie`, `make test-python`, tests ciblés
`tests/unit/test_hindi_hi02.py`, `tests/unit/test_hindi_reference.py` et
`tests/e2e/test_hindi_hi02_rom.py` (avec `-m rom`). Les tests ROM vérifient les
280 valeurs livrées, l'idempotence, les faux pointeurs, les cellules voisines,
la police et le refus atomique d'un saut supprimé.

La preuve Playwright est produite par `playwright.hi02.config.ts`, avec mGBA
hors écran et Chromium headless, sur des copies temporaires de la ROM et de la
sauvegarde. Les sondes déclenchent les lecteurs du dialogue, du Cube et du combat ;
elles ne sauvegardent pas en jeu. Les captures restent hors dépôt.

ROM FR du checkout utilisateur avant travaux :
`74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
Sources FR et police partagée non modifiées. Aucun bundle commun de release,
push ou pipeline distant n'est demandé par ce lot.

## Non vérifié

Relecture linguistique native ; parcours naturel de toutes les branches et de
tous les menus multijoueurs. Les contrôles binaires sont exhaustifs pour les
lecteurs déclarés ; les sondes visuelles couvrent les surfaces représentatives,
pas une partie complète ni toutes les valeurs possibles des buffers.
