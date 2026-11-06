# 25 — PT-84 : Battle Frontier, aide et services

## Périmètre et méthode

F-843 couvre exclusivement les 300 offsets explicites PT-84. Les prérequis F-758 et F-759 sont intégrés. Sources : anglais et français au même offset, confrontés aux octets de la ROM anglaise (SHA256 `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`). Le français sert de comparaison, sans reprise de sa nomenclature.

290 entrées sont traduites ou conservées conformément au glossaire (formats compétitifs, noms propres, objets et natures non attestés). Dix entrées sont exclues avec justification ci-dessous. Aucun offset hors lot ni traduction existante n’est supprimé. Chaque ajout possède sa protection exacte.

## Injection et contraintes

Le finaliseur PT-84 réutilise les primitives structurées du dépôt : préimages contrôlées, allocation sans écrasement des cellules voisines, repointage des seuls consommateurs audités, vérification octet par octet et absence de chevauchement. Les tables de choix, musiques, types, natures et Balls restent à leur adresse ; seules leurs cellules de pointeurs sont actualisées. La classe Frontier Brain utilise le mécanisme à pointeur déjà documenté PT-03.

Les paramètres FC/FD/F8 et les commandes FA/FB sont conservés dans leur ordre exact. Les lignes sont mesurées en pixels et les tailles encodées sont consignées dans `languages/pt/data/pt84_audit.json`. Le suffixe intérieur emploie `<0x00>` pour préserver son espace initial malgré le trim des outils. Les deux motifs accidentels dans les instructions Thumb sont restaurés, jamais repointés.

Les aides 0x1f94d38 et 0x1f95425 dépassent le texte fourni dans combined_en : leur traduction couvre la chaîne ROM intégrale jusqu’au terminateur. Les natures intermédiaires entre Hardy, Docile, Serious et Bashful sont hors manifeste et restent intactes.

## Bilan offset par offset

Les références détaillées, préimages et mesures sont versionnées dans le JSON d’audit. « Traduit/vérifié » inclut les noms conservés selon F-759 ; la validation ROM finale est effectuée par `make_patch(source).verify(rom)` après le build.

| Index | Offset | État / justification |
| --- | --- | --- |
| 0 | `0x1f9433e` | Traduit/vérifié |
| 1 | `0x1f9434d` | Traduit/vérifié |
| 2 | `0x1f94360` | Traduit/vérifié |
| 3 | `0x1f9437b` | Traduit/vérifié |
| 4 | `0x1f94386` | Traduit/vérifié |
| 5 | `0x1f94397` | Traduit/vérifié |
| 6 | `0x1f943ae` | Traduit/vérifié |
| 7 | `0x1f943be` | Traduit/vérifié |
| 8 | `0x1f943d0` | Traduit/vérifié |
| 9 | `0x1f943de` | Traduit/vérifié |
| 10 | `0x1f943e7` | Traduit/vérifié |
| 11 | `0x1f943f1` | Traduit/vérifié |
| 12 | `0x1f9440f` | Traduit/vérifié |
| 13 | `0x1f9441d` | Traduit/vérifié |
| 14 | `0x1f94426` | Traduit/vérifié |
| 15 | `0x1f9443e` | Traduit/vérifié |
| 16 | `0x1f94454` | Traduit/vérifié |
| 17 | `0x1f9446a` | Traduit/vérifié |
| 18 | `0x1f94480` | Traduit/vérifié |
| 19 | `0x1f94497` | Traduit/vérifié |
| 20 | `0x1f944ad` | Traduit/vérifié |
| 21 | `0x1f944c3` | Traduit/vérifié |
| 22 | `0x1f944d9` | Traduit/vérifié |
| 23 | `0x1f944e7` | Traduit/vérifié |
| 24 | `0x1f944fa` | Traduit/vérifié |
| 25 | `0x1f94514` | Traduit/vérifié |
| 26 | `0x1f94526` | Traduit/vérifié |
| 27 | `0x1f94536` | Traduit/vérifié |
| 28 | `0x1f94542` | Traduit/vérifié |
| 29 | `0x1f94559` | Traduit/vérifié |
| 30 | `0x1f94569` | Traduit/vérifié |
| 31 | `0x1f94575` | Traduit/vérifié |
| 32 | `0x1f94582` | Traduit/vérifié |
| 33 | `0x1f94597` | Traduit/vérifié |
| 34 | `0x1f945a6` | Traduit/vérifié |
| 35 | `0x1f945b3` | Traduit/vérifié |
| 36 | `0x1f945cf` | Traduit/vérifié |
| 37 | `0x1f945dd` | Traduit/vérifié |
| 38 | `0x1f945ec` | Traduit/vérifié |
| 39 | `0x1f94601` | Traduit/vérifié |
| 40 | `0x1f9460f` | Traduit/vérifié |
| 41 | `0x1f94627` | Traduit/vérifié |
| 42 | `0x1f94635` | Traduit/vérifié |
| 43 | `0x1f9464e` | Traduit/vérifié |
| 44 | `0x1f9465c` | Traduit/vérifié |
| 45 | `0x1f94674` | Traduit/vérifié |
| 46 | `0x1f94680` | Traduit/vérifié |
| 47 | `0x1f9469b` | Exception : Libellé Black Horizon Exec inutilisé : absent des tables musicales 0x1FB3108 et 0x1FB3A84, aucune référence 32 bits à 0x09F9469B dans toute la ROM. |
| 48 | `0x1f946b6` | Traduit/vérifié |
| 49 | `0x1f946d1` | Traduit/vérifié |
| 50 | `0x1f946e8` | Traduit/vérifié |
| 51 | `0x1f946f7` | Traduit/vérifié |
| 52 | `0x1f94706` | Traduit/vérifié |
| 53 | `0x1f94714` | Traduit/vérifié |
| 54 | `0x1f94724` | Traduit/vérifié |
| 55 | `0x1f94732` | Traduit/vérifié |
| 56 | `0x1f94740` | Traduit/vérifié |
| 57 | `0x1f94752` | Traduit/vérifié |
| 58 | `0x1f94768` | Traduit/vérifié |
| 59 | `0x1f94777` | Traduit/vérifié |
| 60 | `0x1f94790` | Traduit/vérifié |
| 61 | `0x1f947a6` | Traduit/vérifié |
| 62 | `0x1f947b7` | Traduit/vérifié |
| 63 | `0x1f947d0` | Traduit/vérifié |
| 64 | `0x1f947df` | Traduit/vérifié |
| 65 | `0x1f947f7` | Traduit/vérifié |
| 66 | `0x1f9480f` | Traduit/vérifié |
| 67 | `0x1f9481e` | Traduit/vérifié |
| 68 | `0x1f94836` | Traduit/vérifié |
| 69 | `0x1f94844` | Traduit/vérifié |
| 70 | `0x1f9485c` | Traduit/vérifié |
| 71 | `0x1f94873` | Traduit/vérifié |
| 72 | `0x1f94887` | Traduit/vérifié |
| 73 | `0x1f9489e` | Traduit/vérifié |
| 74 | `0x1f948b9` | Traduit/vérifié |
| 75 | `0x1f948cb` | Traduit/vérifié |
| 76 | `0x1f948dd` | Traduit/vérifié |
| 77 | `0x1f948f3` | Traduit/vérifié |
| 78 | `0x1f94901` | Traduit/vérifié |
| 79 | `0x1f94909` | Traduit/vérifié |
| 80 | `0x1f94923` | Traduit/vérifié |
| 81 | `0x1f9492b` | Traduit/vérifié |
| 82 | `0x1f94936` | Traduit/vérifié |
| 83 | `0x1f9493d` | Traduit/vérifié |
| 84 | `0x1f94943` | Traduit/vérifié |
| 85 | `0x1f94952` | Traduit/vérifié |
| 86 | `0x1f94957` | Traduit/vérifié |
| 87 | `0x1f94960` | Traduit/vérifié |
| 88 | `0x1f94965` | Traduit/vérifié |
| 89 | `0x1f9496f` | Traduit/vérifié |
| 90 | `0x1f94979` | Traduit/vérifié |
| 91 | `0x1f94981` | Traduit/vérifié |
| 92 | `0x1f9498e` | Traduit/vérifié |
| 93 | `0x1f94993` | Traduit/vérifié |
| 94 | `0x1f9499e` | Traduit/vérifié |
| 95 | `0x1f949a9` | Traduit/vérifié |
| 96 | `0x1f949b1` | Traduit/vérifié |
| 97 | `0x1f949b7` | Traduit/vérifié |
| 98 | `0x1f949c0` | Traduit/vérifié |
| 99 | `0x1f949c6` | Traduit/vérifié |
| 100 | `0x1f949cf` | Traduit/vérifié |
| 101 | `0x1f949d9` | Traduit/vérifié |
| 102 | `0x1f949ec` | Traduit/vérifié |
| 103 | `0x1f949fb` | Exception : Clé d’extraction dans le bourrage 00 précédant 0x1F949FC. Aucune référence à 0x09F949FB ; le seul consommateur 0x1E9FEDE vise 0x09F949FC, couvert séparément par indice 104. |
| 104 | `0x1f949fc` | Traduit/vérifié |
| 105 | `0x1f94a27` | Traduit/vérifié |
| 106 | `0x1f94b70` | Traduit/vérifié |
| 107 | `0x1f94d38` | Traduit/vérifié |
| 108 | `0x1f94fb5` | Traduit/vérifié |
| 109 | `0x1f95134` | Traduit/vérifié |
| 110 | `0x1f95143` | Traduit/vérifié |
| 111 | `0x1f9514b` | Traduit/vérifié |
| 112 | `0x1f95153` | Traduit/vérifié |
| 113 | `0x1f951e4` | Traduit/vérifié |
| 114 | `0x1f95397` | Traduit/vérifié |
| 115 | `0x1f95425` | Traduit/vérifié |
| 116 | `0x1f95630` | Traduit/vérifié |
| 117 | `0x1f95680` | Exception : Ancienne offre désactivée : aucune référence 32 bits au texte. La table vivante à 0x1FB2ED4 contient les offres Ataque, Velocidade, sexe, zéro, chromatique (120,121,122,124) ; les anciennes offres EV/IV/Gigantamax n’y figurent pas. Le pointeur 0x1EA17E9 vise 0x1F9567D (FD0C FF), un tampon dynamique distinct, pas ce texte. |
| 118 | `0x1f9575b` | Exception : Ancienne offre désactivée : aucune référence 32 bits au texte. La table vivante à 0x1FB2ED4 contient les offres Ataque, Velocidade, sexe, zéro, chromatique (120,121,122,124) ; les anciennes offres EV/IV/Gigantamax n’y figurent pas. Le pointeur 0x1EA17E9 vise 0x1F9567D (FD0C FF), un tampon dynamique distinct, pas ce texte. |
| 119 | `0x1f95876` | Exception : Ancienne offre désactivée : aucune référence 32 bits au texte. La table vivante à 0x1FB2ED4 contient les offres Ataque, Velocidade, sexe, zéro, chromatique (120,121,122,124) ; les anciennes offres EV/IV/Gigantamax n’y figurent pas. Le pointeur 0x1EA17E9 vise 0x1F9567D (FD0C FF), un tampon dynamique distinct, pas ce texte. |
| 120 | `0x1f9598e` | Traduit/vérifié |
| 121 | `0x1f95aa2` | Traduit/vérifié |
| 122 | `0x1f95bb5` | Traduit/vérifié |
| 123 | `0x1f95caf` | Exception : Ancienne offre désactivée : aucune référence 32 bits au texte. La table vivante à 0x1FB2ED4 contient les offres Ataque, Velocidade, sexe, zéro, chromatique (120,121,122,124) ; les anciennes offres EV/IV/Gigantamax n’y figurent pas. Le pointeur 0x1EA17E9 vise 0x1F9567D (FD0C FF), un tampon dynamique distinct, pas ce texte. |
| 124 | `0x1f95d8a` | Traduit/vérifié |
| 125 | `0x1f95e53` | Traduit/vérifié |
| 126 | `0x1f95e9d` | Traduit/vérifié |
| 127 | `0x1f95edf` | Traduit/vérifié |
| 128 | `0x1f95f2d` | Traduit/vérifié |
| 129 | `0x1f95f7a` | Traduit/vérifié |
| 130 | `0x1f96006` | Exception : Ancien résultat désactivé : aucune référence 32 bits au texte. La table des résultats à 0x1FB2EE8 contient uniquement 133,134,136,zéro,137. Les résultats EV/IV/Gigantamax ne sont pas utilisés. |
| 131 | `0x1f96051` | Exception : Ancien résultat désactivé : aucune référence 32 bits au texte. La table des résultats à 0x1FB2EE8 contient uniquement 133,134,136,zéro,137. Les résultats EV/IV/Gigantamax ne sont pas utilisés. |
| 132 | `0x1f9609f` | Exception : Ancien résultat désactivé : aucune référence 32 bits au texte. La table des résultats à 0x1FB2EE8 contient uniquement 133,134,136,zéro,137. Les résultats EV/IV/Gigantamax ne sont pas utilisés. |
| 133 | `0x1f9610c` | Traduit/vérifié |
| 134 | `0x1f9617b` | Traduit/vérifié |
| 135 | `0x1f961ec` | Exception : Ancien résultat désactivé : aucune référence 32 bits au texte. La table des résultats à 0x1FB2EE8 contient uniquement 133,134,136,zéro,137. Les résultats EV/IV/Gigantamax ne sont pas utilisés. Le motif visant le suffixe +4 à 0x8BFD71 traverse deux instructions Thumb BL/LDR ; il ne s’agit pas d’un pointeur. |
| 136 | `0x1f96264` | Traduit/vérifié |
| 137 | `0x1f962d0` | Traduit/vérifié |
| 138 | `0x1f96317` | Traduit/vérifié |
| 139 | `0x1f96325` | Traduit/vérifié |
| 140 | `0x1f96333` | Traduit/vérifié |
| 141 | `0x1f96403` | Traduit/vérifié |
| 142 | `0x1f96428` | Traduit/vérifié |
| 143 | `0x1f96464` | Traduit/vérifié |
| 144 | `0x1f9647e` | Traduit/vérifié |
| 145 | `0x1f964d5` | Traduit/vérifié |
| 146 | `0x1f96539` | Traduit/vérifié |
| 147 | `0x1f9658b` | Traduit/vérifié |
| 148 | `0x1f965d4` | Traduit/vérifié |
| 149 | `0x1f9661a` | Traduit/vérifié |
| 150 | `0x1f96698` | Traduit/vérifié |
| 151 | `0x1f966ca` | Traduit/vérifié |
| 152 | `0x1f966d3` | Traduit/vérifié |
| 153 | `0x1f966db` | Traduit/vérifié |
| 154 | `0x1f966e0` | Traduit/vérifié |
| 155 | `0x1f966e8` | Traduit/vérifié |
| 156 | `0x1f966f1` | Traduit/vérifié |
| 157 | `0x1f966f9` | Traduit/vérifié |
| 158 | `0x1f966ff` | Traduit/vérifié |
| 159 | `0x1f967ce` | Traduit/vérifié |
| 160 | `0x1f96812` | Traduit/vérifié |
| 161 | `0x1f968a6` | Traduit/vérifié |
| 162 | `0x1f9694b` | Traduit/vérifié |
| 163 | `0x1f969d1` | Traduit/vérifié |
| 164 | `0x1f96a4a` | Traduit/vérifié |
| 165 | `0x1f96a74` | Traduit/vérifié |
| 166 | `0x1f96adf` | Traduit/vérifié |
| 167 | `0x1f96b5b` | Traduit/vérifié |
| 168 | `0x1f96b83` | Traduit/vérifié |
| 169 | `0x1f96bcc` | Traduit/vérifié |
| 170 | `0x1f96c14` | Traduit/vérifié |
| 171 | `0x1f96c37` | Traduit/vérifié |
| 172 | `0x1f96cbe` | Traduit/vérifié |
| 173 | `0x1f96d0d` | Traduit/vérifié |
| 174 | `0x1f96d16` | Traduit/vérifié |
| 175 | `0x1f96d23` | Traduit/vérifié |
| 176 | `0x1f96d2e` | Traduit/vérifié |
| 177 | `0x1f96d3e` | Traduit/vérifié |
| 178 | `0x1f96d43` | Traduit/vérifié |
| 179 | `0x1f96e24` | Traduit/vérifié |
| 180 | `0x1f96e48` | Traduit/vérifié |
| 181 | `0x1f96e6e` | Traduit/vérifié |
| 182 | `0x1f96eb8` | Traduit/vérifié |
| 183 | `0x1f96efe` | Traduit/vérifié |
| 184 | `0x1f96f2b` | Traduit/vérifié |
| 185 | `0x1f96f5e` | Traduit/vérifié |
| 186 | `0x1f96f9a` | Traduit/vérifié |
| 187 | `0x1f96fea` | Traduit/vérifié |
| 188 | `0x1f9703a` | Traduit/vérifié |
| 189 | `0x1f9708c` | Traduit/vérifié |
| 190 | `0x1f970d7` | Traduit/vérifié |
| 191 | `0x1f9712f` | Traduit/vérifié |
| 192 | `0x1f9717f` | Traduit/vérifié |
| 193 | `0x1f971bb` | Traduit/vérifié |
| 194 | `0x1f97202` | Traduit/vérifié |
| 195 | `0x1f9721a` | Traduit/vérifié |
| 196 | `0x1f97228` | Traduit/vérifié |
| 197 | `0x1f97233` | Traduit/vérifié |
| 198 | `0x1f97238` | Traduit/vérifié |
| 199 | `0x1f97242` | Traduit/vérifié |
| 200 | `0x1f97251` | Traduit/vérifié |
| 201 | `0x1f97318` | Traduit/vérifié |
| 202 | `0x1f973f6` | Traduit/vérifié |
| 203 | `0x1f97465` | Traduit/vérifié |
| 204 | `0x1f97481` | Traduit/vérifié |
| 205 | `0x1f974b0` | Traduit/vérifié |
| 206 | `0x1f974e1` | Traduit/vérifié |
| 207 | `0x1f97520` | Traduit/vérifié |
| 208 | `0x1f9755a` | Traduit/vérifié |
| 209 | `0x1f9757e` | Traduit/vérifié |
| 210 | `0x1f9762f` | Traduit/vérifié |
| 211 | `0x1f9764e` | Traduit/vérifié |
| 212 | `0x1f97681` | Traduit/vérifié |
| 213 | `0x1f976ef` | Traduit/vérifié |
| 214 | `0x1f97725` | Traduit/vérifié |
| 215 | `0x1f97745` | Traduit/vérifié |
| 216 | `0x1f97781` | Traduit/vérifié |
| 217 | `0x1f9779c` | Traduit/vérifié |
| 218 | `0x1f977d8` | Traduit/vérifié |
| 219 | `0x1f97810` | Traduit/vérifié |
| 220 | `0x1f9781e` | Traduit/vérifié |
| 221 | `0x1f97830` | Traduit/vérifié |
| 222 | `0x1f97837` | Traduit/vérifié |
| 223 | `0x1f97840` | Traduit/vérifié |
| 224 | `0x1f97847` | Traduit/vérifié |
| 225 | `0x1f9784e` | Traduit/vérifié |
| 226 | `0x1f97855` | Traduit/vérifié |
| 227 | `0x1f9785e` | Traduit/vérifié |
| 228 | `0x1f97864` | Traduit/vérifié |
| 229 | `0x1f9786a` | Traduit/vérifié |
| 230 | `0x1f9786f` | Traduit/vérifié |
| 231 | `0x1f97875` | Traduit/vérifié |
| 232 | `0x1f9787b` | Traduit/vérifié |
| 233 | `0x1f97884` | Traduit/vérifié |
| 234 | `0x1f97890` | Traduit/vérifié |
| 235 | `0x1f97897` | Traduit/vérifié |
| 236 | `0x1f9789c` | Traduit/vérifié |
| 237 | `0x1f978a2` | Traduit/vérifié |
| 238 | `0x1f979fd` | Traduit/vérifié |
| 239 | `0x1f97a34` | Traduit/vérifié |
| 240 | `0x1f97a62` | Traduit/vérifié |
| 241 | `0x1f97a97` | Traduit/vérifié |
| 242 | `0x1f97b08` | Traduit/vérifié |
| 243 | `0x1f97b49` | Traduit/vérifié |
| 244 | `0x1f97bd4` | Traduit/vérifié |
| 245 | `0x1f97c23` | Traduit/vérifié |
| 246 | `0x1f97c8c` | Traduit/vérifié |
| 247 | `0x1f97cae` | Traduit/vérifié |
| 248 | `0x1f97d08` | Traduit/vérifié |
| 249 | `0x1f97dba` | Traduit/vérifié |
| 250 | `0x1f97e6a` | Traduit/vérifié |
| 251 | `0x1f97f1a` | Traduit/vérifié |
| 252 | `0x1f97fcf` | Traduit/vérifié |
| 253 | `0x1f97fd6` | Traduit/vérifié |
| 254 | `0x1f980cb` | Traduit/vérifié |
| 255 | `0x1f981c7` | Traduit/vérifié |
| 256 | `0x1f981e1` | Traduit/vérifié |
| 257 | `0x1f9820c` | Traduit/vérifié |
| 258 | `0x1f98232` | Traduit/vérifié |
| 259 | `0x1f98276` | Traduit/vérifié |
| 260 | `0x1f98284` | Traduit/vérifié |
| 261 | `0x1f982ae` | Traduit/vérifié |
| 262 | `0x1f982f0` | Traduit/vérifié |
| 263 | `0x1f98307` | Traduit/vérifié |
| 264 | `0x1f9835e` | Traduit/vérifié |
| 265 | `0x1f9836a` | Traduit/vérifié |
| 266 | `0x1f98375` | Traduit/vérifié |
| 267 | `0x1f98380` | Traduit/vérifié |
| 268 | `0x1f9838a` | Traduit/vérifié |
| 269 | `0x1f98396` | Traduit/vérifié |
| 270 | `0x1f9839f` | Traduit/vérifié |
| 271 | `0x1f983a9` | Traduit/vérifié |
| 272 | `0x1f983b3` | Traduit/vérifié |
| 273 | `0x1f983bf` | Traduit/vérifié |
| 274 | `0x1f983ca` | Traduit/vérifié |
| 275 | `0x1f983d6` | Traduit/vérifié |
| 276 | `0x1f983e3` | Traduit/vérifié |
| 277 | `0x1f983ed` | Traduit/vérifié |
| 278 | `0x1f983f7` | Traduit/vérifié |
| 279 | `0x1f98402` | Traduit/vérifié |
| 280 | `0x1f9840f` | Traduit/vérifié |
| 281 | `0x1f98419` | Traduit/vérifié |
| 282 | `0x1f98423` | Traduit/vérifié |
| 283 | `0x1f9842e` | Traduit/vérifié |
| 284 | `0x1f98438` | Traduit/vérifié |
| 285 | `0x1f98443` | Traduit/vérifié |
| 286 | `0x1f9844d` | Traduit/vérifié |
| 287 | `0x1f98459` | Traduit/vérifié |
| 288 | `0x1f98463` | Traduit/vérifié |
| 289 | `0x1f9846e` | Traduit/vérifié |
| 290 | `0x1f98479` | Traduit/vérifié |
| 291 | `0x1f98484` | Traduit/vérifié |
| 292 | `0x1f98559` | Traduit/vérifié |
| 293 | `0x1f98574` | Traduit/vérifié |
| 294 | `0x1f9858f` | Traduit/vérifié |
| 295 | `0x1f985d2` | Traduit/vérifié |
| 296 | `0x1f9861d` | Traduit/vérifié |
| 297 | `0x1f98643` | Traduit/vérifié |
| 298 | `0x1f98674` | Traduit/vérifié |
| 299 | `0x1f9869a` | Traduit/vérifié |

## Validation

Les résultats exécutés et la preuve Playwright hors écran sont joints au bilan du ticket. La sonde utilise une copie temporaire de la ROM construite et ses véritables pointeurs ; aucune sauvegarde en jeu ni capture n’est versionnée.

## Non vérifié

Le parcours manuel complet de Battle Frontier et chaque combinaison de Pokémon, attributs et montants dynamiques ne sont pas rejoués. Les tests vérifient les commandes, les tampons positionnels, les pages, les budgets et tous les consommateurs du lot ; la preuve visuelle porte sur deux dialogues de services.
