# PT-57 — Catégories Pokédex et extractions binaires

Le domaine provisoire « Scénario étendu » ne correspond pas au contenu anglais.
Le manifeste contient **166 catégories Pokédex** (Ivysaur à Hitmontop, sélection
non exhaustive) et **133 fragments binaires non linguistiques**. La couverture
fermée, dans l'ordre des 299 offsets autorisés, est enregistrée dans
`languages/pt/data/pt57_audit.json` : anglais, comparaison française, préimages,
catégorie PT-BR et justification de chaque exclusion. Aucun offset d'un autre
lot n'est ajouté au combined, aucune traduction existante n'est supprimée.

## Cellules et consommateurs

La base réelle est `0x1a357cc`, indexée par numéro national, pas par l'offset
extrait : `base + dex_index * 36`. Dix références directes à cette base sont
listées dans l'audit et vérifiées dans la ROM finale, dont `0x105860` utilisé
par le rendu Pokédex. Le champ catégorie occupe douze octets. Les champs
numériques commencent à +12 et les pointeurs de descriptions à +16.
La boucle Thumb `0x10583a–0x105880` copie au maximum onze glyphes puis ajoute
le terminateur. Un test exécute cette boucle de la ROM construite pour les
166 catégories, sans remplacer le code ni les données de texte.

Les offsets du manifeste commencent deux octets avant la cellule, ou six pour
`0x1a363de`, `0x1a36816`, `0x1a378d2`. Ces préfixes sont des champs numériques,
pas des codes de contrôle de dialogue : ils restent strictement inchangés.
Les valeurs du combined sont indexées aux seuls offsets du manifeste ; le patch
`batch_57` calcule la cellule réelle, contrôle toutes les préimages et tous les
lecteurs avant la première écriture et ne modifie que les douze octets du champ.
Les catégories ne passent donc pas silencieusement à travers le filtre des tables
fixes du constructeur générique. Le patch est idempotent et refuse une ROM
tronquée, une préimage différente ou un lecteur incohérent.

## Choix linguistiques et budgets

Le glossaire F-759 est intégré, ainsi que les glyphes F-758. Les noms d'espèces
et noms propres restent anglais ; les noms communs des catégories sont traduits
comme **choix éditoriaux PT-BR**, sans revendication de nomenclature officielle.
Les libellés courts sont limités à onze caractères encodés : les formes abrégées
sont nécessaires pour préserver la structure et le plafond du moteur. Exemples :
`Inseto pel.` = inseto peludo, `Abelha ven.` = abelha venenosa,
`Espinho ven` = espinho venenoso, `Marip. ven.` = mariposa venenosa,
`Gato aranh.` = gato arranhador, `Macaco-por.` = macaco-porco,
`Peixe-dour.` = peixe-dourado, `Cinco estr.` = cinco estrelas,
`Bola espin.` = bola espinhosa, `Erva-algod.` = erva-algodão,
`Escorp. voo` = escorpião voador, `Chifre gr.` = chifre grande.
Les budgets sont mesurés en octets et en pixels ; les cinq tables de largeur de
la ROM finale sont contrôlées : maximum 55 pixels en Small et 65 dans chacune
des quatre autres polices. Aucun placeholder, saut de page ou code de
contrôle n'est supprimé d'un texte vivant : ces catégories n'en contiennent pas.

## Exclusions et preuve

Les 133 fragments de `0x1904ed5` à `0x19db21a` sont des suites répétitives de
données binaires, pas des répliques. Chaque ligne du bilan conserve sa préimage,
un contexte hexadécimal et le résultat de la recherche de pointeur sur les
32 Mio anglais : aucune référence directe à ces adresses. Le test ROM exige
qu'ils restent identiques après construction. Aucun n'est revendiqué traduit.

La recette locale est :

```sh
make build-pt
python3 -m pytest -q tests/unit/pt/test_batch_pt57.py tests/unit/test_translation_integrity.py
python3 -m pytest -q tests/e2e/pt/test_batch_pt57_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt57.config.ts
```

Playwright démarre mGBA hors écran sur une copie temporaire de la ROM finale,
lit les cellules via un lecteur réel de la table et rend trois catégories dans
une msgbox native : Leão-do-mar, Dragão et Pintor. Il vérifie les octets, l'OCR,
la présence des trois images et l'absence d'écriture de sauvegarde, puis produit
la capture dans le répertoire temporaire du système.
L'OCR tolère une seule confusion de glyphe via le comparateur PT-BR existant
(Vision peut lire le D de Dragão comme U, même à pixels identiques). Les octets,
les cellules et la copie Thumb restent comparés exactement, sans cette tolérance.

Validation après intégration PT-52/PT-54/PT-55 : build PT réussi,
43 tests source/intégrité réussis, 15 tests ROM réussis (dont les 166 copies
natives du lot PT-57), 1 test Playwright réussi,
lint Python et vérification TypeScript réussis. La capture est jointe au ticket ;
elle n'est pas enregistrée dans Git.

Non vérifié par cette sonde : navigation manuelle dans les 166 pages du Pokédex
et rendu du suffixe partagé « Pokémon ». Le suffixe et l'ordre d'affichage sont
hors des offsets autorisés ; aucune modification n'est faite à ces éléments.
