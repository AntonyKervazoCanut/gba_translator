# ES-015 — préparation et prérequis d’acheminement

F-865, 6 novembre 2026. **Lot non livré : aucune traduction, exclusion finale ni
certification d’affichage revendiquée.** Le contexte A-663 confirme gba_translator ;
D-849 et F-850 sont terminés et intégrés. Le glossaire, l’infrastructure, les
combined et les protections restent inchangés.

## Relevé reproductible des 393 clés

`015_PREPARATION.json` conserve exactement les clés ordonnées d’ES-015 dans
`lots.json`, sans sélection par plage ni `--skip-existing`. Chaque ligne contient
l’inventaire historique EN/ES/FR, la préimage actuelle EN, sa taille avec FF,
les commandes avec leurs arguments, les occurrences binaires de pointeurs à tous
les alignements et leur contexte, les cibles intérieures et voisines ainsi que
la correspondance ES de l’offset map. Les sources et l’offset map sont identifiées
par SHA-256. Une cible ES nulle ou absente reste explicitement non reconstruite.
L’égalité des adresses n’est jamais utilisée comme preuve de correspondance ES.

Le relevé parcourt les octets jusqu’au terminateur FF **hors arguments de
commandes**, sans plafond 512. FC utilise les tailles de `FC_ARG_COUNTS` dans
`apply_inline_overrides_fr.py`, FD/F8/F9 consomment un argument, FA/FB aucun.
Aucun F7 n’a été rencontré ; il faudra vérifier sa grammaire moteur s’il apparaît
lors d’une reconstruction. Les commandes sont rendues entièrement en hexadécimal,
jamais comme des accents ou des lettres. FE reste une nouvelle ligne. Les
préimages qui commencent dans des structures binaires ne sont pas pour autant
validées comme texte. Le plus long relevé mesure 433 octets, FF inclus.

Scan utilisé : toutes les fenêtres de quatre octets de la ROM EN sont interprétées
comme pointeurs little-endian ; les sites visant les préimages sont retenus,
y compris les sites non alignés. Le contexte de chaque site permet sa relecture
dans les scripts. On trouve 299 clés avec au moins une occurrence binaire et
94 sans référence absolue directe. **Une occurrence ne prouve pas un lecteur de
texte ; son absence ne prouve pas une chaîne morte.** Les zones restent donc
explicitement à qualifier depuis les racines de scripts, jamais depuis l’adresse.

## Onze débuts décalés non configurés

`015_ROUTES.json` gèle les onze candidats à +1, avec préfixe, préimages EN/ES,
références exhaustives et contexte. Aucun n’est couvert par `TextAliases` au
moment du relevé. Les tickets B-1030/B-1032/F-1035/F-1037 ont livré le mécanisme
partagé, mais pas ces contrats ; F-1041 concerne exclusivement ES-011.

| Clé contractuelle | Début référencé | Préfixe | Observation |
|---|---|---|---|
| 0x721427 | 0x721428 | 20 | MONEAN CHAMBER ; qualifier la cellule réelle |
| 0x721437 | 0x721438 | 00 | seconde clé déjà dans ES-015 |
| 0x745A54 | 0x745A55 | AA | explication Medalla/MO, lecteur à 0x741868 |
| 0x74BE3C | 0x74BE3D | AA | explication évolution, lecteur à 0x740198 |
| 0x74BF85 | 0x74BF86 | AA | seconde clé déjà dans ES-015 |
| 0x74ED62 | 0x74ED63 | AA | lecteur à 0x744D43 |
| 0x75100E | 0x75100F | AA | lecteur à 0x74BD41 |
| 0x75350F | 0x753510 | AA | lecteur à 0x75249B |
| 0x755532 | 0x755533 | AA | lecteur à 0x7524AF |
| 0x75B4BB | 0x75B4BC | AA | lecteur à 0x75450E |
| 0x75B6F4 | 0x75B6F5 | AA | lecteur à 0x16A79A |

Ces préfixes ne doivent pas devenir du texte traduit. Le prérequis technique doit
certifier les consommateurs, budgets et préimages, ajouter les contrats nécessaires
en réutilisant TextAliases et fixer le traitement canonique des deux doublons,
sans affaiblir `check_keys`. Ajouter simultanément les deux clés au combined
échouerait à juste titre. Les neuf autres débuts nécessitent une route conservant
la clé contractuelle plutôt qu’une traduction ajoutée hors liste.

## Lecteurs intérieurs et faux textes

67 préimages contiennent au moins une cible binaire intérieure ; la liste complète
et les sites sont dans le JSON. Ce nombre inclut des candidats binaires qui peuvent
être fortuits : **ce ne sont pas 67 suffixes textuels certifiés**. Avant toute écriture,
il faut qualifier ces lecteurs et préserver ceux qui ne sont pas sélectionnés.
Exemple concret : la chaîne 0x741625 a une référence de message à 0x740136 et
des lectures intérieures à 0x741693/0x7416B5/0x7416D6. Les sites 0x741548 et
0x741565 sont précédés de `0F 00`, tandis que 0x74155A est précédé de `06 01`.
Une traduction de la chaîne entière ne doit donc pas déplacer arbitrairement ces
lecteurs ni les laisser lire un milieu de phrase espagnole. Le prérequis doit
vérifier le comportement du builder et des patches finaux, et fournir uniquement
l’adaptation mécanique indispensable ; la sélection linguistique reste ici.

À 0x74037D, la référence 0x762EE5 suit `4F FF 00` : il s’agit du branchement
vers du bytecode `11 FE`, avant le vrai message à 0x74037F, lu à 0x78942E.
À 0x745132, la référence 0x744F99 suit `06 01` ; le bloc contient ensuite
`0F 00 CA 56 7C 08 09 06 02` avant le vrai texte à 0x74513B, lu à 0x744F9F.
Les observations concordent avec l’audit PT-20, mais ne constituent pas une
permission d’importer son patch, sa traduction ou ses clés hors sélection.
À 0x74B293, onze octets de script précèdent le panneau référencé à 0x74B29E,
qui est déjà une autre clé du lot. Il ne faut pas créer un alias textuel de ce script.

0x721340 commence dans `MapConnections` de la Route 3. Le pointeur de données
à 0x777C0C vise 0x721344 et ne prouve aucun consommateur de texte. La garde
FR existante `tests/unit/fr/test_route3_dresco_connection_guard.py` documente
ce danger. L’inventaire EN de 0x72134C est vide, mais la ROM actuelle contient
`Parent and child attack together.` (33 octets avec FF) ; aucune référence absolue
directe n’a été trouvée à ce début. La préimage est reconstruite, mais son lecteur
et son statut restent à établir : aucune phrase ne doit être inventée depuis la FR.

Les entrées sans référence directe, hors neuf routes textuelles et doublons,
restent à qualifier dans F-865, sans les déléguer au prérequis. Les noms propres
Keith, Jack, Michael, Oscar, Julian, Daniel, Nathan et Ripper sont des candidats
à conservation selon D-849 ; ce n’est pas encore une validation de leurs usages.

## Vérification et suite

Les tests de préparation vérifient l’égalité ordonnée des 393 clés, les préimages,
les commandes complètes, les onze routes et leurs préfixes, les deux doublons,
et l’absence de qualification abusive d’une zone. Ils ne sont pas des tests de
traduction ou d’injection. Les résultats finaux des suites et des hooks sont consignés dans
l’orchestration avant la mise en attente. Le build es-maint de référence a réussi,
sans import ES-015 (SHA-256 :
`1f4f6e779586a4c91225f5fcc082e40d74d70407f985515015ba5b5ceada1ba2`).
Le témoin FR reconstruit avec BUILD_NUMBER=0 avant les hooks vaut
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863` ;
la comparaison après le second build doit réussir avant le checkpoint.
La première passe Python a rencontré un défaut de préparation locale : des
symlinks de ROM source résolvaient hors de la racine protégée du worktree.
Ils ont été remplacés par des copies locales identiques, sans
modifier les originaux ni assouplir la garde ; ses deux tests et les trois
tests de préparation passent ensemble. La suite standard a été relancée.

Cette seconde passe standard a donné 10 042 réussites, 6 skips et 24 erreurs
de fixture : `shutil.copy2` propageait les permissions 0444 aux copies temporaires
que les tests doivent modifier. Les permissions des seules copies locales
ont été corrigées, sans changement de contenu ni modification des originaux.
Les cinq modules concernés ont ensuite été relancés via `make test-python`
avec un filtre explicite : 42 réussites, 2 skips, aucun échec ni erreur ; les
24 cas auparavant en erreur sont sélectionnés : 23 passent et le cas FD
de `test_quality_gates.py` est ignoré par sa propre garde existante (aucun
texte FD éligible dans le JSON de référence). Aucune garde n’a été modifiée. La suite entière n’a pas été rejouée
après cette correction de préparation. Les hooks ont validé 9 924 tests Python
rapides (5 skips existants), 22 tests de workflow et 80 tests Vitest.

Le second build FR des hooks est strictement identique au témoin par `cmp`.
La campagne `make test-rom` a été interrompue après 573 réussites, 19 skips
et un échec DE dû au backup `GenedRom-de.gba.item-names.bak` absent ; elle
atteignait un ancien scénario mGBA sans configuration hors écran explicite.
Aucune réussite globale ROM n’est revendiquée ; aucun test n’a été assoupli.
La preuve d’affichage ES-015 reste à produire après les traductions.

Il reste à F-865, après intégration du prérequis : qualification des scripts/zonage,
relecture des 37 différences ES, reconstruction des références manquantes,
traduction/import chirurgical et protections exactes, rapport final des 393 décisions,
budgets réels, octets aux pointeurs vivants, builds ES et témoin FR aux mêmes sources,
tests Python et assertions Playwright headless en émulateur avec capture attachée.
Aucune modification visible n’est produite par cette préparation documentaire.
