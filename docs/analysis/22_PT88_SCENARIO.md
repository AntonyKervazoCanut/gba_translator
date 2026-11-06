# PT-88 — Missions secondaires et scénario étendu

## Périmètre et résultat

F-847, après intégration de F-758 (police/charmap) et F-759 (glossaire).
Le manifeste `languages/pt/translation_batches.json` fait autorité : **300 clés**,
290 entrées avec consommateur texte et 10 exceptions. Aucune autre clé de traduction
n'est ajoutée ou modifiée. Les traductions préexistantes restent intactes.

Les scènes réelles sont les ruines et Dugtrio, Nine Tails of Snow, Portal Purge,
Tessy et Cootes Bog, la fille de Rift Cave/Palkia, The Rogue Electivire et la
Science Society, Swords of Justice/Keldeo, The Terror Granbull, et Too Much TV.
Les noms propres non attestés restent anglais suivant F-759 ; les dialogues,
objectifs et titres éditoriaux sont rédigés en portugais brésilien.

## Bilan offset par offset

[`pt88_audit.json`](../../languages/pt/data/pt88_audit.json) contient les 300 clés
**dans l'ordre du manifeste**. Chaque entrée consigne la scène, le texte anglais
complet décodé de la ROM, sa préimage hexadécimale, les sites consommateurs,
la traduction et sa protection exacte, le budget, les largeurs et les variables.
Les textes tronqués de `combined_en.txt`, notamment l'explication Dynamax
(0x1fad816) et la mission TV (0x1fb052c), sont intégralement reconstitués depuis
la ROM source. Le français au même offset sert de comparaison, sans reprendre
ses toponymes ni ses erreurs de sauts de ligne.

| Clé | Statut et justification |
| --- | --- |
| 0x1faa339 | Préfixe d'alignement `00c046` ; lecteurs réels vers 0x1faa33c, traduit dans ce lot. |
| 0x1facb77 | Bourrage `00` ; lecteurs réels vers 0x1facb78, traduit dans ce lot. |
| 0x1fadf36 | Préfixe d'alignement `c046` ; lecteurs réels vers 0x1fadf38, traité dans ce lot. |
| 0x1fae268 | Message inactif, aucun pointeur direct ou intérieur ; lecteurs voisins vers 0x1fae1ff et 0x1fae28d. |
| 0x1fb3869 | Fragment `Team ` sans lecteur direct ou intérieur ; dernier texte voisin vivant 0x1fb0b3b. |
| 0x1fd233c | Motifs 4bpp, pas une chaîne texte. |
| 0x1fd235a | Motifs 4bpp, pas une chaîne texte. |
| 0x1fd2369 | Motifs 4bpp, pas une chaîne texte. |
| 0x1fd23a0 | Motifs 4bpp, pas une chaîne texte. |
| 0x1fd23be | Motifs 4bpp, pas une chaîne texte. |

Les cinq dernières clés appartiennent au graphisme indexé depuis 0x1fd226c,
référencé par le littéral 0x1ed48fc. Le lecteur 0x1ed4882 multiplie l'index par
0xC0. Ses octets, la base et le littéral sont contrôlés dans le test ROM.
Les exceptions ne reçoivent aucune traduction et n'écrivent pas dans ces données.

La clé **0x1fae6f3** est, à l'inverse, traitable : son nom de Dresseur vivant
`Terror Granbull` commence à 0x1fae6f4 et est ciblé par 0x23e60e. Le finaliseur
conserve le préfixe `00` et vérifie la cellule réellement lue. `Science Society`
est également un nom à pointeur (0x23e6eb), pas une cellule de longueur fixe
à écraser sur place. Aucune autre table fixe non couverte n'a été identifiée.

Deux occurrences ressemblant à des pointeurs sont **exclues** : 0x4d50b4
pour 0x1fad0be et 0x1285745 pour 0x1fb07fe se trouvent dans des échantillons
PCM. Leurs en-têtes, tailles et pointeurs d'instrument sont consignés et testés ;
le finaliseur n'altère pas ces quatre octets.

## Injection et contraintes

`batch_88`, après police et repointages génériques, réutilise le finaliseur
partagé `ScenarioTextPatch`. Il valide le SHA256 source, les préimages et chaque
référence avant toute écriture ; il relocalise atomiquement les chaînes dans
l'espace libre final puis vérifie tous leurs lecteurs. La réplique 0x1faee2c reçoit un helper de genre **privé** : seul l'appel
0x1eaed7a est redirigé, avec les deux branches `dele/ele` et `dela/ela`.
Le helper original 0x1e8a141 et les chaînes partagées des lots PT-22/25 restent
intacts. `n` suivi du pronom donne `nele/nela`, et le possessif donne
`dinheiro dele/dela` ; les deux cas sont testés sur les octets du script final.
Aucun changement du noyau ni d'un script partagé. Sauvegarde `.bak` avant modification de la ROM construite.

Les commandes FC/FD/F8/F9/F7 et les ruptures FA/FB conservent leur ordre et leurs
arguments. Les retours FE sont réagencés pour les fenêtres réelles : deux lignes
au début d'une page de dialogue, une ligne après chaque défilement ; trois lignes
au plus dans une description de mission. Budgets : 172 px pour les missions,
104 px pour les noms de Dresseur, 192 px conservateurs pour les autres textes.
Les cinq polices latines sont mesurées, avec développement des variables.
Les octets B0 représentent les ellipses, distincts des guillemets B1/B2.

Le manifeste de protection contient les 290 valeurs exactes dans le même commit
que leur ajout. La présence en source ne vaut pas validation d'injection : le test
ROM relit chaque pointeur de la ROM finale et compare toute la chaîne, terminateur
compris. Il contrôle aussi bornes, absence de chevauchement et idempotence.

## Recette locale

```sh
python3 -m pytest tests/unit/pt/test_batch_pt88.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt88_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt88.config.ts
```

La sonde Playwright lance mGBA hors écran sur une **copie temporaire** de la ROM
finale. Elle appelle la msgbox native avec les pointeurs livrés de trois dialogues
(Electivire, porte à code, Dream Research Lab), vérifie les mots rendus par OCR,
et vérifie que la sauvegarde temporaire n'a pas changé. La capture est produite
dans le répertoire temporaire système et jointe au ticket, jamais au dépôt.

## Non vérifié

La sonde ne remplace pas un parcours manuel des missions ni une certification
complète du jeu : elle contrôle les deux premières lignes de trois dialogues.
Toutes les pages des 290 entrées sont toutefois vérifiées en binaire et en largeur.
Le passage global de la langue à `complete` reste réservé à T-848.
