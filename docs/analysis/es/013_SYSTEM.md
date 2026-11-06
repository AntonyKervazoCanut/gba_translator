# ES-013 — lecteurs système et fenêtres techniques

Les 150 candidates système comprennent 130 clés directement référencées et vingt
alias. Le manifeste conserve **124 routes système**, vingt alias distincts et
refuse six textes de tables héritées sans racine moteur établie. Il n'ajoute
aucune traduction. Les 82 préfixes précédant une autre clé du lot et les autres
exclusions restent interdits à l'import. `013_SYSTEM.json` conserve les préimages,
correspondances ES, sites et chemins des consommateurs de chaque candidate.

Les routes ordinaires réutilisent `preserve_control_flow` : commandes complètes,
arguments et ordre FA/FB, sans rewrap, fallback ni troncature, plafond 512 octets.
Ce contrat ne prétend pas certifier toutes les expansions FD en situation réseau.
Les pointeurs directs sont des littéraux chargés par LDR PC dans les routines de
communication ; les tables indexées ont leurs racines explicitement consignées.
Les menus à stride huit passent par leur `ListMenuTemplate`, pas par un accès
textuel supposé à la structure. Les gardes préservent racines et instructions
sans geler les seuls pointeurs autorisés à changer.

Les tables 457898 (deux cellules), 457B80 (quatre cellules), 458F94 (deux cellules)
n'ont aucune racine littérale dans la ROM, ni charge PC correspondante dans le
code examiné. Les six clés 457860/45787C/457B2C/457B4C/458F2C/458F60 n'ont pas
d'autre lecteur établi : exclusion conservatrice, pas preuve d'inaccessibilité
universelle. La copie 457E78..457E84 est également sans racine, mais les quatre
textes ont des lecteurs code vivants ; leurs pointeurs miroirs restent cohérents.

458314 est une table chargée par 11AE84, racine11AE90 : première cellule458260
hors lot gardée ; seule la seconde cellule458318 vers4582C0 appartient à une
route. 1DCCF22 n'est pas ajouté aux pointeurs textuels de45817E.

## En-tête et aide

459378 est consommé par11A1AC, littéral11A1F8, via11A444 : police0, x8, y1.
Le template à456F1C, racine11A350, décrit28×2tuiles. Le budget après x8 est
**216px**. FC13 3C/6E/C6 déplace le curseur relatif à x initial ; chaque colonne
est vérifiée par `EngineTextLayout`, avec les métriques police0 déjà établies
par F-1040. Aucun octet d'argument ne devient une lettre.

458FC6 utilise l'alias458FC8. Le code116856 charge456CD0 (30×2tuiles), puis
116876..116886 imprime en police0,x8,y2 via11A444. Budget **232px**, une ligne.
Les trois commandes F8 0A/00/01 sont mesurées par la table d'icônes déjà gardée
par `TextAliases`. Le préfixe00 reste inchangé.

## Offre F7

Le vrai lecteur11AF6C est appelé par11995E. L'expansion arrive dans gStringVar4
02021D18 (littéral119978). Les slots F7 0/1/2/3 pointent vers quatre tampons à
stride11 aux offsets58/63/6E/79 de la structure : niveau/espèce/niveau/espèce.
11AFD4 et11B016 écrivent trois chiffres via8E78 ;11AFE6 et11B028 copient les
noms d'espèces par8D84. La table fixe166A98C est chargée aux racines11AFF4 et
11B048 : ses **1294 cellules** (11 octets chacune, jusqu'aux formes Urshifu)
contiennent toutes un FF, au plus dix glyphes et **59px** en police2. La réserve
retenue est dix octets/60px ; les chiffres réservent trois octets/18px.
La table entière et ses racines sont gardées avant et après les patches : une
modification ultérieure des noms oblige à requalifier ce budget.

Le setter13CCAC reçoit les quatre indices par11B056..11B066. L'expanseur13CCC8,
hook8A9270, lit exactement un octet d'index, mécanisme réutilisé de F-1040.
Les deux FB restent dans l'ordre. L'appel11A0F8→F6E08→F6CD0 imprime la fenêtre0
en police2,x0,y1. Le contrat retient deux lignes par page,208px (template41F42C,26×4tuiles, racineF6C84)
et512octets après expansion (la limite globale reste512octets encodés).

L'extension commune est strictement opt-in : `paged_dialogue` permet FB et FA
et contrôle les lignes par page ; `allowed_fc: [8]` permet les pauses FC08 sans
mesurer leur argument comme glyphe. Les anciens contrats continuent à refuser
ces commandes. Les messages d'attente ordinaires gardent leurs FC0814 exacts
par comparaison de contrôle ; le ticket ne réécrit pas leurs pauses.

## Preuves et limites

`test_es013_system.py` exerce toutes les routes sur des tranches ROM réelles,
compare chaque octet après insertion, teste les refus d'exclusions,512octets,
arguments modifiés, ordre des tampons et colonnes. Les tests supplémentaires de
`test_engine_text_layout.py` couvrent capacité cumulée à travers les pages,
limites de lignes, arguments FE/FF dans FC08 et refus sans opt-in.

`es013-system.spec.ts` vérifie les pointeurs du pipeline temporaire final puis
exécute mGBA hors écran. Les fenêtres RAM synthétiques reproduisent les dimensions
des templates qualifiés et utilisent le véritable imprimeur natif. La sonde appelle le vrai expanseur F7 avec quatre tampons
maximaux, vérifie les canaris et l'ordre complet des octets, puis imprime les
fenêtres en moteur natif. La capture montre l'en-tête, l'aide et les trois pages
F7 **isolées après expansion** ; elle ne prétend pas reproduire la navigation
réseau ou l'attente interactive entre pages. Les captures restent temporaires,
aucune sauvegarde en jeu. Les parcours naturels et traductions restent à F-863.
