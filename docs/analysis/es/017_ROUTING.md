# ES-017 — contrats mécaniques F-1046

Aucune traduction de production. Les quatre rapports historiques de préparation
restent inchangés : leur résultat négatif décrit le pipeline avant ce contrat.

## Sélection et acheminement

Les 25 préfixes AA de `017_ROUTES.json` sont déclarés dans `TextAliases`.
Les 19 débuts hors liste gardent la clé contractuelle dans le combined ; la vraie
conversion CSV→JSON produit `contract_offset`, l'adresse vivante à +1, les
préimages EN/ES, les pointeurs explicites et le budget. Le réinserteur existant
est seul responsable des allocations. Aucun plafond global n'est modifié.

Les six paires déjà contractuelles utilisent **uniquement leur clé à +1** :
7A3FD4, 7A4073, 7A7309, 7A7E6B, 7AAB5F et 7B4788. Le préfixe est une donnée,
pas une traduction à ajouter. `check_keys` reste inchangé et rejette les deux
clés présentes ensemble, même avec des valeurs identiques. Les deux possibilités
restent validées individuellement par ce garde, mais la stratégie du parent est
la clé vivante pour ces six paires.

## Consommateurs et budgets

Les contextes de script sont gelés avant et après injection :

- `0F 00 <ptr>` : loadpointer bank0, suivi du callstd de message, deux lignes
  visibles, FA défile et FB change de page, 208 pixels par ligne, police normale.
- `792D32` : réponses de défaite des trainerbattle types 0D et 05 à 79233C et
  792417 ; `7B2B59`, `7B2CF5`, `7B3569` : champ de défaite des types 00.
- `793F7D` : trainerbattle type 03 à 7941B0, pointeur unique à +6 (et non +10).
  Ces textes de combat gardent la fenêtre paginée de deux lignes/208 pixels.
- `7B3BEA` : description de Cherish Ball, **ID moteur 53**, dans gItems
  `876200 + 53*44 + 14h = 876B30`. L'indice 62 de la base de compatibilité
  876074 n'est pas l'ID moteur. L'accesseur 9A96C et les racines de cette table
  sont protégés par les routes objets existantes. Fenêtre Cube : trois lignes,
  176 pixels ; aucune pagination FA/FB. La source EN mesure 171/181/139 pixels :
  elle dépasse déjà la deuxième ligne. La sonde utilise donc TEST sur trois
  lignes, sans changer le plafond ni certifier la formulation finale.

Les 512 métriques de police sont celles du contrat moteur existant. Les buffers
conservent ordre et arguments ; FC/FD/F8/F9/F7 sont traités comme commandes,
FA/FB séparément. Les préimages de ces routes ne nécessitent aucun nouveau code
moteur. Tous les matches ES sont explicites dans la map : les octets et les
pointeurs ES sont vérifiés par `prepare_csv`, pas déduits d'adresses EN égales.

## Préservation

La relocalisation est obligatoire pour les 25 sélections, même pour une sentinelle
plus courte. `TextSourcePreservation` garde chaque préimage complète, y compris
AA, et chaque occurrence intérieure non sélectionnée. Seuls les sites qualifiés
ci-dessus sont repointés. Les occurrences supplémentaires restent marquées
`unproven_binary` ; elles ne deviennent pas des consommateurs textuels certifiés.
Les tests ES-015 gardent leur ensemble exact de 67 préimages ; leur sélection
est explicitement limitée à leur propre rapport lors de l'extension du catalogue.
Les fixtures ES-017 sont des tranches réelles EN/ES, indépendantes des contrats.

Les 98 préimages du relevé complet, les fragments, les zones, les textes de
1047/648 octets et le préfixe de vingt espaces à 7A9E8F restent à F-867.
Aucun combined, protected_entries, glossaire, inventaire ou lots.json ne change.

## Vérifications

- `tests/unit/test_es017_routing.py` : 25 préimages, six collisions, refus
  atomiques de relocalisation, budgets, exhaustivité des occurrences conservées.
- `tests/e2e/es/test_es017_routing.py` : vraie conversion des 19 clés et six
  débuts canoniques, builder, patches finaux, octets à chacun des 27 sites,
  différence bornée contre une ROM témoin ayant reçu les mêmes patches,
  empreintes des sources immuables.
- `tests/e2e-playwright/specs/es017-routing.spec.ts` : mGBA explicitement
  offscreen, lectures natives de tous les sites, expansion et mesure natives
  de toutes les lignes, rendu des sept premières lignes de chaque sentinelle.
  Chromium headless assemble la capture après assertions. Ce n'est pas un
  parcours de jeu ni une certification linguistique. Aucune sauvegarde en jeu.

Les résultats positifs et empreintes sont consignés dans
`017_ACHEMINEMENT_VALIDATION.json`, distinct du rapport historique négatif.
