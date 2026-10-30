# PT-51 — Descriptions Pokédex PT-BR

Le manifeste PT-51 contient exactement 300 descriptions Pokédex, de Garbodor à
Milcery (indices internes 568 à 867), et non des dialogues de scénario.
Les 300 offsets explicites, de `0x16602a4` à `0x166741c`, sont traduits.
Aucun autre offset du combined n'est modifié et aucune traduction antérieure
n'est supprimée. F-758 et F-759 sont intégrés dans la base de travail.

## Bilan offset par offset

Le bilan exhaustif est versionné dans
[languages/pt/data/pt51_audit.json](../../languages/pt/data/pt51_audit.json).
Chaque ligne du manifeste y possède : offset, statut `translated`, texte PT,
préimage binaire EN, anglais réellement lu, comparaison du corpus EN et du FR,
indice Pokédex, adresse du pointeur de structure, longueur encodée et largeurs
maximales sur les cinq polices. Aucun offset mort, corrompu ou sans consommateur :
300 descriptions et 300 pointeurs vivants ; aucune exception.

Le fichier nommé `combined_en.txt` est vide pour 270 offsets et divergent de la
ROM source pour plusieurs autres (du français ou une autre fiche). Il a été
consulté, mais les préimages anglaises de la ROM source font foi pour le sens.
Par exemple, `0x1665d78` décrit les coussinets chauds de Scorbunny, pas un liquide
mauve ; `0x166074a` décrit la fraîcheur agréable de Vanillite au toucher, pas son
souffle. Les noms d'espèces, Team Plasma, Ultra Beast, Ultra Wormhole et Soul-Heart
restent anglais selon le glossaire F-759. Les distances et vitesses sont exprimées
en unités métriques usuelles ; les 100 nœuds de Barraskewda sont conservés.

## Contrat d'injection

Les descriptions ont des pointeurs dans la table fixe `PokedexEntry`, base
`0x1a35800`, pas de 36 octets. Le patch dédié `batch_51` réutilise
`StructuredTextPatch` : vérification des préimages et pointeurs, allocation
atomique en espace libre, mise à jour des seules 300 cellules concernées,
vérification des octets et de l'absence de chevauchement, sauvegarde `.bak`.
La table elle-même reste à son adresse et ses autres champs restent inchangés.
Ce finaliseur suit les réparations et le patch de police. Aucune modification de
`src/core/` ni d'un script partagé.

Les 289 descriptions sur trois lignes et les 11 sur deux conservent leur nombre
de sauts de ligne EN ; aucun placeholder ni code de contrôle n'est ajouté.
Budgets : 53 à 94 octets par chaîne, terminateur compris ; largeur maximale
229/232 pixels sur les cinq tables de largeurs réelles après patch PT.
Chaque texte ajouté a sa protection exacte dans `protected_entries.yaml`.

## Vérification reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_pt51.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt51_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt51.config.ts
```

Les tests ROM contrôlent les 300 pointeurs de structure, toutes les préimages,
les octets réellement livrés, les cinq polices, l'isolation binaire, les autres
fiches et l'idempotence du patch.

La preuve Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen`, une copie
provisoire de la ROM finale et deux descriptions lues via leurs pointeurs
Pokédex (`0x1660637` et `0x166741c`). Une sonde msgbox native affiche les deux
premières lignes et l'OCR vérifie le portugais. La capture est produite dans le
répertoire temporaire du système, hors dépôt.

## Non vérifié

La sonde ne constitue pas une navigation dans les 300 pages du Pokédex. Les
lignes complètes et les budgets de chacune des 300 fiches sont contrôlés en
binaire ; seules deux fiches sont sondées visuellement. La certification du
parcours complet relève de T-848.
