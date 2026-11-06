# ES-008 — Racines du fragment 0x3FE865

La clé contractuelle `0x3FE865` pointe à l'intérieur de `00 DD E7 FF`
(« is » précédé d'un espace), dont le début est `0x3FE864`. Le seul pointeur
absolu vers ce début est le littéral `0xE674C` ; aucun ne vise la clé intérieure.

Le consommateur `0xE6740` charge ce littéral, puis `0xE6744` appelle
`StringAppend` (`0x8DA4`) vers le tampon `0x02021CD0`. La routine propriétaire
`0xE6648–0xE677F` examine les six membres de l'équipe (stride 100 octets),
construit une liste d'espèces depuis la table terminée par FFFF à `0x4020C4`
et sélectionne une terminaison selon le nombre d'espèces. Cette table contient
151, 150, 250, 249, 251, 404, 405, 406, 409 et 410. Les deux terminaisons,
`0x3FE860` et `0x3FE864`, sont identiques dans la source actuelle.
Ce fragment concerne donc une liste d'éligibilité d'équipe, pas une attaque.

## Absence de racine exécutable

Le test `tests/unit/test_es008_dead_party_routine.py` examine la ROM source et
la ROM produite par `make build-es-maint`. Il exige les préimages du corps,
des littéraux et de la table, puis recherche :

- Les adresses absolues vers toute instruction du corps, à tout alignement,
  avec les miroirs ROM 08/0A : aucune racine de code ; deux motifs de ressources
  classifiés ci-dessous.
- Les BL, B et Bcc Thumb externes vers toute instruction du corps : aucun.
- Les ADR Thumb externes pouvant produire une adresse intérieure : aucun.
- Les branches ARM : un seul motif, dans un texte, classifié ci-dessous.
- L'accès séquentiel : la fonction précédente revient par `bx r0` à `0xE663E`,
  avant son pool de littéraux ; aucune chute vers `0xE6648`.

| Motif trouvé | Qualification vérifiée |
|---|---|
| `0x63A700 → 080E66AB` | Données d'un échantillon m4a compressé type 1, en-tête `0x63A398` (`1, 10764288, 0, 6018`), référencé par l'instrument `0x19EAC94`. Le motif est dans le corps de l'échantillon, même en comptant une demi-taille compressée. |
| `0xBEE198 → 080E664A` | Données du bloc LZ77 `0xBEDC3C`, longueur compressée `0x1826`, longueur décompressée 12 000 octets. |
| ARM `0x96CC7C → 0xE6774` | Octets du texte « Bright light… », pas une instruction ARM. |

La routine suivante commence à `0xE678C`. Ses appels ne constituent pas des
racines de `0xE6648`. La ROM communautaire espagnole présente également zéro
BL et zéro adresse absolue vers l'entrée `0xE6648/0xE6649`.

## Conclusion et portée

Cette branche n'est plus consommée dans la ROM examinée. Aucune traduction
isolée, aucun alias d'injection et aucun patch de production ne sont nécessaires
pour `0x3FE865`. F-858 doit conserver la clé dans son bilan avec cette exclusion
motivée ; il ne doit pas revendiquer une phrase espagnole affichée pour elle.

La preuve est propre au code et aux ressources contrôlés ici, et non un postulat
sur une future version de la ROM. Les tests échouent si une racine statique
apparaît, si les préimages changent ou si un motif cesse d'appartenir aux données
classifiées. Le diagnostic des deux autres clés relève du rapport moteur commun.
