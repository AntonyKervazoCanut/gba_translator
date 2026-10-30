# PT-56 — Noms d'espèces et extractions graphiques

Le manifeste PT-56 contient exactement 300 offsets. Son intitulé provisoire
« Scénario étendu » ne décrit pas les données réelles : 216 cellules de noms
d'espèces, puis 84 faux textes issus d'images. Aucun dialogue à traduire.

## Décisions par offset

Le bilan exhaustif est `languages/pt/data/pt56_audit.json`, dans l'ordre exact
du manifeste. Chaque ligne indique l'extraction EN, la comparaison FR, la
préimage binaire, les références et la justification de son traitement.

- 216 `retained_english` : noms anglais réels conservés conformément à F-759,
  ajoutés au combined PT et protégés à valeur exacte. Les abréviations du jeu
  (`Corvsquire`, `Corvknight`, `Centskorch`, `Poltegeist`, `Stonjorner`,
  `Basculegon`) sont conservées, sans inventer de localisation.
- 84 `exception_binary` : 5 offsets internes à des sprites LZ77 de 2048 octets
  décompressés et 79 internes aux icônes référencées par `gMonIconTable`.
  Aucun pointeur direct vers ces 84 offsets. Chaque propriétaire est identifié
  par son adresse, sa taille et le site du pointeur ; les tests redécompressent
  les sprites et vérifient les indices de la table des icônes. Aucune entrée
  de traduction n'est créée pour ces données graphiques.

`languages/en/combined_en.txt` contient des noms français historiques dans cette
zone. La ROM anglaise propre fait foi pour les noms, avec son SHA256 inscrit
dans l'audit. La comparaison FR sert à identifier cette contamination, jamais
à importer ses noms dans le portugais.

## Consommateurs et injection

La table vivante commence à `0x166a98c` (cellule zéro), avec 42 références dans
la ROM source. Les cellules font 11 octets ; les 216 offsets du lot vont de
`0x166d7de` à `0x166e11b`. Elles sont lues par index, sans pointeur individuel.
Le patch `languages/pt/patches/batch_56.py` valide les lecteurs et les préimages,
puis réutilise l'injecteur partagé existant des noms d'espèces avec une sélection
limitée au lot. Il s'exécute après les passes génériques et vérifie les octets
terminés réellement injectés. Les noms déjà corrects restent inchangés.

Tous les noms sont encodables sans commande ni placeholder ; aucun saut de page
n'est à préserver. Leur largeur maximale mesurée est 59 pixels dans les cinq
tables de police moteur. Les tests vérifient aussi l'idempotence, la réparation
de cellules corrompues, le refus atomique d'une préimage/lecture différente et
l'absence d'écritures hors des 216 cellules autorisées.

## Validation reproductible

```sh
make build-pt
python3 -m pytest -q tests/unit/pt/test_batch_pt56.py tests/unit/test_translation_integrity.py
python3 -m pytest -q tests/e2e/pt/test_batch_pt56_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt56.config.ts
```

La sonde Playwright lance mGBA hors écran sur une copie temporaire de la ROM
finale et appelle une vraie msgbox sur les cellules Lycanroc et Glastrier,
résolues depuis le lecteur de table `0x11450`. Elle vérifie les octets et le
texte rendu par OCR, puis capture le résultat hors dépôt. Aucune sauvegarde
en jeu. Cette preuve ne revendique ni une navigation Pokédex ni l'affichage
exhaustif des 216 formes ; ceux-ci ne sont pas vérifiés par cette sonde.

Aucun code partagé ni traduction d'un autre lot n'est modifié. Les 84 données
graphiques doivent rester identiques à la source dans la ROM finale.
