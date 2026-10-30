# PT-44 — Répliques de Dresseurs

Le manifeste fait autorité : 282 offsets, de `0xa451a4` à `0xa479e4`.
Les deux prérequis F-758 et F-759 sont intégrés. Le domaine réel est constitué
de 33 noms propres et de 249 répliques de Dresseurs (avant combat, défaite,
victoire), et non de descriptions de capacités.

Les 33 noms restent anglais selon F-759, notamment Big Mo, Galavan et Tessy,
sans reprendre les adaptations françaises. Les 249 répliques sont ajoutées
chirurgicalement au combined, avec leurs 249 protections exactes. Le talent
Pickpocket garde son nom anglais. Les probabilités de 3 %, le percentile 97,
les séries de victoires, la rinite et les jeux de rôle des Dresseurs sont conservés.

## Bilan exhaustif

`languages/pt/data/pt44_audit.json` contient une ligne par offset du manifeste :
texte anglais, comparaison française, texte PT, statut, préimage, références,
longueur encodée et largeurs. Bilan : 249 `translated`, 33 `verified_retained`,
zéro entrée morte ou corrompue. Les noms conservés sont contrôlés aux pointeurs
vivants dans la ROM construite, sans ajout artificiel au combined.

Les répliques sont référencées dans une table de structures de 20 octets :
la table commence à `0xa6f574`, chaque structure contient huit octets de
métadonnées puis trois pointeurs texte espacés de quatre octets. Ses sept
références moteur sont consignées et vérifiées identiques après build. Le premier enregistrement de ce lot est partiel :
`0xa6f580` et `0xa6f584` sont les deux derniers pointeurs de l'enregistrement
qui commence par son premier pointeur à `0xa6f57c`.

Le motif `44 77 a4 08` à `0x176ca0c` n'est pas un consommateur de
`0xa47744` : il se trouve dans le bloc LZ77 à `0x176c93c`, long de 910 octets,
qui produit 2048 octets graphiques. Le test vérifie la décompression et
l'intégrité de tout ce bloc après build. Seul le vrai pointeur à `0xa6fb98`
est fourni au finaliseur pour cette réplique.

## Livraison et vérifications

Le patch PT `batch_44` réutilise `BorriusTextPatch` : validation des préimages,
allocation bornée et repointage des seuls consommateurs audités. Il garantit
la livraison exacte après les passes génériques, sans agrandir de cellule fixe.
Aucun code partagé, aucune entrée d'un autre lot ni traduction existante ne change.
Les contrôles et ruptures FE/FA/FB sont identiques à l'anglais, dans le même ordre.
Les lignes respectent 204 pixels ; les tests ROM mesurent aussi les largeurs
dans les cinq polices natives. Le plafond encodé est de 512 octets par chaîne.

Commandes de validation :

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt44.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt44_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt44.config.ts
```

La preuve Playwright utilise mGBA hors écran et deux pointeurs de la ROM finale,
avec assertions OCR des deux premières lignes de chaque réplique (accents et
ponctuation normalisés ; mots complets exigés). Les octets, ponctuation comprise,
sont comparés exactement à la source PT avant rendu. Seul un script
événement temporaire appelle les boîtes natives ; les chaînes et glyphes livrés
ne sont pas remplacés. La capture est créée dans le dossier temporaire de l'OS.
Il s'agit d'une sonde de rendu, pas d'un parcours des 249 rencontres en jeu.

Résultats locaux : 32 tests lot/intégrité, 17 tests lot/glossaire/charmap,
2 tests ROM et 1 test Playwright réussis ; lint Python ciblé et diff propres.
Le build PT finalise 249 chaînes, avec 137 repointages supplémentaires.
La largeur maximale mesurée dans le manifeste est de 198 pixels et la chaîne
la plus longue occupe 96 octets, terminateur compris.
