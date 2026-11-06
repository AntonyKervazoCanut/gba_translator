# ES-009 — contrats des choix à prix et messages PC

F-1040, prérequis technique de F-859. Aucune traduction de production importée.
Source EN SHA-256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Les preuves par adresse, préimages, colonnes, consommateurs et observations des
729 noms d’objets figurent dans [009_FORMATTED.json](009_FORMATTED.json).
La préparation des 374 clés reste inchangée.

## Décisions sur les 36 surfaces

| Qualification | Nombre | Contrat |
|---|---:|---|
| Choix des six menus multichoice natifs | 19 | Police effective, colonne de prix et fenêtre source figées |
| Messages PC / F7 | 7 | Fenêtre 144 × 16 px, tampon expansé 80 octets, terminateur compris |
| Choix dont le consommateur historique est contourné | 10 | Injection refusée, textes et pointeurs anciens conservés |

Les cinq choix sans pointeur 417CD1/417CE6/417CFF/417D18/417D32 restent à qualifier
par F-859. Aucun alias n’est créé, notamment pour les six préfixes nuls.

## FC13 et FC06 : preuve moteur et budgets

Le dispatch FC à 58AC/table58CC conduit FC06 à 59DC : l’argument remplace le
nibble bas de la police du renderer. FC13 conduit à 5ADC : il calcule
`cible = x_initial + argument`, efface et avance seulement si la cible dépasse
le curseur courant. Un nom trop long décale donc le prix. Le nouveau calcul
opt-in refuse ce dépassement de colonne avant de contrôler la largeur totale.
GetStringWidth à 5ED4 suit lui aussi FC06 (6058) et FC13 (6090).
Les métriques 512 glyphes des polices 0/1/2 proviennent de 1EEF00/1FB100/207300,
comme dans F-1037 ; leurs préimages sont contrôlées avant et après patches.

La routine 9CAAE lit les groupes de la table3E04B0, mesure tous leurs choix en
police2 et calcule `width_tiles = ((max_width + 9) // 8) + 1`. L’impression via
10FBE8/12E62C part de x8,y2, avec un pas vertical14. Le contrat conserve les
fenêtres source ; il n’autorise aucun agrandissement implicite.

| ID menu | Racine | Table des choix | Largeur fenêtre | Budget depuis x8 |
|---:|---|---|---:|---:|
| 13 | 3E0518 | 3E01B8 | 136 | 128 |
| 14 | 3E0520 | 3E01C8 | 144 | 136 |
| 26 | 3E0580 | 3DFF30 | 120 | 112 |
| 27 | 3E0588 | 3DFFB0 | 112 | 104 |
| 30 | 3E05A0 | 3DFF50 | 136 | 128 |
| 41 | 3E05F8 | 3DFF80 | 144 | 136 |

Les dix clés 4180A7/4180BC/4180D0/4180FA/41810D/41811D/41812F/418142/418152/418163
n’ont que les anciens pointeurs de3F5CBC…3F5CE4. Le trampoline
`CB94C → 1E76978 → CB975` contourne CB970 et son ancien littéral CBA68=3F5BCC.
Les sélecteurs effectifs 1EB48B8/1EB48D4 utilisent 1FB196C ; les listes textuelles
0…30 ne contiennent aucune de ces clés. L’enregistrement31 n’est pas une liste
textuelle valide : aucun consommateur n’en est inventé. Ces faits justifient
le refus d’injection, sans prétendre prouver une inaccessibilité universelle.

## F7 : expansion réelle et limites

Le reset13CC90 efface huit pointeurs à0203F34C. Le setter13CCAC accepte les
indices0…7. L’expanseur13CCC8 est effectivement hooké vers8A9270 : F7 retourne
à13CCE8, lit **un octet d’index**, copie le tampon par8D84, puis reprend la
source après cet index. F7 00 00 est donc tampon0 suivi d’un espace ; F7 00 AB
est tampon0 suivi d’un point d’exclamation. Seul l’index0 est qualifié ici.

ShowPCMessage8FBA4 charge la table3CEA88 (stride8, texte+0/type+4), choisit le
tampon puis expanse dans `structure_PC + 2180`. Le tampon suivant commence à
21D0 : capacité80 avec FF. L’impression à8FCB0 emploie window1, police1,x0,y2.
InitWindows8F048 charge3CEA30 ; son record1 à3CEA38 vaut
`00 0B 11 12 02 0D 14 00`, soit 18×2 tuiles. La table de largeurs police1 est
1FB100, prouvée par le dispatch1EA654 et le littéral65AC.

| Clé | Indices/types actifs | Réserve tampon0 |
|---|---|---|
| 41825C | 4/1 et 23/7 | 17 octets / 95 px |
| 418295 | 7/1 | 10 octets / 60 px |
| 4182CE | 10/4 | 10 octets / 60 px |
| 4182DF | 11/6 | 10 octets / 60 px |
| 418392 | 19/1 | 10 octets / 60 px |
| 418433 | 28/7 | 17 octets / 95 px |
| 418443 | 29/7 | 17 octets / 95 px |

Types1…3 lisent le surnom+CEA, types4…6 sa copie+21D0. Les lecteurs93B56/93C4E
appellent GetMonData/GetBoxMonData champ2 puis8D28, qui borne le surnom à10.
La sonde `WWWWWWWWWW` exerce60px. Le type7 prend le nom d’objet+21DB : la
branche curseur961A8 copie le nom intégral via ItemIdGetName9A8BC→9F324C ;
la branche affichage+D61 possède déjà une ellipse historique àA04F88.
Cette ellipse ne constitue pas une autorisation de tronquer les traductions.

Les729 noms lus par9F324C (table876200, stride44, noms directs ou indirects)
atteignent17 octets/95px. Cette réserve conservatrice inclut des objets clés
non tenables, sans prétendre qu’ils le sont. Les préimages des noms et de leurs
pointeurs indirects sont gardées après patches : une future modification de
ces sources impose de requalifier le budget, au lieu de le dépasser silencieusement.

**Trois messages source ne passent pas le budget maximal.** Avec le nom source
`Strawberry Sweet` (objet716,16 octets/91px), 41825C/418433/418443 mesurent
162/163/160px pour144 disponibles ; avec la réserve95,166/167/164px.
Les tests doivent rejeter ces sources. Les essais positifs utilisent uniquement
la sentinelle temporaire F7 00 ! ; aucun texte de production n’est raccourci.
F-859 devra rédiger ses messages sous le budget résiduel de49px après tampon95.
Le message de dépôt418295 atteint exactement144px avec un surnom maximal.

Les huit pointeurs de la table active et leurs huit miroirs sont tous vérifiés
après relocation. Les miroirs9A425C n’ont pas de racine directe démontrée ; ils
ne sont pas présentés comme des consommateurs naturellement exécutés. La table
d’actions3D353C, lue via94E48 par94DEC, ne contient aucun des sept textes.

## Implémentation et essais reproductibles

`SystemTextRoutes` enrichit toujours le vrai JSON issu du CSV et contrôle les
consommateurs finaux à partir du combined et du contrat canonique, même si le
cache JSON a perdu sa valeur ou son layout. `EngineTextLayout` ne fait que mesurer les contrats
explicitement activés. Aucun second réinserteur, patch moteur, fallback ou
troncature n’est ajouté ; les profils FR/IT/DE ne sont pas activés.

Les fixtures unitaires sont des tranches de la ROM réelle. Les sondes de
pipeline utilisent un combined temporaire et réduisent la capacité des cellules
JSON temporaires à1 pour forcer leur relocation, sans altérer les noms, prix,
nombres ou commandes. Le contrôle compare la ROM entière à une baseline ayant
reçu les mêmes patches, ainsi que les voisins et les cinq occurrences graphiques
PT-12 (3BFC8A/40F1AA/1AAA166/1BB7B57/1DA2F35).

```sh
python3 -m pytest tests/unit/test_engine_text_layout.py tests/unit/test_es009_contract.py -q
python3 -m pytest tests/e2e/es/test_es009_formatted_routes.py -q
npx playwright test -c tests/e2e-playwright/es009.config.ts
make build-es-maint BUILD_NUMBER=0
make test-python
```

Les deux tests Playwright utilisent Chromium headless et mGBA offscreen :
19 colonnes comparées aux bitmaps des suffixes, sept appels réels à
ShowPCMessage, trois expansions source trop larges détectées et six menus
natifs ouverts par opcode6F. Le tampon runtime est comparé octet par octet au
nom attendu ; des canaris réels protègent les deux bords du tampon PC80. Les
captures sont temporaires et jointes au ticket, sans sauvegarde en jeu.

## Limites de certification

Les scénarios naturels et les zones géographiques ne sont pas déduits des
adresses. Les six menus ont des consommateurs natifs qualifiés et peuvent être
exercés par le vrai opcode6F ; cela ne démontre pas l’ensemble des scripts de
scénario. Pour418295, la route index7 existe mais aucun appel naturel n’est
établi. La rédaction ES finale, les cinq clés sans pointeur et les parcours de
F-859 ne sont pas livrés ici. La suite ROM globale demeure hors certification,
notamment ROM PT absente et attendus DE divergents décrits dans le parent.

Témoin FR initial reconstruit avec les mêmes sources et BUILD_NUMBER=0 :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Les résultats exécutés et les captures sont consignés dans la résolution du ticket.
