# 1013 — Injection structurée de combat_ui-03

Suivi fermé des 67 exclusions de B-669. La fixture du parent reste le diagnostic historique ; ses 204 corrections et les autres lots ne sont pas réaudités.

## Traitement

- 44 descriptions absentes de l’extraction EN et 5 présentes mais vides : lecture de la table vivante des attaques, avec contrôle des références supplémentaires (CT/CS).
- 18 boîtes UI : normalisation avec structure explicite, conservation exacte de FE/FB et des commandes dans leur ordre. Les autres traductions conservent le rewrap historique.
- Les textes restent uniquement dans `combined_de.txt` ; le manifeste de production fixe les préimages EN, les références, les identifiants d’attaque et les budgets. Les protections d’absence sont remplacées par les valeurs exactes.
- Le patch final lit les cibles actuelles, relocalise sans écraser leurs cellules partagées et vérifie chaque pointeur avant sauvegarde. Une préimage différente, un dépassement, un chevauchement ou un manque de place bloque la sauvegarde entière. Il s’exécute après les réparations et avant le contrôle des collisions.
- Aucun contenu ou hash de référence FR/IT modifié. Le comportement nouveau de normalisation exige des métadonnées explicites, absentes des builds FR/IT.

## Validation reproductible

`make build-de`, `make test-python`, puis `python3 -m pytest tests/unit/de/test_structured_combat_ui_03.py tests/unit/de/test_combat_ui_03.py -q` (inclut les gardes ROM). Les hooks exécutent également les builds FR/IT et Vitest. Tests négatifs : commandes modifiées, budget dépassé, préimage changée et épuisement de l’espace libre ; test d’idempotence du patch.

`npx playwright test -c tests/e2e-playwright/playwright.structured-combat-ui-03.config.ts` : navigateur headless et mGBA hors écran, assertions OCR sur quatre descriptions dans la fenêtre réelle des attaques et sur une boîte d’échange présentée par son pointeur vivant. Copies ROM/sauvegarde temporaires, aucune sauvegarde en jeu. Captures dans le répertoire temporaire du système, attachées au ticket après réussite.

Non vérifié par ce protocole : parcours naturel de chaque scène UI et de chaque CT/CS. La sonde du dialogue d’échange exerce la boîte standard du moteur ; les quatre descriptions utilisent la navigation du résumé avec une équipe temporaire en RAM. Les 67 entrées sont contrôlées par leurs octets et pointeurs.

## Décision par offset

| Offset | Diagnostic B-669 | Traitement B-1013 | Références | Budget |
|---|---|---|---|---|
| `0x41E16B` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E199` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E1C5` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E414` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E4C0` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E63F` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E6A1` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E6DC` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E717` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E7F2` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E946` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E968` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E98F` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41E9D3` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 2 | 2 lignes par page / 192 px |
| `0x41EA0D` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41EA3F` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41EA86` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0x41EAB7` | Rewrap de boîte | Traduction proposée réintroduite et protégée | 1 | 2 lignes par page / 192 px |
| `0xA37D98` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA37E33` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA37EC4` | Extraction EN absente | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA37F07` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA37F4D` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA37FD7` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA380AB` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA385BB` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38706` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA387D7` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38978` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38BEC` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38D6A` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38E32` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38EB1` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38F75` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA38FB8` | Extraction EN absente | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA38FF2` | Extraction EN vide | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA39075` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39106` | Extraction EN vide | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA39232` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3927C` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39693` | Extraction EN vide | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA396D3` | Extraction EN vide | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA397A7` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39940` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39A1B` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39A60` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39B3C` | Extraction EN absente | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA39B78` | Extraction EN absente | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA39CCD` | Extraction EN vide | Traduction proposée réintroduite et protégée | 2 | 5 lignes / 122 px |
| `0xA39D55` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39DD9` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39E24` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39E67` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39EAA` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39EF6` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA39F84` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A127` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A16F` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A1FE` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A243` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A3B3` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A3F4` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A430` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A903` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3A9EE` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3B306` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
| `0xA3C26B` | Extraction EN absente | Traduction proposée réintroduite et protégée | 1 | 5 lignes / 122 px |
