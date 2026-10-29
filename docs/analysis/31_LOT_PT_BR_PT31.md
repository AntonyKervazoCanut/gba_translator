# PT-31 — Noms d’objets dans la table fixe

Le libellé provisoire « Zones Borrius » ne décrit pas ce lot. Les 288 offsets
explicites du manifeste concernent les noms d’objets : TM13–TM120, HM01–HM08,
objets clés, Méga-Gemmes, Baies et objets tenus. Les trous du manifeste ne sont
pas des autorisations d’édition.

## Décision linguistique et périmètre

F-758 et F-759 sont terminés et intégrés. Le glossaire
`languages/pt/data/official_terminology.yaml`, catégorie `items`, impose
`fallback: preserve_english`, sauf exception nominale attestée. Aucun des 286
noms valides de ce lot n’a d’exception dans ce glossaire. Les graphies sources,
y compris les abréviations imposées par les cellules (`Charizite X`,
`Terrain Ext.`, etc.), sont donc conservées exactement, sans reprendre le FR.

Les 286 lignes sont ajoutées à la fin du combined, avec protections exactes.
Aucune traduction existante n’est supprimée ou modifiée. Le bilan exhaustif,
dans l’ordre du manifeste, est `languages/pt/data/pt31_audit.json` : anglais,
référence FR disponible, valeur PT, octets, largeur, identifiant d’objet,
cellule, références et justification de chaque décision.

## Consommateur et budgets

La table vivante commence à `0x876200`, avec un pas de 44 octets. Le littéral
à `0x09A8D8` du lecteur d’objets pointe sur cette table. Le nom est incorporé
au début de chaque structure, dans un champ de 13 octets, terminateur compris ;
il n’a pas besoin d’un pointeur individuel. Le lecteur et son littéral sont
figés dans l’audit et contrôlés dans la ROM reconstruite. L’absence de pointeur
direct vers un nom ne permet donc pas de le déclarer mort.

Les 286 noms sont encodables strictement, sans contrôle ni saut de page, dans
13 octets et 78 pixels au maximum. Les tests ROM mesurent aussi les largeurs
dans les cinq polices finales, vérifient les noms aux cellules indexées et les
métadonnées voisines, sauf les pointeurs de description traduits par les autres
lots. Aucun nouveau patch de table fixe n’est nécessaire pour ces noms
inchangés : la preuve requise est leur présence exacte dans la ROM finale,
et non une prétention d’injection d’une traduction différente.

## Exceptions

| Offset | Cellule vivante | Justification |
| --- | --- | --- |
| `0x879E88` | `0x879E80`, `Package` | `arce` est un résidu à +8, après le terminateur de `Package` à +7. Aucun pointeur direct ; le lecteur indexé commence à +0. |
| `0x87A0EC` | `0x87A0E8`, `ADM` | `hy Tv` est un résidu à +4, après le terminateur d’`ADM` à +3. Aucun pointeur direct ; le lecteur indexé commence à +0. |

Ces deux faux textes ne sont pas ajoutés au combined. Le test ROM vérifie
leurs octets, leur position après terminateur et l’absence de pointeur direct.

## Rendu

Aucun texte affiché ne change : les 286 valeurs PT sont identiques aux noms
anglais déjà présents dans les cellules vivantes. Il n’y a donc pas de capture
Playwright revendiquée pour ce lot. Le contrôle visuel du parcours complet
reste du ressort de T-848 ; la preuve de ce lot est binaire, sur le build PT.

## Vérification locale

`make build-pt` réussit. Les trois tests PT-31 (unitaires et ROM) passent sur
cette ROM : 286 noms identiques aux octets sources aux cellules effectivement
consommées, budgets des cinq polices, deux résidus intacts et métadonnées
préservées. Les 36 contrôles ciblés d’intégrité, de recettes et de PT-31 passent.
La vérification du diff confirme les 5 824 valeurs PT antérieures intactes.

Le premier passage du hook a révélé qu’un test de `certify-de --dry-run`
nécessite déjà une ROM DE locale : sa sous-recette exécute `cp` et `cmp` même
en simulation. Les ROM locales ont été copiées dans le worktree isolé, puis
le test de recette est passé. Aucun test ni hook n’a été désactivé.
