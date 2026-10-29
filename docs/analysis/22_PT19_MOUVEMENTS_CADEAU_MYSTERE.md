# PT-19 — Descriptions de mouvements et Cadeau Mystère

Le lot F-778 contient exactement les 282 offsets du manifeste PT-19, et non
une plage contiguë de textes. F-758 et F-759 sont intégrés avant cette traduction.

## Bilan par offset

`languages/pt/data/pt19_audit.json` est le bilan exhaustif dans l'ordre du manifeste.
Chaque entrée contient la préimage binaire, les références 32 bits trouvées sur
l'ensemble de la ROM (sans imposer d'alignement), la comparaison anglaise historique
et française, puis la traduction, les budgets et le statut ou la justification.
La ROM anglaise propre, identifiée par SHA-256, prime sur l'extraction historique :
celle-ci contient des valeurs vides et même françaises dans les descriptions.
Aucune traduction française n'est reprise comme source anglaise.

- 255 descriptions de mouvements : quatre lignes conservées, 122 pixels par ligne.
  251 sont référencées dans la table active de descriptions `0x99F190` ; les quatre
  variantes historiques (`0x4852b8`, `0x48581e`, `0x486532`, `0x4881e1`) gardent leurs
  références dans les tables héritées. Elles sont traduites sans changer les cellules
  actives qui emploient d'autres descriptions hors lot.
- 18 messages Cadeau Mystère : pages, nombre de lignes par page et arguments FD
  conservés. Noms HOENN, SEVII ISLANDS, VERMILION CITY et noms de mouvements anglais
  conservés ; PS, Habilidade, Treinador et Bolsa suivent F-759.
- 9 exceptions : `0x4abe2f`, `0x53d24f`, `0x59d2cc`, `0x5a19af`, `0x69e06a`,
  `0x6b47f1`, `0x6c09cf`, `0x6c0a84`, `0x6c0b90`. Leurs octets produisent de courts
  fragments incohérents ou des suites de remplissage ; aucun pointeur 32 bits vers
  ces adresses n'existe dans la ROM. Les préimages et octets voisins sont consignés
  dans le bilan. Aucun consommateur texte démontré : ne pas remplacer ces données
  binaires par une traduction inventée. Aucune entrée combined n'est ajoutée pour elles.

## Injection et contrôles

`batch_19` utilise `StructuredTextPatch` après inline, réparations LZ77 et repointage.
Il vérifie les préimages, les cellules de la table des mouvements et tous les
pointeurs recensés avant écriture. Il alloue des chaînes terminées en espace libre,
puis repointe les cellules fixes ; il n'agrandit aucune cellule en place. Le contrôle
final compare chaque consommateur aux octets exacts et refuse tout chevauchement.
Une seconde application ne modifie aucun octet.

Les tests unitaires fixent le périmètre, les protections exactes, les commandes,
les ruptures et les budgets. Les tests ROM vérifient les préimages et références,
l'atomicité, l'idempotence, l'isolation des écritures et les octets réellement livrés.
Les largeurs sont aussi mesurées avec les cinq tables réelles de police et des
tampons de dix W pour les arguments FD des messages.

```sh
make build-pt
python3 -m pytest -q tests/unit/pt/test_batch_pt19.py tests/unit/test_translation_integrity.py
python3 -m pytest -q tests/e2e/pt/test_batch_pt19_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt19.config.ts
```

La preuve Playwright démarre mGBA hors écran, vérifie deux messages depuis leurs
pointeurs livrés et contrôle leur texte par OCR. Une autre sonde ouvre la vraie
Boîte CT avec une fiche d'objet temporairement sélectionnée : elle contrôle la
quatrième ligne, les bords du cadre et la navigation aller-retour. Les chaînes et
polices proviennent de la ROM construite. Les captures restent dans le répertoire
temporaire du système ; les copies de sauvegarde de test restent inchangées.

## Non vérifié

Les messages Cadeau Mystère sont déclenchés par une sonde msgbox ; cette preuve ne
certifie pas le protocole réseau hérité, un échange physique ou l'obtention réelle
des récompenses. Aucun parcours manuel exhaustif des 273 chaînes n'est revendiqué.
Les quatre variantes historiques sans cellule dans la table active sont contrôlées
au niveau binaire de leurs références héritées, sans prétendre les avoir rencontrées
dans un parcours de jeu actuel. Aucun code partagé ni contenu hors lot n'est modifié.
