# F-764 — PT-05 : descriptions d’objets

## Périmètre réel et sources

Les 281 offsets explicites du manifeste sont couverts individuellement dans
`languages/pt/data/pt05_audit.json`. Le domaine provisoire « Menus et systèmes »
recouvre ici principalement les descriptions d’objets, des copies historiques
de descriptions et des faux positifs binaires. Aucun offset hors lot n’est ajouté.

Prérequis intégrés : F-758 (`c5b5e0b9`) et F-759 (`dcc6ce5d`), vérifiés dans
l’ascendance du worktree. La ROM source anglaise est identifiée par SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

Le corpus `combined_en.txt` contient des descriptions françaises et des entrées
vides héritées d’une ancienne base. Chaque ligne du bilan conserve le corpus EN,
la comparaison FR au même offset, les octets et le décodage de la ROM EN propre.
Cette dernière fait foi pour les effets réels : les flûtes modifient les niveaux,
Silph Co. et Devon Corp. ne sont pas interverties, et les noms d’espèces restent
anglais conformément au glossaire PT-BR. PS, Ataque Especial, Defesa Especial,
Terrestre et les autres types suivent F-759.

## Consommateurs et exceptions

- **180 traductions** : descriptions référencées par la table active à `0x876200`,
  stride 44, champ pointeur à +20. La pseudo-base historique `0x876074` précède
  cette table de neuf cellules. Le lecteur à `0x9a96c` multiplie l’identifiant
  par 44, ajoute 20, puis déréférence ; son littéral de base est à `0x9a98c`.
  Le bilan donne chaque adresse de pointeur active et chaque référence historique.
- **42 faux positifs binaires** : textes non linguistiques avant `0x3d4f26`,
  sans pointeur 32 bits vers leur offset. Aucun octet modifié.
- **42 copies historiques** : seuls des pointeurs dans l’ancienne table FireRed
  `0x3db028` subsistent. Les correspondances par nom dans la table active, lorsqu’elles
  existent, donnent le nouvel offset et le pointeur précis. Elles ne sont pas
  traduites ici : une adresse hors manifeste n’est pas autorisée par ce ticket.
- **17 orphelins sans pointeur** : deux suffixes de flûtes (`0x3d5ab0`, `0x3d5afd`)
  et quinze anciennes descriptions de TM (`0x3d93c9`–`0x3d987a`, liste explicite
  du manifeste). Les textes vivants des flûtes finissent avant ces suffixes.

La recherche de pointeurs parcourt toute la ROM sans contrainte d’alignement.
Les tests comparent cette recherche aux références inventoriées ; l’absence de
pointeur ne sert pas à exclure un champ inline reconnu comme une table fixe.
Ici, les 180 champs vivants sont des descriptions indirectes, pas des noms fixes.
Aucun patch de noms fixes n’est nécessaire. Un patch PT de finalisation des
descriptions est en revanche requis, comme expliqué ci-dessous. Les exceptions
ont chacune une justification, une préimage et les références ou leur absence.

## Contrat d’injection

Les 180 lignes sont ajoutées au combined sans réécriture de l’existant, avec
180 protections exactes dans le même commit. Toutes tiennent dans la longueur
EN d’origine, terminateur compris ; les retours à la ligne sont conservés,
y compris la ligne finale vide du météorite. Aucun placeholder ni code de page
n’est présent dans les descriptions vivantes de ce lot.

Les tests contrôlent les effets (quantités de PS/PP, durées des Repousse,
direction des flûtes), les noms et le glossaire, les budgets de 192 pixels,
les octets livrés derrière **chaque** pointeur actif et les cinq tables de largeur
de police de la ROM finale. Les exceptions doivent rester byte-identiques.

### Correctif d’injection dédié

Le premier `make build-pt` a révélé 29 divergences : 25 textes restaient anglais
et quatre descriptions de soins (`0x3d52b2`, `0x3d546f`, `0x3d54b5`, `0x3d5503`)
subissaient le rewrap de dialogue. Le JSON intermédiaire reprend notamment la
description française historique de Potion ; certaines descriptions anglaises
vides du corpus sont absentes du JSON. Le passage inline n’en rétablit pas toutes,
ses bornes incluant les cellules de l’extraction espagnole.

`languages/pt/patches/pt05_items.py`, branché en fin de pipeline PT, valide les
180 descriptions. Il accepte un texte déjà exact, ou restaure dans sa cellule
originale un texte anglais intact ou un rewrap identifiable sans changement de
mots. Un pointeur inattendu, une préimage inconnue, un contrôle interdit ou un
dépassement fait échouer la passe **avant toute écriture**. Il ne relocalise rien,
ne modifie aucun pointeur et conserve une sauvegarde `.pt05.bak`.
Les fixtures unitaires sont des extraits binaires de la ROM EN canonique.
Aucun code partagé ni patch FR/IT/DE n’est modifié.

## Recette locale

```sh
python3 -m pytest -q tests/unit/pt/test_batch_05_pt.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q -m rom tests/e2e/pt/test_built_batch_05_pt.py tests/e2e/pt/test_built_font_pt.py
npx playwright test --config tests/e2e-playwright/playwright.pt05.config.ts
```

La preuve Playwright utilise mGBA et Chromium hors écran. Une copie temporaire
de la ROM et de la sauvegarde place les champs nom et pointeur du Magnet puis
de Potion dans la Repousse déjà possédée par la fixture. La description reste celle du build,
vérifiée octet par octet avant lancement. Le vrai Cube dessine ensuite ses trois
lignes ; l’OCR doit les retrouver toutes. Aucune sauvegarde en jeu ni capture
dans le dépôt. Cette sonde teste le rendu du champ, pas un parcours d’acquisition
des 180 objets.

## Résultats après intégration de PT-02/03/04/06

- 843 tests réussis : unités PT, intégrité, registre et nouveau routage partagé ES.
- Rebuild PT réussi ; 29 descriptions finalisées et 180 vérifiées par le patch.
- 1 113 tests ROM PT réussis, dont les 283 contrôles PT-05/polices.
- Deux tests Playwright hors écran réussis, Magnet et Potion ; trois lignes
  reconnues dans chaque cas, captures conservées en pièces jointes du ticket.
- Ruff et TypeScript ciblés réussis. Les deux premiers commits ont passé leurs
  hooks complets, dont 4 724 tests Python et 68 Vitest au second passage, puis
  les builds FR/IT/DE. Un skip préexistant était présent au second passage.

Les conflits d’ajout dans combined/protections/lang.yaml ont été résolus en
conservant les blocs de tous les lots. Le chargeur du test ROM PT-05 est borné
au manifeste afin de ne pas encoder les dialogues `\p` d’autres lots.
Les seules modifications hors bilan PT-05 actualisent deux cibles de relocation
dans le bilan PT-06 (`0x3dabf7` et `0x3daf52`) ; leurs textes sont inchangés.
La vérification ROM complète contrôle également leurs 238 consommateurs.
