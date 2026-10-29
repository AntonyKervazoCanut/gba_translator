# 22 — Glossaire brésilien figé (F-759)

Le contrat des lots PT-01 à PT-88 est
`languages/pt/data/official_terminology.yaml`, figé le 29 octobre 2026.
Il distingue les attestations officielles brésiliennes, les choix éditoriaux
et les noms anglais conservés. Il ne constitue pas une liste exhaustive de
traductions officielles : une entrée absente conserve son nom anglais exact.
Chaque exception comporte une preuve de décision, les références consultées
avec leur date et les variantes rejetées lorsqu’elles sont pertinentes.

## Recherche et politique

- Les fiches bilingues officielles de [Ventos e Ondas](https://windswaves.pokemon.com/pt-br/)
  attestent les trois talents des partenaires initiaux. La jointure avec la
  [version anglaise](https://windswaves.pokemon.com/en-us/) porte sur le même Pokémon
  et le même champ, sans déduire une traduction depuis un effet ressemblant.
- Les [règles des coupes GO](https://pokemongo.com/pt-BR/news/go-battle-league-twilight-trails)
  attestent treize types de jeu. Cinq autres restent des choix de projet déclarés.
  Les dix-huit valeurs sont figées ; aucune prétention d’officialité pour un choix non attesté.
- La [Pokédex de Blitzle](https://www.pokemon.com/br/pokedex/blitzle), dans le contenu
  officiel indexé consulté, atteste PS et les cinq autres statistiques principales.
  Certains champs du portail restent anglais ; une page en portugais ne prouve
  donc pas que tous ses noms ont été localisés.
- La [carte Poção](https://www.pokemon.com/br/pokemon-estampas-ilustradas/cartas-de-pokemon/series/sm1/127/)
  atteste ce nom d’objet de soin. Son adoption nominale pour Potion est explicite ;
  les effets et quantités de soin CFRU restent ceux du jeu.
- Le [manuel TCG brésilien](https://assets.pokemon.com/assets/cms2-pt-br/pdf/trading-card-game/rulebook/swsh6_rulebook_br.pdf)
  atteste plusieurs états complets et Nocauteado. Ses types d’Énergie et ses mécaniques
  ne se substituent pas aux types et effets CFRU.
- Les autres capacités, talents, objets et les 25 natures restent anglais en
  l’absence d’une exception sourcée. Aucun synonyme de fans ou du doublage ne devient
  officiel par défaut. Les noms propres originaux de Borrius restent anglais,
  lieux complets et noms de factions compris ; les mots communs hors du nom se traduisent.
- Une source PT-PT n’établit jamais un terme PT-BR. Pour les sources `/pt/` ambiguës,
  contrôler la région et le contexte. Les sources retenues identifient Brasil,
  `pt-BR` ou `pt_BR` ; les variantes communautaires restent séparées.
- Les termes longs ne sont pas tronqués automatiquement. Une limite de cellule
  ou de pixels exige une exception de rendu documentée par offset et testée dans
  le lot propriétaire. Aucun ajout aux fichiers `combined` dans ce ticket.

## Abréviations et contrôle du rendu

Les codes PSN/QMD/CNG/PAR/DRM sont conservés comme **conventions du projet** :
les sources primaires consultées n’attestent pas ces cinq abréviations comme
codes officiels brésiliens. Congelado est également identifié comme choix
éditorial. Le nom complet attesté Adormecido n’implique pas que DRM soit officiel.

La table de texte `0x3DFE18`, stride 8, contient cinq pointeurs vivants.
Contrôle réalisé sur la vraie ROM EN, SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`,
avec application du patch uniquement sur une copie en mémoire :

| État | Adresse EN résolue | Avant | Après |
|---|---|---|---|
| Sommeil | 0x417914 | SLP | DRM |
| Poison | 0x41790C | PSN | PSN |
| Paralysie | 0x417910 | PAR | PAR |
| Brûlure | 0x417918 | BRN | QMD |
| Gel | 0x41791C | FRZ | CNG |

Trois écritures, neuf octets modifiés ; les terminateurs et pointeurs restent
intacts. Les tests permanents vérifient aussi des pointeurs relogés,
l’idempotence, les octets hors cible et l’absence d’écriture du KO.

Les six codes font exactement trois caractères et trois octets CFRU.
Les cinq extraits de polices réelles versionnés sous
`tests/unit/fixtures/pt_fonts/` possèdent les glyphes nécessaires : encre présente,
largeur totale de 15 pixels (police 0) ou 18 pixels (autres polices), comme les
codes anglais de trois lettres. Ces mesures vérifient le budget des glyphes,
pas une capture de l’écran du jeu.

**KO :** DES reste provisoire dans le registre, ignoré par le patch actuel.
Il ne faut pas annoncer un KO rendu en DES. En prose, Nocauteado est attesté par
le TCG. Les badges graphiques de combat constituent une autre couche : aucun
patch `status_badges` PT n’est déclaré, leurs images restent anglaises.

## Validation et limites

Commande du contrat :
`python3 -m pytest tests/unit/pt tests/test_language_registry.py -q`.
Le test du glossaire vérifie schéma, références, dates, catégories, vocabulaires
fermés, décisions, codes, patch par pointeurs vivants et budgets des polices.
Les tests fonctionnent sans réseau et sans ROM privée.

Les relations structurées consultées dans le contexte F-759 contiennent déjà
F-758 et F-759 pour les 88 lots ; aucune création supplémentaire n’est nécessaire.
L’infrastructure des tildes reste du ressort de F-758, et la certification globale
de T-848. Aucune modification de code partagé ni d’artefact ROM dans ce ticket.

### Non vérifié

Pas de capture en émulateur de l’écran de résumé ou du combat PT : la ROM PT
construite n’est pas disponible dans les artefacts locaux consultés. La vérification
ci-dessus couvre les vrais pointeurs EN et les glyphes bruts, sans revendiquer
une preuve visuelle en jeu. Les lots qui modifient le rendu doivent fournir leur
preuve Playwright hors écran ; T-848 doit contrôler texte, badges et KO ensemble.
