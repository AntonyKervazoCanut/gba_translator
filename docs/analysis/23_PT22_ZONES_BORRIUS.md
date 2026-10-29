# PT-22 — Zones de Borrius (F-781)

Le manifeste contient exactement 288 offsets : 240 textes vivants traduits ou noms
conservés selon F-759, et 48 exceptions justifiées ci-dessous. Aucun offset d'un autre
lot n'est traduit et aucune traduction existante n'est supprimée.

Les zones réelles comprennent Icicle Cave, Blizzard City, Frost Mountain, les routes
7–14, Crater Town, Frozen Heights, Dresco, Flower Paradise, Epidimy et le port
d'Antisis. Le lot inclut les scènes de Log, du rival, des Shadows, les arbitres de
Ginásio, la collecte de Honey et les ingrédients des tartes.

## Contrat et choix

F-758 et F-759 sont intégrés : tildes 0x60–0x63 et glossaire figé. Les noms de Borrius,
espèces et mouvements non attestés restent anglais ; Potion devient Poção. Les
versions FR aux mêmes offsets ont été comparées, sans reprendre leurs noms de lieux
ni leur nomenclature de mouvements. L'audit JSON conserve les deux références,
les commandes canoniques EN et la préimage binaire de chaque offset.

Les accents imprimés dans combined_en après FC/FD ne représentent pas leurs vrais
arguments : les commandes proviennent exclusivement des octets ROM, dans le même
ordre, avec exactement les mêmes FE/FA/FB. Les fils/filles restent des tampons
runtime, avec une formulation qui ne force pas l'accord masculin.

Le finaliseur local `languages/pt/patches/batch_22.py` utilise le mécanisme partagé
StructuredTextPatch après les réparations et repointages génériques. Il livre les
240 textes aux 297 consommateurs prouvés, sans écraser une cellule voisine. Il prend
aussi en charge les trois descriptions d'objets : table 0x876200, stride 44, champ
pointeur +20. Aucune nouvelle table de noms fixes à patcher n'a été trouvée.

Les descriptions de mouvements 0x780a50–0x78122b sont historiques : leurs pointeurs
éventuels appartiennent à 0x904000 sans racine ; les consommateurs du moteur
0xe5440, 0x137bc8 et 0x9f3b64 lisent la vraie table 0x99f194. Les traduire ici ne
changerait aucun écran et déborderait vers les lots possédant les vrais textes.
0x778eaf est une liste applymovement (04 FE), dont les cinq référents suivent
l'opcode 0x4f ; le dialogue commence à 0x778eb1. Les séquences ressemblant à des
pointeurs pour 0x780119 et 0x78000f sont des instructions ou arguments, pas du texte.

Budgets : 224 pixels par ligne physique de dialogue et 186 pixels sur trois lignes
pour les objets. Le normaliseur partagé mesure une ligne logique incluant les FA :
son plafond multiplie 224 par le nombre de segments ; les tests contrôlent séparément
chaque ligne physique sur les largeurs de la vraie police et les tampons dynamiques.
Les octets encodés (terminateur compris) sont consignés pour chaque texte. Le patch
alloue chaque chaîne entière, contrôle les préimages et les cibles et vérifie l'absence
de chevauchement. Pas de modification de src/core/ ni de script partagé.

## Validation

Contrôles reproductibles : `make build-pt`, puis
`python3 -m pytest tests/e2e/pt/test_batch_pt22_rom.py -m rom` et
`npx playwright test --config tests/e2e-playwright/playwright.pt22.config.ts`.
Les gardes source s'exécutent avec
`python3 -m pytest tests/unit/pt/test_batch_pt22.py tests/unit/test_translation_integrity.py`.
La preuve Playwright appelle
la boîte native depuis deux pointeurs réels de la ROM PT construite, en copie
 temporaire, avec assertions OCR sur le texte brésilien et absence d'anglais.
L'émulateur et Chromium restent hors écran ; aucune sauvegarde de jeu n'est faite.

## Bilan offset par offset

Les pointeurs sont des offsets de cellules dans la ROM EN ; « aucun » indique
zéro référent 32 bits après scan de toute la ROM. Les préimages complètes et tous
les faux sites, y compris les 210 coïncidences de code pour 0x780119, figurent dans
`languages/pt/data/pt22_audit.json`.

| Offset | Statut | Pointeurs EN / justification |
|---|---|---|
| `0x773613` | traduit / vérifié en ROM | `0x772d87` |
| `0x77365a` | traduit / vérifié en ROM | `0x773171` |
| `0x773719` | traduit / vérifié en ROM | `0x7736e8` |
| `0x77373a` | traduit / vérifié en ROM | `0x7736ee` |
| `0x7737c6` | traduit / vérifié en ROM | `0x77379e` |
| `0x7737dd` | traduit / vérifié en ROM | `0x7737a4` |
| `0x77389c` | traduit / vérifié en ROM | `0x744d1e` |
| `0x775b4e` | traduit / vérifié en ROM | `0x775b2e` |
| `0x775b90` | traduit / vérifié en ROM | `0x75cf92` |
| `0x775c06` | traduit / vérifié en ROM | `0x75cfae` |
| `0x775c38` | traduit / vérifié en ROM | `0x75cfb2` |
| `0x775c6a` | traduit / vérifié en ROM | `0x75cff6` |
| `0x775ce2` | traduit / vérifié en ROM | `0x75d143` |
| `0x775d84` | traduit / vérifié en ROM | `0x75d172` |
| `0x775da6` | traduit / vérifié en ROM | `0x75cfd8`, `0x75d20e` |
| `0x775dbe` | traduit / vérifié en ROM | `0x75d227` |
| `0x775df7` | traduit / vérifié en ROM | `0x75d08a` |
| `0x775e6c` | traduit / vérifié en ROM | `0x75d0a6` |
| `0x775e7b` | traduit / vérifié en ROM | `0x75d0d0` |
| `0x775f18` | traduit / vérifié en ROM | `0x75d298` |
| `0x776047` | traduit / vérifié en ROM | `0x76293c`, `0x77263f`, `0x7763a6`, `0x7e9bbf`, `0x7eeafa`, `0x7f9569`, `0x7fa476`, `0x7fb0c6`, `0x7fca50` |
| `0x77607a` | traduit / vérifié en ROM | `0x76ce3c` |
| `0x7760b6` | traduit / vérifié en ROM | `0x776073` |
| `0x7760e3` | traduit / vérifié en ROM | `0x169eb7` |
| `0x7760f8` | traduit / vérifié en ROM | `0x7758fb` |
| `0x776157` | traduit / vérifié en ROM | `0x776146` |
| `0x776197` | traduit / vérifié en ROM | `0x7548b9` |
| `0x77624a` | traduit / vérifié en ROM | `0x776242` |
| `0x7763eb` | traduit / vérifié en ROM | `0x75bac2` |
| `0x776441` | traduit / vérifié en ROM | `0x754f98` |
| `0x77650a` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x776522` | traduit / vérifié en ROM | `0x7764e2` |
| `0x77653d` | traduit / vérifié en ROM | `0x7764e8` |
| `0x7765a0` | traduit / vérifié en ROM | `0x776583` |
| `0x7765b6` | traduit / vérifié en ROM | `0x776589` |
| `0x7765f5` | traduit / vérifié en ROM | `0x7765d4` |
| `0x776623` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x776686` | traduit / vérifié en ROM | `0x753651` |
| `0x77680c` | traduit / vérifié en ROM | `0x776708` |
| `0x776862` | traduit / vérifié en ROM | `0x776793`, `0x7767d9` |
| `0x7768a4` | traduit / vérifié en ROM | `0x75bad4` |
| `0x776af5` | traduit / vérifié en ROM | `0x77649b` |
| `0x776b0e` | traduit / vérifié en ROM | `0x75bb1e` |
| `0x7787f5` | traduit / vérifié en ROM | `0x77631c` |
| `0x778982` | traduit / vérifié en ROM | `0x77632f` |
| `0x7789b9` | traduit / vérifié en ROM | `0x77633b` |
| `0x778a80` | traduit / vérifié en ROM | `0x77635b` |
| `0x778ac2` | traduit / vérifié en ROM | `0x77636a` |
| `0x778ada` | traduit / vérifié en ROM | `0x776374` |
| `0x778b36` | traduit / vérifié en ROM | `0x778b2f` |
| `0x778ba4` | traduit / vérifié en ROM | `0x778b9c` |
| `0x778baf` | traduit / vérifié en ROM | `0x7635f9` |
| `0x778c62` | traduit / vérifié en ROM | `0x763602` |
| `0x778cb6` | traduit / vérifié en ROM | `0x76360b` |
| `0x778d3f` | traduit / vérifié en ROM | `0x76361a` |
| `0x778d57` | traduit / vérifié en ROM | `0x76365f` |
| `0x778df2` | traduit / vérifié en ROM | `0x763672` |
| `0x778e1d` | traduit / vérifié en ROM | `0x76370a` |
| `0x778e4a` | traduit / vérifié en ROM | `0x763724` |
| `0x778eaf` | exception | aucun consommateur texte — Liste de mouvements applymovement, octets 04 FE ; les cinq pointeurs sont arguments de 0x4f (objets 8/14/15/1/2), pas des consommateurs de texte. Le dialogue vivant commence à 0x778eb1. Sites rejetés : 0x7635d7, 0x7635de, 0x7635e5, 0x7636fa, 0x763701. |
| `0x778eb1` | traduit / vérifié en ROM | `0x76386a` |
| `0x778f41` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x778f75` | traduit / vérifié en ROM | `0x7c76fe` |
| `0x779001` | traduit / vérifié en ROM | `0x78a9ff` |
| `0x779090` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x77915e` | traduit / vérifié en ROM | `0x75d2a6` |
| `0x77922b` | traduit / vérifié en ROM | `0x75d29f` |
| `0x779594` | traduit / vérifié en ROM | `0x779329` |
| `0x7795b8` | traduit / vérifié en ROM | `0x77933b` |
| `0x779637` | traduit / vérifié en ROM | `0x77935e` |
| `0x7797cc` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x7797d4` | traduit / vérifié en ROM | `0x779370` |
| `0x779917` | traduit / vérifié en ROM | `0x7798b9` |
| `0x77efc1` | traduit / vérifié en ROM | `0x77efb9` |
| `0x77f003` | traduit / vérifié en ROM | `0x77effb` |
| `0x77f01e` | traduit / vérifié en ROM | `0x77f016` |
| `0x77f05c` | traduit / vérifié en ROM | `0x77f054` |
| `0x77f096` | traduit / vérifié en ROM | `0x77f08c` |
| `0x77f0c4` | exception | aucun consommateur texte — Fausse entrée extraite depuis le bytecode script avant le texte ; aucun référent vers cet offset. Le vrai msgbox et son texte commencent quelques octets plus loin. |
| `0x77f0d0` | traduit / vérifié en ROM | `0x77f0c6` |
| `0x77f113` | traduit / vérifié en ROM | `0x77f109` |
| `0x77f139` | traduit / vérifié en ROM | `0x74b349` |
| `0x77f168` | traduit / vérifié en ROM | `0x77f160` |
| `0x77f198` | traduit / vérifié en ROM | `0x16a993` |
| `0x77f1e3` | traduit / vérifié en ROM | `0x751f3b` |
| `0x77f375` | traduit / vérifié en ROM | `0x751f56` |
| `0x77f3bf` | traduit / vérifié en ROM | `0x7522e7` |
| `0x77f452` | traduit / vérifié en ROM | `0x7522ff` |
| `0x77f4c8` | traduit / vérifié en ROM | `0x751f82` |
| `0x77f52f` | traduit / vérifié en ROM | `0x752744` |
| `0x77f57b` | traduit / vérifié en ROM | `0x751f69` |
| `0x77f57f` | traduit / vérifié en ROM | `0x751f70` |
| `0x77f662` | traduit / vérifié en ROM | `0x745198` |
| `0x77f9ea` | traduit / vérifié en ROM | `0x77f9e0` |
| `0x77fad8` | traduit / vérifié en ROM | `0x77fa89`, `0x77fab0` |
| `0x77faf1` | traduit / vérifié en ROM | `0x77fa9f` |
| `0x77fb6c` | traduit / vérifié en ROM | `0x77fb1f`, `0x77fb46` |
| `0x77fb88` | traduit / vérifié en ROM | `0x77fb35` |
| `0x77fc48` | traduit / vérifié en ROM | `0x77fbcc`, `0x77fbf3` |
| `0x77fc7b` | traduit / vérifié en ROM | `0x77fbe2` |
| `0x77fd9c` | traduit / vérifié en ROM | `0x77fd55`, `0x77fd7c` |
| `0x77fdbd` | traduit / vérifié en ROM | `0x77fd6b` |
| `0x77fe7c` | traduit / vérifié en ROM | `0x77fe08`, `0x77fe2f` |
| `0x77fea2` | traduit / vérifié en ROM | `0x77fe1e` |
| `0x77ff0f` | exception | aucun consommateur texte — Fausse entrée extraite depuis le bytecode script avant le texte ; aucun référent vers cet offset. Le vrai msgbox et son texte commencent quelques octets plus loin. |
| `0x77ff15` | traduit / vérifié en ROM | `0x77ff0d` |
| `0x77ffe5` | traduit / vérifié en ROM | `0x792d97` |
| `0x78000f` | exception | aucun consommateur texte — Suffixe de 0x77ffe5. La seule coïncidence 32 bits à 0x1e93053 chevauche les opcodes 03 0f 00 et le vrai pointeur 0x09f70878 à 0x1e93055 ; aucun consommateur de ce suffixe. Sites rejetés : 0x1e93053. |
| `0x7800bd` | traduit / vérifié en ROM | `0x779382` |
| `0x780119` | exception | aucun consommateur texte — Suffixe de 0x7800bd ; les occurrences 19 01 78 08 chevauchent instructions Thumb ou arguments (ex. code Thumb à 0xef879/0xef899). Aucun pointeur texte : le script msgbox 0x779382 lit 0x7800bd. |
| `0x7801a4` | traduit / vérifié en ROM | `0x779394` |
| `0x7801d1` | traduit / vérifié en ROM | `0x779575` |
| `0x780230` | traduit / vérifié en ROM | `0x77957c` |
| `0x78028c` | traduit / vérifié en ROM | `0x779583` |
| `0x780301` | traduit / vérifié en ROM | `0x77940d`, `0x779420`, `0x779433` |
| `0x78030e` | traduit / vérifié en ROM | `0x779411`, `0x779424`, `0x779437` |
| `0x78033e` | traduit / vérifié en ROM | `0x77947d` |
| `0x780413` | traduit / vérifié en ROM | `0x780405`, `0x780444`, `0x780461`, `0x78076b`, `0x78179f`, `0x781819` |
| `0x7804c9` | traduit / vérifié en ROM | `0x7804c1`, `0x781809`, `0x781883`, `0x7cf19e` |
| `0x7804f5` | traduit / vérifié en ROM | `0x1a944b`, `0x1a9472` |
| `0x780530` | traduit / vérifié en ROM | `0x1a9505`, `0x1a952c` |
| `0x78055d` | traduit / vérifié en ROM | `0x1a9509`, `0x1a9530` |
| `0x780576` | traduit / vérifié en ROM | `0x16a6d0` |
| `0x78069e` | exception | aucun consommateur texte — Fausse entrée extraite depuis le bytecode script avant le texte ; aucun référent vers cet offset. Le vrai msgbox et son texte commencent quelques octets plus loin. |
| `0x7806b6` | traduit / vérifié en ROM | `0x78065d` |
| `0x7806f6` | traduit / vérifié en ROM | `0x780665` |
| `0x7808dd` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x7808de` | traduit / vérifié en ROM | `0x74b0e1` |
| `0x78095f` | traduit / vérifié en ROM | `0x780958` |
| `0x7809b9` | traduit / vérifié en ROM | `0x770b11` |
| `0x7809c4` | traduit / vérifié en ROM | `0x761687` |
| `0x780a50` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x904794. |
| `0x780a9e` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x90479c. |
| `0x780acd` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047a0, 0x9047bc. |
| `0x780b16` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047a4. |
| `0x780b57` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047a8. |
| `0x780b93` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047ac. |
| `0x780bd7` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047b0. |
| `0x780c21` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047b4. |
| `0x780c69` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x904798. |
| `0x780cb2` | exception | aucun consommateur texte — Description historique sans référent ; aucun consommateur dans la table vivante 0x99f194 (racines 0xe5440, 0x137bc8, 0x9f3b64). |
| `0x780cf7` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047c0. |
| `0x780d3f` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047c4. |
| `0x780d88` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047cc. |
| `0x780e33` | exception | aucun consommateur texte — Description historique sans référent ; aucun consommateur dans la table vivante 0x99f194 (racines 0xe5440, 0x137bc8, 0x9f3b64). |
| `0x780e8c` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047d4, 0x90483c. |
| `0x780ed6` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047d8. |
| `0x780eff` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047dc. |
| `0x780f5d` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047e0. |
| `0x780fb9` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047e4. |
| `0x781001` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047e8. |
| `0x781090` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047f0. |
| `0x7810e6` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047f8. |
| `0x781144` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047f4. |
| `0x78117e` | exception | aucun consommateur texte — Description historique sans référent ; aucun consommateur dans la table vivante 0x99f194 (racines 0xe5440, 0x137bc8, 0x9f3b64). |
| `0x7811d9` | exception | aucun consommateur texte — Description historique : seuls référents dans la table morte 0x904000, sans racine référencée. Les consommateurs 0xe5440/0x137bc8/0x9f3b64 lisent 0x99f194 et des textes différents. Sites rejetés : 0x9047ec. |
| `0x78122b` | exception | aucun consommateur texte — Description historique sans référent ; aucun consommateur dans la table vivante 0x99f194 (racines 0xe5440, 0x137bc8, 0x9f3b64). |
| `0x781278` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x7812cf` | traduit / vérifié en ROM | `0x877420` |
| `0x78133b` | traduit / vérifié en ROM | `0x8771b8` |
| `0x78137a` | traduit / vérifié en ROM | `0x877580` |
| `0x7813d4` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x781506` | traduit / vérifié en ROM | `0x77948f` |
| `0x781561` | traduit / vérifié en ROM | `0x765967` |
| `0x78158d` | traduit / vérifié en ROM | `0x78d20e` |
| `0x7815fc` | traduit / vérifié en ROM | `0x752086` |
| `0x781668` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x781669` | traduit / vérifié en ROM | `0x765974` |
| `0x781697` | traduit / vérifié en ROM | `0x765981` |
| `0x78169b` | traduit / vérifié en ROM | `0x765988` |
| `0x7816a1` | traduit / vérifié en ROM | `0x7611bd`, `0x781710` |
| `0x781718` | traduit / vérifié en ROM | `0x76120f` |
| `0x7818b1` | traduit / vérifié en ROM | `0x781897` |
| `0x7818ee` | traduit / vérifié en ROM | `0x7818aa` |
| `0x787bd5` | traduit / vérifié en ROM | `0x76d548` |
| `0x787c0e` | traduit / vérifié en ROM | `0x76d54c` |
| `0x787c3e` | traduit / vérifié en ROM | `0x76d552` |
| `0x787c66` | traduit / vérifié en ROM | `0x76d55f` |
| `0x787cbb` | traduit / vérifié en ROM | `0x76d563` |
| `0x787cfe` | traduit / vérifié en ROM | `0x76d569` |
| `0x787d9e` | traduit / vérifié en ROM | `0x7419f2`, `0x741a19` |
| `0x787dd0` | traduit / vérifié en ROM | `0x741a08` |
| `0x787e08` | traduit / vérifié en ROM | `0x74611b`, `0x74c0b0` |
| `0x787e5a` | traduit / vérifié en ROM | `0x74611f`, `0x74c0b4` |
| `0x787e87` | traduit / vérifié en ROM | `0x746135` |
| `0x787ec4` | traduit / vérifié en ROM | `0x74c0c3`, `0x78819f` |
| `0x787ee7` | traduit / vérifié en ROM | `0x74c0c7`, `0x7881a3` |
| `0x787f07` | traduit / vérifié en ROM | `0x74c0dd` |
| `0x787f3f` | traduit / vérifié en ROM | `0x7881b2`, `0x7881d9` |
| `0x787f77` | traduit / vérifié en ROM | `0x7881b6`, `0x7881dd` |
| `0x787ffd` | traduit / vérifié en ROM | `0x7881f0`, `0x788217` |
| `0x78801b` | traduit / vérifié en ROM | `0x788206` |
| `0x788050` | traduit / vérifié en ROM | `0x788226`, `0x78dcb1` |
| `0x788084` | traduit / vérifié en ROM | `0x78822a`, `0x78dcb5` |
| `0x7880ac` | traduit / vérifié en ROM | `0x788240` |
| `0x7880e5` | traduit / vérifié en ROM | `0x7a72df`, `0x7a9f69` |
| `0x788132` | traduit / vérifié en ROM | `0x7a72e3`, `0x7a9f6d` |
| `0x788163` | traduit / vérifié en ROM | `0x7a72f9` |
| `0x788255` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x7882b8` | traduit / vérifié en ROM | `0x7c8722`, `0x7c8749` |
| `0x7882f7` | traduit / vérifié en ROM | `0x7c8738` |
| `0x7883d3` | traduit / vérifié en ROM | `0x7883bf` |
| `0x788429` | traduit / vérifié en ROM | `0x7883ca` |
| `0x788537` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x788538` | traduit / vérifié en ROM | `0x771912` |
| `0x78856d` | traduit / vérifié en ROM | `0x771928` |
| `0x78857f` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x788595` | traduit / vérifié en ROM | `0x771958` |
| `0x788601` | traduit / vérifié en ROM | `0x77196f` |
| `0x788607` | traduit / vérifié en ROM | `0x77197d` |
| `0x78860c` | traduit / vérifié en ROM | `0x771996` |
| `0x788633` | traduit / vérifié en ROM | `0x7719a3` |
| `0x788674` | traduit / vérifié en ROM | `0x7719a9` |
| `0x788725` | traduit / vérifié en ROM | `0x77194c` |
| `0x788865` | traduit / vérifié en ROM | `0x788782` |
| `0x78889b` | traduit / vérifié en ROM | `0x788795` |
| `0x7888b6` | traduit / vérifié en ROM | `0x7887a8` |
| `0x7889a5` | traduit / vérifié en ROM | `0x7887bb` |
| `0x788a14` | traduit / vérifié en ROM | `0x7887ce` |
| `0x788a96` | traduit / vérifié en ROM | `0x7887f2` |
| `0x788ad6` | traduit / vérifié en ROM | `0x788805` |
| `0x788b02` | traduit / vérifié en ROM | `0x740734` |
| `0x788bab` | traduit / vérifié en ROM | `0x744c9b` |
| `0x788bcd` | traduit / vérifié en ROM | `0x744cae` |
| `0x788bff` | traduit / vérifié en ROM | `0x744cc8` |
| `0x788c15` | traduit / vérifié en ROM | `0x744cf9` |
| `0x788cab` | traduit / vérifié en ROM | `0x741198` |
| `0x788d2d` | traduit / vérifié en ROM | `0x7411bf` |
| `0x788da9` | traduit / vérifié en ROM | `0x74073d` |
| `0x788dc8` | traduit / vérifié en ROM | `0x752091` |
| `0x788df4` | traduit / vérifié en ROM | `0x75209a` |
| `0x788e28` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x788e54` | traduit / vérifié en ROM | `0x7520be` |
| `0x788f69` | traduit / vérifié en ROM | `0x7522d3` |
| `0x788f90` | traduit / vérifié en ROM | `0x7413e3` |
| `0x78900b` | traduit / vérifié en ROM | `0x752120` |
| `0x78903b` | traduit / vérifié en ROM | `0x7521cb` |
| `0x7890ab` | traduit / vérifié en ROM | `0x7521d3` |
| `0x7890c8` | traduit / vérifié en ROM | `0x752208` |
| `0x78910f` | traduit / vérifié en ROM | `0x75221d` |
| `0x789169` | traduit / vérifié en ROM | `0x752236` |
| `0x7891ab` | traduit / vérifié en ROM | `0x752267` |
| `0x78920b` | traduit / vérifié en ROM | `0x74144e` |
| `0x789224` | traduit / vérifié en ROM | `0x7522ad`, `0x7bd1a9` |
| `0x789228` | traduit / vérifié en ROM | `0x7522b3` |
| `0x78922b` | traduit / vérifié en ROM | `0x7522b9` |
| `0x78922e` | traduit / vérifié en ROM | `0x7522c0`, `0x7bd1b0`, `0x7bd1b6` |
| `0x789232` | traduit / vérifié en ROM | `0x7522c6` |
| `0x789236` | traduit / vérifié en ROM | `0x7522cc` |
| `0x78928e` | traduit / vérifié en ROM | `0x7451b5` |
| `0x7893cb` | traduit / vérifié en ROM | `0x78938d`, `0x7893f3` |
| `0x7893dc` | traduit / vérifié en ROM | `0x78939b`, `0x789401` |
| `0x789483` | traduit / vérifié en ROM | `0x78946b` |
| `0x78a26b` | traduit / vérifié en ROM | `0x78a233` |
| `0x78a61c` | traduit / vérifié en ROM | `0x78a604` |
| `0x78a736` | traduit / vérifié en ROM | `0x75ba5b` |
| `0x78a91d` | traduit / vérifié en ROM | `0x776ac4` |
| `0x78a95e` | traduit / vérifié en ROM | `0x77f63b`, `0x78a427` |
| `0x78aa08` | traduit / vérifié en ROM | `0x78a9e5` |
| `0x78aaa8` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x78ab10` | traduit / vérifié en ROM | `0x776aec` |
| `0x78ab3c` | traduit / vérifié en ROM | `0x776add` |
| `0x78ac1d` | traduit / vérifié en ROM | `0x77f654` |
| `0x78b721` | traduit / vérifié en ROM | `0x78a440` |
| `0x78b7ae` | traduit / vérifié en ROM | `0x78a44e` |
| `0x78b7eb` | traduit / vérifié en ROM | `0x77f628` |
| `0x78b828` | traduit / vérifié en ROM | `0x78a8fd` |
| `0x78b83c` | traduit / vérifié en ROM | `0x7881cc` |
| `0x78b89f` | traduit / vérifié en ROM | `0x7794a1` |
| `0x78b928` | traduit / vérifié en ROM | `0x7794b3` |
| `0x78b9a0` | traduit / vérifié en ROM | `0x7794f3` |
| `0x78ba08` | traduit / vérifié en ROM | `0x77950e` |
| `0x78ba4f` | traduit / vérifié en ROM | `0x77955d` |
| `0x78ba9b` | traduit / vérifié en ROM | `0x7798dc` |
| `0x78bb9a` | traduit / vérifié en ROM | `0x78a90b` |
| `0x78bbc9` | traduit / vérifié en ROM | `0x77f5c0`, `0x78a3b1`, `0x78a87d` |
| `0x78bc10` | traduit / vérifié en ROM | `0x77f5e0`, `0x78a3d6`, `0x78a8a7` |
| `0x78bc9a` | traduit / vérifié en ROM | `0x77f5f6`, `0x78a3ec` |
| `0x78bcff` | traduit / vérifié en ROM | `0x76cf8b` |
| `0x78bd31` | traduit / vérifié en ROM | `0x78bc91` |
| `0x78bdca` | traduit / vérifié en ROM | `0x7465e1` |
| `0x78c0bf` | traduit / vérifié en ROM | `0x78c068` |
| `0x78c189` | traduit / vérifié en ROM | `0x78bb62`, `0x78be6e` |
| `0x78c2a8` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x78c2a9` | traduit / vérifié en ROM | `0x78c280` |
| `0x78c2c9` | traduit / vérifié en ROM | `0x78bb66`, `0x78be72` |
| `0x78c2fd` | exception | aucun consommateur texte — Aucun référent 32 bits dans la ROM EN ; absent des tables vivantes de mouvements et objets. |
| `0x78c2fe` | traduit / vérifié en ROM | `0x78c2c0` |
