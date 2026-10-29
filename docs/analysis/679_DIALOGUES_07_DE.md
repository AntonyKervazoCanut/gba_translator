# B-679 — Dialogues-07

Les 300 offsets exclusifs du ticket ont été relus, sans audit global. Le relevé
`679_DIALOGUES_07_DE.json` conserve EN/FR, la dernière valeur DE avant/après,
le canon EN décodé par commandes atomiques, les octets et les références.

Bilan : 128 corrections, 103 noms/termes légitimes, 58 crédits légitimes,
7 valeurs déjà correctes, 2 déjà patchées, 1 fragment non vivant et 1 besoin
séparé. Les 300 décisions figurent individuellement dans le relevé.

128 corrections, plus une protection de texte déjà correct : sens, terminologie, oublis, commandes, mise en page. Les
attaques sont confrontées à `move_names_de_official.json` et les objets à
`official_terminology.yaml` et à la table DE existante. Exemples : Eishieb,
Prachtfedern, Raub, Bezirzer, Abschlag, Beulenhelm, Einäschern, Glücks-Eier,
Maronbeeren, Rosenrauch, Top-Genesung et Kraftreserve. Le récit de Benjamin
conserve Butterfree/Caterpie ; les évolutions conservent Ducklett, Cutiefly et
Blastoise. Les lieux restent anglais. `0x7A823B` est hors lot.

Sources complémentaires : [formes de Vivillon](https://community.bisafans.de/forum/index.php?pageNo=1&thread%2F238781-vivillon-informationstopic-weltkarte-mit-verbreitungsgebieten%2F=),
[Trainer Catalogue](https://unboundwiki.com/items/key-items/trainer-catalogue/),
[Stat Scanner](https://unboundwiki.com/items/key-items/stat-scanner/).
Les noms propres et les crédits sont conservés, y compris leurs intitulés de
fonctions : ce choix est explicite, pas une couverture traduite revendiquée.
Aucune fiche Pokédex d'espèce dans ce lot.

Le ton familier des habitants et du rival, le bégaiement de la mère, les
hésitations du chercheur, le ton de Big Mo et le vouvoiement du personnel du
magasin sont conservés. Le texte du professeur rétablit FD03 avec « Als
Sohn/Tochter deines Vaters », compatible avec les deux genres. Le dialogue de
Jirachi emploie également une construction sans déterminant genré devant le
buffer. La fille enlevée reste Tochter ; son ravisseur reste un Pokémon.

Les pages FB sont strictement conservées en nombre et ordre pour les textes
corrigés. FE/FA sont réorganisés pour les boîtes à deux lignes, avec une cible
prudente de 180 pixels (plafond 192). Les commandes FC/FD/F8 sont explicites,
préservent leurs paramètres et leur ordre. Les pauses FC08 18/20/30 ne deviennent
pas des lettres accentuées. Les commandes d'alignement et de police des boissons
restent identiques. La lettre plein écran `0x1F0C2CC` n'est pas reformatée.

Les éditions ne concernent que les dernières occurrences ou les ajouts absents,
avec protection exacte dans le même commit. Aucun patch, source FR/IT, hash de
référence FR ou ressource de jeu n'est modifié. Le manifeste de parité ne reçoit
que la déclaration du test de lot.

## Exclusions motivées

- Générique : 58 entrées conservées, noms et intitulés VO légitimes.
- Noms de zones/personnages, cris, incantations et termes comme Items/TMs :
  décisions individuelles dans le relevé. Les préfixes sans référence directe
  (Crystal Peak, Grim Woods, Gurun Town, KBT Expressway, Magnolia Town) ne sont
  pas de nouvelles traductions à injecter. L'absence de référence directe ne
  prouve pas à elle seule une inaccessibilité absolue par calcul d'adresse.
- `0x1F11DAC` et `0x1F11DB8` : déjà pris en charge par le patch de date allemand.
- `0x1EFECF6` : faux début F46 ; coïncidence binaire de pointeur, pas appel de
  dialogue démontré. Le vrai nom commence à `0x1EFECF8`, référencé par
  `0x1FB2E40` et `0x1FB3EAC`. Aucune modification.
- `0x1F1F9DC` : besoin séparé. Le script `0x1E76D8A` reçoit un buffer is/was de
  `0x1F204FA`/`0x1F204FD`, hors lot et déjà couverts par B-687. Il faut corriger ces deux buffers, restaurer
  FD02, remplacer Sandan par Sandslash et conserver les huit pages. Le présent
  ticket ne modifie ni les offsets externes ni le script appelant.

## Validation locale

- `make build-de` : réussi dans les hooks, après chaque série de corrections.
  Les hooks ont aussi validé les builds FR/IT, 3 428 tests Python (1 ignoré)
  et 68 tests JavaScript. Aucun hook désactivé.
- Tests de lot : 301 contrôles des sources et commandes, puis 300 tests ROM
  réussis. Les 1 475 références retenues ont été relues dans la ROM construite,
  dont 161 références vers les 128 textes corrigés. Zéro différence de texte
  après neutralisation des seuls retours de ligne, zéro différence de commande.
- Largeur maximale réelle : 192 pixels ; chaînes corrigées de 5 à 833 octets,
  terminateur compris. Les chaînes relogées sont lues jusqu'au terminateur en
  décodant les paramètres des commandes ; aucun texte tronqué aux anciens budgets.
- Le premier contrôle binaire avait trouvé 16 débordements : le wrapper ignore
  la largeur des ellipses brutes et des icônes F8. Les seules valeurs concernées
  ont été reformulées ; huit emploient trois points encodés plutôt que B0.
  Le test vérifie désormais aussi la largeur après rewrap et encodage, avec une
  réserve de 12 pixels par icône et 60 pixels par buffer. Aucun patch global.
- Playwright headless : 1 test réussi (4 captures natives mGBA), avec assertions
  OCR sur Eishieb, Beulenhelm, Glücks-Eier et Maronbeeren, et rejet des anciens
  noms erronés. Les scripts de déclenchement ne modifient qu'une copie temporaire
  de la ROM ; les textes proviennent des pointeurs réellement injectés.
  Capture conservée hors dépôt et jointe au ticket :
  `2517b76c-9500-4f06-96f3-90c714031eba`.
- SHA-256 inchangés pour la ROM EN canonique, la ROM source FR, les corpus FR/IT
  et `docs/roms_baseline.json`. Aucun texte hors des 300 offsets n'a été modifié.
- `make test-python` : 3 569 réussis, 3 ignorés, 1 943 désélectionnés (170,92 s).

## Non vérifié

Le parcours manuel de toutes les scènes n'est pas couvert. Les adresses sans
référence directe et la coïncidence binaire F46 ne sont pas présentées comme une
preuve universelle d'inaccessibilité. Le besoin de patch séparé reste explicite.
