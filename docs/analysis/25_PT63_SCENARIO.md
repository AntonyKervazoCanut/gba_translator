# 25 — PT-63 : Dehara, Distortion World, Dresco, Epidimy et Fallshore

## Périmètre et livraison

F-822, manifeste PT-63 : exactement 299 offsets, de `0x1efe70a` à
`0x1f052aa`. Les prérequis F-758 et F-759 sont intégrés. Les textes ont été
traduits depuis EN et comparés au FR au même offset ; les noms propres, objets
et mouvements non attestés en PT-BR suivent le glossaire F-759.

Le bilan exhaustif est `languages/pt/data/pt63_audit.json`, dans l'ordre du
manifeste. Il contient, pour chaque offset, EN, FR, préimage ROM, pointeurs,
statut, justification et, pour chaque texte livré, PT, octets, largeurs et
hypothèses des tampons : **272 traductions, 19 noms/cris conservés, 8 exceptions**.
Toutes les 291 entrées ajoutées ont leur protection exacte. Aucune traduction
préexistante n'est supprimée ou remplacée ; aucun autre lot n'est modifié.

Domaines : ascenseur et Luxury Balls de Dehara, Nex et Giratina, missions
Leitura Básica et Não Desligue, Trainer House de Dresco, échanges de Pokémon,
Oddish et Dream Mist, Epidimy/Thundercap Mt., Master Ball et Hoopa, pêche,
effacement des mouvements, marché et Ginásio de Fallshore, Hidden Power.

## Injection et géométrie

Le finaliseur `batch_63` réutilise `BorriusTextPatch` après les réparations,
la police et les repointages. Il contrôle les préimages et toutes les commandes,
alloue sans écraser de voisin, repointe les consommateurs et vérifie les octets
finaux. Il est atomique et idempotent. Ce lot ne contient pas de cellule fixe
indexée : même les menus, missions et titres musicaux ont des pointeurs directs.

Les dialogues Nex `0x1efeda8` et Gem `0x1f00d23` étaient tronqués dans le fichier
EN. Leur fin et leurs FA manquants ont été récupérés dans la ROM jusqu'au FF.
Le libellé `0x1efecf6` conserve intégralement `C0 46` suivi de Distortion World ;
son pointeur script est `0x141eb2b`. Les libellés musicaux D/N restent inchangés.

FA/FB et les contrôles FC/FD sont conservés dans leur ordre exact. Seuls les
retours FE sont ajustés : au plus deux lignes initiales par page, puis une ligne
par FA. Les descriptions de missions utilisent au plus trois lignes à 172 px ;
les menus une ligne à 170 px ; les dialogues sont limités à 198 px. La lettre à
Jax garde ses lignes blanches et son format plein écran.

Les tests ROM mesurent les cinq polices réelles, après application des tildes,
avec des noms de dix W, noms de mouvements/objets de dix-neuf W lorsque requis,
compteurs de trois chiffres et suffixes pluriels. `native_max_width` est le
budget d'affichage. `max_width` est distinct : le finaliseur partagé utilise
un modèle qui réserve 54 px à chaque FD, même à un compteur ou au suffixe s ;
ce plafond théorique n'est jamais présenté comme une largeur écran autorisée.

## Exceptions sans pointeur

`0x1f02269`, `0x1f022fa`, `0x1f02367`, `0x1f023b8`, `0x1f023c9`,
`0x1f0243a`, `0x1f024cd`, `0x1f02510` : anciens dialogues de Mirskle, chacun
sans référence GBA absolue dans le scan à chaque octet des 32 Mio source.
Les préimages et contextes binaires sont conservés dans le bilan. Le script
vivant du Soil référence `0x1f02458` depuis `0x1e68bc6`, vérifié séparément.
Aucune lecture de table fixe identifiée dans ce bloc de chaînes terminées par FF.
Ces huit textes restent intacts ; aucune traduction ni injection n'est revendiquée.
Cette justification porte sur les références statiques observables et ne prétend
pas démontrer l'absence de tout adressage calculé possible.

## Vérifications reproductibles

- `python3 -m pytest -q tests/unit/pt/test_batch_pt63.py tests/unit/test_translation_integrity.py`
- `make build-pt`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt63_rom.py`
- `npx playwright test -c tests/e2e-playwright/playwright.pt63.config.ts`

La preuve Playwright démarre mGBA hors écran sur une copie temporaire de la ROM
finale. Seul un script de sonde est ajouté ; les chaînes, glyphes et fenêtres
sont ceux du jeu. Trois pointeurs livrés sont contrôlés en octets avant affichage
(titre de mission, Dream Mist, reconnaissance de Hoopa). L'OCR assertif valide
les premières lignes rendues avant la capture. La sauvegarde fixture reste
inchangée. La capture est écrite dans le dossier temporaire OS et jointe au ticket.

## Non vérifié

La sonde n'est pas un parcours naturel des 291 entrées ni une visite de chaque
mission dans son menu. Les pages et pointeurs complets sont contrôlés en binaire ;
la certification du parcours intégral revient à T-848. Aucun pipeline distant,
push, artefact de release ou changement du statut global PT n'est inclus.
