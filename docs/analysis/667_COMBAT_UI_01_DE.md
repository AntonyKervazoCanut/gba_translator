# B-667 — Qualification combat_ui-01

Périmètre fermé : 300 offsets du ticket, sans audit global ni modification FR/IT.
Les valeurs EN/FR/DE sont comparées en dernière occurrence gagnante ; la ROM EN
propre fait foi lorsque les extractions historiques sont décalées ou contiennent
des graphismes. La fixture `tests/unit/fixtures/combat_ui_01.json` conserve pour
chaque offset les trois valeurs, la préimage hexadécimale, le texte canonique avec
arguments de commandes, les références absolues et une décision motivée.

## Corrections et exclusions

31 corrections livrées : dialogues absents (Log, arène Dehara, téléportation,
pension, terrain), couleurs et structure des pages, genre neutre du Pokémon,
termes Klimaschutz/Scherenmacht, Anführer et préfixe de combat Für.
Les noms propres anglais explicitement voulus sont conservés. Les emprunts allemands
valables (Shopping, Software, Insomnia, Chlorophyll…) ne sont pas traduits artificiellement.

113 fragments non vivants ou données non textuelles, 86 noms propres légitimes,
68 entrées déjà correctes/patchées et deux besoins séparés sont documentés.
Une absence de pointeur absolu ne suffit pas à déclarer une entrée morte : les
classes de Dresseurs utilisent des cellules indexées, parfois avec pointeur CFRU
en tête ; les fragments graphiques et suffixes sont distingués de ces cellules.

Besoins hors périmètre des éditions de texte :

- `0x192116` : le script `0x16AA68` vise un suffixe à +0x9D du conseil complet
  `0x192079` (Mirskle/Icicle Cave). Rétablir la cible et qualifier le message entier.
- `0x1A5200` : le script `0x1A6990` vise +10 dans `0x1A51F6` (« Obtained the … »).
  Corriger la cible et le message complet dans un ticket distinct.

Cas résolu par une traduction existante : `0x26D4DF`. Les scripts `0x26D3C6`/`0x26D3E4` visent une structure
  `00 FC 03 00 00 00` suivie du suffixe déjà traité à `0x26D4E5`. Ne pas ajouter
  une écriture concurrente chevauchante : après build, les deux pointeurs atteignent
  bien « Fangen wir an! », avec FC0300 conservé. Aucun patch supplémentaire requis.

Les fausses extractions `0x1A5AD5` et `0x1A6447` commencent avant les vrais
messages ; les vrais débuts `0x1A5AD6` et `0x1A6448` sont qualifiés séparément.
`0x3FCB4B` reste absent : suffixe connu de « rose! », susceptible de corrompre le
buffer voisin s’il était réintroduit. Les copies Lichtschild/Reflektor sans
référent `0x3D98DC`/`0x3D9EAC` ne remplacent pas les descriptions actives ailleurs.

## Contraintes vérifiées

Les corrections source gardent strictement l’ordre des commandes FC/FD et de
leurs arguments, ainsi que FE/FA/FB. En ROM, le moteur peut déplacer les mots
autour des ruptures : les tests comparent séparément la suite exacte FC/FD et
la suite exacte FE/FA/FB, plus le texte et les limites de pages. Aucun contrôle,
argument, page ou ligne n’est supprimé ; les boîtes conservent leur forme. Les formes brutes et les alias sont comparés après
encodage, pas par simple recherche d’accolades. Les tests source réservent dix
glyphes larges par buffer et limitent chaque ligne à 192 pixels. Cette borne ne
certifie pas une valeur dynamique arbitraire ; le moteur limite les noms injectés.
Aucun buffer Sohn/Tochter n’est modifié. Le tutoiement est conservé ; Teala garde
l’adresse collective « ihr », la mère le registre affectueux « Schatz ».

Chaque valeur modifiée est protégée exactement dans `protected_entries.yaml` et
validée par `tests/unit/test_translation_integrity.py`. Huit lignes existantes
modifiées et 23 vrais débuts ajoutés ; ordre, doublons et fins de ligne conservés.
Aucun patch, ressource de données de traduction, source FR/IT ou hash FR modifié.
Empreinte de la ROM FR principale, inchangée avant/après validation :
`74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
Les artefacts de build sont privés au worktree ; les entrées ROM sources restent
strictement en lecture seule.

## Validation

- Commit de traduction `cb3c9f2e` : diff relu, exclusivement les 31 offsets annoncés.
- `make build-de` exécuté avec succès par le hook actif, après les builds FR/IT
  également imposés par ce hook (artefacts privés au worktree).
- `python3 -m pytest tests/unit/test_combat_ui_01.py -q -o addopts=''` :
  **65 réussis**, dont 31 vérifications ROM sur **35 sites de pointeurs**.
- `tests/unit/test_translation_integrity.py` : **30 réussis**.
- `npx playwright test --config tests/e2e-playwright/playwright.combat-ui-01.config.ts` :
  **1 réussi**, OCR « Drücke START für das Menü! », capture attachée
  `393754fd-5526-4830-9248-e9f90bd0aea2`, hors dépôt.
- Lint ciblé Ruff : réussi. `make test-python` : **2998 réussis, 3 skips préexistants,
  1373 désélectionnés**, aucun échec (195,83 s). Les deux fichiers de tests ciblés
  totalisent **95 réussis** après ajout des gardes de padding et de non-chevauchement.

Les quatre textes allongés en place utilisent uniquement du padding FF prouvé
par la source EN (0x17FF4A, 0x18EBE6, 0x18ED81, 0x1A59E7) ; aucun pointeur EN
n’entre dans leur extension. Les dix relocalisations ont également une préimage
entièrement FF. Les plages finales corrigées sont disjointes.
La fixture consigne aussi les 192 correspondances de pointeurs du lot après le
build du commit `cb3c9f2e` (instantané documentaire, les tests résolvent toujours
les cibles vivantes du build courant), en
signalant les pseudo-références binaires, sans les présenter comme des scripts.

Les premiers essais de hooks ont détecté deux prérequis locaux manquants : ROM DE
requise par un test dry-run et JSON de préparation FR périmé. Ils ont été résolus
par copies privées des artefacts et `make prepare-fr` local, sans édition FR/IT
ni contournement de hook. Les premiers contrôles ROM refusaient les quatre
allongements dans du padding : les octets FF et l’absence de pointeur dans ces
extensions ont été vérifiés avant de corriger cette borne de test. Les 2857 tests rapides et les 68 tests Vitest du commit
ont ensuite réussi (un skip préexistant signalé, aucun ajouté).

Le test Playwright headless utilise mGBA offscreen et suit le pointeur réel du
tutoriel START. Seul un script d’affichage temporaire est injecté dans une copie
hors dépôt : aucun octet de texte ni police n’est remplacé. Assertions de texte
ROM et OCR avant capture ; aucune sauvegarde en jeu. Cette sonde valide le texte
et la police dans une boîte réelle, sans prétendre parcourir toutes les scènes.

## Non vérifié

Parcours naturel des 300 scènes, valeurs dynamiques arbitraires et corrections
structurelles des deux pointeurs tronqués hors lot ci-dessus. Aucun pipeline distant ni push exécuté.

## Décision par offset

EN canonique, EN/FR historiques et DE avant/après complets sont dans la fixture.
Les références ci-dessous sont les occurrences absolues EN, y compris les faux
positifs explicitement rejetés dans la décision ; les références des corrections
sont contrôlées dans la ROM reconstruite. « ∅ » signifie absence dans le combined.

| Offset | Scène / structure | Décision et justification | DE final | Références EN | Octets EN / DE corrigé |
|---|---|---|---|---|---|
| 0x17FF4A | Dehara, client du grand magasin | corrigé : Absent DE/FR, loadpointer de message valide. Couleurs FC0106 puis FC0104 conservées. | `Ich kann nicht aufhören zu kaufen!\pEs gibt so viel Auswahl im\n<0xFC><0x01><0x06>Dehara Department Store<0xFC><0x01><0x04>!` | 0x166caf | 90 / 93 |
| 0x180AF3 | Données ROM | fragment non vivant : Données binaires prises pour du texte, zéro référent. | ∅ | aucune exacte | 13 / — |
| 0x183482 | Valley Cave, panneau | nom propre légitime : Valley Cave explicitement conservé par english_toponyms.yaml ; référent de panneau valide. | `Valley Cave` | 0x167f70 | 12 / — |
| 0x18EA45 | Laboratoire Prof. Log | corrigé : Absent DE/FR, loadpointer de message valide ; Prof. Log conservé. | `Das ist Prof. Logs Pokémon.` | 0x169de6 | 28 / 28 |
| 0x18EA66 | Laboratoire Prof. Log, tutoriel | corrigé : Aide de commande absente DE/FR ; START conservé comme bouton. | `Drücke START für das Menü!` | 0x169e73 | 30 / 27 |
| 0x18EBE6 | Laboratoire Prof. Log | corrigé : Absent DE/FR, assistant scientifique, première personne. | `Als Prof. Logs Assistent\nerforsche ich Pokémon.` | 0x169e1c | 37 / 48 |
| 0x18ED81 | Laboratoire Prof. Log | corrigé : Absent DE/FR ; stats rendues par Statuswerte, aucune confusion avec statuts. | `Prof. Log erforscht seit Jahren\ndie Statuswerte von Pokémon.\pViele Trainer kommen mit Fragen\nzu diesen Werten zu ihm.` | 0x169e48 | 108 / 118 |
| 0x192116 | Dresco, conseiller arène Mirskle | besoin de patch séparé : Le loadpointer 0x16AA68 vise un suffixe à +0x9D du texte complet 0x192079 (conseil Mirskle/Icicle Cave). Corriger la cible de script et le message complet hors lot ; traduire seulement le fragment perdrait le conseil. ROM DE : le script atteint seulement « Vorteil gegen ihn / verschaffen. » ; début du conseil toujours absent. | ∅ | 0x16aa68 | 26 / — |
| 0x1949CB | PNJ échange Pokémon | déjà correct : Échange Pokémon : buffers FD02 puis FD03, tutoiement et pages conservés. | `Hallo!\nHast du ein {STR_VAR_1}?\pMöchtest du es gegen mein\n{STR_VAR_2} tauschen?` | 0x16b5ee | 50 / — |
| 0x197874 | Dehara, arène Galavan | corrigé : Panneau arène absent DE/FR ; FD06 de liste des vainqueurs conservé brut. | `Pokémon-Arena von Dehara\nLeiter: Galavan\pSiegreiche Trainer:\n<0xFD><0x06>` | 0x16d1d8 | 56 / 64 |
| 0x198BBB | Enfant ninja / parents déplaçant des rochers, script 0x7C0A4C | corrigé : Absent DE/FR ; enfant futur ninja, contraste force/ruse. | `Eines Tages werde ich ein Ninja!\pMeine Eltern setzen auf Gewalt,\naber ich werde listig sein!` | 0x7c0a4c | 97 / 93 |
| 0x19A4F8 | Ville aux cauchemars, voisin | corrigé : Absent DE/FR ; avertissement cauchemars ; tutoiement. | `Diese Stadt leidet schon lange\nunter schlimmen Albträumen.\pWenn du einen Wohnort suchst,\nwäre es wohl besser,\lwoanders zu wohnen.` | 0x16e8fa | 161 / 130 |
| 0x19A5BE | Sommet, service de téléportation Abra | corrigé : Trois loadpointer de proposition de téléportation, absent DE/FR. Abra conservé. | `Brauchst du einen Weg zurück\nden Berg hinunter?\pMein Abra und ich teleportieren\ndich gern nach unten.\pWas meinst du?\nSollen wir dich teleportieren?` | 0x7c3779, 0x7c3811, 0x7c383e | 146 / 148 |
| 0x19A6B1 | Service de téléportation Abra | nom propre légitime : Cri Abra « Bra! », trois messages/opcodes 67 valides ; onomatopée à conserver. | ∅ | 0x7c386f, 0x7c5462, 0x7c550e | 5 / — |
| 0x19A7A0 | Boutique, client objets de combat | corrigé : Objet X Attack = X-Angriff, Attack = Angriff ; absent DE/FR. | `Haben sie kein X-Angriff?\pIch mag es, weil es im Kampf\nden Angriff erhöht.` | 0x16ea12 | 81 / 75 |
| 0x19E9E5 | Assistant Prof. Log, récompense Pokédex | corrigé : Paire couleur autour du titre perdue ; promesse récompense dupliquée. Restaurer FC0106/04 + FD02 + FD01 + FD02 et les 3 pages/1 scroll EN. | `Hallo!\nIch bin <0xFC><0x01><0x06>Prof. Logs Assistent<0xFC><0x01><0x04>.\pHast du im Pokédex Daten zu\n<0xFC><0x01><0x06><0xFD><0x02><0xFC><0x01><0x04> Arten, soll ich\ldich belohnen.\pAlso, <0xFD><0x01>, sag mir:\pHast du schon Daten z… (fixture)` | 0x16fde9 | 217 / 196 |
| 0x1A2328 | Données/graphiques et ancien message objet | fragment non vivant : Suffixe du texte 0x1A231B « Obtained the TRI-PASS! ». Matches dans graphismes (0xC70FFB, 0x125EFF8, 0x12EDDAE), pas référents de texte identifiés. Ne pas injecter un nom isolé. | `TRI-PASS!` | 0xc70ffb, 0x125eff8, 0x12eddae | 10 / — |
| 0x1A2D75 | Ancien dialogue donneur de capacités | fragment non vivant : Suffixe de 0x1A2D43 ; unique match 0x51BD6C dans données graphiques sans opcode de message. | ∅ | 0x51bd6c | 12 / — |
| 0x1A2E4E | Ancien dialogue donneur de capacités | fragment non vivant : Suffixe de 0x1A2E20 ; unique match 0x4E9294 dans données graphiques sans opcode de message. | ∅ | 0x4e9294 | 11 / — |
| 0x1A5200 | Script obtention objet | besoin de patch séparé : Loadpointer 0x1A6990 réellement présent mais vise +10 dans « Obtained the {STR_VAR_2}! » début 0x1A51F6. Restaurer message/cible complet hors lot avant localisation. ROM DE : le script atteint seulement « n! » ; problème de pointeur confirmé, pas une omission à combler au suffixe. | ∅ | 0x1a6990 | 7 / — |
| 0x1A597B | PNJ échange Pokémon | déjà correct : Échange Pokémon, FD02 puis FD03 et ordre des pages conservés. | `Ich suche das Pokémon\n{STR_VAR_1}!\pMöchtest du eins gegen mein\n{STR_VAR_2} tauschen?` | 0x16fd73 | 59 / — |
| 0x1A59E7 | PNJ après échange Pokémon | corrigé : Remplace le pronom masculin er par une phrase neutre ; même buffer FD03, aucune rupture ajoutée. | `Mein altes <0xFD><0x03> ist toll!` | 0x16fdd0 | 23 / 24 |
| 0x1A5AD5 | PNJ échange, faux début extrait | fragment non vivant : Octet AA préfixé (« 9 » décodé), aucun référent ; vrai début à 0x1A5AD6. Ne pas corriger le faux préfixe. | `9Hallo!\nHast du ein {STR_VAR_1}?\pWillst du es gegen mein\n{STR_VAR_2} tauschen?` | aucune exacte | 51 / — |
| 0x1A5AD6 | PNJ échange Pokémon | corrigé : Vrai début référencé 0x16E35F, absent DE/FR ; voisin AA à 0x1A5AD5 est faux début. | `Hallo!\nHast du ein <0xFD><0x02>?\pWillst du es gegen mein\n<0xFD><0x03> tauschen?` | 0x16e35f | 50 / 60 |
| 0x1A5B60 | PNJ après échange Pokémon | déjà correct : FD03 puis FD02 fidèles à EN ; tutoiement, question elliptique acceptable. | `Na, mein früheres {STR_VAR_2}?\nMeinem {STR_VAR_1} geht es super!` | 0x16e3d6, 0x7c2c4b | 40 / — |
| 0x1A5BC6 | PC, évaluation Pokédex | corrigé : Absent DE, accès PC Prof. Log ; contrôle page FB conservé. | `Prof. Logs PC wird aufgerufen…\pPokédex-Bewertung wird\naufgerufen…` | 0x1a6a88 | 61 / 70 |
| 0x1A6046 | Mère, conseil soin/Bellin Town | corrigé : Texte DE fidèle mais pages déplacées ; restaurer 7 FB et garder paires couleur/lieux voulus. Mère, tutoiement affectueux ; aucun buffer Sohn/Tochter ici. | `Oh, gut!\pDu und deine Pokémon seht\nschon viel besser aus.\pSind die KP deiner Pokémon niedrig,\ngeht in ein <0xFC><0x01><0x06>Pokémon Center<0xFC><0x01><0x04>!\pDas nächste ist wohl\nin <0xFC><0x01><0x06>Bellin Town<0xFC><0x01><0x04>.\… (fixture)` | 0x1a8df4 | 328 / 326 |
| 0x1A6447 | Cri Pokémon, faux début extrait | fragment non vivant : Octet AA = faux « 9 », zéro référent ; cri vivant à +1. | `9Gyaoo!` | aucune exacte | 8 / — |
| 0x1A6448 | Cri Pokémon | nom propre légitime : Cri « Gyaoo! », trois opcodes 67 valides, pas une phrase anglaise. | `Gyaoo!` | 0x1637d8, 0x163b53, 0x788909 | 7 / — |
| 0x1A6C74 | Interaction eau profonde | corrigé : Message terrain vivant 0x1A6C6C, absent DE/FR. | `Das Wasser ist tiefblau…` | 0x1a6c6c | 31 / 27 |
| 0x1A6CA3 | PC, évaluation Pokédex | corrigé : Absent DE ; FD02 puis FD03 puis FC0602 (police) conservés explicitement. | `Hier ist dein Fortschritt\nbei der Arbeit am Pokédex:\p<0xFD><0x02> Pokémon gesehen und\n<0xFD><0x03> Pokémon gefangen.\p<0xFC><0x06><0x02>Prof. Logs Bewertung:` | 0x1a740e | 116 / 122 |
| 0x1A71AA | PC, Pokédex national | déjà correct : FD02 puis FD03, page conservée ; « besessen » compréhensible pour owned même si gefangen serait plus idiomatique. | `Und dein Nationaler Pokédex zeigt:\p{STR_VAR_1} Pokémon gesehen und\n{STR_VAR_2} Pokémon besessen.` | 0x1a744b | 68 / — |
| 0x1B1D7D | Imprimante carte Dresseur | corrigé : Absent DE/FR ; service à 50 Pokédollars, trois pages intactes. | `Ein Pokémon-Drucker!\pEr druckt dein Pokémon auf\ndie Rückseite des Trainerpasses.\pEs kostet nur ¥50.\nWillst du es ausprobieren?` | 0x1b286e | 138 / 127 |
| 0x1BDBF8 | Club sans fil, réception | corrigé : Traduction raccourcie supprime 2 pages et 3 scrolls ; restaurer structure source ; garder adresse plurielle ihr. | `Ich erkläre euch, wie der\nPokémon-Funk-Club funktioniert.\pHier im obersten Stockwerk\ngibt es zwei Räume.\pDer Raum auf der linken Seite\nheißt Unions-Raum.\pDort trefft ihr Trainer\naus eurer Nähe, die auch\lim Unions-Raum sind.\pMit … (fixture)` | 0x1bbb8a | 743 / 655 |
| 0x1BDF08 | Club sans fil, faux suffixe | fragment non vivant : Suffixe de 0x1BDEDF. Match 0x1BDF64 chevauche les octets d’instructions/pointeurs adjacents (…08 DF 1B 08…), pas un opérande loadpointer. | ∅ | 0x1bdf64 | 11 / — |
| 0x1BE19A | Interaction rocher / Stärke | corrigé : Message terrain loadpointer valide ; Strength = Stärke, interrogation préservée. | `Ein großer Fels. Ein Pokémon\nkönnte ihn zur Seite schieben.\pMöchtest du Stärke einsetzen?` | 0x1be14d | 96 / 90 |
| 0x1BE42B | Interaction plongée | corrigé : Message terrain loadpointer valide ; pas de demande de capacité à inventer. | `Das Meer ist hier tief. Ein\nPokémon könnte hier tauchen.` | 0x1be3cc | 62 / 57 |
| 0x1BEF88 | PNJ profil/Club | corrigé : Absent DE/FR ; conversation profil, ton familier et trois pages conservés. | `Hallo, schön, dich kennenzulernen!\p...Das ist aber unfreundlich.\nSag doch auch mal Hallo!\pNa komm, erzähl mir\netwas über dich.\pIch würde gern dein Profil hören!` | 0x1bee2e | 143 / 161 |
| 0x1BF555 | Pension Pokémon | corrigé : Absent DE/FR ; employé pension, renvoie à sa femme ; tutoiement. | `Ich bin der Pensionsleiter.\pIch helfe dabei, die wertvollen\nPokémon der Trainer zu betreuen.\pSoll ich deine Pokémon aufziehen,\nsprich mit meiner Frau.` | 0x167d82 | 142 / 151 |
| 0x1BF860 | Pension Pokémon | déjà correct : FD02 et FB conservés ; pension, tutoiement cohérent. | `Okay, wir ziehen dein\n{STR_VAR_1} eine Weile auf.\pKomm später zurück, um es abzuholen.` | 0x1719d9 | 63 / — |
| 0x1BFA3B | Pension Pokémon, prix retrait | déjà correct : FD02 puis FD03 et symbole monétaire conservés ; longueur à contrôler après rewrap pipeline. | `Wenn du dein {STR_VAR_1} abholen möchtest,\nkostet das ¥{STR_VAR_2}.` | 0x171ad4 | 44 / — |
| 0x1BFB5A | Pension Pokémon | corrigé : Interjection absente ; loadpointer de dialogue valide. | `Hm?` | 0x1bf549 | 5 / 4 |
| 0x1C5758 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x130348, 0x130388, 0x463124 | 6 / — |
| 0x1C575E | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x46308c, 0x4630d8 | 4 / — |
| 0x1C5762 | Écran choix du nom | fragment non vivant : Ancien nom de la table de sélection, aucun pointeur ; ne pas réintroduire une cellule inutilisée. | ∅ | aucune exacte | 5 / — |
| 0x1C5767 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463090, 0x4630dc | 5 / — |
| 0x1C576C | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463128 | 5 / — |
| 0x1C5771 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x46312c | 4 / — |
| 0x1C5775 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463130 | 5 / — |
| 0x1C577E | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463098 | 5 / — |
| 0x1C5783 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x46309c | 5 / — |
| 0x1C578C | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630a4 | 6 / — |
| 0x1C5792 | Écran choix du nom | fragment non vivant : Ancien nom de la table de sélection, aucun pointeur ; ne pas réintroduire une cellule inutilisée. | ∅ | aucune exacte | 5 / — |
| 0x1C5797 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630ac | 5 / — |
| 0x1C579D | Écran choix du nom | fragment non vivant : Ancien nom de la table de sélection, aucun pointeur ; ne pas réintroduire une cellule inutilisée. | ∅ | aucune exacte | 5 / — |
| 0x1C57A2 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630b4 | 7 / — |
| 0x1C57A9 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630b8 | 6 / — |
| 0x1C57AF | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630bc | 5 / — |
| 0x1C57BC | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630c8 | 6 / — |
| 0x1C57C6 | Écran choix du nom | fragment non vivant : Ancien nom de la table de sélection, aucun pointeur ; ne pas réintroduire une cellule inutilisée. | ∅ | aucune exacte | 5 / — |
| 0x1C57CB | Écran choix du nom | fragment non vivant : Ancien nom de la table de sélection, aucun pointeur ; ne pas réintroduire une cellule inutilisée. | ∅ | aucune exacte | 5 / — |
| 0x1C57D4 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630e4 | 5 / — |
| 0x1C57D9 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630e8 | 7 / — |
| 0x1C57E0 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630ec | 8 / — |
| 0x1C57E8 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630f0 | 6 / — |
| 0x1C57EE | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630f4 | 6 / — |
| 0x1C57F4 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630f8 | 6 / — |
| 0x1C57FA | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x4630fc | 5 / — |
| 0x1C57FF | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463100 | 7 / — |
| 0x1C580A | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463108 | 5 / — |
| 0x1C580F | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x46310c | 5 / — |
| 0x1C5814 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463110 | 5 / — |
| 0x1C5819 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463114 | 6 / — |
| 0x1C5823 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x46311c | 5 / — |
| 0x1C5828 | Écran choix du nom | nom propre légitime : Nom proposé dans la table de choix du nom ; graphie EN volontaire, aucune traduction. | ∅ | 0x463120 | 5 / — |
| 0x1EAF1A | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 14 / — |
| 0x1EAF3A | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 14 / — |
| 0x1EB1C6 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB1E6 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB246 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB266 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB346 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB366 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB3C6 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x1EB3E6 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x208B85 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 6 / — |
| 0x2094E4 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 29 / — |
| 0x209D0A | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 23 / — |
| 0x209DEB | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 25 / — |
| 0x20A062 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 63 / — |
| 0x2101A0 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 29 / — |
| 0x213720 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 29 / — |
| 0x2197FC | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 29 / — |
| 0x21A05A | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 31 / — |
| 0x21A0E1 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 24 / — |
| 0x21A101 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 25 / — |
| 0x2204B8 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 29 / — |
| 0x223A38 | Graphismes ROM | fragment non vivant : Données de tuiles/polices décodées artificiellement en caractères ; aucun pointeur de texte. Ne pas copier le faux positif FR. | ∅ | aucune exacte | 29 / — |
| 0x237321 | Objet Nugget | nom propre légitime : Nugget est aussi le nom officiel DE (item_names.py) ; référent valide. | `Nugget` | 0x2372d8 | 7 / — |
| 0x23E572 | Table classes Dresseur / faux début | fragment non vivant : Début binaire incluant préfixe avant « Leader », zéro référent ; table structurée voisine à ne pas injecter par extracteur texte. | ∅ | aucune exacte | 11 / — |
| 0x23E57F | Classes de Dresseurs | déjà correct/patché : « Agent » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Agent` | aucune exacte | 6 / — |
| 0x23E5C0 | Classes de Dresseurs | déjà correct/patché : « Idol » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Idol` | aucune exacte | 5 / — |
| 0x23E610 | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E60E : ses quatre premiers octets pointent vers 0x1FAE6F4 (Terror Granbull). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 11 / — |
| 0x23E678 | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E676 : ses quatre premiers octets pointent vers 0x1FA1EE4 (Black Ferrothorn). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 11 / — |
| 0x23E6AC | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E6AA : ses quatre premiers octets pointent vers 0x1FA1EF5 (Black Ferrothorn Boss). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 11 / — |
| 0x23E6B7 | Classes de Dresseurs | déjà correct/patché : « Pokéfan » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Pokéfan` | aucune exacte | 8 / — |
| 0x23E6E1 | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E6DE : ses quatre premiers octets pointent vers 0x1F949EC (Frontier Brain). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 10 / — |
| 0x23E6EC | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E6EB : ses quatre premiers octets pointent vers 0x1FACB8D (Science Society). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 12 / — |
| 0x23E6F8 | Classes de Dresseurs | déjà correct/patché : « Jogger » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Jogger` | aucune exacte | 7 / — |
| 0x23E746 | Classes/factions de Dresseurs | nom propre légitime : Nom propre de faction : cellule fixe de 13 octets (Black Horizon sous forme contrainte / Black Emboar), conservée par trainer_class_names. Aucun contrôle perdu. | ∅ | aucune exacte | 13 / — |
| 0x23E763 | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E760 : ses quatre premiers octets pointent vers 0x1EEA039 (Sinnoh Leader). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 10 / — |
| 0x23E7A1 | Classes/factions de Dresseurs | nom propre légitime : Nom propre de faction : cellule fixe de 13 octets (Black Horizon sous forme contrainte / Black Emboar), conservée par trainer_class_names. Aucun contrôle perdu. | ∅ | aucune exacte | 13 / — |
| 0x23E7AF | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E7AE : ses quatre premiers octets pointent vers 0x1F2CB68 (Light of Ruin Admin). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 9 / — |
| 0x23E7BB | Table des classes de Dresseurs, cellule indirecte | fragment non vivant : Cellule CFRU à 0x23E7BB : ses quatre premiers octets pointent vers 0x1F2CB5A (Light of Ruin). Cet offset est dans le pointeur ou son ancien suffixe, pas le texte vivant ; aucune écriture. | ∅ | aucune exacte | 13 / — |
| 0x23E871 | Classes de Dresseurs | déjà correct/patché : « Camper » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Camper` | aucune exacte | 7 / — |
| 0x23E8B2 | Classes de Dresseurs | déjà correct/patché : « Biker » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Biker` | aucune exacte | 6 / — |
| 0x23E934 | Classes de Dresseurs | déjà correct/patché : « Rocker » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Rocker` | aucune exacte | 7 / — |
| 0x23E98F | Classes de Dresseurs | déjà correct/patché : « Boss » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Boss` | aucune exacte | 5 / — |
| 0x23E9D0 | Classes de Dresseurs | déjà correct/patché : « Gentleman » est un terme allemand valide. Cellule fixe de 13 octets, adressage par index depuis 0x23E558 ; reprise par trainer_class_names, sans dépassement ni commandes. | `Gentleman` | aucune exacte | 10 / — |
| 0x23EAF9 | Données après classes | fragment non vivant : Séquence alphabétique fghijk, hors des 107 cellules de classes, aucun référent. Donnée de test, pas un dialogue. | ∅ | aucune exacte | 7 / — |
| 0x24F3C4 | Description de talent absent | corrigé : Omission DE au vrai début ; 0x24F3C1 est une préimage décalée. La table des talents vivante 0x96DE04 et son entrée 77 référencent ce texte. Traduction courte dans les 20 octets source, aucun contrôle. | `Keine Fähigkeit.` | 0x24fb08, 0x96de04, 0x96df38 | 20 / 17 |
| 0x24FD03 | Ancienne table noms talents | fragment non vivant : Ancienne table de talents ; aucun pointeur sur cette chaîne. Table CFRU active des noms à 0xA36398, maintenue par ability_names. Ne pas traduire cette copie ni ses espaces de bourrage. | `INSOMNIA` | aucune exacte | 9 / — |
| 0x24FDF8 | Ancienne table noms talents | fragment non vivant : Ancienne table de talents ; aucun pointeur sur cette chaîne. Table CFRU active des noms à 0xA36398, maintenue par ability_names. Ne pas traduire cette copie ni ses espaces de bourrage. | `CHLOROPHYLL` | aucune exacte | 14 / — |
| 0x24FF23 | Ancienne table noms talents | fragment non vivant : Ancienne table de talents ; aucun pointeur sur cette chaîne. Table CFRU active des noms à 0xA36398, maintenue par ability_names. Ne pas traduire cette copie ni ses espaces de bourrage. | `PLUS` | aucune exacte | 7 / — |
| 0x24FF2A | Ancienne table noms talents | fragment non vivant : Ancienne table de talents ; aucun pointeur sur cette chaîne. Table CFRU active des noms à 0xA36398, maintenue par ability_names. Ne pas traduire cette copie ni ses espaces de bourrage. | `MINUS` | aucune exacte | 14 / — |
| 0x255689 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 282 / — |
| 0x255A8D | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 282 / — |
| 0x255EF1 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 182 / — |
| 0x2562F1 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 178 / — |
| 0x26CFBB | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 21 / — |
| 0x26CFF3 | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 7 / — |
| 0x26D001 | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 11 / — |
| 0x26D02F | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 6 / — |
| 0x26D06B | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 7 / — |
| 0x26D0A7 | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 8 / — |
| 0x26D0AF | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 18 / — |
| 0x26D0E3 | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 8 / — |
| 0x26D0EB | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 15 / — |
| 0x26D11F | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 8 / — |
| 0x26D15B | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 6 / — |
| 0x26D197 | Structures de noms/surnoms, bloc 0x26CFxx | nom propre légitime : Nom de Dresseur/surnom dans des structures de 60 octets (Quacker, Edmund, The Top, Saige, Alicia, Shroomu, Among Us, Torch, Balogna, NORMA, GARETT). Préfixes binaires/espaces ne sont pas du texte à traduire ; conserver les noms. | ∅ | aucune exacte | 7 / — |
| 0x26D4DF | Dresseur, accès SES Expressway / Challenge Road | déjà correct/patché : Début structuré 00 FC 03 00 00 00 : les deux pointeurs 0x26D3C6/0x26D3E4 atteignent après build « Fangen wir an! » grâce au suffixe déjà traduit 0x26D4E5 hors lot. Contrôle FC0300 intact ; ne pas ajouter une écriture chevauchante. | ∅ | 0x26d3c6, 0x26d3e4 | 24 / — |
| 0x26D524 | Dresseur, accès SES Expressway / Challenge Road | corrigé : Sens conservé mais première ligne DE sans rupture énorme. Rétablir exactement FE, FA, FB, FE dans cet ordre, conserver SES Expressway et tutoiement. Vérifier chaque ligne au build. | `Der SES Expressway ist nun\nnicht mehr versiegelt.\lEndlich konnte ich trainieren!\pWillst du gegen meine frisch\ntrainierten Pokémon kämpfen?` | 0x26d3a8 | 155 / 139 |
| 0x26D6BD | Donateur de trois Pokémon, script 0x26D63x (zone non établie) | corrigé : Dialogue manquant DE, msgbox à 0x26D644. Donateur de trois Pokémon ; tutoiement, deux changements de page et une rupture de ligne préservés. Aucune espèce renommée. | `Hallo, Reisender.\pDrei Pokémon suchen dringend\neinen liebevollen Trainer.\pKümmerst du dich um sie?` | 0x26d644 | 118 / 99 |
| 0x2A49C5 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 6 / — |
| 0x2C486A | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 14 / — |
| 0x2C89B0 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 13 / — |
| 0x2F9AF8 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 33 / — |
| 0x353F9E | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 6 / — |
| 0x354081 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 8 / — |
| 0x369D6A | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 152 / — |
| 0x369E04 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 29 / — |
| 0x38F86F | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x38FBF6 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 18 / — |
| 0x38FDDF | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 19 / — |
| 0x399871 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 8 / — |
| 0x399A71 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 8 / — |
| 0x39BF30 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x39C044 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x39C178 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x39C2AC | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x39C3C0 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x39C4F8 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x3ABDE6 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 24 / — |
| 0x3ABE50 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 15 / — |
| 0x3ABE6E | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 15 / — |
| 0x3ABE86 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 17 / — |
| 0x3ABE9C | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 8 / — |
| 0x3ABEA4 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 17 / — |
| 0x3ABEB9 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 8 / — |
| 0x3ABEC1 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 26 / — |
| 0x3ABEE6 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 20 / — |
| 0x3ABF46 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 17 / — |
| 0x3ABF60 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 21 / — |
| 0x3ABF7E | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 17 / — |
| 0x3ABF9C | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 11 / — |
| 0x3ABFB9 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 12 / — |
| 0x3AC023 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 11 / — |
| 0x3AC05C | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 17 / — |
| 0x3AC07A | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 17 / — |
| 0x3AC094 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 21 / — |
| 0x3AC0B2 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 41 / — |
| 0x3AC0E6 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 20 / — |
| 0x3AC154 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 15 / — |
| 0x3AC172 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 15 / — |
| 0x3AC186 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 5 / — |
| 0x3AC18C | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 16 / — |
| 0x3AC19C | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 13 / — |
| 0x3AC1AA | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 15 / — |
| 0x3CAF09 | Données binaires/graphiques | fragment non vivant : Faux positif d’extraction de données binaires/graphiques ; aucun pointeur vers cet offset, aucune phrase canonique à traduire. | ∅ | aucune exacte | 24 / — |
| 0x3D98DC | Descriptions historiques Lichtschild/Reflektor | fragment non vivant : Copie ancienne de description sans référent ; la table active 0x99F190 pour Lichtschild/Reflektor vise 0x4845C5. Ne pas modifier cette copie morte, même si sa forme DE comporte un habillage perfectible. | `Eine Lichtwand entsteht für fünf\nRunden. Sie verringert Schaden\ndurch Sp.-Angriff-Attacken.` | aucune exacte | 84 / — |
| 0x3D9EAC | Descriptions historiques Lichtschild/Reflektor | fragment non vivant : Copie ancienne de description sans référent ; la table active 0x99F190 pour Lichtschild/Reflektor vise 0x484647. Ne pas modifier cette copie morte, même si sa forme DE comporte un habillage perfectible. | `Eine feste Barriere wird für\nfünf Runden errichtet. Sie\nverringert Schaden durch\nphysische Attacken.` | aucune exacte | 99 / — |
| 0x3DDD0B | Structures anciennes objets | fragment non vivant : Suffixe sans référent dans une structure d’objet ancienne (Dows(e)r/Parcel), pas une chaîne autonome. Aucun ajout DE. | ∅ | aucune exacte | 4 / — |
| 0x3DEC2D | Structures anciennes objets | fragment non vivant : Suffixe sans référent dans une structure d’objet ancienne (Dows(e)r/Parcel), pas une chaîne autonome. Aucun ajout DE. | ∅ | aucune exacte | 4 / — |
| 0x3E1448 | Données binaires avant lexique | fragment non vivant : Données non linguistiques, suite hkiii/ki… sans référent : ne pas reproduire le faux texte présent dans FR. | ∅ | aucune exacte | 6 / — |
| 0x3E144E | Données binaires avant lexique | fragment non vivant : Données non linguistiques, suite hkiii/ki… sans référent : ne pas reproduire le faux texte présent dans FR. | ∅ | aucune exacte | 10 / — |
| 0x3E7F66 | Lexique Easy Chat, Pokémon/communication | déjà correct/patché : Mot du lexique Easy Chat référencé par la table à 0x3E80xx ; terme allemand admis (CENTER, LINK, VERSION) ou nom de fonction POKéNAV. Chaîne courte intacte sans contrôles. | `CENTER` | 0x3e8034 | 7 / — |
| 0x3E7F71 | Lexique Easy Chat, Pokémon/communication | déjà correct/patché : Mot du lexique Easy Chat référencé par la table à 0x3E80xx ; terme allemand admis (CENTER, LINK, VERSION) ou nom de fonction POKéNAV. Chaîne courte intacte sans contrôles. | `LINK` | 0x3e804c | 5 / — |
| 0x3E7F8A | Lexique Easy Chat, Pokémon/communication | déjà correct/patché : Mot du lexique Easy Chat référencé par la table à 0x3E80xx ; terme allemand admis (CENTER, LINK, VERSION) ou nom de fonction POKéNAV. Chaîne courte intacte sans contrôles. | `VERSION` | 0x3e8070 | 8 / — |
| 0x3E7F92 | Lexique Easy Chat, Pokémon/communication | nom propre légitime : Mot du lexique Easy Chat référencé par la table à 0x3E80xx ; terme allemand admis (CENTER, LINK, VERSION) ou nom de fonction POKéNAV. Chaîne courte intacte sans contrôles. | `POKéNAV` | 0x3e807c | 8 / — |
| 0x3E7F9A | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : Pokémon : nom de franchise officiel commun, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `Pokémon` | 0x3e8088 | 8 / — |
| 0x3E7FA6 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : Pokédex : nom d’appareil officiel commun, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `Pokédex` | 0x3e80a0 | 8 / — |
| 0x3E7FB3 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : LEVEL : emprunt usuel allemand désignant le niveau, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `LEVEL` | 0x3e80b8 | 6 / — |
| 0x3E7FCD | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : GOLD : nom allemand de l’or/version, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `GOLD` | 0x3e80f4 | 5 / — |
| 0x3E8187 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | corrigé : AIR LOCK est le talent Klimaschutz (table officielle DE 0xA37498), pas un nom propre EN ; le mot Easy Chat a un pointeur indépendant. | `KLIMASCHUTZ` | 0x3e85a0 | 9 / 12 |
| 0x3E8198 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | corrigé : HYPER CUTTER est le talent Scherenmacht (valeur gagnante DE 0xA3670C) ; oubli anglais dans la liste Easy Chat. | `SCHERENMACHT` | 0x3e85b8 | 13 / 13 |
| 0x3E81D5 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : COOL : adjectif allemand et catégorie Concours, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `COOL` | 0x3e8600 | 5 / — |
| 0x3E838F | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : NORMAL : type officiel Normal, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `NORMAL` | 0x3e8840 | 7 / — |
| 0x3E8402 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : INSOMNIA : talent officiel Insomnia, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `INSOMNIA` | 0x3e88d0 | 9 / — |
| 0x3E8414 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : PLUS : talent officiel Plus, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `PLUS` | 0x3e88e8 | 5 / — |
| 0x3E8467 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : MINUS : talent officiel Minus, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `MINUS` | 0x3e8954 | 6 / — |
| 0x3E84DF | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : CHLOROPHYLL : talent officiel Chlorophyll, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `CHLOROPHYLL` | 0x3e89fc | 12 / — |
| 0x3E8AC3 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : TALENT : nom commun allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `TALENT` | 0x3e8cf0 | 7 / — |
| 0x3E8AD9 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : MATCH : emprunt sportif allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `MATCH` | 0x3e8d14 | 6 / — |
| 0x3E8AE7 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : OFFENSIVE : nom allemand de l’offensive, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `OFFENSIVE` | 0x3e8d2c | 10 / — |
| 0x3E8B9B | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : PARTNER : nom allemand du partenaire, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `PARTNER` | 0x3e8e58 | 8 / — |
| 0x3E8BE1 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | corrigé : LEADER est un rôle, pas un nom propre ; Anführer rend le mot dans la catégorie Combat, sans toucher au nom des champions. | `ANFÜHRER` | 0x3e8ec4 | 7 / 9 |
| 0x3E9369 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : PERSON : nom allemand de la personne, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `PERSON` | 0x3e966c | 7 / — |
| 0x3E97F4 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : EHEHE : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `EHEHE` | 0x3e9a10 | 6 / — |
| 0x3E9822 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : GRAAAH : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `GRAAAH` | 0x3e9a64 | 7 / — |
| 0x3E983B | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HEHE : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `HEHE` | 0x3e9a94 | 5 / — |
| 0x3E9848 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HAHAHA : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `HAHAHA` | 0x3e9ab8 | 7 / — |
| 0x3E9856 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HIYAH : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `HIYAH` | 0x3e9ad0 | 6 / — |
| 0x3E985C | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : FUFUFU : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `FUFUFU` | 0x3e9adc | 7 / — |
| 0x3E9873 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HEHEHE : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `HEHEHE` | 0x3e9b0c | 7 / — |
| 0x3E987E | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HOHOHO : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `HOHOHO` | 0x3e9b24 | 7 / — |
| 0x3E989B | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : MUFUFU : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `MUFUFU` | 0x3e9b54 | 7 / — |
| 0x3E98B2 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : LALALA : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `LALALA` | 0x3e9b84 | 7 / — |
| 0x3E98C7 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : GWAH : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `GWAH` | 0x3e9bb4 | 5 / — |
| 0x3E98CC | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : WAHAHAHA : rire/cri/chant de la catégorie Voix, onomatopée volontaire identique en FR ; pas de prose anglaise résiduelle. | `WAHAHAHA` | 0x3e9bc0 | 9 / — |
| 0x3E9C7C | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : WILD : adjectif allemand sauvage, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `WILD` | 0x3e9ebc | 5 / — |
| 0x3EB849 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : ANIME : emprunt allemand consacré, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `ANIME` | 0x3eb9cc | 6 / — |
| 0x3EB861 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : CHAT : emprunt informatique allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `CHAT` | 0x3eb9fc | 5 / — |
| 0x3EB884 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : SHOPPING : emprunt allemand consacré, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `SHOPPING` | 0x3eba38 | 9 / — |
| 0x3EB8A6 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : GOURMET : nom allemand du gourmet, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `GOURMET` | 0x3eba68 | 8 / — |
| 0x3EB8DE | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HOBBY : nom allemand du loisir, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `HOBBY` | 0x3ebac8 | 6 / — |
| 0x3EB8EB | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : SOFTWARE : nom allemand du logiciel, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `SOFTWARE` | 0x3ebae0 | 9 / — |
| 0x3EB931 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : DESIGN : nom allemand du design, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `DESIGN` | 0x3ebb58 | 7 / — |
| 0x3EB982 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : BALL : nom allemand du ballon, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `BALL` | 0x3ebbdc | 5 / — |
| 0x3EB98C | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : FESTIVAL : nom allemand du festival, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `FESTIVAL` | 0x3ebbf4 | 9 / — |
| 0x3EB9BA | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : LOOK : emprunt allemand pour l’apparence, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `LOOK` | 0x3ebc3c | 5 / — |
| 0x3EBD3B | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : WINTER : nom allemand de l’hiver, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `WINTER` | 0x3ebf2c | 7 / — |
| 0x3EC59E | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : SUPER : intensif allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `SUPER` | 0x3ec698 | 6 / — |
| 0x3EC5C1 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : HYPER : préfixe allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `HYPER` | 0x3ec6c8 | 6 / — |
| 0x3EC5C7 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | nom propre légitime : BATTLE TOWER : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `BATTLE TOWER` | 0x3ec6d4 | 13 / — |
| 0x3EC62D | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : UNION : nom allemand de l’union, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `UNION` | 0x3ec770 | 6 / — |
| 0x3ECA95 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : MEGA : préfixe allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `MEGA` | 0x3ecb98 | 5 / — |
| 0x3ECAF9 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : MODERN : adjectif allemand, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `MODERN` | 0x3ecc40 | 7 / — |
| 0x3ECB09 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : BANG : onomatopée de bruit, conservée comme FR, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `BANG` | 0x3ecc58 | 5 / — |
| 0x3ECB33 | Easy Chat / mots des catégories Pokémon, statut, combat, voix, loisirs et lieux | déjà correct : BABY : nom allemand du bébé, identique à EN sans être un oubli ; aucun contrôle ni buffer dans ce mot isolé. | `BABY` | 0x3ecca0 | 5 / — |
| 0x3EED08 | Carte / noms des zones et bâtiments | nom propre légitime : Bellin Town : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Bellin Town` | 0x3f1cb0 | 12 / — |
| 0x3EED22 | Carte / noms des zones et bâtiments | nom propre légitime : Crater Town : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Crater Town` | 0x3f1cb8 | 12 / — |
| 0x3EED67 | Carte / noms des zones et bâtiments | nom propre légitime : Tarmigan Town : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Tarmigan Town` | 0x3f1ccc | 14 / — |
| 0x3EED77 | Carte / noms des zones et bâtiments | nom propre légitime : INDIGO PLATEAU : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `INDIGO PLATEAU` | 0x3f1cd0 | 15 / — |
| 0x3EED93 | Carte / noms des zones et bâtiments | nom propre légitime : Route 4 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 4` | 0x3f1cd8 | 8 / — |
| 0x3EED9B | Carte / noms des zones et bâtiments | nom propre légitime : Route 10 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 10` | 0x3f1cdc | 9 / — |
| 0x3EEDA4 | Carte / noms des zones et bâtiments | nom propre légitime : Route 1 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 1` | 0x3f1ce0 | 8 / — |
| 0x3EEDAC | Carte / noms des zones et bâtiments | nom propre légitime : Route 2 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 2` | 0x3f1ce4 | 8 / — |
| 0x3EEDB4 | Carte / noms des zones et bâtiments | nom propre légitime : Route 3 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 3` | 0x3f1ce8 | 8 / — |
| 0x3EEDC4 | Carte / noms des zones et bâtiments | nom propre légitime : Route 5 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 5` | 0x3f1cf0 | 8 / — |
| 0x3EEDCC | Carte / noms des zones et bâtiments | nom propre légitime : Route 6 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 6` | 0x3f1cf4 | 8 / — |
| 0x3EEDD4 | Carte / noms des zones et bâtiments | nom propre légitime : Route 7 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 7` | 0x3f1cf8 | 8 / — |
| 0x3EEDDC | Carte / noms des zones et bâtiments | nom propre légitime : Route 8 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 8` | 0x3f1cfc | 8 / — |
| 0x3EEDE4 | Carte / noms des zones et bâtiments | nom propre légitime : Route 9 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 9` | 0x3f1d00 | 8 / — |
| 0x3EEDEC | Carte / noms des zones et bâtiments | nom propre légitime : ROUTE 10 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `ROUTE 10` | 0x3f1d04 | 9 / — |
| 0x3EEDF5 | Carte / noms des zones et bâtiments | nom propre légitime : Route 11 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 11` | 0x3f1d08 | 9 / — |
| 0x3EEDFE | Carte / noms des zones et bâtiments | nom propre légitime : Route 12 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 12` | 0x3f1d0c | 9 / — |
| 0x3EEE07 | Carte / noms des zones et bâtiments | nom propre légitime : Route 13 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 13` | 0x3f1d10 | 9 / — |
| 0x3EEE10 | Carte / noms des zones et bâtiments | nom propre légitime : Route 14 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 14` | 0x3f1d14 | 9 / — |
| 0x3EEE19 | Carte / noms des zones et bâtiments | nom propre légitime : Route 15 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 15` | 0x3f1d18 | 9 / — |
| 0x3EEE22 | Carte / noms des zones et bâtiments | nom propre légitime : Route 16 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 16` | 0x3f1d1c | 9 / — |
| 0x3EEE2B | Carte / noms des zones et bâtiments | nom propre légitime : Route 17 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 17` | 0x3f1d20 | 9 / — |
| 0x3EEE34 | Carte / noms des zones et bâtiments | nom propre légitime : Route 18 : désignation de route identique en allemand, nombre conservé ; référent dans la table des sections carte. | `Route 18` | 0x3f1d24 | 9 / — |
| 0x3EEE7C | Carte / noms des zones et bâtiments | nom propre légitime : Grim Woods : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Grim Woods` | 0x3f1b40, 0x3f1d44 | 11 / — |
| 0x3EEE9F | Carte / noms des zones et bâtiments | nom propre légitime : Underground Pass : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Underground Pass` | 0x3f1d50 | 17 / — |
| 0x3EEEC1 | Carte / noms des zones et bâtiments | nom propre légitime : Valley Cave : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Valley Cave` | 0x3f1b58, 0x3f1d58 | 12 / — |
| 0x3EEED0 | Carte / noms des zones et bâtiments | nom propre légitime : Victory Road : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Victory Road` | 0x3f1b64, 0x3f1d5c | 13 / — |
| 0x3EEF12 | Carte / noms des zones et bâtiments | nom propre légitime : Pokémon League : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Pokémon League` | 0x3f1d70 | 15 / — |
| 0x3EEF2D | Carte / noms des zones et bâtiments | nom propre légitime : Rift Cave : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Rift Cave` | 0x3f1b94, 0x3f1d78 | 10 / — |
| 0x3EEF3D | Carte / noms des zones et bâtiments | nom propre légitime : Vivill Woods : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Vivill Woods` | 0x3f1ba0, 0x3f1d7c | 13 / — |
| 0x3EEF4B | Carte / noms des zones et bâtiments | nom propre légitime : Icicle Cave : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Icicle Cave` | 0x3f1bac, 0x3f1d80 | 12 / — |
| 0x3EEF94 | Carte / noms des zones et bâtiments | nom propre légitime : Cube Corp. : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Cube Corp.` | 0x3f1d98 | 11 / — |
| 0x3EEFEA | Carte / noms des zones et bâtiments | nom propre légitime : Cave of Being : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Cave of Being` | 0x3f1db4 | 14 / — |
| 0x3EF133 | Carte / noms des zones et bâtiments | nom propre légitime : Battle Mine : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Battle Mine` | 0x3f1e14 | 12 / — |
| 0x3EF144 | Carte / noms des zones et bâtiments | nom propre légitime : Battle Tower : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Battle Tower` | 0x3f1e18 | 13 / — |
| 0x3EF183 | Carte / noms des zones et bâtiments | nom propre légitime : Autl Woods : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Autl Woods` | 0x3f1bf4, 0x3f1e2c | 11 / — |
| 0x3EF193 | Carte / noms des zones et bâtiments | nom propre légitime : Cliff Cave : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Cliff Cave` | 0x3f1e30 | 11 / — |
| 0x3EF22E | Carte / noms des zones et bâtiments | nom propre légitime : Dehara Dept. : toponyme EN volontaire de la politique DE (english_toponyms.yaml), graphie canonique conservée ; FR localise les lieux mais ce choix ne se transpose pas en DE. | `Dehara Dept.` | 0xc4da0, 0x3f1e5c | 13 / — |
| 0x3FB284 | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'a boosted', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 10 / — |
| 0x3FB9D6 | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'l!', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 3 / — |
| 0x3FBA2C | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'd!', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 3 / — |
| 0x3FC5E8 | Combat / gBattleStringsTable, objet et bénéficiaire | corrigé : Préfixe du message de combat objet/bénéficiaire non traduit ; garder FD13, FE, FD16, FD00 dans cet ordre. Für remplace For à budget identique (14 octets avec terminateur). Table vivante 0x3FDF3C (référents code dont 0xCEFEC et 0x883580), entrée 0x3FE41C. | `Für <0xFD><0x13>,\n<0xFD><0x16> <0xFD><0x00>` | 0x3fe41c | 14 / 14 |
| 0x3FC873 | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'ith ?ç!', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 8 / — |
| 0x3FC92C | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée ' little!', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 9 / — |
| 0x3FCA27 | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'ack!', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 5 / — |
| 0x3FCB4B | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'ose!', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. Intérieur de rose! à 0x3FCB4A, cas de chevauchement documenté dans la mémoire phantom-tail-overlap ; ne pas réintroduire. | ∅ | aucune exacte | 5 / — |
| 0x3FD361 | Combat / fragments et buffers historiques | fragment non vivant : Extraction tronquée 'k!?\n', aucun référent absolu dans la ROM EN ; aucune traduction DE à ajouter sur ce suffixe. | ∅ | aucune exacte | 5 / — |
| 0x3FD586 | Combat / fragments et buffers historiques | déjà correct : Buffer de ponctuation ! appelé par le moteur (référent 0xd8784) ; absence DE légitime, aucun mot à traduire ni commande perdue. | ∅ | 0xd8784 | 2 / — |
| 0x3FD588 | Combat / fragments et buffers historiques | déjà correct : Buffer de ponctuation ! appelé par le moteur (référent 0xd878c) ; absence DE légitime, aucun mot à traduire ni commande perdue. | ∅ | 0xd878c | 2 / — |
| 0x3FD58A | Combat / fragments et buffers historiques | déjà correct : Buffer de ponctuation ! appelé par le moteur (référent 0xd8794) ; absence DE légitime, aucun mot à traduire ni commande perdue. | ∅ | 0xd8794 | 2 / — |
