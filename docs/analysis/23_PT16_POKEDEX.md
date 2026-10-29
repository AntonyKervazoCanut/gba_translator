# F-775 — PT-16 : descriptions Pokédex

## Périmètre et source

Les 282 offsets explicites de PT-16 sont des **descriptions Pokédex**,
et non des menus système. F-758 et F-759 sont intégrés dans la base utilisée.
Le manifeste `languages/pt/translation_batches.json` reste inchangé.

Le [bilan exhaustif par offset](../../languages/pt/data/pt16_audit.json)
contient les 282 préimages binaires, les textes anglais réellement lus en ROM,
les valeurs du fichier EN et la comparaison FR, les indices Pokédex, toutes les
références sources, les traductions et leurs budgets. Chaque entrée porte
`status: translated` : aucune exception, aucun offset abandonné ou mort.

Source anglaise : SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Le fichier appelé `combined_en.txt` est divergent pour les 282 entrées :
65 valeurs sont vides ; les autres sont essentiellement françaises et ne
correspondent pas toujours au texte anglais vivant. Les traductions suivent
l'anglais de la ROM, sans recopier ces descriptions. Ainsi Dewgong décrit
son plaisir à nager dans l'eau glacée ; Weezing décrit les deux Koffing qui
se gonflent alternativement ; Absol annonce une catastrophe naturelle.

## Injection et conservation

- Ajout limité aux 282 offsets, en fin de `combined_pt.txt`, avec 282 protections
  exactes dans le même commit. Aucune traduction préexistante supprimée.
- Noms d'espèces et de mouvements conservés en anglais conformément à F-759,
  notamment Screech, Selfdestruct, Nincada, Zangoose et Seviper. Poké Ball
  reste Poké Ball. Les distances exprimées en pieds/miles sont converties
  en valeurs métriques arrondies.
- Les 282 descriptions ont chacune deux sauts FE et trois lignes ; aucun
  placeholder ni code de page/contrôle supplémentaire. Total : 26 265 octets
  encodés, terminateurs compris. Maximum de ligne : 230 pixels dans les cinq
  polices latines réelles, tildes composés, pour un budget Pokédex de 232 pixels.
- La table fixe `0x1A35800`, pas de 36 octets, contient les pointeurs de
  descriptions. Le finaliseur `batch_16` réutilise `StructuredTextPatch` et
  relocalise les textes sans déplacer les structures ni écraser leurs champs
  catégorie/taille/poids. Il suit les passes inline, réparations et repointages.
- Weezing `0x447800` a deux consommateurs : littéral `0x146B64` et structure
  `0x1A36754`. Les deux sont vérifiés et repointés. Toutes les autres entrées
  ont un seul pointeur source, consigné dans le bilan.
- L'heuristique `pokedex.iter_entries` exclut la description EN d'Electrode
  à cause de ses guillemets courbes. Ce n'est pas une entrée morte : le test
  lit directement son pointeur de structure et vérifie sa préimage exacte.

## Recette locale

```sh
python3 -m pytest tests/unit/pt/test_batch_pt16.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt16_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt16.config.ts
```

Les tests binaires contrôlent les 282 consommateurs finaux, l'identité exacte
des textes livrés, les trois lignes, les largeurs des cinq polices, les écritures
strictement limitées aux textes et pointeurs, l'idempotence et le rejet atomique
d'une source différente. Les structures et descriptions Pokédex hors lot restent
inchangées lors de l'application isolée du patch.

La preuve Playwright utilise mGBA hors écran et une copie temporaire de la ROM
construite. Elle appelle la msgbox native sur les pointeurs Pokédex des deux bornes
du lot, sans injecter de texte de substitution. Elle exige par OCR les trois lignes
de chaque texte, y compris après défilement, avant de produire la capture dans le
dossier temporaire de l'OS. Aucune sauvegarde en jeu ni capture dans le dépôt.

## Non vérifié

La sonde visuelle n'est pas une navigation dans les 282 pages de l'interface
Pokédex et ne certifie pas le parcours complet du jeu. Cette navigation reste
du ressort de T-848. Les catégories, espèces, métriques et autres textes du
Pokédex hors des offsets PT-16 ne sont pas traduits par ce ticket.
