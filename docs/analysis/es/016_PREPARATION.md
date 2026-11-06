# ES-016 — relevé préalable et acheminement manquant

F-866, 6 novembre 2026. **Lot non livré : aucune traduction ni exclusion finale
n'est certifiée par cette préparation.** Le contexte A-663 confirme le projet
gba_translator ; D-849 et F-850 sont terminés et intégrés. Aucun combined,
manifeste de protection, glossaire ou contrat partagé n'est modifié.

## Périmètre et méthode

`016_PREPARATION.json` contient les **393 clés ordonnées exactes** de `lots.json`,
avec les textes historiques EN/ES/FR et alertes de l'inventaire, les préimages ROM
EN intégrales, les commandes avec leurs arguments, les occurrences absolues LE32
à tous alignements et leur contexte, les références intérieures, les débuts voisins
référencés et les correspondances ES prises exclusivement dans l'offset map.
Les empreintes EN/ES, offset map et six sources préservées sont consignées.
Une correspondance absente ou nulle n'est pas inventée depuis l'adresse ou la FR.

Reproduction :

```sh
python3 scripts/audit_es016_preparation.py
python3 scripts/audit_es016_preparation.py --probe-routing
python3 -m pytest tests/unit/test_es016_preparation.py -q
```

Le lecteur reconnaît les tailles FC du pipeline courant et les arguments FD/F8/F9,
avant d'interpréter FF comme terminateur. FA/FB restent des commandes distinctes,
FE une nouvelle ligne. Aucun F7 n'apparaît dans les préimages relevées ; la taille
F7 du pipeline n'est pas une preuve de sa grammaire moteur dans un autre contexte.
Le décodage reste un diagnostic, notamment pour l'ellipse B0 et les débuts binaires.
Le plus long relevé mesure 500 octets FF inclus : aucun plafond arbitraire 512
n'a été utilisé pour couper les préimages.

Répartition historique conservée : 359 identiques à EN, 31 différentes, 3 absentes
d'ES. 358 clés ont une occurrence binaire directe et 35 n'en ont pas ; 98 préimages
contiennent une cible intérieure. **Ces occurrences ne certifient pas des lecteurs
de texte** : des instructions ARM/Thumb, scripts et données peuvent coïncider.
Inversement, l'absence de pointeur absolu ne prouve pas une chaîne morte.
La zone reste explicitement non qualifiée plutôt que déduite de l'adresse.

Les trois absences ES disposent d'une préimage EN reconstruite : 0x771127
est la notice des services locaux (lecteur `0F 00` à 0x77111F), 0x776047 le
compteur `Missions Completed: FC 01 06 FD 04` avec neuf références recensées,
et 0x78D7C8 le panneau `Cinder Volcano West` (lecteur à 0x78D7C0).
Le caractère « Ç » de l'inventaire du compteur est l'argument 04 du tampon FD,
pas une lettre à traduire. Le relevé ne substitue pas la FR à ces sources EN.

## Blocage reproduit : sept clés disparaissent avant le builder

`016_ROUTES.json` isole dix clés précédées de AA, sans occurrence absolue vers
la clé contractuelle et avec références à +1. Aucun contrat TextAliases ne les
couvre dans les sources relevées. Trois cibles sont déjà d'autres clés du même lot :
0x7808DD/0x7808DE, 0x788537/0x788538, 0x78D43D/0x78D43E. Leur stratégie canonique
doit éviter toute double injection ; AA ne devient pas un caractère espagnol.

Les sept autres candidats sont :

| Clé du lot | Début référencé | Sites des références |
|---|---|---|
| 0x772093 | 0x772094 | 0x762C7F |
| 0x780E33 | 0x780E34 | 0x9047D0 |
| 0x781278 | 0x781279 | 0x877344 |
| 0x781668 | 0x781669 | 0x765974 |
| 0x788255 | 0x788256 | 0x7C871E, 0x7C8745 |
| 0x78C2A8 | 0x78C2A9 | 0x78C280 |
| 0x78C2FD | 0x78C2FE | 0x78C2C0 |

La sonde utilise les sept clés contractuelles dans un combined temporaire, avec
une sentinelle et le texte EN reconstruit, puis appelle le vrai
`build_language.generate_translation_json` avec les contrats actuels. Elle ne
modifie aucun combined de production et ne construit aucune ROM sentinelle.
Résultat dans `016_ACHEMINEMENT_REPRO.json` : **sept absences de l'extraction EN,
zéro entrée JSON, zéro route résolue**. La conversion termine pourtant sans erreur.
Un import à ces clés suivi d'un simple build vert ne satisferait donc pas le ticket.
Les sept vrais débuts ont chacun un match ES explicite dans l'offset map ; leurs
préimages ES sont incluses, sans approbation linguistique implicite.

B-1030/B-1032/F-1035/F-1037 fournissent les mécanismes réutilisables mais pas ces
contrats. F-1041 couvre ES-011, F-1042 les descriptions ES-014 et F-1043 ES-015 :
leurs descriptions ont été consultées ; aucune ne couvre ces sept clés.
Le ticket interdit de modifier l'infrastructure partagée dans ce lot. Un prérequis
technique distinct doit qualifier ces consommateurs et fenêtres et configurer
les seules routes nécessaires, sans étendre la sélection ni changer les traductions.

## Débuts de scripts et coïncidences à ne pas traiter comme alias

0x76D073, 0x76D3CC et 0x76D46A commencent par une structure trainerbattle
(`5C 00 …`) avant les messages à +23 : 0x76D08A, 0x76D3E3, 0x76D481. Les références
internes sont dans la structure elle-même. 0x77F0C4 commence par `0F 00 D0 F0 77 08`
avant le panneau 0x77F0D0 déjà sélectionné. 0x77FF0F commence au milieu des
instructions avant le message 0x77FF15 ; 0x78069E contient 24 octets de script
avant 0x7806B6. Ce ne sont pas des préfixes textuels à importer aveuglément.
Les octets et les sites correspondants restent disponibles pour qualification.

0x78117E contient la description complète de Sludge Wave sans référence absolue
directe identifiée ; les occurrences à +2/+6 ont des contextes d'instructions
dans le code. Elles ne prouvent pas que « It » est du bourrage. 0x78122B présente
également des occurrences intérieures non qualifiées dans du code. Les fragments
`terfall.`, `cicle Cave`, `entre`, ` PKMN Centre` ou `k Cave South` doivent être
reconstruits depuis leurs consommateurs avant décision, jamais traduits comme
des phrases autonomes ni exclus seulement faute de pointeur.

## Validation et travail restant

Les trois gardes ciblées passent : contrat exact, préimages rejouables et tailles
des commandes (y compris FF en argument), préfixes et trois doublons. Ruff passe
sur le script et les tests ajoutés. `make build-es-maint` réussit sur les sources
existantes sans import ES-016 ; son succès n'est pas une preuve de traduction.
Les résultats de la suite standard, des hooks et du témoin FR seront consignés
dans la résolution de préparation avant mise en attente.

La suite standard `make test-python` est terminée : **10 074 passed,
54 skipped, 4 472 deselected**, aucun échec ni erreur (765,14 s).
Les skips ne sont pas revendiqués comme des réussites ; aucune garde n'a été
modifiée. Le Python système de cette première passe est 3.9 ; les hooks sont
ensuite exécutés avec un environnement temporaire Python 3.14 conforme au
`requires-python >=3.11`, avec pytest/PyYAML/Pillow/Ruff installés hors dépôt.

Build es-maint témoin : SHA-256
`32794a3d9d544db9960a59f89608a6f3145879bfe4ed76baf7fc70ff5bb8976a`.
Le premier essai FR a utilisé un ancien JSON dont la copie locale avait rafraîchi
la date : la vérification du message 0x1A63E8 a correctement refusé ce build.
Après `make prepare-fr`, le build FR complet réussit avec BUILD_NUMBER=0 :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
La copie binaire témoin est conservée hors dépôt pour comparaison après les hooks.

`QT_QPA_PLATFORM=offscreen PYTEST_ADDOPTS=--maxfail=1 make test-rom` a été exécuté :
24 réussites, 3 skips, arrêt sur
`tests/e2e/de/test_item_names_objets_01.py::test_all_live_names_metadata_and_remaining_cells`
car `GenedRom-de.gba.item-names.bak` n'existe pas dans les artefacts matérialisés
depuis les BPS. Aucun test ni garde n'est modifié pour masquer cette limite ;
aucune certification globale des ROM distribuées n'est revendiquée.

Après le prérequis : qualifier les scripts et zones, reconstruire les chaînes
partielles, relire les 31 différences ES et les trois absences, traduire/importer
chirurgicalement avec protections exactes, justifier chaque conservation/exclusion,
mesurer cellules/pixels/pages, contrôler les octets à tous les pointeurs vivants,
rebuild ES et témoin FR identique, puis assertions Playwright headless en mGBA
offscreen et capture attachée. Aucune modification d'affichage n'est produite par
la présente préparation ; aucune preuve visuelle de traduction n'est revendiquée.
