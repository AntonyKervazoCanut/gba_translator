# PT-32 — Objets, combat et changements de forme

## Périmètre et décisions

F-791 couvre exactement les 288 clés du manifeste PT-32. Le titre provisoire
« Zones Borrius » ne correspond pas au contenu : 119 noms d'objets en cellules
fixes, le nom AKLOV, messages de combat, Repel, échelles et changements de forme.
F-758 et F-759 sont intégrés ; le glossaire reste inchangé.

- 155 textes traduits depuis EN et confrontés à FR au même offset.
- 120 noms conservés selon F-759, ajoutés avec protection exacte. Les 119 noms
  d'objets restent dans leurs cellules de 14 octets, structures espacées de 44
  octets, à partir de la table atteinte par le pointeur 0x9A8D8. Aucune traduction
  ignorée par le constructeur n'est présentée comme une injection de table fixe.
- 13 exceptions laissées intactes : sept fragments graphiques et six copies
  sans référence absolue trouvée. L'absence de pointeur n'est pas présentée comme
  une preuve universelle d'inaccessibilité par calcul d'adresse.

Le bilan exhaustif versionné est
[`pt32_audit.json`](../../languages/pt/data/pt32_audit.json) : ordre du manifeste,
EN et FR, préimage, références brutes et consommateurs retenus, décision, PT,
longueur encodée et largeur de chaque ligne pour chaque offset.

## Injection et garde-fous

Le finaliseur PT réutilise l'injection atomique partagée et contrôle 156 textes
adressés (155 traductions et AKLOV). Il suit leurs pointeurs vivants après toutes
les réparations génériques. La clé 0x8B105B commence par un octet nul ; le vrai
consommateur 0x8B105C est référencé depuis 0x8AD92C. Le remplissage reste intact.

À 0x8AAA77, les motifs 0x43243E et 0xD407AE ressemblent à des pointeurs mais sont
des données graphiques. Seul 0x8AAA4C est un consommateur de texte. Les deux
motifs sont restaurés après le repointage générique et contrôlés avec leurs voisins.

Les adverbes 0x883590/0x8835A0 conservent leur espace final sous la forme explicite
`<0x00>`, sans dépendre du traitement des espaces par les outils intermédiaires.
L'ordre des paramètres FD/FC/F8 et les pages FA/FB sont conservés. Les retours FE
sont redistribués pour le budget, notamment Wide Guard, Quick Guard et Crafty
Shield sur deux lignes. Le dernier nom corrige la coquille EN « Crafty Sheild »
sans inventer de nom portugais.

## Vérification reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_pt32.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt32_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt32.config.ts
```

Les contrôles ROM couvrent préimages, références complètes, table d'objets,
idempotence, atomicité, bornes des écritures, graphismes et texte final. Les
mesures utilisent les vraies polices et des tampons développés (noms de dix W,
préfixe « The opposing », talent/objet de référence « Primordial Sea »), avec
224 pixels en combat. Weakness Policy est également développé pour les deux
messages de hausse d’Attaque et d’Attaque Especial. Ce choix de tampons est une borne testée, pas une exploration
exhaustive de chaque combinaison de noms d'objets/talents à l'exécution.

La preuve Playwright utilise deux msgbox natives, aux pointeurs du build final :
0x8A0B40 (annulation du mouvement de Fogo sous pluie forte) et 0x8AA459 (absence
de réaction au météore). Elle vérifie les octets livrés puis reconnaît et affirme
les deux lignes rendues par mGBA. La copie temporaire ajoute seulement un script
d'appel ; aucun texte ou glyphe n'est remplacé. Aucun navigateur visible, aucune
sauvegarde en jeu. Capture dans le répertoire temporaire de l'OS, jointe au ticket.
Cela ne revendique pas un parcours naturel de tous les combats et changements de
forme, ni une preuve visuelle de toutes les cellules d'objets conservées.

## Exceptions par offset

| Offset | Références | Justification |
|---|---|---|
| `0x883a3a` | Aucune | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x883c3a` | Aucune | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x883e3a` | Aucune | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x88403a` | Aucune | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x8854d0` | Aucune | Aucune référence absolue dans la ROM EN, ni pointeur sur les quatre octets voisins ; copie non adressée laissée intacte, aucune livraison revendiquée. |
| `0x885510` | Aucune | Aucune référence absolue dans la ROM EN, ni pointeur sur les quatre octets voisins ; copie non adressée laissée intacte, aucune livraison revendiquée. Variante adressée à 0xa4c61a, sites : 0xd7b7c, 0xd7ca4, 0xd7d18, 0xd7d8c, 0xd7e00, 0xd7e74, 0xd82c0, 0xd8554, 0x9bd350, 0x9bd67c, 0x9bda0c, 0x9bda30, 0x9bda3c, 0x9bda44. Hors lot, non modifiée. |
| `0x887280` | `0x888480` | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x8883c8` | Aucune | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x88b8bc` | Aucune | Faux texte extrait de tuiles 4bpp (motifs de nibbles/pixels répétés), pas une chaîne ; préserver les données graphiques et leur pointeur. |
| `0x8b8790` | Aucune | Aucune référence absolue dans la ROM EN, ni pointeur sur les quatre octets voisins ; copie non adressée laissée intacte, aucune livraison revendiquée. Variante adressée à 0xa4af59, sites : 0x3fe424. Hors lot, non modifiée. |
| `0x8b9d70` | Aucune | Aucune référence absolue dans la ROM EN, ni pointeur sur les quatre octets voisins ; copie non adressée laissée intacte, aucune livraison revendiquée. Variante adressée à 0x9075e0, sites : 0x90758f. Hors lot, non modifiée. |
| `0x8b9d90` | Aucune | Aucune référence absolue dans la ROM EN, ni pointeur sur les quatre octets voisins ; copie non adressée laissée intacte, aucune livraison revendiquée. |
| `0x8bd155` | Aucune | Aucune référence absolue dans la ROM EN, ni pointeur sur les quatre octets voisins ; copie non adressée laissée intacte, aucune livraison revendiquée. Variante adressée à 0xa4c636, sites : 0xd7b78, 0xd7ca0, 0xd7d14, 0xd7d88, 0xd7dfc, 0xd7e70, 0xd82bc, 0xd8584, 0x9bd354, 0x9bd684, 0x9bda14. Hors lot, non modifiée. |
