# PT-27 — Borrius : bilan des 288 offsets

F-786. Prérequis F-758 (c5b5e0b9) et F-759 (dcc6ce5d) présents dans l’historique. 270 textes traduits et protégés, 18 exceptions motivées. Aucun offset hors manifeste ajouté. Les noms propres, objets et mouvements non attestés restent anglais selon F-759.

## Injection et limites

Le patch `batch_27` réutilise `BorriusTextPatch` et `StructuredTextPatch`. Il vérifie les préimages et les contrôles avant toute mutation, alloue de nouvelles cellules terminées, puis repointe exclusivement les consommateurs listés. Les quatre libellés d’étage ont chacun un consommateur `loadpointer` (0x7d8e18, 0x7d8e26, 0x7d8e34, 0x7d8e42) : T, S1, S2, S3 sont injectés par ce patch dédié, sans modifier une table fixe. Aucun autre consommateur de table fixe n’a été identifié pour ce lot. Les anciennes cellules et leurs voisins ne sont pas réécrits par ce finaliseur. Les contrôles FA/FB, couleurs et tampons conservent leur ordre exact ; les retours FE sont ajustés aux pixels, au plus deux lignes initiales puis une ligne par scroll.

Les textes 0x7dda44 et 0x7ddc4c sont tronqués dans le corpus EN : leur fin complète est relue dans la ROM, stockée dans `source_complete` et traduite. La comparaison FR est conservée par offset dans le JSON d’audit. Ce JSON inclut les octets EN, le hash source, tous les référents avec leur contexte, la longueur encodée et chaque largeur de ligne. Les tampons réservent neuf glyphes larges ; les cinq polices réelles sont contrôlées par le test ROM.

Les exceptions ne sont pas présentées comme injectées. En particulier, 0x7e97f3 a un vrai pointeur vers un préfixe de script corrompu : la traduction du texte sain 0x7e9805 ne corrige pas ce consommateur corrompu. 0x7ea1fb est un suffixe dont la prétendue référence coupe des instructions Thumb. 0x7e7554, véritable début après le faux 0x7e7553, est hors manifeste et reste intact.

## Recette locale

```sh
python3 -m pytest tests/unit/pt/test_batch_pt27.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt27_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt27.config.ts
```

Playwright utilise deux messages complets lus aux pointeurs de la ROM finale (0x7e94cb, 0x7eaae7), affichés par le moteur natif dans une copie temporaire mGBA hors écran. Les assertions OCR portent sur toutes leurs lignes. La sonde ne revendique pas un parcours des 270 dialogues. Les images restent dans le répertoire temporaire de l’OS, hors dépôt.

## Bilan offset par offset

| Offset | État | Référents EN | Justification |
|---|---|---|---|
| 0x7d61ad | traduit / à vérifier en ROM | 0x7d5b0e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d632c | traduit / à vérifier en ROM | 0x7d5b25 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d655a | traduit / à vérifier en ROM | 0x7d651b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d65ac | traduit / à vérifier en ROM | 0x7d6527 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d65be | traduit / à vérifier en ROM | 0x7d6532 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d688a | traduit / à vérifier en ROM | 0x7d665d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d68a1 | traduit / à vérifier en ROM | 0x7d667b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d68d5 | traduit / à vérifier en ROM | 0x7d669b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6905 | traduit / à vérifier en ROM | 0x7d66bb | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6975 | traduit / à vérifier en ROM | 0x7d66cd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d69d7 | traduit / à vérifier en ROM | 0x7d66df | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6a35 | traduit / à vérifier en ROM | 0x7d66f1 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6b1e | traduit / à vérifier en ROM | 0x7d6703 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6b45 | traduit / à vérifier en ROM | 0x7d671c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6b7c | traduit / à vérifier en ROM | 0x7d6746 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6b9e | traduit / à vérifier en ROM | 0x7d6758 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6bd9 | traduit / à vérifier en ROM | 0x7d6786 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6c37 | traduit / à vérifier en ROM | 0x7d6885, 0x9a5348 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6c5a | traduit / à vérifier en ROM | 0x7d67c8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6cd7 | traduit / à vérifier en ROM | 0x7d67fa | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d6d10 | traduit / à vérifier en ROM | 0x7d6812 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7053 | traduit / à vérifier en ROM | 0x7d6df3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7109 | traduit / à vérifier en ROM | 0x7d6e0f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7159 | traduit / à vérifier en ROM | 0x7d6e38 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d716e | traduit / à vérifier en ROM | 0x7d6e54 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d71a9 | traduit / à vérifier en ROM | 0x7d6e6d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d71da | traduit / à vérifier en ROM | 0x7d6e7f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d71f3 | traduit / à vérifier en ROM | 0x7d6ead | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7203 | traduit / à vérifier en ROM | 0x7d6ebf | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d726d | traduit / à vérifier en ROM | 0x7d6ed1 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d72d5 | traduit / à vérifier en ROM | 0x7d6ee3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d742f | traduit / à vérifier en ROM | 0x7d6ef5 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7480 | traduit / à vérifier en ROM | 0x7d6f13 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d752f | traduit / à vérifier en ROM | 0x7d6f25 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d761f | traduit / à vérifier en ROM | 0x7d6f3e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7642 | traduit / à vérifier en ROM | 0x7d6f7b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d768f | traduit / à vérifier en ROM | 0x7d6fb2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d770e | traduit / à vérifier en ROM | 0x7d7015 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7750 | traduit / à vérifier en ROM | 0x7d7027 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d79fb | traduit / à vérifier en ROM | 0x7d795f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7a4f | traduit / à vérifier en ROM | 0x7d798b, 0x7d79d2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7a67 | traduit / à vérifier en ROM | 0x7d79a0 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7aa6 | traduit / à vérifier en ROM | 0x7d79e9 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d7fcc | traduit / à vérifier en ROM | 0x7d7d29 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d808f | exception | aucun (scan ROM complète) | Préfixe de script de 73 octets, aucun pointeur vers 0x7d808f ; texte vivant à 0x7d80d8 (traité). |
| 0x7d80d8 | traduit / à vérifier en ROM | 0x7d8093 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d819f | traduit / à vérifier en ROM | 0x7d80b0 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d821b | traduit / à vérifier en ROM | 0x7d80c5 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8270 | traduit / à vérifier en ROM | 0x7d80aa | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8297 | traduit / à vérifier en ROM | 0x78c450 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d83f8 | traduit / à vérifier en ROM | 0x7d83e7 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d84c3 | traduit / à vérifier en ROM | 0x7d84b2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d85df | traduit / à vérifier en ROM | 0x7d85ce | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d86b9 | traduit / à vérifier en ROM | 0x7d7cda | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8704 | traduit / à vérifier en ROM | 0x7d7bf1, 0x7d7c4b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d879a | traduit / à vérifier en ROM | 0x7d8793 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d882c | traduit / à vérifier en ROM | 0x7d87f3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d88a8 | traduit / à vérifier en ROM | 0x7d880a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d88c0 | traduit / à vérifier en ROM | 0x7d8811 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d891c | traduit / à vérifier en ROM | 0x7d8823 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d896b | traduit / à vérifier en ROM | 0x7d8a29 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8a4e | traduit / à vérifier en ROM | 0x7d8a3d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8acf | traduit / à vérifier en ROM | 0x78c406 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8ae2 | traduit / à vérifier en ROM | 0x78c850 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8b30 | traduit / à vérifier en ROM | 0x7e6d5b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8bbb | traduit / à vérifier en ROM | 0x7d8b1f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8bea | traduit / à vérifier en ROM | 0x7cf2b6 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8f5a | traduit / à vérifier en ROM | 0x7d8e9f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8f73 | traduit / à vérifier en ROM | 0x7d8f2e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8f91 | traduit / à vérifier en ROM | 0x7d8e18 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8f94 | traduit / à vérifier en ROM | 0x7d8e26 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8f98 | traduit / à vérifier en ROM | 0x7d8e34 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8f9c | traduit / à vérifier en ROM | 0x7d8e42 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8fd7 | traduit / à vérifier en ROM | 0x7c771d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d8ffd | traduit / à vérifier en ROM | 0x7c8297 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d904f | traduit / à vérifier en ROM | 0x7e70c2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d98e5 | traduit / à vérifier en ROM | 0x7d90bb | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d990e | traduit / à vérifier en ROM | 0x7d90cd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9974 | traduit / à vérifier en ROM | 0x7d90df | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d99c0 | traduit / à vérifier en ROM | 0x7d90f1 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9a33 | traduit / à vérifier en ROM | 0x7d9103 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9b0d | traduit / à vérifier en ROM | 0x7d9115 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9b56 | traduit / à vérifier en ROM | 0x7d9127 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9b8d | traduit / à vérifier en ROM | 0x7d9139 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9c82 | traduit / à vérifier en ROM | 0x7d9144 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9d41 | traduit / à vérifier en ROM | 0x7d9156 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9de8 | traduit / à vérifier en ROM | 0x7d9168 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9f57 | traduit / à vérifier en ROM | 0x7d917a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7d9fba | traduit / à vérifier en ROM | 0x7d91aa | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da048 | traduit / à vérifier en ROM | 0x7d91bc | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da08d | traduit / à vérifier en ROM | 0x7d91d8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da0ff | traduit / à vérifier en ROM | 0x7d9203 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da220 | traduit / à vérifier en ROM | 0x7d924c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da24a | traduit / à vérifier en ROM | 0x7d9260 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da253 | traduit / à vérifier en ROM | 0x7d926b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da272 | traduit / à vérifier en ROM | 0x7d9292 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da358 | traduit / à vérifier en ROM | 0x7d92ae | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da3ef | traduit / à vérifier en ROM | 0x7d92c3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da4c9 | traduit / à vérifier en ROM | 0x7d92d5 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da57f | traduit / à vérifier en ROM | 0x7d92e7 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da5bf | traduit / à vérifier en ROM | 0x7d92f2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da6d8 | traduit / à vérifier en ROM | 0x7d9304 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da74a | traduit / à vérifier en ROM | 0x7d9338 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da7b8 | traduit / à vérifier en ROM | 0x7d934a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da831 | traduit / à vérifier en ROM | 0x7d935c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da87b | traduit / à vérifier en ROM | 0x7d9371 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da8fb | traduit / à vérifier en ROM | 0x7d938a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7da9a0 | traduit / à vérifier en ROM | 0x7d98d9 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7daaaa | traduit / à vérifier en ROM | 0x7d98e0 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7daba4 | traduit / à vérifier en ROM | 0x7d93bd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dac1e | traduit / à vérifier en ROM | 0x7d9403 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dcd85 | traduit / à vérifier en ROM | 0x7d9418 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dcdf6 | traduit / à vérifier en ROM | 0x7d9423 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dce3b | traduit / à vérifier en ROM | 0x7d9435 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dce96 | traduit / à vérifier en ROM | 0x7d944a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dced2 | traduit / à vérifier en ROM | 0x7d945c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dcf16 | traduit / à vérifier en ROM | 0x7d946e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dcf55 | traduit / à vérifier en ROM | 0x7d9480 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd0c7 | traduit / à vérifier en ROM | 0x7d9492 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd0ed | traduit / à vérifier en ROM | 0x7d94a4 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd149 | traduit / à vérifier en ROM | 0x7d94cd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd2a4 | traduit / à vérifier en ROM | 0x7d94df | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd2ff | traduit / à vérifier en ROM | 0x7d94f1 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd330 | traduit / à vérifier en ROM | 0x7d94fc | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd361 | traduit / à vérifier en ROM | 0x7d950e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd390 | traduit / à vérifier en ROM | 0x7d9520 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd3cb | traduit / à vérifier en ROM | 0x7d953d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd441 | traduit / à vérifier en ROM | 0x7d954f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd480 | traduit / à vérifier en ROM | 0x7d956a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd5c2 | traduit / à vérifier en ROM | 0x7d95b0 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd5e6 | traduit / à vérifier en ROM | 0x7d95cc | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd61c | traduit / à vérifier en ROM | 0x7d95de | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd64a | traduit / à vérifier en ROM | 0x7d95fe | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd676 | traduit / à vérifier en ROM | 0x7d9610 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd690 | traduit / à vérifier en ROM | 0x7d9630 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd6c3 | traduit / à vérifier en ROM | 0x7d963f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd6ef | traduit / à vérifier en ROM | 0x7d9651 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd724 | traduit / à vérifier en ROM | 0x7d9667 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd768 | traduit / à vérifier en ROM | 0x7d9684 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd7a5 | traduit / à vérifier en ROM | 0x7d9696 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd813 | traduit / à vérifier en ROM | 0x7d96b3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd826 | traduit / à vérifier en ROM | 0x7d96cc | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd877 | traduit / à vérifier en ROM | 0x7d96ef | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd8a4 | traduit / à vérifier en ROM | 0x7d96fd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd8cb | traduit / à vérifier en ROM | 0x7d9712 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd974 | traduit / à vérifier en ROM | 0x7d9724 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dd9b0 | traduit / à vérifier en ROM | 0x7d9736 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dda44 | traduit / à vérifier en ROM | 0x7d9754 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ddc4c | traduit / à vérifier en ROM | 0x7d9771 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7dde5d | traduit / à vérifier en ROM | 0x7d97d5 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ddf90 | traduit / à vérifier en ROM | 0x7d980f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de002 | traduit / à vérifier en ROM | 0x7d981a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de06b | traduit / à vérifier en ROM | 0x7d982c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de0ea | traduit / à vérifier en ROM | 0x7d9845 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de155 | traduit / à vérifier en ROM | 0x7d987d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de1e1 | traduit / à vérifier en ROM | 0x7d98c5 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de1e5 | traduit / à vérifier en ROM | 0x7d98d2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de34e | traduit / à vérifier en ROM | 0x7de303 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de459 | traduit / à vérifier en ROM | 0x7de335 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de4da | traduit / à vérifier en ROM | 0x764e56 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de55f | exception | aucun (scan ROM complète) | Octet 9 parasite avant 0x7de560, aucun pointeur vers 0x7de55f ; 0x7de560 traité. |
| 0x7de560 | traduit / à vérifier en ROM | 0x7de7e0 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de5c1 | traduit / à vérifier en ROM | 0x7d903d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de806 | exception | aucun (scan ROM complète) | Script et remplissage avant 0x7de83e ; aucun pointeur vers 0x7de806 ; 0x7de83e traité. |
| 0x7de83e | traduit / à vérifier en ROM | 0x78146a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7de8a7 | traduit / à vérifier en ROM | 0x1a9a97, 0x1a9abe | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e3f05 | traduit / à vérifier en ROM | 0x7de694 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e5bf8 | traduit / à vérifier en ROM | 0x7403f3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e5c7c | traduit / à vérifier en ROM | 0x16b65f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e65e6 | traduit / à vérifier en ROM | 0x74b261 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6741 | traduit / à vérifier en ROM | 0x74b274 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6783 | traduit / à vérifier en ROM | 0x74b287 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6816 | traduit / à vérifier en ROM | 0x79468c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6862 | traduit / à vérifier en ROM | 0x1a9a9b, 0x1a9ac2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6883 | traduit / à vérifier en ROM | 0x1a9ab1, 0x1a9ac8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6b88 | exception | aucun (scan ROM complète) | Octet 9 avant le panneau vivant 0x7e6b89, traité ; aucun pointeur vers 0x7e6b88. |
| 0x7e6b89 | traduit / à vérifier en ROM | 0x78198d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6bbb | exception | aucun (scan ROM complète) | Fragment hannel, aucun pointeur vers 0x7e6bbb ; ne constitue pas un texte autonome. |
| 0x7e6c2e | exception | aucun (scan ROM complète) | Octet 9 avant le message vivant 0x7e6c2f, traité ; aucun pointeur vers 0x7e6c2e. |
| 0x7e6c2f | traduit / à vérifier en ROM | 0x78098b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6c96 | traduit / à vérifier en ROM | 0x78099e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6cc5 | traduit / à vérifier en ROM | 0x7809b0, 0x7f12bc, 0x7f2830, 0x7f2b5a, 0x7f2fa6 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6d12 | traduit / à vérifier en ROM | 0x7807d3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6e28 | traduit / à vérifier en ROM | 0x7ba3bd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6eee | traduit / à vérifier en ROM | 0x7e70da | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6f26 | traduit / à vérifier en ROM | 0x7e70de | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6f49 | traduit / à vérifier en ROM | 0x7e70f6 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6f84 | traduit / à vérifier en ROM | 0x7e70fa | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6f9e | traduit / à vérifier en ROM | 0x7e7112 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e6fd4 | traduit / à vérifier en ROM | 0x7e7116 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e700b | traduit / à vérifier en ROM | 0x78c180 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7128 | exception | aucun (scan ROM complète) | Ancien panneau du Gym de Dehara sans aucun pointeur ROM EN vers 0x7e7128 ; aucune table fixe identifiée comme consommateur. Non revendiqué injecté. |
| 0x7e74e0 | traduit / à vérifier en ROM | 0x7e724d, 0x7e7278 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7553 | exception | aucun (scan ROM complète) | Octet 9 parasite avant le vrai texte 0x7e7554 (hors manifeste PT-27). Aucun pointeur vers 0x7e7553 ; le vrai texte reste hors périmètre. |
| 0x7e75bb | traduit / à vérifier en ROM | 0x7c77f3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7677 | traduit / à vérifier en ROM | 0x7d9067 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7a5c | traduit / à vérifier en ROM | 0x7e7a04 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7b48 | exception | aucun (scan ROM complète) | Copie sans pointeur du refus du maître de mouvements à 0x7e7b48 ; copie vivante 0x7e7c41 traitée. |
| 0x7e7b78 | traduit / à vérifier en ROM | 0x7c3e1e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7c41 | traduit / à vérifier en ROM | 0x7e7c2d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7cc7 | traduit / à vérifier en ROM | 0x7e7c7c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7d68 | traduit / à vérifier en ROM | 0x7e7ca3 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7da6 | traduit / à vérifier en ROM | 0x7e7cb6 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7e64 | traduit / à vérifier en ROM | 0x7e7de4 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7f5d | traduit / à vérifier en ROM | 0x7e7e0b | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e7fe2 | traduit / à vérifier en ROM | 0x7e7e39 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e801a | traduit / à vérifier en ROM | 0x7e7e50 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8066 | traduit / à vérifier en ROM | 0x7e7e1e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e83de | traduit / à vérifier en ROM | 0x7e80b9 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e842c | traduit / à vérifier en ROM | 0x7e8149, 0x7e8193, 0x7e81e2, 0x7e8231, 0x7e8280, 0x7e82cf, 0x7e831e, 0x7e836d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8485 | traduit / à vérifier en ROM | 0x7e8161, 0x7e81ab, 0x7e81fa, 0x7e8249, 0x7e8298, 0x7e82e7, 0x7e8336, 0x7e8385, 0x7eb9c3, 0x7eba12, 0x7eba61, 0x7ebab0, 0x7ebaff, 0x7ebb4e, 0x7ebb9d, 0x7ebbec, 0x7ebc3b, 0x7ebc8a, 0x7ebcd9, 0x7ebd28, 0x7ebd77, 0x7ebdc6, 0x7ebe15, 0x7ebe64 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e84b6 | traduit / à vérifier en ROM | 0x7e83a1 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e84e8 | traduit / à vérifier en ROM | 0x7e83cd | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8526 | traduit / à vérifier en ROM | 0x7e83b7 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e857e | traduit / à vérifier en ROM | 0x7e725a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e85fc | exception | aucun (scan ROM complète) | Script avant le texte vivant 0x7e8627, traité ; aucun pointeur vers 0x7e85fc. |
| 0x7e8627 | traduit / à vérifier en ROM | 0x7e8617 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e86d9 | traduit / à vérifier en ROM | 0x7e8620 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8786 | traduit / à vérifier en ROM | 0x78c1c0 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e880a | traduit / à vérifier en ROM | 0x78c200 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8841 | traduit / à vérifier en ROM | 0x7a6ba2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8885 | traduit / à vérifier en ROM | 0x7a6ba6 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e888d | traduit / à vérifier en ROM | 0x7a6bac | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e88d7 | traduit / à vérifier en ROM | 0x7e8a90 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e89c1 | traduit / à vérifier en ROM | 0x78c22a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8aa2 | traduit / à vérifier en ROM | 0x78c446 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8b55 | traduit / à vérifier en ROM | 0x78c486 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8c86 | traduit / à vérifier en ROM | 0x78c506 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8cc1 | traduit / à vérifier en ROM | 0x78c546 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8cf8 | traduit / à vérifier en ROM | 0x78c586 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8d4b | traduit / à vérifier en ROM | 0x7e8d0f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8ef5 | traduit / à vérifier en ROM | 0x7e8d27 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e8fa1 | traduit / à vérifier en ROM | 0x7e8d3a | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9072 | traduit / à vérifier en ROM | 0x7e8fcf | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e90ab | traduit / à vérifier en ROM | 0x7e8ff9 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9160 | traduit / à vérifier en ROM | 0x7e9060 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e91e6 | traduit / à vérifier en ROM | 0x7e900c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9283 | traduit / à vérifier en ROM | 0x7e9019 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e928f | traduit / à vérifier en ROM | 0x7e901f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e934e | traduit / à vérifier en ROM | 0x771b3f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9423 | traduit / à vérifier en ROM | 0x771b8e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e94cb | traduit / à vérifier en ROM | 0x780940 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e94ea | traduit / à vérifier en ROM | 0x7c06ae | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9529 | exception | aucun (scan ROM complète) | Ancienne copie non référencée du défi du chef ; copie vivante 0x7e9872 traitée. |
| 0x7e95b2 | exception | aucun (scan ROM complète) | Ancienne copie non référencée du rire ; copie vivante 0x7e98fb traitée. |
| 0x7e95c0 | exception | aucun (scan ROM complète) | Ancienne copie non référencée du changement de nom ; copie vivante 0x7e9909 traitée. |
| 0x7e96b2 | exception | aucun (scan ROM complète) | Ancienne copie non référencée du dialogue du frère ; copie vivante 0x7e99fb traitée. |
| 0x7e9734 | traduit / à vérifier en ROM | 0x7946df | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e97f3 | exception | 0x7e97b6 | Pointeur msgbox 0x7e97b6 vers une extraction corrompue : 18 octets de script avant le texte 0x7e9805. Préfixe 75 08 4f 07 00 4e 17 7c 08 51 00 00 17 06 50 02 00 02. Impossible de conserver ces octets comme texte sain. Consommateurs directs du message sain 0x7e9805 traités ; ce pointeur corrompu est laissé intact et non revendiqué traduit. |
| 0x7e9805 | traduit / à vérifier en ROM | 0x771af9, 0x7b89bc, 0x7e97e7 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9872 | traduit / à vérifier en ROM | 0x771b52 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e98fb | traduit / à vérifier en ROM | 0x771b5f | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9909 | traduit / à vérifier en ROM | 0x771b65 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e99fb | traduit / à vérifier en ROM | 0x771b71 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9a7c | exception | aucun (scan ROM complète) | Suffixe th you. sans aucun pointeur vers 0x7e9a7c ; fragment non autonome. |
| 0x7e9bc7 | traduit / à vérifier en ROM | 0x7e9a89 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9c25 | traduit / à vérifier en ROM | 0x7e9a9c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9ca1 | traduit / à vérifier en ROM | 0x7e9aaf | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9d4b | traduit / à vérifier en ROM | 0x7e9ac2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9d68 | traduit / à vérifier en ROM | 0x753a1d, 0x7a6bd8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9ec0 | traduit / à vérifier en ROM | 0x7e9ae5 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9efa | traduit / à vérifier en ROM | 0x7e9afb | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9f91 | traduit / à vérifier en ROM | 0x7e9b15 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7e9fde | traduit / à vérifier en ROM | 0x7e9b30 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea030 | traduit / à vérifier en ROM | 0x7e9b1e | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea067 | traduit / à vérifier en ROM | 0x7e9b4d | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea1eb | traduit / à vérifier en ROM | 0x7e9b56 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea1fb | exception | 0x05d293 | Coïncidence de quatre octets à 0x5d293 dans le code Thumb (contexte 0b f0 e4 fb a1 7e 08 01 40 18 80 00), pas un pointeur de texte : le mot non aligné coupe des instructions. Suffixe intérieur de 0x7ea1eb, dont le véritable consommateur 0x7e9b56 est traité. |
| 0x7ea20e | traduit / à vérifier en ROM | 0x7e9b74, 0x7e9b90 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea26a | traduit / à vérifier en ROM | 0x771ba2, 0x7b65fc | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea6e4 | traduit / à vérifier en ROM | 0x7ea6dc, 0x7ead90 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea704 | traduit / à vérifier en ROM | 0x780944 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea772 | traduit / à vérifier en ROM | 0x78d2f4 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea7a9 | traduit / à vérifier en ROM | 0x78d2f8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea7bd | traduit / à vérifier en ROM | 0x78d2fe | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea84a | traduit / à vérifier en ROM | 0x7d8b07 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea889 | traduit / à vérifier en ROM | 0x7d8b11 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea8e3 | traduit / à vérifier en ROM | 0x7ea8c6 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea8fb | traduit / à vérifier en ROM | 0x7ea8cc | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea953 | exception | aucun (scan ROM complète) | Suffixe gate this Gym. sans aucun pointeur vers 0x7ea953 ; fragment non autonome. |
| 0x7ea9b1 | traduit / à vérifier en ROM | 0x7ea96c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7ea9bc | traduit / à vérifier en ROM | 0x7ea972 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7eaa1b | traduit / à vérifier en ROM | 0x7ea9e8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7eaa26 | traduit / à vérifier en ROM | 0x7ea9ee | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7eaadb | traduit / à vérifier en ROM | 0x7eaaa2 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7eaae7 | traduit / à vérifier en ROM | 0x7eaaa8 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7eab7f | traduit / à vérifier en ROM | 0x7eab36 | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
| 0x7eab8a | traduit / à vérifier en ROM | 0x7eab3c | Traduction EN confrontée au FR ; consommateur texte direct prouvé. Relocalisation bornée dédiée ; couleurs, tampons et pages conservés. |
