# PT-73 — Options, Ligue et Polder Town

## Périmètre

Le manifeste PT-73 contient 299 clés. Le bilan individuel versionné est
`languages/pt/data/pt73_audit.json` : anglais complet lu en ROM, traduction,
préimage, lecteurs, commandes, taille encodée, budgets et mesures dans les cinq
polices PT. Les sources EN et FR ont été comparées au même offset ; l'anglais ROM
fait foi lorsque l'extraction tronque un dialogue ou décrit une autre chaîne.

296 entrées sont ajoutées (286 traduites, 10 noms/cris conservés et vérifiés), sans
suppression ni modification d'autres lignes, avec leurs protections exactes.
Le glossaire F-759 impose la conservation des noms
non attestés : Elite Four, Pokémon League, Trainer Card, lieux, objets et mouvements.
Les indices de TMs conservent notamment les étages anglais 1F/4F/B1F : les étages
français ne sont pas recopiés.

## Lecteurs et budgets

Le finaliseur `batch_73` utilise l'injection structurée existante, après les
réparations et la police. Il relocalise uniquement les consommateurs audités,
vérifie les préimages, les commandes et la pagination exactes. Aucun texte vivant
de ce lot n'est une cellule ROM fixe non repointable. La contrainte fixe pertinente
est la copie des libellés Options dans des cellules **RAM de 20 octets**.

Le désassemblage et les templates natifs établissent : libellés 94 pixels,
19 octets + terminateur ; titres 96 pixels ; valeurs 112 pixels ; aide 223 pixels.
Les dialogues ont un budget de 208 pixels. Les mesures incluent les glyphes tildés
PT et les tampons développés : noms joueur/rival, espèces, mouvements, lieux,
récompenses et compteur de pêche jusqu'à 65535.

Sept occurrences binaires ressemblant à des pointeurs sont en réalité dans des
échantillons PCM. Le bilan donne pour chacune le début d'onde, son en-tête, sa taille
et le pointeur d'instrument. Elles sont exclues du repointage et restaurées si une
passe générique les a prises pour du texte.

À `0x1f4e4e2`, le corpus EN indique « None » : le lecteur vivant affiche en réalité
la confirmation de sauvegarde des options. La traduction suit les octets et couleurs
réels, pas ce libellé erroné.

## Tampon local Croagunk

Le message `0x1f530b3` compose une description dans FD03. Son helper natif est
référencé uniquement par le spectacle de Croagunk. Une table privée et quatre textes
PT localisent ce tampon ; seul le littéral du helper `0x1ec99d4` change. La table
commune, les quatre textes sources hors manifeste et les autres lecteurs sont
préservés. Les preuves du script, du helper et des sources sont dans le bilan.

## Trois exceptions

- `0x1f4dba5` (Light) et `0x1f4dbab` (Dark) : aucun pointeur ROM, absents des tables
  Options vivantes utilisées par le lecteur `0x1ebc2d4`. Aucune traduction injectée.
- `0x1f4e244` : ancienne légende sans pointeur ROM. Le constructeur `0x1ebd090`
  charge les actifs graphiques via `0x1ebd364`/`0x1ebd36c`, tandis que l'aide vient
  du lecteur `0x1ebc760`. Une écriture in-place de cette chaîne ne serait pas une
  preuve de traduction visible ; elle reste intacte.

## Vérifications reproductibles

```sh
python3 -m pytest tests/unit/pt/test_batch_pt73.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt73_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt73.config.ts
```

La sonde Playwright ouvre les Options natives par les boutons GBA et affiche un
message du Centre Pokémon via son pointeur livré dans une copie temporaire. Elle
vérifie l'OCR, les octets attendus et l'absence d'écriture de sauvegarde. Les captures
restent dans le répertoire temporaire du système, hors dépôt. Elle ne constitue pas
un parcours manuel de tous les dialogues de la Ligue et de Polder Town.

## Validation de reprise F-832

- 33 tests unitaires et d'intégrité réussis ; diff contrôlé : 296 ajouts exacts,
  aucune suppression et aucun offset d'un autre lot.
- `make build-pt` réussi ; les quatre tests ROM réussissent sur ce build, y compris
  les pointeurs vivants, les cinq polices et l'atomicité/idempotence du finaliseur.
- Lint Python ciblé et compilation TypeScript réussis.
- Playwright hors écran : un test réussi, trois scènes réelles contrôlées par OCR,
  octets aux consommateurs et sauvegarde inchangée. L'OCR confond parfois le « o »
  pixelisé de Pokémon avec « a » ; cette seule variante est tolérée après inspection
  de la capture, tandis que les octets restent comparés exactement.
- Les libellés anglais visibles hors PT-73 restent du ressort de leurs propres lots.

Non vérifié : parcours manuel intégral des dialogues Ligue/Polder Town ; la sonde
Centre Pokémon déclenche le message via le pointeur livré dans une copie temporaire.
