# Hindi romanisé HI-01 — F-693

## Périmètre et dépendances

Dépôt gba_translator, branche unbound, suite de A-665. Les préalables F-691
(infrastructure) et D-692 (glossaire) sont livrés et intégrés avant traduction.
HI-LATIN-1 reste la convention ; le glossaire central passe à 1.1.0 avec neuf
termes communs rencontrés ici (Type, evolution, stat, nickname, storage, coin,
Egg, species, aide). Le nom historique `glossary_v1.json` reste compatible.
Ces équivalents sont éditoriaux, ancrés dans l'anglais vivant, pas officiels.

Snapshot `languages/en/combined_en.txt` : SHA-256
`65e93f43b9f92f19ba011fb4971aea6f44d9cd419363d7b51d9dbe094235af19`.
Les 425 occurrences de l'intervalle inclusif 0x28780–0x1A5301 se résolvent en
400 offsets distincts, hors seeds 0x1773FD, 0x177489, 0x183509. Aucune adresse
n'est interprétée comme une zone géographique. Aucun autre lot n'est inclus.

L'inventaire exhaustif est `languages/indie/data/hi01_inventory.json` : anglais
last-wins, octets EN témoins, sites de pointeurs, contexte, classe et décision
pour chacune des 400 entrées. ROM EN témoin : SHA-256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

## Décisions

355 entrées traduites, 5 conservées et 40 exclues. Les conservations couvrent
les panneaux Log Pokemon Research Lab, Valley Cave et Unbound Development Room,
le format de durée et le cri `Bra!`. La suppression de l'accent de Pokemon suit
le glossaire. Les noms d'espèces, personnages, lieux, objets, attaques et talents
restent EN à l'intérieur des phrases traduites.

Les exclusions distinguent : 11 débuts décalés d'un octet, 2 extractions non
textuelles/vides, 2 fragments sans référence, 18 textes sans consommateur vivant
démontré, 5 correspondances de pointeur dans du bruit binaire, 2 fragments
malformés réellement appelés. Aucun de ces cas n'est injecté. L'absence de
pointeur direct n'est pas une preuve d'inaccessibilité absolue.

Les fragments 0x192116 et 0x1A5200 ont des `loadpointer` réels à 0x16AA68 et
0x1A6990. Ils restent exclus : traduire leur fragment indépendamment ferait
passer une anomalie source pour une traduction validée. Leurs octets doivent
rester intacts lorsque les textes englobants sont relogés.

Les références `trainerbattle`, `loadpointer`, `message` et le pointeur code de
la question PC sont distingués des occurrences binaires accidentelles. Aucune
entrée ne relève d'une cellule fixe déclarée. Les budgets incluent FF ; la
relocalisation exige la vérification de chaque pointeur après build.

## Contrat d'encodage et de rendu

Chaque ajout possède une protection exacte last-wins dans le même commit.
Les sources cumulatives existantes ne sont ni triées ni régénérées. Les trois
seeds restent inchangées. Aucun fichier FR ni police partagée n'est modifié.

Les faux caractères accentués des contrôles du snapshot sont remplacés par
leurs octets bruts vérifiés : FD01/02/03/04/05/06/0F/10 et FC0104/06/08.
Le caractère `"` du snapshot correspond à l'ellipse B0 : il est conservé comme
`<0xB0>`. Ordre, multiplicité, couleurs, pauses et séquence FE/FA/FB sont testés
contre les témoins EN, et non contre un réencodage naïf du snapshot.

La largeur est mesurée avec la table de police de la ROM et des bornes par
buffer : joueur/rival 42 px, espèce 60 px, objet 78 px, attaque 72 px, combat
90 px ; chronomètre 18 px et mesures de pêche 36 px. Les sondes ne prouvent pas
les expansions personnalisées hors de ces contrats de cellules EN.

Les sondes Playwright headless réutilisent le moteur natif mGBA hors écran,
les pointeurs de la ROM livrée et une copie privée de sauvegarde. Elles
vérifient les octets, le texte réellement rendu par OCR et la sauvegarde
inchangée pour une défaite, un dialogue et la question PC. Elles ne constituent
pas un parcours intégral des quêtes ni une preuve de toutes les branches.

Le contrat `hi01_preserved_sources.json` active le mécanisme existant de
relocalisation et de préservation des contrôles pour les 360 entrées. Le
normaliseur générique aurait autrement reformaté 254 textes. Les sources EN
restent intactes, les faux pointeurs restent inchangés et seuls les sites
qualifiés sont repointés ; aucun code partagé n'est modifié.

## Validation

Commandes : `make test-python`, `make build-indie`, tests métier HI-01,
contrôle ROM vivant puis
`npx playwright test -c tests/e2e-playwright/playwright.hi01.config.ts`.
La preuve PNG est créée dans le répertoire temporaire système puis attachée au
ticket ; elle ne fait pas partie du dépôt. Aucun bundle de release commun,
push ou pipeline distant n'est produit.

Le hash FR du checkout principal, relevé avant travaux, est
`74a0b3b13a1b02cebb1519c36df7552dfde8e6a383ff16e17ae46bbdd0830a6e`.
Les builds imposés par les hooks restent locaux au worktree.

Non vérifié : relecture linguistique native, parcours complet des branches et
toutes les expansions runtime des buffers. Les exclusions sont explicites et
ne sont pas comptées comme traductions réussies.
