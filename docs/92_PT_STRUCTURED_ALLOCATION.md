# PT-BR : supprimer les copies intermédiaires des textes structurés

## Diagnostic B-1034

Sur la base intégrant les 88 lots, la ROM partielle avant PT-86 ne possède
plus qu'un bloc libre : `0xB4C9CD`, longueur 13 867 octets. Les textes restant
à allouer nécessitent 14 816 octets pour PT-86 et 9 229 pour PT-87, hors
préparateurs. Cette ROM partielle n'est pas une livraison validée.

Le problème n'est pas uniquement la fragmentation. La normalisation générique
rééquilibre les lignes ; les finaliseurs rétablissent ensuite les traductions
verbatim. Pour PT-86/87, respectivement 89/43 chaînes divergentes tiennent dans
leur cellule source (14 670/8 731 octets). Les réallouer au finaliseur consomme
donc de l'espace inutilement. Réemployer une cible déjà exacte parmi les
lecteurs n'économise que 66 octets à ce stade.

## Contrat de propriété

`structured_text_patches` déclare dans `lang.yaml` les finaliseurs qui fournissent
les octets canoniques avant le build générique. PT active cette optimisation
pour PT-83 à PT-88 ; les autres langues gardent leur chemin existant.

`StructuredTextRoutes` réutilise `make_patch(source)` et `entries()` : validation
des préimages, commandes, budgets et lecteurs par les mêmes objets qui finalisent
la ROM. Un scan des pointeurs non alignés exige que chaque occurrence source soit
soit un lecteur audité, soit une référence non textuelle déjà classifiée dans le
manifeste. Deux propriétaires ne peuvent pas réclamer le même lecteur.

Le JSON générique reçoit les `raw_bytes` canoniques et les pointeurs audités.
`SmartReinserter` conserve son allocation best-fit et sa déduplication existantes.
Les écritures en place sont bornées à la préimage, avec zéro padding disponible ;
la troncature et le fallback sont interdits pour ces cellules. La passe inline
reçoit uniquement le sous-ensemble canonique à protéger, afin de ne pas
renormaliser ces cellules. Les autres traductions suivent le chemin antérieur.

Tous les finaliseurs restent exécutés. Le contrôle final exige leurs traductions
intégrales aux pointeurs vivants et l'absence de chevauchement entre finaliseurs.
Les deux titres PT-87 et son possessif contextuel restent traités par leur patch.

Aucune région nouvelle n'est réclamée. `MIN_FREE_RUN`, `RUN_MARGIN`, les exclusions
moteur et les réservations espagnoles ne changent pas. Aucune copie prétendument
morte n'est effacée et aucun fichier `combined` n'est modifié.

## Régressions couvertes

Les tests unitaires couvrent le JSON immuable/idempotent, les bornes, les
propriétaires concurrents, la présence obligatoire des finaliseurs, l'activation
PT seule et la protection sélective de la passe inline.

`tests/e2e/pt/test_structured_allocation_rom.py` utilise la ROM source réelle :
il sature exclusivement les blocs autorisés, injecte une traduction canonique,
exécute la passe inline puis le finaliseur sans nouvelle allocation, et compare
tous les octets hors cellule (PCM/code/graphismes compris). Il vérifie aussi le
rollback intégral en cas de saturation, les préimages invalides, un lecteur
inconnu, les pointeurs hors bornes et l'idempotence.

La preuve visuelle finale de F-846 reste dans le périmètre de ce ticket parent.

## Résultats mesurés

Le build complet des 88 lots réussit. Le contrôle commun valide 1 761 cellules
et 2 672 lecteurs. PT-83/84/85/88 ne relocalisent plus de texte au finaliseur ;
PT-86/87 en relocalisent respectivement 1/3. Il reste un bloc autorisé de
65 092 octets après PT-87, sans modifier les limites de l'allocateur.

Les tests ROM PT-83 à PT-88 et de pression passent : 34 tests, dont les
7 tests officiels de `test_batch_pt87_rom.py`. Les 11 tests ciblés de routage
et de pression passent également.

La passe générique signale deux chaînes hors budget (`0x1FA1EF5`, `0x1FA91BD`)
que son heuristique de pointeurs ne reloge pas. Leurs finaliseurs stricts les
livrent intégralement ; les tests ROM vérifient leurs lecteurs finaux. Il ne
s'agit pas de traductions abandonnées. Les fallbacks génériques passent de
10 à 8 ; aucun n'est autorisé sur les cellules canoniques routées.

Deux builds PT complets successifs produisent le même SHA256 :
`dbd465155173ba676a2f5963ca742097c4860a755e567282bc2b498342d6b1eb`.
Les rebuilds IT et DE réussissent également. Le build FR de référence conserve
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.

La suite `make test-python` termine sans échec : 9 605 tests réussis,
3 tests ignorés par leurs conditions existantes (pont émulateur, garde FD,
CSV dynamique ES absent). Les hooks exécutent également 9 464 tests rapides
réussis et 80 tests Vitest ; aucun test n'a été désactivé par ce correctif.
