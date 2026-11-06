# PT-85 — Battle Frontier

Le manifeste PT-85 fait foi : 300 clés, de `0x1f986c0` à `0x1f9b035`.
F-758 et F-759 sont intégrés. Ce lot contient les dialogues des installations,
le changement de Habilidade, les records, les échanges BP, les tuteurs et leurs
listes de prix. Aucune traduction existante n'est supprimée.

## Bilan par offset

`languages/pt/data/pt85_audit.json` contient les 300 lignes dans l'ordre du
manifeste : anglais, comparaison française, portugais, décision, octets source,
taille encodée, références et préimages des lecteurs. 64 textes sont localisés ;
236 libellés canoniques (objets, Berries, mouvements et machines avec leurs prix)
sont conservés selon la politique des noms non attestés F-759. Il n'y a aucune
exception morte ou corrompue dans ce lot. Le français « manqué » pour `miss`
n'est pas repris : le lecteur de `0x1ea283a` utilise le titre féminin `senhorita`.

Les 63 premières clés sont référencées par les scripts de la Frontier ; les
237 suivantes sont dans des tables de pointeurs alignés `0x1fb2378–0x1fb28ac`.
Les chaînes de ces tables sont relogeables ; ce ne sont pas des cellules de noms
à stride fixe. Le patch PT `batch_85` réutilise `BorriusTextPatch`, après les
réparations et repointages génériques, pour vérifier et finaliser tous les
consommateurs. Les chaînes ignorées par le CSV ne sont donc pas déclarées
validées sur la seule foi du combined. Les références partagées d'une même clé
sont toutes traitées, notamment `sir` et `Cancelar`.

## Budgets et preuves exécutables

- Chaque nouvelle ligne est protégée à valeur exacte dans `protected_entries.yaml`.
- Comparaison des commandes à la ROM source, dans leur ordre, y compris les
  changements de page et le positionnement `FC 13` des prix.
- Le budget de rendu est 192 pixels. Le champ `line_widths` de l'audit utilise
  l'estimation générique de 54 pixels pour chaque tampon ; `max_width` y décrit
  cette estimation, pas une extension de fenêtre. Les tests ROM contrôlent
  séparément la limite réelle de 192 pixels dans les cinq polices vivantes,
  avec six chiffres pour les nombres, 100 pixels pour un nom, neuf caractères
  pour le joueur et un caractère pour le pluriel. Ils vérifient aussi que le nom
  ne dépasse pas la position absolue du prix.
- Test ROM des 300 pointeurs finaux, préimages source, absence de chevauchement,
  idempotence et bornage de toutes les écritures du patch sur la ROM réelle.
- Playwright hors écran : deux vraies boîtes de dialogue mGBA, l'erreur de BP
  insuffisants et la machine gratuite quotidienne. OCR PT-BR et assertions sur
  les lignes rendues, ROM temporaire et sauvegarde inchangée. La capture est
  produite dans le répertoire temporaire du système, jamais dans le dépôt.

Commandes :

```sh
make build-pt
python3 -m pytest tests/unit/pt/test_batch_pt85.py tests/unit/test_translation_integrity.py -q
python3 -m pytest tests/e2e/pt/test_batch_pt85_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt85.config.ts
```

## Non vérifié

La preuve visuelle utilise les consommateurs finaux dans une sonde native de
boîte de dialogue ; elle ne prétend pas couvrir un parcours manuel complet de
toutes les installations ni l'achat effectif de chaque produit. La certification
complète du jeu reste dans T-848. Aucun code partagé, ROM distribuée, push ou
pipeline distant ne fait partie de ce lot.
