# ES-008 — sept débuts de menus contractuels

F-1037, prérequis technique de F-858. Aucune traduction de production.
Les valeurs finales et leur relecture restent à F-858. Les 373 préimages de
[008_PREPARATION.json](008_PREPARATION.json) restent la référence de préparation.

## Acheminement

`TextAliases` conserve les clés du lot dans le CSV et le combined, puis transmet
au builder commun l'adresse vivante, la préimage complète et les consommateurs.
Aucun réinserteur ni patch de traduction supplémentaire. Le mode `english_only`
est explicite, limité au contrat IDNo. : cible espagnole nulle, préimage ES
interdite et statut unique `only_in_english` exigé dans l'offset map. Les autres
contrats exigent toujours `matched`, préimage ES et pointeurs ES conformes.
Les données viennent des ROM EN/ES et de leurs extractions actuelles ; aucune
égalité d'adresse n'est inférée des combined de référence.

| Clé | Début vivant | Référents exhaustifs | Police | Budget pixels |
|---|---|---|---|---|
| 415D45 | 415D48 | 12EF3C, 12F484, 12F62C | 0 | 188 |
| 415D4F | 415D50 | 12F038, 12F640 | 0 | 188 |
| 415D5E | 415D60 | F2D54, 9F2868 | 0 | 115 |
| 415D77 | 415D78 | F2D20, 9F285C | 0 | 115 |
| 415D8A | 415D8C | F30FC | 0 | 232 |
| 4160F9 | 4160FC | F35F8 | 2 | 64 |
| 416101 | 416104 | F33D8, F3600, 9F2B98 | 2 | 80 |

Adresses hexadécimales, sans base 08000000. Les sept préfixes de 1 à 3 octets
nuls ne sont jamais du texte. Les 18 anciens alias restent présents.
Six correspondances ES sont confirmées à la même adresse ; IDNo. est EN seul.

Les `table_offsets` 9F2850 et 9F2B7C de l'extracteur sont en réalité des
pools de littéraux Thumb, sans racine de table référencée. Les alias 9F285C,
9F2868 et 9F2B98 sont chargés par instructions PC-relatives aux adresses
9F27E6, 9F2816 et 9F2B24. Les littéraux voisins sont protégés par la comparaison
intégrale des écritures ; aucun faux consommateur n'est inventé.

## Fenêtres et mesure moteur

- Aides de contrôles : routines 10F5E8/10F650, police 0, y=1,
  x=(236−GetStringWidth(0, texte, 0)) & 255. `Controls` à gauche est rendu
  en police 1 à x=4, largeur 43 : réserve jusqu'à x=48, budget droit 188.
- Aides Palmarès : fenêtre dynamique créée par 10F558, 30×2 tuiles,
  racine 9F2948. `Hall of Fame No. 999` à gauche prend 116 pixels,
  x=4 et marge 1 : budget droit 115. `Exit`, sans ce voisin, garde 4 pixels
  de marge à gauche et dispose de 232 pixels.
- Fiche Pokédex : fenêtre 40C234 (17×6 tuiles), racines F2754/F35EC.
  `Name` à x=4,y=3 ; nom aligné sur x=130, réserve conservatrice de
  neuf caractères ×6 pixels et marge 8 : budget libellé 64 pixels.
  Le template joueur 3E245C (table active A6CE38, racine 9DB58) autorise
  réellement sept caractères. Les trois pages du clavier 3E22D0–3E232F
  (racine 9F664) n'ont aucun glyphe de plus de 6 pixels en police 2,
  y compris ♂/♀ : 42 pixels réels au maximum, contre 54 réservés.
  `IDNo.` à x=4,y=18 précède le numéro placé à x=100.
- Palmarès : IDNo. est aussi concaténé avec cinq chiffres via StringCopy
  8D84 et ConvertIntToDecimalStringN, puis imprimé à x=96 dans 208 pixels.
  Réserve de 30 pixels pour les chiffres : plafond conservateur 80 pixels.
  Plafond complémentaire de 32 octets FF inclus pour le libellé, laissant
  les cinq chiffres et le terminateur dans le buffer de 40 octets.

Largeurs Latin de police 0 : 1EEF00 (fonction 64D0, littéral 64E4).
Police 2 : 207300 (66F8, littéral 6720). La police 1 du titre gauche
(1FB100, fonction 6598) est également gelée. Les 512 valeurs de chaque table
sont gelées dans le contrat. F9 utilise l'indice 100+argument. F8 lit la
largeur à +2 dans la table 1EA6CC, stride 4 (fonction 6428) : 00/01/0A
avancent de 8 pixels. Le moteur 5C28..5C4E n'ajoute l'espacement configuré
qu'en mode japonais ; ces chaînes Latin n'en ajoutent pas.

Ces métriques sont opt-in. La mesure historique des descriptions/dialogues
reste inchangée. Une seule ligne est admise ; commandes et arguments restent
identiques. Fallback, troncature, terminateur interne et disparition à la
conversion sont refusés. Les racines, fenêtres et métriques sont contrôlées
avant injection et après tous les patches ; chaque consommateur final doit
contenir les octets encodés de la valeur du combined, même si un cache JSON
perdait cette valeur. Le builder ne peut donc réussir après un retour en EN.

## Vérification reproductible

- `tests/unit/test_text_aliases.py` : préimages ROM figées, nouveaux et anciens
  contrats, absence ES explicite, collisions, commandes/arguments F8/F9/FC,
  largeur exacte, racines et corruption après patches.
- `tests/e2e/es/test_es008_alias_routes.py` : combined temporaire uniquement,
  vrai CSV → JSON → builder → patches. Chaque texte est préfixé de `Z` pour
  imposer une relocation sans modifier ses commandes. Sept clés et quatorze
  consommateurs vérifiés. Comparaison intégrale avant patches avec EN et
  après patches avec témoin vide traité par les mêmes patches : aucune
  écriture hors pointeurs et nouvelles allocations autorisées. Préfixes,
  textes originaux et voisins conservés. Empreintes des sources de traduction,
  protections, glossaire et lots inchangées.
- `tests/e2e/es/test_contractual_aliases.py` : tous les alias, anciens compris.
- Preuve Playwright/mGBA : mire temporaire des sept chaînes réellement lues
  aux pointeurs finaux, avec fonctions natives de largeur et d'impression.
  Elle certifie l'acheminement et le rendu moteur des sentinelles ; les parcours
  complets et textes espagnols définitifs restent à F-858. Aucune sauvegarde.

Les résultats, empreintes et éventuelles limites de validation sont consignés
au ticket après exécution. Aucun combined, protected_entries.yaml, glossaire
ou lots.json modifié. Aucun push ni pipeline distant.

Reproduction de la mire (après présence des ROM sources et caches d'extraction) :

```sh
python3 -m pytest tests/e2e/es/test_es008_alias_routes.py -q
npx playwright test -c tests/e2e-playwright/es008.config.ts
```

Première exécution réelle : pipeline 1 passed (82,66 s), Playwright 1 passed
(2,2 s). Les largeurs calculées par GetStringWidth en mGBA sont respectivement
33, 66, 108, 83, 32, 30 et 35 pixels, égales aux tables gelées du contrat.
La capture après assertions est attachée au ticket, hors dépôt.

Les aides F8 doivent conserver leurs arguments binaires (`F8 00`, `F8 01`,
`F8 0A`) : les graphies `À` ou espace de l'extraction ne désignent pas des
lettres à traduire. Utiliser les commandes complètes de la préimage canonique.

## Validation locale du 6 novembre 2026

- `make build-fr build-it build-de build-es-maint BUILD_NUMBER=0` : succès.
- FR avant/après : identité octet par octet,
  `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
- ES maintenu sans import :
  `c415e3913a23dfc296746ebfe9dcafabd81efe05023e2c4b56967960999e141b`.
- `make test-python` : 9664 passed, 3 skips préexistants, 4430 deselected.
  Le worktree doit avoir ses builds avant cette suite : un test de recette
  Make lit la ROM DE même en dry-run. L'interpréteur temporaire Python 3.14
  est sélectionné via PATH ; passer PYTHON en argument de Make perturbe un
  test existant qui compare une commande littérale `python3`.
- `make lint` : 14097 tests collectés. Typecheck Playwright et Ruff ciblé
  réussis ; aucun diagnostic supplémentaire dans le builder historique.
- `make -o materialize-test-roms test-rom` sur les quatre reconstructions :
  2597 passed, 32 skips, 84 failed et 1526 erreurs. Ce contrôle global
  n'est donc pas certifié : les artefacts PT-BR ne sont pas construits ici ;
  cinq autres tests signalent des divergences DE (attendus de contenu F-601,
  rival et dialogues-09) et le hash du BPS historique FR. Aucun attendu
  modifié ni test désactivé. Les tests ROM ES-001/002/003/005, les alias
  antérieurs et les sept nouvelles routes passent dans cette exécution.
- Témoin DE supplémentaire : builder d'origine de HEAD, mêmes JSON/patches,
  sortie distincte puis comparaison intégrale avec le builder modifié :
  identité binaire `fc1774fdd24ba441b2f5fc21fcbd0518a73bdd5f8b64ffc6a8753272c174c39f`.
  Les écarts DE de la suite ROM globale ne sont pas introduits par ce ticket.
