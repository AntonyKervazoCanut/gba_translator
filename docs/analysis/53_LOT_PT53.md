# PT-53 — Noms d’espèces en table fixe (F-812)

Le manifeste PT-53 contient exactement 300 cellules de 11 octets, de
`0x166b040` à `0x166be16`, avec des trous exclus du lot. Ce ne sont pas des
répliques du scénario : ce sont des noms d’espèces, des formes Unown et deux
libellés système d’œuf. F-758 et F-759 sont intégrés avant cette traduction.

## Sources et décisions

`languages/en/combined_en.txt` contient ici des noms français historiques
(Feurisson, Kaiminus, etc.), également comparés au corpus FR au même offset.
La source anglaise effective est donc la ROM propre `input/roms/englishrom.gba`.
Le bilan `languages/pt/data/pt53_audit.json` conserve pour chaque offset les deux
corpus, le nom anglais décodé, les octets source/final, la valeur PT, la décision,
le budget et la formule de pointeur. Son SHA256 identifie la source exacte.

Conformément au glossaire F-759, 298 noms internationaux/identifiants sont
conservés exactement, dont Typhlosion, Unown et ses suffixes. Les libellés système
`Egg` et `Bad Egg` deviennent `Ovo` et `Ovo ruim` : choix éditoriaux, sans prétendre
qu’il s’agit de noms officiellement localisés. Aucun offset n’est abandonné.
`0x166b46b` (`MISSINGNO.`, identifiant réservé) est conservé et vérifié comme cellule
valide ; aucune affirmation de rencontre de cette espèce en jeu.

## Injection et lecteurs

La base indexée réelle est `0x166a98c` (entrée 0), Bulbasaur étant l’entrée 1 à
`0x166a997`. La formule est `0x0966a98c + species_id * 11`. Il n’existe aucun
pointeur individuel par cellule. Les 42 références exactes à la base sont listées
dans le bilan et doivent rester inchangées dans la ROM finale. La sonde de rendu
lit le littéral moteur `0x11450`, puis calcule l’adresse de la cellule.

`batch_53.py`, enregistré dans `lang.yaml`, s’exécute après les passes génériques.
Il vérifie intégralement manifeste, préimages et lecteurs avant d’écrire exactement
les 300 cellules. Il ne relocalise rien et ne touche pas aux offsets des autres
lots. Les noms conservés gardent même le remplissage source ; les deux libellés
traduits sont terminés puis complétés par FF jusqu’à la limite de leur cellule.
Toutes les nouvelles valeurs ont leur protection exacte dans le même commit.

## Vérification et limites

Les tests unitaires contrôlent les 300 valeurs, le glossaire, les protections,
l’encodage sans contrôles et le budget maximal de 11 octets / 60 pixels théoriques.
Les tests ROM contrôlent chaque cellule finale, les 42 lecteurs, les largeurs dans
les cinq polices vivantes (plafond 70 pixels), les voisins inchangés, l’idempotence
et le rejet atomique de lecteurs/préimages altérés ou de ROM tronquée.

Commandes reproductibles :

```sh
make build-pt
python3 -m pytest tests/unit/pt/test_batch_pt53.py tests/unit/test_translation_integrity.py -q
python3 -m pytest tests/e2e/pt/test_batch_pt53_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt53.config.ts
```

Playwright démarre mGBA hors écran sur une copie temporaire de la ROM finale,
affiche les trois cellules `Ovo`, `Ovo ruim`, `Drifloon` avec la msgbox native,
et affirme leur texte par OCR. La sonde ajoute uniquement un script temporaire ;
elle ne remplace ni les cellules ni les glyphes et vérifie la sauvegarde inchangée.
La capture finale reste hors dépôt, dans le répertoire temporaire du système.
Cette preuve porte sur le rendu natif des cellules, pas sur une navigation complète
dans les menus Pokémon ni sur la rencontre des 298 espèces/formes.
