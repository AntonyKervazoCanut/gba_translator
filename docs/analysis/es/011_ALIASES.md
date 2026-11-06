# ES-011 — contrat des clés décalées (F-1041)

## Périmètre et résultat de qualification

Ce contrat traite les **57 candidats exacts** de `011_ROUTES.json`, sans traduire
ES-011. La préparation recensait des occurrences binaires de pointeurs : elle
ne certifiait pas que chaque table était encore utilisée. La ROM actuelle et ses
routines priment sur l’inventaire historique et sur la décompilation FireRed.

La qualification distingue **15 routes textuelles actives** (14 Berry Crush et
le surnom/comparand GHOST) et **42 exclusions techniques** (ancienne table de
crédits remplacée). Parmi les 52 candidats sans autre clé du lot à leur cible,
**11 sont actifs et 41 sont exclus**. Parmi les cinq paires, quatre sont actives
et une appartient aux crédits exclus. Aucun nom propre n’est traduit
artificiellement pour justifier une route.

Les contrats sont dans `languages/es-maint/text_aliases.json` et réutilisent
`TextAliases`, le CSV, le convertisseur JSON, le builder et les patches existants.
Il n’existe aucun second réinserteur. Les préimages EN complètes, préfixes nuls,
références exhaustives à tous les alignements et correspondances ES sont
contrôlés avant insertion ; les consommateurs et préfixes sont relus après les
patches. Les gardes figent les racines, fenêtres, routines et polices pertinentes.

Pour chacun des 57 cas, l’offset map contient une correspondance `matched` **au
début textuel vivant** ; les octets ES et les pointeurs aux sites recensés sont
vérifiés. Ces versions ont ici des adresses EN/ES égales : cette égalité n’est
jamais utilisée comme preuve de correspondance. Le cas `english_only` existant
reste disponible sans être nécessaire pour ces candidats.

## Consommateurs établis dans la ROM actuelle

### Messages de Berry Crush

La table `0x46E328` est chargée aux instructions `0x14BCBC` et `0x14BCF0`
(littéraux `0x14BCEC` et `0x14BD1C`). Le lecteur choisit son entrée, développe
éventuellement les buffers via `0x8FCC`, puis imprime via `0xF6CD0`, police 2.
Cela couvre les débuts `41CE3C`, `41CEA8`, `41CF14`, `41CF50`, `41CFD4`, `41D008`.

L’initialisation Berry Crush appelle `0xF6C6C` à `0x14D774`. Son littéral
`0xF6C84` pointe sur `0x41F42C`, template `00020f1a040f9801` : fenêtre de
26 × 4 tuiles, soit **208 × 32 pixels**. Le printer initialise x=0, y=1.
Les textes sont limités à **208 pixels et deux lignes par page**. Les commandes
FC/FD/F8/F9/F7 et leurs arguments, FA/FB ainsi que l’ordre des buffers restent
identiques à la source. Les ruptures de page terminales ne créent pas une page
visible supplémentaire. La réserve conservatrice des buffers FD est de 54 pixels.

**Défaut EN préexistant à `41CF13→41CF14`.** La source contient trois lignes sans
pagination. Le moteur FE avance de 15 pixels (routine `0x5880–0x589C`, hauteur de
police 14 + espacement 1), plaçant la troisième à y=31 dans une fenêtre de hauteur
32. Ce contrat n’autorise pas cette disposition défectueuse : sa valeur identique
EN est refusée par le budget. Pour F-861, une formulation sur deux lignes est
requise. Seul ce cas déclare `preserve_line_count: false` ; aucune commande ni
argument n’est supprimé ou ajouté, et FA/FB restent protégés. F-1041 ne propose
ni n’enregistre cette traduction finale.

### Résultats et classements Berry Crush

La table `0x46F4B8` est chargée à `0x14E060` et `0x14E76A`. Les titres de
classement passent par `0x14DF44` : largeur calculée par `0x5ED4`, centrage,
puis impression `0x12E51C`, police 2. Les templates `0x46E428` et `0x46E430`
ont une largeur de **176 pixels** ; celui de `0x46E438`, de **192 pixels**.
Les titres ont donc un budget de 176 pixels sur une ligne.

Les libellés Time et Pressing Speed sont lus dans `0x14E32C` (sites `0x14E564`
et `0x14E584`), puis imprimés à x=2. Les réserves horizontales tiennent compte
des nombres et unités de droite : Time dispose de **102 pixels**
(190 − 22 pour « sec. » − 32 pour le nombre − 20 pour « min. » − 3 − 9 − 2).
Pressing Speed dispose de **95 pixels**, avec 38 pixels pour le nombre et
55 pour Times/sec. Le suffixe Times/sec est borné à **55 pixels**, afin que ces
budgets indépendants ne puissent se chevaucher. Les voisins utilisés dans ces
réserves restent hors de ce contrat.

Times/sec est lu aux deux sites `0x14E588` et `0x14EA28`, imprimé avec la
**police 3**. Ses métriques latines sont celles de la police 2, table `0x207300` :
le dispatch `0x1EA664`/`0x1EA66C` sélectionne `0x66F9`/`0x67CD`, cette dernière
chargeant la même table via le littéral `0x67E0`. Le rendu police 3 rejoint les
glyphes latins police 2 (`0x5BCE→0x6724→0x67C0→0x65B8`). La table `0x1FB100`
correspond à la police 1 et ne doit pas être substituée ici.

Le suffixe « times » conserve un budget conservateur de **32 pixels** pour
préserver la colonne des noms et le nombre de pressions. Le fragment BERRY a
**90 pixels**, réserve du buffer comprise (54 + 36). L’espace entre le buffer et BERRY
appartient au texte vivant, comme l’espace initial du suffixe « times ». Il ne
faut pas les confondre avec les deux octets nuls d’alignement précédant les
débuts `0x41D034` et `0x41D044`.

### Surnom GHOST

`0x41D147→0x41D148` n’est pas un simple label décoratif. Le littéral `0x44940`
est chargé à `0x4492C` et transmis à la comparaison de chaînes `0x8E28`.
Les sites `0x7F864` et `0x7F994` alimentent `SetMonData` à `0x4037C`, champ 2
(surnom). Les trois consommateurs doivent donc recevoir exactement la même
chaîne. Le contrat est borné à **10 octets de surnom plus FF**, une ligne et
60 pixels ; aucune troncature du surnom n’est admise.

## Exclusion de l’ancienne table de crédits

Les 42 pointeurs recensés sont des champs de l’ancienne table `0x4145BC`,
stride 12 (titre, noms, métadonnée). Cette structure identifie des crédits,
mais **ce n’est plus la racine utilisée par le moteur**. Les instructions
`0xF3EC6` et `0xF3F26` chargent la table **`0x1FB0DB0`**, via les littéraux
`0xF3F18` et `0xF3F78`. Le script actuel est **`0x1FB12D8`**, via `0xF3F1C`
et `0xF3F7C`. Les 53 enregistrements actuels pointent sur les crédits Unbound,
notamment `0x1EEFE30` et suivants ; aucun ne pointe sur les 42 cibles candidates.
Une réinsertion dans l’ancienne table ne prouverait donc aucun affichage joué.

Le moteur actuel utilise la fenêtre `0x410E08` (240 × 96 pixels), les titres en
police 1 à x=2/y=6, et les noms en police 2 à x=8/y=6. Ces faits sont documentés
pour distinguer le consommateur réel du vestige ; ils n’autorisent aucune
modification des nouveaux crédits, hors périmètre. Les préimages des crédits
exclus, leurs lignes vides, leur éventuel FC13 et leurs voisins restent intactes.
`TextAliases` refuse une saisie sous la clé contractuelle **ou** la cible de
chaque entrée exclue. L’exclusion est technique, pas un jugement de traduction.

## Stratégie des cinq doublons pour F-861

Pour `41CE3B→41CE3C`, `41CEA7→41CEA8`, `41CF13→41CF14` et
`41CF4F→41CF50`, utiliser **une seule saisie sous la clé contractuelle décalée**.
Dans le rapport des 374 entrées, la clé vivante est qualifiée comme doublon
canonique de cette route, sans seconde injection. `check_keys` refuse les deux
clés présentes ensemble, même avec deux textes identiques ; il n’est pas affaibli.

Pour `41DC45→41DC48`, les **deux clés sont exclues** : ancien crédit sans lecteur
actuel. Aucune saisie artificielle, copie de nom propre ou traduction identique
ne doit contourner ce refus.

## Relevé exhaustif des 57 candidats

La colonne ES donne la cible contrôlée par l’offset map et les préimages ;
« ancien crédit » désigne un pointeur dormant, et non un consommateur final actif.
Toutes les adresses sont des offsets physiques ROM en hexadécimal.

| Clé contractuelle | Début textuel / ES | Sites de référence EN | Traitement | Budget |
|---|---|---|---|---|
| `41CE3B` | `41CE3C` / `41CE3C` | `46E328` | Alias actif, doublon canonique | 208 px, 2 lignes/page |
| `41CEA7` | `41CEA8` / `41CEA8` | `46E330` | Alias actif, doublon canonique | 208 px, 2 lignes/page |
| `41CF13` | `41CF14` / `41CF14` | `46E334` | Alias actif, doublon canonique | 208 px, 2 lignes/page ; EN 3 lignes refusé |
| `41CF4F` | `41CF50` / `41CF50` | `46E338` | Alias actif, doublon canonique | 208 px, 2 lignes/page |
| `41CFD1` | `41CFD4` / `41CFD4` | `46E344` | Alias actif | 208 px, 2 lignes/page |
| `41D005` | `41D008` / `41D008` | `46E348` | Alias actif | 208 px, 2 lignes/page |
| `41D032` | `41D034` / `41D034` | `46F4B8` | Alias actif | 32 px, 1 ligne |
| `41D042` | `41D044` / `41D044` | `46F4C0` | Alias actif | 90 px, 1 ligne |
| `41D04D` | `41D050` / `41D050` | `14E564` | Alias actif | 102 px, 1 ligne |
| `41D056` | `41D058` / `41D058` | `14E584` | Alias actif | 95 px, 1 ligne |
| `41D096` | `41D098` / `41D098` | `14E588`, `14EA28` | Alias actif | 55 px, 1 ligne |
| `41D0D1` | `41D0D4` / `41D0D4` | `46F4C4` | Alias actif | 176 px, 1 ligne |
| `41D0E6` | `41D0E8` / `41D0E8` | `46F4C8` | Alias actif | 176 px, 1 ligne |
| `41D0FD` | `41D100` / `41D100` | `46F4CC` | Alias actif | 176 px, 1 ligne |
| `41D147` | `41D148` / `41D148` | `044940`, `07F864`, `07F994` | Alias actif | 60 px, 1 ligne ; 11 octets avec FF |
| `41D1FD` | `41D200` / `41D200` | `4145C8` | Exclu : ancien crédit | Aucune injection |
| `41D222` | `41D224` / `41D224` | `4145CC` | Exclu : ancien crédit | Aucune injection |
| `41D247` | `41D248` / `41D248` | `4145D4` | Exclu : ancien crédit | Aucune injection |
| `41D281` | `41D284` / `41D284` | `4145D8` | Exclu : ancien crédit | Aucune injection |
| `41D2C5` | `41D2C8` / `41D2C8` | `4145E4` | Exclu : ancien crédit | Aucune injection |
| `41D312` | `41D314` / `41D314` | `4145EC` | Exclu : ancien crédit | Aucune injection |
| `41D32D` | `41D330` / `41D330` | `4145F0` | Exclu : ancien crédit | Aucune injection |
| `41D36D` | `41D370` / `41D370` | `4145F8` | Exclu : ancien crédit | Aucune injection |
| `41D3BE` | `41D3C0` / `41D3C0` | `414604` | Exclu : ancien crédit | Aucune injection |
| `41D3FB` | `41D3FC` / `41D3FC` | `414610` | Exclu : ancien crédit | Aucune injection |
| `41D471` | `41D474` / `41D474` | `41462C` | Exclu : ancien crédit | Aucune injection |
| `41D4B9` | `41D4BC` / `41D4BC` | `414638` | Exclu : ancien crédit | Aucune injection |
| `41D546` | `41D548` / `41D548` | `414650` | Exclu : ancien crédit | Aucune injection |
| `41D56B` | `41D56C` / `41D56C` | `414658` | Exclu : ancien crédit | Aucune injection |
| `41D587` | `41D588` / `41D588` | `41465C` | Exclu : ancien crédit | Aucune injection |
| `41D6E9` | `41D6EC` / `41D6EC` | `414694` | Exclu : ancien crédit | Aucune injection |
| `41D707` | `41D708` / `41D708` | `414698` | Exclu : ancien crédit | Aucune injection |
| `41D766` | `41D768` / `41D768` | `4146A4` | Exclu : ancien crédit | Aucune injection |
| `41D799` | `41D79C` / `41D79C` | `4146B0` | Exclu : ancien crédit | Aucune injection |
| `41D7F1` | `41D7F4` / `41D7F4` | `4146BC` | Exclu : ancien crédit | Aucune injection |
| `41D849` | `41D84C` / `41D84C` | `4146C8` | Exclu : ancien crédit | Aucune injection |
| `41D8AD` | `41D8B0` / `41D8B0` | `4146D4` | Exclu : ancien crédit | Aucune injection |
| `41D8EA` | `41D8EC` / `41D8EC` | `4146E0` | Exclu : ancien crédit | Aucune injection |
| `41D94B` | `41D94C` / `41D94C` | `4146EC` | Exclu : ancien crédit | Aucune injection |
| `41DA06` | `41DA08` / `41DA08` | `41470C` | Exclu : ancien crédit | Aucune injection |
| `41DA39` | `41DA3C` / `41DA3C` | `414718` | Exclu : ancien crédit | Aucune injection |
| `41DA6B` | `41DA6C` / `41DA6C` | `414724` | Exclu : ancien crédit | Aucune injection |
| `41DA85` | `41DA88` / `41DA88` | `414728` | Exclu : ancien crédit | Aucune injection |
| `41DAC3` | `41DAC4` / `41DAC4` | `414734` | Exclu : ancien crédit | Aucune injection |
| `41DAE5` | `41DAE8` / `41DAE8` | `41473C` | Exclu : ancien crédit | Aucune injection |
| `41DB3A` | `41DB3C` / `41DB3C` | `41474C` | Exclu : ancien crédit | Aucune injection |
| `41DB7B` | `41DB7C` / `41DB7C` | `414754` | Exclu : ancien crédit | Aucune injection |
| `41DBA1` | `41DBA4` / `41DBA4` | `414758` | Exclu : ancien crédit | Aucune injection |
| `41DBDA` | `41DBDC` / `41DBDC` | `414760` | Exclu : ancien crédit | Aucune injection |
| `41DBF6` | `41DBF8` / `41DBF8` | `414764` | Exclu : ancien crédit | Aucune injection |
| `41DC29` | `41DC2C` / `41DC2C` | `41476C` | Exclu : ancien crédit | Aucune injection |
| `41DC45` | `41DC48` / `41DC48` | `414770` | Exclu : ancien crédit ; deux clés interdites | Aucune injection |
| `41DCC5` | `41DCC8` / `41DCC8` | `41477C` | Exclu : ancien crédit | Aucune injection |
| `41DD1D` | `41DD20` / `41DD20` | `414788` | Exclu : ancien crédit | Aucune injection |
| `41DD79` | `41DD7C` / `41DD7C` | `414794` | Exclu : ancien crédit | Aucune injection |
| `41DDC6` | `41DDC8` / `41DDC8` | `41479C` | Exclu : ancien crédit | Aucune injection |
| `41DE21` | `41DE24` / `41DE24` | `4147A8` | Exclu : ancien crédit | Aucune injection |

## Préservation et validation

Aucun `combined`, `protected_entries.yaml`, glossaire ou `lots.json` n’est
modifié par ce ticket. Les huit clés sans référence directe ni candidat
(`41CC7B`, `41D195`, `41E2EC`, `41E76B`, `41EFB8`, `41F0A8`, `41F0BD`, `41F160`)
et les notices Pokédex restent à la qualification de F-861. Aucun préfixe nul
n’est converti en espace traduit. Aucun fallback ni aucune troncature ne sont
admis ; les commandes et leur ordre restent contrôlés après les patches.

La campagne CSV réel → JSON → builder → patches utilise uniquement un combined
et des sentinelles temporaires. Les 15 routes sont forcées en relocation ; les
18 lectures finales sont exactes. Les comparaisons complètes avant patches puis
contre un témoin portant les mêmes patches acceptent uniquement les pointeurs
sélectionnés et les allocations. Les préfixes, voisins et sources de production
restent inchangés. Les cinq doubles revendications et les clés exclues sont
refusées. Les préimages et les pointeurs des 42 crédits exclus sont également
gardés après patches, y compris leurs lignes vides et commandes FC13.

Le test Playwright `specs/es011-aliases.spec.ts` passe en headless avec mGBA
offscreen : 18 lectures, commandes avec arguments, sept rendus par les routines
natives, mesures moteur et bornes des pixels. Il vérifie aussi les deux racines
actuelles des crédits et l’absence des 42 cibles historiques dans leur table.
La capture est conservée dans le dossier temporaire OS et attachée au ticket
(`6f869387-403e-4a05-8d1d-3e6f71b6335c`). Aucune sauvegarde en jeu.

Le build ES maintenu passe avec `BUILD_NUMBER=0`. Le témoin FR avant modification
est `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Les résultats finaux des suites et des builds multilingues sont consignés dans
la résolution du ticket, après les hooks et le rebase.

Non vérifié : parcours complets des minijeux et du combat GHOST. La preuve est
une mire native en RAM lisant les pointeurs finaux ; elle ne certifie pas les
traductions finales de F-861. Les 42 anciens crédits ne sont pas rendus pour
simuler un parcours qui ne les consomme plus.
