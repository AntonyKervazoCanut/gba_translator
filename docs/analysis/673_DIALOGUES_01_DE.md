# B-673 — Qualification de dialogues-01

Périmètre exclusif : les 300 offsets du ticket B-673, de `0x4ABE2F` à
`0x7BA306`. Aucun audit global relancé. Le relevé
[673_DIALOGUES_01_DE.json](673_DIALOGUES_01_DE.json) contient une décision pour
chaque adresse, les dernières valeurs EN/FR/DE, les octets canoniques, tous les
sites de référence et leur contexte binaire. Une absence FR reste explicitement
`null` ; le corpus dit EN ne remplace pas la ROM canonique.

## Sources et méthode

ROM EN vérifiée : SHA-256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
Les noms d'attaques sont confrontés au référentiel figé
`languages/de/data/move_names_de_official.json`, les objets au glossaire
`official_terminology.yaml` et à la table allemande existante, lus sans édition.
Les 162 traductions préparées sont toutes présentes dans l'extraction EN utilisée
par le build ; leur insertion ne repose donc pas sur une hypothèse de couverture.

Les corrections portent notamment sur Eishieb (au lieu d'Eisenfaust), Rückkehr
(au lieu de Vergeltung), Reflektor (au lieu de Schutzschild), Beleber et
Stromisierer. La scène `0x7A823B` décrit bien Electabuzz, appelé **Elektek** en
allemand, et non Elekid : le texte conserve **Electabuzz**, conformément à la
politique des noms d'espèces EN du build. L'objet devient Stromisierer.
Le récit du Rotom-Fan et du Luftballon retrouve sa chute complète et son ironie.
Les descriptions de Magmariseur, Honor Ball et Bel'Écaille sont traitées comme
des descriptions d'objets ; aucune fiche Pokédex n'est présente dans ce lot.
`0x780E33` est un faux début de description d'attaque, pas une fiche d'espèce.

Le registre ordinaire s'adresse au joueur avec `du`. Le vendeur s'adresse
poliment au client menaçant avec `Sie`, les Rüpel gardent leur ton brusque,
Marlon ses impératifs, et le personnage reconnaissant de `0x7882F7` garde son
`Ihr` respectueux. La fille de `0x75DA52` parle à son père (`Tochter`, `Papa`).
Dans la quête du Pokémon volé, l'artiste parle d'un Pokémon femelle : les
pronoms `sie` et l'œuf pondu sont conservés, sans transformer le genre en neutre
à cause du mot `Baby`. Aucune variable Sohn/Tochter n'a été supprimée ou permutée.

## Protection des sources

Éditions par patch de lignes exactes, sur une relecture fraîche du fichier :
seules les dernières occurrences gagnantes sont remplacées ; les entrées absentes
sont ajoutées en fin de fichier. Aucun tri, aucune régénération et aucune
suppression de doublon. Chaque nouvelle valeur est protégée exactement dans
`protected_entries.yaml`, dans le même commit que le texte. La matrice
`parity.yaml` ne reçoit que la déclaration du nouveau test exigée par le hook.
Aucun patch ni donnée de jeu, aucune source FR/IT et aucun hash de référence FR
ne sont modifiés.

Les commandes FC/FD sont comparées comme séquences multioctets, dans leur ordre,
et non comme lettres accentuées. Les alias de couleurs sont écrits en octets bruts
pour lever les ambiguïtés. Les 162 textes conservent **toutes les coupures de page
FB** du canon, dans le même ordre. Les retours FE et défilements FA sont réagencés
pour les boîtes à deux lignes, à 192 pixels maximum ; les trois descriptions
d'objets restent sur trois lignes. Les umlauts ä/ö/ü et ß sont réellement encodés.

## Exclusions et suites techniques

Le relevé distingue les noms de personnages, toponymes, panneaux de destinations,
cris et termes allemands identiques à l'anglais (`Winter`, `Cafeteria`). Ils ne
constituent pas des oublis de traduction. Le nom Pokémon Day Care reste conservé,
comme le prévoit déjà sa protection de toponyme.

Les entrées sans pointeur direct sont documentées individuellement. Les faux
préfixes `9`, les départs au milieu d'une instruction et les copies obsolètes ne
sont pas traduits artificiellement. Pour `0x722125` et `0x724AD9`, la même chaîne
possède une copie référencée à `0x787C0E`, corrigée dans ce lot. Pour les adresses
sans scène active démontrée, l'absence de référence directe est le constat
binaire ; elle ne constitue pas une preuve universelle d'inaccessibilité par
calcul d'adresse. Aucune insertion n'est faite sur cette seule supposition.

Vingt offsets possèdent une référence mais commencent dans un fragment ou des
instructions : ils sont classés **besoin de patch séparé**, et non « chaîne morte ».
Les sites exacts sont consignés dans le JSON. Corriger leur pointeur ou traduire
le début de leur chaîne hors lot dépasserait l'autorisation du présent ticket.
C'est notamment le cas de l'aide des arènes de Vega et Mirskle, du texte
Protective Pads, de plusieurs fragments de la famille de Mel et de la légende
de Darkrai. Le cas `0x778EAF` commence par `04 FE` après une suite de commandes de
déplacement : ce préfixe n'est pas une lettre à traduire aveuglément.

## Validation locale

Résultats binaires et visuels à compléter après le build et la lecture du commit.
Le test `tests/unit/test_dialogues_01_de.py` contrôle les 300 décisions et les
valeurs gagnantes ; ses tests marqués `rom` suivent les sites de pointeurs
originaux après toute la chaîne de patches. Le test Playwright
`tests/e2e-playwright/specs/dialogues-01-de.spec.ts` ouvre les textes réellement
injectés dans l'imprimante native mGBA, hors écran, et contrôle leur rendu par OCR.
Il utilise une copie temporaire de la ROM et de la sauvegarde ; aucune sauvegarde
en jeu n'est effectuée.
