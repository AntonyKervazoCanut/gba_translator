# B-1026 — Raccordement des 122 noms fixes DE d’objets-01

Périmètre : les 122 offsets du ticket enfant, sans audit global. Le rapport du
parent B-683 reste distinct. Les 122 décisions individuelles, noms officiels,
préimages, descriptions spécifiques et budgets figurent dans
`1026_OBJETS_01_DE.json`.

## Raccordement

La ROM EN canonique est vérifiée par SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
La routine à `0x9A8CA` lit la base `0x08876200` au site `0x9A8D8` et utilise
un stride de 44 octets. Chaque nom inline possède 14 octets, terminateur inclus.
La pseudo-base historique `0x876074` précède la vraie table de neuf strides.

Les noms proviennent exclusivement de `languages/de/combined_de.txt`, last-wins.
Les 122 lignes étaient absentes : elles sont ajoutées sans modifier l’existant,
avec les 122 valeurs exactes dans `protected_entries.yaml`. Le manifeste
`item_names_objets_01.json` ne contient que le périmètre et les préimages EN.

Les deux passages générique et inline excluent ces offsets en DE. Ils ne
réutilisent donc ni les préimages françaises périmées de l’extraction ni ses
références brutes, notamment `0x9AF055`. Le patch dédié valide toutes les
préimages, la base vivante, les bornes, les noms et leurs budgets avant toute
écriture. Il refuse un état cible inattendu et reste idempotent. Aucune
relocation, aucun pointeur ni métadonnée de struct n’est écrit.

Le patch historique commençant à `0x878504` est supprimé : il ne peut plus
rétablir « Harter Stein » à `0x878510`, désormais alimenté par « Granitstein ».
La copie historique hors lot à `0x3DD32C` reste inchangée ; elle n’est pas la
cellule inline lue pour cet objet dans la table canonique.

## Terminologie et budgets

Référence : [PokeAPI item_names.csv, révision c0a9bc75](https://raw.githubusercontent.com/PokeAPI/pokeapi/c0a9bc75af3a455cdfa27dde21e4ec95aedd3f25/data/v2/csv/item_names.csv),
langues 9 et 6, SHA256
`0341c5acf63b8b1ded13af81f3daadfc33d4ce03d77365fab665f01c98044ff2`.
Confrontation au glossaire DE du dépôt. Alias EN traités : Parlyz Heal,
EnergyPowder, Weak Policy et SS. Ticket.

113 objets ont une correspondance PokeAPI ; neuf objets Unbound sont traduits
d’après leurs descriptions EN vivantes, sans prétendre à une désignation officielle.
Meersalz, Seemuschel, Dyna-Pulver, Traumnebel, Tauschstein, Werte-Scanner,
Barrierenpass et Codekarte: 2/3 désignent respectivement le sel, le coquillage,
la poudre modifiant le facteur Gigamax, le talent caché, l’évolution, les
statistiques cachées et les accès de la base des Shadows.

Abréviations version 1, conservées dans la source et les protections :

| Nom EN | Nom officiel DE | Forme injectée |
|---|---|---|
| Black Flute | Schwarze Flöte | Schwarz.Flöte |
| X Defense | X-Verteidigung | X-Abwehr |
| Weak Policy | Schwächenschutz | Schwächensch. |
| Red Orb | Roter Edelstein | Roter Edlst. |
| Blue Orb | Blauer Edelstein | Blauer Edlst. |
| Storage Key | Lagerschlüssel | Lager-Schl. |

X-Abwehr correspond aussi au nom allemand des générations antérieures.
Les six formes longues ne sont jamais tronquées à l’encodage. Les noms retenus
occupent au maximum 14 octets, terminateur compris, et 75 pixels de police
normale, sous la limite conservatrice de 78 pixels retenue pour le sac.
Le message `WWWWWWW hat <nom> in der` culmine à 184 pixels sur 192, avec le
maximum moteur de sept caractères pour le joueur. Aucun nom du lot ne contient
de contrôle ni de placeholder ; les umlauts utilisent leurs glyphes DE réels.

## Vérifications

Les fixtures binaires sont extraites de la table canonique. Les tests couvrent
l’échec atomique, les préimages, les cibles inattendues, le pointeur de base,
les dépassements, les noms manquants, les contrôles, l’idempotence et les deux
exclusions. Les tests ROM comparent les 122 noms et les 178 autres cellules au
build qualifié par B-683, ainsi que les données et pointeurs de description.

La sonde Playwright headless appelle `bufferitemname` dans le moteur mGBA réel
pour les 122 identifiants et compare les buffers obtenus aux cellules de la ROM.
Douze noms sont rendus dans les boîtes natives et vérifiés par OCR, dont les
orbes, les abréviations, les umlauts, Granitstein et plusieurs objets Unbound.
La ROM de sonde et les captures restent dans le répertoire temporaire système.

Résultats locaux :

- Hooks activés : 3 169 tests Python rapides réussis (un skip préexistant),
  68 tests Vitest réussis, builds FR/IT/DE réussis dans le worktree isolé.
- `make test-python` : 3 310 réussis, 96 sous-tests réussis, trois skips
  préexistants (bridge mGBA facultatif, échantillon FD absent, CSV dynamique ES).
- Test ROM : 300 cellules vérifiées, dont 122 corrigées et 178 préservées ;
  métadonnées et pointeurs de description inchangés par rapport à la qualification.
- Playwright : un test réussi, 122 lookups moteur, douze noms rendus, OCR et
  assertions de pixels sur ö/ä. Deux ambiguïtés OCR connues (Blouer/Blauer,
  Herte-Sconner/Werte-Scanner) sont tolérées ; les buffers restent comparés
  octet par octet et le a de Blauer est aussi comparé au a de Granitstein.
- Ruff et TypeScript : aucune erreur sur le périmètre contrôlé.
- SHA256 DE reconstruite :
  `dd961d9091f3c3e6214a2773aa0f8f509b8684ec62d15de9a6f73d1d49ca73af`.
- Capture attachée au ticket : `0d44263f-3538-48b3-9da4-482d5053b4fc`.
- SHA256 de la ROM FR du dépôt principal inchangé. Aucun fichier FR/IT livré,
  aucun push ni pipeline distant.

Les captures montrent les boîtes natives de messages ; la largeur du sac est
contrôlée par budget pixels et non par une capture de chacune des 122 lignes.
