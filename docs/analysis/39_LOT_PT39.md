# PT-39 — descriptions et noms de mouvements (F-798)

Le manifeste fermé contient 282 offsets, sans exception morte : 149 descriptions
traduites et 133 noms conservés exactement en anglais selon F-759. Les descriptions
sont lues par 201 pointeurs, dont deux variantes physiques/spéciales pour les
mouvements Dynamax et G-Max. Les noms sont des cellules de 13 octets dans la table
vivante 0xA40A10, référencée notamment par le littéral 0x308A4. Ils ne sont pas
classés morts en l'absence de pointeur individuel.

## Sources et décisions

F-758 et F-759 sont intégrés. Chaque offset, texte EN/FR consulté, préimage binaire,
index de mouvement, pointeur, texte PT et budget est recensé dans
`languages/pt/data/pt39_audit.json`. Ce fichier constitue le bilan offset par offset.

268 valeurs du corpus `languages/en/combined_en.txt` diffèrent de la ROM anglaise
propre : entrées vides, retours perdus et fragments français issus de l'ancienne
base contaminée, notamment du Pokédex dans les cellules de noms. Le texte anglais
est donc décodé à l'offset exact dans la ROM SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
La comparaison française est conservée, sans la prendre pour autorité mécanique.
Ainsi Freezing Glare décrit une lésion par froid, pas le gel du corpus EN contaminé.
« lesão por frio » est une traduction descriptive éditoriale de frostbite, sans
prétention de nomenclature officielle. Les noms de mouvements, terrains et formes
non attestés restent anglais. Les types et statistiques suivent F-759 (PS,
Velocidade, Ataque Especial, etc.).

## Injection et limites

Le patch PT dédié est exécuté après les passes génériques. Il résout les descriptions
par les pointeurs audités, préserve leurs ruptures exactement et respecte cinq
lignes de 122 pixels au maximum. Aucune description n'a de variable, code de page
ou contrôle autre que FE/FF. Les noms restent dans leurs cellules fixes, terminateur
compris, sans effacer le remplissage voisin. Les 282 valeurs sont protégées dans
le même changement ; le combined existant est préservé octet pour octet avant les
ajouts du lot.

Le compteur partagé historique `MOVE_COUNT=894` ne couvre pas les derniers G-Max
présents dans cette ROM : PT-39 atteint les indices 921/922. Le patch valide
explicitement ces index et leurs préimages sans modifier le code partagé. Le helper
`StructuredTextPatch` assure ensuite allocation, repointage et vérification.

## Vérification reproductible

- `python3 -m pytest tests/unit/pt/test_batch_pt39.py`
- `make build-pt`
- `python3 -m pytest tests/e2e/pt/test_batch_pt39_rom.py -m rom`
- `npx playwright test --config tests/e2e-playwright/playwright.pt39.config.ts`

Les tests contrôlent la couverture exacte, les protections, la politique des noms,
les effets sensibles, les contrôles et budgets ; puis toutes les références ROM,
les lecteurs Thumb, les octets finaux, les métriques des cinq polices, l'idempotence,
l'atomicité sur préimage invalide et l'absence d'écriture hors des cellules/pointeurs
ou nouvelles zones allouées du lot.

La preuve Playwright utilise le véritable résumé mGBA sur une copie temporaire :
les textes livrés sont placés dans les slots du Pokémon de la fixture pour atteindre
les trois cas sans sauvegarde en jeu. Le nom Pound et la description sélectionnée
sont intentionnellement associés pour la sonde ; cela ne représente pas une
association de gameplay livrée. La preuve ne certifie pas les effets de combat de
tous les mouvements ni un parcours complet du jeu. Captures hors dépôt uniquement.
