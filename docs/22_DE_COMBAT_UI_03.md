# 22 — Qualification DE combat_ui-03 (B-669)

Périmètre fermé : les 300 offsets du ticket, comparés aux dernières valeurs EN, FR et DE.
La fixture `tests/unit/fixtures/de_combat_ui_03.json` conserve les trois valeurs avant correction,
les octets canoniques EN, les sites de pointeurs et les décisions individuelles.

## Méthode et limites

- Source EN SHA-256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
- 204 corrections : 203 ajouts et un pied de menu existant raccourci, protégés exactement.
- 67 besoins de patch séparé (B-1013), 16 noms légitimes, 10 fragments non vivants et 3 sentinelles : voir décisions ci-dessous.
- Recherche des références 32 bits little-endian, y compris non alignées. Pour les attaques,
  table vivante `0x99F190` ; pour les talents, table de noms `0xA36398`, pas 17 octets,
  et table de descriptions `0x96DE04`. L’absence de référence ne prouve pas à elle seule
  l’impossibilité d’un accès arithmétique : les exclusions sans référence restent conservées,
  jamais écrasées. Aucun nouveau patch ou changement de ressource linguistique. Les propositions non injectables sont conservées dans `proposed_after` de la fixture ; leur absence DE est protégée.
- L’EN extrait est vide pour de nombreuses attaques et contient même du FR à `0xA3A821` :
  la ROM EN tranche. Le FR est comparé, mais ses contresens ne sont pas repris
  (ex. `0xA3A006` ajoute à tort une hausse d’Attaque, `0xA39A1B` traduit les coquilles par des obus).
- Glossaire : Attacke, Fähigkeit, KP, Angriff, Verteidigung, Spezialangriff,
  Spezialverteidigung, Initiative ; abréviations Sp.-Ang./Sp.-Vert. en fenêtre étroite.
  Frostbrand désigne la gelure spécifique Unbound, distincte du statut Gefroren.
- Registre : tutoiement pour le joueur ; descriptions impersonnelles. Aucun buffer
  Sohn/Tochter ni pronom genré de personnage dans ce lot. Noms DAISY/BILL/FUJI conservés.
- Commandes : comparaison des octets FC/FD/F7/F8 et des ruptures FE/FA/FB dans l’ordre.
  Alias bruts explicites pour éviter les arguments perdus. Même nombre de lignes que l’EN
  pour chaque correction ; descriptions ≤122 px et ≤5 lignes ; textes UI ≤208 px
  avec réserve de largeur pour les buffers. Les cellules fixes sont vérifiées en octets.
- Les noms officiels allemands identiques à l’anglais restent légitimes, même absents du
  fichier DE : leur cellule EN est déjà correcte (Insomnia, Chlorophyll, Plus, Minus, etc.).

## Validation

Validation finale après retrait des 67 injections non conformes : en cours.
Le premier build a prouvé 49 omissions d’extraction et 18 rewraps incompatibles.
B-1013 porte exclusivement leur réparation ; aucune de ces entrées n’est comptée corrigée.
Playwright headless + mGBA hors écran et OCR : 1 test passé, capture attachée à B-669.
Le prérequis ES/FR de T-915 est déjà résolu par A-663 (`6988ec86`) dans la base reprise.
La suite ciblée vérifie les 300 décisions et les octets de chaque correction, pas seulement
la présence du texte dans le fichier. Aucun audit global A-661 relancé.

## Décision par offset

| Offset | Scène / surface | Décision | Justification | Références EN |
|---|---|---|---|---|
| `0x41E067` | Easy Chat / catégories | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x3EDFDC` |
| `0x41E06E` | Easy Chat / catégories | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x3EDFE0` |
| `0x41E075` | Easy Chat / catégories | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x3EDFE4` |
| `0x41E07C` | Easy Chat / catégories | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x3EDFE8` |
| `0x41E08A` | Easy Chat / catégories | nom propre légitime | Catégorie Easy Chat Pokémon2 : nom de franchise et suffixe numérique conservés. | `0x3EDF98` |
| `0x41E098` | Easy Chat / catégories | fragment non vivant | Lv isolé, sans référence littérale ; ne pas écraser une ancienne cellule non reliée au résumé actif. | aucune (voir méthode) |
| `0x41E0A5` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x4DBC8` |
| `0x41E0B9` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x16C1C6`, `0x261ECC`, `0x7D8E50`, `0x1E62441`, `0x1E6C46E`, `0x1E6C5D8`, `0x1E6C717`, `0x1E6C857`, `0x1E6CA7A`, `0x1E80B1D`, `0x1E80B72`, `0x1E8DA14`, `0x1E8DAB3`, `0x1E912F2`, `0x1E9E53E`, `0x1E9E6F2`, `0x1E9E7A8`, `0x1E9E835`, `0x1E9E8C2`, `0x1E9E941`, `0x1E9E9B5`, `0x1E9EB1D`, `0x1E9EE63`, `0x1E9F25A`, `0x1E9FA01`, `0x1E9FADF`, `0x1E9FB91`, `0x1E9FC57`, `0x1E9FDC3`, `0x1EA0744`, `0x1EA085C`, `0x1EA098C`, `0x1EA0AA2`, `0x1EA0B54`, `0x1EA0C24`, `0x1EA0CA6`, `0x1EA2428`, `0x1EA29C0`, `0x1EA2E9E`, `0x1EA38B9`, `0x1EA3972`, `0x1EA3A72`, `0x1EA419C`, `0x1EA4381`, `0x1EA4497`, `0x1EA4624`, `0x1EA46C0`, `0x1EA4AB6`, `0x1EA4C60`, `0x1EB018B`, `0x1EB0215`, `0x1EB0434`, `0x1EB04D7`, `0x1EB0581` |
| `0x41E0C0` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261ED0` |
| `0x41E0D2` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261ED4` |
| `0x41E0DA` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261ED8` |
| `0x41E0E0` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261EDC` |
| `0x41E0EE` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261EE0` |
| `0x41E10A` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261EE4` |
| `0x41E112` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261EEC` |
| `0x41E118` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261EF4` |
| `0x41E145` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x261EF8` |
| `0x41E16B` | Échange de Pokémon | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x261EFC` |
| `0x41E199` | Échange de Pokémon | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x261F04` |
| `0x41E1C5` | Échange de Pokémon | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x261F08` |
| `0x41E1E9` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x514B0`, `0x528A0` |
| `0x41E200` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x51528`, `0x52918` |
| `0x41E20D` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x52158`, `0x535B4` |
| `0x41E21E` | Échange de Pokémon | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x521FC`, `0x53658` |
| `0x41E234` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xBF1E4`, `0xBF350` |
| `0x41E245` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAAC` |
| `0x41E263` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAB0` |
| `0x41E273` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAB4` |
| `0x41E284` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAB8` |
| `0x41E29E` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FABC` |
| `0x41E2B4` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FA9C` |
| `0x41E2BF` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAA0` |
| `0x41E2C9` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAA4` |
| `0x41E2D4` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x46FAA8` |
| `0x41E2EC` | État réseau / Konnex-Klub | fragment non vivant | Ancien pied de menu B/Cancel sans référence littérale ; les pieds vivants 41E5B9 et 41EDCA sont corrigés. | aucune (voir méthode) |
| `0x41E325` | État réseau / Konnex-Klub | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x54064`, `0xCF9C8` |
| `0x41E33C` | Pension : compatibilité de reproduction | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x25F82C` |
| `0x41E361` | Pension : compatibilité de reproduction | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x25F830` |
| `0x41E37C` | Pension : compatibilité de reproduction | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x25F834` |
| `0x41E3A8` | Pension : compatibilité de reproduction | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x25F838` |
| `0x41E3E3` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE4F50` |
| `0x41E3FB` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE526C`, `0x9F73F8` |
| `0x41E405` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE4AD8` |
| `0x41E414` | Maître des capacités / apprentissage | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0xE4B68` |
| `0x41E481` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE4BEC` |
| `0x41E493` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE4E68` |
| `0x41E4C0` | Maître des capacités / apprentissage | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0xE4E88` |
| `0x41E4E2` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE5280`, `0xE52DC` |
| `0x41E50C` | Maître des capacités / apprentissage | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0xE4BC8` |
| `0x41E538` | Combat réseau / pieds de menus | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x11C384` |
| `0x41E572` | Combat réseau / pieds de menus | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x11C538` |
| `0x41E58D` | Combat réseau / pieds de menus | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x11C4DC` |
| `0x41E5A4` | Combat réseau / pieds de menus | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x12D164` |
| `0x41E5B9` | Combat réseau / pieds de menus | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x12D16C` |
| `0x41E5D2` | Combat réseau / pieds de menus | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x12D168` |
| `0x41E5ED` | Aide : personnages | nom propre légitime | Nom propre DAISY dans la table de personnages ; politique de conservation des noms EN. | `0x45F610` |
| `0x41E5F3` | Aide : personnages | nom propre légitime | Nom propre BILL dans la table de personnages ; pas le renommage français LEO. | `0x45F614` |
| `0x41E5F8` | Aide : personnages | nom propre légitime | Nom propre FUJI, identique en EN/FR. | `0x45F618` |
| `0x41E5FD` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x466ED8` |
| `0x41E63F` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x466EDC` |
| `0x41E669` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x466EE0` |
| `0x41E685` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x466EE4` |
| `0x41E6A1` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142FBC` |
| `0x41E6DC` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142FE0` |
| `0x41E717` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142FF4` |
| `0x41E741` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x143004` |
| `0x41E76B` | Cadeau Mystère / connexion sans fil | fragment non vivant | Ancien message Link standby sans référence littérale ; les messages référencés de connexion sont corrigés. | aucune (voir méthode) |
| `0x41E794` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x1430F8` |
| `0x41E7A3` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x143258` |
| `0x41E7BC` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142CC8`, `0x142D6C`, `0x1435A8` |
| `0x41E7D1` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142CA4` |
| `0x41E7F2` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x1431D8` |
| `0x41E823` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x143204` |
| `0x41E866` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C40` |
| `0x41E88F` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C58` |
| `0x41E8BD` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C44` |
| `0x41E8E2` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C5C` |
| `0x41E90C` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C68` |
| `0x41E92B` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142CD4` |
| `0x41E946` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142C74` |
| `0x41E968` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142C8C` |
| `0x41E98F` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142C80` |
| `0x41E9AB` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C98`, `0x142DF8` |
| `0x41E9D3` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142C2C`, `0x142DBC` |
| `0x41EA0D` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142CBC` |
| `0x41EA3F` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142CB8` |
| `0x41EA6F` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142C20`, `0x142DB4` |
| `0x41EA86` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142928` |
| `0x41EAB7` | Cadeau Mystère / connexion sans fil | besoin de patch séparé | B-1013 : le rewrap automatique du build modifie les ruptures de cette boîte ; injection retirée pour préserver commandes et forme. | `0x142988` |
| `0x41EAE7` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x1434FC` |
| `0x41EB01` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x143510` |
| `0x41EB20` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142DC4` |
| `0x41EB46` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142DD0` |
| `0x41EB71` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142DD8` |
| `0x41EB8E` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142E0C` |
| `0x41EBAA` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142DE0` |
| `0x41EBDE` | Cadeau Mystère / connexion sans fil | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x142DF0` |
| `0x41EDCA` | Cadeau Mystère / connexion sans fil | corrigé | Pied de menu raccourci (Zurück), boutons F8 explicites ; évite le libellé Verlassen trop long. | `0x1423A4` |
| `0x41EFB8` | Cadeau Mystère / connexion sans fil | fragment non vivant | Faux positif de décodage de données binaires (motifs répétitifs), sans pointeur de texte ; ne pas injecter de prose. | aucune (voir méthode) |
| `0x41F0A8` | Cadeau Mystère / connexion sans fil | fragment non vivant | Faux positif de décodage de données binaires (motifs répétitifs), sans pointeur de texte ; ne pas injecter de prose. | aucune (voir méthode) |
| `0x41F0BD` | Cadeau Mystère / connexion sans fil | fragment non vivant | Faux positif de décodage de données binaires (motifs répétitifs), sans pointeur de texte ; ne pas injecter de prose. | aucune (voir méthode) |
| `0x41F160` | Cadeau Mystère / connexion sans fil | fragment non vivant | Faux positif de décodage de données binaires (motifs répétitifs), sans pointeur de texte ; ne pas injecter de prose. | aucune (voir méthode) |
| `0xA34F4C` | Résumé : description de talent | corrigé | Immunité au Frostbrand (gelure), et non au gel : effet Unbound conservé. | `0x96DEA4` |
| `0xA35424` | Résumé : description de talent | fragment non vivant | Ancienne description sans référence dans la ROM, notamment aucune dans la table de talents 96DE04. | aucune (voir méthode) |
| `0xA35811` | Résumé : description de talent | fragment non vivant | Ancienne description sans référence dans la table de talents 96DE04 ni ailleurs dans la ROM. | aucune (voir méthode) |
| `0xA35DCF` | Résumé : description de talent | fragment non vivant | Ancienne description sans référence dans la table de talents 96DE04 ni ailleurs dans la ROM. | aucune (voir méthode) |
| `0xA36398` | Table des noms de talents | déjà correct/patché | Sentinelle -------, talent 0 de la table indexée de pas 17 octets. | `0x1C0`, `0xD8004`, `0xD8624`, `0x1367A0`, `0x8BF5F4`, `0x9A9CDC` |
| `0xA36497` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Insomnia. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA365DA` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Chlorophyll. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA36761` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Plus. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA36772` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Minus. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA36860` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Transistor. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA36A4D` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Filter. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA36A6F` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Download. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA36AB3` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Hydration. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA37322` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Receiver. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA37377` | Table des noms de talents | corrigé | Valiant Shield : traduction du talent défensif Wackerer Schild, 16 octets avec terminateur, cellule 17 octets. | aucune (voir méthode) |
| `0xA373EE` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Punk Rock. Cellule indexée de 17 octets, absence de pointeur individuel normale. | aucune (voir méthode) |
| `0xA37487` | Table des noms de talents | déjà correct/patché | Sentinelle - dans la table indexée de talents ; aucune prose à traduire. | aucune (voir méthode) |
| `0xA3750F` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Teravolt. Cellule indexée de 17 octets, absence de pointeur individuel normale. | `0x9A9C28` |
| `0xA37531` | Table des noms de talents | nom propre légitime | Nom de talent identique en allemand : Libero. Cellule indexée de 17 octets, absence de pointeur individuel normale. | `0x9A9C48` |
| `0xA37C58` | Table des noms de talents | déjà correct/patché | Sentinelle - partagée par les cases inutilisées de la table des descriptions ; préserver les pointeurs. | `0x99FD8C`, `0x99FD90`, `0x99FD94`, `0x99FD98`, `0x99FD9C`, `0x99FDA0`, `0x99FDA4`, `0x99FDA8`, `0x99FDAC`, `0x99FDB0`, `0x99FDB4`, `0x99FDB8`, `0x99FDBC`, `0x99FDC0`, `0x99FDC4`, `0x99FDC8`, `0x99FDCC`, `0x99FDD0`, `0x99FDD4`, `0x99FDD8`, `0x99FDDC`, `0x99FDE0`, `0x99FDE4`, `0x99FDE8`, `0x99FDEC`, `0x99FDF0`, `0x99FDF4`, `0x99FDF8`, `0x99FDFC`, `0x99FE00`, `0x99FE04`, `0x99FE08`, `0x99FE0C`, `0x99FE10`, `0x99FE14`, `0x99FE18`, `0x99FE1C`, `0x99FE20`, `0x99FE24`, `0x99FE28`, `0x99FE2C`, `0x99FE30`, `0x99FE34`, `0x99FE38`, `0x99FE3C`, `0x99FE40`, `0x99FE44`, `0x99FE48`, `0x99FE4C`, `0x99FE50`, `0x99FE54`, `0x99FE58`, `0x99FE5C` |
| `0xA37D4F` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F2B8` |
| `0xA37D98` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F414` |
| `0xA37E33` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F524` |
| `0xA37EC4` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x879C00`, `0x99F71C` |
| `0xA37F07` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F720` |
| `0xA37F4D` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F724` |
| `0xA37F8D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F728` |
| `0xA37FD7` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F72C` |
| `0xA38061` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F734` |
| `0xA380AB` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F738` |
| `0xA380F4` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F73C` |
| `0xA38183` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F744` |
| `0xA381CF` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F748` |
| `0xA3825A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F750` |
| `0xA382AD` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F754` |
| `0xA38385` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F760` |
| `0xA38538` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F778` |
| `0xA3857A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F77C` |
| `0xA385BB` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F780` |
| `0xA385FF` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F784` |
| `0xA3863E` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F788` |
| `0xA38686` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F78C` |
| `0xA386D1` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F790` |
| `0xA38706` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F794` |
| `0xA3874A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F798` |
| `0xA3878C` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F79C` |
| `0xA387D7` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F7A0` |
| `0xA38821` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7A4` |
| `0xA38864` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7A8` |
| `0xA388A6` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7AC` |
| `0xA38978` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F7B8` |
| `0xA38A0F` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7C0` |
| `0xA38A89` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7C8` |
| `0xA38ACF` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7CC` |
| `0xA38B60` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7D4` |
| `0xA38BA4` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7D8` |
| `0xA38BEC` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F7DC` |
| `0xA38C87` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7E4` |
| `0xA38D6A` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F7F0` |
| `0xA38DAC` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x879D34`, `0x99F7F4` |
| `0xA38DEA` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F7F8` |
| `0xA38E32` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F7FC` |
| `0xA38E70` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F800` |
| `0xA38EB1` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F804` |
| `0xA38F30` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F80C` |
| `0xA38F75` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F810` |
| `0xA38FB8` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87A5CC`, `0x99F814` |
| `0xA38FF2` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87AAF4`, `0x99F818` |
| `0xA39075` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F820` |
| `0xA390BE` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F824` |
| `0xA39106` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87A338`, `0x99F828` |
| `0xA39198` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x87A6D4`, `0x99F830` |
| `0xA391E4` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F834` |
| `0xA39232` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F838` |
| `0xA3927C` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F83C` |
| `0xA392C2` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F840` |
| `0xA3939A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F84C` |
| `0xA393E1` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F850` |
| `0xA3942D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F854` |
| `0xA3947A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F858` |
| `0xA394C9` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F85C` |
| `0xA3950E` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F860` |
| `0xA39557` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F864` |
| `0xA39592` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F868` |
| `0xA395D6` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F86C` |
| `0xA39663` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F874` |
| `0xA39693` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87A7B0`, `0x99F878` |
| `0xA396D3` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87A834`, `0x99F87C` |
| `0xA3975D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F884` |
| `0xA397A7` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F888` |
| `0xA397E7` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F88C` |
| `0xA39830` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F890` |
| `0xA398C0` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F898` |
| `0xA39940` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8A0` |
| `0xA3998B` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F8A4` |
| `0xA399D2` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F8A8` |
| `0xA39A1B` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8AC` |
| `0xA39A60` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8B0` |
| `0xA39AA8` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F8B4` |
| `0xA39AEF` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F8B8` |
| `0xA39B3C` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87A6A8`, `0x99F8BC` |
| `0xA39B78` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x879D08`, `0x99F8C0` |
| `0xA39BF5` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F8C8` |
| `0xA39C81` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F8D0` |
| `0xA39CCD` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x87AB4C`, `0x99F8D4` |
| `0xA39D55` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8DC` |
| `0xA39DD9` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8E4` |
| `0xA39E24` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8E8` |
| `0xA39E67` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8EC` |
| `0xA39EAA` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8F0` |
| `0xA39EF6` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8F4` |
| `0xA39F84` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F8FC` |
| `0xA39FC8` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F900` |
| `0xA3A006` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F904` |
| `0xA3A04E` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F908` |
| `0xA3A097` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F90C` |
| `0xA3A0DA` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F910` |
| `0xA3A127` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F914` |
| `0xA3A16F` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F918` |
| `0xA3A1B6` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F91C` |
| `0xA3A1FE` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F920` |
| `0xA3A243` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F924` |
| `0xA3A31C` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F930` |
| `0xA3A364` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F934` |
| `0xA3A3B3` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F938` |
| `0xA3A3F4` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F93C` |
| `0xA3A430` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F940` |
| `0xA3A474` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F944` |
| `0xA3A506` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F94C` |
| `0xA3A55C` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F950` |
| `0xA3A5AB` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F954` |
| `0xA3A5F3` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F958` |
| `0xA3A682` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F960` |
| `0xA3A821` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F974` |
| `0xA3A8C5` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F97C` |
| `0xA3A903` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F980` |
| `0xA3A955` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F984` |
| `0xA3A9EE` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F98C` |
| `0xA3AAA0` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F994` |
| `0xA3AAFD` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F998` |
| `0xA3AB56` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F99C` |
| `0xA3ABB2` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9A0` |
| `0xA3ACBE` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9AC` |
| `0xA3AD6B` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9B4` |
| `0xA3ADC8` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9B8` |
| `0xA3AE26` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9BC` |
| `0xA3AE83` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9C0` |
| `0xA3AF8E` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9CC` |
| `0xA3AFED` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9D0` |
| `0xA3B037` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9D4` |
| `0xA3B14D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9E0` |
| `0xA3B1A8` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9E4` |
| `0xA3B1FD` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9E8` |
| `0xA3B25A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9EC` |
| `0xA3B2A6` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9F0` |
| `0xA3B306` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99F9F4` |
| `0xA3B35D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99F9F8` |
| `0xA3B408` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA00` |
| `0xA3B45D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA04` |
| `0xA3B4A8` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA08` |
| `0xA3B4FD` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA0C` |
| `0xA3B552` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA10` |
| `0xA3B5AE` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA14` |
| `0xA3B60A` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA18` |
| `0xA3B663` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA1C` |
| `0xA3B6C0` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA20` |
| `0xA3B71D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA24` |
| `0xA3B779` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA28` |
| `0xA3B892` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA34` |
| `0xA3B8EF` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA38` |
| `0xA3BA60` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA48` |
| `0xA3BB24` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA50` |
| `0xA3BC91` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA60` |
| `0xA3BCE2` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA64` |
| `0xA3BD35` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA68` |
| `0xA3BD94` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA6C` |
| `0xA3BDEF` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA70` |
| `0xA3BE9D` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA78` |
| `0xA3BEF9` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA7C` |
| `0xA3BFFD` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA88` |
| `0xA3C052` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA8C` |
| `0xA3C0AD` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA90` |
| `0xA3C157` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA98` |
| `0xA3C1B4` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FA9C` |
| `0xA3C210` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAA0` |
| `0xA3C26B` | Résumé / apprentissage : description d’attaque | besoin de patch séparé | B-1013 : offset absent de l’extraction EN du build ; les pointeurs restent sur le texte EN après construction. | `0x99FAA4` |
| `0xA3C314` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAAC` |
| `0xA3C36C` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAB0` |
| `0xA3C3C6` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAB4` |
| `0xA3C41C` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAB8` |
| `0xA3C5DB` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FACC` |
| `0xA3C67C` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAD4` |
| `0xA3C750` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAE0` |
| `0xA3C7AE` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAE4` |
| `0xA3C863` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAEC` |
| `0xA3C8C0` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAF0` |
| `0xA3C90E` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAF4` |
| `0xA3C96B` | Résumé / apprentissage : description d’attaque | corrigé | Traduction absente ; source canonique EN en ROM, commandes conservées et texte DE borné. | `0x99FAF8` |
