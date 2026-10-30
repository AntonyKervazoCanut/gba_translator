# PT-52 — Pokédex étendu

## Périmètre livré

F-811 couvre les **299 offsets explicites** de PT-52, de `0x1667474` à
`0x166b035`. Le domaine réel est le Pokédex : 125 descriptions de Pokémon
récents et de formes régionales, 19 catégories et 155 noms d'espèces
(Bulbasaur à Cyndaquil). Aucune entrée d'un autre lot n'est modifiée.

Les 125 descriptions et 18 catégories sont traduites en PT-BR. La catégorie
`Cruel` et les 155 noms anglais canoniques sont conservés selon F-759 :
**143 traductions, 156 valeurs conservées, aucune exception morte ou ignorée**.
Chaque valeur figure dans le combined et dans `protected_entries.yaml`.

## Sources et contamination du corpus

F-758 (`c5b5e0b9`) et F-759 (`dcc6ce5d`) sont ancêtres du socle de travail.
Le glossaire figé conserve les noms d'espèces, mouvements et objets sans
attestation PT-BR : notamment Strawberry Sweet et les autres Sweet, Water Gun,
Hydro Pump, Dreepy, Necrozma et les noms des espèces de la table fixe.

Le bilan complet, dans l'ordre du manifeste, est
`languages/pt/data/pt52_audit.json`. Il associe à chacun des 299 offsets :
corpus anglais, comparaison française au même offset, texte anglais réel,
préimage binaire, références, statut, décision, valeur attendue, longueur en
octets et largeurs. La ROM source est identifiée par son SHA256.

22 descriptions du corpus anglais sont vides ; plusieurs autres ont perdu un
retour à la ligne. Les entrées `0x1667b19`, `0x1667c5f`, `0x1667d39`,
`0x1667e8f` et `0x1667f7e` contiennent des descriptions françaises, parfois
pour la mauvaise espèce. Leurs consommateurs vivants lisent respectivement
Dreepy, Zacian, Eternatus, Zarude et Regidrago. Les traductions suivent le texte
anglais réel, sans recopier le français contaminé. Les tests métier protègent
ces divergences : sœur de Zamazenta, météorite de 20 000 ans, cipós de Zarude,
énergie de dragon cristallisée de Regidrago.

125 noms d'espèces du corpus anglais diffèrent du nom anglais effectivement
présent dans la ROM. Aucun nom français du corpus n'est importé en PT.

## Consommateurs et budgets

- Les descriptions gardent exactement trois lignes, sans tampon ni contrôle
  ajouté ; les 125 préimages comportent elles aussi deux retours. Les budgets
  sont de 232 pixels par ligne. Les textes restent sous 222 pixels selon la
  métrique partagée et sont également mesurés dans les cinq polices réelles.
- Les 19 catégories sont lues par des pointeurs de la table indirecte
  `0x1a35450–0x1a354f8`, avec plusieurs consommateurs pour High King,
  Unique Horn et Sphere. Le budget conservateur est de 96 pixels (maximum
  mesuré par la métrique partagée : 80 pixels).
- Les noms sont les cellules `base + species_id * 11`, base `0x166a98c`,
  identifiants 1 à 155. Les lecteurs de base (dont `0x144`) sont contrôlés
  avant injection et dans la ROM finale. Chaque cellule conserve intégralement
  ses onze octets anglais, terminateur et remplissage compris. Les noms
  respectent 70 pixels ; leur maximum dans la métrique partagée est 58 pixels.
- La séquence ressemblant à un pointeur vers Muk (`0x166ad5f`) à
  `0x1a43086` est une occurrence non alignée au milieu de données, sans
  consommateur texte établi ; elle reste inchangée. La cellule Muk est
  vérifiée via la base indexée, comme toutes les autres espèces.

`languages/pt/patches/batch_52.py` finalise uniquement ces consommateurs après
les passes génériques. Il réutilise `BorriusTextPatch` / `StructuredTextPatch`
pour la relocalisation atomique et bornée. Il ne reloge aucune cellule fixe.
Une préimage, un lecteur ou un budget invalide bloque le patch ; aucune entrée
n'est silencieusement ignorée. Aucun module partagé ni source FR n'est modifié.

Les lecteurs Thumb de `0x165bbca` (descriptions régionales) et `0x165bbf4`
(catégories) parcourent des paires `species_id + pointeur`, au pas de huit
octets, et retournent le champ `+4`. Leurs littéraux sont respectivement
`0x165bbec → 0x1a35504` et `0x165bc2c → 0x1a3544c`.
Les instructions source, les identifiants d’espèces et les deux lecteurs sont
aussi contrôlés sans modification dans la ROM finale. Le bilan indique chaque
paire consommée, y compris les catégories partagées par plusieurs formes.

## Recette de vérification

```sh
python3 -m pytest tests/unit/pt/test_batch_pt52.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt52_rom.py -m rom -q
npx playwright test -c tests/e2e-playwright/playwright.pt52.config.ts
npx tsc --noEmit
python3 -m ruff check languages/pt/patches/batch_52.py tests/unit/pt/test_batch_pt52.py tests/e2e/pt/test_batch_pt52_rom.py
```

Les contrôles binaires suivent toutes les cibles finales et comparent les
chaînes encodées exactes, plutôt que les anciens emplacements après
relocalisation. Ils contrôlent également les cellules voisines hors lot,
l'idempotence, les écritures bornées et le refus atomique d'une préimage ou
d'un lecteur endommagé.

La preuve Playwright utilise mGBA hors écran et une copie temporaire de la
ROM finale. Elle affiche deux descriptions, une catégorie et le nom Cyndaquil
lus depuis leurs consommateurs réels, sans réécrire le texte ni les glyphes.
Les octets sont vérifiés avant lancement puis la lecture des deux premières
lignes est vérifiée par OCR. La capture reste dans le répertoire temporaire du
système et est jointe au ticket ; aucun screenshot n'est versionné.

## Non vérifié

La sonde visuelle n'est pas une navigation dans les 299 entrées de l'interface
Pokédex. Les trois lignes complètes des descriptions et les 299 valeurs sont
contrôlées en binaire et par leurs budgets ; la sonde msgbox ne montre que les
deux premières lignes des descriptions. Le parcours exhaustif en jeu et la
certification globale relèvent de T-848. Aucun push ni pipeline distant.
