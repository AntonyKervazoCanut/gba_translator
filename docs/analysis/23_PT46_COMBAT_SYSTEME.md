# PT-46 — Combat, menus et avertissements système

Le manifeste PT-46 contient exactement 282 clés. Le bilan machine
`languages/pt/data/pt46_audit.json` donne, pour chacune, la comparaison EN/FR,
la préimage binaire complète, tous les pointeurs absolus (scan sans contrainte
 d’alignement), la traduction, ses octets et sa largeur estimée, ou une exception.
La source EN est identifiée par SHA256. F-758 et F-759 sont intégrés.

## Périmètre réel

263 clés disposent de consommateurs directs : messages de combat CFRU,
préfixes et buffers, commandes du menu combat, descriptions des effets Z/Max,
avertissements de configuration et objets de terrain. Les noms sans attestation
PT-BR restent anglais conformément à F-759 ; PS, Habilidade, movimento,
Nocauteado et les types suivent le glossaire. La congeladura CFRU est distincte
du gel classique. Les noms Shadow/Black et les noms de mouvements sont conservés.

Les 19 exceptions sont documentées individuellement dans l’audit. Elles incluent
les suffixes internes 0xa4c000, 0xa4c6fe, 0xa4ca6f, 0xa4cb9e, 0xa4cbb2,
0xa4ccd2, la clé de bourrage 0xa4cdc7 avant le consommateur 0xa4cdc8,
et des variantes sans pointeur absolu. Aucun rendu ni lecteur indirect n’est
revendiqué pour ces clés. Elles ne sont pas ajoutées artificiellement au combined.

Le corpus EN est périmé à 0xa4cb06 : la ROM contient « Acc: », pas « None ».
Les deux avertissements de 759/829 octets sont tronqués dans le corpus EN ;
la traduction reprend leur contenu intégral depuis la ROM. La comparaison FR
est consultative : ses permutations de variables et ses libellés Physique/Spécial
ne remplacent pas les contrôles et les libellés Contact/No Contact de cette source.

## Injection et contrats

Le patch PT `batch_46` réutilise `BorriusTextPatch` et `StructuredTextPatch`.
Il valide toutes les préimages et références avant une écriture atomique,
alloue des chaînes indépendantes, repointe les seuls consommateurs audités,
puis vérifie octets, terminateurs et absence de chevauchement. Il suit les passes
génériques pour éviter qu’une normalisation ne perde un contrôle. Aucune table
fixe indexée n’a été identifiée parmi les 263 clés : les menus ont des pointeurs
littéraux, les textes de combat des pointeurs de scripts ou de tables.

Tous les FD, FC, F8, FA et FB restent dans leur ordre binaire exact. Les espaces
de concaténation sont écrits `<0x00>` car les chargeurs suppriment les espaces
textuels en bordure. Les tabulations FC13 38 du menu gardent leurs paramètres.
Chaque entrée ajoutée possède sa protection exacte dans le même commit.

Les largeurs de l’audit utilisent la métrique partagée (214 pixels maximum,
estimation des buffers dynamiques incluse). Les libellés courts du menu sont
contrôlés séparément dans leur colonne de 56 pixels. Le test ROM mesure aussi les cinq polices avec des surnoms de dix W, leur
préfixe adverse, des classes de Treinador de treize W, des noms de douze W,
des mouvements/objets de douze/treize W et les buffers « Defesa Especial » /
« subiu drasticamente! ». Cette vérification a entraîné 21 ajustements de
lignes ou de formulation. Elle ne remplace pas un parcours exhaustif de toutes
les combinaisons de combat, réservé à la certification T-848.

## Vérification reproductible

- `python3 -m pytest -q tests/unit/pt/test_batch_pt46.py tests/unit/test_translation_integrity.py`
- `make build-pt`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt46_rom.py`
- `npx playwright test --config tests/e2e-playwright/playwright.pt46.config.ts`

La sonde Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen`, vérifie les
textes aux pointeurs de la ROM finale, puis leur rendu par OCR. Elle affiche
l’interdiction de fuite et la course automatique avec ses couleurs dans une
msgbox native sur une copie temporaire. Elle ne prétend pas reproduire un
combat complet ou tous les écrans de configuration. La capture est produite
hors dépôt et attachée au ticket après réussite. Aucun code partagé modifié.
