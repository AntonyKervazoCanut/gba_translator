# B-690 — Reliquats français de noms propres DE

Le périmètre corrigé par A-661 contient **15 offsets**, malgré le titre historique
« 14 ». La liste exhaustive et les consommateurs EN figurent dans
`690_NOMS_PROPRES_DE.json`. Le relevé historique est celui de la ROM locale,
avant reconstruction ; les tests vérifient ensuite la nouvelle ROM.

## Décisions

| Offset | Décision et preuve |
|---|---|
| 0x1762D7 | Inchangé : aucun pointeur EN entrant. Message hérité de FireRed ; ne pas réécrire une cellule sans consommateur démontré. LAPRAS conservé. |
| 0x17FF49 | Inchangé : aucun pointeur EN entrant ; doublon ancien du message actif 0x1EF97C8, préfixe scanner « 9 » conservé. |
| 0x197873 | Inchangé : aucun pointeur EN entrant ; variante ancienne du panneau de Galavan, préfixe scanner « 9 » conservé. |
| 0x1978AC | Dehara : panneau actif via 0x16D1E2. |
| 0x7CFD04 | Dehara-Spielhalle : appel de Looker actif via 0x7BA9CF. |
| 0x7E7128 | Inchangé : aucun pointeur EN entrant ; doublon ancien du panneau de l’arène. |
| 0x7EAC6A | Arena von Dehara : conseil actif via 0x7EAC00. |
| 0x7EC0EF | Dehara : déclaration sur le Kaufhaus, via 0x78DF41. |
| 0x1EF97C8 | Dehara-Kaufhaus : courses, via 0x1E62CC2. |
| 0x1EFA91B | Strand von Dehara : mission via 0x1E632B4 ; Gufa reste inchangé. |
| 0x1EFDFB1 | Kaufhaus de Dehara : via 0x1E6427D ; accord neutre das/es, sens de Department Store conservé. |
| 0x1F1A819 | Arena von Dehara : conseil via 0x1E75929. |
| 0x1F1EE71 | Dehara : panneau avec Jax et rival, via 0x1E767AA. |
| 0x1F1EEAE | Dehara : panneau avec Jax, rival et joueur, via 0x1E767B4. |
| 0x1F74017 | Kaufhaus von Dehara : conseil sur les vitamines via 0x1E937F6. |

Les onze consommateurs historiques affichaient réellement Daherapolis : aucun
remplacement tardif par patch ne les corrigeait. Les adresses relocalisées du
relevé historique ne sont pas des constantes à reproduire : le test suit les
mêmes cellules de pointeur dans chaque nouvelle ROM et compare les octets
attendus, les commandes, les placeholders dans leur ordre et les largeurs.

## Sources et limites

La source canonique `languages/en/combined_en.txt` nomme Dehara sur ces surfaces.
La politique `languages/de/data/english_toponyms.yaml` utilise également Dehara
(Dehara City, Dehara Game Corner, Dehara Dept.). Les remplacements du présent
lot portent sur le référent Dehara ; les noms allemands Galavan et Gufa restent
intacts. Aucun offset hors liste ni lot B-666 à B-687 n’est modifié.

Pour la société, EN 0x1762D7 dit « SILPH employee » ; EN 0x3D856E explicite
« Silph Co. », et 0x41B21C « SILPH CO. ». Vérification du glossaire officiel DE
`languages/de/data/official_terminology.yaml` : il ne contient aucune entrée de
société Silph (il couvre les nomenclatures Pokémon). Il ne justifie donc pas
SILPHE SARL. La graphie à employer si un consommateur de ce message est réactivé
est **Silph Co.**, conformément au ticket et à EN ; aucune modification de
ressource ou de patch n’est requise pour les onze textes visibles corrigés.
L’absence de pointeur entrant ne prouve pas l’impossibilité de tout accès calculé,
mais aucun consommateur documenté n’autorise à réécrire ces quatre cellules.

## Validation reproductible

- `make build-de` et `make test-python`.
- `python3 -m pytest -q tests/unit/de/test_noms_propres_690.py -m rom` :
  onze cibles vivantes, octets exacts, contrôles et boîtes de 192 pixels.
- `npx playwright test --config tests/e2e-playwright/playwright.noms-propres-690-de.config.ts` :
  imprimante native mGBA hors écran, quatre scènes (panneau, deux Kaufhaus,
  plage), assertions OCR et capture dans le dossier temporaire système.
- Les onze valeurs exactes sont couvertes par `protected_entries.yaml` et
  `tests/unit/test_translation_integrity.py` dans le commit de traduction.

## Non vérifié

Les quatre cellules sans pointeur n’ont pas été déclenchées en jeu ; aucun
parcours manuel complet de l’histoire n’est revendiqué. La sonde visuelle
appelle l’imprimante native avec les cibles vivantes dans une copie temporaire
de la ROM, sans sauvegarde ni modification de la ROM construite.
