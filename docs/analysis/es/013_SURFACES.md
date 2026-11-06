# ES-013 — Natures et structures de décorations

Les 80 clés examinées sont les 54 descriptions, le fragment `4556F6` et les
25 natures de la sélection exacte ES-013. Les préimages et correspondances
ES uniques sont conservées dans `013_SURFACES.json`, sans import linguistique.
Les absences ES portent explicitement le statut `only_in_english` ; les deux
consommateurs EN suffisent à reconstruire ces noms, sans traduction depuis FR.

## Natures : contrat commun, deux consommateurs par ID

Les tables `463E60` et `1FE65F4` contiennent les mêmes 25 cibles, dans l'ordre
Hardy à Quirky. Le scan LE32 tous alignements ne trouve que ces deux références
par nom. Les sept racines sont figées par des gardes de routines complètes :

- `488B8` : GetNature à `48850`, index ×4, StringCopy à `48864`, impression
  `6124` en police 0. Le nom est copié à sp+0x16 ; le prochain usage de pile
  mémorisé commence à sp+0x28.
- `1375F0`, `1377A8` : index ×4, placeholder 0 du résumé via `13CCAC`.
- `1EB8D0C`, `1EC820C`, `1ECB154`, `1ECB198` : routines CFRU, index ×4,
  copie `StringCopy` (`8D85` Thumb) vers `gStringVar1` (`02021CF0`).
  La première vérifie explicitement ID ≤24 avant lecture.

Le contrat réutilise SystemTextRoutes, sans patch dédié ni seconde traduction.
Il limite volontairement les noms à l'enveloppe source : une ligne, sept octets
visibles, huit avec FF et 42 px (police 2). C'est une limite conservatrice de
contenu, pas une affirmation sur la largeur des fenêtres contenant le nom et
leur prose. Les noms officiels proposés par D-849 tiennent dans cette enveloppe.
Les commandes et ruptures absentes de la source ne peuvent être introduites.
La vérification finale relit les deux cibles après tous les patches.

## Décorations : fenêtre non certifiée, injection différée

Chaque description occupe le champ +0x18 d'une structure de 32 octets dans
`gDecorations` (`4556F8`). La racine est exportée à `14C` dans GFRomHeader.
Les 54 pointeurs descriptifs sont bien des champs distincts des noms, prix et
pointeurs graphiques. Cela ne prouve pas un lecteur d'écran natif accessible.

Le scan des références vers la table ne fournit aucune racine de routine
établie ; les occurrences intérieures non alignées ne démontrent pas de lecture
textuelle. ES-012 documente déjà la même limite (`012_VALIDATION.md`) : son
budget de 110 px est conservateur et n'est pas mesuré depuis un appelant.
PT-17 annonce 112 px mais ne fournit pas cette preuve de fenêtre. Ces chiffres
ne sont donc pas transformés en contrat certifié ES-013.

Les 54 descriptions restent explicitement exclues d'import jusqu'à qualification
moteur de la fenêtre. Les structures complètes et leurs textes sont gardés,
y compris les pointeurs descriptifs. `4556F6` est également exclu : ses octets
précèdent le nom SMALL DESK dans la première structure, pas une nouvelle phrase.
Aucun changement de nom, prix ou graphisme n'est autorisé.

## Contrôles reproductibles

`tests/unit/test_es013_surfaces.py` utilise des tranches réelles de la ROM EN
canonique. Il force la relocation des noms courts vers des sentinelles de sept
caractères, vérifie les deux tables, compare chaque octet hors allocations et
pointeurs autorisés, puis corrompt le second consommateur pour démontrer le refus.
Il contrôle toutes les racines et refuse les 55 clés non certifiées. Les fixtures
sont des préimages, jamais des traductions de production.

Non vérifié : fenêtre et accessibilité moteur des décorations ; parcours naturels
exhaustifs des consommateurs des natures ; certification linguistique finale.

La sonde `es013-natures.spec.ts` a passé ses assertions Playwright Chromium
headless + mGBA offscreen : 25 ID aux deux tables, soit 50 lectures des pointeurs
livrés, copies par StringCopy natif, canaris avant/après les tampons, métriques
natives des polices 0 et 2 ≤42 px. Pour chaque ID, les deux impressions moteur
ont des bitmaps identiques, non vides et contenus dans le budget. La capture
`f1044-natures-proof.png` est produite après assertions dans le dossier temporaire
système. Le test indexe explicitement les tables dans une sonde RAM : il ne
revendique pas l'exécution des sept parcours naturels ni une nouvelle fenêtre
native. Aucune sauvegarde ni modification de la ROM produite par le pipeline.
