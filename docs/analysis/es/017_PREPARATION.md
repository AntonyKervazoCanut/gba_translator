# ES-017 — préparation et prérequis d’acheminement

F-867, 6 novembre 2026. **Lot non livré : aucune traduction ni exclusion finale
certifiée.** Projet gba_translator confirmé par A-663 ; D-849 et F-850 terminés
et intégrés. Aucun combined, protection, glossaire ou contrat de production modifié.

## Relevé exhaustif

`017_PREPARATION.json` conserve les 393 clés ordonnées exactes de `lots.json`,
355 identiques à EN et 38 différentes selon l’inventaire historique. Pour chaque
clé : EN/ES/FR historique, alertes, préimage EN intégrale, commandes complètes et
arguments, occurrences absolues LE32 à tous alignements avec contexte, références
intérieures, débuts voisins et correspondances ES exclusivement depuis l’offset map.
Les empreintes des ROM sources, de la map et des sources préservées sont consignées.

348 clés ont une occurrence binaire directe, 45 n’en ont pas ; 98 préimages ont
une occurrence intérieure. Ces occurrences ne certifient pas automatiquement un
consommateur de texte. Les zones restent à qualifier par les scripts, jamais par
l’adresse. L’absence de pointeur n’est pas une preuve de texte mort.

Le lecteur existant ES-016 est réutilisé avec un paramètre de lot ; aucun changement
au builder, à l’extracteur ou aux contrats partagés d’injection. Reproduction :

```sh
python3 scripts/audit_es016_preparation.py --lot ES-017
python3 scripts/audit_es016_preparation.py --lot ES-017 --probe-routing
python3 -m pytest tests/unit/test_es017_preparation.py tests/unit/test_es016_preparation.py -q
```

Les tailles FC et arguments FD/F8/F9/F7 sont ceux du pipeline courant ; FA/FB sont
conservés séparément et FE représente une nouvelle ligne. Ce relevé reste un
outil de diagnostic : la grammaire de chaque consommateur doit être qualifiée.
Les six gardes unitaires passent, ainsi que Ruff sur les deux fichiers Python touchés.

## Blocage reproduit dans la vraie conversion

25 clés n’ont pas de référence directe au préfixe AA et ont un début à +1 référencé.
Aucun alias actuel ne les couvre. Six débuts sont déjà contractuels dans ce lot :
7A3FD3/7A3FD4, 7A4072/7A4073, 7A7308/7A7309, 7A7E6A/7A7E6B,
7AAB5E/7AAB5F et 7B4787/7B4788. Leur stratégie canonique doit éviter une double
injection. AA n’est pas un chiffre espagnol à importer.

Les 19 autres clés :

| Clé contractuelle | Début référencé | Sites |
|---|---|---|
| 0x0078E7AC | 0x0078E7AD | 0x0078C5C6 |
| 0x0078FA4A | 0x0078FA4B | 0x00745A14 |
| 0x00792D31 | 0x00792D32 | 0x00792346, 0x00792421 |
| 0x00793EDD | 0x00793EDE | 0x00781067 |
| 0x00793F44 | 0x00793F45 | 0x007941A1 |
| 0x00793F7C | 0x00793F7D | 0x007941B6 |
| 0x007A6A12 | 0x007A6A13 | 0x0078E557 |
| 0x007A70F2 | 0x007A70F3 | 0x00793248 |
| 0x007A9F78 | 0x007A9F79 | 0x0075C0DD |
| 0x007AA4DE | 0x007AA4DF | 0x00794212 |
| 0x007AB4FF | 0x007AB500 | 0x0078C625 |
| 0x007B223D | 0x007B223E | 0x0078C7C1 |
| 0x007B2B58 | 0x007B2B59 | 0x007AA976 |
| 0x007B2CF4 | 0x007B2CF5 | 0x007B2CC2 |
| 0x007B3520 | 0x007B3521 | 0x007B2D4F |
| 0x007B3568 | 0x007B3569 | 0x007B2D61 |
| 0x007B3BE9 | 0x007B3BEA | 0x00876B30 |
| 0x007B46B9 | 0x007B46BA | 0x0078BC87, 0x007B452A |
| 0x007B8E39 | 0x007B8E3A | 0x007A2A9D |

Chaque vrai début possède un match ES explicite, sans supposer que les adresses
EN/ES sont égales. Les préimages sont dans `017_ROUTES.json`.
La sonde place temporairement une sentinelle et le texte reconstruit aux 19 clés,
puis appelle le vrai `build_language.generate_translation_json` avec les contrats
actuels. Résultat dans `017_ACHEMINEMENT_REPRO.json` : **19 absences de l’extraction
EN, zéro ligne CSV ajoutée, zéro entrée JSON, zéro route résolue**, sans erreur de
conversion. Aucun combined de production n’est touché ; aucune ROM sentinelle
n’est construite. Un build vert après import ne prouverait donc pas l’injection.

Les prérequis B-1030/B-1032/F-1035/F-1037 et les contrats ES-014/015 ne couvrent
pas ces clés. F-1045 porte exclusivement sur ES-016 ; F-1044 sur ES-013.
Le ticket interdit de modifier l’infrastructure partagée : un prérequis distinct
est nécessaire pour qualifier les 19 consommateurs, leurs budgets et leurs
contrats opt-in, ainsi que la stratégie des six doublons.

## Sources historiques trompeuses et plafond

La ROM EN propre contredit plusieurs descriptions historiques déjà en français :
7B3C6A contient Life Orb (coût en PS), pas une Potion ; 7B3EB0 décrit Quick Ball,
pas Master Ball. Les préimages EN sont reconstruites directement depuis la ROM.
Les descriptions intermédiaires vides dans l’inventaire ont également leur texte
EN intégral dans le relevé. Ne jamais traduire seulement la FR historique.
7B3BE9 préfixe une description lue par 876B30 : le consommateur d’objet et sa
fenêtre doivent être qualifiés, pas traités comme un dialogue par analogie.

Deux sources dépassent 512 octets : 7A9A75 = **1047**, 7AAECA = **648**, FF inclus.
Le relevé ne les tronque pas à 512. Leur pagination et le traitement du plafond
restent à résoudre avant traduction ; aucune phrase inventée pour combler les
troncatures de l’inventaire. 7A9E8F commence par vingt espaces avant 7A9EA3 déjà
contractuel : ne pas l’assimiler au préfixe AA sans qualification.
Les autres fragments (par exemple 78D982, 78DC2B, 7A289C, 7B8908) restent à
reconstruire par leurs consommateurs, et ne sont pas exclus par simple absence
de référence directe.

## Validation et reprise

Les résultats des builds témoins, de la suite standard et des hooks sont consignés
dans le bilan de session ci-dessous. Ils ne certifient aucune traduction ES-017.
Après le prérequis : qualifier les zones/scripts et fragments, relire les 38
différences communautaires, traduire/importer les seuls textes corrects, protéger
chaque valeur exacte et justifier chaque conservation/exclusion. Contrôler toutes
les commandes et arguments, buffers, FA/FB, pages, cellules et pixels ; vérifier
les octets à chaque pointeur vivant. Reconstruire ES et un témoin FR identique,
puis Playwright headless/mGBA offscreen avec assertions et capture attachée.
Aucun affichage n’est modifié par cette préparation ; aucune preuve visuelle de
traduction n’est revendiquée. Aucun push ni pipeline distant.
