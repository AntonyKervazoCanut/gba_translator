# B-1030 — Identifiants contractuels d’ES-001

Ce prérequis de F-851 ne traduit aucune entrée. Les 373 identifiants de
`lots.json`, les inventaires, les sources EN/ES/FR, le glossaire et les fichiers
combined/manifeste restent inchangés. Les 18 fragments/références indirectes
restent à reconstruire par F-851 ; ce travail ne qualifie pas le lot comme traduit.

## Contrat et utilisation

`languages/es-maint/lang.yaml` active explicitement `text_aliases`, pointant sur
`languages/es-maint/text_aliases.json`. Les autres langues n’activent rien ;
leur chaîne et le builder conservent leur comportement par défaut.

Pour F-851, écrire la traduction et sa protection **à la clé contractuelle**,
jamais à la clé vivante. Ne pas ajouter le caractère parasite `9` (`AA`).
Ne pas recalculer les lots. Le cas `0x0018D43D / 0x0018D43E` n’est pas un alias
configuré : les deux clés sont déjà contractuelles et ne doivent pas recevoir
de traductions concurrentes.

Le résolveur partagé `src/core/text_aliases.py` :

1. Vérifie le préfixe, la préimage EN complète (FF compris), l’absence de tout
   pointeur vers le faux début et l’ensemble exact des pointeurs EN (scan non
   aligné, également pour les trois références de `0x0019A5BD`).
2. Refuse clés ou cibles dupliquées, chaînes d’alias, chevauchements et coexistence
   d’une traduction contractuelle et de sa clé vivante, même à valeurs identiques.
3. Exige une correspondance unique dans l’offset map **à l’adresse EN vivante**,
   puis vérifie la préimage ES, son extraction et les pointeurs ES à cette cible.
   Il n’interprète pas l’ES au faux début ni par égalité supposée avec l’adresse EN.
4. Crée seulement un CSV dérivé `output/translation/es-maint_alias_base.csv` :
   le texte source vivant y porte temporairement la clé contractuelle pour recevoir
   le combined. Le CSV générique partagé n’est pas modifié. Aucun combined n’est
   généré, déplacé, trié ou réécrit.
5. Après conversion, exige que chaque alias demandé soit présent dans le JSON.
   Le JSON réellement transmis au builder porte `offset` vivant, `contract_offset`
   de provenance, `english_raw_bytes`, `pointer_offsets`, `spanish_offset` et le
   budget exact de préimage. `max_length` inclut FF ; `original_length` l’exclut.
   Fallback et troncature sont désactivés pour ces entrées : dépasser le budget
   impose la relocalisation habituelle. Le mode opt-in
   `preserve_control_flow` refuse une différence de commandes FC/FD/F8/F9/F7
   (arguments inclus), de FA/FB ou d’ordre des buffers et un texte encodé de plus
   de 512 octets. Il désactive le rewrap automatique, qui changeait FA en FE dans
   la preuve sentinelle. Les sauts FE sont éditables par le lot ; la largeur et
   la hauteur des fenêtres restent à contrôler dans F-851.
6. L’étape inline reçoit explicitement `--text-aliases` : elle revalide le contrat
   EN et exclut les clés contractuelles, empêchant une seconde injection à AA.
   Le repointage final utilise le JSON aux adresses vivantes.

Les préimages sont des octets, pas une traduction ES approuvée. F-851 doit encore
relire la phrase, ses commandes et arguments, les buffers, FA/FB, les budgets en
pixels, les fenêtres et le plafond 512, puis vérifier le rendu de ses traductions.

## Les dix alias

| Clé contractuelle | Début vivant EN | Pointeurs EN |
|---|---|---|
| 0x0017FF49 | 0x0017FF4A | 0x00166CAF |
| 0x0018EA44 | 0x0018EA45 | 0x00169DE6 |
| 0x0018EA65 | 0x0018EA66 | 0x00169E73 |
| 0x0018EBE5 | 0x0018EBE6 | 0x00169E1C |
| 0x0018ED80 | 0x0018ED81 | 0x00169E48 |
| 0x00197873 | 0x00197874 | 0x0016D1D8 |
| 0x00198BBA | 0x00198BBB | 0x007C0A4C |
| 0x0019A4F7 | 0x0019A4F8 | 0x0016E8FA |
| 0x0019A5BD | 0x0019A5BE | 0x007C3779, 0x007C3811, 0x007C383E |
| 0x0019A79F | 0x0019A7A0 | 0x0016EA12 |

Dans la version épinglée, l’offset map donne les mêmes dix adresses en ES.
Un test déplace explicitement une référence ES pour vérifier que le résolveur
suit réellement la map. Toute dérive de map/préimage doit être réauditée,
pas acceptée automatiquement comme une nouvelle version compatible.

## Reproduction locale

```sh
python3 -m pytest tests/unit/test_text_aliases.py tests/test_generic_build_patches.py tests/test_language_registry.py -q
python3 -m pytest tests/e2e/es/test_contractual_aliases.py -q -s
make build-es-maint
make build-it build-de
make test-python
make build-fr BUILD_NUMBER=0
```

Le test ROM exige les extractions EN/ES et la map du pipeline dans `output/`.
Il crée un combined sentinelle uniquement dans `tmp_path`, exécute les vraies
commandes d’application, la conversion, le builder et **tous** les patches es-maint.
Il vérifie les dix entrées du JSON, les douze pointeurs après relocalisation,
les octets complets (FC/FD et arguments, FA/FB/FE/FF inclus), les préimages restées
intactes et les SHA-256 des combined, manifestes et ROM sources. `-s` affiche
les commandes complètes et leurs arguments, y compris les chemins temporaires.
Les fixtures unitaires sont des tranches réelles des ROMs épinglées, et non du
texte ASCII ou des mocks de ROMReader.

La sentinelle est un test binaire temporaire, pas une nouvelle traduction livrée.
Aucune modification de rendu n’est attendue avec le combined es-maint inchangé ;
la preuve visuelle des futures phrases appartient à F-851.

## Résultats locaux (2026-10-29)

- Tests ciblés du résolveur, du dispatch et du registre : **93 réussis**.
- Sentinelle après toute la chaîne es-maint : **1 réussi**, 10 entrées et
  12 pointeurs, comparaison des octets entiers et SHA-256 des sources.
- `make test-python` : **4393 réussis, 3 ignorés préexistants, 2289 désélectionnés**.
- `make lint` : **6688 tests collectés sans erreur** ; Ruff des nouveaux modules
  et `git diff --check` réussissent.
- `make build-es-maint`, `make build-it build-de` : réussis.
- FR reconstruite avant/après avec `make build-fr BUILD_NUMBER=0` aux mêmes sources :
  SHA-256 identique `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
- ES maintenu : `43504c10e47ff2ff655d0fcecf5cbc5030c1b30902d7c549ca4b9cdd194c33c0`,
  identique à F-850. Son JSON de production contient toujours zéro traduction.
- EN source : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7` ;
  ES source : `a98a14adc231327db22baa7d7762b95abc0fe5bfe6fcc64e38a2c6b525429ff6`.
  Ces empreintes correspondent aussi à la préqualification jointe à F-851.
- 17 fichiers combined, manifestes, glossaires, inventaire et listes contractuelles
  comparés à HEAD : aucune différence. Aucune sentinelle dans ces sources.

Les commandes complètes de la preuve sentinelle sont jointes au ticket B-1030.

Le contrôle supplémentaire `make test-rom` matérialise les BPS versionnés et
remplace les ROMs locales : **1186 réussis, 34 ignorés, 878 échecs** sur ces
instantanés (dont PT absente avant sa reconstruction). Les écarts concernent
principalement les contenus DE plus récents que les BPS, comme déjà signalé par
F-850. Ce résultat ne certifie pas les artefacts distribués. Le test sentinelle
réussit aussi dans ce profil. PT a ensuite été reconstruite avec `make build-pt`.
Les reconstructions FR/IT/DE et la vérification après intégration sont consignées
dans la résolution du ticket ; aucun BPS ni attendu de test n’est modifié ici.
