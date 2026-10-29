# B-1032 — Acheminement technique ES-002

## Changements

Quatre alias étendent les données de B-1030, sans nouveau résolveur :
`1A5AD5→1A5AD6`, `1B1D7C→1B1D7D`, `1BC310→1BC311`, `1C27E6→1C27E7`.
Les clés contractuelles restent dans le combined ; les préfixes AA ne sont pas
écrits. Aucun autre faux début AA d’ES-002 n’est ajouté.

`system_texts.json` décrit quatre préimages complètes et cinq consommateurs
pour `1A552B`, `1BC4CE`, `1BC7E2`, `1BDBF8`. La dernière contient 742 octets
utiles : aucune dépendance au plafond du CSV. Le script 9B est aussi vérifié.
`SystemTextRoutes` réutilise l’enrichissement JSON, la validation des préimages,
le contrôle exhaustif des pointeurs, l’insertion et la vérification finale de
B-1031. Seules la validation du consommateur et la sélection de layout diffèrent.
Le contrat `preserve_control_flow` déjà intégré par F-853 conserve les commandes
FC/FD/F8/F9/F7, leurs arguments et l’ordre FA/FB. Les traductions invalides sont
refusées ; aucun fallback ni troncature. Les layouts gItems restent inchangés.

Les cinq noms de classes passent par `trainer_class_names_it`, déjà activé par
F-853, avec le combined ES. Aucune seconde passe ni texte de patch n’est ajouté.

La passe inline reçoit désormais le JSON de livraison pour es-maint : les
cellules déjà prises en charge ne sont plus réécrites à leur ancienne adresse
après relocation. Son ancien fallback par templates est désactivé explicitement
pour cette cible afin de ne pas étendre les écritures hors sélection. FR/IT/DE
conservent leurs paramètres et leur comportement par défaut. L’absence de JSON
est une erreur explicite pour ce contrat.

## Vérification reproductible

- `make build-es-maint`, `make test-python` et hooks actifs (FR/IT/DE).
- `python3 -m pytest tests/unit/test_es002_routing.py tests/unit/test_text_aliases.py tests/unit/test_item_description_routes.py`.
- `B1032_PROBE_ROM=/tmp/b1032-probe.gba python3 -m pytest tests/e2e/es/test_es002_routing.py` : vrai CSV, JSON consommé, builder et patches.
- `npx playwright test --config tests/e2e-playwright/es002-routing.config.ts` :
  treize rendus natifs mGBA hors écran, assertions OCR, puis progression effective
  de FA et FB avec assertions sur les pages suivantes ; capture temporaire.

Les valeurs préparées de l’attachment parent sont uniquement des fixtures de
régression et sont écrites dans un combined temporaire. Les six textes
`1A5FDF`, `1A63C4`, `1BC54C`, `1BCA43`, `1C0DB0`, `2374F7` reçoivent des
sentinelles temporaires pour exercer les relocations. Avant les patches, la ROM
entière est comparée aux seules plages autorisées (sources, cibles, pointeurs).
La passe inline isolée doit laisser cette ROM strictement identique. Après tous
les patches, les treize valeurs sont vérifiées à tous leurs consommateurs,
ainsi que les six voisinages, les AA, les deux bases de table et toutes les
cellules non sélectionnées. Les cinq cellules sélectionnées restent à 13 octets.

Le témoin FR aux mêmes sources et paramètres est
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Les résultats finaux et la capture sont joints au ticket.

## Limites

La sonde déclenche l’imprimante native depuis des scripts temporaires ; elle ne
certifie pas les parcours naturels (échange, connexion câble, imprimante).
Les buffers de la sonde sont vides, mais leurs codes et arguments sont vérifiés
octet par octet. Aucune sauvegarde en jeu. La relecture et la certification des
374 traductions finales restent à F-852. Aucun combined, glossaire, lot ou source
EN/ES référence/FR n’est modifié ; aucun push ni pipeline distant.
