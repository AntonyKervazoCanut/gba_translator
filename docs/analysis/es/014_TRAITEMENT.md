# ES-014 — Traductions et relecture (F-864)

Les 374 clés contractuelles sont traitées dans `014_TRAITEMENT.json` : 339
descriptions actives et 18 textes système traduits/corrigés, huit anciennes
descriptions conservées sans injection et neuf fragments audio/graphiques exclus.
Les preuves des exclusions, préimages EN propres, références et surfaces sont dans
`014_ROUTES.json` et `014_ROUTES.md` (F-1042, commit 041bf40b intégré).
D-849 et F-850 sont terminés et intégrés avant la traduction.

## Choix linguistiques

Chaque candidat ES de l'inventaire a été relu contre l'EN propre intégral. Les
357 valeurs finales sont des traductions/corrections es-ES, ajoutées une seule
fois au combined et protégées exactement dans le même commit. Aucun import
aveugle, aucune traduction depuis le cache EN historique contaminé.

Corrections particulièrement significatives : Tornade décrivait la grêle,
Double-Dard annonçait la confusion au lieu du poison, Provoc inversait l'utilisateur
et le rival, Possessif répétait Échange, Larcin perdait sa condition d'objet,
Vampipoing et Dévorêve omettaient la récupération de PS, et plusieurs attaques
perdaient leurs chances d'effet, leurs délais ou la force du changement de stat.
La traduction suit l'effet EN de ce hack, même lorsqu'il diffère des générations
commerciales récentes : Acide baisse ici la Défense, Poursuite ne reçoit pas une
mécanique réinventée et Effort conserve la description vivante EN.

PS, PP, Ataque, Defensa, At. Esp., Def. Esp., Velocidad, Precisión et Evasión
suivent D-849. Les compactes Precis., Def., mov. et estad. sont des choix de budget
de ce lot ; elles ne sont pas présentées comme des noms officiels. Les fenêtres
partagées utilisent des phrases plus courtes, sans perdre les conditions d'effet.
Les descriptions évitent les noms de mouvements sauf les mentions déjà présentes
dans l'EN : Reserva, Reflejo, Pantalla de Luz. Les textes système gardent Hoenn,
Pokédex, Cinta, Baya, Regalo Misterioso et Ciudad Carmín. Le groupe géographique
Sevii est rendu **Archi7**, forme es-ES confirmée par la page Nintendo de
[Pokémon Version Vert Feuille](https://www.nintendo.com/es-es/Juegos/Programas-descargables-Nintendo-Switch/Pokemon-Version-Vert-Feuille-3031351.html).
Les autres termes sont ceux du glossaire et de la localisation de génération III,
sans revendication de copie d'une notice commerciale. Aucun nouveau nom Unbound.

Références terminologiques complémentaires : [Ciudad Carmín dans le guide Nintendo
Rojo Fuego/Verde Hoja, génération III](https://www.guiasnintendo.com/1_GAMEBOY_ADVANCE/pokemon_rojofuego_verdehoja/pokemon_rojofuego_verdehoja_sp/ciudad_carmin.html) ;
Stockpile (ID 254) → Reserva dans le [guide Nintendo Esmeralda, génération III](https://www.guiasnintendo.com/1_GAMEBOY_ADVANCE/Pokemon_Esmeralda/pok_esmeralda_SP/moves.html) ;
Reflect (ID 115) → Reflejo et Light Screen (ID 113) → Pantalla de Luz dans
[l'article stratégique Pokémon consacré à Eevee](https://www.pokemon.com/es/estrategia/evoluciona-tu-estrategia-con-eevee),
contexte Soleil/Lune, génération VII (forme longue moderne conservée ;
le guide Platine, génération IV, emploie la compacte Pantalla Luz).
Ces sources attestent les noms ; les effets restent ceux de l'EN vivant d'Unbound.

## Traçabilité et contrats

Le rapport donne pour chaque offset la décision, le candidat communautaire, la
correspondance de l'offset map lorsqu'elle existe, les cibles réellement lues aux
références dans la ROM ES, la valeur finale, les octets avec FF et les largeurs par
ligne. Les 69 correspondances actives absentes de l'offset map sont reconstruites
par les références figées : toutes les références ES des 357 clés actives ciblent
la même clé canonique. La carte d'offsets n'est donc pas extrapolée aux voisins.

Les surfaces sont celles démontrées par F-1042 : résumé des capacités, autre liste
de capacités, Cube et CT/MO, routines vers gStringVar4 et scripts Mystery Gift.
Aucune zone géographique n'est déduite de l'adresse. Les mots Hoenn/Archi7/Carmín
désignent le contenu des messages et ne prouvent pas leur accessibilité naturelle.

270 descriptions : au plus cinq lignes de 122 px ; 69 partagées : au plus trois
lignes de 122 px. FE explicites, aucun FA/FB dans ces descriptions, moins de 512
octets. Les 18 textes système conservent tous les FC/FD/F8/F9/F7 avec arguments,
l'ordre des buffers et chaque FE/FA/FB. Trois textes scriptés sont raccourcis pour
rester dans leur cellule source ; aucun réinserteur nouveau ni changement partagé.

`test_es014_translation.py` réinsère les 357 valeurs finales sur les tranches ROM
réelles, vérifie tous les consommateurs et compare tout le binaire hors plages
permises. Les valeurs protégées assurent la régression exacte du combined.
Les sondes Playwright ES-014 acceptent `ES014_FINAL=1` pour lire la ROM intégrée et
les textes du rapport. Les associations de consommateurs de la sauvegarde sont
adaptées uniquement dans une copie éphémère, après assertions des octets livrés.

## Validation et limites

Le vrai pipeline sur les 357 valeurs finales vérifie les 1 177 références, dont
166 relocalisées. Comparaison intégrale avant patches avec la ROM source, puis
après patches avec un témoin soumis aux mêmes étapes : aucune différence hors
des plages autorisées. Les 31 tests ciblés et les trois sondes Playwright natives
passent ; le maximum mesuré est 122 px et 248 octets par texte, terminateur inclus.

`make test-python` sous Python 3.14 : 10 227 réussis, trois skips préexistants,
aucun échec. Les quatre tests de recette et les contrôles ciblés passent (35 tests).
Le premier hook complet valide 10 086 tests Python et 80 tests Vitest, puis les
builds FR/IT/DE. La reconstruction FR est identique au témoin, octet par octet :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Les relances initiales ont corrigé l'environnement local (ROM DE absente et
argument `PYTHON=python` incompatible avec une assertion de recette qui attend
littéralement `python3`) ; aucun attendu ni test n'a été neutralisé.

Les résultats des commandes de build, des tests complets, de la non-régression FR
et des sondes natives sont consignés dans la résolution du ticket avec les captures.
Le routage F-1042 a été relu ; ses sentinelles ne constituent pas une preuve des
traductions finales. Le test final du présent lot utilise les valeurs réellement
livrées et conserve les contrôles de tous les octets.

Non vérifié : parcours naturels Mystery Gift et expansion de tous les buffers en
situation réelle ; certification globale des autres lots et des BPS distribués.
Les captures natives prouvent les surfaces du résumé et du Cube sur les textes
finaux, ainsi que les deux lignes de la mise à jour Pokédex dans l'imprimeur natif
(sonde temporaire jointe au ticket). Elles ne certifient pas les chemins naturels
Mystery Gift ni toutes les expansions de buffers. Aucune sauvegarde en jeu. Les sources ES de référence/FR, le glossaire,
`lots.json` et l'infrastructure partagée ne sont pas modifiés. Aucun push ni
lancement de pipeline distant.
