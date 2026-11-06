# ES-012 — 374 décisions, 361 textes livrés

F-862, suite de A-663 dans gba_translator. D-849 et F-850 terminés et intégrés
ont été consultés avant la traduction. Le lot contractuel ES-012 de lots.json
est conservé intégralement, sans nouvelle sélection ni `--skip-existing`.

## Traitement exhaustif

[012_TRAITEMENT.json](012_TRAITEMENT.json) donne les 374 clés dans l'ordre du
contrat, les trois colonnes de l'inventaire, la préimage ROM EN complète, les
référents, la correspondance ES et chaque décision motivée.

| Décision | Nombre |
|---|---:|
| Traduit ou corrigé depuis EN vivant | 353 |
| Import communautaire fidèle, valeur ES exacte | 8 |
| Copie textuelle héritée non référencée, conservée sans injection | 4 |
| Fragment exclu, sans phrase inventée | 7 |
| Donnée graphique exclue | 2 |
| Total | 374 |

Les 361 valeurs sont ajoutées chirurgicalement au combined es-maint et
protégées exactement dans le même commit. Aucun ancien offset du combined
n'est réécrit, supprimé ou déplacé ; aucun offset d'un autre lot n'est ajouté.
Aucune écriture dans les combined ES référence, EN ou FR, le glossaire ou
l'infrastructure partagée. Les empreintes initiales des sources sont dans le JSON.

Le corpus nommé EN de l'inventaire contient notamment des descriptions FR.
La ROM EN canonique (`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`)
prime systématiquement. L'extraction EN locale a été isolée puis refaite depuis
cette ROM ; le cache historique du checkout principal n'a pas été réutilisé ni
modifié. Les offsets contractuels restent ceux du lot, malgré ces écarts de corpus.

## Consommateurs, correspondances et exclusions

- 296 fiches sont référencées par les champs primaires de la table Pokédex
  `0x1A35800`, stride 36. La surface est identifiée par la structure consommatrice,
  sans attribuer une carte ou un personnage depuis la banque ROM.
- 65 descriptions appartiennent aux ID 2 à 66 de gDecorations, racine
  `0x4556F8`, stride 32, description à +0x18 ; la racine est exportée par le
  champ d'en-tête `0x14C`. Aucun menu naturellement accessible n'est revendiqué.
- 289 correspondances EN→ES sont présentes dans l'offset map et concordent
  avec les pointeurs homologues des tables. Les 72 absences sont reconstruites
  depuis ces tables dans les deux ROMs, avec adresse et préimage ES par entrée.
  Une absence de texte EN dans l'inventaire n'a jamais été traduite depuis FR.
- Les huit imports (`44870B`, `448C25`, `44934A`, `4495BA`, `449D99`, `44A3D5`,
  `44A953`, `44AA17`) sont identiques aux chaînes ES aux pointeurs homologues.
  Les autres variantes sont retraduites pour rester fidèles au scénario EN,
  y compris modalités, nombres, qualificatifs et noms officiels des mouvements.
- `0x146B64` et `0xCBA129` sont deux coïncidences binaires, déjà qualifiées par
  B-686, pas des références vivantes. Le contrôle ROM garde leurs quatre octets
  intacts ; elles ne figurent pas parmi les consommateurs certifiés du rapport.
- Les copies non référencées sont `44E5F5`, `44E71C`, `44E785`, `44E7E6`.
  Aucun pointeur direct ni champ primaire des 1024 racines Pokédex ne les cible.
  Les voisins de `44E5F5` et du fragment `44E65D` ciblent un FF précédent :
  une chaîne secondaire vide, pas un alias vers la phrase suivante. Le test
  garde le pointeur et le FF, sans déplacer ce consommateur vers la copie.
- Les sept fragments (`44E65D`, `44E6C2`, `44E6CC`, `44E6D7`, `44E6DF`,
  `44E6F9`, `44E703`) et les deux données graphiques (`452FCB`, `453010`)
  sont laissés intacts. Les quatre copies conservées ne sont pas des noms
  officiels laissés en anglais ; ce sont des données sans consommateur retrouvé.

Les noms d'espèces contenus dans les phrases gardent leur graphie officielle
ES, généralement identique à EN. Les motifs des tapis emploient notamment Surf,
Trueno, Llamarada, Nieve Polvo, Atracción, Fisura et Púas. Aucun ajout promotionnel
n'est importé ; aucune phrase n'est reconstruite à partir d'un fragment.

## Octets, budgets et rendu

Toutes les chaînes vivantes sélectionnées sont de la prose sans FC/FD/F8/F9/F7,
ni FA/FB. Cette absence est vérifiée sur les préimages et les octets réencodés,
pas seulement sur des marqueurs décodés. Les exclusions gardent leurs préimages.
Le plafond 512 inclut FF ; le maximum livré est de 117 octets, avec trois lignes
au plus. Trois mises en page ont été adaptées au normaliseur du builder, dont
`4499BE`, qui serait sinon passée à quatre lignes. Une garde exécute ce
normaliseur sur les 361 valeurs et refuse toute réécriture des lignes relues.

La sonde RAM Playwright lance mGBA avec `QT_QPA_PLATFORM=offscreen`, sans
sauvegarde, sans port partagé et sans fenêtre visible. Pour les 361 chaînes,
elle lit leurs pointeurs finaux et appelle le vrai GetStringWidth, fonte normale
2 ; les maxima mesurés sont **232 px Pokédex** et **110 px décorations**.
Elle vérifie aussi longueur terminée et nombre de lignes. Les colonnes
`largeur_moteur_px`, `lignes_moteur`, `octets_moteur` conservent ces observations.

Six impressions utilisent AddTextPrinterParameterized3 du moteur, avec les trois
lignes simultanées. La sonde travaille en RAM et lit directement les chaînes de
la ROM livrée : aucun texte, glyphe ou pointeur ROM n'est remplacé par une mire.
Chaque ligne est contrôlée par OCR. L'OCR compare les mots sans ponctuation et
tolère les hampes i/l/1 ; les octets, accents et ponctuation ont leur vérification
binaire exacte indépendante. La capture est produite après les assertions, dans
le répertoire temporaire du système, puis attachée au ticket, jamais au dépôt.

La garde ROM contrôle les 361 valeurs à tous leurs référents, les deux faux
pointeurs, les 13 exclusions et les chaînes secondaires vides. Elle était rouge
sur la ROM témoin non traduite, puis passe sur le build livré.

## Reproduction et résultats

Environnement de validation : Python 3.14 isolé hors dépôt, dépendances du projet,
Pillow, Capstone, Unicorn, WebSockets et NumPy ; node_modules existants du projet.
Les artefacts de build restent locaux et ignorés par Git.

```sh
python3 src/extractors/pointer_text_extractor.py input/roms/englishrom.gba --output output/extracted/extracted_texts/englishrom_texts.json --scan-all-pointers
make build-es-maint
python3 -m pytest tests/unit/test_es012_translation.py -q
npx playwright test --config tests/e2e-playwright/es012.config.ts
make test-python
make -o materialize-test-roms test-rom
npx tsc --noEmit
```

Le dernier `test-rom` lit les reconstructions locales FR/IT/DE/Indie/PT/es-maint,
sans rematérialiser les anciens BPS versionnés. La certification des artefacts
distribués relève du ticket T-914. Les résultats finaux des suites globales et
après rebase sont consignés dans la résolution du ticket ; aucun échec de ces
suites n'est assimilé au succès des tests ciblés.

Un écart hors lot a été diagnostiqué dans la garde PT-22
`test_applymovement_and_accidental_code_pointers_are_unchanged` : le motif
`0F 00 78 08` à `0x1E93053` ressemble au pointeur `0x0878000F`, mais contient
l'opcode `loadpointer 0` et les deux premiers octets du vrai pointeur à
`0x1E93055`. PT-78 reloge légitimement le panneau `Frozen Heights` de
`0x1F70878` vers `0xB34364` (voir pt78_audit.json). La garde PT-22 exige encore
le motif brut original. Le mouvement `04 FE` à `0x778EAF` est intact.
Aucun fichier PT ni ce test n'est modifié par ES-012 ; cet écart ne doit pas
être présenté comme une corruption causée par les traductions espagnoles.

Résultat global sur ces six reconstructions : **4 226 réussis, 13 échecs,
31 ignorés, 9 874 désélectionnés**, 91 sous-tests réussis (1 218,98 s).
Aucun échec ES. Les 13 écarts concernent cinq gardes PT (PT-22, PT-69, deux
cas PT-72 et une classe PT-04), sept gardes DE (rival, F-601, trois descriptions
de combat et dialogues-09), et le hash de l'ancien BPS FR dans la garde Corps Gel.
Les différences de mots et de mise en page DE sont déjà présentes dans les
sources DE de la base, que ce ticket ne modifie pas. PT-72 attend encore le
buffer anglais « boy » là où une autre localisation livre « menino ».
Ces attentes inter-lots ne sont ni neutralisées ni corrigées dans ce lot ES.

Le hash FR reconstruit est `2c2f602e…c863`, alors que la garde Corps Gel exige
encore le hash distribué `c6031984…a7c4`. Les octets du message sont vérifiés
indépendamment à `0x3FE3D8 → 0x1AAF65`, y compris FD 18, FD 0F, FE et FF :
ils sont exacts. Le résultat global n'est donc pas présenté comme une
certification réussie des six langues ni des anciens patches de distribution.

Validation initiale de la ROM avant rebase : build es-maint réussi ; trois tests
ES-012 réussis ; Playwright headless réussi, 361 mesures et six impressions.
`make test-python` : 9 675 réussis, trois ignorés préexistants, 4 466 désélectionnés,
96 sous-tests réussis, aucun échec (599,07 s).
Hooks actifs : 9 534 tests Python rapides, 80 tests Vitest, builds FR/IT/DE réussis.
SHA-256 initial ES : `1cfbe1bbd84e429d98a76751cebaf785fd7de91ac3c846bfc24c1a8bd286f343`.
Les relevés finaux aux pointeurs après intégration sont joints au ticket si la
base a avancé ; ce hash est celui de la validation initiale, pas une promesse
sur les allocations d'un build enrichi par d'autres lots.

Le témoin FR contrôlé, reconstruit après préparation des extractions et avant
le build ES-012, est `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
La comparaison avant/après utilise les mêmes sources, paramètres et environnement ;
le résultat final est consigné au ticket. L'ancien artefact local produit avant
cette préparation n'est pas utilisé comme témoin comparable.

## Non vérifié

Besoin distinct d'infrastructure : le cache d'extraction devrait être lié au
SHA-256 de son entrée, et non accepté sur la seule présence de son fichier.
La commande d'extraction ci-dessus est nécessaire si un ancien cache FR porte
encore le nom EN. Ce lot corrige sa préparation locale, sans modifier le driver
partagé ni les caches du checkout principal.

La sonde certifie les octets, les métriques et l'impression native, pas un
parcours naturel de toutes les fiches ni l'accessibilité du menu décorations.
Le budget de 110 px reste une garde conservatrice de B-686, pas une mesure de
fenêtre obtenue depuis un appelant de ce menu. Aucun affichage simultané des
361 fiches, aucun changement de statut complete, aucun BPS de distribution,
aucun push et aucun déclenchement de pipeline distant.
