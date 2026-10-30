# PT-72 — Scénario final et après-campagne

Périmètre : les **300 offsets explicites** PT-72 de
`languages/pt/translation_batches.json`. Prérequis F-758 et F-759 intégrés.
Aucun autre offset de combined n'est modifié ; toutes les traductions préexistantes
sont conservées. Les 299 lignes ajoutées ont une protection exacte dans le même commit.

Le bilan exhaustif, dans l'ordre du manifeste, est
`languages/pt/data/pt72_audit.json` : anglais complet extrait de la ROM, préimage,
consommateurs, traduction, taille encodée, largeur de chaque ligne dans les cinq
polices et majorants des tampons. `translated` signifie texte livré au consommateur ;
`retained_english` signifie nom propre conservé conformément au glossaire, et non
absence d'injection. Les essais ROM contrôlent les octets finaux aux pointeurs vivants.

## Zones et décisions

Le lot couvre Aklove et The Shadows, Distortion World, Rift Cave, Vivill Town,
le trajet vers East Borrius et Crystal Peak, la réconciliation familiale,
le titre de Champion et le Hall of Fame, le post-jeu et l'arrestation d'Aklove,
Newmoon Island/Darkrai, puis quatre libellés de menus. Les noms propres restent
anglais conformément à F-759 ; les mouvements et Habilités non attestés aussi.
Le nom Ultimate Weapon est conservé en anglais, selon le glossaire F-759 et les lots voisins.

Les longues répliques ont été comparées à leurs versions françaises au même offset,
mais traduites depuis l'anglais. La ROM complète fait foi lorsque le combined EN
est absent ou limité : notamment 0x1f464ab, 0x1f474c3, 0x1f476ec, 0x1f478ee,
0x1f49a85, 0x1f4aa46, 0x1f4ad47, 0x1f4b2e0, 0x1f4b80a, 0x1f4bef9 et 0x1f4c2ed.

## Consommateurs particuliers et exception

- **0x1f454a2 : exception non référencée.** Aucun pointeur vers son début ou son
  intérieur n'a été trouvé dans la ROM EN. Le script précédent utilise le pointeur
  0x1e9de08 vers 0x1f45482, puis se termine. La réplique suivante est appelée via
  0x1e64aa7 vers 0x1f454e9. Aucun texte n'est ajouté pour cette réplique inutilisée.
  Cela ne constitue pas une preuve d'accessibilité dans toutes les variantes du jeu.
- **0x1f4b6d9 : suffixe vivant, traduit et injecté.** Le script trainerbattle utilise
  le pointeur 0x1e7e9be vers 0x1f4b6d0, neuf octets avant la clé du manifeste.
  Le finaliseur recompose un préfixe « Uau, [joueur] ! » et le suffixe traduit,
  puis repointe le consommateur. Aucune clé supplémentaire hors lot n'est ajoutée.
- **0x1f4d5e8 : faux pointeur audio exclu.** La correspondance 0x11383a0 appartient
  à l'échantillon PCM M4A 0x1137b90–0x113afd0, référencé par quatre instruments.
  Elle est restaurée après le builder générique ; le seul consommateur texte
  réel est 0x1e8d721. Préimage, en-tête audio et pointeurs d'instruments testés.
- **0x1f4da6c–0x1f4da8a : tables de pointeurs**, pas cellules texte contiguës fixes.
  Le patch dédié repointe ces seuls libellés. Il ne force pas une écriture en place.

## Tampons contextuels

Trois appels locaux sont enveloppés : 0x1e9ddf6 (`his/her` → `seu`),
0x1e6d6ee (`boy/dear` → `jovem`) et 0x1e8d6e6 (`son/daughter` →
`meu filho/minha filha`). Chaque wrapper appelle d'abord la routine originale
et conserve VAR_RESULT (genre). Les routines partagées et les entrées des
lots PT-71/PT-75 ne sont pas modifiées. Un interpréteur des seuls opcodes
présents dans ces helpers exécute les vrais octets source et finaux pour
les deux genres ; il contrôle les valeurs des tampons utilisés par PT-72.

## Contrat et validation reproductible

Les séquences FC/FD et les pages FA/FB gardent exactement leur ordre et leurs
paramètres. Seuls les retours de ligne FE sont redistribués à l'intérieur d'une
page ; deux lignes maximum par page, une seule ligne après un défilement FA.
Budget dialogue : 208 pixels ; options : 112 pixels. Noms joueur/rival majorés
par sept W, autres tampons par dix ou onze W ; aucun simple comptage Unicode.

Le finaliseur réutilise les primitives partagées sans les modifier : préimages
strictes, allocation libre, transaction atomique et contrôle des pointeurs.
Les tests métier vérifient notamment la Batalha Dupla, les destinations, les
instructions et les fins des longs discours ; le test ROM vérifie toutes les
299 livraisons, le suffixe, l'audio intact, les bornes et l'idempotence.

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt72.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt72_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt72.config.ts
```

La preuve Playwright démarre trois copies temporaires de la ROM finale dans
mGBA offscreen et appelle la msgbox native aux pointeurs livrés. Elle compare
les octets ROM, contrôle par OCR les premières pages d'Aklove, du réglage de
l'arme et de la fin de campagne, puis capture leur montage dans le dossier
temporaire système. Elle ne certifie pas un parcours complet du scénario ni
le rendu de toutes les pages ou des options en navigation réelle.
Aucune sauvegarde utilisateur, aucun push et aucun pipeline distant.
