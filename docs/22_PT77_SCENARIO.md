# PT-77 — Routes, Ruins of Void, Safari Zone et Seaport City

Ticket F-836. Les 300 offsets explicites de `languages/pt/translation_batches.json`
sont l'unique périmètre. F-758 et F-759 sont intégrés. Noms propres, espèces,
capacités et objets sans équivalent attesté suivent le glossaire F-759.

277 traductions PT-BR et 21 noms/cris anglais conservés sont ajoutés, sans supprimer
ni réécrire les traductions préexistantes. Chaque ligne possède sa valeur exacte
protégée. Le bilan **offset par offset** est
`languages/pt/data/pt77_audit.json` : source ROM complète, comparaison française,
texte portugais, statut, justification, pointeurs, commandes, octets et largeurs.
Les pages FA/FB et l'ordre de tous les paramètres restent identiques à la ROM.
Les retours FE sont ajustés dans les limites de chaque fenêtre.

## Consommateurs et exceptions

`batch_77` finalise les 298 entrées aux pointeurs audités, après inline, réparations,
repointages et police. Le finaliseur partagé existant effectue une transaction
atomique et idempotente, alloue sans écraser les voisins et vérifie tous les octets
aux cibles finales. Les tables rencontrées sont des tables de **pointeurs** : aucune
cellule fixe de texte à écraser. Aucun code partagé ni autre lot n'est modifié.

- `0x1f65e5b` : clé dans le bourrage 00 précédant Route 8, sans pointeur.
  Le vrai début `0x1f65e5c`, dans ce même lot, est conservé et livré aux cinq sites
  `0x1e61400`, `0x1e93aac`, `0x1eafa64`, `0x1eafa74`, `0x1fb3fe4`.
- `0x1f6a89d` : ancienne réplique Hip Waders sans pointeur direct ni intérieur.
  Le chemin de réussite emploie directement `0x1f6a969` via `0x1e8e29e`.
  Les erreurs passent par `0x1f6a844`, `0x1f6a8ba`, `0x1f6a913`.
  Aucune traduction fictivement déclarée injectée pour cette entrée morte.
- `0x1f674a5` : le site `0x61da65` est une coïncidence binaire dans un WaveData
  delta-PCM compressé à `0x61d868`, pas un consommateur texte. Les deux ToneData
  sont référencés dans l'audit. Le payload `[0x61d878,0x61e2cf)` est conservé
  intégralement, hash vérifié. Seul le vrai pointeur de script `0x1e8962a` est
  traduit. La fin audio se calcule sur les blocs compressés, pas sur le nombre
  d'échantillons décodés.
- `0x1f6a078` : discours de 518 octets source, tronqué dans combined EN ; sa fin
  est récupérée dans la ROM et traduite intégralement jusqu'à Sharpedo.

## Budgets et comportement

Les dialogues conservent au plus deux lignes avant la première attente, puis une
ligne par FA. Les descriptions et la tablette conservent leur format distinct.
Les cinq tables natives sont mesurées avec les tampons développés : noms de joueur,
espèces, boîtes, nombres, objets et types. `max_width` couvre aussi l'estimation
conservatrice du validateur partagé ; `native_max_width` donne le vrai budget HUD.
Les octets alloués incluent le terminateur FF.

Le HUD Safari aux offsets `0x1f6822d` et `0x1f6834c` est une exception au dialogue :
fenêtre 1 de 240 × 16 pixels, police Small (0), x=3, y=0, **une seule ligne de
237 pixels**. Les libellés compacts mesurent 214 pixels (30/99 Balls) et 218 pixels
(Wepear Berry ; 216 avec Babiri Berry). Template à `0x1fb4ef8`, rendu à `0x1ec3f94` ;
préimages binaires et preuves dans `safari_hud` de l'audit. Aucun retour ajouté.

Les tests métier vérifient notamment Batalha Dupla, les Habilidades d'éclosion,
Link Stone, les règles Safari (trois Baies et rencontre chromatique sur 30), les
mesures de Pokémon et le discours intégral Sharpedo. Enter est traduit Entrar,
conformément à l'anglais, et non au français divergent « Débutant ».

## Recette locale

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt77.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt77_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt77.config.ts
```

La preuve Playwright utilise mGBA hors écran, une copie temporaire de la ROM finale
et de la sauvegarde, les vrais pointeurs après build et la msgbox native. Elle
contrôle par OCR les premières pages Batalha Dupla, Safari et Sharpedo, puis prend
une capture dans le répertoire temporaire système. Elle ne remplace ni une
traversée complète des zones ni une certification du mini-jeu Safari interactif.
