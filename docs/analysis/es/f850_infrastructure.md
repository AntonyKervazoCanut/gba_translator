# Infrastructure de l'espagnol maintenu — F-850

Dépendances consultées : audit A-663 intégré (6988ec86), glossaire D-849 terminé
(753e30ee). La cible reste **in_progress** ; aucune traduction n'est certifiée ici.

## Préservation des sources

Création initiale expressément autorisée de `combined_es-maint.txt`, ne contenant que
des commentaires, et de `protected_entries.yaml` avec `entries: []`. Zéro entrée
recopiée depuis ES. Les futurs lots ajoutent leurs valeurs vérifiées et protégées
ensemble, sans régénérer les sources existantes.

Empreintes SHA-256 relevées avant toute modification et vérifiées après :

| Source | Avant = après |
|---|---|
| `languages/en/combined_en.txt` | `65e93f43b9f92f19ba011fb4971aea6f44d9cd419363d7b51d9dbe094235af19` |
| `languages/es/combined_es.txt` | `2c38c5949a3c5df46758abb7b58d156e72cae753c64b4dfcc4f74bf1af0bb591` |
| `languages/fr/combined_fr.txt` | `b5ec52f6aa0c488006b66946141a9f416bf81beb6c07b248a3e69a8fff602520` |
| `input/roms/englishrom.gba` | `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7` |
| `input/roms/spanishrom.gba` | `a98a14adc231327db22baa7d7762b95abc0fe5bfe6fcc64e38a2c6b525429ff6` |

Deux reconstructions FR complètes avec les mêmes sources et `BUILD_NUMBER=0`, avant
et après modification du code partagé, sont identiques octet par octet (`cmp`) :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
La recette `build-fr`, `build-es` et le pipeline historique ne sont pas modifiés.
Le nouveau S du marquage ES est une entrée supplémentaire dans le dictionnaire de
pixels partagé ; les marquages FR/IT/DE conservent leurs octets.

## Encodage, polices et statuts

Octets attendus **littéraux**, hors terminateur :

```text
á é í ó ú ü ñ Á É Í Ó Ú Ü Ñ ¡ ¿
17 1B 6F 23 27 F6 29 02 06 5A 0E 12 F3 14 52 51
```

Les slots de ponctuation sont ceux de la
[charmap FireRed de pret](https://github.com/pret/pokefirered/blob/master/charmap.txt).
Le profil est explicite dans les arguments du builder et de l'étape inline ; les
alias historiques par défaut donnent toujours `üÜ¡¿ → E9 CF AB AC`. Le builder ES
historique ne reçoit pas cette option. Les caractères TypeScript sont synchronisés.

Les six blocs latins compressés sont complétés uniquement pour Ü/ü après les deux
réparations LZ77. Les heuristiques générales acceptent aussi un graphisme à 0x40C650 :
la sélection ES exige les deux paires latines Ë/E et ë/e pour préserver ce graphisme.
Les cinq polices natives du moteur sont conservées ; les tests ROM comparent les
16 cellules aux sources. Les statuts texte sont contrôlés aux pointeurs vivants de
la table 0x3DFE18 (stride 8), avec des attentes binaires indépendantes de l'encodeur.

Les quatre blocs de badges (0xB1E11C, 0xB1E280, 0xE82EA0, 0xE9BF48) rendent
ENV/PAR/DOR/CON/QUE et DEB. Les libellés viennent du glossaire et du descripteur ;
le patch conserve bordures, palettes et cellules non concernées. Il refuse un
recompactage qui écraserait des octets non libres. Aucun patch de contenu FR n'est
copié dans le descripteur.

## Preuve en émulateur

```sh
npx playwright test --config tests/e2e-playwright/es-maint.config.ts
```

Le test démarre une copie temporaire de la ROM dans mGBA avec
`QT_QPA_PLATFORM=offscreen`, sans sauvegarde. Après le boot réel, une sonde Thumb en
RAM appelle les cinq décompresseurs de glyphes originaux (0x08006448, 0x080064F0,
0x080065B8, 0x08006724, 0x080067EC), avec les 16 codepoints littéraux. Leurs buffers
rendus par le moteur sont dessinés dans une mire GBA. Les badges et la bande de
version sont décompressés par le BIOS depuis les assets réellement injectés.

Playwright headless compare les pixels de chaque glyphe aux données 2bpp natives,
contrôle les six badges dans les quatre blocs et le S du préfixe ES. La capture
est produite **après** les assertions dans le répertoire temporaire de l'OS puis
attachée au ticket, sans être ajoutée au dépôt. Cette mire teste les fonctions de
rendu et les assets ; elle ne remplace pas un parcours de traduction en jeu.

## Builds et conditionnement locaux

Deux invocations complètes de `make build-es-maint BUILD_NUMBER=0`, après ajout du
S au marquage de version, sont identiques octet par octet :
`43504c10e47ff2ff655d0fcecf5cbc5030c1b30902d7c549ca4b9cdd194c33c0`.

`make build-it` et `make build-de` réussissent sur le code partagé modifié.
Le conditionnement local de la seule cible es-maint via `PatchReleasePackager`
vérifie le round-trip BPS sur la ROM complète et conserve `status: in_progress`
dans le manifeste. L'artefact reste sous `output/release/es-maint-local/` ; aucune
mise à jour du bundle de distribution ni publication n'est effectuée.

## Contrôles des artefacts distribués

`make test-rom` a été exécuté après la reconstruction FR. Cette cible matérialise
les **BPS versionnés**, puis teste ces instantanés : 794 succès, 47 skips existants,
343 échecs. Les échecs portent sur une description CT/CS FR et sur des lots DE dont
les sources/tests sont plus récents que les BPS distribués. D-849 signalait déjà
cette dérive (139 échecs avec son corpus antérieur) ; de nouveaux tests DE ont été
intégrés depuis. Aucun test existant, hash de distribution ou bundle BPS n'est
modifié pour masquer ces écarts. Les builds locaux FR/IT/DE sont conservés séparément
de cette matérialisation pour les contrôles de source.

Les nouveaux tests ROM es-maint sont des contrôles de build privé explicitement
lancés après `make build-es-maint`, car aucun BPS es-maint n'est encore versionné :

```sh
python3 -m pytest tests/e2e/es/test_maintained_infrastructure.py -m rom
```

Ils vérifient les pointeurs et octets des statuts, les 16 glyphes des cinq polices
moteur, les six polices compressées et la conservation du graphisme non latin.
Aucun skip n'est ajouté dans ces tests.

## Résultats locaux sur les sources

- `make test-python` : 2 878 succès, 3 skips préexistants, aucun échec.
- `make sync-charmap-check`, contrôle TypeScript et Ruff des nouveaux fichiers : OK.
- Playwright headless : 1 succès, capture finale attachée au ticket (polices,
  quatre jeux de six statuts et préfixe ES.2.1.0).
- `make -o materialize-test-roms test-rom` sur les reconstructions locales :
  1 148 succès, 32 skips existants, **un échec**. Cette option empêche seulement la
  rematérialisation des anciens BPS ; la sélection des tests est inchangée.
  L'échec est l'assertion SHA-256 global du test Corps Gel, déjà relevée par D-849,
  qui exige le hash exact du BPS FR versionné. Ses attentes ne sont pas modifiées.
  Le message a été vérifié indépendamment au pointeur vivant 0x3FE3D8, commandes
  **FD 18**, **FD 0F**, saut FE, texte et terminateur compris :

```text
FD 18 00 D8 D9 00 FD 0F FE E6 D9 E7 E8 D5 E9 E6 D9 00 E7 D9 E7 00 CA D0 00 AB FF
```

## Vérification après rebase d'intégration

Le rebase conserve les tildes PT-BR (slots 60–63), le profil explicite ES et les
contrôles de fenêtres structurées DE. Les conflits étaient limités à l'ajout de
ces constantes dans `text_codec.py` et aux imports du builder ; les deux
charmaps TypeScript ont été régénérées depuis la table canonique fusionnée.
Les sources combined EN/ES/FR gardent les empreintes ci-dessus.

- `make lint` : 4 311 tests collectés, aucune erreur.
- `npx tsc --noEmit` et `make sync-charmap-check` : succès.
- `make test-python` après rebase : **2 966 succès**, 3 skips préexistants,
  1 342 tests désélectionnés, aucun échec.
- Les nouvelles gardes PT (tildes, polices natives) et DE (67 chaînes structurées)
  sont incluses dans cette passe ; leurs tests ont été relus.

Un échec transitoire du test d'idempotence des icônes IT a révélé une collision
entre suites concurrentes : une ROM sous un nom fixe dans `/tmp` avait été
tronquée par l'autre processus (lecture intermédiaire vide). Les trois tests
écrivant ces ROMs utilisent désormais `tmp_path`, sans modifier leurs assertions
ni le patch de production. Deux exécutions simultanées du fichier corrigé
réussissent chacune leurs **11 tests**. Aucun test n'a été neutralisé.

## Limites de périmètre

Les dialogues, noms, types et autres contenus restent à traiter par ES-001 à ES-063.
Aucun lot n'est importé ici et aucun statut complete n'est attribué. La certification
intégrale, y compris les parcours de gameplay et les graphismes hors statuts/polices,
reste à T-914. Aucun push ni déclenchement de pipeline distant.
