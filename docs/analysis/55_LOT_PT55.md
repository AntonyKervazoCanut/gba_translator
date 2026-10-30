# PT-55 — noms d'espèces et formes

F-814 concerne exactement les 299 offsets du manifeste PT-55. Le domaine
réel est la table fixe de noms d'espèces, et non le scénario étendu.
Les prérequis F-758 et F-759 sont intégrés ; leur politique impose de garder
les noms anglais et les noms de formes du jeu, sans inventer de traduction.

## Sources et résultat

`languages/pt/data/pt55_audit.json` donne le bilan offset par offset : référence
EN historique, comparaison FR, nom canonique effectivement décodé dans la ROM
EN propre, préimage complète de 11 octets, identifiant interne, budget encodé,
largeur et décision. Les 299 entrées sont conservées en anglais et vérifiées ;
aucune exception morte/corrompue. Le corpus `combined_en.txt` est contaminé par
les noms français dans cette table (Cabriolain au lieu de Skiddo, par exemple).
La ROM propre et la règle F-759 priment sur cette référence historique.

Les abréviations de la ROM sont conservées exactement, notamment Blacphalon.
Il ne s'agit pas d'affirmer une nouvelle nomenclature officielle brésilienne.
Chaque valeur est ajoutée avec sa protection exacte. Aucune ancienne traduction
ni entrée d'un autre lot n'est modifiée ou supprimée.

## Structure et injection

Le véritable début indexé est 0x166a98c (espèce 0, ??????), suivi de Bulbasaur
à 0x166a997 (espèce 1). Le pas est 11 octets ; il n'existe pas de pointeur
individuel par cellule. Les 42 références à la base, dont les littéraux des
lecteurs à 0x11450, 0x40fec et 0x12190c, sont consignées et vérifiées dans
la ROM source et la ROM finale. Les cellules sont adressées par base + ID*11.

Le patch dédié `batch_55` valide toutes les références, préimages, valeurs et
budgets avant la première écriture. Il rétablit seulement les 299 cellules du
manifeste après les passes génériques. Le test de réparation part d'une vraie
ROM dont ces seules cellules sont endommagées et exige une égalité binaire
complète avec la source après réparation, puis après une seconde passe.
Une référence altérée doit faire échouer le patch sans écriture partielle.

Les noms ont au plus 10 octets de texte + FF et 59 pixels (métriques normales),
sans placeholder, commande, saut de ligne ou page. Les tests d'intégrité
contrôlent les protections ; le test ROM contrôle les 299 cellules et les
42 lecteurs après `make build-pt`.

## Preuve visuelle et limites

`playwright.pt55.config.ts` exécute mGBA avec Qt offscreen et Chromium headless.
La sonde lit Type: Null et Blacphalon directement aux adresses fixes de la ROM
finale, les présente par une véritable msgbox du moteur, puis exige leur
reconnaissance OCR avant la capture temporaire. Seule une copie temporaire de
ROM reçoit le script de sonde ; les noms et polices restent ceux du build.
Cette preuve vérifie le rendu de deux noms, pas un parcours des 299 fiches ni
le placement de chaque nom dans tous les menus du jeu.
