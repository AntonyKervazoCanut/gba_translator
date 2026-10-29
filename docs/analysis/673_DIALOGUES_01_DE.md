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
Les 162 traductions corrigées sont toutes présentes dans l'extraction EN utilisée
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

Bilan des 300 décisions : **162 corrigés**, **6 déjà corrects**, **83 noms/cris
légitimes**, **29 entrées sans référence directe**, **20 besoins de patch séparé**.

Vingt offsets possèdent une référence mais commencent dans un fragment ou des
instructions : ils sont classés **besoin de patch séparé**, et non « chaîne morte ».
Les sites exacts sont consignés dans le JSON. Corriger leur pointeur ou traduire
le début de leur chaîne hors lot dépasserait l'autorisation du présent ticket.
C'est notamment le cas de l'aide des arènes de Vega et Mirskle, du texte
Protective Pads, de plusieurs fragments de la famille de Mel et de la légende
de Darkrai. Le cas `0x778EAF` commence par `04 FE` après une suite de commandes de
déplacement : ce préfixe n'est pas une lettre à traduire aveuglément.

## Validation locale

Les gardes ROM suivent les **312 sites de référence** du lot après la chaîne
complète, et comparent les textes, commandes et pages aux attentes. Les adresses
allouées sont résolues à chaque test, car elles peuvent changer lors d'un rebuild.
Les octets attendus sont consignés par site dans le JSON. Les vingt fragments
référencés y sont expressément identifiés comme défectueux : le test documente
leur état, sans prétendre qu'ils sont traduits correctement.

Le dialogue complet de Darkrai (`0x7B8E3A`) est relocalisé : le pointeur
`0x7A2A9D` lit les 257 octets DE et ne réécrit plus le suffixe `0x7B8EDD`,
encore atteint en anglais via `0x7A8C9A`. Une garde interdit qu'une nouvelle
chaîne DE recouvre un des vingt suffixes non résolus. Le seul partage interne
entre deux textes corrigés est le suffixe enfant `0x7AA8E5` du dialogue
`0x7AA8CE` : les deux chaînes complètes attendues sont vérifiées séparément.

La mesure des boîtes utilise aussi les **octets encodés et les largeurs de
glyphes**, pas seulement les jetons de la source. Cela inclut le glyphe B0
d'ellipse (6 pixels) : `0x7B8CFF` est limité à 180 pixels. Les commandes FC01
sont sans largeur ; les variables FD réservent la largeur prudente du moteur
de mise en page du dépôt. Les pages FB restent strictement identiques en nombre
et en ordre au canon, et aucune variable n'est supprimée ou déplacée.

Commandes de validation locale :

- `make build-de` (également imposé par les hooks, avec les builds FR/IT isolés) ;
- `make test-python` et `make lint` ;
- `python3 -m pytest tests/unit/test_dialogues_01_de.py tests/unit/test_translation_integrity.py -q` ;
- `npx playwright test -c tests/e2e-playwright/playwright.dialogues-01-de.config.ts`.

Le test Playwright ouvre les textes réellement injectés dans l'imprimante
native mGBA, hors écran, puis vérifie Zerschneider, Eishieb, Rückkehr, Electabuzz,
Stromisierer et la fin du dialogue d'évolution par OCR. La capture est produite
dans le répertoire temporaire du système et jointe au ticket, jamais au dépôt.
Une copie temporaire de la ROM reçoit seulement les scripts de déclenchement ;
les textes proviennent des pointeurs de la ROM reconstruite. Aucune sauvegarde
en jeu n'est effectuée. Les résultats de la dernière exécution sur la branche
intégrée et la capture sont consignés dans la résolution de B-673.

## Non vérifié / travail distinct

Le parcours manuel de toutes les scènes et l'inaccessibilité absolue des données
sans référence directe ne sont pas démontrés. La qualification précise ce que
prouvent les octets, les sites de référence et les scénarios visuels couverts.
Les vingt fragments ci-dessous nécessitent une analyse de leur script appelant
et un patch séparé : aucune relocalisation aveugle ni modification d'un début
de chaîne hors lot n'est autorisée ici. Le relevé conserve leur texte réellement
atteint, y compris les fragments allemands tronqués et les résidus français.

| Offset | Sites à qualifier / repointer |
|---|---|
| 0x741693 | 0x741548 |
| 0x7416B5 | 0x741565 |
| 0x741717 | 0x74157f |
| 0x7417CE | 0x7414ac |
| 0x74C34E | 0x74c228 |
| 0x74C367 | 0x74c237 |
| 0x778EAF | 0x7635d7, 0x7635de, 0x7635e5, 0x7636fa, 0x763701 |
| 0x788BAB | 0x744c9b |
| 0x788BCD | 0x744cae |
| 0x788BFF | 0x744cc8 |
| 0x788C15 | 0x744cf9 |
| 0x78C6F8 | 0x78c664 |
| 0x78D961 | 0x78dcca |
| 0x78DC12 | 0x78dcf8 |
| 0x7A3D5D | 0x7a3f10 |
| 0x7A3D98 | 0x7a3f26 |
| 0x7A3DFE | 0x7a3f41 |
| 0x7AB089 | 0x7538cb |
| 0x7B4A4E | 0xb50347 |
| 0x7B8EDD | 0x7a8c9a |
