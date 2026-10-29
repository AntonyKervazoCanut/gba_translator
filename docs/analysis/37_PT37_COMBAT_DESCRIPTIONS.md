# PT-37 — Habilités, combat et descriptions de mouvements

Le manifeste explicite PT-37 contient 282 offsets : **198 cellules de noms de Habilités**,
**42 messages de combat** et **42 descriptions/libellés de mouvements**.
Les prérequis F-758 et F-759 sont intégrés. Aucun offset étranger au manifeste
n'est ajouté au combined ; son contenu antérieur est conservé octet par octet.

Le bilan exhaustif est [pt37_audit.json](../../languages/pt/data/pt37_audit.json).
Chaque entrée donne la préimage binaire, l'anglais ROM, les références EN/FR
historiques, le statut, la cible PT, les pointeurs et les budgets. **83 textes
sont traduits, 199 valeurs conservées** : 197 noms de talents non attestés
par le glossaire et deux marqueurs `-` réservés (`0xa37487`, cellule de nom
ID 255 ; `0xa37c58`, descriptions de mouvements réservés partagées). Aucune
entrée n'est abandonnée comme morte, vide ou corrompue. Les 282 lignes ont une
protection exacte dans `protected_entries.yaml`.

## Source et consommateurs

`combined_en.txt` n'est pas fiable pour les descriptions de cette plage :
plusieurs valeurs sont françaises ou vides. La ROM anglaise propre, identifiée
par SHA-256 dans l'audit, possède les descriptions anglaises complètes.
Les références FR servent de comparaison, sans imposer leurs formulations.
Les paramètres FD affichés comme `Û`, `Ù`, `Œ` dans l'extraction historique
sont réellement `FD 13`, `FD 11`, `FD 10` : les traductions emploient les codes
binaires explicites, vérifiés contre les préimages. L'ordre des tampons et les
commandes FA/FB sont inchangés.

Les noms sont des cellules fixes de **17 octets**, depuis `0xa36398`, indexées
par ID. Les six littéraux de base sont figés dans l'audit ; les noms additionnels
ont également les pointeurs de la table d'alias `0x9a9bxx`. Le glossaire F-759
impose de conserver ces noms anglais. La ROM finale doit conserver chaque
cellule entière, remplissage compris : aucune relocalisation ni traduction
ignorée n'est revendiquée pour cette table. Un patch de noms supplémentaire
n'est donc pas nécessaire ; les 198 cellules sont contrôlées dans la ROM finale.

Les messages ont des pointeurs de combat directs, certains non alignés : le
scan ne se limite pas aux multiples de quatre. Les descriptions sont atteintes
par la table active `0x99f190`, dont les lecteurs utilisent `0x0899f194` en
`0x0e5440`, `0x137bc8` et `0x9f3b64`. Certaines sont partagées avec les objets
CT ; tous les consommateurs recensés sont conservés et vérifiés.

Le patch `languages/pt/patches/batch_37.py` réutilise l'injecteur borné existant
`BorriusTextPatch` / `StructuredTextPatch`. Il est exécuté après les autres
passes, valide préimages, références, ordre des commandes et budgets avant
écriture, alloue sans écraser les voisins et vérifie chaque pointeur final.
Il est atomique et idempotent. Aucun code partagé n'est modifié.

## Décisions de traduction et budgets

- `Frostbite` est rendu par **congeladura**, une blessure de froid CFRU ; il ne
  devient pas le gel classique. Howl vise l'équipe, Rapid Spin augmente la
  Velocidade, les priorités et récupérations de moitié des dégâts sont conservées.
- Les statistiques suivent le glossaire : Ataque, Defesa, Ataque Especial,
  Defesa Especial, Velocidade, Precisão et PS. Les noms tels que Ice Face et
  Neutralizing Gas restent anglais conformément à la règle des noms non attestés.
- Descriptions : quatre lignes au plus, **118 pixels** au plus par ligne selon
  les métriques versionnées du projet. Messages : **204 pixels**, avec estimation
  des tampons à 54 pixels ; cette estimation n'est pas une preuve pour tous les
  noms adverses possibles. Les commandes FA/FB et l'ordre FD restent exacts.
- Les longueurs encodées, terminateur FF inclus, sont consignées pour chaque
  offset. Les textes à pointeurs peuvent être relocalisés ; la limite fixe de
  17 octets ne s'applique qu'aux noms, conservés exactement.

## Recette de validation locale

```sh
python3 -m pytest tests/unit/pt/test_batch_pt37.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt37_rom.py -q
npx playwright test --config tests/e2e-playwright/playwright.pt37.config.ts
```

La suite ROM compare les préimages et toutes les occurrences de pointeur à la
source identifiée, puis contrôle les 282 valeurs finales et les cellules fixes.
La preuve Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen` et Chromium
headless : deux messages issus de pointeurs vivants sont affichés via une sonde
msgbox ; Ice Beam est affiché dans la vraie Boîte CT sur copie temporaire de la
fiche CT56. La navigation change puis restitue la description, les limites du
panneau et la dernière ligne sont contrôlées. Les captures de preuve sont écrites
dans le répertoire temporaire système, jamais dans le dépôt.

## Non vérifié

Les sondes météo/Habilité n'attestent pas un déclenchement naturel de tous les
42 événements en combat. Le parcours complet, tous les noms runtime possibles,
les autres lots et la promotion du registre restent dans T-848. Aucun push ni
pipeline distant n'est lancé, aucun artefact ROM distribué n'est publié.
