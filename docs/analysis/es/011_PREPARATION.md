# ES-011 — préparation des sources et besoin de routage

F-861, 6 novembre 2026. Lot non livré. D-849 et F-850 sont terminés ;
le parent A-663 confirme gba_translator. Aucun texte importé ni traduction
certifiée à ce stade.

011_PREPARATION.json contient les 374 clés exactes de lots.json, dans leur
ordre contractuel : inventaire original, préimage complète actuelle EN,
décodage indicatif, taille avec terminateur, occurrences directes des pointeurs
à tous les alignements, candidats à +1/+2/+3 et correspondance de l'offset map
avec préimage ES. Les SHA-256 identifient précisément les sources consultées.
Le décodage est indicatif : il ne constitue pas une analyse des arguments FC/FD.
Les occurrences binaires ne sont pas toutes des consommateurs textuels prouvés.
Aucune zone géographique n'est déduite des adresses.

## Prérequis technique distinct

57 clés n'ont pas de référence directe, mais possèdent une cible référencée
à +1, +2 ou +3, précédée de zéros. 011_ROUTES.json énumère les candidats,
préfixes, préimages et sites. Le manifeste partagé text_aliases.json ne couvre
aucune de ces clés. Il faut étendre ce contrat séparément ; le lot interdit
les modifications d'infrastructure partagée. Réutiliser TextAliases, sans
nouveau résolveur, avec contrôles de préimage et conflits d'alias.

Exemples vérifiés dans la ROM actuelle :

- 0x41CE3B : préfixe 00 ; début 0x41CE3C lu à 0x46E328.
- 0x41D04D : préfixe 000000 ; début Time: à 0x41D050 lu à 0x14E564.
- 0x41D1FD : préfixe 000000 ; crédit Art Director à 0x41D200 lu à 0x4145C8.
- 0x41DC45 : préfixe 000000 ; crédit à 0x41DC48 lu à 0x414770.

Cinq cibles sont aussi des clés contractuelles du même lot : 41CE3C,
41CEA8, 41CF14, 41CF50, 41DC48. Le prérequis doit établir la stratégie
canonique et refuser des traductions contradictoires, sans double injection.
La seule proximité d'une référence ne valide pas automatiquement l'alias.

Les huit autres clés sans référence directe sont 41CC7B, 41D195, 41E2EC,
41E76B, 41EFB8, 41F0A8, 41F0BD et 41F160. Leur qualification reste ouverte :
absence de pointeur direct ne signifie pas absence de lecteur dynamique.
Aucune exclusion finale ni phrase inventée n'est proposée.

## Divergence de l'inventaire

La colonne EN historique ne représente pas toujours la source actuelle.
À 0x444CB2 elle est vide, mais la ROM contient « It carries a seed on its back »
et le pointeur 0x1A35800. À 0x444D12 l'inventaire EN contient du français ;
la ROM contient « If the bud on its back starts to smell » et le pointeur
0x1A35824. Il faudra traduire ces notices depuis les préimages actuelles,
sans substituer une notice communautaire d'une autre version. Les descriptions
Pokédex imposent une fenêtre non paginée ; les crédits conservent leurs lignes
vides et les minijeux leurs commandes et arguments. Aucune chaîne extraite
par recherche du terminateur dans ce relevé ne dépasse 512 octets.

## Vérification de la préparation et limites

Contrôles locaux : égalité ordonnée avec les 374 clés, unicité, préimages
relues dans les deux ROM, occurrences de pointeurs et préfixes recoupés.
Aucun combined, manifeste de protection, glossaire ou code partagé modifié.
Le relevé ne certifie pas les scripts racines, les largeurs, les contrôles
complets, les traductions, l'injection, le build es-maint ni les rendus.
Ces validations restent à exécuter après intégration du prérequis de routage.
Aucun nouvel affichage n'est produit par cette préparation documentaire.
