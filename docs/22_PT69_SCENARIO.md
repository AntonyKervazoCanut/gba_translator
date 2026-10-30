# PT-69 — Magnolia et scénario des Shadows

F-828 ; prérequis F-758/F-759 intégrés. Manifeste fermé de 300 offsets :
273 traductions, 20 valeurs anglaises conservées et 7 exceptions justifiées.
Aucun offset d’un autre lot ajouté au combined ; aucune traduction antérieure supprimée.
L’audit `languages/pt/data/pt69_audit.json` contient anglais ROM intégral, comparaison FR,
préimages, lecteurs, octets et mesures dans les cinq polices avec tampons développés.
SHA256 EN : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

## Zones et consommateurs

Magnolia Town : ferme, lait, quiz, café. Puis entrepôt des Shadows, choix du Pokémon,
rival et Professor Log, colis/Articuno, Arthur/Jax et capture de Moltres à Cinder Volcano.

Les dix réponses sont lues dans la table pointeurs 0x1fb583c. Le normaliseur 0x1ec9a40
ne transforme que A–Z ; `agua` est volontairement sans accent pour le clavier.
Espèces, noms propres Borrius, mouvements et objets sans équivalent attesté restent anglais.
PS et Poção respectent F-759.

Les fragments du café sont concaténés par 0x1ebb414 : espaces initial et finaux explicites
(`<0x00>`) pour résister au chargement. La routine 0x1ebb914 ajoutait un possessif anglais :
une immédiate et un littéral sont adaptés pour produire `Nom: ` dans les deux branches.
Les tests mesurent aussi les textes développés, pas seulement leurs fragments.

Quatre appels de helpers sont adaptés localement : le helper original s’exécute puis
un seul tampon est vidé pour une phrase neutre portée par le combined. Aucun helper
partagé ni chaîne des lots PT-71/PT-75 n’est traduit ici. Les pronoms ele/ela de PT-22
restent utilisés ; la phrase réflexive ne conserve pas le suffixe anglais `self`.

0x1f2ecd5 et 0x1f30c2d sont traduits intégralement depuis la ROM, au-delà des troncatures
EN. Trois faux pointeurs PCM et un match chevauchant deux littéraux Thumb sont exclus
et restaurés après l’injecteur générique ; préimages/en-têtes/instruments sont audités.
Aucune cellule texte fixe brute dans ce lot : tables, noms de classes étendus et fragments
sont lus par pointeurs. La passe finale dédiée `batch_69` livre les 293 consommateurs.

## Vérification reproductible

```sh
python3 scripts/check_translation_integrity.py --lang pt
python3 -m pytest tests/unit/pt/test_batch_pt69.py
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt69_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt69.config.ts
```

Playwright lance mGBA hors écran sur une copie temporaire de ROM, contrôle trois vrais
msgbox par OCR et le tampon local d’Arthur. Aucune sauvegarde en jeu. La capture reste
dans le dossier temporaire de l’OS puis est jointe au ticket, jamais versionnée.

## Non vérifié

La navigation naturelle complète dans les 300 offsets n’est pas automatisée. La sonde
msgbox ne certifie pas le parcours des zones ; toutes les pages et tous les lecteurs
sont vérifiés en binaire. Le registre reste in_progress, certification globale T-848.

## Bilan par offset

| Offset | Décision | Pointeurs texte source / justification | Octets PT | Pixels max |
|---|---|---|---:|---:|
| `0x1f2b5f0` | Traduit/vérifié | 0x1e7cb78 | 214 | 175 |
| `0x1f2b6d6` | Traduit/vérifié | 0x1e7cbbd | 96 | 150 |
| `0x1f2b747` | Traduit/vérifié | 0x1e7cbc6 | 95 | 166 |
| `0x1f2b7ad` | Traduit/vérifié | 0x1e7cbeb, 0x1e7cc1e, 0x1eaba1d | 12 | 48 |
| `0x1f2b7b9` | Traduit/vérifié | 0x1e7cbfa, 0x1e7cc2d | 23 | 155 |
| `0x1f2b7d0` | Conservé/vérifié | 0x1e7cfd4, 0x1e7d010, 0x1e7d0b3, 0x1e7d121, 0x1e7d137, 0x1e7d1f0, 0x1e7d2bd, 0x1e7d352, 0x1e7d3f8 | 4 | 18 |
| `0x1f2b7d4` | Conservé/vérifié | 0x1e7d033, 0x1e7d07a, 0x1e7d094, 0x1e7d0fd, 0x1e7d15a, 0x1e7d170, 0x1e7d1c2, 0x1e7d23a, 0x1e7d293, 0x1e7d307, 0x1e7d3dc | 4 | 18 |
| `0x1f2b7d8` | Conservé/vérifié | 0x1e7d05a, 0x1e7d0dd, 0x1e7d21a, 0x1e7d2e7, 0x1e7d410 | 6 | 27 |
| `0x1f2b7de` | Traduit/vérifié | 0x1e7cfdf | 31 | 131 |
| `0x1f2b7fa` | Traduit/vérifié | 0x1e7d01b | 87 | 190 |
| `0x1f2b858` | Traduit/vérifié | 0x1e7d03e | 141 | 188 |
| `0x1f2b8e4` | Traduit/vérifié | 0x1e7d065 | 14 | 57 |
| `0x1f2b8f2` | Traduit/vérifié | 0x1e7d085 | 17 | 75 |
| `0x1f2b901` | Traduit/vérifié | 0x1e7d0be | 62 | 165 |
| `0x1f2b949` | Traduit/vérifié | 0x1e7d0e8 | 21 | 98 |
| `0x1f2b95e` | Traduit/vérifié | 0x1e7d108 | 41 | 125 |
| `0x1f2b98b` | Traduit/vérifié | 0x1e7d12c | 28 | 99 |
| `0x1f2b9aa` | Traduit/vérifié | 0x1e7d165 | 43 | 133 |
| `0x1f2b9e4` | Traduit/vérifié | 0x1e7d1cd | 30 | 109 |
| `0x1f2ba07` | Traduit/vérifié | 0x1e7d1fb | 25 | 121 |
| `0x1f2ba20` | Traduit/vérifié | 0x1e7d225 | 26 | 126 |
| `0x1f2ba3c` | Traduit/vérifié | 0x1e7d245 | 52 | 117 |
| `0x1f2ba7a` | Traduit/vérifié | 0x1e7d29e | 57 | 156 |
| `0x1f2bab6` | Traduit/vérifié | 0x1e7d2c8 | 25 | 114 |
| `0x1f2bac7` | Traduit/vérifié | 0x1e7d2f2 | 28 | 74 |
| `0x1f2bae7` | Traduit/vérifié | 0x1e7d312 | 71 | 157 |
| `0x1f2bb31` | Traduit/vérifié | 0x1e7d35d | 70 | 171 |
| `0x1f2bb7e` | Traduit/vérifié | 0x1e7d3e7 | 33 | 183 |
| `0x1f2bb96` | Traduit/vérifié | 0x1e7d403 | 27 | 151 |
| `0x1f2bbaf` | Traduit/vérifié | 0x1e7d41b | 14 | 76 |
| `0x1f2bbbf` | Traduit/vérifié | 0x1fb57ec | 58 | 157 |
| `0x1f2bbee` | Traduit/vérifié | 0x1fb57f0 | 64 | 191 |
| `0x1f2bc2a` | Traduit/vérifié | 0x1fb57f4 | 40 | 165 |
| `0x1f2bc57` | Traduit/vérifié | 0x1fb57f8 | 70 | 159 |
| `0x1f2bca2` | Traduit/vérifié | 0x1fb57fc | 63 | 179 |
| `0x1f2bcdd` | Traduit/vérifié | 0x1fb5800 | 39 | 150 |
| `0x1f2bd08` | Traduit/vérifié | 0x1fb5804 | 46 | 165 |
| `0x1f2bd3c` | Traduit/vérifié | 0x1fb5808 | 71 | 188 |
| `0x1f2bd80` | Traduit/vérifié | 0x1fb580c | 62 | 181 |
| `0x1f2bdbc` | Traduit/vérifié | 0x1fb5810 | 33 | 165 |
| `0x1f2bdda` | Traduit/vérifié | 0x1fb5814 | 54 | 174 |
| `0x1f2be0d` | Traduit/vérifié | 0x1fb5818 | 40 | 173 |
| `0x1f2be37` | Traduit/vérifié | 0x1fb581c | 27 | 98 |
| `0x1f2be59` | Traduit/vérifié | 0x1fb5820 | 41 | 180 |
| `0x1f2be82` | Traduit/vérifié | 0x1fb5824 | 25 | 88 |
| `0x1f2be99` | Traduit/vérifié | 0x1fb5828 | 31 | 119 |
| `0x1f2beb5` | Traduit/vérifié | 0x1fb582c | 30 | 116 |
| `0x1f2bed0` | Traduit/vérifié | 0x1fb5830 | 35 | 142 |
| `0x1f2bef8` | Traduit/vérifié | 0x1fb5834 | 26 | 93 |
| `0x1f2bf16` | Traduit/vérifié | 0x1fb5838 | 25 | 88 |
| `0x1f2bf32` | Traduit/vérifié | 0x1fb583c | 6 | 29 |
| `0x1f2bf39` | Conservé/vérifié | 0x1fb5840 | 10 | 50 |
| `0x1f2bf43` | Traduit/vérifié | 0x1fb5844 | 5 | 24 |
| `0x1f2bf49` | Conservé/vérifié | 0x1fb5848 | 8 | 37 |
| `0x1f2bf51` | Traduit/vérifié | 0x1fb584c | 6 | 29 |
| `0x1f2bf57` | Traduit/vérifié | 0x1fb5850 | 7 | 34 |
| `0x1f2bf5d` | Traduit/vérifié | 0x1fb5854 | 9 | 43 |
| `0x1f2bf63` | Conservé/vérifié | 0x1fb5858 | 5 | 22 |
| `0x1f2bf68` | Traduit/vérifié | 0x1fb585c | 9 | 45 |
| `0x1f2bf6e` | Conservé/vérifié | 0x1fb5860 | 6 | 27 |
| `0x1f2bf74` | Traduit/vérifié | 0x1e7d42b | 102 | 174 |
| `0x1f2bff8` | Traduit/vérifié | 0x1e6a335, 0x1e6a38b, 0x1e7d498, 0x1e7d4ee | 29 | 98 |
| `0x1f2c016` | Traduit/vérifié | 0x1e7d4be | 10 | 56 |
| `0x1f2c02b` | Traduit/vérifié | 0x1e7d514 | 11 | 62 |
| `0x1f2c041` | Traduit/vérifié | 0x1e6a314, 0x1e7d477 | 29 | 101 |
| `0x1f2c066` | Traduit/vérifié | 0x1e6a3d4, 0x1e7d537 | 50 | 142 |
| `0x1f2c0a0` | Traduit/vérifié | 0x1e6a2d4, 0x1e7d437 | 10 | 51 |
| `0x1f2c0a9` | Traduit/vérifié | 0x1e6a2e2, 0x1e7d445 | 8 | 40 |
| `0x1f2c0b1` | Traduit/vérifié | 0x1e7ccb8 | 47 | 176 |
| `0x1f2c0e7` | Traduit/vérifié | 0x1e7ccda | 135 | 180 |
| `0x1f2c171` | Traduit/vérifié | 0x1e7cc9c | 184 | 161 |
| `0x1f2c240` | Traduit/vérifié | 0x1e7cca6 | 176 | 187 |
| `0x1f2c30c` | Traduit/vérifié | 0x1e7cd19 | 22 | 115 |
| `0x1f2c324` | Traduit/vérifié | 0x1e7cd4b | 80 | 164 |
| `0x1f2c383` | Traduit/vérifié | 0x1e7cedc | 50 | 150 |
| `0x1f2c3c4` | Traduit/vérifié | 0x1e7cd6f | 63 | 163 |
| `0x1f2c418` | Traduit/vérifié | 0x1e7cf26 | 47 | 122 |
| `0x1f2c45f` | Traduit/vérifié | 0x1e7cf15 | 53 | 149 |
| `0x1f2c4a5` | Traduit/vérifié | 0x1e7cdb0 | 58 | 143 |
| `0x1f2c4f1` | Traduit/vérifié | 0x1e7cdc3 | 33 | 184 |
| `0x1f2c516` | Traduit/vérifié | 0x1e7cdf0 | 49 | 149 |
| `0x1f2c555` | Traduit/vérifié | 0x1e7ce07 | 9 | 67 |
| `0x1f2c565` | Traduit/vérifié | 0x1e7ce21 | 38 | 138 |
| `0x1f2c58d` | Traduit/vérifié | 0x1e7ce55 | 26 | 69 |
| `0x1f2c5a1` | Traduit/vérifié | 0x1e7ce64 | 42 | 155 |
| `0x1f2c5c6` | Traduit/vérifié | 0x1e7ce8b | 14 | 74 |
| `0x1f2c5da` | Traduit/vérifié | 0x1e7cef4 | 47 | 181 |
| `0x1f2c605` | Traduit/vérifié | 0x1e7cf00, 0x1e7cf09 | 24 | 74 |
| `0x1f2c629` | Traduit/vérifié | 0x1e7cf33 | 89 | 204 |
| `0x1f2c693` | Traduit/vérifié | 0x1e7cf43 | 73 | 142 |
| `0x1f2c6dc` | Traduit/vérifié | 0x1ebb530 | 26 | 100 |
| `0x1f2c6fd` | Traduit/vérifié | 0x1ebb514 | 12 | 55 |
| `0x1f2c709` | Traduit/vérifié | 0x1ebb518 | 10 | 51 |
| `0x1f2c715` | Traduit/vérifié | 0x1ebb51c | 9 | 46 |
| `0x1f2c723` | Traduit/vérifié | 0x1e7d559 | 262 | 178 |
| `0x1f2c84b` | Traduit/vérifié | 0x1e7d563 | 181 | 186 |
| `0x1f2c8f8` | Traduit/vérifié | 0x1e7d576 | 110 | 181 |
| `0x1f2c962` | Traduit/vérifié | 0x1e7d599 | 143 | 192 |
| `0x1f2c9fe` | Traduit/vérifié | 0x1e7d5a3 | 98 | 170 |
| `0x1f2ca6d` | Traduit/vérifié | 0x1e7d5b1 | 124 | 173 |
| `0x1f2caef` | Conservé/vérifié | 0x1e67fa5, 0x1e67fe5, 0x1e68042, 0x1e68087, 0x1e680b4, 0x1e680f9, 0x1e68112, 0x1e684ea, 0x1e68608, 0x1e6d6f5, 0x1e6d71b, 0x1e6d82d, 0x1e6d86d, 0x1e6d938, 0x1e6d978, 0x1e6d9e0, 0x1e6da12, 0x1e6da3e, 0x1e6da73, 0x1e6da95, 0x1e6dbe9, 0x1e6dc1d, 0x1e79c0b, 0x1e79c22, 0x1e79c39, 0x1e79c50, 0x1e79c67, 0x1e79c7e, 0x1e79c95, 0x1e79cc2, 0x1e79ceb, 0x1e79d02, 0x1e79d1e, 0x1e79d3c, 0x1e79d66, 0x1e79d86, 0x1e79db4, 0x1e79dd6, 0x1e79e00, 0x1e79e21, 0x1e79e55, 0x1e79e82, 0x1e79ea4, 0x1e79ee7, 0x1e79f22, 0x1e79f44, 0x1e79f6b, 0x1e79fbf, 0x1e7a067, 0x1e7a08e, 0x1e83cd8, 0x1e83d18, 0x1e83d62, 0x1e83d93, 0x1e83dd3, 0x1e83df7, 0x1e83e65, 0x1e86720, 0x1e8679b, 0x1ead08c, 0x1ead0b9, 0x1ead114 | 10 | 51 |
| `0x1f2caf9` | Conservé/vérifié | 0x1e57b3d, 0x1e57baf, 0x1e57c5d, 0x1e57de0, 0x1e57dfe, 0x1e581d6, 0x1e585df, 0x1e5861f, 0x1e58740, 0x1e58770, 0x1e58789, 0x1e587b6, 0x1e5883d, 0x1e5892f, 0x1e5894a, 0x1e5e647, 0x1e5e69e, 0x1e5e7c3, 0x1e5e85b, 0x1e5e92a, 0x1e5e98e, 0x1e5eb61, 0x1e5ec31, 0x1e5f032, 0x1e5f197, 0x1e5f1d7, 0x1e5f679, 0x1e5f6ef, 0x1e5f7bc, 0x1e5f7e8, 0x1e5fa16, 0x1e602ab, 0x1e60379, 0x1e626fe, 0x1e62722, 0x1e6276b, 0x1e64a9c, 0x1e64ab5, 0x1e64ace, 0x1e64ae8, 0x1e64b05, 0x1e64b94, 0x1e64c12, 0x1e64c2f, 0x1e65053, 0x1e65070, 0x1e6508d, 0x1e650aa, 0x1e650dc, 0x1e66ebd, 0x1e66ed6, 0x1e66f1a, 0x1e66f7f, 0x1e67017, 0x1e6702e, 0x1e670b0, 0x1e670c7, 0x1e670de, 0x1e67133, 0x1e67150, 0x1e671a1, 0x1e671be, 0x1e6721c, 0x1e6723e, 0x1e67702, 0x1e67736, 0x1e67ee4, 0x1e67f24, 0x1e67f64, 0x1e68005, 0x1e68449, 0x1e68489, 0x1e68536, 0x1e68557, 0x1e685ae, 0x1e692a3, 0x1e6932c, 0x1e6939f, 0x1e693b9, 0x1e693d3, 0x1e69410, 0x1e6942e, 0x1e69d02, 0x1e69d3f, 0x1e69dae, 0x1e69f03, 0x1e69f64, 0x1e69f85, 0x1e69fcb, 0x1e6a033, 0x1e6a060, 0x1e6a077, 0x1e6a091, 0x1e6f68e, 0x1e6f6c2, 0x1e7e949, 0x1e7e98d, 0x1e7e9e2, 0x1e7e9fb, 0x1e7ea48, 0x1e7f01c, 0x1e7f033, 0x1e7f0da, 0x1e7f4d0, 0x1e7f4fa, 0x1e7f542, 0x1e7f589, 0x1e82c1e, 0x1e82c41, 0x1e82c62, 0x1e82c90, 0x1e82cbe, 0x1e879a3, 0x1e893c9, 0x1e893f9, 0x1e8947e, 0x1e894c3, 0x1e894f4, 0x1e89578, 0x1e895bf, 0x1e895e1, 0x1e8960f, 0x1e899fd, 0x1e89a3d, 0x1e89a7d, 0x1e89abd, 0x1e89b0f, 0x1e89cae, 0x1e89d2f, 0x1e89d95, 0x1e89ef6, 0x1e89f3e, 0x1e89f5b, 0x1e89f9f, 0x1e89fe7, 0x1e8a07c, 0x1e8a584, 0x1e8a5af, 0x1e8a5c8, 0x1e8a5e8, 0x1e8a6c2, 0x1e8a756, 0x1e8a774, 0x1e8a791, 0x1e8a7ab, 0x1e8a7cb, 0x1e8ac7d, 0x1e8aca8, 0x1e8accc, 0x1e8ad9c, 0x1e8add2, 0x1e8adeb, 0x1e8ae59, 0x1e8ae7a, 0x1e8ae95, 0x1e8aec1, 0x1e8aee2, 0x1e8af08, 0x1e8d25f, 0x1e8d289, 0x1e8d2db, 0x1e8d35e, 0x1e8d3a1, 0x1e8d3e1, 0x1e8d41b, 0x1e8d475, 0x1e8d5ed, 0x1e8d62f, 0x1e8d65b, 0x1e8f5bb, 0x1e8f60a, 0x1e8f628, 0x1e95346, 0x1e953a7, 0x1e953f0, 0x1e9b120, 0x1e9b172, 0x1e9b443, 0x1e9b45d, 0x1e9b4c0, 0x1e9b4ef, 0x1e9b545, 0x1ea3de3, 0x1ea3e04, 0x1ea3e40, 0x1ea3e60 | 4 | 18 |
| `0x1f2cafd` | Exception justifiée | Aucun pointeur ROM vers ce texte isolé ; pas de traduction injectée. | — | — |
| `0x1f2cb04` | Conservé/vérifié | 0x1e5157f, 0x1e515d1, 0x1e51709, 0x1e51749, 0x1e5179d, 0x1e517ee, 0x1e5182e, 0x1e518cc, 0x1e5190c, 0x1e5195e, 0x1e5199e, 0x1e519de, 0x1e51a8a, 0x1e51acf, 0x1e57bcf, 0x1e57c13, 0x1e57c85, 0x1e57c9f, 0x1e57d64, 0x1e57d81, 0x1e57d9f, 0x1e57e26, 0x1e57ebd, 0x1e58665, 0x1e586ae, 0x1e59263, 0x1e592ca, 0x1e5932a, 0x1e5938a, 0x1e593ca, 0x1e59443, 0x1e59533, 0x1e595fc, 0x1e5978c, 0x1e59947, 0x1e59991, 0x1e599d1, 0x1e59a11, 0x1e59ada, 0x1e59b94, 0x1e59bde, 0x1e59c8e, 0x1e59cbc, 0x1e59cd6, 0x1e59d8c, 0x1e59dbd, 0x1e59e1a, 0x1e59e37, 0x1e59e50, 0x1e5e0ad, 0x1e5e0da, 0x1e5e1e5, 0x1e5e225, 0x1e5e265, 0x1e5e2a5, 0x1e5e2e5, 0x1e5e413, 0x1e5ea36, 0x1e5fb16, 0x1e5fc90, 0x1e5fd38, 0x1e60009, 0x1e6009b, 0x1e600db, 0x1e6011b, 0x1e603ff, 0x1e6048a, 0x1e6d641, 0x1e6dd12, 0x1e6de08, 0x1e6de3c, 0x1e6de64, 0x1e6dea6, 0x1e6df11, 0x1e6df30, 0x1e6e6e7, 0x1e7efc0, 0x1e7efd7, 0x1e82e42, 0x1e82e82, 0x1e82ec2, 0x1e82f02, 0x1e82f23, 0x1e83fa6, 0x1e86d79, 0x1e86db9, 0x1e86df9, 0x1e8d455, 0x1e8d499, 0x1e8d4b7, 0x1e8d4fa, 0x1e8d589, 0x1e91031, 0x1e91052, 0x1e91097, 0x1e910d7, 0x1e91d6f, 0x1e91d93, 0x1e91e81, 0x1e91ea4, 0x1e91ee4, 0x1e91f24, 0x1e91f74, 0x1e91fb4, 0x1e9200c, 0x1e92044, 0x1e92124, 0x1e92164, 0x1e9223d, 0x1e92436, 0x1e9262f, 0x1e92a74, 0x1e92b41, 0x1e92b66, 0x1e92b97, 0x1e97842, 0x1e97880, 0x1e978f4, 0x1e97914, 0x1e97970, 0x1e97990, 0x1e979d2, 0x1e979eb, 0x1e97a33, 0x1e97a6d, 0x1e97a9e, 0x1e97ae0, 0x1e97af9, 0x1e97b36, 0x1e97c29, 0x1e9cefa, 0x1e9d064, 0x1e9d28d, 0x1e9d2cd, 0x1e9d34b, 0x1e9d7fb, 0x1e9d81d, 0x1e9d83e, 0x1e9d87e, 0x1e9d96d, 0x1ea3d4e, 0x1ea3d6f, 0x1ea3dab, 0x1ea3dcb, 0x1fb0d38, 0x1fb0d3c | 7 | 33 |
| `0x1f2cb0b` | Conservé/vérifié | 0x1e56579, 0x1e56599, 0x1e57bef, 0x1e586d2, 0x1e58b41, 0x1e58be1, 0x1e58c3f, 0x1e58d25, 0x1e58e8c, 0x1e5dc36, 0x1e5dc76, 0x1e5dc93, 0x1e5dcda, 0x1e5dd01, 0x1e5de23, 0x1e5de7d, 0x1e5e6d3, 0x1e5eb1b, 0x1e5f9ab, 0x1e5fa59, 0x1e5fae5, 0x1e5fb3d, 0x1e6044d, 0x1e69d5f, 0x1e69d78, 0x1e69dfd, 0x1e69e21, 0x1e6cb97, 0x1e6cbd7, 0x1e6cbf5, 0x1e6cc41, 0x1e7efee, 0x1e7f005, 0x1e888a0, 0x1e8890b, 0x1e89a1d, 0x1e89a5d, 0x1e89a9d, 0x1e89add, 0x1e89b3f, 0x1e89b5d, 0x1e89bfc, 0x1e89cdd, 0x1e89d53, 0x1e89de8, 0x1e8a05c, 0x1e8a0b0, 0x1e8be85, 0x1e8bec5, 0x1e92085, 0x1e920e1, 0x1e921a4, 0x1e92202, 0x1e925b2, 0x1e9d123, 0x1e9d14d, 0x1e9d19b, 0x1e9d23f, 0x1e9d26d, 0x1e9d2ad, 0x1e9d32b, 0x1e9d36b, 0x1e9d426, 0x1e9d4fa, 0x1e9d54e, 0x1e9d723, 0x1e9d73d | 6 | 29 |
| `0x1f2cb11` | Conservé/vérifié | 0x1e58ae0, 0x1e58b01, 0x1e58bc1, 0x1e58c09, 0x1e58c63, 0x1e58c7d, 0x1e58cf0, 0x1e58d45, 0x1e58d63, 0x1e58de1, 0x1e58e67, 0x1e58ec4, 0x1e58efd, 0x1e5f8ed, 0x1e5f953, 0x1e5faae, 0x1e5fc0d, 0x1e5fc70, 0x1e6c5ae, 0x1e6c66e, 0x1e7ed54, 0x1e8bea5, 0x1e8bee5, 0x1e8befe, 0x1e8bf2f, 0x1e8bf62, 0x1e8bfaa, 0x1e8bff2, 0x1e8c03a, 0x1e8c056, 0x1e8c0aa, 0x1e8c0c6, 0x1e8c12b, 0x1e8c16b, 0x1e8c1ab, 0x1e8c1eb, 0x1e8c208, 0x1e8c2d0, 0x1e8c315, 0x1e8c374, 0x1e8c46b, 0x1e8c4af, 0x1e8c4ef, 0x1e8c546, 0x1e8c58a, 0x1e8c86f, 0x1e8c8b7, 0x1e91d4f, 0x1e91dc6, 0x1e91e05, 0x1e91e50, 0x1e91ec4, 0x1e91f04, 0x1e91f54, 0x1e91f94, 0x1e91fe8, 0x1e920a8, 0x1e920c1, 0x1e92104, 0x1e92144, 0x1e92184, 0x1e921c9, 0x1e921e2, 0x1e9226c, 0x1e922c6, 0x1e922fd, 0x1e9232b, 0x1e923af, 0x1e923e6, 0x1e92465, 0x1e9249f, 0x1e92511, 0x1e9258b, 0x1e925d2, 0x1e9264f, 0x1e9266f, 0x1e92693, 0x1e926be, 0x1e926fb, 0x1e92720, 0x1e92743, 0x1e9276f, 0x1e927a7, 0x1e927ca, 0x1e92804, 0x1e9285a, 0x1e9288f, 0x1e92917, 0x1e92981, 0x1e929cc, 0x1e92a12, 0x1e92aa4, 0x1e92b08, 0x1e92b21, 0x1e92be5, 0x1e92f15, 0x1e92f3e, 0x1e92f73, 0x1e92fac, 0x1e92fc3, 0x1e92fda, 0x1e92ff1, 0x1e9cf21, 0x1e9cf38, 0x1e9d01d, 0x1e9d044, 0x1e9d084, 0x1e9d0f9, 0x1e9d16d, 0x1e9d2ed, 0x1e9d38b, 0x1e9d44d, 0x1e9d5ff, 0x1e9d656, 0x1e9da84 | 5 | 24 |
| `0x1f2cb16` | Conservé/vérifié | 0x1e5e6f3, 0x1e5e731, 0x1e5e765, 0x1e5e83b, 0x1e5e87b, 0x1e5e894, 0x1e5e8dd, 0x1e5e960, 0x1e5e9c7, 0x1e5e9e1, 0x1e5e9fb, 0x1e5eaa8, 0x1e5eac9, 0x1e5f0f0, 0x1e5f15b, 0x1e5f1b7, 0x1e5f52b, 0x1e5f642, 0x1e5f699, 0x1e5f825, 0x1e5f853, 0x1e5f8a7, 0x1e5f90d, 0x1e5f933, 0x1e5f973, 0x1e5f9e2, 0x1e6031b, 0x1e60359, 0x1e6c5a0, 0x1e6c61c, 0x1e8c14b, 0x1e8c18b, 0x1e8c1cb, 0x1e8c24e, 0x1e8c2f5, 0x1e8c335, 0x1e8c39b, 0x1e8c3c3, 0x1e8c429, 0x1e8c48f, 0x1e8c4cf, 0x1e8c514, 0x1e8c56a, 0x1e8c5aa, 0x1e8c5c4, 0x1e8c5de, 0x1e8c6d2, 0x1e8c6ec, 0x1e8c7f2, 0x1e8c80c, 0x1e8c838, 0x1e8c893, 0x1e8c8e0, 0x1e8c8fa, 0x1e8c916, 0x1e8d231, 0x1e8d2b4, 0x1e8d33e, 0x1e8d37e, 0x1e8d3c1, 0x1e8d401, 0x1e9d4da, 0x1e9d52e, 0x1e9d56e, 0x1e9d58f, 0x1e9d67e, 0x1e9d6c8, 0x1e9d6e5, 0x1e9d6ff, 0x1e9d75d, 0x1e9d7ba, 0x1e9d7d4, 0x1e9d8aa, 0x1e9d8c4, 0x1e9d991, 0x1e9da24, 0x1e9da4c, 0x1e9daa8, 0x1e9dd06, 0x1e9dd47, 0x1e9dd61, 0x1e9dd7a, 0x1e9dda4, 0x1e9ddc4, 0x1e9ddde, 0x1e9ddfd | 7 | 34 |
| `0x1f2cb1d` | Traduit/vérifié | 0x1e61895, 0x1e618d8, 0x1e89b7d, 0x1e89d05, 0x1e90f39, 0x1e90f79, 0x1e918fa, 0x1e92ae0, 0x1e94869, 0x1e9488a, 0x1e948c1, 0x1e9cffa, 0x1ea7c72, 0x1ea7d11, 0x1ea98ae, 0x1ea98c8, 0x1ea991a, 0x1eae620, 0x1eae65b, 0x1eae675, 0x1eae6af, 0x1eae6dd, 0x1eae755, 0x1eae77d, 0x1eae79b | 10 | 46 |
| `0x1f2cb27` | Traduit/vérifié | 0x1e57cbf, 0x1e58db9, 0x1e59119, 0x1e5913c, 0x1e59222, 0x1e5923c, 0x1e5930a, 0x1e5936a, 0x1e59423, 0x1e594c1, 0x1e594e0, 0x1e5ac53, 0x1e694fc, 0x1e695a5, 0x1e6df7e, 0x1e6dfbf, 0x1e6dfe1, 0x1e82e62, 0x1e82ea2, 0x1e82ee2, 0x1e82f43, 0x1e9024d, 0x1e90271, 0x1e9029b, 0x1e907a5, 0x1e907f2, 0x1e90845, 0x1e908b4, 0x1e9099b, 0x1e90b41, 0x1e963b0, 0x1e963eb, 0x1e9640c, 0x1e96f29, 0x1e9adee, 0x1e9ae58, 0x1e9ae72, 0x1e9aeb2, 0x1e9bfd8, 0x1e9c3dd, 0x1e9c72a, 0x1e9c7c6, 0x1e9c810, 0x1e9c833, 0x1e9c92d, 0x1e9c9ad, 0x1e9c9f7, 0x1e9ca1a, 0x1e9cb84, 0x1e9cc04, 0x1e9cc1d, 0x1e9cc3a, 0x1e9ccd5, 0x1e9ccf6, 0x1e9cd4a, 0x1e9cd63 | 8 | 40 |
| `0x1f2cb2d` | Traduit/vérifié | 0x1e86d99, 0x1e86dd9, 0x1e888c3, 0x1e8a660, 0x1e8a966, 0x1e8abc6 | 9 | 45 |
| `0x1f2cb34` | Traduit/vérifié | 0x1e5ab7f, 0x1e8a900, 0x1e8aa5d, 0x1e8ab18, 0x1e8ad4f, 0x1e8be1d, 0x1e953c7, 0x1e9bcbe, 0x1e9bcde, 0x1e9c0f4, 0x1e9c19f, 0x1e9c522, 0x1e9c577, 0x1e9c5bf, 0x1e9c5f9 | 10 | 52 |
| `0x1f2cb3c` | Traduit/vérifié | 0x1e5aba0, 0x1e8a923, 0x1e8aae4, 0x1e8ad80, 0x1e8be3d, 0x1e9c108, 0x1e9c205, 0x1e9c545, 0x1e9c597, 0x1e9c5df, 0x1e9c61c | 10 | 52 |
| `0x1f2cb44` | Traduit/vérifié | 0x1e9bd1a, 0x1e9bd43, 0x1e9c11c | 10 | 52 |
| `0x1f2cb4c` | Exception justifiée | Aucun pointeur ROM vers ce texte isolé ; pas de traduction injectée. | — | — |
| `0x1f2cb54` | Conservé/vérifié | 0x1e8c3e5, 0x1e8c444, 0x1e8c5fc, 0x1e8c707 | 6 | 30 |
| `0x1f2cb5a` | Conservé/vérifié | 0x23e7bb | 14 | 71 |
| `0x1f2cb68` | Traduit/vérifié | 0x23e7ae | 24 | 127 |
| `0x1f2cb7c` | Traduit/vérifié | 0x23e572 | 23 | 124 |
| `0x1f2cb91` | Traduit/vérifié | 0x1e6e583, 0x1ec02f0, 0x1fb40d8 | 22 | 121 |
| `0x1f2cba2` | Traduit/vérifié | 0x1e6e58a, 0x1ebe8a0, 0x1ec02e8 | 25 | 140 |
| `0x1f2cbb6` | Traduit/vérifié | 0x1e91905 | 32 | 97 |
| `0x1f2cbda` | Traduit/vérifié | 0x1e9192a | 53 | 134 |
| `0x1f2cc17` | Traduit/vérifié | 0x1e9194d | 76 | 130 |
| `0x1f2cc7e` | Traduit/vérifié | 0x1e8fef5 | 29 | 160 |
| `0x1f2cc98` | Traduit/vérifié | 0x1e8ff6d | 190 | 162 |
| `0x1f2cd70` | Traduit/vérifié | 0x1e8ff8e | 35 | 127 |
| `0x1f2cda7` | Traduit/vérifié | 0x1e8ffc4 | 251 | 192 |
| `0x1f2ceb3` | Traduit/vérifié | 0x1e8ffe1 | 16 | 84 |
| `0x1f2cec2` | Traduit/vérifié | 0x1e90001 | 10 | 49 |
| `0x1f2cec8` | Traduit/vérifié | 0x1e9001b | 39 | 130 |
| `0x1f2cefb` | Traduit/vérifié | 0x1e90146 | 76 | 153 |
| `0x1f2cf50` | Traduit/vérifié | 0x1ea3f1c | 94 | 119 |
| `0x1f2cfb0` | Traduit/vérifié | 0x1e9032a, 0x1ea3f2d | 21 | 148 |
| `0x1f2cfc3` | Traduit/vérifié | 0x1e90191 | 42 | 172 |
| `0x1f2cff4` | Traduit/vérifié | 0x1e901a8 | 64 | 188 |
| `0x1f2d02e` | Traduit/vérifié | 0x1e901bf | 35 | 174 |
| `0x1f2d04e` | Traduit/vérifié | 0x1e901d6 | 52 | 175 |
| `0x1f2d07e` | Traduit/vérifié | 0x1e90238 | 132 | 182 |
| `0x1f2d124` | Traduit/vérifié | 0x1e90258 | 66 | 153 |
| `0x1f2d162` | Traduit/vérifié | 0x1e9027c | 58 | 171 |
| `0x1f2d192` | Traduit/vérifié | 0x1e902a6 | 66 | 154 |
| `0x1f2d1d7` | Traduit/vérifié | 0x1e902e1 | 156 | 177 |
| `0x1f2d28b` | Traduit/vérifié | 0x1e902fa | 108 | 163 |
| `0x1f2d2f9` | Traduit/vérifié | 0x1e90313 | 164 | 178 |
| `0x1f2d3b2` | Traduit/vérifié | 0x1e90348 | 206 | 184 |
| `0x1f2d412` | Exception justifiée | Suffixe interne du dialogue 0x1f2d3b2, sans propre pointeur ; couvert par traduction du propriétaire. Propriétaire 0x1f2d3b2, lecteurs 0x1e90348. | — | — |
| `0x1f2d495` | Exception justifiée | Aucun pointeur ROM vers ce texte isolé ; pas de traduction injectée. | — | — |
| `0x1f2d4f0` | Traduit/vérifié | 0x1e903cf | 90 | 143 |
| `0x1f2d560` | Traduit/vérifié | 0x1e903fb | 37 | 135 |
| `0x1f2d590` | Traduit/vérifié | 0x1e903f2 | 50 | 166 |
| `0x1f2d5c1` | Traduit/vérifié | 0x1e90404 | 36 | 137 |
| `0x1f2d5e5` | Traduit/vérifié | 0x1e90423 | 27 | 149 |
| `0x1f2d5ff` | Traduit/vérifié | 0x1e904c9 | 220 | 188 |
| `0x1f2d6e9` | Exception justifiée | Aucun pointeur ROM vers ce texte isolé ; pas de traduction injectée. | — | — |
| `0x1f2d705` | Traduit/vérifié | 0x1e9057a | 36 | 155 |
| `0x1f2d733` | Traduit/vérifié | 0x1e905c0 | 48 | 171 |
| `0x1f2d76f` | Traduit/vérifié | 0x1e90662 | 32 | 159 |
| `0x1f2d78c` | Traduit/vérifié | 0x1e906ac, 0x1e906de, 0x1e90714 | 20 | 116 |
| `0x1f2d7aa` | Traduit/vérifié | 0x1e9073c | 85 | 176 |
| `0x1f2d80a` | Traduit/vérifié | 0x1e907b0 | 59 | 153 |
| `0x1f2d84c` | Traduit/vérifié | 0x1e907d0 | 95 | 143 |
| `0x1f2d8c0` | Traduit/vérifié | 0x1e907fd | 75 | 158 |
| `0x1f2d90e` | Traduit/vérifié | 0x1e90825 | 47 | 183 |
| `0x1f2d942` | Traduit/vérifié | 0x1e90850 | 113 | 156 |
| `0x1f2d9b9` | Traduit/vérifié | 0x1e90884 | 57 | 166 |
| `0x1f2d9eb` | Traduit/vérifié | 0x1e90888 | 36 | 109 |
| `0x1f2da1d` | Traduit/vérifié | 0x1e908ec | 135 | 184 |
| `0x1f2daab` | Traduit/vérifié | 0x1e90a97 | 149 | 192 |
| `0x1f2db4e` | Exception justifiée | Aucun pointeur ROM vers ce texte isolé ; pas de traduction injectée. | — | — |
| `0x1f2db6d` | Traduit/vérifié | 0x1e908bf | 18 | 70 |
| `0x1f2db7d` | Traduit/vérifié | 0x1e90b4c | 16 | 58 |
| `0x1f2db8b` | Traduit/vérifié | 0x1e90b73 | 21 | 94 |
| `0x1f2dba3` | Conservé/vérifié | 0x1e90953, 0x1e90af7, 0x1e9acdf, 0x1e9ad1e, 0x1e9ad5d | 12 | 161 |
| `0x1f2dbb6` | Traduit/vérifié | 0x1e909a6 | 117 | 192 |
| `0x1f2dc22` | Traduit/vérifié | 0x1e5e1b1, 0x1e909d4 | 11 | 106 |
| `0x1f2dc2e` | Traduit/vérifié | 0x1e90a09 | 135 | 171 |
| `0x1f2dcc8` | Traduit/vérifié | 0x1e90bee | 174 | 180 |
| `0x1f2dd91` | Traduit/vérifié | 0x1e90c1c | 174 | 173 |
| `0x1f2de5b` | Traduit/vérifié | 0x1e90c05 | 156 | 173 |
| `0x1f2df13` | Traduit/vérifié | 0x1e90eeb | 15 | 79 |
| `0x1f2df20` | Traduit/vérifié | 0x1e90f44 | 80 | 160 |
| `0x1f2df7c` | Traduit/vérifié | 0x1e90f64 | 37 | 113 |
| `0x1f2dfa4` | Traduit/vérifié | 0x1e90f84 | 124 | 177 |
| `0x1f2e027` | Traduit/vérifié | 0x1e90fa4 | 37 | 138 |
| `0x1f2e048` | Traduit/vérifié | 0x1e9101c | 234 | 192 |
| `0x1f2e150` | Traduit/vérifié | 0x1e9103c | 114 | 148 |
| `0x1f2e1d2` | Traduit/vérifié | 0x1e9105d | 42 | 135 |
| `0x1f2e1fa` | Traduit/vérifié | 0x1e9107d | 46 | 142 |
| `0x1f2e221` | Traduit/vérifié | 0x1e910a2 | 219 | 181 |
| `0x1f2e311` | Traduit/vérifié | 0x1e910c2 | 148 | 167 |
| `0x1f2e3cf` | Traduit/vérifié | 0x1e910e2 | 146 | 156 |
| `0x1f2e479` | Traduit/vérifié | 0x1e91102 | 26 | 139 |
| `0x1f2e491` | Traduit/vérifié | 0x1e91136 | 82 | 160 |
| `0x1f2e4f2` | Traduit/vérifié | 0x1e6d7ed | 36 | 171 |
| `0x1f2e50f` | Traduit/vérifié | 0x1e6d80d | 121 | 152 |
| `0x1f2e593` | Traduit/vérifié | 0x1e6d838 | 324 | 193 |
| `0x1f2e6fe` | Traduit/vérifié | 0x1e6d858 | 68 | 150 |
| `0x1f2e742` | Traduit/vérifié | 0x1e6d878 | 337 | 173 |
| `0x1f2e8e9` | Traduit/vérifié | 0x1e6d898 | 228 | 183 |
| `0x1f2e9d8` | Traduit/vérifié | 0x1e6db51 | 101 | 194 |
| `0x1f2ea3b` | Traduit/vérifié | 0x1e6db68 | 93 | 161 |
| `0x1f2ea9b` | Traduit/vérifié | 0x1e6d8e5 | 24 | 132 |
| `0x1f2eaad` | Traduit/vérifié | 0x1e6d8e9 | 37 | 134 |
| `0x1f2eadd` | Traduit/vérifié | 0x1e6d943 | 61 | 130 |
| `0x1f2eb1f` | Traduit/vérifié | 0x1e6d963 | 108 | 165 |
| `0x1f2eb85` | Traduit/vérifié | 0x1e6d983 | 116 | 156 |
| `0x1f2ec0a` | Traduit/vérifié | 0x1e6d9a3 | 98 | 152 |
| `0x1f2ec73` | Traduit/vérifié | 0x1e6d9eb | 89 | 155 |
| `0x1f2ecd5` | Traduit/vérifié | 0x1e6da1d | 482 | 182 |
| `0x1f2ef1c` | Traduit/vérifié | 0x1e6da49 | 229 | 193 |
| `0x1f2f01a` | Traduit/vérifié | 0x1e6da61 | 38 | 166 |
| `0x1f2f045` | Traduit/vérifié | 0x1e6da7e | 209 | 185 |
| `0x1f2f123` | Traduit/vérifié | 0x1e6daa0 | 271 | 185 |
| `0x1f2f24d` | Traduit/vérifié | 0x1e55ec6 | 6 | 30 |
| `0x1f2f252` | Traduit/vérifié | 0x1e55ed8 | 29 | 157 |
| `0x1f2f269` | Traduit/vérifié | 0x1e55f05 | 78 | 151 |
| `0x1f2f2c8` | Traduit/vérifié | 0x1e55f14 | 42 | 177 |
| `0x1f2f2f2` | Traduit/vérifié | 0x1e55f23 | 321 | 182 |
| `0x1f2f468` | Traduit/vérifié | 0x1e82e4d | 34 | 112 |
| `0x1f2f493` | Traduit/vérifié | 0x1e82e6d | 13 | 65 |
| `0x1f2f4a4` | Traduit/vérifié | 0x1e82e8d | 20 | 106 |
| `0x1f2f4c3` | Traduit/vérifié | 0x1e82ead | 134 | 163 |
| `0x1f2f55d` | Traduit/vérifié | 0x1e82ecd | 83 | 145 |
| `0x1f2f5be` | Traduit/vérifié | 0x1e82eed | 47 | 129 |
| `0x1f2f5ea` | Traduit/vérifié | 0x1e82f0d | 153 | 175 |
| `0x1f2f69e` | Traduit/vérifié | 0x1e82f2e | 109 | 171 |
| `0x1f2f718` | Conservé/vérifié | 0x1e6dd1d | 20 | 92 |
| `0x1f2f72c` | Conservé/vérifié | 0x1e57ed7, 0x1e6dd2d | 8 | 24 |
| `0x1f2f734` | Traduit/vérifié | 0x1e6dd84 | 27 | 123 |
| `0x1f2f759` | Traduit/vérifié | 0x1e6de13 | 173 | 149 |
| `0x1f2f80d` | Traduit/vérifié | 0x1e6de47 | 32 | 90 |
| `0x1f2f82b` | Traduit/vérifié | 0x1e6de6f | 44 | 129 |
| `0x1f2f85c` | Traduit/vérifié | 0x1e6deb1 | 50 | 148 |
| `0x1f2f896` | Traduit/vérifié | 0x1e6df1c | 260 | 184 |
| `0x1f2f9b9` | Traduit/vérifié | 0x1e6df3b | 35 | 145 |
| `0x1f2f9d7` | Traduit/vérifié | 0x1e6df89 | 110 | 162 |
| `0x1f2fa62` | Traduit/vérifié | 0x1e6dfa7 | 7 | 32 |
| `0x1f2fa6a` | Traduit/vérifié | 0x1e6dfca | 95 | 176 |
| `0x1f2fac9` | Traduit/vérifié | 0x1e6dfec | 41 | 117 |
| `0x1f2faf3` | Traduit/vérifié | 0x1e6e0de | 40 | 196 |
| `0x1f2fb19` | Traduit/vérifié | 0x1e86d84 | 110 | 167 |
| `0x1f2fb92` | Traduit/vérifié | 0x1e86dc4 | 241 | 188 |
| `0x1f2fc9a` | Traduit/vérifié | 0x1e82f4e, 0x1e86da4, 0x1e86de4, 0x1e8a66b, 0x1e8a971 | 13 | 66 |
| `0x1f2fca4` | Traduit/vérifié | 0x1e86e04 | 11 | 55 |
| `0x1f2fcae` | Conservé/vérifié | 0x1e5fbd8, 0x1e5fc2d, 0x1e6294b, 0x1e629b4, 0x1e62a06, 0x1e62a26, 0x1e62a46, 0x1e62ab0, 0x1e62af0, 0x1e62b78, 0x1e67e32, 0x1e67e67, 0x1e67ec4, 0x1e67f04, 0x1e67f44, 0x1e67fc5, 0x1e68067, 0x1e680d9, 0x1e681f9, 0x1e68214, 0x1e6822f, 0x1e6824a, 0x1e68265, 0x1e68280, 0x1e6829b, 0x1e682bf, 0x1e682ec, 0x1e68320, 0x1e6833b, 0x1e68429, 0x1e68469, 0x1e684a9, 0x1e7f562, 0x1e8d60e, 0x1e9b14a, 0x1e9b19a, 0x1e9b1f9, 0x1e9b24b, 0x1e9b28f, 0x1e9b2db, 0x1e9b323, 0x1e9b37b, 0x1e9b398, 0x1e9b3d0, 0x1e9b513 | 7 | 33 |
| `0x1f2fcb5` | Traduit/vérifié | 0x1e67e3d | 245 | 181 |
| `0x1f2fd07` | Exception justifiée | Suffixe tronqué interne du dialogue0x1f2fcb5 ; seul mot correspondant au pointeur situé dans PCM, pas consommateur texte. Propriétaire 0x1f2fcb5, lecteurs 0x1e67e3d. Exclusions : 0x1338c2a. | — | — |
| `0x1f2fdbe` | Traduit/vérifié | 0x1e68204 | 119 | 188 |
| `0x1f2fe44` | Traduit/vérifié | 0x1e67e72 | 395 | 187 |
| `0x1f2fffe` | Traduit/vérifié | 0x1e67e8e Exclusions : 0x10f95d1, 0x13c5889. | 13 | 69 |
| `0x1f3000d` | Traduit/vérifié | 0x1e67ecf | 18 | 101 |
| `0x1f30020` | Traduit/vérifié | 0x1e67eef Exclusions : 0x9ff6c2. | 72 | 178 |
| `0x1f30071` | Traduit/vérifié | 0x1e67f0f | 172 | 181 |
| `0x1f30116` | Traduit/vérifié | 0x1e67f2f | 81 | 153 |
| `0x1f30167` | Traduit/vérifié | 0x1e67f4f | 112 | 167 |
| `0x1f301f7` | Traduit/vérifié | 0x1e67f6f | 19 | 105 |
| `0x1f3020b` | Traduit/vérifié | 0x1e67fb0 | 89 | 177 |
| `0x1f30263` | Traduit/vérifié | 0x1e67fd0 | 264 | 191 |
| `0x1f30375` | Traduit/vérifié | 0x1e67ff0 | 46 | 120 |
| `0x1f303b0` | Traduit/vérifié | 0x1e68010 | 60 | 170 |
| `0x1f303f6` | Traduit/vérifié | 0x1e6804d | 251 | 189 |
| `0x1f30506` | Traduit/vérifié | 0x1e68072 | 207 | 181 |
| `0x1f305eb` | Traduit/vérifié | 0x1e68092 | 61 | 185 |
| `0x1f30627` | Traduit/vérifié | 0x1e680bf | 105 | 154 |
| `0x1f3068c` | Traduit/vérifié | 0x1e680e4 | 234 | 146 |
| `0x1f3078a` | Traduit/vérifié | 0x1e68104 | 93 | 182 |
| `0x1f307eb` | Traduit/vérifié | 0x1e6811d | 148 | 164 |
| `0x1f30899` | Traduit/vérifié | 0x1e6821f | 120 | 158 |
| `0x1f30933` | Traduit/vérifié | 0x1e6823a | 128 | 173 |
| `0x1f309be` | Traduit/vérifié | 0x1e68255 | 184 | 178 |
| `0x1f30a7f` | Traduit/vérifié | 0x1e68270 | 137 | 142 |
| `0x1f30b16` | Traduit/vérifié | 0x1e6828b | 118 | 197 |
| `0x1f30b8f` | Traduit/vérifié | 0x1e682a6 | 136 | 174 |
| `0x1f30c2d` | Traduit/vérifié | 0x1e682ca | 535 | 185 |
| `0x1f30e6a` | Traduit/vérifié | 0x1e682f7 | 199 | 156 |
| `0x1f30f62` | Traduit/vérifié | 0x1e6832b | 25 | 186 |
| `0x1f30f7b` | Traduit/vérifié | 0x1e68613 | 103 | 150 |
| `0x1f30ffc` | Traduit/vérifié | 0x1e879ae | 48 | 151 |
| `0x1f3102e` | Traduit/vérifié | 0x1e58477 | 178 | 182 |
| `0x1f310e9` | Traduit/vérifié | 0x1e584c6 | 20 | 110 |
| `0x1f31102` | Traduit/vérifié | 0x1e5849e | 39 | 130 |
| `0x1f31125` | Traduit/vérifié | 0x1e58517 | 82 | 168 |
| `0x1f31172` | Traduit/vérifié | 0x1e585ea | 60 | 114 |
| `0x1f311b8` | Traduit/vérifié | 0x1e5860a | 107 | 170 |
| `0x1f31226` | Traduit/vérifié | 0x1e5862a | 116 | 192 |
| `0x1f3129d` | Traduit/vérifié | 0x1e5864a | 181 | 180 |
| `0x1f31357` | Traduit/vérifié | 0x1e58670 | 18 | 80 |
| `0x1f31367` | Traduit/vérifié | 0x1e586b9 | 83 | 128 |
| `0x1f313cd` | Traduit/vérifié | 0x1e586dd | 29 | 139 |
| `0x1f313eb` | Traduit/vérifié | 0x1e5874b | 103 | 160 |
| `0x1f3145d` | Traduit/vérifié | 0x1e5877b | 121 | 152 |
| `0x1f314ef` | Traduit/vérifié | 0x1e58794 | 114 | 159 |
| `0x1f31574` | Traduit/vérifié | 0x1e587ad, 0x1e893f0 | 26 | 173 |
| `0x1f31592` | Traduit/vérifié | 0x1e587c1 | 170 | 162 |
| `0x1f3164b` | Traduit/vérifié | 0x1e58848 | 56 | 168 |
| `0x1f31686` | Traduit/vérifié | 0x1e58818, 0x1e89439 | 94 | 170 |
| `0x1f316ef` | Traduit/vérifié | 0x1e5893a | 70 | 146 |
| `0x1f3174b` | Traduit/vérifié | 0x1e58955 | 46 | 155 |
| `0x1f31781` | Traduit/vérifié | 0x1e581e1 | 78 | 146 |
| `0x1f317d8` | Conservé/vérifié | 0x1e57b48 | 26 | 141 |
