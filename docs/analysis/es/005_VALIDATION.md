# ES-005 — lexique Easy Chat

F-855. Liste contractuelle : 374 offsets, inchangée. D-849 et F-850 terminés
et intégrés avant traduction. Les sources ES de référence et FR restent intactes.

[005_TRAITEMENT.json](005_TRAITEMENT.json) fournit une décision par offset :
369 traductions, un import relu (`Sí`, espace terminal retiré), quatre formes
espagnoles identiques conservées (`NORMAL`, `RIVAL`, `LALALA`, `TERRIBLE`).
Aucune exclusion ni phrase reconstruite artificiellement. Les 374 valeurs sont
ajoutées chirurgicalement et protégées exactement dans le même commit.

## Référents réels

Les 374 chaînes sont des mots combinables Easy Chat, chacun avec une référence
unique dans une cellule de 12 octets (pointeur, index de tri, disponibilité).
La table de groupes est 0x3ECED4. Les groupes 2 à 9 correspondent à État,
Combat, Salutations, Personnes, Voix, Discours, Connecteurs, Émotions. Les
routines moteur qui lisent les groupes sont vérifiées aux sites 0xBD788,
0xBD7C0, 0xBD84C, 0xBDA38, 0xBDD2C, 0xBE270 et 0xBE414.
Ce sont des consommateurs globaux, sans attribution inventée à une carte.
Le rapport donne groupe, index, descripteur, pointeur EN, correspondance ES
issue de l’offset map et pointeurs ES. Aucun offset voisin n’est ajouté au lot.

Types selon D-849. Noms des talents selon la localisation es-ES de Platine,
[guide Nintendo, habilités](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/habilidades.html),
génération IV : formes compactes attestées telles que ESCAMA ESP., EFEC. ESPORA,
ABSOR. FUEGO et ESPÍR. VITAL. L’identité est celle du mot de la catégorie État,
pas un index supposé de la table CFRU des talents. Les autres mots sont traduits
comme lexèmes combinables et gardent leurs distinctions grammaticales lorsque
l’espagnol les exprime. TALENTO est ici le nom commun anglais TALENT, pas le
terme mécanique ability ; Movimiento appartient au lexique combat, pas au PC.
Daughter devient HIJA, sans reprendre « filleule » de la comparaison FR.
La relecture distingue aussi WINS (GANA, verbe), NO MATCH (NO SOY RIVAL,
infériorité et non invincibilité), MISS (FALLAR, rater) et GIDDY (MAREADO,
étourdi). Ces sens sont protégés par les gardes unitaires du lot.

## Contrôles

Aucune commande FC/FD/F8/F9/F7 ni FA/FB dans ces chaînes ; absence vérifiée
sur les préimages ROM et les valeurs encodées complètes. Aucun buffer ni page.
Au maximum 12 glyphes plus FF ; largeur mesurée dans les cinq polices moteur :
60 pixels pour la petite, 72 pour les quatre autres, enveloppe du lexique EN.
Le sélecteur conserve ses index et disponibilités ; aucun tri partagé modifié.
Les chaînes plus longues sont relocalisables via leur pointeur unique.

Environnement de validation : Python 3.14 (Python 3.15 supprime une API
`SourceFileLoader.load_module` encore utilisée par un test FR existant ;
aucun test du dépôt n’a été modifié pour contourner cette incompatibilité).

Commandes de reproduction :

```sh
make build-fr BUILD_NUMBER=0
make build-es-maint
python3 -m pytest tests/unit/test_es005_contract.py tests/e2e/es/test_es005_delivery.py -q
make test-python
npx playwright test --config tests/e2e-playwright/es005.config.ts
```

La suite ROM vérifie toutes les valeurs aux cibles vivantes, les métadonnées,
les descripteurs et les cellules non sélectionnées des huit groupes, les budgets
et les empreintes EN/ES/FR. Les cibles ne sont pas figées dans le rapport : le
build peut changer leur allocation ; elles sont résolues à chaque test.
Playwright contrôle huit rendus (un par groupe) dans l’imprimante native mGBA,
compare les pixels d’encre aux glyphes natifs et vérifie l’absence de débordement.
La copie temporaire ne modifie que le script de déclenchement ; les textes sont
lus aux pointeurs du build. Captures dans /tmp puis attachées au ticket.
Aucune sauvegarde en jeu, aucun navigateur visible.

## Non vérifié

Le parcours naturel de chaque sélection Easy Chat et toutes les combinaisons
possibles de mots ne sont pas certifiés par la sonde d’imprimante. Les huit
rendus ne constituent pas un parcours du sélecteur. L’ordre alphabétique des
index EN est conservé, conformément au périmètre sans modification technique
partagée. La certification globale et le statut complete restent à T-914.
Aucun push ni déclenchement de pipeline distant.

## Préparation des contrôles globaux

Le premier `make test-python` a exposé un prérequis local implicite du test
`test_de_certification_rebuilds_fr_it_before_shared_playwright` : même en dry run,
la recette récursive Make lit la ROM DE. Une construction locale IT/DE a fourni
les artefacts réels, sans modification de Make ni des tests partagés. Le test
et les contrôles IT auparavant privés de ROM passent ensuite : 18 réussites.
La suite globale est relancée sur cet environnement complet ; ses résultats
finaux et les hooks sont consignés dans la résolution du ticket.

Build es-maint vérifié :
`c415e3913a23dfc296746ebfe9dcafabd81efe05023e2c4b56967960999e141b`.
FR témoin, mêmes sources et numéro 0 :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Tests ES-005 : deux gardes unitaires et quatre contrôles ROM réussis.
Playwright headless : huit rendus réussis, un par groupe, captures attachées.
Ruff ciblé, TypeScript et contrôle du diff fermé réussis.

Validation globale finale avant commit : `make test-python` sous Python 3.14,
9 280 réussites, aucun échec, 7 skips préexistants, 4 402 désélections et
96 sous-tests réussis (520,37 s). Aucun skip ajouté par ES-005. La passe ciblée
finale donne 36 réussites ; les huit tests Playwright donnent huit réussites.
Les skips existants portent sur une sonde de mémoire émulateur non connectée,
une garde FD sans entrée vérifiable dans sa ROM de test, le CSV dynamique
historique absent, et quatre sondes ARM (préfixe et catégorie Pokédex) dont
le moteur Unicorn optionnel n’est pas installé.
Ils ne sont pas comptés comme vérifiés ; les contrôles propres au lot sont tous
exécutés. Les hooks obligatoires et l’intégration sont détaillés dans la
résolution du ticket.
