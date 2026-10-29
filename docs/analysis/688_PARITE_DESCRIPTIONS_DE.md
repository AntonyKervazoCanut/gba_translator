# B-688 — Parité des descriptions DE : preuve partielle et blocage technique

La parité n'est **pas acquise**. Le réinséreur générique suffit pour une partie du
corpus, mais **combined_de.txt seul ne suffit pas pour l'ensemble** : après deux
commits de corrections textuelles et un build frais, 33 des 72 références de ce
lot restent anglaises. B-1013 fournit le prérequis d'injection structurée des
descriptions absentes de l'extraction. Aucun patch dédié n'est ajouté ici.

## Périmètre exact et sources

Les fichiers FR sont lus uniquement pour leurs clés :
`move_descriptions_fr_overrides.json` contient **220 index numériques et une clé
_comment**, non une 221e attaque ; `tm_item_descriptions_fr.json` contient huit
index d'objets. Les 229 clés donnent donc **228 descriptions réelles**. Aucune
formulation FR n'a été recopiée. La clé `_comment` est explicitement exclue de
l'injection, avant comme après.

La fixture `tests/unit/fixtures/de_move_parity_688.json` conserve pour chaque
référence son index, site de pointeur, offset EN canonique, propriétaire du lot,
texte source EN, dernière valeur DE initiale, texte réellement injecté avant et
après, cible relocalisée, octets hexadécimaux, largeur et nombre de lignes.
`authored` est la valeur DE finale rédigée dans ce ticket, pas une affirmation
qu'elle a été injectée. `after.exact` vérifie tous les octets, terminateur compris.
Les deux SHA-256 de ROM DE et celui de la source EN identifient les mesures ;
aucun hash de référence FR n'est changé.

État avant : base `224fca42`, ROM DE reconstruite localement. État après : sources
au commit `2ec5b6be`, après `1acd4989`, puis build DE complet. Les captures et la
fixture décrivent ce point de contrôle ; une reprise après B-1013 doit refaire
l'audit, et non déduire la conformité de ces fichiers historiques.

## Résultat mesuré

| Mesure | Avant | Après |
|---|---:|---:|
| Descriptions réelles | 228 | 228 |
| Identiques à la source EN | 195 | 189 |
| Références B-688 encore EN | 39 / 72 | 33 / 72 |
| Références B-688 contenant le texte DE attendu, dans le budget | — | 39 / 72 |
| Égalité stricte des octets avec le texte DE B-688 | — | 37 / 72 |
| Références B-688 dépassant le budget | 30 | 1 |

Les deux cas DE non identiques à l'octet conservent tous les mots mais changent
les retours à la ligne : la différence est enregistrée, pas assimilée à une
égalité stricte. La seule description B-688 hors budget restante est Zenitstürmer
(index 559, 0xA3BABD), encore EN, à 124 px pour un budget de 122 px.

Les 72 références propres au ticket correspondent à **71 offsets distincts** :
Kaskade, index d'attaque 127, et HM07, index d'objet 452, partagent 0x484986.
Les 71 dernières occurrences ont été corrigées chirurgicalement et protégées
exactement dans le même commit. Comparaison des octets du fichier avec la base :
71 lignes modifiées, même nombre de lignes, mêmes offsets, ordre, doublons et
fins de ligne ; toutes les autres lignes sont identiques.

**156 références réservées** : 72 à B-669 et 84 à B-670. Aucune traduction de ces
lots n'est éditée ici. Elles restent EN dans ce point de contrôle : leur
attribution n'est pas une preuve de correction. Les listes explicites B-666 à
B-687 ont été croisées avec les offsets résolus, et non avec les index FR.

40 des 72 références B-688 sont absentes de `de_translation_ready.json` malgré
leur présence dans combined. Certaines sont néanmoins récupérées en place par
la passe inline ; l'absence du JSON ne suffit donc pas non plus à conclure.
L'échec résiduel est prouvé par les **33 valeurs anglaises aux pointeurs actifs**.
Il correspond au défaut d'extraction/injection déjà décrit par B-1013.

## Résolution des tables et CT/CS

La table utilisée par le patch FR et `src/core/moves.py` est 0x99F190 ; une
référence d'attaque `i` est lue à `0x99F190 + 4*i`. Les descriptions d'objets se
lisent à `0x876074 + 44*item + 0x14`. Le même site est déréférencé dans EN puis
DE ; on ne cherche jamais une traduction au seul ancien offset. Les huit
associations ci-dessous sont établies par l'égalité des pointeurs source avec
les entrées de la table d'attaques, avec la nomenclature CFRU indexée de
`languages/de/data` (et non les numéros nationaux d'une autre génération).

| Objet/index | Attaque/index CFRU | Offset EN | Responsable texte |
|---|---|---|---|
| TM26 / 323 | Erdbeben / 89 | 0x483F44 | B-688 |
| TM29 / 326 | Psychokinese / 94 | 0x484098 | B-688 |
| TM74 / 399 | Gyroball / 510 | 0xA3A99E | B-688 |
| TM76 / 401 | Tarnsteine / 468 | 0xA39D8D | B-688 |
| TM84 / 409 | Gifthieb / 424 | 0xA39198 | B-669 |
| TM104 / 429 | Psychoschock / 502 | 0xA3A733 | B-688 |
| HM07 / 452 | Kaskade / 127 | 0x484986 | B-688 |
| TM107 / 432 | Akrobatik / 440 | 0xA3961D | B-688 |

## Texte, encodage et fenêtres

Les formulations DE sont condensées pour préserver l'effet : drainage et ratio
de KP, conditions de sommeil/item/terrain, tours de charge, recul, modifications
de statistiques, efficacité contre Eau, impossibilité de fuir, coup critique,
vol de bonus et interactions avec les barrières. Le texte parle de
`zurückschrecken` pour le flinch, non de peur générique. Les noms et statistiques
suivent le glossaire local : KP, Initiative, Fluchtwert, Spezialangriff,
Spezialverteidigung, Lichtschild, Reflektor, Kreuzflamme. Les umlauts sont réels.
Schnüffler est distingué de l'effet de Miracle Eye ; Säure mentionne la
Spezialverteidigung et Raserei l'augmentation d'Angriff. La variante Unbound
« frostbite » de Gefriertrockner reste une Erfrierung, sans la transformer
silencieusement en gel classique.

Les 228 descriptions EN sont du texte simple : aucun placeholder ni FC/FD/F7/F8/F9,
FA ou FB. Les 71 valeurs rédigées le restent ; `TextEncoder` avec
`GERMAN_UMLAUT_CHARS` est comparé aux octets ROM, terminateur FF compris. Les
sauts FE sont mesurés séparément, les contrôles spéciaux ne sont pas ignorés.
Budgets : résumé ≤5 lignes, 122 px ; CT/CS ≤4 lignes, 144 px. Les textes B-688
sont rédigés à 122 px y compris pour les CT/CS, pour conserver une marge et
respecter les consommateurs partagés. Les textes sources tiennent tous ; cela
ne rend pas automatiquement conformes les chaînes réellement injectées.

## Contradictions des descripteurs et suivis techniques

`lang.yaml` confondait « aucun patch dédié » et « table non couverte ». Les
mesures montrent une couverture partielle : son commentaire est précisé, sans
changer le statut de langue. `parity.yaml` ne présente plus un hash global ou
la présence dans combined comme une preuve de traduction.

- **Tri Cube** : 0xA4E047→pointeur 0x9F4880 ; 0xA4E07A→0xA6BAE4 ;
  0xA4E096→0x9F30C0 et 0xA6BA60 ; 0xA4E09D→0x9F3080 ;
  0xA4E0AF→0x9F4C84. Tous visent déjà des textes DE relocalisés. Les
  placeholders FD de tri sont présents ; les ruptures réécrites sont conservées
  dans la preuve. Le graphisme `cube_sort_hint` est réinjecté par `menu_sprites`.
  L'exclusion « sera porté avec ses libellés graphiques » était périmée.
  Aucun nouveau lot de traductions ni patch n'est justifié sur ces cinq textes.
- **Cube V3** : 0x1E67DB8→0xB4E640 affiche la valeur DE de 0x1F01074,
  avec les pauses/pages. Le dialogue est déjà couvert.
- **Cube TV** : 0x1EAF7F5→0x1FB052C reste EN ; 0x1285745→0x1FB07FE
  reste EN alors que 0x1EAF820 est déjà relocalisé. B-682 détient les textes ;
  B-1016 traite l'acheminement technique des références résiduelles.
- **Dialogues longs** : 0x7A9A75 (1046 octets), 0x1EEE8BE (1037),
  0x1F0F004 (1441), 0x1F8E271 (1044), 0x1F4C2ED (1060) restent EN aux
  sites 0x74B0AA, 0x1E5B206, 0x1E70293, 0x1E9FA40, 0x1E6D700.
  Leurs valeurs DE existent déjà. B-681/B-680 détiennent les deux derniers
  textes ; B-1016 répare le plafond d'extraction/acheminement, sans doublonner
  ces traductions. La déclaration « injecté par combined » était fausse.
- Les cibles de mise en page 0x1F2E221 et 0x1A63E8 du patch FR
  `meteorite_dialogue` sont déjà relocalisées en DE. La preuve garde leurs
  commandes décodées ; leur mise en page n'est pas déclarée identique au FR.

La fixture contient également tous les sites et textes des exclusions
ci-dessus. B-1016 est un suivi technique autonome, pas un transfert du lot B-688.

## Vérifications et reprise

- `make build-de` réussi ; les hooks des deux commits ont également exécuté
  les tests Python/Vitest et les builds FR/IT/DE dans le worktree isolé.
- `make test-python` après corrections : **2182 réussis, 3 ignorés,
  742 désélectionnés**. Aucun échec. Les ignorés sont ceux du profil existant.
- Cinq tests ciblés contrôlent l'inventaire, les budgets des textes rédigés,
  l'association CT/attaque, Schnüffler et le suivi d'une cible relocalisée à
  partir d'octets ROM capturés. Ruff passe sur les deux fichiers Python ajoutés.
- `check_de_parity.py` et `check_de_scope.py --staged` réussissent.
- Playwright headless `move-parity-688-de.spec.ts` : **1 réussi**. La copie
  temporaire présente la fiche réelle de TM26 dans l'emplacement TM56 de la
  sauvegarde de test. Assertions : texte exact via son pointeur, dernière ligne
  visible, aucun pixel de texte rogné à droite, navigation aller/retour restituant
  le panneau. Aucun texte ROM n'est fabriqué, aucune sauvegarde en jeu.
  Capture hors dépôt attachée : `4a10d632-4ad7-4ed7-b826-0c5281be6618`.

Commande de reprise, indépendante des fichiers temporaires de la session :

```sh
make build-de
python3 scripts/audit_de_move_parity.py --output output/reports/b688-parite.json
make test-python
```

Le contrôleur retourne actuellement **1**, intentionnellement : il ne masque
pas les descriptions EN ou non conformes en les marquant comme réussies. Après
B-1013, puis intégration des textes B-669/B-670, il doit retourner 0 sur les
228 références avant toute certification complète.

### Non vérifié

La parité totale, l'injection des 33 références propres à B-688 encore EN, la
correction des 156 références réservées aux lots voisins et les 228 affichages
individuels ne sont pas validés. Les mécaniques de combat ne sont pas rejouées
attaque par attaque en émulation. La preuve Playwright porte sur TM26, pas sur
toutes les fenêtres du résumé. B-688 doit rester en attente du prérequis
technique et des lots propriétaires ; aucun succès global n'est revendiqué.
Aucun push, pipeline distant, patch dédié ni modification FR/IT ou hash FR.

## Décision pour chacune des 229 clés

Les textes et octets complets avant/après sont dans la fixture citée ; cette
vue indexée donne les sites, résultats et responsabilités sans omettre de clé.

| Source / clé | Offset EN | Site du pointeur | Avant | Après | Décision |
|---|---|---|---|---|---|
| attaques / _comment | — | — | Métadonnée | Métadonnée | Exclue, aucun texte ROM |
| attaque / 23 | 0x482dc8 | 0x99f1ec | DE | DE exact ; 4 l. / 95 px | Corrigé et injecté |
| attaque / 29 | 0x482f4c | 0x99f204 | DE hors budget | DE exact ; 3 l. / 122 px | Corrigé et injecté |
| attaque / 44 | 0x483358 | 0x99f240 | DE hors budget | DE replié ; 4 l. / 98 px | Corrigé et injecté |
| attaque / 51 | 0x483534 | 0x99f25c | EN | EN ; 4 l. / 106 px | Source corrigée ; attend B-1013 |
| attaque / 69 | 0x4839f8 | 0x99f2a4 | EN | DE exact ; 4 l. / 112 px | Corrigé et injecté |
| attaque / 78 | 0x483c5d | 0x99f2c8 | DE | DE exact ; 3 l. / 106 px | Corrigé et injecté |
| attaque / 90 | 0x483f89 | 0x99f2f8 | EN | EN ; 4 l. / 107 px | Source corrigée ; attend B-1013 |
| attaque / 99 | 0x4841e9 | 0x99f31c | EN | EN ; 4 l. / 102 px | Source corrigée ; attend B-1013 |
| attaque / 127 | 0x484986 | 0x99f38c | EN | EN ; 4 l. / 106 px | Source corrigée ; attend B-1013 |
| attaque / 133 | 0x484b27 | 0x99f3a4 | EN | EN ; 4 l. / 76 px | Source corrigée ; attend B-1013 |
| attaque / 135 | 0x484ba1 | 0x99f3ac | EN | EN ; 4 l. / 104 px | Source corrigée ; attend B-1013 |
| attaque / 138 | 0x484c75 | 0x99f3b8 | EN | EN ; 4 l. / 103 px | Source corrigée ; attend B-1013 |
| attaque / 141 | 0x484d42 | 0x99f3c4 | EN | EN ; 4 l. / 103 px | Source corrigée ; attend B-1013 |
| attaque / 148 | 0x484f20 | 0x99f3e0 | EN | DE exact ; 4 l. / 88 px | Corrigé et injecté |
| attaque / 161 | 0xa37d98 | 0x99f414 | EN | EN ; 4 l. / 115 px | B-669 : édition réservée |
| attaque / 182 | 0x485857 | 0x99f468 | EN | EN ; 4 l. / 107 px | Source corrigée ; attend B-1013 |
| attaque / 193 | 0x485b55 | 0x99f494 | EN | EN ; 4 l. / 108 px | Source corrigée ; attend B-1013 |
| attaque / 197 | 0x485c66 | 0x99f4a4 | EN | EN ; 4 l. / 107 px | Source corrigée ; attend B-1013 |
| attaque / 208 | 0x485f6c | 0x99f4d0 | EN | DE exact ; 4 l. / 96 px | Corrigé et injecté |
| attaque / 217 | 0x4861d1 | 0x99f4f4 | EN | EN ; 4 l. / 107 px | Source corrigée ; attend B-1013 |
| attaque / 222 | 0x486330 | 0x99f508 | EN | DE exact ; 4 l. / 106 px | Corrigé et injecté |
| attaque / 249 | 0x486aa6 | 0x99f574 | EN | EN ; 4 l. / 96 px | Source corrigée ; attend B-1013 |
| attaque / 251 | 0x486b36 | 0x99f57c | EN | EN ; 4 l. / 103 px | Source corrigée ; attend B-1013 |
| attaque / 254 | 0x486c10 | 0x99f588 | DE | EN ; 4 l. / 94 px | Source corrigée ; attend B-1013 |
| attaque / 280 | 0x4872f2 | 0x99f5f0 | EN | EN ; 4 l. / 106 px | Source corrigée ; attend B-1013 |
| attaque / 289 | 0x487558 | 0x99f614 | EN | DE exact ; 4 l. / 110 px | Corrigé et injecté |
| attaque / 291 | 0x4875e5 | 0x99f61c | EN | EN ; 4 l. / 96 px | Source corrigée ; attend B-1013 |
| attaque / 316 | 0x487c8b | 0x99f680 | EN | EN ; 4 l. / 108 px | Source corrigée ; attend B-1013 |
| attaque / 344 | 0x488408 | 0x99f6f0 | EN | EN ; 4 l. / 102 px | Source corrigée ; attend B-1013 |
| attaque / 347 | 0x4884c5 | 0x99f6fc | EN | EN ; 4 l. / 91 px | Source corrigée ; attend B-1013 |
| attaque / 355 | 0xa37ec4 | 0x99f71c | EN | EN ; 4 l. / 103 px | B-669 : édition réservée |
| attaque / 362 | 0xa380ab | 0x99f738 | EN | EN ; 4 l. / 110 px | B-669 : édition réservée |
| attaque / 363 | 0xa380f4 | 0x99f73c | EN | EN ; 4 l. / 103 px | B-669 : édition réservée |
| attaque / 372 | 0xa38385 | 0x99f760 | EN | EN ; 4 l. / 115 px | B-669 : édition réservée |
| attaque / 373 | 0xa383d5 | 0x99f764 | EN | EN ; 4 l. / 110 px | Source corrigée ; attend B-1013 |
| attaque / 374 | 0xa38422 | 0x99f768 | EN | EN ; 4 l. / 102 px | Source corrigée ; attend B-1013 |
| attaque / 391 | 0xa388a6 | 0x99f7ac | EN | EN ; 4 l. / 102 px | B-669 : édition réservée |
| attaque / 404 | 0xa38c36 | 0x99f7e0 | EN | EN ; 4 l. / 107 px | Source corrigée ; attend B-1013 |
| attaque / 410 | 0xa38dea | 0x99f7f8 | EN | EN ; 4 l. / 107 px | B-669 : édition réservée |
| attaque / 411 | 0xa38e32 | 0x99f7fc | EN | EN ; 4 l. / 101 px | B-669 : édition réservée |
| attaque / 412 | 0xa38e70 | 0x99f800 | EN | EN ; 4 l. / 108 px | B-669 : édition réservée |
| attaque / 415 | 0xa38f30 | 0x99f80c | EN | EN ; 4 l. / 106 px | B-669 : édition réservée |
| attaque / 427 | 0xa3927c | 0x99f83c | EN | EN ; 4 l. / 97 px | B-669 : édition réservée |
| attaque / 434 | 0xa3947a | 0x99f858 | EN | EN ; 4 l. / 117 px | B-669 : édition réservée |
| attaque / 437 | 0xa39557 | 0x99f864 | EN | EN ; 4 l. / 90 px | B-669 : édition réservée |
| attaque / 442 | 0xa39693 | 0x99f878 | EN | EN ; 4 l. / 94 px | B-669 : édition réservée |
| attaque / 443 | 0xa396d3 | 0x99f87c | EN | EN ; 4 l. / 94 px | B-669 : édition réservée |
| attaque / 449 | 0xa3987a | 0x99f894 | EN | EN ; 4 l. / 99 px | Source corrigée ; attend B-1013 |
| attaque / 451 | 0xa398ff | 0x99f89c | EN | EN ; 4 l. / 94 px | Source corrigée ; attend B-1013 |
| attaque / 452 | 0xa39940 | 0x99f8a0 | EN | EN ; 4 l. / 113 px | B-669 : édition réservée |
| attaque / 453 | 0xa3998b | 0x99f8a4 | EN | EN ; 4 l. / 104 px | B-669 : édition réservée |
| attaque / 465 | 0xa39ccd | 0x99f8d4 | EN | EN ; 4 l. / 111 px | B-669 : édition réservée |
| attaque / 473 | 0xa39ef6 | 0x99f8f4 | EN | EN ; 4 l. / 109 px | B-669 : édition réservée |
| attaque / 475 | 0xa39f84 | 0x99f8fc | EN | EN ; 4 l. / 107 px | B-669 : édition réservée |
| attaque / 477 | 0xa3a006 | 0x99f904 | EN | EN ; 4 l. / 105 px | B-669 : édition réservée |
| attaque / 479 | 0xa3a097 | 0x99f90c | EN | EN ; 4 l. / 106 px | B-669 : édition réservée |
| attaque / 480 | 0xa3a0da | 0x99f910 | EN | EN ; 4 l. / 102 px | B-669 : édition réservée |
| attaque / 481 | 0xa3a127 | 0x99f914 | EN | EN ; 4 l. / 104 px | B-669 : édition réservée |
| attaque / 482 | 0xa3a16f | 0x99f918 | EN | EN ; 4 l. / 107 px | B-669 : édition réservée |
| attaque / 486 | 0xa3a285 | 0x99f928 | DE | DE exact ; 4 l. / 90 px | Corrigé et injecté |
| attaque / 495 | 0xa3a506 | 0x99f94c | EN | EN ; 5 l. / 103 px | B-669 : édition réservée |
| attaque / 498 | 0xa3a5f3 | 0x99f958 | EN | EN ; 4 l. / 99 px | B-669 : édition réservée |
| attaque / 501 | 0xa3a6d6 | 0x99f964 | DE hors budget | DE exact ; 4 l. / 97 px | Corrigé et injecté |
| attaque / 503 | 0xa3a77d | 0x99f96c | EN | EN ; 4 l. / 105 px | Source corrigée ; attend B-1013 |
| attaque / 505 | 0xa3a821 | 0x99f974 | EN | EN ; 5 l. / 108 px | B-669 : édition réservée |
| attaque / 506 | 0xa3a87d | 0x99f978 | EN | EN ; 4 l. / 102 px | Source corrigée ; attend B-1013 |
| attaque / 507 | 0xa3a8c5 | 0x99f97c | EN | EN ; 4 l. / 108 px | B-669 : édition réservée |
| attaque / 508 | 0xa3a903 | 0x99f980 | EN | EN ; 5 l. / 99 px | B-669 : édition réservée |
| attaque / 509 | 0xa3a955 | 0x99f984 | EN | EN ; 4 l. / 100 px | B-669 : édition réservée |
| attaque / 511 | 0xa3a9ee | 0x99f98c | EN | EN ; 5 l. / 104 px | B-669 : édition réservée |
| attaque / 513 | 0xa3aaa0 | 0x99f994 | EN | EN ; 5 l. / 102 px | B-669 : édition réservée |
| attaque / 515 | 0xa3ab56 | 0x99f99c | EN | EN ; 5 l. / 104 px | B-669 : édition réservée |
| attaque / 516 | 0xa3abb2 | 0x99f9a0 | EN | EN ; 5 l. / 105 px | B-669 : édition réservée |
| attaque / 517 | 0xa3ac0c | 0x99f9a4 | DE hors budget | DE exact ; 3 l. / 117 px | Corrigé et injecté |
| attaque / 518 | 0xa3ac63 | 0x99f9a8 | DE hors budget | DE exact ; 3 l. / 114 px | Corrigé et injecté |
| attaque / 522 | 0xa3adc8 | 0x99f9b8 | EN | EN ; 5 l. / 120 px | B-669 : édition réservée |
| attaque / 523 | 0xa3ae26 | 0x99f9bc | EN | EN ; 5 l. / 111 px | B-669 : édition réservée |
| attaque / 525 | 0xa3aed7 | 0x99f9c4 | DE hors budget | DE exact ; 4 l. / 90 px | Corrigé et injecté |
| attaque / 527 | 0xa3af8e | 0x99f9cc | EN | EN ; 5 l. / 105 px | B-669 : édition réservée |
| attaque / 529 | 0xa3b037 | 0x99f9d4 | EN | EN ; 5 l. / 108 px | B-669 : édition réservée |
| attaque / 530 | 0xa3b090 | 0x99f9d8 | DE hors budget | DE exact ; 4 l. / 109 px | Corrigé et injecté |
| attaque / 531 | 0xa3b0f3 | 0x99f9dc | DE hors budget | DE exact ; 4 l. / 109 px | Corrigé et injecté |
| attaque / 532 | 0xa3b14d | 0x99f9e0 | EN | EN ; 5 l. / 109 px | B-669 : édition réservée |
| attaque / 534 | 0xa3b1fd | 0x99f9e8 | EN | EN ; 5 l. / 109 px | B-669 : édition réservée |
| attaque / 535 | 0xa3b25a | 0x99f9ec | EN | EN ; 4 l. / 103 px | B-669 : édition réservée |
| attaque / 536 | 0xa3b2a6 | 0x99f9f0 | EN | EN ; 5 l. / 107 px | B-669 : édition réservée |
| attaque / 538 | 0xa3b35d | 0x99f9f8 | EN | EN ; 5 l. / 107 px | B-669 : édition réservée |
| attaque / 540 | 0xa3b408 | 0x99fa00 | EN | EN ; 5 l. / 113 px | B-669 : édition réservée |
| attaque / 543 | 0xa3b4fd | 0x99fa0c | EN | EN ; 5 l. / 108 px | B-669 : édition réservée |
| attaque / 544 | 0xa3b552 | 0x99fa10 | EN | EN ; 5 l. / 113 px | B-669 : édition réservée |
| attaque / 545 | 0xa3b5ae | 0x99fa14 | EN | EN ; 5 l. / 113 px | B-669 : édition réservée |
| attaque / 550 | 0xa3b779 | 0x99fa28 | EN | EN ; 5 l. / 115 px | B-669 : édition réservée |
| attaque / 551 | 0xa3b7d7 | 0x99fa2c | DE hors budget | DE exact ; 4 l. / 100 px | Corrigé et injecté |
| attaque / 552 | 0xa3b836 | 0x99fa30 | DE hors budget | DE replié ; 5 l. / 90 px | Corrigé et injecté |
| attaque / 553 | 0xa3b892 | 0x99fa34 | EN | EN ; 5 l. / 105 px | B-669 : édition réservée |
| attaque / 554 | 0xa3b8ef | 0x99fa38 | EN | EN ; 5 l. / 107 px | B-669 : édition réservée |
| attaque / 556 | 0xa3b9a7 | 0x99fa40 | DE hors budget | DE exact ; 4 l. / 97 px | Corrigé et injecté |
| attaque / 557 | 0xa3ba04 | 0x99fa44 | DE hors budget | DE exact ; 4 l. / 95 px | Corrigé et injecté |
| attaque / 559 | 0xa3babd | 0x99fa4c | EN hors budget | EN ; 5 l. / 124 px | Source corrigée ; attend B-1013 |
| attaque / 560 | 0xa3bb24 | 0x99fa50 | EN | EN ; 5 l. / 120 px | B-669 : édition réservée |
| attaque / 563 | 0xa3bc34 | 0x99fa5c | DE hors budget | DE exact ; 3 l. / 110 px | Corrigé et injecté |
| attaque / 565 | 0xa3bce2 | 0x99fa64 | EN | EN ; 4 l. / 117 px | B-669 : édition réservée |
| attaque / 566 | 0xa3bd35 | 0x99fa68 | EN | EN ; 5 l. / 110 px | B-669 : édition réservée |
| attaque / 568 | 0xa3bdef | 0x99fa70 | EN | EN ; 5 l. / 116 px | B-669 : édition réservée |
| attaque / 570 | 0xa3be9d | 0x99fa78 | EN | EN ; 5 l. / 118 px | B-669 : édition réservée |
| attaque / 571 | 0xa3bef9 | 0x99fa7c | EN | EN ; 5 l. / 92 px | B-669 : édition réservée |
| attaque / 573 | 0xa3bfa0 | 0x99fa84 | DE hors budget | DE exact ; 4 l. / 100 px | Corrigé et injecté |
| attaque / 574 | 0xa3bffd | 0x99fa88 | EN | EN ; 5 l. / 115 px | B-669 : édition réservée |
| attaque / 575 | 0xa3c052 | 0x99fa8c | EN | EN ; 5 l. / 110 px | B-669 : édition réservée |
| attaque / 576 | 0xa3c0ad | 0x99fa90 | EN | EN ; 5 l. / 108 px | B-669 : édition réservée |
| attaque / 579 | 0xa3c1b4 | 0x99fa9c | EN | EN ; 5 l. / 118 px | B-669 : édition réservée |
| attaque / 580 | 0xa3c210 | 0x99faa0 | EN | EN ; 5 l. / 122 px | B-669 : édition réservée |
| attaque / 581 | 0xa3c26b | 0x99faa4 | EN | EN ; 4 l. / 121 px | B-669 : édition réservée |
| attaque / 583 | 0xa3c314 | 0x99faac | EN | EN ; 5 l. / 112 px | B-669 : édition réservée |
| attaque / 584 | 0xa3c36c | 0x99fab0 | EN | EN ; 5 l. / 107 px | B-669 : édition réservée |
| attaque / 585 | 0xa3c3c6 | 0x99fab4 | EN | EN ; 5 l. / 112 px | B-669 : édition réservée |
| attaque / 587 | 0xa3c46a | 0x99fabc | DE hors budget | DE exact ; 4 l. / 102 px | Corrigé et injecté |
| attaque / 588 | 0xa3c4c7 | 0x99fac0 | DE hors budget | DE exact ; 4 l. / 96 px | Corrigé et injecté |
| attaque / 590 | 0xa3c57d | 0x99fac8 | DE hors budget | DE exact ; 4 l. / 109 px | Corrigé et injecté |
| attaque / 591 | 0xa3c5db | 0x99facc | EN | EN ; 5 l. / 118 px | B-669 : édition réservée |
| attaque / 594 | 0xa3c6bd | 0x99fad8 | DE hors budget | DE exact ; 4 l. / 96 px | Corrigé et injecté |
| attaque / 597 | 0xa3c7ae | 0x99fae4 | EN | EN ; 5 l. / 102 px | B-669 : édition réservée |
| attaque / 599 | 0xa3c863 | 0x99faec | EN | EN ; 5 l. / 118 px | B-669 : édition réservée |
| attaque / 601 | 0xa3c90e | 0x99faf4 | EN | EN ; 5 l. / 113 px | B-669 : édition réservée |
| attaque / 602 | 0xa3c96b | 0x99faf8 | EN | EN ; 5 l. / 108 px | B-669 : édition réservée |
| attaque / 603 | 0xa3c9c6 | 0x99fafc | EN | EN ; 5 l. / 115 px | B-670 : édition réservée |
| attaque / 604 | 0xa3ca1f | 0x99fb00 | EN | EN ; 5 l. / 107 px | B-670 : édition réservée |
| attaque / 606 | 0xa3cad9 | 0x99fb08 | EN | EN ; 5 l. / 117 px | B-670 : édition réservée |
| attaque / 608 | 0xa3cb88 | 0x99fb10 | EN | EN ; 5 l. / 102 px | B-670 : édition réservée |
| attaque / 609 | 0xa3cbe2 | 0x99fb14 | EN | EN ; 5 l. / 107 px | B-670 : édition réservée |
| attaque / 611 | 0xa3cc78 | 0x99fb1c | EN | EN ; 5 l. / 122 px | B-670 : édition réservée |
| attaque / 612 | 0xa3ccd7 | 0x99fb20 | EN | EN ; 5 l. / 110 px | B-670 : édition réservée |
| attaque / 613 | 0xa3cd26 | 0x99fb24 | DE hors budget | DE exact ; 4 l. / 107 px | Corrigé et injecté |
| attaque / 617 | 0xa3ce5a | 0x99fb34 | EN | EN ; 4 l. / 115 px | B-670 : édition réservée |
| attaque / 619 | 0xa3cefc | 0x99fb3c | DE hors budget | DE exact ; 4 l. / 109 px | Corrigé et injecté |
| attaque / 620 | 0xa3cf56 | 0x99fb40 | EN | EN ; 5 l. / 115 px | B-670 : édition réservée |
| attaque / 621 | 0xa3cfb3 | 0x99fb44 | EN | EN ; 5 l. / 116 px | B-670 : édition réservée |
| attaque / 622 | 0xa3d013 | 0x99fb48 | DE hors budget | DE exact ; 4 l. / 88 px | Corrigé et injecté |
| attaque / 625 | 0xa3d10e | 0x99fb54 | EN | EN ; 5 l. / 109 px | B-670 : édition réservée |
| attaque / 626 | 0xa3d16c | 0x99fb58 | EN | EN ; 5 l. / 108 px | B-670 : édition réservée |
| attaque / 627 | 0xa3d1c9 | 0x99fb5c | EN | EN ; 5 l. / 109 px | B-670 : édition réservée |
| attaque / 628 | 0xa3d228 | 0x99fb60 | EN | EN ; 5 l. / 107 px | B-670 : édition réservée |
| attaque / 629 | 0xa3d286 | 0x99fb64 | EN | EN ; 4 l. / 120 px | B-670 : édition réservée |
| attaque / 630 | 0xa3d2d5 | 0x99fb68 | EN | EN ; 4 l. / 118 px | B-670 : édition réservée |
| attaque / 631 | 0xa3d325 | 0x99fb6c | EN | EN ; 4 l. / 106 px | B-670 : édition réservée |
| attaque / 633 | 0xa3d3ca | 0x99fb74 | EN | EN ; 5 l. / 111 px | B-670 : édition réservée |
| attaque / 634 | 0xa3d424 | 0x99fb78 | EN | EN ; 5 l. / 103 px | B-670 : édition réservée |
| attaque / 635 | 0xa3d47d | 0x99fb7c | EN | EN ; 5 l. / 97 px | B-670 : édition réservée |
| attaque / 636 | 0xa3d4d0 | 0x99fb80 | EN | EN ; 5 l. / 113 px | B-670 : édition réservée |
| attaque / 637 | 0xa3d530 | 0x99fb84 | EN | EN ; 4 l. / 106 px | B-670 : édition réservée |
| attaque / 638 | 0xa3d56d | 0x99fb88 | EN | EN ; 4 l. / 96 px | B-670 : édition réservée |
| attaque / 641 | 0xa3d652 | 0x99fb94 | EN | EN ; 5 l. / 113 px | B-670 : édition réservée |
| attaque / 646 | 0xa3d81d | 0x99fba8 | EN | EN ; 5 l. / 112 px | B-670 : édition réservée |
| attaque / 647 | 0xa3d87a | 0x99fbac | EN | EN ; 5 l. / 96 px | B-670 : édition réservée |
| attaque / 648 | 0xa3d8c9 | 0x99fbb0 | EN | EN ; 5 l. / 112 px | B-670 : édition réservée |
| attaque / 651 | 0xa3d9cd | 0x99fbbc | EN | EN ; 5 l. / 112 px | B-670 : édition réservée |
| attaque / 652 | 0xa3da2c | 0x99fbc0 | EN | EN ; 5 l. / 109 px | B-670 : édition réservée |
| attaque / 653 | 0xa3da7e | 0x99fbc4 | EN | EN ; 5 l. / 112 px | B-670 : édition réservée |
| attaque / 659 | 0xa3dc7c | 0x99fbdc | EN | EN ; 5 l. / 105 px | B-670 : édition réservée |
| attaque / 661 | 0xa3dd2a | 0x99fbe4 | EN | EN ; 5 l. / 110 px | B-670 : édition réservée |
| attaque / 662 | 0xa3dd88 | 0x99fbe8 | EN | EN ; 5 l. / 106 px | B-670 : édition réservée |
| attaque / 663 | 0xa3dde1 | 0x99fbec | EN | EN ; 5 l. / 112 px | B-670 : édition réservée |
| attaque / 664 | 0xa3de3f | 0x99fbf0 | EN | EN ; 5 l. / 114 px | B-670 : édition réservée |
| attaque / 667 | 0xa3df4d | 0x99fbfc | EN | EN ; 5 l. / 110 px | B-670 : édition réservée |
| attaque / 669 | 0xa3dfd8 | 0x99fc04 | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 673 | 0xa3e0ea | 0x99fc14 | EN | EN ; 5 l. / 95 px | B-670 : édition réservée |
| attaque / 675 | 0xa3e195 | 0x99fc1c | EN | EN ; 5 l. / 102 px | B-670 : édition réservée |
| attaque / 678 | 0xa3e256 | 0x99fc28 | EN | EN ; 4 l. / 119 px | B-670 : édition réservée |
| attaque / 679 | 0xa3e2a6 | 0x99fc2c | EN | EN ; 4 l. / 113 px | B-670 : édition réservée |
| attaque / 680 | 0xa3e2ee | 0x99fc30 | EN | EN ; 4 l. / 112 px | B-670 : édition réservée |
| attaque / 682 | 0xa3e37b | 0x99fc38 | EN | EN ; 4 l. / 111 px | B-670 : édition réservée |
| attaque / 683 | 0xa3e3c8 | 0x99fc3c | EN | EN ; 4 l. / 107 px | B-670 : édition réservée |
| attaque / 685 | 0xa3e462 | 0x99fc44 | EN | EN ; 4 l. / 94 px | B-670 : édition réservée |
| attaque / 686 | 0xa3e4a6 | 0x99fc48 | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 687 | 0xa3e4ef | 0x99fc4c | EN | EN ; 4 l. / 108 px | B-670 : édition réservée |
| attaque / 688 | 0xa3e538 | 0x99fc50 | EN | EN ; 4 l. / 101 px | B-670 : édition réservée |
| attaque / 689 | 0xa3e580 | 0x99fc54 | EN | EN ; 4 l. / 101 px | B-670 : édition réservée |
| attaque / 692 | 0xa3e63a | 0x99fc60 | EN | EN ; 4 l. / 88 px | B-670 : édition réservée |
| attaque / 694 | 0xa3e6c4 | 0x99fc68 | EN | EN ; 4 l. / 101 px | B-670 : édition réservée |
| attaque / 695 | 0xa3e70b | 0x99fc6c | EN | EN ; 4 l. / 100 px | B-670 : édition réservée |
| attaque / 697 | 0xa3e795 | 0x99fc74 | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 698 | 0xa3e7df | 0x99fc78 | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 699 | 0xa3e82a | 0x99fc7c | EN | EN ; 4 l. / 102 px | B-670 : édition réservée |
| attaque / 702 | 0xa3e904 | 0x99fc88 | EN | EN ; 4 l. / 104 px | B-670 : édition réservée |
| attaque / 703 | 0xa3e94c | 0x99fc8c | EN | EN ; 4 l. / 107 px | B-670 : édition réservée |
| attaque / 704 | 0xa3e998 | 0x99fc90 | EN | EN ; 4 l. / 108 px | B-670 : édition réservée |
| attaque / 705 | 0xa3e9e4 | 0x99fc94 | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 707 | 0xa3ea7b | 0x99fc9c | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 708 | 0xa3eac2 | 0x99fca0 | EN | EN ; 4 l. / 106 px | B-670 : édition réservée |
| attaque / 709 | 0xa3eb0d | 0x99fca4 | EN | EN ; 4 l. / 97 px | B-670 : édition réservée |
| attaque / 711 | 0xa3eb9c | 0x99fcac | EN | EN ; 4 l. / 101 px | B-670 : édition réservée |
| attaque / 712 | 0xa3ebe3 | 0x99fcb0 | EN | EN ; 4 l. / 92 px | B-670 : édition réservée |
| attaque / 713 | 0xa3ec26 | 0x99fcb4 | EN | EN ; 4 l. / 118 px | B-670 : édition réservée |
| attaque / 714 | 0xa3ec76 | 0x99fcb8 | EN | EN ; 4 l. / 114 px | B-670 : édition réservée |
| attaque / 715 | 0xa3ecc8 | 0x99fcbc | EN | EN ; 4 l. / 104 px | B-670 : édition réservée |
| attaque / 716 | 0xa3ed0e | 0x99fcc0 | EN | EN ; 4 l. / 122 px | B-670 : édition réservée |
| attaque / 717 | 0xa3ed59 | 0x99fcc4 | EN | EN ; 4 l. / 116 px | B-670 : édition réservée |
| attaque / 718 | 0xa3eda8 | 0x99fcc8 | EN | EN ; 4 l. / 105 px | B-670 : édition réservée |
| attaque / 719 | 0xa3edf3 | 0x99fccc | EN | EN ; 4 l. / 98 px | B-670 : édition réservée |
| attaque / 720 | 0xa3ee3a | 0x99fcd0 | EN | EN ; 4 l. / 117 px | B-670 : édition réservée |
| attaque / 723 | 0xa3ef25 | 0x99fcdc | EN | EN ; 4 l. / 116 px | B-670 : édition réservée |
| attaque / 724 | 0xa3ef73 | 0x99fce0 | EN | EN ; 4 l. / 114 px | B-670 : édition réservée |
| attaque / 725 | 0xa3efbd | 0x99fce4 | EN | EN ; 4 l. / 108 px | B-670 : édition réservée |
| attaque / 728 | 0xa3f0a1 | 0x99fcf0 | EN | EN ; 4 l. / 94 px | B-670 : édition réservée |
| attaque / 732 | 0xa3f1bc | 0x99fd00 | EN | EN ; 4 l. / 96 px | B-670 : édition réservée |
| attaque / 733 | 0xa3f202 | 0x99fd04 | EN | EN ; 4 l. / 109 px | B-670 : édition réservée |
| attaque / 734 | 0xa3f24a | 0x99fd08 | EN | EN ; 4 l. / 115 px | B-670 : édition réservée |
| attaque / 736 | 0xa3f2e3 | 0x99fd10 | EN | EN ; 4 l. / 103 px | B-670 : édition réservée |
| attaque / 737 | 0xa3f32a | 0x99fd14 | EN | EN ; 4 l. / 117 px | B-670 : édition réservée |
| attaque / 738 | 0xa3f377 | 0x99fd18 | EN | EN ; 4 l. / 117 px | B-670 : édition réservée |
| attaque / 739 | 0xa3f3c7 | 0x99fd1c | EN | EN ; 4 l. / 119 px | B-670 : édition réservée |
| attaque / 740 | 0xa3f410 | 0x99fd20 | EN | EN ; 4 l. / 100 px | B-670 : édition réservée |
| attaque / 744 | 0xa3f53a | 0x99fd30 | DE hors budget | DE exact ; 3 l. / 110 px | Corrigé et injecté |
| attaque / 747 | 0xa3f612 | 0x99fd3c | DE hors budget | DE exact ; 4 l. / 103 px | Corrigé et injecté |
| attaque / 750 | 0xa3f6fb | 0x99fd48 | DE hors budget | DE exact ; 3 l. / 114 px | Corrigé et injecté |
| attaque / 751 | 0xa3f74b | 0x99fd4c | DE hors budget | DE exact ; 4 l. / 92 px | Corrigé et injecté |
| attaque / 754 | 0xa3f832 | 0x99fd58 | DE hors budget | DE exact ; 4 l. / 120 px | Corrigé et injecté |
| attaque / 758 | 0xa3f985 | 0x99fd68 | DE hors budget | DE exact ; 5 l. / 93 px | Corrigé et injecté |
| attaque / 759 | 0xa3f9d8 | 0x99fd6c | DE hors budget | DE exact ; 4 l. / 118 px | Corrigé et injecté |
| attaque / 820 | 0xa3fc31 | 0x99fe60 | DE hors budget | DE exact ; 4 l. / 121 px | Corrigé et injecté |
| CT/CS / 323 | 0x483f44 | 0x87980c | EN | DE exact ; 3 l. / 119 px | Corrigé et injecté |
| CT/CS / 326 | 0x484098 | 0x879890 | EN | DE exact ; 4 l. / 108 px | Corrigé et injecté |
| CT/CS / 399 | 0xa3a99e | 0x87a51c | EN | EN ; 4 l. / 111 px | Source corrigée ; attend B-1013 |
| CT/CS / 401 | 0xa39d8d | 0x87a574 | EN | EN ; 4 l. / 107 px | Source corrigée ; attend B-1013 |
| CT/CS / 409 | 0xa39198 | 0x87a6d4 | EN | EN ; 4 l. / 111 px | B-669 : édition réservée |
| CT/CS / 429 | 0xa3a733 | 0x87aa44 | EN | EN ; 4 l. / 110 px | Source corrigée ; attend B-1013 |
| CT/CS / 452 | 0x484986 | 0x87ae38 | EN | EN ; 4 l. / 106 px | Source corrigée ; attend B-1013 |
| CT/CS / 432 | 0xa3961d | 0x87aac8 | EN | EN ; 4 l. / 102 px | Source corrigée ; attend B-1013 |
