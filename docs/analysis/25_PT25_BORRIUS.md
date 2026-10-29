# PT-25 — Zones Borrius (F-784)

## Périmètre et décisions

Les 288 offsets sont exactement ceux de `languages/pt/translation_batches.json`,
lot PT-25. Les prérequis F-758 (tildes, c5b5e0b9) et F-759 (glossaire,
dcc6ce5d) sont ancêtres du travail. Les noms propres restent anglais selon
F-759 ; aucun offset des autres lots n'est traduit ici.

L'anglais confirme les domaines : Electivire et le nerd, rival/Pokédex,
Sandslash voleur de nourriture, police et Terror Granbull (Route 10),
Ivory/Harth/Marlon, Epidimy Town, Fallshore Gym/Mel, Antisis Port,
Skiers Club, Tarmigan Mansion/Successor Maxima, Articuno, ailes,
fillette emportée par le vent et tunnel Dig.

## Bilan exhaustif

`languages/pt/data/pt25_audit.json` fournit, dans l'ordre du manifeste,
les 288 fiches : anglais, comparaison FR au même offset, préimage binaire,
pointeurs et contexte de chaque référence, statut, justification,
traduction exacte, longueur encodée et largeurs avec marge pour les tampons.

- 272 consommateurs texte référencés : traductions/protections ajoutées.
  Les cris et noms propres peuvent rester identiques à l'anglais.
- 16 exceptions : aucune référence absolue dans la ROM source entière.
  Le bilan indique leurs copies identiques référencées et leurs éventuels
  conteneurs ; elles ne sont ni ajoutées au combined ni revendiquées injectées.
- `0x7c182c` : fragment « resident of the Skiers Club » référencé directement ;
  le contexte `0x7c1821` permet de restaurer un message autonome de présidente.
- `0x7c4d1a` : fragment « elp benefit humanity » directement référencé ;
  restauration de la conclusion autonome sans écrire le début hors lot.

## Injection et contrôles

La passe PT dédiée `batch_25` réutilise `BorriusTextPatch` et
`StructuredTextPatch` existants. Elle intervient après les réparations et
repointages génériques, avant la passe PT-20 dont les références sont disjointes.
Elle valide les préimages, les commandes FC/FD et les pages FA/FB dans leur
ordre original ; seuls les retours souples sont adaptés à la largeur.
Les textes sont relocalisés atomiquement et tous les consommateurs sont
repointés, sans écriture dans les cellules partagées ou les voisins hors lot.
Les tampons `his`, `sir`, `madam` et le nom Distortion World sont donc couverts
au même titre que les msgbox ; aucune table fixe ignorée n'est déclarée traduite.

Les tests unitaires couvrent le manifeste, les protections, pages, tampons,
récompenses, noms et mécanismes (niveau 70, Hidden Power 70, Dig, quatre jours).
Les tests ROM vérifient toutes les références source et leurs cibles finales,
les octets exacts et terminateurs, l'absence de chevauchement, les limites des
écritures, l'atomicité, l'idempotence et les budgets des cinq polices réelles.

## Preuve de rendu et limites

`playwright.pt25.config.ts` lance exclusivement hors écran une sonde mGBA.
Deux msgbox utilisent les pointeurs de la ROM finale, sans substituer leur texte
ni modifier les glyphes. Playwright vérifie les octets, puis le texte rendu par
OCR avant de capturer la preuve dans le répertoire temporaire du système.
Il ne s'agit pas d'une navigation complète dans les 272 dialogues : les autres
pages sont vérifiées en binaire et en budgets de police.

Les résultats effectifs des commandes et la capture jointe figurent dans le
bilan du ticket. Aucun patch BPS distribué n'est actualisé dans ce lot ; la
certification de la totalité du parcours et de la release relève de T-848.
