# PT-54 — noms d’espèces et de formes

Le manifeste contient exactement 300 offsets, de `0x166be21` à `0x166cafa`.
Le domaine réel est la table fixe des noms d’espèces (cellules de 11 octets),
non le scénario. F-758 et F-759 sont intégrés dans l’ascendance du lot.

Le corpus `combined_en.txt` est historiquement français dans cette zone.
Chaque entrée a été comparée au FR au même offset puis à la ROM EN propre.
Le glossaire F-759 impose de conserver les noms internationaux de cette ROM,
formes et ponctuation comprises : Drifblim, Mime Jr., Gurdurr, Flabébé, etc.
`Warrior` à `0x166c7e2` reste le nom particulier du slot Unbound ; ce n’est
pas un dialogue à traduire en « Guerreiro ». Les six Rotom et les dix-sept
Arceus sont des cellules distinctes de formes, pas des doublons à éliminer.

Le bilan exhaustif est `languages/pt/data/pt54_audit.json` : une ligne par
entrée du manifeste avec références EN/FR, nom PT retenu, préimage binaire,
index d’espèce, longueur et largeur. Les 300 entrées ont le statut
`retained_english`, conformément au glossaire ; aucune exception morte ou
corrompue, aucune entrée omise. Le FR ne contient pas `0x166caef` : cette
absence est enregistrée par `null`, sans inventer une référence française.

La base réellement référencée est `0x166a98c` (slot zéro), pas `0x166a997`
(Bulbasaur, slot un). Les 42 références sont enregistrées et vérifiées dans
la source et la ROM finale. Chaque consommateur résout `base + espèce * 11` ;
Le lecteur Thumb à `0x040fe0` charge le littéral `0x040fec`, multiplie
l’identifiant par 11 et additionne la base ; ses huit octets sont protégés
par un test ROM. L’absence d’un pointeur direct vers chaque cellule n’en fait pas du texte mort.

Le patch final PT `batch_54` utilise le correcteur partagé des noms d’espèces,
limité au manifeste PT-54. Il valide les lecteurs, les préimages et les noms
avant toute écriture, puis conserve également le remplissage FF original.
Il ne relocalise aucune table et n’écrit aucun offset d’un autre lot.
Les tests vérifient réparation, idempotence, atomicité et isolation binaire.
Toutes les valeurs ajoutées au combined sont protégées exactement.

Validation reproductible :

```sh
python3 -m pytest tests/unit/pt/test_batch_pt54.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt54_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt54.config.ts
```

Les budgets sont de 11 octets avec terminateur et de 60 pixels ; les tests ROM
mesurent les cinq polices réelles. Aucun contrôle ou saut de page n’est présent.
La sonde Playwright affiche Mime Jr. depuis sa cellule indexée réelle dans
une msgbox native mGBA hors écran ; elle contrôle les octets, le texte reconnu
par OCR et l’absence de modification de la sauvegarde. La copie instrumentée
et les captures sont temporaires, hors dépôt. Cette preuve n’est pas une
navigation exhaustive des 300 espèces dans tous les menus du jeu.
