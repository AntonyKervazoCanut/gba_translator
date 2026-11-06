# ES-013 — Validation locale du checkpoint technique

F-1044, 6 novembre 2026. Ce checkpoint ne clôt pas le besoin de preuve moteur
sur les 54 descriptions de décorations. Aucun combined, protection, glossaire,
inventaire ou lots.json modifié ; aucun push ni pipeline distant.

## Pipeline réel et isolation

`prepare_es013_pipeline.py` a traversé le vrai CSV → JSON → builder → patches
avec **175 sentinelles uniques**, **241 références finales** et les préimages
EN propres. Les SHA-256 EN/ES et les correspondances ES uniques (ou
`only_in_english`) ont été contrôlés. Vingt clés restent contractuelles via
TextAliases ; aucun début vivant ajouté aux clés de production.

La comparaison intégrale avant patches autorise uniquement les allocations de
texte et les sites de pointeurs sélectionnés. La comparaison après patches
emploie un témoin soumis aux mêmes patches, sans traductions : aucune autre
différence. Cela couvre préfixes, structures, tables, voisins et branches hors
sélection ; chaque octet aux consommateurs est également vérifié individuellement.
Les premiers passages de 51 puis 175 sentinelles sur le cache historique étaient
également réussis. Le dernier passage utilise une extraction EN propre isolée,
nécessaire aux tests de livraison ES-012 déjà documentés par ce lot ; aucun cache
partagé n'est modifié.

## Preuves natives

Trois scénarios Playwright Chromium headless / mGBA offscreen réussis sur la ROM
sentinelle finale :

- `es013-moves.spec.ts` : 18 pointeurs des six descriptions, cinq lignes dans le
  résumé, OCR du texte entier et restauration après navigation.
- `es013-natures.spec.ts` : 25 IDs aux deux tables, 50 copies natives, canaris,
  largeurs des polices 0/2 et comparaison des deux rendus par ID.
- `es013-system.spec.ts` : pointeurs FC13/F8/F7, trois colonnes FC13, pictogrammes
  F8, expansion des quatre tampons maximaux, ordre 0/1/2/3, deux FB, canaris et
  largeurs natives dans les budgets 216/232/208 px.

Le premier rejeu groupé a subi une déconnexion du pont mGBA sur LOADSTATE du
résumé. Le rejeu isolé du même test a réussi sans modifier ses assertions ;
les deux autres scénarios avaient déjà réussi. Aucune sauvegarde en jeu.

Captures finales hors dépôt, attachées après assertions :

- Résumé : `attachment://aab1c141-a593-4bb7-bf4a-ae47ca976b5a`.
- Natures : `attachment://28770859-6c5d-4682-9431-6c5df56e4f35`.
- Système : `attachment://54f030ae-60c5-45df-80a1-e84eb2b6b175`.

Les fenêtres système sont préparées en RAM aux dimensions des templates qualifiés,
puis imprimées par le moteur natif. Les trois pages F7 sont isolées après
expansion ; aucun parcours réseau naturel n'est revendiqué. Le résumé réaffecte
les slots de la fixture uniquement dans une copie éphémère après contrôle des
pointeurs livrés. Ces associations artificielles ne sont jamais livrées.

## Non-régression et revue

Le témoin FR est reconstruit avant l'extension partagée, avec BUILD_NUMBER=0 :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
La vérification finale compare la reconstruction aux mêmes paramètres octet
par octet. Les builds es-maint, DE et IT ont réussi. La ROM es-maint vaut
`32794a3d9d544db9960a59f89608a6f3145879bfe4ed76baf7fc70ff5bb8976a`,
identique au témoin intégré avant ce ticket. Ruff ciblé, TypeScript et revue
sémantique des manifestes ont réussi : aucune ancienne route modifiée ; seules
les six cellules de table désormais possédées par ES-013 remplacent leurs
anciennes gardes d'exclusion ES-014.

L'assertion ES-009 compare toujours ses 26 routes exactes, dans sa sélection
contractuelle ; elle n'interdit plus qu'un autre lot réutilise engine_layout.
L'exemption ES-014 est limitée aux six cellules explicites, avec vérification
que chaque cible appartient à sa nouvelle route. Aucun affaiblissement global.

Le premier lancement de `make test-python PYTHON=python` a été interrompu après
deux erreurs de préparation : lecture de la ROM IT pendant la fin de son build,
et héritage de PYTHON=python dans une assertion de recette attendue en python3.
Les cinq tests d'accents IT repassent après le build. La suite est relancée via
`make test-python` sans substitution du Makefile ; aucun attendu n'est neutralisé.
Les résultats finaux de la suite standard sont consignés ci-dessous ; ceux des
hooks sont reportés dans le bilan du checkpoint au ticket.

## Résultat de la suite standard

`make test-python` avec Python 3.14 : **10 314 réussis**, trois ignorés
préexistants, 4 474 désélectionnés, 96 sous-tests réussis, aucun échec (880,84 s).
Les trois ignorés concernent le pont émulateur optionnel, un ancien contrôle FD
conditionnel et l'insertion CSV dynamique espagnole ; aucun skip ajouté ici.
Unicorn est présent et les contrôles ARM sont exécutés.

## Non vérifié — prérequis restant

Les 54 descriptions de décorations ont des champs de structure et un export
GFRomHeader prouvés, mais pas de fenêtre/police/accessibilité moteur attestées.
Leurs exclusions sont temporaires, pas une qualification définitive de données
non textuelles. La capacité physique totale de gStringVar4 n'est pas certifiée
par le seul plafond contractuel 512 : destination 02021D18, autre variable lue à
02022100, écart de 1000 octets. Les tampons F7 individuels sont, eux, bornés par
les routines et la table de 1294 noms gardée après patches.

Les six textes de tables sans racine établie restent conservatoires ; les
traductions, protections et parcours naturels définitifs restent à F-863.
