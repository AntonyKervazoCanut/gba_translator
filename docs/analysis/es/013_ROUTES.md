# ES-013 — Contrats techniques et qualification (F-1044)

Périmètre : les **374 clés exactes** de `013_PREPARATION.json` et `lots.json`.
Aucun combined, protected_entries, glossaire, inventaire ni lots.json modifié.
Les sentinelles sont exclusivement temporaires ; les traductions finales restent
à F-863. `TextAliases` et `SystemTextRoutes` restent les seuls mécanismes
existants de routage ; aucun réinserteur ou patch de traduction ajouté.

| Décision technique | Clés |
|---|---:|
| Alias contractuels à préfixe nul | 20 |
| Messages système qualifiés | 124 |
| Natures, deux tables par ID | 25 |
| Descriptions de mouvements, préimages propres | 6 |
| Décorations en attente de preuve de fenêtre, et fragment 4556F6 | 55 |
| Autres exclusions techniques ou conservatoires | 144 |
| Total | 374 |

Les vingt alias conservent la clé contractuelle ; les débuts vivants ne deviennent
ni des clés de lot ni une seconde route. Les préimages EN/ES, correspondances
uniques, préfixes et références sont contrôlés par le résolveur existant.
Les 82 doublons de remplissage sont refusés à l'import, leur autre clé vivante
restant seule propriétaire. La table `458314` conserve son premier pointeur
vers `458260` hors sélection ; son deuxième champ peut suivre `4582C0`.
La coïncidence graphique `1DCCF22` n'est pas repointée.

Détails de consommateurs, racines, préimages et limites :

- [013_SYSTEM.md](013_SYSTEM.md), données et fixtures correspondantes : messages,
  en-tête FC13, offre F7, aide F8, attentes FC0814 et exclusions.
- [013_SURFACES.md](013_SURFACES.md) : deux tables de natures et structures de
  décorations ; les 54 fenêtres ne sont **pas certifiées**.
- [013_MOVES.md](013_MOVES.md) : six descriptions reconstruites depuis EN propre,
  réutilisant F-1042, cinq lignes et 122 px. Les six anciennes gardes de cellules
  hors sélection ES-014 sont remplacées par ces six propriétaires explicites.

Les exclusions conservatoires ne sont ni des traductions ni des preuves que
les chaînes seraient intrinsèquement non textuelles. En particulier, les
54 descriptions de décorations restent bloquées jusqu'à preuve moteur de
leur fenêtre ; 110/112 px des audits précédents ne sont pas une telle preuve.
Six textes de tables sans racine qualifiée restent également sans injection.

## Validation reproductible

`tests/unit/test_es013_selection.py` impose une décision exclusive pour chacune
des 374 clés. Les tests `test_es013_aliases/moves/surfaces/system.py` couvrent
préimages, consommateurs, racines, commandes et arguments, collisions, voisins,
budgets et refus. Les tests du mécanisme FC13/F7 couvrent les opt-in paginés.

`tests/e2e-playwright/fixtures/prepare_es013_pipeline.py` utilise le vrai CSV →
JSON → builder → tous les patches. Ses valeurs sont construites dans un combined
privé temporaire. Chaque consommateur final est vérifié ; la ROM entière est
comparée à la source avant patches et à un témoin ayant subi les mêmes patches
après. Seules les allocations de texte et les cellules de pointeurs sélectionnées
peuvent différer. Les caches partagés sont copiés dans le worktree, jamais écrits
à travers un lien symbolique.

`tests/e2e-playwright/es013-routes.config.ts` pilote Chromium headless et mGBA
natif offscreen. Les preuves utilisent des sondes techniques et ne revendiquent
ni navigation exhaustive ni connexion multijoueur. Aucune sauvegarde en jeu.
Les captures sont temporaires hors dépôt et attachées après assertions.

Les résultats de builds, tests, témoin FR et preuves sont consignés dans
`013_VALIDATION.md` à l'issue de l'exécution locale. La qualification manquante
des décorations interdit de présenter ce checkpoint comme une livraison complète.
