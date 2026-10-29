# B-1027 — Raccordement des 104 noms fixes DE objets-02

Le patch lit exclusivement les 104 valeurs last-wins de `combined_de.txt`,
protégées individuellement dans `protected_entries.yaml`. Le rapport JSON voisin
fige les correspondances, les propositions Unbound et les abréviations v1.
Lors de la reprise, la ROM précédemment construite contenait les corrections mais
les 104 sources et protections manquaient dans HEAD : elles ont été réintroduites
par ajout ciblé, sans réécrire ni réordonner le corpus existant.

## Raccordement et périmètre

- Réutilisation de `item_names.apply_scoped_item_names` de B-1026, avec préimages
  explicites propres à B-1027 ; les 122 offsets par défaut de B-1026 sont inchangés.
- Vérification SHA256 de la source canonique
  `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
- Routine `0x9A8CA`, base `0x876200` lue à `0x9A8D8`, stride 44,
  cellule nom de 14 octets, terminateur FF inclus ; aucune relocation.
- Validation atomique : source inattendue, contrôle, texte absent ou dépassement
  interrompent le lot avant toute écriture. Réapplication idempotente.
- L'ancienne écriture centrée de Berry Pouch à `0x87A0B0` est retirée : la cellule
  vivante `0x87A0BC` reçoit Beerentüte, sans toucher les 12 octets précédents.
  Le libellé distinct à `0x3DEED8` reste hors périmètre.
- Sauvegarde `.objets02.bak` pour comparer les métadonnées du build courant,
  y compris les pointeurs de description à +20.

## Abréviations explicites v1

| Nom complet | Nom injecté |
|---|---|
| Ultranecronium Z | Ultranecr. Z |
| Aerodactylonit | Aerodactylnit |
| Illumina-Galette | Illum.Galette |
| Feldbeschichtung | Feldbesch. |
| Silberkronkorken | Silberkorken |
| Purpurner Nektar | Purpur-Nektar |

Ces formes sont versionnées, jamais produites par troncature automatique.
Les propositions Unbound fournies par le ticket sont retenues comme noms propres
au projet, sans les présenter comme terminologie officielle des jeux Pokémon.
Maximum mesuré sur les 104 noms : 14 octets avec FF, 75 pixels dans le sac
(budget 78), 184 pixels pour `WWWWWWW hat <nom> in der` (budget 192).
Aucun placeholder ou code de contrôle n'est ajouté dans les noms.

## Vérifications reproductibles

- `make build-de` et `make test-python` ; hooks Python/Vitest et builds locaux
  exécutés sans désactivation.
- `python3 -m pytest -q tests/unit/de/test_item_names_objets02.py tests/e2e/de/test_item_names_objets_01.py` :
  vérifie les deux lots disjoints, les 104 noms finaux, les 196 autres noms
  qualifiés par B-684 et les métadonnées des cellules corrigées.
- La fixture des 300 noms vient de la pièce jointe `684_OBJETS_02_DE.json`.
  Le rejeu du patch sur sa sauvegarde vérifie l'absence de toute écriture hors
  des 104 champs de noms sur la ROM entière. Neuf pointeurs de description de
  CT hors liste sont relocalisés par les étapes ultérieures existantes : ils ne
  doivent pas être confondus avec une écriture du patch objets-02.
- `npx playwright test -c tests/e2e-playwright/playwright.item-names-objets02-de.config.ts` :
  14 scénarios headless mGBA (Beerentüte et les six abréviations, chacun dans le
  Cube et dans un message de réception). Chaque scénario résout aussi les 104
  vrais IDs avec `bufferitemname` et compare les octets du buffer moteur.
- Le test visuel utilise une copie temporaire instrumentée de la ROM : le nom
  et le pointeur de description de l'objet choisi remplacent ceux de la Repousse
  déjà présente dans la sauvegarde, pour exercer le rendu natif du Cube. Le
  ramassage emploie le vrai ID et le template vivant de réception. Les captures
  sont faites après assertions OCR ; A/R et Z/2 sont les seules variantes OCR
  admises, avec égalité stricte des octets en ROM et en mémoire.
- Captures et journaux joints au ticket, hors dépôt. Aucun push ni pipeline distant.

## Non vérifié

Pas de parcours manuel d'acquisition des 104 objets ni de capture individuelle
pour chacun : les 104 noms sont vérifiés en mémoire et les sept cas les plus
sensibles sont rendus dans les deux contextes. Les tests optionnels ignorés par
la suite standard restent signalés dans son journal ; aucun skip ajouté ici.
Aucune source FR/IT ni référence de hash FR modifiée. Les hooks reconstruisent
les ROM locales FR/IT ; l'artefact FR est restauré à l'identique de l'état observé
au début de cette reprise après les validations.
