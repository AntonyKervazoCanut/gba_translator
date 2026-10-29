# PT-18 — Communication sans fil, natures, saisie et descriptions

Périmètre fermé : les **282 offsets explicites** du manifeste PT-18, et non toute
la plage. F-758 et F-759 sont intégrés. Sources comparées au même offset :
`languages/en/combined_en.txt`, `languages/fr/combined_fr.txt` et préimage de
`input/roms/englishrom.gba` (SHA-256 dans l’audit JSON).

## Décisions et livraison

- 168 textes traduits ; 36 conservés (25 natures selon F-759, 11 groupes de lettres).
- 28 noms propres du Trainer Tower conservés dans leurs cellules brutes.
- 50 exceptions : 38 doublons commençant dans le remplissage avant une autre
  entrée vivante du lot, 7 extractions commençant dans les métadonnées de Pokémon,
  une séquence binaire sans pointeur à `0x4716b4`, quatre descriptions remplacées.
- 204 nouvelles lignes, toutes protégées exactement, sans suppression ni changement
  d’une traduction antérieure. Aucun offset d’un autre lot ajouté au combined.

L’export anglais des descriptions est ancien : plusieurs valeurs y sont vides ou
françaises. Les préimages ROM anglaises établissent le sens : Mist à `0x483606`
protège l’équipe par une brume, l’ancienne Growth à `0x483b57` ne décrit que l’Attaque Spéciale,
Fire Spin à `0x483db0` indique deux à cinq tours dans cette chaîne ancienne.
Aucune reprise aveugle du français ni modernisation de ces préimages.
Wonder Cards, Wonder News et les noms de mini-jeux sont conservés faute
d’équivalent officiel attesté. Les natures suivent explicitement F-759.

Le finaliseur `languages/pt/patches/batch_18.py` réutilise `StructuredTextPatch`
après les réparations et repointages génériques. Il vérifie les préimages et tous
les pointeurs déclarés, alloue hors des cellules voisines et contrôle le résultat.
Pour les clés de remplissage sans doublon vivant dans le lot, une route explicite
relie la clé du manifeste au vrai début de la chaîne, sans écrire dans le padding.
Cela livre aussi les libellés de menus absents du CSV et les descriptions omises
par l’export. Les références de tables fixes sont repointées individuellement ;
aucune table brute de noms n’est déplacée.

Les descriptions conservées dans le résumé sont livrées à leurs cellules de la
table active (première entrée `0x99f194`, littéraux `0xe5440` et `0x137bc8`),
ainsi qu’aux autres références exactes de leur préimage pour éviter les copies
anglaises. Les tables historiques `0x4886e8` et `0x904000` n’ont plus de référence
de base. Quatre descriptions (Ice Punch, Ice Beam, Blizzard, Growth) ne sont plus
les valeurs du résumé actuel et n’ont pas de consommateur actif établi : elles
sont des **exceptions**, sans ajout au combined ni écriture du finaliseur. L’audit
indique les anciens pointeurs et les nouvelles descriptions (frostbite, effet
collectif de Blizzard, double hausse de Growth). Ces remplacements sont hors lot
et ne sont pas modifiés. Leur traduction n’est pas revendiquée.

Les noms Trainer Tower appartiennent aux blocs référencés par `0x4827b4` ; le
code atteint cette table via le littéral `0x15dd24`. L’audit indique le bloc et ses
cellules de référence pour chaque nom/métadonnée. Les neuf occurrences non alignées
de `0x08480618` (KADEN) se trouvent dans du code : elles ne sont jamais repointées.
Les préimages des noms et des huit faux textes binaires sont vérifiées intactes
après build.

## Contrats vérifiés

L’audit versionné `languages/pt/data/pt18_audit.json` contient, offset par offset,
EN exporté, anglais ROM, comparaison FR, préimage hexadécimale, références source,
route canonique, décision, PT et taille encodée. Les ruptures FE/FA/FB et les
commandes FC/FD/F7/F8 sont contrôlées dans leur ordre exact, arguments inclus.

Les descriptions conservent le nombre de lignes original (au plus cinq) avec
122 px par ligne ; les messages restent dans 224 px, sur les cinq vraies polices.
Les tests développent les noms et types variables à leur taille maximale. L’en-tête
du tableau de troc garde les positions FC 13 (60, 110, 198) et chaque libellé tient
dans sa colonne. Le patch est testé sur la ROM réelle : idempotence, écritures
bornées, échec atomique sur préimage erronée, absence de chevauchement, et octets
exacts à toutes les cibles du build final.

## Bilan exhaustif

Le détail binaire et les justifications complètes se trouvent dans le JSON ;
`—` dans la colonne cible indique une conservation brute ou une exception sans
consommateur texte. Une exception de remplissage indique la chaîne de remplacement.

| Offset du manifeste | Décision | Cible/consommateur | Justification |
| --- | --- | --- | --- |
| `0x4586f8` | traduit / vérifié | `0x4586f8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458722` | exception justifiée | `0x458724` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458724 du même lot. Seule cette chaîne est traduite  |
| `0x458724` | traduit / vérifié | `0x458724` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458799` | exception justifiée | `0x45879c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x45879c du même lot. Seule cette chaîne est traduite  |
| `0x45879c` | traduit / vérifié | `0x45879c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4587d7` | exception justifiée | `0x4587d8` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x4587d8 du même lot. Seule cette chaîne est traduite  |
| `0x4587d8` | traduit / vérifié | `0x4587d8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4587fb` | exception justifiée | `0x4587fc` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x4587fc du même lot. Seule cette chaîne est traduite  |
| `0x4587fc` | traduit / vérifié | `0x4587fc` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458828` | traduit / vérifié | `0x458828` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45884c` | traduit / vérifié | `0x45884c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458868` | traduit / vérifié | `0x458868` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458896` | exception justifiée | `0x458898` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458898 du même lot. Seule cette chaîne est traduite  |
| `0x458898` | traduit / vérifié | `0x458898` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458915` | exception justifiée | `0x458918` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458918 du même lot. Seule cette chaîne est traduite  |
| `0x458918` | traduit / vérifié | `0x458918` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45893a` | exception justifiée | `0x45893c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x45893c du même lot. Seule cette chaîne est traduite  |
| `0x45893c` | traduit / vérifié | `0x45893c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45897b` | exception justifiée | `0x45897c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x45897c du même lot. Seule cette chaîne est traduite  |
| `0x45897c` | traduit / vérifié | `0x45897c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4589e3` | exception justifiée | `0x4589e4` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x4589e4 du même lot. Seule cette chaîne est traduite  |
| `0x4589e4` | traduit / vérifié | `0x4589e4` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458a22` | exception justifiée | `0x458a24` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458a24 du même lot. Seule cette chaîne est traduite  |
| `0x458a24` | traduit / vérifié | `0x458a24` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458a44` | traduit / vérifié | `0x458a44` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458a98` | traduit / vérifié | `0x458a98` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458ab7` | exception justifiée | `0x458ab8` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458ab8 du même lot. Seule cette chaîne est traduite  |
| `0x458ab8` | traduit / vérifié | `0x458ab8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458b41` | exception justifiée | `0x458b44` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458b44 du même lot. Seule cette chaîne est traduite  |
| `0x458b44` | traduit / vérifié | `0x458b44` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458cd3` | exception justifiée | `0x458cd4` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458cd4 du même lot. Seule cette chaîne est traduite  |
| `0x458cd4` | traduit / vérifié | `0x458cd4` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458d19` | exception justifiée | `0x458d1c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458d1c du même lot. Seule cette chaîne est traduite  |
| `0x458d1c` | traduit / vérifié | `0x458d1c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458d52` | exception justifiée | `0x458d54` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458d54 du même lot. Seule cette chaîne est traduite  |
| `0x458d54` | traduit / vérifié | `0x458d54` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458d75` | exception justifiée | `0x458d78` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458d78 du même lot. Seule cette chaîne est traduite  |
| `0x458d78` | traduit / vérifié | `0x458d78` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458d9a` | exception justifiée | `0x458d9c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458d9c du même lot. Seule cette chaîne est traduite  |
| `0x458d9c` | traduit / vérifié | `0x458d9c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458dba` | exception justifiée | `0x458dbc` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458dbc du même lot. Seule cette chaîne est traduite  |
| `0x458dbc` | traduit / vérifié | `0x458dbc` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458de7` | exception justifiée | `0x458de8` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458de8 du même lot. Seule cette chaîne est traduite  |
| `0x458de8` | traduit / vérifié | `0x458de8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458e0d` | exception justifiée | `0x458e10` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458e10 du même lot. Seule cette chaîne est traduite  |
| `0x458e10` | traduit / vérifié | `0x458e10` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458e6e` | exception justifiée | `0x458e70` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458e70 du même lot. Seule cette chaîne est traduite  |
| `0x458e70` | traduit / vérifié | `0x458e70` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458ed0` | traduit / vérifié | `0x458ed0` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458f01` | exception justifiée | `0x458f04` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458f04 du même lot. Seule cette chaîne est traduite  |
| `0x458f04` | traduit / vérifié | `0x458f04` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458f2a` | exception justifiée | `0x458f2c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458f2c du même lot. Seule cette chaîne est traduite  |
| `0x458f2c` | traduit / vérifié | `0x458f2c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458f5f` | exception justifiée | `0x458f60` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458f60 du même lot. Seule cette chaîne est traduite  |
| `0x458f60` | traduit / vérifié | `0x458f60` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458fbc` | traduit / vérifié | `0x458fbc` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458fc6` | traduit / vérifié | `0x458fc8` | Entrée du manifeste commençant dans le remplissage  |
| `0x458fe3` | exception justifiée | `0x458fe4` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x458fe4 du même lot. Seule cette chaîne est traduite  |
| `0x458fe4` | traduit / vérifié | `0x458fe4` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x458ffd` | exception justifiée | `0x459000` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459000 du même lot. Seule cette chaîne est traduite  |
| `0x459000` | traduit / vérifié | `0x459000` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45902d` | exception justifiée | `0x459030` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459030 du même lot. Seule cette chaîne est traduite  |
| `0x459030` | traduit / vérifié | `0x459030` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45905d` | exception justifiée | `0x459060` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459060 du même lot. Seule cette chaîne est traduite  |
| `0x459060` | traduit / vérifié | `0x459060` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45908d` | exception justifiée | `0x459090` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459090 du même lot. Seule cette chaîne est traduite  |
| `0x459090` | traduit / vérifié | `0x459090` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4590b9` | exception justifiée | `0x4590bc` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x4590bc du même lot. Seule cette chaîne est traduite  |
| `0x4590bc` | traduit / vérifié | `0x4590bc` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4590f3` | exception justifiée | `0x4590f4` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x4590f4 du même lot. Seule cette chaîne est traduite  |
| `0x4590f4` | traduit / vérifié | `0x4590f4` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45912a` | exception justifiée | `0x45912c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x45912c du même lot. Seule cette chaîne est traduite  |
| `0x45912c` | traduit / vérifié | `0x45912c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45915e` | exception justifiée | `0x459160` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459160 du même lot. Seule cette chaîne est traduite  |
| `0x459160` | traduit / vérifié | `0x459160` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459187` | exception justifiée | `0x459188` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459188 du même lot. Seule cette chaîne est traduite  |
| `0x459188` | traduit / vérifié | `0x459188` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459235` | traduit / vérifié | `0x459238` | Entrée du manifeste commençant dans le remplissage  |
| `0x459250` | traduit / vérifié | `0x459250` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45928c` | traduit / vérifié | `0x45928c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4592e8` | traduit / vérifié | `0x4592e8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459311` | exception justifiée | `0x459314` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459314 du même lot. Seule cette chaîne est traduite  |
| `0x459314` | traduit / vérifié | `0x459314` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45934b` | traduit / vérifié | `0x45934c` | Entrée du manifeste commençant dans le remplissage  |
| `0x459351` | traduit / vérifié | `0x459354` | Entrée du manifeste commençant dans le remplissage  |
| `0x45935e` | traduit / vérifié | `0x459360` | Entrée du manifeste commençant dans le remplissage  |
| `0x459365` | traduit / vérifié | `0x459368` | Entrée du manifeste commençant dans le remplissage  |
| `0x45936d` | traduit / vérifié | `0x459370` | Entrée du manifeste commençant dans le remplissage  |
| `0x459375` | exception justifiée | `0x459378` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459378 du même lot. Seule cette chaîne est traduite  |
| `0x459378` | traduit / vérifié | `0x459378` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459394` | traduit / vérifié | `0x459394` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4593a2` | traduit / vérifié | `0x4593a4` | Entrée du manifeste commençant dans le remplissage  |
| `0x4593b2` | traduit / vérifié | `0x4593b4` | Entrée du manifeste commençant dans le remplissage  |
| `0x4593c1` | traduit / vérifié | `0x4593c4` | Entrée du manifeste commençant dans le remplissage  |
| `0x4593d3` | traduit / vérifié | `0x4593d4` | Entrée du manifeste commençant dans le remplissage  |
| `0x4593d9` | traduit / vérifié | `0x4593dc` | Entrée du manifeste commençant dans le remplissage  |
| `0x4593e2` | traduit / vérifié | `0x4593e4` | Entrée du manifeste commençant dans le remplissage  |
| `0x4593f1` | traduit / vérifié | `0x4593f4` | Entrée du manifeste commençant dans le remplissage  |
| `0x459400` | traduit / vérifié | `0x459400` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45940d` | traduit / vérifié | `0x459410` | Entrée du manifeste commençant dans le remplissage  |
| `0x45942a` | traduit / vérifié | `0x45942c` | Entrée du manifeste commençant dans le remplissage  |
| `0x459449` | exception justifiée | `0x45944c` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x45944c du même lot. Seule cette chaîne est traduite  |
| `0x45944c` | traduit / vérifié | `0x45944c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459460` | traduit / vérifié | `0x459460` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459474` | traduit / vérifié | `0x459474` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459488` | traduit / vérifié | `0x459488` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x45949c` | traduit / vérifié | `0x45949c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459541` | exception justifiée | `0x459544` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459544 du même lot. Seule cette chaîne est traduite  |
| `0x459544` | traduit / vérifié | `0x459544` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x459561` | exception justifiée | `0x459564` | Offset de remplissage sans pointeur, doublon de la chaîne vivante 0x459564 du même lot. Seule cette chaîne est traduite  |
| `0x459564` | traduit / vérifié | `0x459564` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4595b0` | traduit / vérifié | `0x4595b0` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x463dbc` | conservé / vérifié | `0x463dbc` | Nature en anglais selon le glossaire F-759. |
| `0x463dc2` | conservé / vérifié | `0x463dc2` | Nature en anglais selon le glossaire F-759. |
| `0x463dc9` | conservé / vérifié | `0x463dc9` | Nature en anglais selon le glossaire F-759. |
| `0x463dcf` | conservé / vérifié | `0x463dcf` | Nature en anglais selon le glossaire F-759. |
| `0x463dd7` | conservé / vérifié | `0x463dd7` | Nature en anglais selon le glossaire F-759. |
| `0x463ddf` | conservé / vérifié | `0x463ddf` | Nature en anglais selon le glossaire F-759. |
| `0x463de4` | conservé / vérifié | `0x463de4` | Nature en anglais selon le glossaire F-759. |
| `0x463deb` | conservé / vérifié | `0x463deb` | Nature en anglais selon le glossaire F-759. |
| `0x463df3` | conservé / vérifié | `0x463df3` | Nature en anglais selon le glossaire F-759. |
| `0x463dfa` | conservé / vérifié | `0x463dfa` | Nature en anglais selon le glossaire F-759. |
| `0x463dfe` | conservé / vérifié | `0x463dfe` | Nature en anglais selon le glossaire F-759. |
| `0x463e04` | conservé / vérifié | `0x463e04` | Nature en anglais selon le glossaire F-759. |
| `0x463e0a` | conservé / vérifié | `0x463e0a` | Nature en anglais selon le glossaire F-759. |
| `0x463e12` | conservé / vérifié | `0x463e12` | Nature en anglais selon le glossaire F-759. |
| `0x463e18` | conservé / vérifié | `0x463e18` | Nature en anglais selon le glossaire F-759. |
| `0x463e1e` | conservé / vérifié | `0x463e1e` | Nature en anglais selon le glossaire F-759. |
| `0x463e25` | conservé / vérifié | `0x463e25` | Nature en anglais selon le glossaire F-759. |
| `0x463e2a` | conservé / vérifié | `0x463e2a` | Nature en anglais selon le glossaire F-759. |
| `0x463e30` | conservé / vérifié | `0x463e30` | Nature en anglais selon le glossaire F-759. |
| `0x463e38` | conservé / vérifié | `0x463e38` | Nature en anglais selon le glossaire F-759. |
| `0x463e3d` | conservé / vérifié | `0x463e3d` | Nature en anglais selon le glossaire F-759. |
| `0x463e42` | conservé / vérifié | `0x463e42` | Nature en anglais selon le glossaire F-759. |
| `0x463e49` | conservé / vérifié | `0x463e49` | Nature en anglais selon le glossaire F-759. |
| `0x463e4f` | conservé / vérifié | `0x463e4f` | Nature en anglais selon le glossaire F-759. |
| `0x463e57` | conservé / vérifié | `0x463e57` | Nature en anglais selon le glossaire F-759. |
| `0x4716b4` | exception justifiée | `—` | Faux texte dans des données non textuelles (FD EC, motifs répétés)  |
| `0x475638` | conservé / vérifié | `0x475638` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47aac1` | conservé / vérifié | `0x47aac1` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47aac7` | conservé / vérifié | `0x47aac7` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47aacd` | conservé / vérifié | `0x47aacd` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47aad3` | conservé / vérifié | `0x47aad3` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47aad9` | conservé / vérifié | `0x47aad9` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47aafd` | conservé / vérifié | `0x47aafd` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47ab03` | conservé / vérifié | `0x47ab03` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47ab09` | conservé / vérifié | `0x47ab09` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47ab0f` | conservé / vérifié | `0x47ab0f` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47ab15` | conservé / vérifié | `0x47ab15` | Alphabet de saisie conservé : les lettres du clavier ne sont pas des mots à traduire. |
| `0x47b7ab` | exception justifiée | `0x47b74c` | Extraction binaire commençant dans les métadonnées d’un Pokémon du Trainer Tower  |
| `0x47b85b` | exception justifiée | `0x47b74c` | Extraction binaire commençant dans les métadonnées d’un Pokémon du Trainer Tower  |
| `0x47b898` | nom propre / vérifié | `0x47b74c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47bc78` | nom propre / vérifié | `0x47bb2c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47c058` | nom propre / vérifié | `0x47bf0c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47c432` | nom propre / vérifié | `0x47c2ec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47c57a` | nom propre / vérifié | `0x47c2ec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47c818` | nom propre / vérifié | `0x47c6cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47c960` | nom propre / vérifié | `0x47c6cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47d798` | nom propre / vérifié | `0x47d64c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47db78` | nom propre / vérifié | `0x47da2c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47df58` | nom propre / vérifié | `0x47de0c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47e277` | exception justifiée | `0x47e1ec` | Extraction binaire commençant dans les métadonnées d’un Pokémon du Trainer Tower  |
| `0x47e338` | nom propre / vérifié | `0x47e1ec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47e480` | nom propre / vérifié | `0x47e1ec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47e718` | nom propre / vérifié | `0x47e5cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47e860` | nom propre / vérifié | `0x47e5cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47edeb` | exception justifiée | `0x47ed8c` | Extraction binaire commençant dans les métadonnées d’un Pokémon du Trainer Tower  |
| `0x47ee9b` | exception justifiée | `0x47ed8c` | Extraction binaire commençant dans les métadonnées d’un Pokémon du Trainer Tower  |
| `0x47f698` | nom propre / vérifié | `0x47f54c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47fa78` | nom propre / vérifié | `0x47f92c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x47fe58` | nom propre / vérifié | `0x47f92c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x480234` | nom propre / vérifié | `0x4800ec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x480380` | nom propre / vérifié | `0x4800ec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x480618` | nom propre / vérifié | `0x4804cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x480760` | nom propre / vérifié | `0x4804cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x4814ab` | exception justifiée | `0x48106c` | Extraction binaire commençant dans les métadonnées d’un Pokémon du Trainer Tower  |
| `0x481598` | nom propre / vérifié | `0x48106c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x481978` | nom propre / vérifié | `0x48182c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x481d58` | nom propre / vérifié | `0x48182c` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x482138` | nom propre / vérifié | `0x481fec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x482280` | nom propre / vérifié | `0x481fec` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x482518` | nom propre / vérifié | `0x4823cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x482660` | nom propre / vérifié | `0x4823cc` | Nom propre de la table fixe Trainer Tower conservé exactement selon F-759, avec son remplissage. Table référencée par le littéral 0x15dd24 → 0x4827b4  |
| `0x482834` | traduit / vérifié | `0x482834` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482874` | traduit / vérifié | `0x482874` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4828bd` | traduit / vérifié | `0x4828bd` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4828ff` | traduit / vérifié | `0x4828ff` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482946` | traduit / vérifié | `0x482946` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482985` | traduit / vérifié | `0x482985` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4829c9` | traduit / vérifié | `0x4829c9` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482a11` | exception justifiée | `0xa37c6f` | Ancienne description remplacée dans la table active du résumé (base 0x99f194, littéraux 0xe5440 et 0x137bc8). Les références historiques listées ne prouvent pas une utilisation actuelle  |
| `0x482a53` | traduit / vérifié | `0x482a53` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482aa0` | traduit / vérifié | `0x482aa0` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482acd` | traduit / vérifié | `0x482acd` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482b00` | traduit / vérifié | `0x482b00` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482b46` | traduit / vérifié | `0x482b46` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482b94` | traduit / vérifié | `0x482b94` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482bd5` | traduit / vérifié | `0x482bd5` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482c16` | traduit / vérifié | `0x482c16` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482c4f` | traduit / vérifié | `0x482c4f` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482c89` | traduit / vérifié | `0x482c89` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482cd3` | traduit / vérifié | `0x482cd3` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482d1d` | traduit / vérifié | `0x482d1d` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482d66` | traduit / vérifié | `0x482d66` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482d96` | traduit / vérifié | `0x482d96` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482dc8` | traduit / vérifié | `0x482dc8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482e08` | traduit / vérifié | `0x482e08` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482e45` | traduit / vérifié | `0x482e45` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482e83` | traduit / vérifié | `0x482e83` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482ecc` | traduit / vérifié | `0x482ecc` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482f0a` | traduit / vérifié | `0x482f0a` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482f4c` | traduit / vérifié | `0x482f4c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482f8f` | traduit / vérifié | `0x482f8f` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x482fd0` | traduit / vérifié | `0x482fd0` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483014` | traduit / vérifié | `0x483014` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48305c` | traduit / vérifié | `0x48305c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4830a2` | traduit / vérifié | `0x4830a2` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4830eb` | traduit / vérifié | `0x4830eb` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483130` | traduit / vérifié | `0x483130` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483178` | traduit / vérifié | `0x483178` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4831bf` | traduit / vérifié | `0x4831bf` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483203` | traduit / vérifié | `0x483203` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483249` | traduit / vérifié | `0x483249` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48328b` | traduit / vérifié | `0x48328b` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4832d2` | traduit / vérifié | `0x4832d2` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483314` | traduit / vérifié | `0x483314` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483358` | traduit / vérifié | `0x483358` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483397` | traduit / vérifié | `0x483397` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4833dc` | traduit / vérifié | `0x4833dc` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483426` | traduit / vérifié | `0x483426` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48346c` | traduit / vérifié | `0x48346c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4834a8` | traduit / vérifié | `0x4834a8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4834ed` | traduit / vérifié | `0x4834ed` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483534` | traduit / vérifié | `0x483534` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483580` | traduit / vérifié | `0x483580` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4835c2` | traduit / vérifié | `0x4835c2` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483606` | traduit / vérifié | `0x483606` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48364b` | traduit / vérifié | `0x48364b` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483693` | traduit / vérifié | `0x483693` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4836d6` | traduit / vérifié | `0x4836d6` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48371f` | exception justifiée | `0xa37cb9` | Ancienne description remplacée dans la table active du résumé (base 0x99f194, littéraux 0xe5440 et 0x137bc8). Les références historiques listées ne prouvent pas une utilisation actuelle  |
| `0x483760` | exception justifiée | `0xa37d02` | Ancienne description remplacée dans la table active du résumé (base 0x99f194, littéraux 0xe5440 et 0x137bc8). Les références historiques listées ne prouvent pas une utilisation actuelle  |
| `0x4837a1` | traduit / vérifié | `0x4837a1` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4837e3` | traduit / vérifié | `0x4837e3` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48382a` | traduit / vérifié | `0x48382a` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48386d` | traduit / vérifié | `0x48386d` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4838b3` | traduit / vérifié | `0x4838b3` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4838ea` | traduit / vérifié | `0x4838ea` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483927` | traduit / vérifié | `0x483927` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48396e` | traduit / vérifié | `0x48396e` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4839ae` | traduit / vérifié | `0x4839ae` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4839f8` | traduit / vérifié | `0x4839f8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483a3a` | traduit / vérifié | `0x483a3a` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483a82` | traduit / vérifié | `0x483a82` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483ac5` | traduit / vérifié | `0x483ac5` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483b0c` | traduit / vérifié | `0x483b0c` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483b57` | exception justifiée | `0xa37d4f` | Ancienne description remplacée dans la table active du résumé (base 0x99f194, littéraux 0xe5440 et 0x137bc8). Les références historiques listées ne prouvent pas une utilisation actuelle  |
| `0x483b94` | traduit / vérifié | `0x483b94` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483bda` | traduit / vérifié | `0x483bda` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483c22` | traduit / vérifié | `0x483c22` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483c5d` | traduit / vérifié | `0x483c5d` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483c9b` | traduit / vérifié | `0x483c9b` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483cdb` | traduit / vérifié | `0x483cdb` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483d24` | traduit / vérifié | `0x483d24` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483d6b` | traduit / vérifié | `0x483d6b` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483db0` | traduit / vérifié | `0x483db0` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483dfe` | traduit / vérifié | `0x483dfe` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483e3e` | traduit / vérifié | `0x483e3e` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483e80` | traduit / vérifié | `0x483e80` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483ec2` | traduit / vérifié | `0x483ec2` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483f03` | traduit / vérifié | `0x483f03` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483f44` | traduit / vérifié | `0x483f44` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483f89` | traduit / vérifié | `0x483f89` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x483fc7` | traduit / vérifié | `0x483fc7` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x48400f` | traduit / vérifié | `0x48400f` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x484058` | traduit / vérifié | `0x484058` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x484098` | traduit / vérifié | `0x484098` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4840df` | traduit / vérifié | `0x4840df` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x484123` | traduit / vérifié | `0x484123` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x484165` | traduit / vérifié | `0x484165` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4841a8` | traduit / vérifié | `0x4841a8` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
| `0x4841e9` | traduit / vérifié | `0x4841e9` | Traduction depuis la ROM EN, confrontée au combined EN et au FR  |
