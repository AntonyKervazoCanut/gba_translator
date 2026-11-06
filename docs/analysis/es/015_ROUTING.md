# ES-015 — contrats mécaniques d’acheminement

F-1043, prérequis de F-865. Aucune traduction ni certification linguistique.
La sélection reste les 393 clés figées ; aucun combined, manifeste de protection,
glossaire ou lot n’est modifié. Les sources du relevé `015_PREPARATION.json` et
`015_ROUTES.json` restent inchangées.

## Débuts décalés

Les onze contrats sont dans `languages/es-maint/text_aliases.json`. Les
préimages EN/ES et tous les sites proviennent du relevé, contrôlés contre les ROM,
les extractions et l’offset map. Les onze correspondances sont `matched` : aucun
`english_only` inventé. Le préfixe n’est jamais du texte traduit.

| Clé | Début vivant | Préfixe | Capacité EN avec FF | Lecteur |
|---|---|---|---:|---|
| 721427 | 721428 | 20 | 15 | 3F1E3C, table de noms |
| 721437 | 721438 | 00 | 15 | 3F1D64, table de noms ; doublon |
| 745A54 | 745A55 | AA | 280 | 741868, `0F 00` |
| 74BE3C | 74BE3D | AA | 253 | 740198, `0F 00` |
| 74BF85 | 74BF86 | AA | 64 | 74AD39, `0F 00` ; doublon |
| 74ED62 | 74ED63 | AA | 65 | 744D43, `0F 00` |
| 75100E | 75100F | AA | 85 | 74BD41, `0F 00` |
| 75350F | 753510 | AA | 131 | 75249B, `0F 00` |
| 755532 | 755533 | AA | 213 | 7524AF, `0F 00` |
| 75B4BB | 75B4BC | AA | 31 | 75450E, `0F 00` |
| 75B6F4 | 75B6F5 | AA | 86 | 16A79A, `0F 00` |

Pour les neuf routes hors doublons, F-865 garde la clé contractuelle dans son
combined : CSV préparé depuis le vrai début, JSON enrichi, réinserteur existant.
Pour les deux doublons, F-865 doit sélectionner **721438 et 74BF86 seulement**
et compter leurs prédécesseurs comme doublons documentés, sans seconde ligne.
Le mécanisme accepte une seule représentation et `check_keys` refuse toujours
les deux simultanément, même avec un texte identique. Le vrai début reçoit
également préimage, commandes, budget et relocalisation obligatoire.

## Fenêtres effectivement consommées

Les noms passent par la table 3F1CAC. Le littéral C0C94 et GetMapName C4D78/C4DB8
la référencent. Les fenêtres 3F1A60 et 3F1A68 font 15 tuiles, soit 120 pixels.
Les impressions C0B66 et C0C68 utilisent la police 2 à x=2 et x=12 : intersection
**108 pixels, une ligne**. Le tampon suivant commence à état+13h : capacité
**19 octets avec FF**. Les routines, littéraux, templates et métriques sont gardés.

Les dialogues `0F 00` passent par ShowFieldMessage 694C8, expansion vers
`gStringVar4` (02021D18), puis F6D5C/F6CD0. La fenêtre 41F42C fait 26 tuiles :
**208 pixels, deux lignes visibles**, x=0/y=1. Les polices dynamiques 2/4/5 ont
les mêmes tables de 512 largeurs (207300, 217618, 227930), vérifiées par préimage.
FE avance de ligne, FA fait défiler, FB recommence une page. FC01 est une couleur,
pas un glyphe ni un changement de police. Les autres commandes non qualifiées
sont refusées par ce contrat de fenêtre, jamais estimées silencieusement.

FD01 retourne le nom joueur via 91E0, table 231E70 et routine 9120. Le template
de saisie 3E245C, utilisé par A6CE38, borne sa longueur à sept caractères ; les
routines 9F826 et 9F676 confirment copie et borne. Réserve conservatrice :
**7 × 12 = 84 pixels**, maximum des métriques gardées. Le plafond encodé du
builder reste 512 octets. Les séquences FC/FD/F8/F9/F7 complètes, leurs arguments,
FA/FB et l’ordre des buffers sont comparés avant injection ; aucune troncature ni
fallback. Les tests de contrats existants couvrent également F8/F9/F7.

## Lecteurs intérieurs : 67 préimages, pas 67 textes certifiés

`preserved_sources` conserve les 67 préimages, les sites directs et intérieurs,
leurs contextes binaires et leurs qualifications. Les 110 occurrences intérieures
visent 91 cibles : 21 `0F 00`, un `67`, six champs de `5C`, huit appels `04`,
deux branches `06 01`, deux structures de scripts d’événements, une MapConnections,
deux noms de régions, une table de pointeurs sans consommateur démontré, une
ancienne description d’objet et **65 occurrences binaires non prouvées**.
Ces dernières ne sont pas déclarées fausses : leurs octets restent inchangés.
Aucune zone n’est déduite des adresses.

46 débuts possèdent 50 lecteurs directs textuels qualifiés. Leur sélection force
une relocalisation, **même si le texte traduit tient dans le budget EN**. Le JSON
porte la préimage et la seule liste de lecteurs directs autorisés. SmartReinserter
utilise son allocateur et sa file de relocalisation habituels ; aucun second
réinserteur. L’absence de préimage, de lecteur sûr ou de capacité de relocalisation
interdit l’écriture. La vérification finale refuse aussi une allocation manquée.
La passe inline ignore ces routes et le repointeur de secours ne les complète
pas à partir d’occurrences binaires plus larges.

Les préimages restent à leur adresse d’origine et les consommateurs non
sélectionnés restent inchangés. À 741625, seul 740136 change de cible ; les
lecteurs 741548/741565 conservent 741693/7416B5, le branchement 74155A conserve
7416D6. Aucun suffixe hors lot n’est traduit. La même règle protège les occurrences
non prouvées à l’intérieur de 75100F et 755533.

Six clés sans lecteur direct certifié (71A3D2, 71A73A, 71A814, 7213FC, 745973,
7502A5) restent à la qualification F-865. Leur sélection sans route échoue
explicitement : ce n’est **pas une exclusion linguistique**. Les autres clés sans
référence directe ne sont pas filtrées par cette adaptation.

721340 (MapConnections, 12 octets), 74037D (script, 2 octets), 745132 (script,
9 octets) et 74B293 (script, 11 octets) sont hors traduction et refusés comme
clés d’injection. Aucun alias textuel de ces scripts. Les textes suivants ne sont
pas exclus par cette garde. Le panneau 74B29E est une clé distincte du lot :
son champ pointeur 74B296 peut être repointé uniquement si ce panneau est sélectionné
et que ses octets finaux et commandes sont vérifiés ; les opcodes restent gardés.
Le texte 72134C sans lecteur direct reste à qualifier dans F-865.

## Vérification reproductible

`tests/unit/test_es015_routing.py` reproduit d’abord l’écrasement par une traduction
courte, puis contrôle relocalisation, refus, branche, clés et fenêtres paginées.
Les fixtures sont des tranches ROM réelles ; les contrats existants restent testés.
`tests/e2e/es/test_es015_routing.py` utilise un combined temporaire : **57 entrées**
(9 alias, 2 doublons canoniques, 46 préimages), vrai CSV → JSON → builder → patches.
Une seule lettre de chaque préimage est remplacée par une sentinelle de même
longueur ; toutes les commandes et leurs arguments sont conservés.
Le contrôle des différences binaires est exhaustif avant patches et après patches
contre un témoin passé par les mêmes patches : seuls les champs pointeurs et
allocations sélectionnés sont autorisés. Les préfixes, voisins, branches et autres
consommateurs restent inchangés. Les sources sont hachées avant/après.

Les ROM source sont des copies locales ordinaires, sans symlink extérieur ni mode
0444. Le témoin FR avant modification, BUILD_NUMBER=0, vaut
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`, identique
au témoin F-865. Les résultats finaux des builds, suites, hooks et de la sonde
Playwright headless/mGBA offscreen sont consignés dans la résolution du ticket.
Les traductions finales, leurs parcours naturels et leur certification restent à F-865.

## Preuve native

`npx playwright test --config tests/e2e-playwright/fixtures/es015-routing.config.ts`
a passé son assertion : 57 routes lues dans mGBA, neuf mires et toutes leurs
largeurs mesurées par GetStringWidth. La configuration est autonome, headless,
sans serveur ; mGBA reçoit explicitement `QT_QPA_PLATFORM=offscreen`.
Les pointeurs non alignés sont lus octet par octet, pour éviter la rotation ARM
de read32. FD01 est développé par StringExpandPlaceholders sur un nom temporaire
de sept caractères en RAM. La ROM reste inchangée ; la flash créée automatiquement
par mGBA reste entièrement FF (aucune sauvegarde en jeu).
La capture OS temporaire est attachée à F-1043 :
`attachment://60ebf30e-b881-4d4f-aeb7-66d1d519c1cb`.
La mire affiche les sept premières lignes au maximum par alias, séparément ;
toutes les lignes sont mesurées, sans prétendre certifier les parcours naturels.

## Résultats locaux intermédiaires

Les quatre commandes `make build-es-maint build-it build-de build-fr BUILD_NUMBER=0`
ont réussi. Le `cmp` FR avant/après est identique ; le SHA-256 reste le témoin F-865.
Le build ES sans nouvelles traductions garde également son empreinte de préparation :
`1f4f6e779586a4c91225f5fcc082e40d74d70407f985515015ba5b5ceada1ba2`.
Le test intégral ES-015, avec témoin après patches, passe (85,65 s) ; le test de
tous les alias existants passe également. Les 31 tests unitaires ES-015 passent.
Les fichiers Python ajoutés passent ruff ; aucun diagnostic supplémentaire n’est
introduit dans les fichiers historiques modifiés. Les deux fichiers TypeScript
ajoutés passent le contrôle de types. Les résultats complets des suites et hooks
sont donnés dans la résolution, après leur achèvement.
