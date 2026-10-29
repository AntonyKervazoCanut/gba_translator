# PT-36 — descriptions et noms de talents

## Périmètre et sources

F-795, manifeste PT-36 : 282 offsets explicites, de `0xa34f4c` à
`0xa369d6`. Les zones réelles sont 187 descriptions de talents et 95 noms
indexés ; aucune description de mouvement ni dialogue dans ce lot.
F-758 et F-759 sont intégrés avant cette traduction. L'anglais de
`languages/en/combined_en.txt` est recoupé avec les octets de la ROM propre,
et le français au même offset sert uniquement de comparaison. Le bilan
exhaustif, dans l'ordre du manifeste, est
`languages/pt/data/pt36_audit.json` : texte EN, comparaison FR, PT, préimage,
références, identifiants, statut, justification et budgets pour chaque offset.

279 entrées possèdent une valeur protégée exacte : 184 descriptions traduites,
3 noms officiellement localisés et 92 noms/sentinelles conservés selon F-759.
Aucune traduction antérieure n'est supprimée. Aucune entrée d'un autre lot
n'est ajoutée au combined ou au manifeste de protection.

## Choix linguistiques et contraintes

Le glossaire figé impose `Supercrescimento`, `Incêndio`, `Dilúvio` pour
Overgrow, Blaze et Torrent. Tous les autres noms restent anglais, y compris
la sentinelle `-------` et la cellule nommée `Unused`. Cette conservation
ne signifie pas que chaque talent figure dans une équipe rencontrée en jeu.
Les noms anglais de mouvements, Berries, Memory, Plate, Honey et terrains
non attestés sont conservés dans les descriptions. Les types suivent F-759.
PS désigne les points de santé. `Atq. Esp.` et `stats` sont des raccourcis
éditoriaux de descriptions ; aucune nouvelle nomenclature officielle n'est
revendiquée. Les signes + et - indiquent une hausse/baisse sans changer la
mécanique anglaise. Weak Armor concerne les stats du porteur ; Gooey concerne
la Velocidade de l'attaquant. Filter/Solid Rock partagent bien leurs pointeurs.

Aucune chaîne source de ce lot ne contient de variable, contrôle ni saut de
page. Les traductions restent sur une ligne, sans nouveau contrôle. Budgets :
192 pixels par description, 17 octets terminateur inclus et 120 pixels par
nom. Les tests vérifient aussi les cinq vraies tables de largeurs dans la
ROM PT finale. Le nom Supercrescimento occupe les 16 caractères disponibles,
avec son terminateur dans le dernier octet de sa propre cellule.

## Consommateurs et injection

Les descriptions sont adressées par la table `0x96de04`, indexée par ID de
talent. Les quatre variantes contextuelles de mouvements (Grass, Tail,
Water/Sp. Atk, Drill) sont les littéraux `0x9a9438`, `0x9a943c`, `0x9a9440`,
`0x9a9444` du lecteur Thumb `0x9a93fc`. Celui-ci sélectionne les variantes
selon les paramètres ; il ne s'agit pas de chaînes mortes absentes de la table
principale. L'audit conserve aussi le pointeur supplémentaire de Moxie à
`0x2bf759`. Chaque référence déclarée est vérifiée sur la ROM source entière.

Les noms commencent à `0xa36398` avec un pas de 17. Le lecteur à `0x9a9ca8`
multiplie bien l'ID par 17 et utilise le littéral à `0x9a9cdc`. Le patch PT
`batch_36` est exécuté après les réparations génériques. Il réutilise
`StructuredTextPatch` pour finaliser tous les pointeurs de descriptions et
écrit les noms dans leurs cellules, avec validation préalable et écriture
atomique. Il ne dépend pas de l'absence silencieuse d'une entrée du CSV.
Les tests en ROM vérifient les octets aux cibles finales, l'idempotence et
l'absence d'écriture hors des cellules/références/cibles autorisées.
Aucun code partagé n'est modifié.

## Trois exceptions mortes justifiées

| Ancien offset | Anglais résiduel | Référence active du talent | Cible EN réellement consommée |
| --- | --- | --- | --- |
| `0xa35424` | Hurts to touch. | `0x96dff0`, ID 123 | `0xa36294`, Knockouts boost Sp. Atk. |
| `0xa35811` | No special Ability. | `0x96e0c0`, ID 175 | `0x24f66f`, formulation active hors PT-36 |
| `0xa35dcf` | Blocks priority moves. | `0x96e170`, ID 219 | `0xa362eb`, Sometimes moves quicker. |

La recherche des pointeurs 32 bits sur toute la ROM ne trouve aucune référence
vers ces trois anciens textes. Ils restent sans entrée PT et sans écriture
par le patch. Les remplacements de 123 et 219 sont traduits à leurs offsets
vivants du même lot ; le texte de 175 appartient à un autre lot et reste hors
périmètre. Les preuves binaires et références sont vérifiées par les tests ROM.

## Vérification reproductible

- `python3 -m pytest -q tests/unit/pt/test_batch_pt36.py tests/unit/test_translation_integrity.py`
- `make build-pt`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt36_rom.py -m rom`
- `npx playwright test --config tests/e2e-playwright/playwright.pt36.config.ts`
- Ruff ciblé sur le patch et les tests Python ; hooks de commit actifs.

La preuve Playwright utilise le vrai résumé Pokémon de mGBA hors écran, une
copie temporaire de ROM et une copie de sauvegarde. Les chaînes sont d'abord
comparées exactement aux octets livrés, puis leurs cellules sont substituées
uniquement dans la copie pour rendre les cas indépendants du talent de la
fixture. La sonde n'affirme pas l'association mécanique entre ces noms et ces
descriptions. Elle vérifie par OCR les noms complets et les descriptions (tolérance bornée
aux confusions de la police inclinée pour les noms, octets exacts en amont),
puis leur restitution après un aller-retour entre onglets. Les captures sont
produites après assertions dans le répertoire temporaire du système, hors dépôt.

Validation locale du lot : 33 tests ciblés intégrité/glossaire réussis,
construction `make build-pt` réussie, 2 tests binaires réussis et 3 tests
Playwright réussis. Ruff ciblé et diff sans erreur.

## Non vérifié

Ce lot ne certifie pas toutes les interactions des talents en combat, ni leur
présence dans chaque équipe rencontrée. La sonde de résumé valide le rendu,
pas une partie complète. La certification globale relève de T-848. Aucun
push ni pipeline distant n'est lancé.
