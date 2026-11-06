# ES-013 — Qualification résiduelle et limites de preuve (F-1047)

## Conclusion exploitable

**Aucune nouvelle injection autorisée.** Les 54 descriptions et les six textes
système restent exclus. Le plafond 512 reste un contrat logiciel, pas une
capacité physique démontrée. Les preuves disponibles ne permettent pas encore
la certification demandée par F-1044. Ce rapport conserve les résultats nouveaux
et désigne précisément le livrable manquant ; il ne clôt pas cette certification.

Le checkpoint 3ede161d est ancêtre du travail. Aucun combined, protection,
glossaire, inventaire, lots.json, contrat de route ni code d'injection modifié.
SystemTextRoutes, StructuredTextRoutes, TextAliases et EngineTextLayout restent
les mécanismes uniques. Les fenêtres/F7 déjà qualifiés dans 013_SYSTEM.md et
F-1040 ne sont ni redéfinis ni réinjectés.

## Reproduction sur les sources canoniques

```sh
python3 scripts/audit_es013_residual.py
python3 -m pytest tests/unit/test_es013_residual.py -q
cmp output/analysis/es013_residual.json docs/analysis/es/013_RESIDUAL.json
cmp output/analysis/es013_residual_rom.json tests/unit/fixtures/es013_residual_rom.json
```

Les trois sondes ARM exigent Unicorn, déjà utilisé par les tests moteur du
dépôt ; elles sont lancées explicitement malgré le marqueur `emulator`.

Le script refuse une empreinte EN/ES différente du checkpoint, une préimage
altérée et une correspondance ES absente ou ambiguë. Il relit les 54 clés de la
qualification précise de 013_SURFACES.json et les six clés explicites du ticket.
Il n'extrapole aucune sélection à partir d'une plage. Les tests existants
`test_es013_surfaces.py` et `test_es013_system.py` gardent les structures et les
refus d'import. Les tranches supplémentaires sont prélevées dans l'EN canonique,
jamais compilées depuis une source supposée identique.

Le scan LE32 couvre les 32 Mio, tous alignements, les bases **et chaque adresse
intérieure** des trois tables et des 121 structures de décorations. Ce dernier
périmètre est une recherche de racines, pas une extension des clés autorisées.
Chaque occurrence porte les candidats LDR Thumb PC-relatifs (portée de 1024
octets, PC aligné) : ils ne sont pas automatiquement classés comme instructions
exécutées. Les adresses calculées, copies RAM, accès ARM, scripts et programmes
externes ne sont pas exclus par ce scan. Aucun graphe de contrôle exhaustif
n'est revendiqué.

## Décorations : racine exportée, pas de fenêtre inventée

Dans l'EN canonique : `gDecorations=084556F8`, stride 32, description +24.
La référence de base unique est `14C` dans le header. Les quatorze autres
occurrences pointent à l'intérieur des structures ; aucun candidat LDR Thumb
PC-relatif ne les charge. Le JSON conserve ces quatorze sites, sans les
transformer en lecteurs ni en faux positifs définitivement éliminés.

La source FireRed publique possède seulement déclaration, définition, export
header et une ancienne copie de nom commentée. Elle ne contient pas de lecteur
actif des descriptions. Cela explique l'hypothèse d'héritage dormant **dans
FireRed**, pas l'inaccessibilité dans Unbound. Aucun consommateur externe du
header n'est attesté ici. Sans ce consommateur, on ne peut lui attribuer une
police GBA ou un budget d'écran. Les valeurs 110/112 px ne deviennent pas des
fenêtres certifiées ; les champs police/fenêtre/budget du rapport restent null.
`4556F6`, les noms, prix et graphismes sont inchangés.

Un contre-exemple concret interdit d'assimiler les deux moteurs : le slot `81`
de la table de commandes à `15F9B4`, cellule `15FBB8`, vaut `09EC9D39` dans la
ROM EN. Il entre dans le code CFRU à `1EC9D38`. Le stub FireRed
`ScrCmd_bufferdecorationname` ne constitue donc pas une preuve sur ce chemin
Unbound. La cellule et le début du code sont figés dans la fixture.

## Six textes : héritage source identifié, accessibilité non certifiée

| Table EN | Source FireRed correspondante | Structure canonique |
|---|---|---|
| 457898 | sDoYouWantModeTexts | 457860, 45787C |
| 457B80 | sDoSomethingTexts | 457B14 hors lot, 457B2C, 457B4C, 457B4C |
| 458F94 | sCantTradeMonTexts | 458F2C, 458F60 |

Chacun de ces trois symboles statiques n'apparaît qu'à sa définition dans la
source FireRed examinée ; les tables y sont signalées inutilisées. Le doublon
intentionnel de la deuxième table est un repère structurel supplémentaire.
Les chaînes Unbound peuvent différer typographiquement : ce rapprochement ne
revendique pas une reconstruction binaire de l'ensemble du module.

Dans la ROM EN complète, aucune occurrence LE32 ne pointe vers les bases **ou
l'intérieur** des trois tables. Ce résultat renforce l'identification d'un
héritage inutilisé, sans exclure les adresses calculées ni les consommateurs
externes. Les six préimages restent textuelles et conservées. Pas de certificat
de code mort, pas de nouveau budget.

## gStringVar4 : déclaration source et contre-test natif

FireRed déclare 1000 octets dans `src/string_util.c`; `sym_ewram.txt` place ce
module dans l'EWRAM. CFRU public associe explicitement le symbole à `02021D18`
dans BPRE.ld, mais sa déclaration C est sans taille. Ces sources corroborent
l'hypothèse 1000 ; elles ne fournissent ni édition de liens ni inventaire des
alias correspondant à la construction de l'EN canonique Unbound.

Le getter natif `9118` charge `02022100`. Son écart de 1000 est conservé comme
corroboration, jamais utilisé seul comme preuve d'allocation. Le scan intégral
recense 511 occurrences LE32 vers les octets de la région hypothétique, dont
409 vers la base. Les occurrences intérieures et leurs candidats LDR restent
visibles dans le rapport : une absence de symbole nommé ne prouve pas une
absence d'alias RAM.

La chaîne déjà qualifiée est conservée : `11995E→11AF6C`, destination
`02021D18`, expanseur `13CCC8`, hook CFRU `8A9270`, branche F7 `13CCE8`, copie
`8D84`. Les lecteurs de l'affichage sont `11A0F8→F6E08→F6CD0` ; fenêtre 208 px,
police 2, deux lignes par page selon 013_SYSTEM.md. Aucun de ces lecteurs
n'exprime à lui seul une taille d'allocation.

**Nouveau test négatif natif :** Unicorn exécute les octets exacts de
l'expanseur, du trampoline et de StringCopy, sans stub. Un slot F7 fournit
respectivement 511, 999 et 1000 glyphes suivis de FF. Le test exige le retour
normal, le pointeur de fin exact, le contenu complet et les bornes de chaque
écriture, avec canaris. Les tailles écrites sont 512, 1000 et **1001** : le
FF du dernier cas écrase `02022100` dans la machine privée. Le moteur ne borne
pas l'expansion à 512 ou 1000. La mémoire simulée plus grande est volontaire ;
ce résultat démontre l'absence de garde, **pas** la sûreté d'une allocation réelle.

Il manque donc une preuve d'allocation ou une borne sûre indépendante des
canaris. Aucun relèvement du plafond n'est proposé. La protection contractuelle
512 ne doit pas être présentée comme substitut à cette preuve.

## Sources épinglées et portée

Sources consultées le 6 novembre 2026, uniquement en lecture :

- [pret/pokefirered](https://github.com/pret/pokefirered/tree/ce6406d8c2eaf46d543c8a2606de0c3cb1951982),
  commit `ce6406d8c2eaf46d543c8a2606de0c3cb1951982` : string_util.c lignes 4–12,
  union_room_message.c lignes 149–156, 186–200, 461–468, rom_header_gf.c,
  scrcmd.c lignes 1660–1667 et sym_ewram.txt.
- [CFRU](https://github.com/Skeli789/Complete-Fire-Red-Upgrade/tree/b637a27898b14e25dd24d0f69a3e302f0069deb8),
  commit `b637a27898b14e25dd24d0f69a3e302f0069deb8` : BPRE.ld lignes 196–199,
  include/text.h lignes 293–296. Ce commit public n'est pas identifié comme
  celui ayant construit la ROM Unbound canonique.

Pour reproduire la recherche source, extraire ces commits puis lancer
`rg -n 'gDecorations|sDoYouWantModeTexts|sDoSomethingTexts|sCantTradeMonTexts'`
sur leurs sources C/H/assembleur et examiner la déclaration et l'ordre EWRAM.
Le résultat de recherche n'est pas assimilé à une preuve de compilation.

## Non vérifié et prérequis précis

Il faut un artefact de construction **correspondant à l'EN canonique** : sources
ou cartographie symbolique/édition de liens avec sections, tailles et alias RAM,
ainsi que l'identification des lecteurs externes du header s'ils sont supportés.
Son identité doit être reliée au SHA-256 EN `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`,
pas uniquement à « FireRed » ou à une révision publique de CFRU. La vérification
binaire et les tests de reprise restent à F-1047 une fois cet artefact disponible.

F-862, F-776/PT-17 et F-1040 ont été consultés : leurs résultats n'apportent
pas cet artefact. Aucun rendu nouveau n'est livré ou revendiqué ; Playwright
n'est donc pas remplacé par une capture artificielle. Aucune sauvegarde en jeu,
aucun push et aucun lancement de pipeline distant.

## Validation locale de la préparation

- `make build-es-maint` réussi ; aucune source de traduction modifiée.
- `make test-python` avec Python 3.14 et Unicorn installé : **10 333 réussis**,
  trois skips préexistants, 96 sous-tests réussis, zéro échec (836,76 s).
- `test_es013_residual.py` exécuté explicitement : **11 réussis**, incluant les
  trois exécutions ARM, la reproduction canonique et les refus de données altérées.
- Ruff ciblé et `git diff --check` réussis.
- Témoin FR reconstruit avec `BUILD_NUMBER=0` :
  `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
  Le résultat des hooks et la comparaison après leur rebuild sont consignés
  au ticket. Aucun code partagé de génération modifié.

Les lancements de préparation dans un environnement incomplet ont été remplacés
par l'exécution complète ci-dessus : aucun test neutralisé ni skip ajouté.
Ces validations protègent le dossier de preuves ; elles ne certifient pas les
inconnues moteur exposées dans ce rapport.
