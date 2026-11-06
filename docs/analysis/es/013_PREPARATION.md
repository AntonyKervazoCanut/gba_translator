# ES-013 — préparation des consommateurs, lot non livré

F-863, 6 novembre 2026. Dépôt gba_translator confirmé par le contexte A-663.
D-849 et F-850 sont terminés et intégrés. Le glossaire, la référence ES,
les sources EN/FR et les fichiers combined/manifeste es-maint sont inchangés.

[013_PREPARATION.json](013_PREPARATION.json) couvre dans leur ordre les **374 clés
exactes** de lots.json. Il ne constitue pas un rapport de traductions injectées.
Chaque entrée conserve l'inventaire EN/ES/FR et ses alertes, la préimage de la
ROM EN, toutes les occurrences LE32 à tous les alignements, le début vivant
candidat, les commandes complètes du parseur du builder et les correspondances
ES disponibles dans l'offset map. Les empreintes des ROMs et sources de texte
sont consignées. Les champs de décodage naïf sont explicitement non normatifs :
les arguments FC/FD/F8/F9/F7 ne sont pas des lettres à traduire.

| Qualification provisoire | Nombre |
|---|---:|
| Descriptions de décorations | 54 |
| Nom dans une structure de décoration | 1 |
| Données binaires | 9 |
| Doublons de remplissage avant une autre clé vivante du lot | 82 |
| Textes système avec référence directe à qualifier | 130 |
| Alias vers un début absent des clés du lot | 20 |
| Coïncidence binaire à qualifier | 1 |
| Table de pointeurs, pas un texte | 1 |
| Natures | 25 |
| Alphabets conservés | 11 |
| Métadonnées de Pokémon | 6 |
| Noms propres conservés | 28 |
| Descriptions de mouvements | 6 |
| Total | 374 |

## Constats et besoin technique distinct

Le lot interdit de modifier l'infrastructure partagée. Les 20 alias identifiés
ne figurent pas dans text_aliases.json ; les autres contrats système existants
ne certifient pas les surfaces ES-013. Le prérequis doit compléter les contrats
existants, sans seconde chaîne de réinsertion ni traduction de production.
Le défaut est reproduit par la vraie conversion CSV→JSON, avec vingt
sentinelles dans un combined temporaire : **zéro entrée** atteint le JSON
consommable, donc **0/20 alias résolu**. Les résultats individuels figurent
dans [013_ACHEMINEMENT_REPRO.json](013_ACHEMINEMENT_REPRO.json). Il ne
s'agit pas simplement d'une absence de certification ou de manifeste.
Les clés contractuelles restent les seules clés autorisées dans le combined.
Les 82 doublons de remplissage doivent être exclus des écritures : leur texte
vivant possède déjà sa propre clé dans ce lot. Une absence de pointeur absolu
isolée ne prouve jamais à elle seule qu'une chaîne est inaccessible.

Les 54 descriptions de décorations ont chacune un référent de structure à
stride 32 (premier site 0x455F70). Il faut attester leur fenêtre moteur et ne
modifier ni les noms ni les prix ni les pointeurs graphiques. Les budgets
112 pixels des travaux PT-17 sont un point de départ à contrôler, pas une
certification de futures traductions espagnoles. À 0x4556F6, les trois octets
initiaux précèdent SMALL DESK dans une structure ; aucun texte ne doit être
injecté aveuglément à cette clé.

Les surfaces sans fil proviennent des consommateurs et tables identifiés dans
PT-17/PT-18, confrontés à la ROM EN actuelle. Elles ne désignent pas une carte
déduite de l'adresse. Les occurrences brutes restent distinguées des lecteurs
validés. Le motif 0x1DCCF22 vers 0x45817E est graphique selon PT-17 ; il doit
rester exclu d'un repointage textuel sans preuve moteur contraire.

**0x458314 est une table**, référencée par 0x11AE90 : ses deux cellules
pointent vers 0x458260 et 0x4582C0. La seconde est aussi une clé du lot.
La première appartient à une autre sélection ; ne pas fabriquer une phrase
avec les huit octets de pointeurs ni changer son texte hors périmètre.

**0x459378 est une vraie chaîne**, bien que sa colonne EN d'inventaire soit
vide. Son lecteur est 0x11A1F8. Ses commandes de positionnement sont
FC 13 3C, FC 13 6E et FC 13 C6. Le C6 final est un argument, pas un L de
« LLv. ». L'aide 0x458FC6 doit être acheminée vers 0x458FC8 en conservant
F8 0A, F8 00 et F8 01. L'offre 0x457D44 utilise F7 00/01/02/03 dans
l'ordre niveau/espèce/niveau/espèce et deux FB ; aucun réordonnancement.
Les séquences FC 08 14 répétées des messages d'attente font partie des données
de contrôle. La plus grande préimage du lot fait 316 octets avec FF ; le
plafond 512 n'est donc pas une troncature des sources de cette préparation.

Les 25 natures ont deux tables de pointeurs, à 0x463E60 et 0x1FE65F4.
Les 25 propositions lexicales sont consignées selon D-849, notamment
Timid→Miedosa, Quiet→Mansa et Bashful→Tímida. Elles ne sont pas importées
ni certifiées rendues. Une cellule anglaise courte ne doit pas écraser la
nature suivante ; les deux lecteurs doivent suivre toute relocation.

Les 28 noms propres Trainer Tower suivent la conservation prescrite par
D-849, espaces de cellules compris. Les six extractions démarrant dans des
métadonnées de Pokémon ne doivent pas être réécrites comme des noms.
Les onze groupes d'alphabet gardent leur ordre et leur casse. La racine de
Trainer Tower 0x4827B4 et le consommateur 0x15DD24 sont documentés dans
les audits B-666/PT-18 ; les snapshots ROM du rapport préservent la structure.

Les six descriptions finales sont reconstruites depuis la ROM EN et leurs
références, pas traduites depuis les colonnes historiques francisées/vides.
La clé 0x482985 décrit les pièces lancées et l'argent obtenu après le combat.
Leur table de descriptions est à 0x99F190 ; distinguer les lecteurs du résumé
des références historiques 0x4886xx/0x9040xx. Le prérequis doit attester leurs
fenêtres, leurs racines et tous les consommateurs avant import.

## Reproduction et reprise

```sh
python3 scripts/audit_es013_preparation.py
python3 scripts/audit_es013_preparation.py --probe-routing
python3 -m pytest tests/unit/test_es013_preparation.py -q
```

Le script ne lit que les 374 clés contractuelles ; il ne sélectionne aucune
plage et n'utilise jamais --skip-existing. Les lectures ROM ne sont pas
limitées à 512 octets. Les audits PT voisins fournissent des hypothèses de
consommateurs dont les préimages et références retenues sont revalidées ;
aucune traduction portugaise ne sert de source ES. Les caches d'extraction
et de différences sont des copies isolées dans le worktree, pas des liens
vers des fichiers mutables partagés.

Après intégration du prérequis technique : terminer la relecture des textes
vivants, traduire/importer les seules clés exactes, protéger chaque valeur,
mesurer les budgets et vérifier tous les pointeurs après les patches. Produire
alors le rapport final, les builds et tests, les témoins FR identiques et les
assertions Playwright headless avec captures attachées. Cette préparation
ne remplace aucun de ces critères et ne doit pas permettre de clore F-863
ou de certifier T-914. Aucun nouvel affichage n'est livré à cette étape.

Les résultats locaux de préparation et des hooks sont consignés au ticket.
Aucun push ni déclenchement de pipeline distant.
