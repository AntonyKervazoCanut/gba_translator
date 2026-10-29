# PT-15 — crédits, échanges, Cadeau Mystère et Pokédex

F-774, dépendances F-758/F-759 intégrées. Le manifeste PT-15 est le périmètre fermé : 281 offsets, 273 entrées livrées et 8 exceptions.

La zone réelle dépasse les menus : crédits FireRed historiques, catégories de phrases, échanges, compatibilité de Pension, apprentissage, Cadeau Mystère et 86 descriptions Pokédex (générique puis Bulbasaur à Dodrio). Les noms des personnes, organisations, espèces et mouvements non attestés restent anglais. PRESENTE MISTÉRIO, CARTÃO MISTÉRIO, NOTÍCIAS MISTÉRIO et SELO sont des choix éditoriaux, sans revendication officielle.

## Sources et injection

Le fichier `pt15_audit.json` consigne pour chaque offset les références EN/FR, les vrais octets source, la traduction, les pointeurs consommateurs, le décalage éventuel des crédits, les commandes et budgets. La ROM EN actuelle est anglaise dans le Pokédex ; `combined_en.txt` y contient des variantes françaises périmées ou des lignes vides. La traduction part donc des octets anglais vivants, avec comparaison FR, jamais de la variante française aveuglément.

Le patch final `batch_15` réutilise `StructuredTextPatch`, après les réparations et repointages génériques. Les pointeurs des tables fixes sont modifiés ; leurs cellules de texte ne sont jamais agrandies sur place. Les crédits extraits depuis du padding restent indexés dans combined par l'offset du manifeste : le patch enlève uniquement les octets nuls précédant la cible réelle. L'alias 0x41dc45 n'est pas injecté une deuxième fois ; 0x41dc48 livre déjà la même chaîne.

Les descriptions conservent trois lignes, les menus leurs ruptures et toutes les commandes conservent arguments et ordre. Budgets : 512 octets maximum par allocation, 224 pixels pour les crédits, 208 pour les autres messages, 232 pour le Pokédex. Les tests ROM mesurent les cinq polices, les icônes, colonnes FC13 et tampons développés avec dix W. Les protections `expected` suivent la normalisation historique du garde partagé ; `expected_raw` et le test PT-15 protègent aussi exactement les espaces initiaux/finals.

## Validation reproductible

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt15.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt15_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt15.config.ts
```

Playwright lance mGBA hors écran sur une copie temporaire, vérifie les octets aux pointeurs vivants puis l'OCR des messages rendus par le moteur. La capture est dans le répertoire temporaire du système, hors dépôt. Il s'agit d'une sonde de rendu : elle ne certifie ni une connexion réseau entre deux consoles, ni le parcours complet du Pokédex, ni une sauvegarde réelle. Aucun fichier de sauvegarde source n'est modifié.

## Bilan par offset

| Offset | Décision | Consommateurs / justification |
|---|---|---|
| `0x41d56b` | traduit/vérifié | `0x414658` ; cible +1 octets |
| `0x41d587` | traduit/vérifié | `0x41465c` ; cible +1 octets |
| `0x41d5fc` | traduit/vérifié | `0x414674` |
| `0x41d658` | traduit/vérifié | `0x414680` |
| `0x41d6b0` | traduit/vérifié | `0x41468c` |
| `0x41d6e9` | traduit/vérifié | `0x414694` ; cible +3 octets |
| `0x41d707` | traduit/vérifié | `0x414698` ; cible +1 octets |
| `0x41d74c` | traduit/vérifié | `0x4146a0` |
| `0x41d766` | traduit/vérifié | `0x4146a4` ; cible +2 octets |
| `0x41d799` | traduit/vérifié | `0x4146b0` ; cible +3 octets |
| `0x41d7f1` | traduit/vérifié | `0x4146bc` ; cible +3 octets |
| `0x41d849` | traduit/vérifié | `0x4146c8` ; cible +3 octets |
| `0x41d894` | traduit/vérifié | `0x4146d0` |
| `0x41d8ad` | traduit/vérifié | `0x4146d4` ; cible +3 octets |
| `0x41d8cc` | traduit/vérifié | `0x4146dc` |
| `0x41d8ea` | traduit/vérifié | `0x4146e0` ; cible +2 octets |
| `0x41d94b` | traduit/vérifié | `0x4146ec` ; cible +1 octets |
| `0x41d9a0` | traduit/vérifié | `0x4146f8` |
| `0x41d9d4` | traduit/vérifié | `0x414704` |
| `0x41da06` | traduit/vérifié | `0x41470c` ; cible +2 octets |
| `0x41da39` | traduit/vérifié | `0x414718` ; cible +3 octets |
| `0x41da6b` | traduit/vérifié | `0x414724` ; cible +1 octets |
| `0x41da85` | traduit/vérifié | `0x414728` ; cible +3 octets |
| `0x41daa0` | traduit/vérifié | `0x414730` |
| `0x41dac3` | traduit/vérifié | `0x414734` ; cible +1 octets |
| `0x41dae5` | traduit/vérifié | `0x41473c` ; cible +3 octets |
| `0x41db04` | traduit/vérifié | `0x414740` |
| `0x41db3a` | traduit/vérifié | `0x41474c` ; cible +2 octets |
| `0x41db7b` | traduit/vérifié | `0x414754` ; cible +1 octets |
| `0x41dba1` | traduit/vérifié | `0x414758` ; cible +3 octets |
| `0x41dbda` | traduit/vérifié | `0x414760` ; cible +2 octets |
| `0x41dbf6` | traduit/vérifié | `0x414764` ; cible +2 octets |
| `0x41dc29` | traduit/vérifié | `0x41476c` ; cible +3 octets |
| `0x41dc45` | exception | Alias avec 3 octets de padding ; seul 0x41dc48 est visé par 0x414770 et traité dans ce même lot. Aucune seconde traduction. |
| `0x41dc48` | traduit/vérifié | `0x414770` |
| `0x41dcac` | traduit/vérifié | `0x414778` |
| `0x41dcc5` | traduit/vérifié | `0x41477c` ; cible +3 octets |
| `0x41dd1d` | traduit/vérifié | `0x414788` ; cible +3 octets |
| `0x41dd79` | traduit/vérifié | `0x414794` ; cible +3 octets |
| `0x41ddc6` | traduit/vérifié | `0x41479c` ; cible +2 octets |
| `0x41dde4` | traduit/vérifié | `0x4147a0` |
| `0x41de21` | traduit/vérifié | `0x4147a8` ; cible +3 octets |
| `0x41de9d` | traduit/vérifié | `0xaf28` |
| `0x41def0` | traduit/vérifié | `0xaec8` |
| `0x41df05` | traduit/vérifié | `0xaecc` |
| `0x41df4c` | traduit/vérifié | `0xb000` |
| `0x41df6b` | traduit/vérifié | `0xafa4` |
| `0x41df82` | traduit/vérifié | `0x807e4` |
| `0x41df8b` | traduit/vérifié | `0x3c6ab8` |
| `0x41df92` | traduit/vérifié | `0x3c6abc` |
| `0x41df99` | traduit/vérifié | `0x3c6ac0` |
| `0x41dfa0` | traduit/vérifié | `0x3c6ac4` |
| `0x41dfa5` | traduit/vérifié | `0x12bc7c` |
| `0x41dfac` | traduit/vérifié | `0x12b518` |
| `0x41dfbe` | traduit/vérifié | `0x12be50` |
| `0x41dfc9` | traduit/vérifié | `0x12b608` |
| `0x41dfde` | traduit/vérifié | `0x3edfec` |
| `0x41dfe6` | traduit/vérifié | `0x3edf9c` |
| `0x41dfee` | traduit/vérifié | `0x3edfa0` |
| `0x41dff5` | traduit/vérifié | `0x3edfa4` |
| `0x41dffc` | traduit/vérifié | `0x3edfa8` |
| `0x41e006` | traduit/vérifié | `0x3edfac` |
| `0x41e00d` | traduit/vérifié | `0x3edfb0` |
| `0x41e014` | traduit/vérifié | `0x3edfb4` |
| `0x41e01b` | traduit/vérifié | `0x3edfb8` |
| `0x41e023` | traduit/vérifié | `0x3edfbc` |
| `0x41e02c` | traduit/vérifié | `0x3edfc0` |
| `0x41e037` | traduit/vérifié | `0x3edfc4` |
| `0x41e03f` | traduit/vérifié | `0x3edfc8` |
| `0x41e049` | traduit/vérifié | `0x3edfcc` |
| `0x41e051` | traduit/vérifié | `0x3edfd0` |
| `0x41e056` | traduit/vérifié | `0x3edfd4` |
| `0x41e05c` | traduit/vérifié | `0x3edfd8` |
| `0x41e067` | traduit/vérifié | `0x3edfdc` |
| `0x41e06e` | traduit/vérifié | `0x3edfe0` |
| `0x41e075` | traduit/vérifié | `0x3edfe4` |
| `0x41e07c` | traduit/vérifié | `0x3edfe8` |
| `0x41e08a` | traduit/vérifié | `0x3edf98` |
| `0x41e098` | exception | Aucun pointeur ROM vers cet offset (recherche LE32 exhaustive) ; fragment historique non référencé, laissé intact. |
| `0x41e0a5` | traduit/vérifié | `0x4dbc8` |
| `0x41e0b9` | traduit/vérifié | `0x16c1c6`, `0x261ecc`, `0x7d8e50`, `0x1e62441`, `0x1e6c46e`, `0x1e6c5d8`, `0x1e6c717`, `0x1e6c857`, `0x1e6ca7a`, `0x1e80b1d`, `0x1e80b72`, `0x1e8da14`, `0x1e8dab3`, `0x1e912f2`, `0x1e9e53e`, `0x1e9e6f2`, `0x1e9e7a8`, `0x1e9e835`, `0x1e9e8c2`, `0x1e9e941`, `0x1e9e9b5`, `0x1e9eb1d`, `0x1e9ee63`, `0x1e9f25a`, `0x1e9fa01`, `0x1e9fadf`, `0x1e9fb91`, `0x1e9fc57`, `0x1e9fdc3`, `0x1ea0744`, `0x1ea085c`, `0x1ea098c`, `0x1ea0aa2`, `0x1ea0b54`, `0x1ea0c24`, `0x1ea0ca6`, `0x1ea2428`, `0x1ea29c0`, `0x1ea2e9e`, `0x1ea38b9`, `0x1ea3972`, `0x1ea3a72`, `0x1ea419c`, `0x1ea4381`, `0x1ea4497`, `0x1ea4624`, `0x1ea46c0`, `0x1ea4ab6`, `0x1ea4c60`, `0x1eb018b`, `0x1eb0215`, `0x1eb0434`, `0x1eb04d7`, `0x1eb0581` |
| `0x41e0c0` | traduit/vérifié | `0x261ed0` |
| `0x41e0d2` | traduit/vérifié | `0x261ed4` |
| `0x41e0da` | traduit/vérifié | `0x261ed8` |
| `0x41e0e0` | traduit/vérifié | `0x261edc` |
| `0x41e0ee` | traduit/vérifié | `0x261ee0` |
| `0x41e10a` | traduit/vérifié | `0x261ee4` |
| `0x41e112` | traduit/vérifié | `0x261eec` |
| `0x41e118` | traduit/vérifié | `0x261ef4` |
| `0x41e145` | traduit/vérifié | `0x261ef8` |
| `0x41e16b` | traduit/vérifié | `0x261efc` |
| `0x41e199` | traduit/vérifié | `0x261f04` |
| `0x41e1c5` | traduit/vérifié | `0x261f08` |
| `0x41e1e9` | traduit/vérifié | `0x514b0`, `0x528a0` |
| `0x41e200` | traduit/vérifié | `0x51528`, `0x52918` |
| `0x41e20d` | traduit/vérifié | `0x52158`, `0x535b4` |
| `0x41e21e` | traduit/vérifié | `0x521fc`, `0x53658` |
| `0x41e234` | traduit/vérifié | `0xbf1e4`, `0xbf350` |
| `0x41e245` | traduit/vérifié | `0x46faac` |
| `0x41e263` | traduit/vérifié | `0x46fab0` |
| `0x41e273` | traduit/vérifié | `0x46fab4` |
| `0x41e284` | traduit/vérifié | `0x46fab8` |
| `0x41e29e` | traduit/vérifié | `0x46fabc` |
| `0x41e2b4` | traduit/vérifié | `0x46fa9c` |
| `0x41e2bf` | traduit/vérifié | `0x46faa0` |
| `0x41e2c9` | traduit/vérifié | `0x46faa4` |
| `0x41e2d4` | traduit/vérifié | `0x46faa8` |
| `0x41e2ec` | exception | Aucun pointeur ROM vers cet offset (recherche LE32 exhaustive) ; fragment historique non référencé, laissé intact. |
| `0x41e325` | traduit/vérifié | `0x54064`, `0xcf9c8` |
| `0x41e33c` | traduit/vérifié | `0x25f82c` |
| `0x41e361` | traduit/vérifié | `0x25f830` |
| `0x41e37c` | traduit/vérifié | `0x25f834` |
| `0x41e3a8` | traduit/vérifié | `0x25f838` |
| `0x41e3e3` | traduit/vérifié | `0xe4f50` |
| `0x41e3fb` | traduit/vérifié | `0xe526c`, `0x9f73f8` |
| `0x41e405` | traduit/vérifié | `0xe4ad8` |
| `0x41e414` | traduit/vérifié | `0xe4b68` |
| `0x41e481` | traduit/vérifié | `0xe4bec` |
| `0x41e493` | traduit/vérifié | `0xe4e68` |
| `0x41e4c0` | traduit/vérifié | `0xe4e88` |
| `0x41e4e2` | traduit/vérifié | `0xe5280`, `0xe52dc` |
| `0x41e50c` | traduit/vérifié | `0xe4bc8` |
| `0x41e538` | traduit/vérifié | `0x11c384` |
| `0x41e572` | traduit/vérifié | `0x11c538` |
| `0x41e58d` | traduit/vérifié | `0x11c4dc` |
| `0x41e5a4` | traduit/vérifié | `0x12d164` |
| `0x41e5b9` | traduit/vérifié | `0x12d16c` |
| `0x41e5d2` | traduit/vérifié | `0x12d168` |
| `0x41e5ed` | traduit/vérifié | `0x45f610` |
| `0x41e5f3` | traduit/vérifié | `0x45f614` |
| `0x41e5f8` | traduit/vérifié | `0x45f618` |
| `0x41e5fd` | traduit/vérifié | `0x466ed8` |
| `0x41e63f` | traduit/vérifié | `0x466edc` |
| `0x41e669` | traduit/vérifié | `0x466ee0` |
| `0x41e685` | traduit/vérifié | `0x466ee4` |
| `0x41e6a1` | traduit/vérifié | `0x142fbc` |
| `0x41e6dc` | traduit/vérifié | `0x142fe0` |
| `0x41e717` | traduit/vérifié | `0x142ff4` |
| `0x41e741` | traduit/vérifié | `0x143004` |
| `0x41e76b` | exception | Aucun pointeur ROM vers cet offset (recherche LE32 exhaustive) ; fragment historique non référencé, laissé intact. |
| `0x41e794` | traduit/vérifié | `0x1430f8` |
| `0x41e7a3` | traduit/vérifié | `0x143258` |
| `0x41e7bc` | traduit/vérifié | `0x142cc8`, `0x142d6c`, `0x1435a8` |
| `0x41e7d1` | traduit/vérifié | `0x142ca4` |
| `0x41e7f2` | traduit/vérifié | `0x1431d8` |
| `0x41e823` | traduit/vérifié | `0x143204` |
| `0x41e866` | traduit/vérifié | `0x142c40` |
| `0x41e88f` | traduit/vérifié | `0x142c58` |
| `0x41e8bd` | traduit/vérifié | `0x142c44` |
| `0x41e8e2` | traduit/vérifié | `0x142c5c` |
| `0x41e90c` | traduit/vérifié | `0x142c68` |
| `0x41e92b` | traduit/vérifié | `0x142cd4` |
| `0x41e946` | traduit/vérifié | `0x142c74` |
| `0x41e968` | traduit/vérifié | `0x142c8c` |
| `0x41e98f` | traduit/vérifié | `0x142c80` |
| `0x41e9ab` | traduit/vérifié | `0x142c98`, `0x142df8` |
| `0x41e9d3` | traduit/vérifié | `0x142c2c`, `0x142dbc` |
| `0x41ea0d` | traduit/vérifié | `0x142cbc` |
| `0x41ea3f` | traduit/vérifié | `0x142cb8` |
| `0x41ea6f` | traduit/vérifié | `0x142c20`, `0x142db4` |
| `0x41ea86` | traduit/vérifié | `0x142928` |
| `0x41eab7` | traduit/vérifié | `0x142988` |
| `0x41eae7` | traduit/vérifié | `0x1434fc` |
| `0x41eb01` | traduit/vérifié | `0x143510` |
| `0x41eb20` | traduit/vérifié | `0x142dc4` |
| `0x41eb46` | traduit/vérifié | `0x142dd0` |
| `0x41eb71` | traduit/vérifié | `0x142dd8` |
| `0x41eb8e` | traduit/vérifié | `0x142e0c` |
| `0x41ebaa` | traduit/vérifié | `0x142de0` |
| `0x41ebde` | traduit/vérifié | `0x142df0` |
| `0x41ec12` | traduit/vérifié | `0x142de8` |
| `0x41ec40` | traduit/vérifié | `0x142e00` |
| `0x41ec6a` | traduit/vérifié | `0x142e1c` |
| `0x41ec99` | traduit/vérifié | `0x142b1c` |
| `0x41ecd3` | traduit/vérifié | `0x142b08` |
| `0x41ecf9` | traduit/vérifié | `0x1433f8` |
| `0x41ed2f` | traduit/vérifié | `0x142b74` |
| `0x41ed50` | traduit/vérifié | `0x142b88` |
| `0x41ed7b` | traduit/vérifié | `0x142b3c` |
| `0x41ed9c` | traduit/vérifié | `0x142b2c` |
| `0x41edbd` | traduit/vérifié | `0x1423b0` |
| `0x41edca` | traduit/vérifié | `0x1423a4` |
| `0x41eddd` | traduit/vérifié | `0x466dd0` |
| `0x41edea` | traduit/vérifié | `0x466dd8` |
| `0x41edf6` | traduit/vérifié | `0x466de8` |
| `0x41ee0d` | traduit/vérifié | `0x466df0` |
| `0x41ee14` | traduit/vérifié | `0x466de0` |
| `0x41ee19` | traduit/vérifié | `0x466e18`, `0x466e38`, `0x466e50`, `0x466e68` |
| `0x41ee21` | traduit/vérifié | `0x466e20`, `0x466e58` |
| `0x41ee26` | traduit/vérifié | `0x466e28`, `0x466e40` |
| `0x41ee2b` | traduit/vérifié | `0x1024bc` |
| `0x41efb8` | exception | Faux positif graphique, aucun pointeur ROM LE32 ; séquence répétitive de tuiles non linguistique, laissée intacte. |
| `0x41f0a8` | exception | Faux positif graphique, aucun pointeur ROM LE32 ; séquence répétitive de tuiles non linguistique, laissée intacte. |
| `0x41f0bd` | exception | Faux positif graphique, aucun pointeur ROM LE32 ; séquence répétitive de tuiles non linguistique, laissée intacte. |
| `0x41f160` | exception | Faux positif graphique, aucun pointeur ROM LE32 ; séquence répétitive de tuiles non linguistique, laissée intacte. |
| `0x444c35` | traduit/vérifié | `0x1a357dc` |
| `0x444cb2` | traduit/vérifié | `0x1a35800` |
| `0x444d12` | traduit/vérifié | `0x1a35824` |
| `0x444d77` | traduit/vérifié | `0x1a35848` |
| `0x444ddf` | traduit/vérifié | `0x1a3586c` |
| `0x444e48` | traduit/vérifié | `0x1a35890` |
| `0x444ead` | traduit/vérifié | `0x1a358b4` |
| `0x444f18` | traduit/vérifié | `0x1a358d8` |
| `0x444f80` | traduit/vérifié | `0x1a358fc` |
| `0x444fe7` | traduit/vérifié | `0x1a35920` |
| `0x44504a` | traduit/vérifié | `0x1a35944` |
| `0x4450af` | traduit/vérifié | `0x1a35968` |
| `0x44510f` | traduit/vérifié | `0x1a3598c` |
| `0x445170` | traduit/vérifié | `0x1a359b0` |
| `0x4451d3` | traduit/vérifié | `0x1a359d4` |
| `0x445234` | traduit/vérifié | `0x1a359f8` |
| `0x445296` | traduit/vérifié | `0x1a35a1c` |
| `0x4452fd` | traduit/vérifié | `0x1a35a40` |
| `0x44535e` | traduit/vérifié | `0x1a35a64` |
| `0x4453c8` | traduit/vérifié | `0x1a35a88` |
| `0x445427` | traduit/vérifié | `0x1a35aac` |
| `0x445480` | traduit/vérifié | `0x1a35ad0` |
| `0x4454ea` | traduit/vérifié | `0x1a35af4` |
| `0x445551` | traduit/vérifié | `0x1a35b18` |
| `0x4455b6` | traduit/vérifié | `0x1a35b3c` |
| `0x44561d` | traduit/vérifié | `0x1a35b60` |
| `0x445686` | traduit/vérifié | `0x1a35b84` |
| `0x4456eb` | traduit/vérifié | `0x1a35ba8` |
| `0x44574c` | traduit/vérifié | `0x1a35bcc` |
| `0x4457b5` | traduit/vérifié | `0x1a35bf0` |
| `0x44581b` | traduit/vérifié | `0x1a35c14` |
| `0x445875` | traduit/vérifié | `0x1a35c38` |
| `0x4458db` | traduit/vérifié | `0x1a35c5c` |
| `0x44594a` | traduit/vérifié | `0x1a35c80` |
| `0x4459b0` | traduit/vérifié | `0x1a35ca4` |
| `0x445a18` | traduit/vérifié | `0x1a35cc8` |
| `0x445a7b` | traduit/vérifié | `0x1a35cec` |
| `0x445adb` | traduit/vérifié | `0x1a35d10` |
| `0x445b33` | traduit/vérifié | `0x1a35d34` |
| `0x445b94` | traduit/vérifié | `0x1a35d58` |
| `0x445bfa` | traduit/vérifié | `0x1a35d7c` |
| `0x445c62` | traduit/vérifié | `0x1a35da0` |
| `0x445ccb` | traduit/vérifié | `0x1a35dc4` |
| `0x445d35` | traduit/vérifié | `0x1a35de8` |
| `0x445da1` | traduit/vérifié | `0x1a35e0c` |
| `0x445e08` | traduit/vérifié | `0x1a35e30` |
| `0x445e70` | traduit/vérifié | `0x1a35e54` |
| `0x445ed7` | traduit/vérifié | `0x1a35e78` |
| `0x445f43` | traduit/vérifié | `0x1a35e9c` |
| `0x445fa1` | traduit/vérifié | `0x1a35ec0` |
| `0x44600a` | traduit/vérifié | `0x1a35ee4` |
| `0x446079` | traduit/vérifié | `0x1a35f08` |
| `0x4460e3` | traduit/vérifié | `0x1a35f2c` |
| `0x446144` | traduit/vérifié | `0x1a35f50` |
| `0x4461a7` | traduit/vérifié | `0x1a35f74` |
| `0x446214` | traduit/vérifié | `0x1a35f98` |
| `0x446274` | traduit/vérifié | `0x1a35fbc` |
| `0x4462e6` | traduit/vérifié | `0x1a35fe0` |
| `0x44634c` | traduit/vérifié | `0x1a36004` |
| `0x4463b2` | traduit/vérifié | `0x1a36028` |
| `0x446417` | traduit/vérifié | `0x1a3604c` |
| `0x44647e` | traduit/vérifié | `0x1a36070` |
| `0x4464dc` | traduit/vérifié | `0x1a36094` |
| `0x446540` | traduit/vérifié | `0x1a360b8` |
| `0x44659b` | traduit/vérifié | `0x1a360dc` |
| `0x4465f7` | traduit/vérifié | `0x1a36100` |
| `0x446664` | traduit/vérifié | `0x1a36124` |
| `0x4466ca` | traduit/vérifié | `0x1a36148` |
| `0x446732` | traduit/vérifié | `0x1a3616c` |
| `0x44679b` | traduit/vérifié | `0x1a36190` |
| `0x446803` | traduit/vérifié | `0x1a361b4` |
| `0x446862` | traduit/vérifié | `0x1a361d8` |
| `0x4468c8` | traduit/vérifié | `0x1a361fc` |
| `0x446938` | traduit/vérifié | `0x1a36220` |
| `0x4469a1` | traduit/vérifié | `0x1a36244` |
| `0x446a06` | traduit/vérifié | `0x1a36268` |
| `0x446a6c` | traduit/vérifié | `0x1a3628c` |
| `0x446ada` | traduit/vérifié | `0x1a362b0` |
| `0x446b42` | traduit/vérifié | `0x1a362d4` |
| `0x446ba0` | traduit/vérifié | `0x1a362f8` |
| `0x446c02` | traduit/vérifié | `0x1a3631c` |
| `0x446c62` | traduit/vérifié | `0x1a36340` |
| `0x446cc9` | traduit/vérifié | `0x1a36364` |
| `0x446d2f` | traduit/vérifié | `0x1a36388` |
| `0x446d97` | traduit/vérifié | `0x1a363ac` |
| `0x446dff` | traduit/vérifié | `0x1a363d0` |
