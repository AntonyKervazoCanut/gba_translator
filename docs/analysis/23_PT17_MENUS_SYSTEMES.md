# PT-17 — Pokédex, décorations et communication sans fil

F-776. Prérequis F-758/F-759 intégrés. Le manifeste ferme le périmètre à 281 offsets : 210 traductions et 71 exceptions. La source textuelle EN contient des valeurs françaises et des chaînes tronquées ; les octets de la ROM anglaise et la table vivante ont priorité pour identifier le sens. La comparaison FR sert uniquement de référence secondaire.

Les noms d’espèces, de mouvements et les noms propres non attestés en PT-BR sont conservés. Les notes musicales sont localisées (dó à si). Les dialogues utilisent movimento, Treinador et Cartão de Treinador. Chaque traduction possède une protection exacte.

`languages/pt/data/pt17_audit.json` contient les préimages, le SHA256 source, les sites de pointeurs, les budgets et les décisions individuelles. Le finaliseur `batch_17` réutilise StructuredTextPatch : contrôle des préimages, allocation distincte des cellules, repointage de tous les consommateurs validés, contrôle des octets finaux et des chevauchements. Il ne réécrit aucune table de noms hors lot.

Les descriptions de décorations sont référencées dans une table fixe à stride 32 ; seuls les pointeurs descriptifs sont remplacés, jamais les noms, prix ou données graphiques. Le faux pointeur 0xCBA129 vers 0x454D13 est exclu. Le faux pointeur graphique 0x1DCCF22 vers 0x45817E est également exclu. À 0x458314, le code charge une table de choix de textes, pas un texte ; ses deux pointeurs doivent rester des pointeurs.

Budgets de rendu : police moteur 2, 112 pixels pour les descriptions de décorations, 224 pour les descriptions Pokédex et dialogues. Les variables et commandes sont contrôlées dans leur ordre binaire ; FA/FB/FE sont conservés exactement. La longueur des données relocalisées inclut le terminateur et n’est pas limitée par la taille de l’ancienne cellule.

## Bilan offset par offset

| Offset | Décision | Pointeurs source validés | Justification |
|---|---|---|---|
| `0x44dec7` | traduit / à vérifier en ROM | 0x1a38b9c | Texte vivant ; table Pokédex. |
| `0x44df35` | traduit / à vérifier en ROM | 0x1a38bc0 | Texte vivant ; table Pokédex. |
| `0x44df9d` | traduit / à vérifier en ROM | 0x1a38be4 | Texte vivant ; table Pokédex. |
| `0x44e000` | traduit / à vérifier en ROM | 0x1a38c08 | Texte vivant ; table Pokédex. |
| `0x44e063` | traduit / à vérifier en ROM | 0x1a38c2c | Texte vivant ; table Pokédex. |
| `0x44e0db` | traduit / à vérifier en ROM | 0x1a38c50 | Texte vivant ; table Pokédex. |
| `0x44e13e` | traduit / à vérifier en ROM | 0x1a38c74 | Texte vivant ; table Pokédex. |
| `0x44e199` | traduit / à vérifier en ROM | 0x1a38c98 | Texte vivant ; table Pokédex. |
| `0x44e1f1` | traduit / à vérifier en ROM | 0x1a38cbc | Texte vivant ; table Pokédex. |
| `0x44e25d` | traduit / à vérifier en ROM | 0x1a38ce0 | Texte vivant ; table Pokédex. |
| `0x44e2cc` | traduit / à vérifier en ROM | 0x1a38d04 | Texte vivant ; table Pokédex. |
| `0x44e334` | traduit / à vérifier en ROM | 0x1a38d28 | Texte vivant ; table Pokédex. |
| `0x44e3a5` | traduit / à vérifier en ROM | 0x1a38d4c | Texte vivant ; table Pokédex. |
| `0x44e406` | traduit / à vérifier en ROM | 0x1a38d70 | Texte vivant ; table Pokédex. |
| `0x44e477` | traduit / à vérifier en ROM | 0x1a38d94 | Texte vivant ; table Pokédex. |
| `0x44e4dd` | traduit / à vérifier en ROM | 0x1a38db8 | Texte vivant ; table Pokédex. |
| `0x44e535` | traduit / à vérifier en ROM | 0x1a38ddc | Texte vivant ; table Pokédex. |
| `0x44e594` | traduit / à vérifier en ROM | 0x1a38e00 | Texte vivant ; table Pokédex. |
| `0x44e5f5` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e65d` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e6c2` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e6cc` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e6d7` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e6df` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e6f9` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e703` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e71c` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e785` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x44e7e6` | exception | aucun pointeur texte | Ancienne description Pokédex ou suffixe extrait au milieu du texte ; zéro référence vers cet offset. La table Pokédex vivante utilise d’autres cellules ; aucune injection de ce doublon mort. |
| `0x452fcb` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x453010` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x454254` | traduit / à vérifier en ROM | 0x455750 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454284` | traduit / à vérifier en ROM | 0x455770 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4542bc` | traduit / à vérifier en ROM | 0x455790 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4542f3` | traduit / à vérifier en ROM | 0x4557b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45432c` | traduit / à vérifier en ROM | 0x4557d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454362` | traduit / à vérifier en ROM | 0x4557f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454398` | traduit / à vérifier en ROM | 0x455810 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4543d1` | traduit / à vérifier en ROM | 0x455830 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454404` | traduit / à vérifier en ROM | 0x455850 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454420` | traduit / à vérifier en ROM | 0x455870 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454451` | traduit / à vérifier en ROM | 0x455890 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45446e` | traduit / à vérifier en ROM | 0x4558b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45448b` | traduit / à vérifier en ROM | 0x4558d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4544a9` | traduit / à vérifier en ROM | 0x4558f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4544c5` | traduit / à vérifier en ROM | 0x455910 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4544e2` | traduit / à vérifier en ROM | 0x455930 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4544fe` | traduit / à vérifier en ROM | 0x455950 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45451a` | traduit / à vérifier en ROM | 0x455970 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454534` | traduit / à vérifier en ROM | 0x455990 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454559` | traduit / à vérifier en ROM | 0x4559b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454570` | traduit / à vérifier en ROM | 0x4559d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454598` | traduit / à vérifier en ROM | 0x4559f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4545c6` | traduit / à vérifier en ROM | 0x455a10 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4545ee` | traduit / à vérifier en ROM | 0x455a30 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454625` | traduit / à vérifier en ROM | 0x455a50 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45465a` | traduit / à vérifier en ROM | 0x455a70 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45468d` | traduit / à vérifier en ROM | 0x455a90 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4546c4` | traduit / à vérifier en ROM | 0x455ab0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4546fc` | traduit / à vérifier en ROM | 0x455ad0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454734` | traduit / à vérifier en ROM | 0x455af0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45475e` | traduit / à vérifier en ROM | 0x455b10 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454789` | traduit / à vérifier en ROM | 0x455b30 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4547b7` | traduit / à vérifier en ROM | 0x455b50 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4547dc` | traduit / à vérifier en ROM | 0x455b70 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4547ff` | traduit / à vérifier en ROM | 0x455b90 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454822` | traduit / à vérifier en ROM | 0x455bb0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454857` | traduit / à vérifier en ROM | 0x455bd0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454874` | traduit / à vérifier en ROM | 0x455bf0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4548a1` | traduit / à vérifier en ROM | 0x455c10 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4548d2` | traduit / à vérifier en ROM | 0x455c30 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454901` | traduit / à vérifier en ROM | 0x455c50 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454933` | traduit / à vérifier en ROM | 0x455c70 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454966` | traduit / à vérifier en ROM | 0x455c90 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45499f` | traduit / à vérifier en ROM | 0x455cb0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4549be` | traduit / à vérifier en ROM | 0x455cd0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4549e9` | traduit / à vérifier en ROM | 0x455cf0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454a14` | traduit / à vérifier en ROM | 0x455d10 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454a3c` | traduit / à vérifier en ROM | 0x455d30 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454a6a` | traduit / à vérifier en ROM | 0x455d50 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454a99` | traduit / à vérifier en ROM | 0x455d70 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454ac8` | traduit / à vérifier en ROM | 0x455d90 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454af3` | traduit / à vérifier en ROM | 0x455db0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454b1f` | traduit / à vérifier en ROM | 0x455dd0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454b4b` | traduit / à vérifier en ROM | 0x455df0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454b76` | traduit / à vérifier en ROM | 0x455e10 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454ba2` | traduit / à vérifier en ROM | 0x455e30 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454bcd` | traduit / à vérifier en ROM | 0x455e50 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454bfd` | traduit / à vérifier en ROM | 0x455e70 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454c31` | traduit / à vérifier en ROM | 0x455e90 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454c68` | traduit / à vérifier en ROM | 0x455eb0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454ca2` | traduit / à vérifier en ROM | 0x455ed0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454cdb` | traduit / à vérifier en ROM | 0x455ef0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454d13` | traduit / à vérifier en ROM | 0x455f10 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454d4a` | traduit / à vérifier en ROM | 0x455f30 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454d80` | traduit / à vérifier en ROM | 0x455f50 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454da8` | traduit / à vérifier en ROM | 0x455f70 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454dcd` | traduit / à vérifier en ROM | 0x455f90 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454df2` | traduit / à vérifier en ROM | 0x455fb0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454e16` | traduit / à vérifier en ROM | 0x455fd0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454e3c` | traduit / à vérifier en ROM | 0x455ff0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454e6b` | traduit / à vérifier en ROM | 0x456010 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454e90` | traduit / à vérifier en ROM | 0x456030 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454eb7` | traduit / à vérifier en ROM | 0x456050 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454edc` | traduit / à vérifier en ROM | 0x456070 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454f02` | traduit / à vérifier en ROM | 0x456090 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454f2d` | traduit / à vérifier en ROM | 0x4560b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454f5a` | traduit / à vérifier en ROM | 0x4560d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454f86` | traduit / à vérifier en ROM | 0x4560f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454fb2` | traduit / à vérifier en ROM | 0x456110 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x454fe1` | traduit / à vérifier en ROM | 0x456130 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455010` | traduit / à vérifier en ROM | 0x456150 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45503e` | traduit / à vérifier en ROM | 0x456170 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45506e` | traduit / à vérifier en ROM | 0x456190 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45509a` | traduit / à vérifier en ROM | 0x4561b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4550c8` | traduit / à vérifier en ROM | 0x4561d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4550f3` | traduit / à vérifier en ROM | 0x4561f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455121` | traduit / à vérifier en ROM | 0x456210 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45514e` | traduit / à vérifier en ROM | 0x456230 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45517b` | traduit / à vérifier en ROM | 0x456250 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4551a7` | traduit / à vérifier en ROM | 0x456270 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4551d4` | traduit / à vérifier en ROM | 0x456290 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455200` | traduit / à vérifier en ROM | 0x4562b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45522c` | traduit / à vérifier en ROM | 0x4562d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455259` | traduit / à vérifier en ROM | 0x4562f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455287` | traduit / à vérifier en ROM | 0x456310 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4552b3` | traduit / à vérifier en ROM | 0x456330 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4552df` | traduit / à vérifier en ROM | 0x456350 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45530b` | traduit / à vérifier en ROM | 0x456370 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455336` | traduit / à vérifier en ROM | 0x456390 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455362` | traduit / à vérifier en ROM | 0x4563b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455392` | traduit / à vérifier en ROM | 0x4563d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4553c1` | traduit / à vérifier en ROM | 0x4563f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4553f2` | traduit / à vérifier en ROM | 0x456410 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455424` | traduit / à vérifier en ROM | 0x456430 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455453` | traduit / à vérifier en ROM | 0x456450 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455483` | traduit / à vérifier en ROM | 0x456470 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4554b0` | traduit / à vérifier en ROM | 0x456490 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4554e3` | traduit / à vérifier en ROM | 0x4564b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455515` | traduit / à vérifier en ROM | 0x4564d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455548` | traduit / à vérifier en ROM | 0x4564f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455573` | traduit / à vérifier en ROM | 0x456510 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45559e` | traduit / à vérifier en ROM | 0x456530 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4555c9` | traduit / à vérifier en ROM | 0x456550 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4555f4` | traduit / à vérifier en ROM | 0x456570 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45561f` | traduit / à vérifier en ROM | 0x456590 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x45564a` | traduit / à vérifier en ROM | 0x4565b0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x455675` | traduit / à vérifier en ROM | 0x4565d0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4556a0` | traduit / à vérifier en ROM | 0x4565f0 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4556cb` | traduit / à vérifier en ROM | 0x456610 | Description de décoration ; cellule de pointeur fixe, texte relocalisable. |
| `0x4556f6` | exception | aucun pointeur texte | Deux octets de padding puis identifiant 0 de la table fixe à 0x4556F8 (littéral 0x14C). Le nom SMALL DESK commence à 0x4556F9, hors lot ; 0x4556F6 n’est pas une chaîne consommée. Ne pas écraser le début de table. |
| `0x4566c8` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x4566e8` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x456708` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x456728` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x45687c` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x45689c` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x4568bc` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x4568dc` | exception | aucun pointeur texte | Données binaires graphiques interprétées à tort comme du texte ; zéro pointeur texte, aucune injection. |
| `0x4571b7` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4571b8` | traduit / à vérifier en ROM | 0x117e44, 0x118264 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4571de` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4571e0` | traduit / à vérifier en ROM | 0x1185b0 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457231` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457264` | traduit / à vérifier en ROM | 0x115cac | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4573c5` | traduit / à vérifier en ROM | 0x457444, 0x457468 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4573d7` | traduit / à vérifier en ROM | 0x457440 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4573f4` | traduit / à vérifier en ROM | 0x457430, 0x457458 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457402` | traduit / à vérifier en ROM | 0x45745c, 0x457470 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457410` | traduit / à vérifier en ROM | 0x45744c, 0x457460, 0x457474 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x45741e` | traduit / à vérifier en ROM | 0x457464, 0x457478 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x45749d` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4574a0` | traduit / à vérifier en ROM | 0x1162bc | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4574c1` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4574c4` | traduit / à vérifier en ROM | 0x1162cc | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4574e9` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4574ec` | traduit / à vérifier en ROM | 0x1162dc | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457512` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457514` | traduit / à vérifier en ROM | 0x116054 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x45752e` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457530` | traduit / à vérifier en ROM | 0x1160bc | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457553` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x45756c` | traduit / à vérifier en ROM | 0x45767c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4575a3` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4575a4` | traduit / à vérifier en ROM | 0x457608 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4575dc` | traduit / à vérifier en ROM | 0x45760c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457644` | traduit / à vérifier en ROM | 0x457680, 0x457758 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4576ac` | traduit / à vérifier en ROM | 0x116430, 0x1181e8 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4576c2` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4576c4` | traduit / à vérifier en ROM | 0x116440 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4576ff` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x45771c` | traduit / à vérifier en ROM | 0x116bac | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457731` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457734` | traduit / à vérifier en ROM | 0x457778 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4577b9` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4577bc` | traduit / à vérifier en ROM | 0x1185a4 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4577f5` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4577f8` | traduit / à vérifier en ROM | 0x117c08, 0x45783c, 0x457840 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457824` | traduit / à vérifier en ROM | 0x457850 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457860` | traduit / à vérifier en ROM | 0x457898 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457879` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x45787c` | traduit / à vérifier en ROM | 0x45789c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4578ba` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4578bc` | traduit / à vérifier en ROM | 0x118c24 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457950` | traduit / à vérifier en ROM | 0x457a38 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4579bc` | traduit / à vérifier en ROM | 0x457a3c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457a70` | traduit / à vérifier en ROM | 0x457b08 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457a97` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457a98` | traduit / à vérifier en ROM | 0x457b0c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457ad0` | traduit / à vérifier en ROM | 0x457b10 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457b2a` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457b2c` | traduit / à vérifier en ROM | 0x457b84 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457b4c` | traduit / à vérifier en ROM | 0x457b88, 0x457b8c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457baf` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457bb0` | traduit / à vérifier en ROM | 0x457bd0 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457c00` | traduit / à vérifier en ROM | 0x457c24 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457c47` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457c48` | traduit / à vérifier en ROM | 0x11b084, 0x457e78 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457ca3` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457ca4` | traduit / à vérifier en ROM | 0x11afbc, 0x457e7c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457cf6` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457cf8` | traduit / à vérifier en ROM | 0x11afc4, 0x457e80 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457d44` | traduit / à vérifier en ROM | 0x11b074, 0x457e84 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457db8` | traduit / à vérifier en ROM | 0x11b04c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457e0a` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457e0c` | traduit / à vérifier en ROM | 0x11b0a0 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457e28` | traduit / à vérifier en ROM | 0x116308 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457e41` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457e44` | traduit / à vérifier en ROM | 0x116318 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457e5d` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457e60` | traduit / à vérifier en ROM | 0x1191c0 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457ebd` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457ec0` | traduit / à vérifier en ROM | 0x457f88 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457efd` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457f00` | traduit / à vérifier en ROM | 0x457f84 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457f3c` | traduit / à vérifier en ROM | 0x457f8c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457fb4` | traduit / à vérifier en ROM | 0x4580f4 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x457fe6` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x457fe8` | traduit / à vérifier en ROM | 0x4580f8 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458019` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458053` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458054` | traduit / à vérifier en ROM | 0x458104 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458087` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458088` | traduit / à vérifier en ROM | 0x458108 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4580be` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4580c0` | traduit / à vérifier en ROM | 0x458110 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x45812c` | traduit / à vérifier en ROM | 0x458248 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458161` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458164` | traduit / à vérifier en ROM | 0x45824c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x45817e` | exception | aucun pointeur texte | Coïncidence binaire dans des données graphiques à 0x1dccf22 ; aucun consommateur texte. Le vrai début est 0x458180 (cellule 0x458254), hors lot. |
| `0x4581ad` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4581b0` | traduit / à vérifier en ROM | 0x458258 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4581d6` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4581d8` | traduit / à vérifier en ROM | 0x458238, 0x458244, 0x458250, 0x45825c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4581f6` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4581f8` | traduit / à vérifier en ROM | 0x458230, 0x45823c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458217` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458218` | traduit / à vérifier en ROM | 0x458234, 0x458240 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4582c0` | traduit / à vérifier en ROM | 0x458318 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458314` | exception | aucun pointeur texte | Table de deux pointeurs, pas une chaîne : littéral 0x11AE90 vers la table ; cellules 0x458314→0x458260 et 0x458318→0x4582C0. Le vrai texte de carte commence à 0x45831C (pointeur 0x4583B4), hors lot. Ne pas traduire les octets de pointeur. |
| `0x458369` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x45836c` | traduit / à vérifier en ROM | 0x4583b8 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4583f8` | traduit / à vérifier en ROM | 0x458430 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458479` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x45847c` | traduit / à vérifier en ROM | 0x118d18 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4584c0` | traduit / à vérifier en ROM | 0x119284 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4584fb` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4584fc` | traduit / à vérifier en ROM | 0x458548 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458527` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458528` | traduit / à vérifier en ROM | 0x45854c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458596` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458598` | traduit / à vérifier en ROM | 0x4585ec | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458617` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458618` | traduit / à vérifier en ROM | 0x45875c | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458643` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x458644` | traduit / à vérifier en ROM | 0x458760 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x458668` | traduit / à vérifier en ROM | 0x458764 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x45869f` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4586a0` | traduit / à vérifier en ROM | 0x458768 | Dialogue/choix du système de communication ; commandes conservées. |
| `0x4586cd` | exception | aucun pointeur texte | Aucun pointeur texte vers cet offset ; fragment/padding avant une cellule vivante. Ne pas injecter dans le voisin. |
| `0x4586d0` | traduit / à vérifier en ROM | 0x45876c | Dialogue/choix du système de communication ; commandes conservées. |

Les anciennes copies Deoxys et leurs suffixes n’appartiennent pas à la table Pokédex vivante : 0x1A38E24 pointe à 0x165C254. Les doublons Rayquaza/Jirachi 0x44E71C/0x44E785 sont remplacés dans cette table par 0x44E535/0x44E594, via 0x1A38DDC/0x1A38E00. Ces dernières cellules sont dans le lot et traduites. Poké Ball et Poké Balls restent en anglais conformément au glossaire F-759.
