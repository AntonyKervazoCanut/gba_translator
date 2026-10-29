# B-1016 — Acheminement borné des dialogues DE

## Préparation du 29 octobre 2026 (non activée)

Le build DE local reproduit les cinq dialogues longs EN et les consommateurs
Cube TV résiduels. Le réinséreur générique ne suffit pas. Le module
`languages/de/patches/dialogue_routing.py` prépare une passe à huit sites explicites,
sans scan global de pointeurs, avec validation des préimages EN, encodage partagé,
umlauts DE, allocation existante, réutilisation d'une copie identique et application
atomique. Aucune formulation FR n'est utilisée.

Les pages FB restent des frontières dures ; les retours FE/FA sont recalculés
avec le rewrap existant (192 px maximum, une première ligne puis défilements).
Les séquences FC/FD et autres commandes doivent rester identiques à EN, dans
leur ordre exact. Les corps DE proviennent toujours de la dernière valeur combined.

## Prérequis B-680 identifié par les octets

À `0x1F4C2ED`, EN exige `FD 01, FD 02, FD 02`. La valeur DE actuelle ne contient
que `FD 01` ; les deux buffers suivants ont été remplacés par des formulations
statiques. Le garde rejette cette entrée avant toute écriture. Sa correction
textuelle appartient explicitement à B-680, encore à faire. Aucun texte ni
`protected_entries.yaml` n'est modifié ici. Ne pas activer la passe dans
`lang.yaml` avant intégration de ce prérequis.

Les tests d'acheminement utilisent des extraits binaires EN réels pour les sept
chaînes et les huit sites, avec un court texte de test explicitement synthétique
pour ce seul offset tant que B-680 manque. Cela prouve le mécanisme, **pas** la
validité du texte DE vivant à cet offset. Un test distinct impose le rejet atomique
des commandes manquantes.

## Mesure du build de référence

`make build-de` réussi, avant activation du nouveau module.
SHA-256 : `81e136fd620677b1b58c9b827f547c23db87cef44f7960a5c0cd71d945b1d5bc`.
Les adresses relocalisées dépendent des autres textes du build ; elles ne sont
pas codées en dur dans le correctif.

| Source EN | Octets EN hors FF | Sites → cibles actuelles | Encodage préparé (FF inclus) | Largeur max |
|---|---:|---|---:|---:|
| 0x7A9A75 | 1046 | 0x74B0AA → 0x7A9A75 | 1034 | 192 px |
| 0x1EEE8BE | 1037 | 0x1E5B206 → 0x1EEE8BE | 902 | 188 px |
| 0x1F0F004 | 1441 | 0x1E70293 → 0x1F0F004 | 1280 | 192 px |
| 0x1F8E271 | 1044 | 0x1E9FA40 → 0x1F8E271 | 1019 | 192 px |
| 0x1F4C2ED | 1060 | 0x1E6D700 → 0x1F4C2ED | refusé : B-680 | — |
| 0x1FB052C | 721 | 0x1EAF7F5 → 0x1FB052C | 519 | 190 px |
| 0x1FB07FE | 285 | 0x1285745 → 0x1FB07FE ; 0x1EAF820 → 0xB3E4FB | 360 | 188 px |

Cube V3 : `0x1E67DB8 → 0x18A750`, non modifié par ce module.

Commandes attendues, dans l'ordre :

- 0x7A9A75 et 0x1EEE8BE : `FC 01 06 ; FC 01 08`.
- 0x1F0F004 : aucune commande positionnelle.
- 0x1F8E271 : `FC 01 06 ; FC 01 08 ; FC 01 06 ; FC 01 08`.
- 0x1F4C2ED : `FD 01 ; FD 02 ; FD 02`.
- 0x1FB052C : `FD 02 ; FC 01 06 ; FD 03 ; FC 01 08`.
- 0x1FB07FE : `FC 01 06 ; FD 02 ; FC 01 08`.

## Vérifications de la préparation

- `make test-python` : 2 559 réussis, 97 ignorés existants, 1 132 désélectionnés.
- Tests ciblés : 13 réussis (sept offsets, huit consommateurs, idempotence,
  réutilisation Cube, préimage invalide, perte de commandes, allocation refusée, umlauts).
- Ruff ciblé et `scripts/check_de_parity.py` : réussis.
- Aucune ressource, traduction, déclaration de couverture ni référence de hash FR/IT modifiée.

## Reprise après B-680

1. Relire la dernière valeur DE et vérifier les trois buffers de 0x1F4C2ED.
2. Activer `dialogue_routing` après les autres passes de relocalisation DE.
3. Exécuter `make build-de`, vérifier chaque cible et tous ses octets, puis
   `make test-python` et les tests ciblés.
4. Exécuter Playwright headless avec assertions sur le rendu mGBA et joindre
   une capture depuis le répertoire temporaire du système.
5. Mettre à jour les déclarations de couverture de `parity.yaml` seulement
   après cette preuve. Les exclusions existantes restent inchangées pour le moment ;
   seul l'inventaire du nouveau test est ajouté.

## Non vérifié à ce stade

Acheminement final en ROM, capture Playwright finale et couverture complète :
bloqués par les deux buffers manquants de B-680. Aucun parcours naturel des scènes
n'est revendiqué. Les corrections linguistiques B-681/B-682 restent hors périmètre.
