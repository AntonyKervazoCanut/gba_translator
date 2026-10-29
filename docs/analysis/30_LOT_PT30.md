# PT-30 — Noms fixes des objets CFRU

Le domaine réel est la table des noms d’objets, et non les zones de Borrius.
Le bilan exhaustif, dans l’ordre exact des 288 offsets du manifeste, est
`languages/pt/data/pt30_audit.json` : corpus EN, comparaison FR, octets source,
cellule, identifiant, décision, octets et largeur de chaque nom.

283 cellules vivantes : Potion devient Poção (F-759) ; les 282 autres noms
restent anglais selon la politique explicite du glossaire pour les objets.
Le corpus « EN » contient des noms français hérités ; la ROM source propre
est décodée pour retrouver Great Ball, Net Ball, Burn Heal, Life Orb, etc.
Aucune francisation des noms n’est importée. Les graphies compactes du jeu
(Thunderstone, EnergyPowder, Weak Policy) sont conservées.

La racine moteur 0x09a8d8 contient 0x08876200. Le lecteur indexé emploie
un stride de 44 octets et un nom de 14 octets, terminateur compris.
Le patch local batch_30 valide le lecteur réel et les budgets avant écriture.
Il ne modifie ni identifiants, prix, effets, descriptions, ni pointeurs.
Les noms tiennent sur une ligne, sans contrôle ni placeholder, au maximum
13 glyphes/14 octets et 70 pixels ; budget conservateur de 78 pixels.

Cinq exceptions, sans pointeur direct dans la ROM :

| Offset | Cellule | Motif |
|---|---|---|
| 0x876b49 | 0x876b48 | +1 après un terminateur initial ; ancien nom BROKEN, cellule vide |
| 0x8770f5 | 0x8770f4 | +1 après un terminateur initial ; ancien Oddish Leaf, cellule vide |
| 0x8775f7 | 0x8775f0 | suffixe résiduel « ring » après Sachet et son terminateur |
| 0x878015 | 0x878014 | +1 après un terminateur initial ; ancien Enigma Berry, cellule vide |
| 0x8781f9 | 0x8781f8 | +1 après un terminateur initial ; ancien Choice Band, cellule vide |

Ces suffixes ne sont jamais les débuts de noms lus par la table indexée.
Ils ne sont pas traduits et leurs octets doivent rester identiques après build.
Les rencontres de quatre octets ayant la valeur d’un pointeur sont conservées
comme observations brutes dans l’audit ; la preuve de vie des noms repose sur
le lecteur indexé, pas sur ces matches parfois non alignés.

Validation automatisée : intégrité et protections exactes des 283 lignes,
contrat du glossaire, cellules bornées, idempotence, refus atomique si lecteur
inconnu ; oracle ROM final pour les 283 noms et les cinq exceptions.
La preuve Playwright hors écran utilise mGBA et une copie temporaire de la ROM :
seul le champ nom Poção livré est copié sur la Repousse déjà dans le Cube de
la sauvegarde de test. L’OCR affirme Poção sur le vrai rendu ; aucune sauvegarde
en jeu, aucune capture dans le dépôt. Ce test démontre le rendu du nom et ne
prétend pas démontrer une acquisition naturelle de Potion.
