# PT-81 — Tombe, minage, Victory Road et Vivill Town

Le manifeste contient 299 clés, de `0x1f80178` à `0x1f855f0`. Le bilan
exhaustif se trouve dans `languages/pt/data/pt81_audit.json`, dans l'ordre du
manifeste : anglais exporté, référence française, préimage binaire, sites et
contextes des pointeurs, traduction, octets encodés, largeurs et justification.

297 clés ont une valeur PT protégée ; deux sont des exceptions démontrées.
Les 35 surnoms et noms propres des échanges restent anglais selon F-759.
Aucune traduction existante n'est supprimée et aucun autre lot n'est édité.

## Zones et consommateurs

- Thundercap Mt. : Dresseurs et amélioration des Power Items.
- Tombe de Borrius : puzzle, Fred, lave, Dusknoir, pièges et trésors.
- Tables d'échanges : surnoms et noms des partenaires, conservés.
- Carte de Dresseur : libellés, dates et douze mois ; espaces séparateurs
  encodés explicitement avec `<0x00>` pour survivre aux lecteurs de texte.
- Minage : outils, découverte d'objets, effondrement et Mining Scan.
- Underground Pass : défi quotidien (moins de 15 secondes, gros prix à
  10 secondes ou moins), objets cachés et mission.
- Toxapex, Sharpedo, inscriptions, Victory Road et Vivill Town ; tuteur
  Seed Bomb, échanges de Pokémon champignons et légendaires.

`batch_81` utilise les classes d'injection existantes. Il contrôle les préimages,
les paramètres binaires et les budgets, puis finalise les pointeurs après les
réparations, la police et le repointage générique. Une traduction ignorée ou
raccourcie par l'étape générique est ainsi réinjectée intégralement à ses vrais
lecteurs. Les tables de ce lot contiennent des pointeurs ; leurs cellules de
pointeur restent en place. Aucun offset n'appartient aux tables fixes centrales.

Les clés `0x1f80b7b`, `0x1f81d27` et `0x1f84fbf` commencent par un octet de
bourrage. Leurs consommateurs visent respectivement `0x1f80b7c`, `0x1f81d28`
et `0x1f84fc0` ; le patch conserve le bourrage et repointe ces lecteurs.
Le dialogue `0x1f806f5`, tronqué dans le combined anglais, est traité sur ses
554 octets binaires complets, jusqu'à la consigne du Pokémon de type Lutador.

## Exceptions

| Clé | Preuve | Traitement |
| --- | --- | --- |
| `0x1f80400` | Suffixe interne du dialogue `0x1f803f0`. Seule correspondance à `0x133f78a`, dans le PCM `0x133d2e4` de 23 345 octets, dont le pointeur d'instrument est `0x104fef0`. | Aucun texte ajouté, aucun repointage audio. Le dialogue parent est traduit. |
| `0x1f82bbb` | Bourrage suivi du texte `0x1f82bbc`, sans pointeur propre. Le lecteur `0x1e992b3` vise la seconde clé. | Traduction uniquement à `0x1f82bbc`, également dans PT-81. |

## Suffixe anglais du minage

Le code Thumb prépare STR_VAR_2 avec `n` si le nom d'objet commence par une
voyelle, pour construire « a/an ». Les messages PT gardent exactement les
paramètres FD03 puis FD02, mais l'article anglais n'a pas de sens en portugais.
Le patch PT remplace uniquement deux instructions à `0x1edbf5a` et
`0x1edbf5e` : la branche voyelle écrit désormais deux terminateurs FF au lieu
de `n` puis FF. La branche sans voyelle est inchangée. Les préimages sont
contrôlées et l'opération reste atomique et idempotente.

## Recette locale

```sh
python3 -m pytest tests/unit/pt/test_batch_pt81.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt81_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt81.config.ts
```

Les tests ROM vérifient tous les pointeurs et toutes les valeurs finales,
l'absence de chevauchement, les écritures bornées, l'idempotence, l'atomicité,
les exceptions et les largeurs dans les cinq polices réelles. Les dialogues
restent à deux lignes puis défilement ; missions et inscriptions gardent leur
fenêtre dédiée. Les commandes et sauts de page restent dans l'ordre source.

La preuve Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen`, une copie
ROM et une sauvegarde temporaires. Elle vérifie les octets aux pointeurs vivants,
puis la lecture OCR des deux premières lignes de deux véritables msgbox.
Elle ne prouve pas un parcours complet des zones ni tous les états des menus.
La capture reste dans le dossier temporaire du système, hors dépôt.
