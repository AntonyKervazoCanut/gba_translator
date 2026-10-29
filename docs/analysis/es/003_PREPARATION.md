# ES-003 — préparation et blocage d’acheminement

Ticket F-853, 29 octobre 2026. **Lot non certifié, travail en cours.**
La liste contractuelle reste celle de `lots.json` : 374 offsets.
D-849 et F-850 ont été consultés et sont terminés.

## Sources préparées

216 valeurs ajoutées chirurgicalement au combined es-maint, chacune protégée
exactement dans `protected_entries.yaml` : 86 classes de Dresseurs, 15 noms de
types effectivement au début d’une chaîne, 77 descriptions d’habilités,
11 dialogues/messages de combat et 27 descriptions d’objets.
Il ne s’agit pas d’une certification de leur acheminement en ROM.

Les descriptions d’objets absentes du champ EN de l’inventaire ont été relues
dans la ROM anglaise. Exemple : `0x3D4F26`, « A very high-grade Ball… », est
référencé par `0x3DB094` et `0x87626C`. Les textes français de l’inventaire EN
ne sont pas utilisés comme source de traduction. Les champs source EN/ES/FR,
les deux ROM sources, le glossaire et les scripts partagés restent inchangés.

Les effets ont été revus : Wonder Guard ne signifie pas « évite les coups
efficaces », Color Change change le type du Pokémon, Lightning Rod attire les
mouvements électriques et Revive restaure la moitié des PS maximaux.
Le dialogue SES conserve Autovía SES, sans substitution par KBT/RBT.
La ponctuation finale de `0x270FA1` est l’octet `B0` (points de suspension),
et non un guillemet : aucune fin de phrase inventée.

La classe Collector utilise la compacte de budget du projet `Coleccion.` :
`Coleccionista` fait 14 octets terminateur compris, contre une cellule de 13.
Cette compacte ne prétend pas être un nom officiel complet. Le test physique
de cellule a d’abord échoué sur le nom complet, puis passe avec la compacte.
Le descripteur réutilise la passe existante `trainer_class_names_it`, qui
accepte le combined de la langue courante ; aucune infrastructure partagée
n’a été modifiée. Le suffixe historique du nom de passe ne fixe pas la langue.

## Blocage distinct : alias contractuels

L’offset `0x24F3C1` commence par `05 00 00` ; le texte anglais « No special
ability. » débute à `0x24F3C4`. Les habilités 0 et 77 de la table vivante
`0x96DE04` visent `0x24F3C4`. Une traduction écrite au faux début ne constitue
donc pas une preuve d’injection au pointeur vivant et écraserait le préfixe.

B-1030 implémente déjà la résolution explicite des alias contractuels pour
es-maint. Il doit être réutilisé comme prérequis ; ne pas créer un mécanisme
concurrent, modifier les lots ou ajouter une clé combined hors contrat.
Après son intégration, déclarer et tester l’alias +3 d’ES-003, puis traduire
le texte vivant sans importer les trois octets de préfixe comme des lettres.

## Reprise et limites

Le rapport de préqualification joint au ticket examine les 374 offsets :
préimages ROM, décodage de diagnostic, offset map, références à l’offset et
dans ses onze premiers octets, décisions provisoires et budgets des textes
préparés. Un décodage de diagnostic ne certifie pas des arguments de contrôle.

Restent à certifier : exclusions binaires, fragments aux limites de cellules,
ancienne copie des noms d’habilités (la table actuelle est à `0xA36398`), noms
propres inchangés, cartes réelles depuis les scripts, commandes complètes et
arguments, budgets rendus et injection de chaque valeur aux consommateurs.
La plage d’adresses ne sert jamais d’attribution géographique.

La préparation est protégée par les tests d’intégrité partagés et
`tests/unit/test_es003_scope.py` : cellules physiques, plafond 512 et gardes
de scénario/effets. Les résultats du build et des suites sont consignés dans
la résolution intermédiaire du ticket. Aucun taux d’achèvement ni conformité
aux 374 entrées n’est revendiqué avant la reprise et les preuves d’émulateur.
