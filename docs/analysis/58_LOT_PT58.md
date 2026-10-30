# PT-58 — Catégories Pokédex et Antisis

Périmètre : les 300 clés explicites de `languages/pt/translation_batches.json`,
sans extension à toute la plage d'adresses. F-758 et F-759 sont intégrés.

## Bilan exhaustif

`languages/pt/data/pt58_audit.json` fournit les 300 lignes dans l'ordre du
manifeste : référence anglaise, comparaison française, préimage binaire,
pointeurs directs (scan non aligné de toute la ROM), décision et justification.
Les 239 textes ajoutés ont chacun une protection exacte dans le même commit.
Aucune traduction préexistante n'est supprimée.

- 113 catégories Pokédex : traductions éditoriales compactes, pas de prétention
  à une nomenclature officielle. Cellules de 12 octets, terminateur compris,
  dans les structures de 36 octets de la table `0x1a357cc`.
- 126 textes d'Antisis City, Antisis Port et Antisis Sewers : dialogues de gangs,
  police, livraisons, moteurs de Rotom, expériences et répliques de combats.
  Sept noms propres/cris restent identiques à l'anglais selon F-759.
- 61 exceptions non textuelles : les octets EN/FR ressemblent à des fragments
  binaires, sans phrase ni pointeur absolu vers la clé. Le rapport contient
  chaque préimage, le contexte binaire et le résultat nul du scan. Aucun
  consommateur texte n'est identifié ; aucune traduction n'est inventée.

Les 113 clés de catégorie se trouvent **deux octets avant** le texte réellement
lu. `consumer_offset` documente la vraie cellule ; les dix références à la base
indexée sont vérifiées dans la source et la ROM finale. Le finaliseur restaure
les deux octets de bourrage et remplit exclusivement la cellule de 12 octets,
sans déplacer les données numériques qui suivent. Il ne parcourt pas les
catégories des autres lots.

Le fichier anglais tronque `0x1edda75` à « t ». La préimage ROM complète jusqu'au
terminateur fournit la fin : Big Mo intervient quand la situation dégénère.
La traduction conserve cette fin et toutes les commandes du texte complet.
Les noms de lieux, factions, personnages, mouvements et objets non attestés
restent anglais conformément au glossaire, sans recopier les noms français.

## Validation reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_pt58.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt58_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt58.config.ts
```

Le finaliseur réutilise `BorriusTextPatch` : contrôles/pages exacts, allocation
bornée et repointage des seules références auditées. Les tests vérifient aussi
l'atomicité, l'idempotence et l'ensemble des octets modifiés, les 61 exceptions
intactes, les champs voisins des catégories, et les budgets de toutes les
chaînes dans les cinq polices natives (variables joueur/Pokémon/objet développées).
Aucun code partagé n'est modifié.

La preuve Playwright exécute mGBA hors écran, sur une copie temporaire de la ROM
finale. Un script de sonde affiche une catégorie et deux répliques depuis leurs
cellules/pointeurs livrés, sans remplacer leurs textes ni les glyphes. Les
assertions comparent les octets puis reconnaissent le texte rendu par OCR ; la
sauvegarde est vérifiée inchangée. La capture est produite dans le répertoire
temporaire système, jamais dans le dépôt.

Validation locale effectuée : build PT réussi, cinq tests ROM réussis,
33 tests unitaires/intégrité réussis et un test Playwright réussi (trois cas
rendus avec reconnaissance du texte). Lint Python ciblé et TypeScript passent.

## Non vérifié

La sonde native ne constitue pas un parcours de tous les événements d'Antisis,
ni une navigation dans les 113 écrans du Pokédex. La livraison intégrale et les
budgets sont contrôlés en binaire ; le rendu est échantillonné par Playwright.
Les 61 faux positifs restent des exceptions sans consommateur texte identifié,
pas des entrées déclarées traduites.
