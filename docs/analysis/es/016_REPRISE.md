# ES-016 — revue de F-1045 et brouillon de reprise

**NON LIVRÉ.** Cette reprise ne constitue ni une livraison de traduction ni une
certification des 393 entrées. Aucun combined, protection, glossaire ou contrat de
production n’est modifié. `016_REPRISE.json` conserve les 393 clés exactes, les
préimages EN, les références et les candidats ES du relevé historique, ainsi que
340 traductions **en brouillon non injecté**. Les zones restent non qualifiées.

## Revue du prérequis intégré

Les commits `197c2166` et `1d19f2a3` sont présents dans l’ascendance locale.
Les six alias et les trois vrais débuts doublonnés sont documentés dans
`016_ROUTING.md`. L’exclusion de 780E33 est conservée : la cellule 9047D0
appartient à la table dormante 904000 ; les racines moteur chargent 99F194 et
la cellule active 99F964 vise A3A6D6, texte différent du lot ES-025.
Aucun repointage de l’ancienne table ne peut être compté comme une injection
vivante. Le contrat opt-in du prérequis n’injecte aucune traduction à lui seul.

## Travail indépendant conservé

Les 340 brouillons sont rédigés depuis l’EN intégral, sans import automatique de
la communauté ni reprise de la FR. Les commandes complètes FC/FD et les contrôles
FA/FB sont comparés dans l’ordre : aucune différence sur ces 340 brouillons.
Ce contrôle ne certifie ni les largeurs après expansion des tampons ni le rendu.
Les longueurs encodées avec terminateur sont consignées. Les préimages ne sont
jamais tronquées à 512 octets.

Un essai temporaire de la vraie conversion CSV a retrouvé les 340 clés :
340 lignes correspondantes, 340 mises à jour, zéro ajout. L’enrichissement JSON
a ensuite refusé 7808DE pour dépassement de sa fenêtre. Le brouillon a été
raccourci en `Un pueblo feliz y dichoso.` ; la conversion complète corrigée
n’est pas certifiée ici. Aucun de ces CSV/JSON temporaires n’est une source de
production. Il faut régénérer le JSON de production avant tout build es-maint.

La vérification statique de largeur a aussi signalé des lignes longues, notamment
avec deux noms dynamiques. Le brouillon a été recomposé ; ces mesures ne sont pas
une qualification des producteurs de tampons. Les choix de noms, de registre,
les nuances du scénario et les budgets doivent encore être relus avant import.

Les occurrences directes ont été annotées par leur contexte : loadpointer bank0,
bufferstring, message, champs trainerbattle et descriptions gItems. Une signature
locale ne prouve pas à elle seule qu’un script est accessible depuis une carte.
Les occurrences 90E85E vers 76D100 et 7413F5 vers 77151E n’ont pas été ajoutées
aux pointeurs qualifiés ; ce sont des cas à conserver sans repointage aveugle.
Toutes les occurrences intérieures restent des preuves à qualifier, pas des
lecteurs supplémentaires automatiquement approuvés.

## Décisions restant à certifier

Le JSON distingue 340 brouillons, 32 conservations documentées sans injection
(scripts, doublons AA et anciennes tables) et **21 qualifications à terminer**.
Ces nombres ne sont pas un taux de livraison. Chaque ligne est explicitement
marquée `injection_certified: false`.

Les 21 clés encore ouvertes comprennent les 18 fragments/textes sans consommateur
qualifié et trois descriptions sans référence absolue (780CB2, 78117E, 78122B).
78000F est contenu dans la source vivante 77FFE5 ; 780119 dans 7800BD.
Leurs références machine ne doivent pas devenir des lecteurs textuels.
Pour les autres fragments, le balayage des débuts terminés par FF dans les
256 octets précédents n’a pas produit de contenant référencé qualifié. Ce résultat
borné **ne prouve pas leur mort** et ne justifie pas une exclusion définitive.
Les six vrais textes après les scripts initiaux ne sont pas déplacés vers des
clés hors lot. Les tableaux actif et dormant restent intacts.

Pour livrer F-866 : terminer les reconstructions et les zones depuis les scripts,
relire les 31 différences communautaires et les trois absences, arrêter les 393
décisions finales, puis importer chirurgicalement et protéger les valeurs exactes.
Réutiliser la relocalisation existante pour préserver les préimages partagées et
ne repointer que les lecteurs qualifiés. Vérifier le vrai pipeline après patches,
les octets à tous les consommateurs, les tampons, commandes, cellules et pixels ;
rebuild ES et témoin FR identique ; make test-python ; assertions Playwright
headless avec rendu natif mGBA offscreen puis capture jointe au ticket.

## Non vérifié

Aucune injection finale des brouillons, aucune attribution exhaustive aux cartes,
aucun parcours naturel ni certification linguistique. Aucune capture de brouillon
n’est présentée comme preuve d’affichage final. Aucun état de sauvegarde en jeu
n’est créé. Aucun push ni lancement de pipeline distant.

Les validations fraîches de cette revue sont consignées dans la résolution du
ticket ; les grandes campagnes de F-1045 restent attribuées à ce prérequis.
