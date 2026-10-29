# PT-41 — Noms de mouvements conservés selon F-759

## Périmètre et décision

F-800 couvre exactement les 282 offsets du manifeste PT-41. Il s'agit de
cellules de noms de mouvements, et non de descriptions. F-758 et F-759 sont
intégrés. La politique `categories.moves.fallback: preserve_english` impose
les noms anglais exacts de la ROM, y compris ses contractions historiques.
Aucun nom portugais non attesté n'est inventé. Les 282 entrées sont donc
**conservées et vérifiées**, et ne sont pas revendiquées comme des traductions
lexicales portugaises. Aucun offset n'est exclu, mort ou corrompu dans la ROM.
La cellule 0xa42034, absente du manifeste, n'est pas touchée.

## Sources et consommateurs

`languages/pt/data/pt41_audit.json` constitue le bilan offset par offset : nom
anglais décodé depuis la ROM, comparaison FR au même offset, contenu du corpus
EN, identifiant de mouvement, cellule source complète de 13 octets, taille
encodée et largeur. Le corpus `languages/en/combined_en.txt` contient ici des
vides et des fragments de descriptions françaises provenant de l'ancienne
base déplacée ; ces fragments ne sont pas une source de noms anglais fiable.
La comparaison française permet d'identifier le domaine, sans recopier les
valeurs françaises. Le SHA256 source est figé dans l'audit.

Le moteur lit `base + move_id * 13` : la base propre est 0xa40a10, chargée
notamment via le pointeur 0x308a4. Les 41 références binaires de base sont
répertoriées dans l'audit et contrôlées dans les deux ROMs. Il n'est donc pas
nécessaire qu'un pointeur individuel vise chaque nom. Les IDs couverts vont
de 419 à 701, avec les seules discontinuités du manifeste.

## Livraison et contrôles reproductibles

Chaque ajout au combined possède une protection exacte. Le patch PT dédié
`batch_41` vérifie les lecteurs, les préimages et les noms du combined avant
la première écriture, puis restaure uniquement les 282 cellules complètes,
bourrage inclus. Il ne dépend pas de la réinsertion générique des chaînes
identiques à l'anglais et ne touche pas aux noms des autres lots.

```sh
python3 -m pytest tests/unit/pt/test_batch_pt41.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt41_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt41.config.ts
```

Les tests contrôlent les cellules finales aux adresses lues, l'identité des
41 pointeurs, les limites de 13 octets avec terminateur, l'absence de contrôles,
les largeurs dans les cinq polices réelles, l'idempotence, le refus atomique
d'un lecteur modifié et l'absence d'écritures en dehors du manifeste.
Chaque cellule finale est strictement identique à la cellule anglaise source,
bourrage compris. Une comparaison avec la sauvegarde du build juste avant le
patch dédié révèle cependant une corruption générique à 0xa42340 : l'espace
de `Shadow Force` avait été remplacé par un terminateur, affichant `Shadow`.
La finalisation restaure bien le nom entier. Les 281 autres cellules restent
identiques avant/après le patch.

La preuve Playwright hors écran lit ce nom dans la ROM finale, via la base
chargée au pointeur moteur 0x308a4 et l'index 496. Un script privé lance une
msgbox native sans modifier les octets du nom ni les glyphes ; l'OCR doit lire
`Shadow Force` au complet. La capture est produite après cette assertion dans
le dossier temporaire de l'OS, hors dépôt. Aucune sauvegarde en jeu n'est faite.

## Non vérifié

Les 282 noms restent anglais selon F-759. La sonde msgbox démontre le rendu
du nom restauré, sans revendiquer une navigation dans le menu des mouvements
ou un parcours exhaustif des 282 mouvements en combat. La certification globale
de la ROM reste du ressort de T-848.
