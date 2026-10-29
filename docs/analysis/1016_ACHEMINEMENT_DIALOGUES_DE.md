# B-1016 — Acheminement des dialogues DE

## Résultat du 29 octobre 2026

B-680 est intégré : le texte vivant de `0x1F4C2ED` contient désormais
`FD01, FD02, FD02`. Le patch borné est activé après les relocalisations DE,
avant la restauration des noms d'espèces. Le test synthétique provisoire a
été remplacé par la vraie dernière valeur de combined_de.

Sept textes et huit consommateurs explicites sont vérifiés octet par octet
sur le build final. Aucun scan aveugle ni copie de formulations FR. Le patch
réutilise les copies déjà identiques, valide les préimages EN et refuse
atomiquement les pertes de commandes ou allocations impossibles.

| Source | Consommateurs → cible DE | Octets avec FF | Largeur max | FB |
|---|---|---:|---:|---:|
| 0x7a9a75 | 0x74b0aa → 0x198107 | 1034 | 192 px | 14 |
| 0x1eee8be | 0x1e5b206 → 0x198511 | 902 | 188 px | 14 |
| 0x1f0f004 | 0x1e70293 → 0x19c1d4 | 1280 | 192 px | 13 |
| 0x1f8e271 | 0x1e9fa40 → 0x19c6d4 | 836 | 192 px | 12 |
| 0x1f4c2ed | 0x1e6d700 → 0x19ca18 | 951 | 192 px | 17 |
| 0x1fb052c | 0x1eaf7f5 → 0x1fb052c | 519 | 190 px | 7 |
| 0x1fb07fe | 0x1285745 → 0x1fe7638 ; 0x1eaf820 → 0x1fe7638 | 360 | 188 px | 2 |

Les séquences FC/FD sont identiques à EN, dans leur ordre exact. Les pages FB
sont celles de combined_de ; FE/FA sont recalculés par le rewrap partagé,
avec une première ligne puis défilement, sans dépassement de 192 pixels.
La TV `0x1FB052C` conserve les sept FB de la valeur DE existante contre dix
pour EN : sa correction textuelle appartient à B-682, toujours actif lors de
cette vérification. Le correctif technique ne modifie aucune traduction.
Le tri Cube reste couvert par le générique et menu_sprites selon B-688 :
aucun nouveau patch ajouté. Les déclarations meteorite/Cube TV de parity.yaml
sont mises à jour seulement après preuve des consommateurs.

Cube V3 : `0x1E67DB8 → 0xb4eb26`, exclu de TARGETS et inchangé
par la passe. Réapplication de la passe sur la ROM finale : aucun octet modifié.
SHA-256 DE : `218db617486adcc6a7e432d3c96f22d5dc8c76931369184a093ece5e2ee5fca0`.

## Validation

- `make build-de` réussi via les hooks actifs ; builds FR/IT également imposés
  par le hook, uniquement dans le worktree. Aucune ressource ni référence de
  hash FR/IT modifiée dans les commits.
- `python3 -m pytest tests/unit/de/test_dialogue_routing.py -q` : 21 tests,
  dont sept contrôles sur le build réel et chacun des huit consommateurs.
- Hook Python rapide : 3901 réussis, une exclusion existante ; Vitest : 68 réussis.
- `make test-python` : 4042 réussis, 3 ignorés par les conditions existantes,
  2285 désélectionnés.
- `npx playwright test --config tests/e2e-playwright/playwright.dialogue-routing-de.config.ts` :
  huit rendus natifs mGBA, assertions OCR sur les textes DE, capture jointe au ticket.
- `python3 scripts/check_de_parity.py` : matrice complète et cohérente.

## Non vérifié

Pas de parcours naturel des sept scènes ni de visionnage de toutes les pages.
La sonde utilise une copie ROM temporaire et l'imprimante native avec les
pointeurs réels ; les buffers secondaires sont vides pour isoler le texte.
Les contrôles binaires portent sur les chaînes complètes. La qualité linguistique
et les frontières de pages Cube TV restent du ressort de B-682 ; aucun résultat
linguistique global n'est revendiqué ici. Aucun push ni pipeline distant.
