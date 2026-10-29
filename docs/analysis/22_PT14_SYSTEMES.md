# PT-14 — Journal, systèmes, tutoriels, mini-jeux et crédits

Périmètre F-773 : les 282 offsets explicites du manifeste PT-14. F-758 et
F-759 intégrés avant traduction. Aucun offset des autres lots n'est ajouté.

250 entrées référencées : 216 traductions et 34 noms propres/identifiants
ou libellés courts conservés (dont Speed, Sp. Atk/Sp. Def et BERRY CRUSH).
32 exceptions : 28 débuts d'extraction dans le padding, quatre anciennes chaînes
non référencées. L'absence de pointeur seule ne certifie pas l'inaccessibilité de
chaque ancien sous-système : les consommateurs alternatifs sont documentés.

Le fichier `languages/pt/data/pt14_audit.json` donne pour chaque offset : source EN,
comparaison FR, préimage complète, sites de pointeurs, décision, texte PT, taille
encodée et largeurs littérales. Les noms de personnes/lieux et mouvements non attestés
restent anglais selon F-759. Focus Punch n'est pas transformé en Fire Punch ; le
retour à la maison reste distinct du retour au Centre Pokémon.

## Injection et budgets

Aucune cellule du lot n'est une table fixe à stride de caractères. Les tables de
labels et crédits contiennent des pointeurs ; le finaliseur `batch_14` utilise
`StructuredTextPatch` et ne réécrit ni le voisin ni une table hors lot. Les chaînes
sont allouées dans l'espace libre et leurs pointeurs audités mis à jour. Les noms
conservés sont vérifiés sans forcer une nouvelle allocation si déjà exacts.

La coïncidence non alignée 0x15e923d dans les données graphiques est exclue des
consommateurs de 0x41d388 ; le véritable pointeur de crédits est 0x4145fc.
Les préfixes de padding sans pointeur ne sont jamais injectés. Quand leur vraie
cible est hors manifeste, elle est explicitement hors périmètre de ce ticket.

Les commandes FC/FD/F7/F8 et leurs arguments, ainsi que FE/FA/FB, restent dans
l'ordre exact de la ROM. Le tutoriel 0x41be76 est tronqué dans combined_en ; sa
fin est restaurée depuis la préimage ROM complète. Les lignes vides des crédits
et les espaces de concaténation sont conservés. Le plafond `layout.max_width`
du normaliseur porte sur une ligne logique pouvant contenir FA ; la garde ROM
mesure séparément chaque ligne réellement affichée, au plus 224 pixels dans
les cinq polices. Les budgets avec buffers sont testés sur les scénarios indiqués
par les tests, pas présentés comme une exploration exhaustive du jeu.

Speed, Sp. Atk et Sp. Def restent anglais : la fonction native 0x11e7f0
imprime les libellés en police 2 à x=0 et le signe à x=56 (instructions
0x11e89c/0x11e8ce, table via 0x11e930). Les équivalents intégraux
Velocidade/Ataque Especial/Defesa Especial mesurent 57/85/84 pixels. Aucune abréviation PT non prévue par le glossaire n'est inventée.
Le code partagé et les sources FR/IT/DE restent inchangés.

## Vérification reproductible

- `make build-pt`
- `python3 -m pytest tests/unit/pt/test_batch_pt14.py tests/unit/test_translation_integrity.py -q`
- `python3 -m pytest tests/e2e/pt/test_batch_pt14_rom.py -m rom -q`
- `npx playwright test --config tests/e2e-playwright/playwright.pt14.config.ts`

La preuve Playwright utilise le vrai moteur mGBA hors écran, sur copie temporaire,
avec des msgbox pointant vers les chaînes livrées. Elle contrôle octets et OCR.
Elle ne revendique pas un parcours natif complet de pêche, de chat multijoueur,
de journal, de TEACHY TV ou de crédits. Aucune sauvegarde en jeu ni capture suivie.

## Bilan offset par offset

| Offset | Décision | Pointeurs / justification |
|---|---|---|
| `0x41a1e7` | Traduit / contrat vérifié | 0x11405c |
| `0x41a210` | Traduit / contrat vérifié | 0x114070 |
| `0x41a220` | Traduit / contrat vérifié | 0x114098 |
| `0x41a255` | Traduit / contrat vérifié | 0x114148 |
| `0x41a277` | Traduit / contrat vérifié | 0x114114 |
| `0x41a2b0` | Traduit / contrat vérifié | 0x114458 |
| `0x41a2e1` | Traduit / contrat vérifié | 0x115144 |
| `0x41a312` | Traduit / contrat vérifié | 0x115190 |
| `0x41a349` | Traduit / contrat vérifié | 0x1151bc |
| `0x41a391` | Traduit / contrat vérifié | 0x114cbc |
| `0x41a3da` | Traduit / contrat vérifié | 0x114d14 |
| `0x41a3ff` | Traduit / contrat vérifié | 0x1144e8 |
| `0x41a422` | Traduit / contrat vérifié | 0x114574 |
| `0x41a477` | Traduit / contrat vérifié | 0x114600 |
| `0x41a4c6` | Traduit / contrat vérifié | 0x11470c |
| `0x41a506` | Traduit / contrat vérifié | 0x456ae8 |
| `0x41a50b` | Traduit / contrat vérifié | 0x114740 |
| `0x41a53a` | Traduit / contrat vérifié | 0x456bbc |
| `0x41a566` | Traduit / contrat vérifié | 0x114914 |
| `0x41a59c` | Traduit / contrat vérifié | 0x114a9c |
| `0x41a5d9` | Traduit / contrat vérifié | 0x11498c |
| `0x41a5fa` | Traduit / contrat vérifié | 0x114b08 |
| `0x41a60a` | Traduit / contrat vérifié | 0x114a18 |
| `0x41a632` | Traduit / contrat vérifié | 0x114b74 |
| `0x41a64f` | Traduit / contrat vérifié | 0x114be0 |
| `0x41a66e` | Traduit / contrat vérifié | 0x114c64 |
| `0x41a694` | Traduit / contrat vérifié | 0x114c3c |
| `0x41a6a5` | Traduit / contrat vérifié | 0x114284 |
| `0x41a6e1` | Traduit / contrat vérifié | 0x1143ec |
| `0x41a732` | Traduit / contrat vérifié | 0x114774 |
| `0x41a74e` | Traduit / contrat vérifié | 0x456acc |
| `0x41a756` | Traduit / contrat vérifié | 0x456ad0 |
| `0x41a762` | Traduit / contrat vérifié | 0x456ad4, 0x456adc |
| `0x41a76a` | Traduit / contrat vérifié | 0x114804 |
| `0x41a7b0` | Traduit / contrat vérifié | 0x114888 |
| `0x41a7dd` | Traduit / contrat vérifié | 0x11556c |
| `0x41a810` | Traduit / contrat vérifié | 0x1155a0 |
| `0x41a858` | Traduit / contrat vérifié | 0x11568c |
| `0x41a896` | Traduit / contrat vérifié | 0x1156d4 |
| `0x41a8d4` | Traduit / contrat vérifié | 0x115644 |
| `0x41a8e0` | Traduit / contrat vérifié | 0x456c48 |
| `0x41a90c` | Traduit / contrat vérifié | 0x456c44 |
| `0x41a938` | Traduit / contrat vérifié | 0x114130 |
| `0x41a965` | Traduit / contrat vérifié | 0x114100 |
| `0x41a9a9` | Traduit / contrat vérifié | 0x114f44 |
| `0x41a9d4` | Traduit / contrat vérifié | 0x114f58 |
| `0x41aa01` | Traduit / contrat vérifié | 0x114f14 |
| `0x41aa2b` | Traduit / contrat vérifié | 0x114f28 |
| `0x41aa76` | Traduit / contrat vérifié | 0x114f74 |
| `0x41aaaa` | Traduit / contrat vérifié | 0x114f88 |
| `0x41aaec` | Traduit / contrat vérifié | 0x114fa0 |
| `0x41ab29` | Traduit / contrat vérifié | 0x114fb8 |
| `0x41ab74` | Traduit / contrat vérifié | 0x1141cc |
| `0x41ab8e` | Traduit / contrat vérifié | 0x114228 |
| `0x41abab` | Traduit / contrat vérifié | 0x456c24 |
| `0x41abcd` | Traduit / contrat vérifié | 0x456c28 |
| `0x41abf9` | Traduit / contrat vérifié | 0x456c30 |
| `0x41ac2a` | Traduit / contrat vérifié | 0x456c2c |
| `0x41ac51` | Traduit / contrat vérifié | 0x456c20 |
| `0x41ac93` | Traduit / contrat vérifié | 0x456c34 |
| `0x41acbc` | Traduit / contrat vérifié | 0x456c38 |
| `0x41ad1d` | Traduit / contrat vérifié | 0x456c40 |
| `0x41ad3c` | Traduit / contrat vérifié | 0x456c4c |
| `0x41ad69` | Traduit / contrat vérifié | 0x456c3c |
| `0x41ad9e` | Traduit / contrat vérifié | 0x456bc0 |
| `0x41adc8` | Traduit / contrat vérifié | 0x456bc4 |
| `0x41adff` | Traduit / contrat vérifié | 0x456bc8 |
| `0x41ae1e` | Traduit / contrat vérifié | 0x456bcc |
| `0x41ae48` | Traduit / contrat vérifié | 0x115330, 0x456bd0 |
| `0x41ae8f` | Traduit / contrat vérifié | 0x115374 |
| `0x41aea7` | Traduit / contrat vérifié | 0x456bd4 |
| `0x41aedc` | Traduit / contrat vérifié | 0x456bd8 |
| `0x41af0c` | Traduit / contrat vérifié | 0x114de4 |
| `0x41af3e` | Traduit / contrat vérifié | 0x115074 |
| `0x41af6d` | Traduit / contrat vérifié | 0x11527c |
| `0x41af98` | Traduit / contrat vérifié | 0x456ad8 |
| `0x41af9f` | Traduit / contrat vérifié | 0x456ae0 |
| `0x41afa6` | Traduit / contrat vérifié | 0x114030 |
| `0x41afd1` | Traduit / contrat vérifié | 0x456aec |
| `0x41afd6` | Traduit / contrat vérifié | 0x456bdc |
| `0x41b005` | Traduit / contrat vérifié | 0x456be0 |
| `0x41b03f` | Traduit / contrat vérifié | 0x115744 |
| `0x41b064` | Traduit / contrat vérifié | 0x115830 |
| `0x41b073` | Traduit / contrat vérifié | 0x11203c |
| `0x41b09f` | Traduit / contrat vérifié | 0x1154a8, 0x456af0 |
| `0x41b0a4` | Nom conservé / octets vérifiés | 0x456af4 |
| `0x41b0b9` | Nom conservé / octets vérifiés | 0x456afc, 0x456b00 |
| `0x41b0cd` | Nom conservé / octets vérifiés | 0x456b04, 0x456b08 |
| `0x41b0dd` | Nom conservé / octets vérifiés | 0x456b0c |
| `0x41b0f6` | Nom conservé / octets vérifiés | 0x456b14, 0x456b18 |
| `0x41b0ff` | Traduit / contrat vérifié | 0x456b20 |
| `0x41b109` | Nom conservé / octets vérifiés | 0x456b24 |
| `0x41b116` | Traduit / contrat vérifié | 0x456b28 |
| `0x41b11f` | Nom conservé / octets vérifiés | 0x456b2c, 0x456b30, 0x456b60, 0x456b64 |
| `0x41b130` | Traduit / contrat vérifié | 0x456b34 |
| `0x41b141` | Nom conservé / octets vérifiés | 0x456b3c |
| `0x41b14b` | Nom conservé / octets vérifiés | 0x456b40, 0x456b44 |
| `0x41b15a` | Nom conservé / octets vérifiés | 0x456b48, 0x456b4c |
| `0x41b166` | Traduit / contrat vérifié | 0x456b50 |
| `0x41b172` | Nom conservé / octets vérifiés | 0x456b54 |
| `0x41b180` | Traduit / contrat vérifié | 0x456b58 |
| `0x41b190` | Traduit / contrat vérifié | 0x456b5c |
| `0x41b1a3` | Nom conservé / octets vérifiés | 0x456b68 |
| `0x41b1b7` | Nom conservé / octets vérifiés | 0x456b6c |
| `0x41b1c7` | Nom conservé / octets vérifiés | 0x456b70 |
| `0x41b1da` | Traduit / contrat vérifié | 0x456b78 |
| `0x41b1e5` | Nom conservé / octets vérifiés | 0x456b7c |
| `0x41b1f4` | Nom conservé / octets vérifiés | 0x456b80 |
| `0x41b200` | Traduit / contrat vérifié | 0x456b88 |
| `0x41b20e` | Traduit / contrat vérifié | 0x456b8c |
| `0x41b21c` | Nom conservé / octets vérifiés | 0x456b94 |
| `0x41b226` | Nom conservé / octets vérifiés | 0x456b98, 0x456b9c |
| `0x41b236` | Nom conservé / octets vérifiés | 0x456ba0 |
| `0x41b246` | Traduit / contrat vérifié | 0x456ba8 |
| `0x41b25b` | Nom conservé / octets vérifiés | 0x456bac, 0x456bb0 |
| `0x41b268` | Traduit / contrat vérifié | 0x456bb4 |
| `0x41b277` | Nom conservé / octets vérifiés | 0x456bb8 |
| `0x41b285` | Traduit / contrat vérifié | 0x11d384 |
| `0x41b295` | Traduit / contrat vérifié | 0x11d3d4 |
| `0x41b2a9` | Traduit / contrat vérifié | 0x459b48 |
| `0x41b2b7` | Traduit / contrat vérifié | 0x459b4c, 0x8c1011, 0x8c9821 |
| `0x41b2be` | Traduit / contrat vérifié | 0x459b50, 0x8c1026, 0x8c9836 |
| `0x41b2c6` | Nom conservé / octets vérifiés | 0x459b5c, 0x8c103b, 0x8c984b |
| `0x41b2cc` | Nom conservé / octets vérifiés | 0x459b54, 0x8c1050, 0x8c9860 |
| `0x41b2d4` | Nom conservé / octets vérifiés | 0x459b58, 0x8c1065, 0x8c9875 |
| `0x41b2f1` | Traduit / contrat vérifié | 0x11d444, 0x45999c |
| `0x41b2ff` | Traduit / contrat vérifié | 0x4599a0 |
| `0x41b306` | Traduit / contrat vérifié | 0x11d478 |
| `0x41b31b` | Traduit / contrat vérifié | 0x11d494 |
| `0x41b32e` | Traduit / contrat vérifié | 0x11d400 |
| `0x41b33d` | Traduit / contrat vérifié | 0x45abec |
| `0x41b343` | Traduit / contrat vérifié | 0x45abf4 |
| `0x41b349` | Exception justifiée | Ancien onglet OtherS sans pointeur ; table chat utilise SYMBOLS à 0x45abfc. Cible 0x41b350 via 0x45abfc. |
| `0x41b350` | Traduit / contrat vérifié | 0x45abfc |
| `0x41b358` | Traduit / contrat vérifié | 0x45ac04 |
| `0x41b361` | Traduit / contrat vérifié | 0x45ac0c |
| `0x41b366` | Traduit / contrat vérifié | 0x45ab64 |
| `0x41b375` | Traduit / contrat vérifié | 0x45ab70 |
| `0x41b38a` | Traduit / contrat vérifié | 0x45ab7c |
| `0x41b39e` | Traduit / contrat vérifié | 0x45ab88 |
| `0x41b3aa` | Traduit / contrat vérifié | 0x129684 |
| `0x41b3be` | Traduit / contrat vérifié | 0x1296e8 |
| `0x41b3e9` | Traduit / contrat vérifié | 0x45ab94 |
| `0x41b3fb` | Traduit / contrat vérifié | 0x45aba0 |
| `0x41b426` | Traduit / contrat vérifié | 0x45abac |
| `0x41b469` | Traduit / contrat vérifié | 0x45abb8 |
| `0x41b4a4` | Traduit / contrat vérifié | 0x45abc4 |
| `0x41b4c6` | Traduit / contrat vérifié | 0x45abd0 |
| `0x41b4d9` | Traduit / contrat vérifié | 0x45abdc |
| `0x41b510` | Traduit / contrat vérifié | 0x1298ac |
| `0x41b516` | Nom conservé / octets vérifiés | 0x1298b4 |
| `0x41b51e` | Traduit / contrat vérifié | 0x1298bc |
| `0x41b524` | Traduit / contrat vérifié | 0x1298c4 |
| `0x41b52b` | Traduit / contrat vérifié | 0x1298cc |
| `0x41b535` | Traduit / contrat vérifié | 0x1298dc |
| `0x41b541` | Traduit / contrat vérifié | 0x1298ec |
| `0x41b54b` | Traduit / contrat vérifié | 0x1298f4 |
| `0x41b554` | Traduit / contrat vérifié | 0x7f53c, 0x88345c, 0x1ec2244 |
| `0x41b5b6` | Traduit / contrat vérifié | 0x7f578, 0x883460, 0x9fff8c, 0x1ec2274 |
| `0x41b60e` | Traduit / contrat vérifié | 0xf50e4, 0x8b43d0 |
| `0x41b619` | Traduit / contrat vérifié | 0xf50ec, 0x8b4410 |
| `0x41b684` | Nom conservé / octets vérifiés | 0xf50f0, 0x8b444c |
| `0x41b68f` | Traduit / contrat vérifié | 0xf5044 |
| `0x41b698` | Exception justifiée | Ancien label Kanto sans pointeur ; diplôme choisit National via 0xf5044. Cible 0x41b68f via 0xf5044. |
| `0x41b69e` | Traduit / contrat vérifié | 0xf5698 |
| `0x41b6b9` | Traduit / contrat vérifié | 0xf5788 |
| `0x41b6d5` | Traduit / contrat vérifié | 0xcecc |
| `0x41b6dc` | Traduit / contrat vérifié | 0xcf34 |
| `0x41b6e3` | Nom conservé / octets vérifiés | 0xcfbc |
| `0x41b6ec` | Traduit / contrat vérifié | 0xd03c |
| `0x41b6f4` | Traduit / contrat vérifié | 0x456e3c, 0x45a690, 0x820768, 0xa6ca94 |
| `0x41b6fd` | Traduit / contrat vérifié | 0x474e0 |
| `0x41b716` | Traduit / contrat vérifié | 0x47544 |
| `0x41b747` | Traduit / contrat vérifié | 0x1415ac |
| `0x41b76b` | Traduit / contrat vérifié | 0x1415f4 |
| `0x41b779` | Traduit / contrat vérifié | 0x1413d8 |
| `0x41b7a4` | Traduit / contrat vérifié | 0x479308, 0x479340 |
| `0x41b7bc` | Traduit / contrat vérifié | 0x479310, 0x479348 |
| `0x41b7d6` | Traduit / contrat vérifié | 0x479318, 0x479350 |
| `0x41b7ee` | Traduit / contrat vérifié | 0x479320, 0x479358 |
| `0x41b807` | Traduit / contrat vérifié | 0x479328 |
| `0x41b81b` | Traduit / contrat vérifié | 0x479330 |
| `0x41b836` | Traduit / contrat vérifié | 0x479338, 0x479360 |
| `0x41b83d` | Traduit / contrat vérifié | 0x15b4b0 |
| `0x41b8bf` | Traduit / contrat vérifié | 0x479560 |
| `0x41ba41` | Traduit / contrat vérifié | 0x479578 |
| `0x41bb40` | Traduit / contrat vérifié | 0x479564 |
| `0x41bd10` | Traduit / contrat vérifié | 0x47957c |
| `0x41be76` | Traduit / contrat vérifié | 0x479568 |
| `0x41c0af` | Traduit / contrat vérifié | 0x479580 |
| `0x41c23b` | Traduit / contrat vérifié | 0x47956c |
| `0x41c384` | Traduit / contrat vérifié | 0x479584 |
| `0x41c459` | Traduit / contrat vérifié | 0x479570 |
| `0x41c587` | Traduit / contrat vérifié | 0x1330d4 |
| `0x41c693` | Traduit / contrat vérifié | 0x133150 |
| `0x41c7b4` | Traduit / contrat vérifié | 0x479588 |
| `0x41c82a` | Traduit / contrat vérifié | 0x479574 |
| `0x41c994` | Traduit / contrat vérifié | 0x47958c |
| `0x41cb3c` | Nom conservé / octets vérifiés | 0x13c1e0 |
| `0x41cb41` | Traduit / contrat vérifié | 0x13c1d8 |
| `0x41cb49` | Traduit / contrat vérifié | 0x13ba08 |
| `0x41cb52` | Traduit / contrat vérifié | 0x14a8b0 |
| `0x41cb5a` | Traduit / contrat vérifié | 0x14a8b4 |
| `0x41cb63` | Traduit / contrat vérifié | 0x14b6cc |
| `0x41cb78` | Traduit / contrat vérifié | 0x46e2d4 |
| `0x41cb88` | Traduit / contrat vérifié | 0x46e2d8 |
| `0x41cb94` | Traduit / contrat vérifié | 0x46e2dc |
| `0x41cba9` | Traduit / contrat vérifié | 0x14a534 |
| `0x41cbca` | Traduit / contrat vérifié | 0x14a5b0 |
| `0x41cbe4` | Traduit / contrat vérifié | 0x14a628 |
| `0x41cbfd` | Traduit / contrat vérifié | 0x14a120 |
| `0x41cc11` | Traduit / contrat vérifié | 0x14a2bc |
| `0x41cc42` | Traduit / contrat vérifié | 0x14a1cc |
| `0x41cc64` | Traduit / contrat vérifié | 0x14a360 |
| `0x41cc7b` | Exception justifiée | Ancienne copie SAVING sans pointeur ; mini-jeu utilise 0x41cc42 via 0x14a1cc. Cible 0x41cc42 via 0x14a1cc. |
| `0x41cc9f` | Traduit / contrat vérifié | 0x4755e8 |
| `0x41ccbc` | Traduit / contrat vérifié | 0x4755ec |
| `0x41cccc` | Traduit / contrat vérifié | 0x4755f0 |
| `0x41ccd8` | Traduit / contrat vérifié | 0x4755f4 |
| `0x41cd03` | Traduit / contrat vérifié | 0x1551b4 |
| `0x41cd43` | Traduit / contrat vérifié | 0x15533c |
| `0x41cd58` | Traduit / contrat vérifié | 0x155568 |
| `0x41cd7a` | Traduit / contrat vérifié | 0x15556c |
| `0x41cd9f` | Traduit / contrat vérifié | 0x155570 |
| `0x41cdba` | Traduit / contrat vérifié | 0x1555c4 |
| `0x41cdd7` | Traduit / contrat vérifié | 0x155854 |
| `0x41cdeb` | Traduit / contrat vérifié | 0x155d48 |
| `0x41ce1c` | Traduit / contrat vérifié | 0x154f68 |
| `0x41ce24` | Traduit / contrat vérifié | 0x155be4 |
| `0x41ce3b` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41ce3c via 0x46e328. |
| `0x41ce3c` | Traduit / contrat vérifié | 0x46e328 |
| `0x41ce78` | Traduit / contrat vérifié | 0x46e32c |
| `0x41cea7` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41cea8 via 0x46e330. |
| `0x41cea8` | Traduit / contrat vérifié | 0x46e330 |
| `0x41cf13` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41cf14 via 0x46e334. |
| `0x41cf14` | Traduit / contrat vérifié | 0x46e334 |
| `0x41cf4f` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41cf50 via 0x46e338. |
| `0x41cf50` | Traduit / contrat vérifié | 0x46e338 |
| `0x41cf70` | Traduit / contrat vérifié | 0x46e33c |
| `0x41cfa0` | Traduit / contrat vérifié | 0x46e340 |
| `0x41cfd1` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41cfd4 via 0x46e344. |
| `0x41d005` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d008 via 0x46e348. |
| `0x41d032` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d034 via 0x46f4b8. |
| `0x41d042` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d044 via 0x46f4c0. |
| `0x41d04d` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d050 via 0x14e564. |
| `0x41d056` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d058 via 0x14e584. |
| `0x41d068` | Traduit / contrat vérifié | 0x14e634 |
| `0x41d096` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d098 via 0x14e588, 0x14ea28. |
| `0x41d0a8` | Traduit / contrat vérifié | 0x14e75c |
| `0x41d0c0` | Traduit / contrat vérifié | 0x14e7d4 |
| `0x41d0d1` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d0d4 via 0x46f4c4. |
| `0x41d0e6` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d0e8 via 0x46f4c8. |
| `0x41d0fd` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d100 via 0x46f4cc. |
| `0x41d118` | Nom conservé / octets vérifiés | 0x14e9fc |
| `0x41d124` | Traduit / contrat vérifié | 0x14ea04 |
| `0x41d13c` | Traduit / contrat vérifié | 0x14ea10 |
| `0x41d147` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d148 via 0x44940, 0x7f864, 0x7f994. |
| `0x41d14e` | Traduit / contrat vérifié | 0x5d6c4 |
| `0x41d169` | Traduit / contrat vérifié | 0x5d834 |
| `0x41d17e` | Traduit / contrat vérifié | 0x5d8a8 |
| `0x41d18d` | Traduit / contrat vérifié | 0x984a0 |
| `0x41d195` | Exception justifiée | Ancienne dédicace sans pointeur ; table des crédits commence par Creator à 0x41d1d8 via 0x4145bc, hors lot. Cible 0x41d1d8 via 0x4145bc. |
| `0x41d1fd` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d200 via 0x4145c8. |
| `0x41d222` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d224 via 0x4145cc. |
| `0x41d247` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d248 via 0x4145d4. |
| `0x41d281` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d284 via 0x4145d8. |
| `0x41d2c5` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d2c8 via 0x4145e4. |
| `0x41d312` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d314 via 0x4145ec. |
| `0x41d32d` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d330 via 0x4145f0. |
| `0x41d36d` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d370 via 0x4145f8. |
| `0x41d388` | Nom conservé / octets vérifiés | 0x4145fc |
| `0x41d3be` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d3c0 via 0x414604. |
| `0x41d3d8` | Nom conservé / octets vérifiés | 0x414608 |
| `0x41d3fb` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d3fc via 0x414610. |
| `0x41d414` | Nom conservé / octets vérifiés | 0x414614 |
| `0x41d434` | Traduit / contrat vérifié | 0x41461c |
| `0x41d448` | Nom conservé / octets vérifiés | 0x414620 |
| `0x41d471` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d474 via 0x41462c. |
| `0x41d4b9` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d4bc via 0x414638. |
| `0x41d504` | Nom conservé / octets vérifiés | 0x414644 |
| `0x41d524` | Traduit / contrat vérifié | 0x41464c |
| `0x41d546` | Exception justifiée | Offset extrait dans le padding, sans pointeur. Le consommateur vise la cible indiquée dans replacement ; cible traduite seulement si présente dans PT-14, sinon hors périmètre. Cible 0x41d548 via 0x414650. |
