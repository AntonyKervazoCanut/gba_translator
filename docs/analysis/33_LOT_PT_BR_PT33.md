# PT-33 — histoire, missions et combat CFRU

F-792, prérequis F-758 et F-759 intégrés. Le domaine réel couvre l’histoire
de Borrius, Frozen Heights, Dresco Town, Mission HQ, Looker, les Sky Battles,
les messages de combat CFRU et des descriptions de mouvements historiques.
Il ne s’agit pas uniquement de noms de zones.

Le manifeste explicite comporte 288 clés : **260 traductions, trois noms
internationaux conservés et 25 exceptions**. Les 263 lignes ajoutées sont
protégées exactement ; aucun offset hors PT-33 ni aucune traduction antérieure
n’est modifié. `languages/pt/data/pt33_audit.json` donne, dans l’ordre du
manifeste, EN, comparaison FR, préimage ROM complète, références et contexte,
texte PT, longueur encodée, largeurs, décision et justification.

## Livraison et contrats

Le finaliseur PT seul réutilise `BorriusTextPatch` : validation des préimages,
des commandes et de tous leurs arguments, ordre des tampons, conservation des
pages FA/FB, relocalisation transactionnelle et validation des cibles. Les
retours FE peuvent être repositionnés pour le budget. Les deux introductions
conservent leurs lignes vides et l’écran introductif suivant ses trois lignes.
Les dialogues utilisent 192 pixels estimés et 208 pixels mesurés, le combat
224 pixels. Les cinq polices sont mesurées dans la ROM avec noms adverses de
dix W, Habilités de dix-sept W et objets de treize W (cellules gItems de
14 octets, terminateur compris). Sp. Atk/Sp. Def restent des libellés anglais
compacts lorsque les noms complets avec tampons longs déborderaient ; aucune
abréviation de statistique canonique inventée. Les marqueurs +/++ indiquent
les hausses normales/fortes et « máx. » l’Attaque maximale.

Les sources extraites 0x8cf0e4 et 0x8d0933 sont tronquées. La ROM contient
respectivement 729 et 883 octets : leur fin complète est traduite et les
commandes sont vérifiées jusqu’au terminateur. Les pronoms de 0x8cdd6c
viennent de PT-22 déjà intégré : aucun changement de ces autres offsets.
Les titres centrés gardent leurs espaces via des protections `expected_raw`.

## Ancienne table de descriptions : absence de livraison revendiquée

La table 0x904000 ne possède aucun référent vers sa base ni son premier
élément 0x904004. Le moteur utilise la table moderne commençant à 0x99f194,
visée par les littéraux 0xe5440, 0x137bc8 et 0x9f3b64. Les dix descriptions
0x920xxx ont des équivalents vivants 0xa37xxx–0xa38xxx, dont l’offset, le
mouvement, le pointeur et la préimage sont documentés dans l’audit. Ces
équivalents appartiennent à d’autres lots ; ils ne sont pas modifiés ici.
Les dix descriptions de la table ancienne et leurs sept clés de remplissage
sont donc des exceptions, pas des traductions prétendument injectées.
La proposition PT reste dans l’audit pour faciliter une lecture ultérieure.
Aucune table fixe vivante ne nécessite de patch de texte dans ce lot.

0x920000 possède en plus deux faux référents : 0x2d692 chevauche deux octets
de bourrage et le littéral Thumb 0x08250892 à 0x2d694 ; 0x440db7 est un motif
dans des tuiles et références graphiques compressées. Ces sites et l’ancienne
table restent intacts. La clé 0x920284 commence dans un octet nul ; le
pointeur 0x90458c vers 0x920285 est lui aussi dans l’ancienne table morte,
et ne prouve donc pas une consommation en jeu.

Les huit autres exceptions sont des copies de messages de combat sans
référence absolue. Leurs consommateurs apparentés sont indiqués sans
revendiquer une identité de paramètres ni modifier les lots correspondants.

## Bilan exhaustif

Les références ci-dessous sont des positions ROM, pas des adresses CPU.
« Exception » signifie aucune traduction/injection revendiquée pour cette clé.
Les sites, préimages et motifs détaillés sont dans l’audit JSON.

| Offset | Décision | Pointeurs / justification |
|---|---|---|
| `0x8bf460` | Traduit et contrôlé | 0x8bf3ee |
| `0x8bf9f0` | Traduit et contrôlé | 0x8bfbaa |
| `0x8c0e2d` | Traduit et contrôlé | 0x8c0de0 |
| `0x8c5720` | Traduit et contrôlé | 0x820a14 |
| `0x8c579e` | Traduit et contrôlé | 0x8c578a |
| `0x8c57b4` | Traduit et contrôlé | 0x8c5773 |
| `0x8c8da0` | Traduit et contrôlé | 0x8c8d45 |
| `0x8c8dd0` | Traduit et contrôlé | 0x8c8d65 |
| `0x8c8e10` | Traduit et contrôlé | 0x8c8d85 |
| `0x8c8ff0` | Traduit et contrôlé | 0x8c8fc8 |
| `0x8c9050` | Traduit et contrôlé | 0x8c919e |
| `0x8c9070` | Traduit et contrôlé | 0x8c91c5 |
| `0x8c976e` | Traduit et contrôlé | 0x8c9710 |
| `0x8c9a17` | Traduit et contrôlé | 0x8c99d6 |
| `0x8c9a4c` | Traduit et contrôlé | 0x8c99d0 |
| `0x8ca5e0` | Traduit et contrôlé | 0x8ca5b7 |
| `0x8ca6c5` | Traduit et contrôlé | 0x8ca65e |
| `0x8ca792` | Traduit et contrôlé | 0x8ca671 |
| `0x8ca7ef` | Traduit et contrôlé | 0x8ca67c |
| `0x8ca8c3` | Traduit et contrôlé | 0x8ca693 |
| `0x8caa11` | Traduit et contrôlé | 0x8ca6a0 |
| `0x8caa4a` | Traduit et contrôlé | 0x8ca6a8 |
| `0x8caf31` | Traduit et contrôlé | 0x8cad7e |
| `0x8caf99` | Traduit et contrôlé | 0x8cad87 |
| `0x8caffd` | Traduit et contrôlé | 0x8cade4 |
| `0x8cb023` | Traduit et contrôlé | 0x8cadee |
| `0x8cb03c` | Traduit et contrôlé | 0x8cadfd |
| `0x8cb0ff` | Traduit et contrôlé | 0x8cad90 |
| `0x8cb14b` | Traduit et contrôlé | 0x8cad97 |
| `0x8cb199` | Traduit et contrôlé | 0x8cae1d |
| `0x8cb1fd` | Traduit et contrôlé | 0x8cae36 |
| `0x8cb260` | Traduit et contrôlé | 0x8cae70 |
| `0x8cb3f5` | Traduit et contrôlé | 0x8cae8d |
| `0x8cb47b` | Traduit et contrôlé | 0x8caea6 |
| `0x8cb5a8` | Traduit et contrôlé | 0x8caeb0 |
| `0x8cb5d3` | Traduit et contrôlé | 0x8caecb |
| `0x8cb66f` | Traduit et contrôlé | 0x8caed8 |
| `0x8cb695` | Traduit et contrôlé | 0x8caeef |
| `0x8cb6f7` | Traduit et contrôlé | 0x8caf0b |
| `0x8cb773` | Traduit et contrôlé | 0x8caf24 |
| `0x8cb82c` | Traduit et contrôlé | 0x8cadae |
| `0x8cb872` | Traduit et contrôlé | 0x8cadb7 |
| `0x8cb932` | Traduit et contrôlé | 0x8cadc0 |
| `0x8cba7a` | Traduit et contrôlé | 0x8cadc9 |
| `0x8cbaec` | Traduit et contrôlé | 0x8cadd2 |
| `0x8cbb58` | Traduit et contrôlé | 0x8caddb |
| `0x8cc387` | Traduit et contrôlé | 0x8cbe3a |
| `0x8cc391` | Traduit et contrôlé | 0x8cbe65 |
| `0x8cc43b` | Traduit et contrôlé | 0x8cbe97 |
| `0x8cc49c` | Traduit et contrôlé | 0x8cbecf |
| `0x8cc55b` | Traduit et contrôlé | 0x8cbf03 |
| `0x8cc605` | Traduit et contrôlé | 0x8cbf42 |
| `0x8cc6e1` | Traduit et contrôlé | 0x8cbf67 |
| `0x8cc752` | Traduit et contrôlé | 0x8cbf9f |
| `0x8cc850` | Traduit et contrôlé | 0x8cc01c |
| `0x8cc8db` | Traduit et contrôlé | 0x8cc044 |
| `0x8cc8f9` | Traduit et contrôlé | 0x8cc076 |
| `0x8cc9b2` | Traduit et contrôlé | 0x8cc093 |
| `0x8cca05` | Nom conservé et contrôlé | 0x8cc0b9 |
| `0x8cca10` | Nom conservé et contrôlé | 0x8cc0e0 |
| `0x8cca18` | Nom conservé et contrôlé | 0x8cc10a |
| `0x8cca21` | Traduit et contrôlé | 0x8cc12d |
| `0x8ccaac` | Traduit et contrôlé | 0x8cc164 |
| `0x8ccad3` | Traduit et contrôlé | 0x8cc19f |
| `0x8ccb3e` | Traduit et contrôlé | 0x8cc1e1 |
| `0x8ccba6` | Traduit et contrôlé | 0x8cc1b9 |
| `0x8ccbbf` | Traduit et contrôlé | 0x8cc330 |
| `0x8ccce0` | Traduit et contrôlé | 0x8ccc02 |
| `0x8ccd09` | Traduit et contrôlé | 0x8ccc27 |
| `0x8ccd61` | Traduit et contrôlé | 0x8ccc3f |
| `0x8ccdd2` | Traduit et contrôlé | 0x8ccc54 |
| `0x8ccdf4` | Traduit et contrôlé | 0x8ccc7d |
| `0x8ccdff` | Traduit et contrôlé | 0x8ccc92 |
| `0x8cd03d` | Traduit et contrôlé | 0x8ccf18 |
| `0x8cd093` | Traduit et contrôlé | 0x8ccf2d |
| `0x8cd10e` | Traduit et contrôlé | 0x8ccf46 |
| `0x8cd15f` | Traduit et contrôlé | 0x8ccf9a |
| `0x8cd194` | Traduit et contrôlé | 0x8ccfe6 |
| `0x8cd1a5` | Traduit et contrôlé | 0x8cd016 |
| `0x8cd1b2` | Traduit et contrôlé | 0x8cd02b |
| `0x8cd5fc` | Traduit et contrôlé | 0x8cd371 |
| `0x8cd6a6` | Traduit et contrôlé | 0x8cd588 |
| `0x8cd70a` | Traduit et contrôlé | 0x8cd384 |
| `0x8cd8a6` | Traduit et contrôlé | 0x8cd3a1 |
| `0x8cd8be` | Traduit et contrôlé | 0x8cd3d4 |
| `0x8cd8dc` | Traduit et contrôlé | 0x8cd3e6 |
| `0x8cd935` | Traduit et contrôlé | 0x8cd3f8 |
| `0x8cd9d8` | Traduit et contrôlé | 0x8cd40a |
| `0x8cd9fc` | Traduit et contrôlé | 0x8cd41c |
| `0x8cda59` | Traduit et contrôlé | 0x8cd42e |
| `0x8cda75` | Traduit et contrôlé | 0x8cd480 |
| `0x8cdad4` | Traduit et contrôlé | 0x8cd492 |
| `0x8cdb97` | Traduit et contrôlé | 0x8cd4a4 |
| `0x8cdc07` | Traduit et contrôlé | 0x8cd4b6 |
| `0x8cdc55` | Traduit et contrôlé | 0x8cd4dc |
| `0x8cdcd3` | Traduit et contrôlé | 0x8cd505 |
| `0x8cdd6c` | Traduit et contrôlé | 0x8cd517 |
| `0x8cddd0` | Traduit et contrôlé | 0x8cd522 |
| `0x8cde49` | Traduit et contrôlé | 0x8cd5a3 |
| `0x8cdebb` | Traduit et contrôlé | 0x8cd5b0 |
| `0x8cdf4b` | Traduit et contrôlé | 0x8cd5bd |
| `0x8ce03c` | Traduit et contrôlé | 0x8cd5ca |
| `0x8ce0c8` | Traduit et contrôlé | 0x8cd5d7 |
| `0x8ce141` | Traduit et contrôlé | 0x8cd5e4 |
| `0x8ce1df` | Traduit et contrôlé | 0x8cd5f1 |
| `0x8ce1f8` | Traduit et contrôlé | 0x8cd595 |
| `0x8ce1fc` | Traduit et contrôlé | 0x8cd59c |
| `0x8ce9cb` | Traduit et contrôlé | 0x8ce507 |
| `0x8cea72` | Traduit et contrôlé | 0x8ce543 |
| `0x8ceac2` | Traduit et contrôlé | 0x8ce55c |
| `0x8cead9` | Traduit et contrôlé | 0x8ce592, 0x8ce6f6 |
| `0x8ceaf0` | Traduit et contrôlé | 0x8ce5b9, 0x8ce659, 0x8ce71d, 0x8ce7b3 |
| `0x8ceb09` | Traduit et contrôlé | 0x8ce5e0, 0x8ce623, 0x8ce680, 0x8ce6b6, 0x8ce744, 0x8ce77d, 0x8ce7da, 0x8ce810 |
| `0x8ceb24` | Traduit et contrôlé | 0x8ce939 |
| `0x8ceb4c` | Traduit et contrôlé | 0x8ce94b |
| `0x8ceb5d` | Traduit et contrôlé | 0x8ce983 |
| `0x8cefb1` | Traduit et contrôlé | 0x8ced47 |
| `0x8cf025` | Traduit et contrôlé | 0x8ced7f |
| `0x8cf09d` | Traduit et contrôlé | 0x8ced86 |
| `0x8cf0e4` | Traduit et contrôlé | 0x8ced6a |
| `0x8cf3bd` | Traduit et contrôlé | 0x8cefa6 |
| `0x8cf3fb` | Traduit et contrôlé | 0x8ceda7, 0x8cedf8, 0x8cef08, 0x8cef78 |
| `0x8cf44a` | Traduit et contrôlé | 0x8ced3a |
| `0x8cf4cb` | Traduit et contrôlé | 0x8cee18 |
| `0x8cf4de` | Traduit et contrôlé | 0x8ceee1 |
| `0x8cf522` | Traduit et contrôlé | 0x8ced96 |
| `0x8cf52b` | Traduit et contrôlé | 0x8cede7 |
| `0x8cf53a` | Traduit et contrôlé | 0x8ceef7 |
| `0x8cf554` | Traduit et contrôlé | 0x8cef67 |
| `0x8d072f` | Traduit et contrôlé | 0x8d05d0 |
| `0x8d0906` | Traduit et contrôlé | 0x8d0614 |
| `0x8d0933` | Traduit et contrôlé | 0x8d0626 |
| `0x8d0ca6` | Traduit et contrôlé | 0x8d0646 |
| `0x8d0d33` | Traduit et contrôlé | 0x8d065f |
| `0x8d0d5f` | Traduit et contrôlé | 0x8d0671 |
| `0x8d0e55` | Traduit et contrôlé | 0x8d0683 |
| `0x8d0f02` | Traduit et contrôlé | 0x8d0695 |
| `0x8d0f8a` | Traduit et contrôlé | 0x8d06b1 |
| `0x8d1043` | Traduit et contrôlé | 0x8d06eb |
| `0x8d1651` | Traduit et contrôlé | 0x8d1558 |
| `0x8d1726` | Traduit et contrôlé | 0x8d157b |
| `0x8d1757` | Traduit et contrôlé | 0x8d158f |
| `0x8d1777` | Traduit et contrôlé | 0x8d15a7 |
| `0x8d17db` | Traduit et contrôlé | 0x8d1646 |
| `0x8d1826` | Traduit et contrôlé | 0x8d15f6 |
| `0x8d184b` | Traduit et contrôlé | 0x8d161d |
| `0x905690` | Traduit et contrôlé | 0x905572 |
| `0x9056b4` | Traduit et contrôlé | 0x905736 |
| `0x905770` | Traduit et contrôlé | 0x905605 |
| `0x905a30` | Traduit et contrôlé | 0x8bd531, 0x8bd5c5, 0x905ab5 |
| `0x905a50` | Traduit et contrôlé | 0x8bd560, 0x8bd58f, 0x8bd5ee, 0x905b04, 0x905b45 |
| `0x905c25` | Traduit et contrôlé | 0x905c12 |
| `0x905c40` | Traduit et contrôlé | 0x905cc3 |
| `0x905e9a` | Traduit et contrôlé | 0x90e62a |
| `0x906470` | Traduit et contrôlé | 0x906450 |
| `0x9064a0` | Traduit et contrôlé | 0x90643d |
| `0x906520` | Traduit et contrôlé | 0x8c3211, 0x8c323b, 0x8c3265, 0x8c3299, 0x8c32bf, 0x90650e |
| `0x906540` | Traduit et contrôlé | 0x907160 |
| `0x906619` | Traduit et contrôlé | 0x906610 |
| `0x9066d0` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa4aeff via 0x3fe148 |
| `0x906740` | Traduit et contrôlé | 0x9067d5 |
| `0x906810` | Traduit et contrôlé | 0x905978, 0x9059a4, 0x906604 |
| `0x9068a0` | Traduit et contrôlé | 0x906608 |
| `0x9068e0` | Traduit et contrôlé | 0x90660c |
| `0x906b90` | Traduit et contrôlé | 0x906b62 |
| `0x906bf0` | Traduit et contrôlé | 0x906614 |
| `0x906c20` | Traduit et contrôlé | 0x90e7d6 |
| `0x906c40` | Traduit et contrôlé | 0x90e7eb |
| `0x906d20` | Traduit et contrôlé | 0x906d13 |
| `0x906d70` | Traduit et contrôlé | 0x906d53 |
| `0x906dd0` | Traduit et contrôlé | 0x906db9 |
| `0x906e20` | Traduit et contrôlé | 0x906e03 |
| `0x906e70` | Traduit et contrôlé | 0x906e53 |
| `0x906f60` | Traduit et contrôlé | 0x906f43 |
| `0x906fb0` | Traduit et contrôlé | 0x906f93 |
| `0x906fe0` | Traduit et contrôlé | 0x8b67e7, 0x9070dd |
| `0x907000` | Traduit et contrôlé | 0x906ea3 |
| `0x907070` | Traduit et contrôlé | 0x8b7188, 0x907053, 0x90ffa8 |
| `0x907250` | Traduit et contrôlé | 0x90723f |
| `0x907310` | Traduit et contrôlé | 0x9072ff |
| `0x9073e0` | Traduit et contrôlé | 0x9073cf |
| `0x9074d0` | Traduit et contrôlé | 0x9074bf, 0x9076a0, 0x9081a9 |
| `0x9075e0` | Traduit et contrôlé | 0x90758f |
| `0x907600` | Traduit et contrôlé | 0x9075c8 |
| `0x907730` | Traduit et contrôlé | 0x9076f6 |
| `0x907860` | Traduit et contrôlé | 0x907839 |
| `0x907bf0` | Traduit et contrôlé | 0x907b9c |
| `0x907c40` | Traduit et contrôlé | 0x907c23 |
| `0x907de5` | Traduit et contrôlé | 0x907dd6 |
| `0x9082a0` | Traduit et contrôlé | 0x908133 |
| `0x9085a0` | Traduit et contrôlé | 0x90537f |
| `0x9089e0` | Traduit et contrôlé | 0x9089a7 |
| `0x908a00` | Traduit et contrôlé | 0x9089c4 |
| `0x908cdb` | Traduit et contrôlé | 0x908c6d |
| `0x908cf9` | Traduit et contrôlé | 0x908c7b |
| `0x9092d0` | Traduit et contrôlé | 0x909106 |
| `0x9092f0` | Traduit et contrôlé | 0x909125 |
| `0x909311` | Traduit et contrôlé | 0x909144 |
| `0x909330` | Traduit et contrôlé | 0x909165 |
| `0x909351` | Traduit et contrôlé | 0x909184 |
| `0x909372` | Traduit et contrôlé | 0x9091a3 |
| `0x909394` | Traduit et contrôlé | 0x9091c2 |
| `0x9093b9` | Traduit et contrôlé | 0x9091e1 |
| `0x9093d9` | Traduit et contrôlé | 0x909200 |
| `0x9093fa` | Traduit et contrôlé | 0x90921f |
| `0x909419` | Traduit et contrôlé | 0x90923e |
| `0x90943a` | Traduit et contrôlé | 0x90925d |
| `0x90945b` | Traduit et contrôlé | 0x90927c |
| `0x90947d` | Traduit et contrôlé | 0x90929b |
| `0x909af0` | Traduit et contrôlé | 0x909a1f |
| `0x909bf0` | Traduit et contrôlé | 0x909bcb |
| `0x909d00` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa43f03 via 0x96d666 |
| `0x909d20` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa43f8f via 0x3fe188 |
| `0x909d5f` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa43def via 0xa6b9e4 |
| `0x909d90` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa43dbe via 0xa6b9e8 |
| `0x90a718` | Traduit et contrôlé | 0x90a6d6 |
| `0x90a740` | Traduit et contrôlé | 0x90a704 |
| `0x90a7a0` | Traduit et contrôlé | 0x90a6ed |
| `0x90a9c0` | Traduit et contrôlé | 0x90a9a6 |
| `0x90b2a0` | Traduit et contrôlé | 0x271b00 |
| `0x90b780` | Traduit et contrôlé | 0x8a9ab8, 0x90b751, 0x90e660 |
| `0x90c710` | Traduit et contrôlé | 0x90c6df |
| `0x90c802` | Traduit et contrôlé | 0x90c7e9 |
| `0x90c827` | Traduit et contrôlé | 0x90cc49 |
| `0x90c850` | Traduit et contrôlé | 0x271c34 |
| `0x90cae0` | Traduit et contrôlé | 0x271b98 |
| `0x90cc62` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0x908cf9 via 0x908c7b |
| `0x90cf46` | Traduit et contrôlé | 0x90cead |
| `0x90d120` | Traduit et contrôlé | 0x90cfcb |
| `0x90d160` | Traduit et contrôlé | 0x90cfe4 |
| `0x90d2c0` | Traduit et contrôlé | 0x8b6787, 0x90d1c0 |
| `0x90d3f0` | Traduit et contrôlé | 0x8b6735, 0x90d303 |
| `0x90d430` | Traduit et contrôlé | 0x8b674e, 0x90d31c |
| `0x90d780` | Traduit et contrôlé | 0x8b6a98, 0x908678, 0x908ab7 |
| `0x90d930` | Traduit et contrôlé | 0x90d8fd |
| `0x90d9b0` | Traduit et contrôlé | 0x90d993 |
| `0x90db70` | Traduit et contrôlé | 0x90d769 |
| `0x90dc60` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa4af18 via 0x3fe068 |
| `0x90dd30` | Traduit et contrôlé | 0x90dd1b |
| `0x90e0d0` | Exception justifiée | Aucun pointeur ; copie non référencée, apparenté 0xa43f8f via 0x3fe188 |
| `0x90e100` | Traduit et contrôlé | 0x90e046 |
| `0x90e130` | Traduit et contrôlé | 0x90e08e |
| `0x90e400` | Traduit et contrôlé | 0x90ad2c |
| `0x90e940` | Traduit et contrôlé | 0x9052af |
| `0x90ea30` | Traduit et contrôlé | 0x90ea12 |
| `0x90eaa0` | Traduit et contrôlé | 0x90eb03 |
| `0x90ef70` | Traduit et contrôlé | 0x90ef60 |
| `0x90f3a0` | Traduit et contrôlé | 0x90f45c |
| `0x90f530` | Traduit et contrôlé | 0x8bcb1e |
| `0x90f560` | Traduit et contrôlé | 0x90f7cb |
| `0x90f580` | Traduit et contrôlé | 0x90f708 |
| `0x90f5a0` | Traduit et contrôlé | 0x90f78e |
| `0x90f5f0` | Traduit et contrôlé | 0x90f74b |
| `0x90f640` | Traduit et contrôlé | 0x90f822 |
| `0x90f670` | Traduit et contrôlé | 0x90f8a2, 0x90f8d7 |
| `0x90f8f0` | Traduit et contrôlé | 0x90fb64 |
| `0x90f920` | Traduit et contrôlé | 0x90fb68 |
| `0x90f960` | Traduit et contrôlé | 0x90fb6c |
| `0x90f9a0` | Traduit et contrôlé | 0x90fb70 |
| `0x90f9c0` | Traduit et contrôlé | 0x90fb74 |
| `0x90f9f0` | Traduit et contrôlé | 0x90fb7c |
| `0x90fa20` | Traduit et contrôlé | 0x90fb78 |
| `0x90fc0b` | Traduit et contrôlé | 0x90fe44 |
| `0x90fc30` | Traduit et contrôlé | 0x90fe48 |
| `0x90fc60` | Traduit et contrôlé | 0x90fe4c |
| `0x90fc80` | Traduit et contrôlé | 0x90fe50 |
| `0x90fcb0` | Traduit et contrôlé | 0x90fe54 |
| `0x90fcf0` | Traduit et contrôlé | 0x90fe58 |
| `0x90fd30` | Traduit et contrôlé | 0x8bb95f |
| `0x90fd50` | Traduit et contrôlé | 0x8bb9dc, 0x8bba14, 0x8bba4c |
| `0x9100b0` | Traduit et contrôlé | 0x90f4a7 |
| `0x920000` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa38422 via 0x99f768 |
| `0x920045` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa37f8d via 0x99f728 |
| `0x92008f` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x920090 via 0x904598 |
| `0x920090` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa37fd7 via 0x99f72c |
| `0x9200d2` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x9200d3 via 0x9045a0 |
| `0x9200d3` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa38061 via 0x99f734 |
| `0x92011d` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x92011e via 0x9045a4 |
| `0x92011e` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa380ab via 0x99f738 |
| `0x920167` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x920168 via 0x9045a8 |
| `0x920168` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa380f4 via 0x99f73c |
| `0x9201ad` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x9201ae via 0x9045ac |
| `0x9201ae` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa38139 via 0x99f740 |
| `0x9201f8` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x9201f9 via 0x9045b0 |
| `0x9201f9` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa38183 via 0x99f744 |
| `0x92023e` | Exception justifiée | Aucun pointeur ; remplissage, cible ancienne 0x92023f via 0x9045b8 |
| `0x92023f` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa38215 via 0x99f74c |
| `0x920284` | Exception justifiée | Ancienne table sans consommateur ; cible moderne 0xa37f07 via 0x99f720 |

## Validation

Les résultats de build, tests ROM et Playwright sont consignés après exécution.
La sonde visuelle appelle la vraie msgbox sur une copie temporaire de ROM, à
partir des pointeurs finaux des missions, du Bird Keeper et du combat. Elle
contrôle par OCR les premières lignes et l’absence de modification du fichier
de sauvegarde, puis Playwright capture les trois états vérifiés hors dépôt.
Elle ne prétend pas parcourir toutes les pages ni certifier le jeu complet.
