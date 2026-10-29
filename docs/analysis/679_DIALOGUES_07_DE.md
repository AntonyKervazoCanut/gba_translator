# B-679 — Dialogues-07

Les 300 offsets exclusifs du ticket ont été relus, sans audit global. Le relevé
`679_DIALOGUES_07_DE.json` conserve EN/FR, la dernière valeur DE avant/après,
le canon EN décodé par commandes atomiques, les octets et les références.

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
  dialogue démontré. Aucune modification.
- `0x1F1F9DC` : besoin séparé. Le script `0x1E76D8A` reçoit un buffer is/was de
  `0x1F204FA`/`0x1F204FD`, hors lot et déjà couverts par B-687. Il faut corriger ces deux buffers, restaurer
  FD02, remplacer Sandan par Sandslash et conserver les huit pages. Le présent
  ticket ne modifie ni les offsets externes ni le script appelant.

## Validation locale

À renseigner après le build et les tests : contrôles des pointeurs et octets
réellement injectés, `make build-de`, `make test-python`, tests ciblés et preuve
Playwright headless via l'imprimante native de mGBA.

## Non vérifié

Le parcours manuel de toutes les scènes n'est pas couvert. Les adresses sans
référence directe et la coïncidence binaire F46 ne sont pas présentées comme une
preuve universelle d'inaccessibilité. Le besoin de patch séparé reste explicite.
