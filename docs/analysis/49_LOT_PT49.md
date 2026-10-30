# PT-49 — Descriptions d’objets et de mouvements

F-808 ; dépendances F-758 et F-759 intégrées. Manifeste explicite : 283 offsets.
Source ROM EN SHA256 : `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

## Domaine réel et livraison

- 199 descriptions d’objets (gemmes, disques, objets légendaires, Méga-Gemmes, cristaux Z, objets tenus).
- 11 descriptions de mouvements dans les cellules de description des TM de gItems.
- 33 noms longs d’objets anglais vivants, conservés selon le glossaire F-759.
- 5 noms longs sans pointeur consommateur : aucune injection revendiquée.
- 35 faux textes binaires : deux blocs LZ77 et 33 zones de tuiles brutes.

Les 210 traductions sont ajoutées en fin de combined, sans supprimer ni modifier
les traductions existantes. Chaque valeur exacte est protégée dans le même commit.
Le patch local `batch_49` réutilise `StructuredTextPatch` : validation des préimages,
allocation finale, écriture des seuls pointeurs sélectionnés et vérification exacte.
Les cellules de gItems (base 0x876074, pas 44 octets, description à +20, nom long
à +0) restent en place ; aucun texte ne déborde dans la cellule suivante.
Il n’y a aucun nom fixe à traduire : les noms anglais vivants restent inchangés.

Les descriptions ont le même nombre de sauts FE que l’anglais et aucun jeton
positionnel. Budgets : 192 pixels / 2–3 lignes pour les objets, 122 pixels /
4 lignes pour les TM. Les octets de contrôle ne sont pas traduits.
F-759 : noms d’espèces, de mouvements et d’objets sans attestation conservés ;
les types et statistiques suivent le glossaire, notamment PS et Ataque Especial.
Le besoin de lumière de Necrozma est attribué à Necrozma (ambiguïté FR évitée).

## Preuve et limites

Le manifeste machine `languages/pt/data/pt49_audit.json` conserve l’anglais,
la comparaison FR, les préimages, toutes les références brutes, les IDs d’objets,
les budgets et la décision pour chacun des 283 offsets. Pour chaque faux texte,
les descripteurs graphiques ou blocs LZ77 prouvent la nature non textuelle.
Les rares valeurs ressemblant à un pointeur dans d’autres données binaires sont
enregistrées avec leur contexte, mais ne sont jamais repointées.

Commandes de validation :

```sh
python3 -m pytest tests/unit/pt/test_batch_pt49.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt49_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt49.config.ts
```

La preuve Playwright utilise mGBA hors écran, une sauvegarde copiée en dossier
temporaire et les véritables octets livrés. Elle présente trois descriptions
dans le Cube en substituant uniquement les champs de la Repousse sur une copie
temporaire de ROM. L’OCR vérifie toutes les lignes attendues avant la capture.
Ce contrôle du moteur réel n’est pas un parcours de collecte de tous les objets.
Aucune sauvegarde en jeu, aucun push, aucun pipeline distant.

## Bilan offset par offset

| Offset | Décision | Consommateur ou preuve |
| --- | --- | --- |
| `0xeb4946` | Traduit / contrôle ROM dédié | 0x87c77c |
| `0xeb49a6` | Traduit / contrôle ROM dédié | 0x87c7a8 |
| `0xeb4a09` | Traduit / contrôle ROM dédié | 0x87c7d4 |
| `0xeb4a67` | Traduit / contrôle ROM dédié | 0x87c800 |
| `0xeb4ac8` | Traduit / contrôle ROM dédié | 0x87c82c |
| `0xeb4b27` | Traduit / contrôle ROM dédié | 0x87c858 |
| `0xeb4b84` | Traduit / contrôle ROM dédié | 0x87c884 |
| `0xeb4be4` | Traduit / contrôle ROM dédié | 0x87c8b0 |
| `0xeb4c42` | Traduit / contrôle ROM dédié | 0x87c8dc |
| `0xeb4ca1` | Traduit / contrôle ROM dédié | 0x87c908 |
| `0xeb4cfe` | Traduit / contrôle ROM dédié | 0x87c934 |
| `0xeb4d5d` | Traduit / contrôle ROM dédié | 0x87c960 |
| `0xeb4dbd` | Traduit / contrôle ROM dédié | 0x87c98c |
| `0xeb4e26` | Traduit / contrôle ROM dédié | 0x87c9b8 |
| `0xeb4e8a` | Traduit / contrôle ROM dédié | 0x87c9e4 |
| `0xeb4ee6` | Traduit / contrôle ROM dédié | 0x87ca10 |
| `0xeb4f45` | Traduit / contrôle ROM dédié | 0x87ca3c |
| `0xeb4fa6` | Traduit / contrôle ROM dédié | 0x87ca68 |
| `0xeb5007` | Traduit / contrôle ROM dédié | 0x87cf0c |
| `0xeb5057` | Traduit / contrôle ROM dédié | 0x87cf38 |
| `0xeb50a8` | Traduit / contrôle ROM dédié | 0x87cf64 |
| `0xeb50fc` | Traduit / contrôle ROM dédié | 0x87cf90 |
| `0xeb514b` | Traduit / contrôle ROM dédié | 0x87cfbc |
| `0xeb51a4` | Traduit / contrôle ROM dédié | 0x87cfe8 |
| `0xeb51fb` | Traduit / contrôle ROM dédié | 0x87d014 |
| `0xeb5252` | Traduit / contrôle ROM dédié | 0x87d040 |
| `0xeb52a9` | Traduit / contrôle ROM dédié | 0x87d06c |
| `0xeb52fe` | Traduit / contrôle ROM dédié | 0x87d098 |
| `0xeb5352` | Traduit / contrôle ROM dédié | 0x87d0c4 |
| `0xeb53a8` | Traduit / contrôle ROM dédié | 0x87d0f0 |
| `0xeb53fe` | Traduit / contrôle ROM dédié | 0x87d11c |
| `0xeb5453` | Traduit / contrôle ROM dédié | 0x87d148 |
| `0xeb54a9` | Traduit / contrôle ROM dédié | 0x87d174 |
| `0xeb54ff` | Traduit / contrôle ROM dédié | 0x87d1a0 |
| `0xeb5558` | Traduit / contrôle ROM dédié | 0x87d1cc |
| `0xeb55b0` | Traduit / contrôle ROM dédié | 0x87d1f8 |
| `0xeb5604` | Traduit / contrôle ROM dédié | 0x87d224 |
| `0xeb565b` | Traduit / contrôle ROM dédié | 0x87d250 |
| `0xeb56b0` | Traduit / contrôle ROM dédié | 0x87d27c |
| `0xeb5706` | Traduit / contrôle ROM dédié | 0x87d2a8 |
| `0xeb5730` | Traduit / contrôle ROM dédié | 0x87d2d4 |
| `0xeb575a` | Traduit / contrôle ROM dédié | 0x87d300 |
| `0xeb5797` | Traduit / contrôle ROM dédié | 0x87d32c |
| `0xeb57d2` | Traduit / contrôle ROM dédié | 0x87d358, 0x87d384 |
| `0xeb5827` | Traduit / contrôle ROM dédié | 0x87d3b0 |
| `0xeb5887` | Traduit / contrôle ROM dédié | 0x87d3dc |
| `0xeb58e5` | Traduit / contrôle ROM dédié | 0x87be08 |
| `0xeb594f` | Traduit / contrôle ROM dédié | 0x87be34 |
| `0xeb598f` | Traduit / contrôle ROM dédié | 0x87be60 |
| `0xeb59f5` | Traduit / contrôle ROM dédié | 0x87be8c |
| `0xeb5a55` | Traduit / contrôle ROM dédié | 0x87d408 |
| `0xeb5a99` | Traduit / contrôle ROM dédié | 0x87d434 |
| `0xeb5add` | Traduit / contrôle ROM dédié | 0x87d460 |
| `0xeb5b1f` | Traduit / contrôle ROM dédié | 0x87d48c |
| `0xeb5b64` | Traduit / contrôle ROM dédié | 0x87d4b8 |
| `0xeb5bab` | Traduit / contrôle ROM dédié | 0x87d4e4 |
| `0xeb5bf2` | Traduit / contrôle ROM dédié | 0x87d510 |
| `0xeb5c36` | Traduit / contrôle ROM dédié | 0x87ae90 |
| `0xeb5c8b` | Traduit / contrôle ROM dédié | 0x87aebc |
| `0xeb5ce0` | Traduit / contrôle ROM dédié | 0x87aee8 |
| `0xeb5d36` | Traduit / contrôle ROM dédié | 0x87af14 |
| `0xeb5d8c` | Traduit / contrôle ROM dédié | 0x87af40 |
| `0xeb5de2` | Traduit / contrôle ROM dédié | 0x87af6c |
| `0xeb5e37` | Traduit / contrôle ROM dédié | 0x87af98 |
| `0xeb5e8b` | Traduit / contrôle ROM dédié | 0x87afc4 |
| `0xeb5ee0` | Traduit / contrôle ROM dédié | 0x87aff0 |
| `0xeb5f34` | Traduit / contrôle ROM dédié | 0x87b01c |
| `0xeb5f87` | Traduit / contrôle ROM dédié | 0x87b048 |
| `0xeb5fde` | Traduit / contrôle ROM dédié | 0x87b074 |
| `0xeb6031` | Traduit / contrôle ROM dédié | 0x87b0a0 |
| `0xeb6086` | Traduit / contrôle ROM dédié | 0x87b0cc |
| `0xeb60dd` | Traduit / contrôle ROM dédié | 0x87b0f8 |
| `0xeb6130` | Traduit / contrôle ROM dédié | 0x87b124 |
| `0xeb6183` | Traduit / contrôle ROM dédié | 0x87b150 |
| `0xeb61d8` | Traduit / contrôle ROM dédié | 0x87b17c |
| `0xeb622c` | Traduit / contrôle ROM dédié | 0x87b1a8 |
| `0xeb627f` | Traduit / contrôle ROM dédié | 0x87b1d4 |
| `0xeb62d5` | Traduit / contrôle ROM dédié | 0x87b200 |
| `0xeb632a` | Traduit / contrôle ROM dédié | 0x87b22c |
| `0xeb6380` | Traduit / contrôle ROM dédié | 0x87b258 |
| `0xeb63d5` | Traduit / contrôle ROM dédié | 0x87b284 |
| `0xeb642a` | Traduit / contrôle ROM dédié | 0x87b2b0 |
| `0xeb647f` | Traduit / contrôle ROM dédié | 0x87b2dc |
| `0xeb64d5` | Traduit / contrôle ROM dédié | 0x87b308 |
| `0xeb6529` | Traduit / contrôle ROM dédié | 0x87b334 |
| `0xeb657c` | Traduit / contrôle ROM dédié | 0x87b360 |
| `0xeb65cf` | Traduit / contrôle ROM dédié | 0x87b38c |
| `0xeb6624` | Traduit / contrôle ROM dédié | 0x87b3b8 |
| `0xeb667a` | Traduit / contrôle ROM dédié | 0x87b3e4 |
| `0xeb66cf` | Traduit / contrôle ROM dédié | 0x87b410 |
| `0xeb6724` | Traduit / contrôle ROM dédié | 0x87b43c |
| `0xeb6778` | Traduit / contrôle ROM dédié | 0x87b468 |
| `0xeb67cc` | Traduit / contrôle ROM dédié | 0x87b494 |
| `0xeb681e` | Traduit / contrôle ROM dédié | 0x87b4c0 |
| `0xeb6871` | Traduit / contrôle ROM dédié | 0x87b4ec |
| `0xeb68c7` | Traduit / contrôle ROM dédié | 0x87b518 |
| `0xeb691d` | Traduit / contrôle ROM dédié | 0x87b544 |
| `0xeb6970` | Traduit / contrôle ROM dédié | 0x87b570 |
| `0xeb69c3` | Traduit / contrôle ROM dédié | 0x87b59c |
| `0xeb6a17` | Traduit / contrôle ROM dédié | 0x87b5c8 |
| `0xeb6a6c` | Traduit / contrôle ROM dédié | 0x87b5f4 |
| `0xeb6ac0` | Traduit / contrôle ROM dédié | 0x87b620 |
| `0xeb6b16` | Traduit / contrôle ROM dédié | 0x87b64c |
| `0xeb6b6a` | Traduit / contrôle ROM dédié | 0x87b678 |
| `0xeb6bbd` | Traduit / contrôle ROM dédié | 0x87b6a4 |
| `0xeb6c11` | Traduit / contrôle ROM dédié | 0x87d53c |
| `0xeb6c63` | Traduit / contrôle ROM dédié | 0x87d568 |
| `0xeb6cb7` | Traduit / contrôle ROM dédié | 0x87d594 |
| `0xeb6d09` | Traduit / contrôle ROM dédié | 0x87d5c0 |
| `0xeb6d5b` | Traduit / contrôle ROM dédié | 0x87d5ec |
| `0xeb6dad` | Traduit / contrôle ROM dédié | 0x87d618 |
| `0xeb6dfd` | Traduit / contrôle ROM dédié | 0x87d644 |
| `0xeb6e4c` | Traduit / contrôle ROM dédié | 0x87d670 |
| `0xeb6e9d` | Traduit / contrôle ROM dédié | 0x87d69c |
| `0xeb6eee` | Traduit / contrôle ROM dédié | 0x87d6c8 |
| `0xeb6f3e` | Traduit / contrôle ROM dédié | 0x87d6f4 |
| `0xeb6f8f` | Traduit / contrôle ROM dédié | 0x87d720 |
| `0xeb6fe0` | Traduit / contrôle ROM dédié | 0x87d74c |
| `0xeb7034` | Traduit / contrôle ROM dédié | 0x87d778 |
| `0xeb7087` | Traduit / contrôle ROM dédié | 0x87d7a4 |
| `0xeb70d6` | Traduit / contrôle ROM dédié | 0x87d7d0 |
| `0xeb7128` | Traduit / contrôle ROM dédié | 0x87d7fc |
| `0xeb7178` | Traduit / contrôle ROM dédié | 0x87d828 |
| `0xeb71c9` | Traduit / contrôle ROM dédié | 0x87d854 |
| `0xeb7226` | Traduit / contrôle ROM dédié | 0x87d880 |
| `0xeb727f` | Traduit / contrôle ROM dédié | 0x87d8ac |
| `0xeb72d4` | Traduit / contrôle ROM dédié | 0x87d8d8 |
| `0xeb732e` | Traduit / contrôle ROM dédié | 0x87d904 |
| `0xeb7386` | Traduit / contrôle ROM dédié | 0x87d930 |
| `0xeb73db` | Traduit / contrôle ROM dédié | 0x87d95c |
| `0xeb7432` | Traduit / contrôle ROM dédié | 0x87d988 |
| `0xeb748b` | Traduit / contrôle ROM dédié | 0x87d9b4 |
| `0xeb74da` | Traduit / contrôle ROM dédié | 0x87d9e0 |
| `0xeb7530` | Traduit / contrôle ROM dédié | 0x87da0c |
| `0xeb7587` | Traduit / contrôle ROM dédié | 0x87da38 |
| `0xeb75ea` | Traduit / contrôle ROM dédié | 0x87da64 |
| `0xeb7644` | Traduit / contrôle ROM dédié | 0x87da90 |
| `0xeb769b` | Traduit / contrôle ROM dédié | 0x87dabc |
| `0xeb76f7` | Traduit / contrôle ROM dédié | 0x87dae8 |
| `0xeb7750` | Traduit / contrôle ROM dédié | 0x87ba98 |
| `0xeb77ba` | Traduit / contrôle ROM dédié | 0x87bac4 |
| `0xeb781a` | Traduit / contrôle ROM dédié | 0x87baf0 |
| `0xeb786c` | Traduit / contrôle ROM dédié | 0x87bb1c |
| `0xeb78bb` | Traduit / contrôle ROM dédié | 0x87bb48 |
| `0xeb790e` | Traduit / contrôle ROM dédié | 0x87bb74 |
| `0xeb7963` | Traduit / contrôle ROM dédié | 0x87cc4c, 0x87cc78, 0x87cca4, 0x87ccd0 |
| `0xeb79c1` | Traduit / contrôle ROM dédié | 0x87ba6c |
| `0xeb7a1b` | Traduit / contrôle ROM dédié | 0x87ba40 |
| `0xeb7a7d` | Traduit / contrôle ROM dédié | 0x87cbf4 |
| `0xeb7ad9` | Traduit / contrôle ROM dédié | 0x87cc20 |
| `0xeb7b35` | Traduit / contrôle ROM dédié | 0x878d38 |
| `0xeb7b9a` | Traduit / contrôle ROM dédié | 0x87bba0 |
| `0xeb7bf7` | Traduit / contrôle ROM dédié | 0x87bbcc |
| `0xeb7c56` | Traduit / contrôle ROM dédié | 0x87bbf8 |
| `0xeb7cb4` | Traduit / contrôle ROM dédié | 0x87bc24 |
| `0xeb7d12` | Traduit / contrôle ROM dédié | 0x87bc50 |
| `0xeb7d74` | Traduit / contrôle ROM dédié | 0x87bc7c |
| `0xeb7ddd` | Traduit / contrôle ROM dédié | 0x878290, 0x878d64 |
| `0xeb7e43` | Traduit / contrôle ROM dédié | 0x878d90 |
| `0xeb7e91` | Traduit / contrôle ROM dédié | 0x878dbc |
| `0xeb7ee6` | Traduit / contrôle ROM dédié | 0x878de8 |
| `0xeb7f50` | Traduit / contrôle ROM dédié | 0x878e14 |
| `0xeb7fa2` | Traduit / contrôle ROM dédié | 0x878e40 |
| `0xeb7ff5` | Traduit / contrôle ROM dédié | 0x878e6c |
| `0xeb8048` | Traduit / contrôle ROM dédié | 0x87899c |
| `0xeb80ad` | Traduit / contrôle ROM dédié | 0x8789c8 |
| `0xeb810e` | Traduit / contrôle ROM dédié | 0x8789f4 |
| `0xeb816a` | Traduit / contrôle ROM dédié | 0x878a20 |
| `0xeb81b7` | Traduit / contrôle ROM dédié | 0x878a4c |
| `0xeb8213` | Traduit / contrôle ROM dédié | 0x87dc74 |
| `0xeb8271` | Traduit / contrôle ROM dédié | 0x87dca0 |
| `0xeb82ce` | Traduit / contrôle ROM dédié | 0x87dccc, 0x87dcf8 |
| `0xeb8334` | Traduit / contrôle ROM dédié | 0x87dd24 |
| `0xeb8384` | Traduit / contrôle ROM dédié | 0x87dd50 |
| `0xeb83cf` | Traduit / contrôle ROM dédié | 0x87dd7c |
| `0xeb841a` | Traduit / contrôle ROM dédié | 0x87dda8 |
| `0xeb8466` | Traduit / contrôle ROM dédié | 0x87ddd4 |
| `0xeb84b2` | Traduit / contrôle ROM dédié | 0x87de00 |
| `0xeb84fe` | Traduit / contrôle ROM dédié | 0x87de2c |
| `0xeb8548` | Traduit / contrôle ROM dédié | 0x87de58 |
| `0xeb85a7` | Traduit / contrôle ROM dédié | 0x87de84 |
| `0xeb8608` | Traduit / contrôle ROM dédié | 0x87dedc |
| `0xeb866d` | Traduit / contrôle ROM dédié | 0x87df08 |
| `0xeb86ce` | Traduit / contrôle ROM dédié | 0x87df34 |
| `0xeb8732` | Traduit / contrôle ROM dédié | 0x878ce0 |
| `0xeb8798` | Traduit / contrôle ROM dédié | 0x878c04 |
| `0xeb87fe` | Traduit / contrôle ROM dédié | 0x878c30 |
| `0xeb8865` | Traduit / contrôle ROM dédié | 0x878c5c |
| `0xeb88cc` | Traduit / contrôle ROM dédié | 0x878c88 |
| `0xeb8933` | Traduit / contrôle ROM dédié | 0x878cb4 |
| `0xeb8998` | Traduit / contrôle ROM dédié | 0x877134 |
| `0xeb8a01` | Traduit / contrôle ROM dédié | 0x87db14 |
| `0xeb8a65` | Traduit / contrôle ROM dédié | 0x87db40 |
| `0xeb8ac1` | Traduit / contrôle ROM dédié | 0x87db6c |
| `0xeb8b20` | Traduit / contrôle ROM dédié | 0x87db98 |
| `0xeb8b82` | Traduit / contrôle ROM dédié | 0x87dbc4 |
| `0xeb8be5` | Traduit / contrôle ROM dédié | 0x87dbf0 |
| `0xeb8c40` | Traduit / contrôle ROM dédié | 0x87dc1c |
| `0xeb8caa` | Traduit / contrôle ROM dédié | 0x87dc48 |
| `0xeb8d15` | Traduit / contrôle ROM dédié | 0x87a994 |
| `0xeb8d71` | Traduit / contrôle ROM dédié | 0x87a9c0 |
| `0xeb8dce` | Traduit / contrôle ROM dédié | 0x87aa18 |
| `0xeb8e28` | Traduit / contrôle ROM dédié | 0x87aa70 |
| `0xeb8e7d` | Traduit / contrôle ROM dédié | 0x87ab20 |
| `0xeb8ed7` | Traduit / contrôle ROM dédié | 0x87ab78 |
| `0xeb8f29` | Traduit / contrôle ROM dédié | 0x87abd0 |
| `0xeb8f7d` | Traduit / contrôle ROM dédié | 0x87ac54 |
| `0xeb8fd7` | Traduit / contrôle ROM dédié | 0x87ac80 |
| `0xeb902d` | Traduit / contrôle ROM dédié | 0x87acac |
| `0xeb9089` | Traduit / contrôle ROM dédié | 0x87acd8 |
| `0xeb90ea` | Vérifié : anglais conservé (F-759) | 0x8780c4 |
| `0xeb90f8` | Vérifié : anglais conservé (F-759) | 0x878250 |
| `0xeb9106` | Vérifié : anglais conservé (F-759) | 0x878300 |
| `0xeb9115` | Vérifié : anglais conservé (F-759) | 0x87832c |
| `0xeb9124` | Vérifié : anglais conservé (F-759) | 0x878568 |
| `0xeb9132` | Vérifié : anglais conservé (F-759) | 0x878670 |
| `0xeb9141` | Vérifié : anglais conservé (F-759) | 0x8786c8 |
| `0xeb914f` | Vérifié : anglais conservé (F-759) | 0x87cc0c |
| `0xeb915f` | Exception : nom long inutilisé | Aucun pointeur vers cet offset dans les 32 Mio EN |
| `0xeb9170` | Vérifié : anglais conservé (F-759) | 0x87b6bc |
| `0xeb917f` | Vérifié : anglais conservé (F-759) | 0x87ba58 |
| `0xeb918d` | Vérifié : anglais conservé (F-759) | 0x87bb34 |
| `0xeb919b` | Vérifié : anglais conservé (F-759) | 0x87be78 |
| `0xeb91a9` | Exception : nom long inutilisé | Aucun pointeur vers cet offset dans les 32 Mio EN |
| `0xeb91b7` | Exception : nom long inutilisé | Aucun pointeur vers cet offset dans les 32 Mio EN |
| `0xeb91c6` | Vérifié : anglais conservé (F-759) | 0x87c4a8 |
| `0xeb91d4` | Exception : nom long inutilisé | Aucun pointeur vers cet offset dans les 32 Mio EN |
| `0xeb91e5` | Vérifié : anglais conservé (F-759) | 0x87c6b8 |
| `0xeb91f3` | Vérifié : anglais conservé (F-759) | 0x87cc64 |
| `0xeb91fe` | Exception : nom long inutilisé | Aucun pointeur vers cet offset dans les 32 Mio EN |
| `0xeb920e` | Vérifié : anglais conservé (F-759) | 0x87bcec |
| `0xeb921c` | Vérifié : anglais conservé (F-759) | 0x8790c0 |
| `0xeb922a` | Vérifié : anglais conservé (F-759) | 0x877120 |
| `0xeb9238` | Vérifié : anglais conservé (F-759) | 0x87db58 |
| `0xeb9247` | Vérifié : anglais conservé (F-759) | 0x87dbb0 |
| `0xeb9257` | Vérifié : anglais conservé (F-759) | 0x87dc08 |
| `0xeb9264` | Vérifié : anglais conservé (F-759) | 0x87dc34 |
| `0xeb9272` | Vérifié : anglais conservé (F-759) | 0x87dd10 |
| `0xeb9283` | Vérifié : anglais conservé (F-759) | 0x87de44 |
| `0xeb9291` | Vérifié : anglais conservé (F-759) | 0x87de70 |
| `0xeb92a1` | Vérifié : anglais conservé (F-759) | 0x87dec8 |
| `0xeb92b0` | Vérifié : anglais conservé (F-759) | 0x878edc |
| `0xeb92c0` | Vérifié : anglais conservé (F-759) | 0x87a064 |
| `0xeb92ce` | Vérifié : anglais conservé (F-759) | 0x87a1c4 |
| `0xeb92dd` | Vérifié : anglais conservé (F-759) | 0x87ca80 |
| `0xeb92ed` | Vérifié : anglais conservé (F-759) | 0x87a198 |
| `0xeb92fc` | Vérifié : anglais conservé (F-759) | 0x87903c |
| `0xeb930e` | Vérifié : anglais conservé (F-759) | 0x87a16c |
| `0xed9e72` | Exception : données graphiques | LZ77 0xed99dc (pointeurs 0xeb9384, 0xeb9758, 0xeb9b2c) |
| `0xef0a0f` | Exception : données graphiques | LZ77 0xef0870 (pointeurs 0xf4a10) |
| `0xef76b3` | Exception : données graphiques | Tuiles 0xef7508 / 512 octets (descripteur 0xec0fb0) |
| `0xef84d1` | Exception : données graphiques | Tuiles 0xef8308 / 512 octets (descripteur 0xec0fe8) |
| `0xef84d9` | Exception : données graphiques | Tuiles 0xef8308 / 512 octets (descripteur 0xec0fe8) |
| `0xf4d2fe` | Exception : données graphiques | Tuiles 0xf4d148 / 512 octets (descripteur 0xec38bc) |
| `0xf4daa8` | Exception : données graphiques | Tuiles 0xf4d948 / 512 octets (descripteur 0xec38dc) |
| `0xf4def8` | Exception : données graphiques | Tuiles 0xf4dd48 / 512 octets (descripteur 0xec38ec) |
| `0xf4e2ef` | Exception : données graphiques | Tuiles 0xf4e148 / 512 octets (descripteur 0xec3944) |
| `0xf4e4f3` | Exception : données graphiques | Tuiles 0xf4e348 / 512 octets (descripteur 0xec394c) |
| `0xf4e701` | Exception : données graphiques | Tuiles 0xf4e548 / 512 octets (descripteur 0xec3954) |
| `0xf4f101` | Exception : données graphiques | Tuiles 0xf4ef48 / 512 octets (descripteur 0xec397c) ; coïncidences binaires : 0x603383 |
| `0xf4f301` | Exception : données graphiques | Tuiles 0xf4f148 / 512 octets (descripteur 0xec3984) |
| `0xf4f901` | Exception : données graphiques | Tuiles 0xf4f748 / 512 octets (descripteur 0xec387c) |
| `0xf50501` | Exception : données graphiques | Tuiles 0xf50348 / 512 octets (descripteur 0xec38ac) ; coïncidences binaires : 0x13e4a9b |
| `0xf6caa1` | Exception : données graphiques | Tuiles 0xf6c8e8 / 512 octets (descripteur 0xec0818) |
| `0xf6d4a1` | Exception : données graphiques | Tuiles 0xf6d2e8 / 512 octets (descripteur 0xec0840) |
| `0xf7c5ea` | Exception : données graphiques | Tuiles 0xf7c528 / 512 octets (descripteur 0xebf810) |
| `0xf7c7ea` | Exception : données graphiques | Tuiles 0xf7c728 / 512 octets (descripteur 0xebf818) |
| `0xf818f3` | Exception : données graphiques | Tuiles 0xf81748 / 512 octets (descripteur 0xebf500) |
| `0xf820f0` | Exception : données graphiques | Tuiles 0xf81f48 / 512 octets (descripteur 0xebf520) |
| `0xf82719` | Exception : données graphiques | Tuiles 0xf82548 / 512 octets (descripteur 0xebf538) |
| `0xf874f3` | Exception : données graphiques | Tuiles 0xf87348 / 512 octets (descripteur 0xebf130) |
| `0xf87cf0` | Exception : données graphiques | Tuiles 0xf87b48 / 512 octets (descripteur 0xebf150) |
| `0xf88319` | Exception : données graphiques | Tuiles 0xf88148 / 512 octets (descripteur 0xebf168) |
| `0xf8f4f7` | Exception : données graphiques | Tuiles 0xf8f368 / 512 octets (descripteur 0xec3cec) ; coïncidences binaires : 0x4b3768, 0x4d0167 |
| `0xf8f50d` | Exception : données graphiques | Tuiles 0xf8f368 / 512 octets (descripteur 0xec3cec) ; coïncidences binaires : 0x11fc191 |
| `0xf8fd13` | Exception : données graphiques | Tuiles 0xf8fb68 / 512 octets (descripteur 0xec3d0c) |
| `0xfcd773` | Exception : données graphiques | Tuiles 0xfcd5c8 / 512 octets (descripteur 0xec0be0) |
| `0xfce591` | Exception : données graphiques | Tuiles 0xfce3c8 / 512 octets (descripteur 0xec0c18) |
| `0xfce599` | Exception : données graphiques | Tuiles 0xfce3c8 / 512 octets (descripteur 0xec0c18) |
| `0xffa2da` | Exception : données graphiques | Tuiles 0xff9da8 / 2048 octets (descripteur 0xec2814), 0xff9da8 / 2048 octets (descripteur 0xec281c) |
| `0xffafa4` | Exception : données graphiques | Tuiles 0xffadc8 / 2048 octets (descripteur 0xec1cac) |
| `0xffb093` | Exception : données graphiques | Tuiles 0xffadc8 / 2048 octets (descripteur 0xec1cac) |
| `0xffd884` | Exception : données graphiques | Tuiles 0xffd5c8 / 2048 octets (descripteur 0xec1ce4), 0xffd5c8 / 2048 octets (descripteur 0xec1cec) |
