# PT-13 — Menus, systèmes et résumé Pokémon (F-772)

## Périmètre et décisions

Les 281 offsets explicites du manifeste ont été audités : 276 entrées vivantes
traduites ou conservées selon le glossaire F-759, cinq exceptions binaires.
Les prérequis F-758 (c5b5e0b9) et F-759 (dcc6ce5d) sont intégrés.
Aucun offset des autres lots n’est traduit, supprimé ou réécrit.

Le domaine réel comprend Boîtes PC, fonds, étages, phrases prédéfinies,
sauvegarde, notices Kanto/Sevii, résumé Pokémon, Carte de Dresseur et Options.
Les noms non attestés (badges Kanto, produits de boutique, FAME CHECKER,
Mail, Cube V3, lieux anglais et BERRY CRUSH) restent anglais conformément
à la politique de conservation du glossaire. Les mots communs sont traduits.
Les étages sont numérotés 1º–11º, puis S1–S4 pour les sous-sols.

## Livraison et contrôles

`languages/pt/patches/batch_13.py` réutilise `StructuredTextPatch` après
les passes génériques : préimages réelles, commandes et arguments exacts,
ruptures conservées, allocation sans écrasement des cellules voisines et
repointage de chaque consommateur recensé dans la ROM source. Les tables
PC/étages/Options sont des tables de pointeurs : ce finaliseur dédié garantit
leur livraison même si la passe générique ignore ou raccourcit une entrée.
Aucune table à adresse calculée n’a été identifiée dans ce lot.

Le corpus EN affiche parfois les paramètres FC/FD/F7/F8/F9 comme des lettres
accentuées. La traduction utilise les vrais octets bruts, jamais ces faux glyphes.
Les cinq pauses B0 à 0x4183ba restent explicites. Les positions FC13 des tarifs
et résultats sont inchangées ; leurs colonnes sont contrôlées.
Chaque ligne est protégée exactement dans `protected_entries.yaml`.

Le manifeste détaillé `languages/pt/data/pt13_audit.json` conserve pour chaque
offset la source EN, la comparaison FR, les octets anglais, les pointeurs,
la valeur PT, sa longueur encodée et la justification de décision.

Les tests ROM vérifient toutes les cibles du build final, les terminateurs,
l’absence de chevauchement, l’idempotence et la borne exacte des écritures.
Les largeurs utilisent les cinq polices réelles, les icônes et les colonnes FC13.
Les tampons PC sont développés avec dix W, les lieux du résumé avec dix-huit W
et les niveaux avec 100. Limites testées : 192 px pour les messages PC,
208 px pour le résumé, 120 px pour les trois lignes des œufs, 224 px ailleurs.

## Bilan offset par offset

Les sites ci-dessous sont ceux de la ROM EN ; les tests suivent leurs cibles
relocalisées dans le build PT. « Vérifié » désigne le contrat binaire automatisé,
pas une visite manuelle de chaque écran du jeu.

| Offset | Décision | Pointeurs source / preuve |
|---|---|---|
| `0x417fd0` | Traduit / vérifié | `0xca734` |
| `0x417fd9` | Conservé / vérifié | `0x3f5bcc` |
| `0x417fe6` | Conservé / vérifié | `0x3f5bd0` |
| `0x417ff3` | Conservé / vérifié | `0x3f5bd4` |
| `0x418000` | Conservé / vérifié | `0x3f5bd8` |
| `0x41800d` | Conservé / vérifié | `0x3f5bdc` |
| `0x418017` | Conservé / vérifié | `0x3f5be0` |
| `0x418022` | Conservé / vérifié | `0x3f5be4` |
| `0x41802f` | Conservé / vérifié | `0x3f5be8` |
| `0x41803a` | Traduit / vérifié | `0x3f5b54`, `0x3f5c24`, `0x3f5c6c` |
| `0x41803d` | Traduit / vérifié | `0x3f5b58`, `0x3f5c20`, `0x3f5c68` |
| `0x418040` | Traduit / vérifié | `0x3f5b5c`, `0x3f5c1c`, `0x3f5c64` |
| `0x418043` | Traduit / vérifié | `0x3f5b60`, `0x3f5c18`, `0x3f5c60` |
| `0x418046` | Traduit / vérifié | `0x3f5b64`, `0x3f5c14`, `0x3f5c5c` |
| `0x418049` | Traduit / vérifié | `0x3f5b68`, `0x3f5c10` |
| `0x41804c` | Traduit / vérifié | `0x3f5b6c`, `0x3f5c0c` |
| `0x41804f` | Traduit / vérifié | `0x3f5b70`, `0x3f5c08` |
| `0x418052` | Traduit / vérifié | `0x3f5b74`, `0x3f5c04` |
| `0x418055` | Traduit / vérifié | `0x3f5b78`, `0x3f5c00` |
| `0x418059` | Traduit / vérifié | `0x3f5b7c`, `0x3f5bfc` |
| `0x41805d` | Traduit / vérifié | `0x3dfec0`, `0x3e0228`, `0x3f5b50`, `0x3f5c2c`, `0x3f5cf0` |
| `0x418061` | Traduit / vérifié | `0x3e0230`, `0x3f5b4c`, `0x3f5c30` |
| `0x418065` | Traduit / vérifié | `0x3f5b48` |
| `0x418069` | Traduit / vérifié | `0x3e0238`, `0x3f5b44`, `0x3f5c34` |
| `0x41806d` | Traduit / vérifié | `0x3dfeb8`, `0x3f5b80`, `0x3f5cec` |
| `0x418075` | Traduit / vérifié | `0xcb630` |
| `0x41807d` | Traduit / vérifié | `0x3e0248`, `0x3f5c8c` |
| `0x41808e` | Traduit / vérifié | `0x3e0250`, `0x3f5c90` |
| `0x41809c` | Traduit / vérifié | `0x3e0258`, `0x3f5c94` |
| `0x4180a7` | Conservé / vérifié | `0x3f5cbc` |
| `0x4180bc` | Conservé / vérifié | `0x3f5cc0` |
| `0x4180d0` | Conservé / vérifié | `0x3f5cc4` |
| `0x4180e4` | Conservé / vérifié | `0x3f5cc8` |
| `0x4180fa` | Conservé / vérifié | `0x3f5ccc` |
| `0x41810d` | Conservé / vérifié | `0x3f5cd0` |
| `0x41811d` | Conservé / vérifié | `0x3f5cd4` |
| `0x41812f` | Conservé / vérifié | `0x3f5cd8` |
| `0x418142` | Conservé / vérifié | `0x3f5cdc` |
| `0x418152` | Conservé / vérifié | `0x3f5ce0` |
| `0x418163` | Conservé / vérifié | `0x3f5ce4` |
| `0x418174` | Traduit / vérifié | `0xcdca0` |
| `0x418188` | Traduit / vérifié | `0xcdac8` |
| `0x4181a4` | Traduit / vérifié | `0xcdcb0` |
| `0x4181c3` | Traduit / vérifié | `0x12ddec` |
| `0x418208` | Traduit / vérifié | `0x3cea88`, `0x9a425c` |
| `0x41821b` | Traduit / vérifié | `0x3cea90`, `0x9a4264` |
| `0x418233` | Traduit / vérifié | `0x3cea98`, `0x9a426c` |
| `0x418248` | Traduit / vérifié | `0x3ceaa0`, `0x9a4274` |
| `0x41825c` | Traduit / vérifié | `0x3ceaa8`, `0x3ceb40`, `0x9a427c`, `0x9a4314` |
| `0x41826c` | Traduit / vérifié | `0x3ceab0`, `0x9a4284` |
| `0x41827f` | Traduit / vérifié | `0x3ceab8`, `0x9a428c` |
| `0x418295` | Traduit / vérifié | `0x3ceac0`, `0x9a4294` |
| `0x4182a7` | Traduit / vérifié | `0x3ceac8`, `0x9a429c` |
| `0x4182b8` | Traduit / vérifié | `0x3cead0`, `0x9a42a4` |
| `0x4182ce` | Traduit / vérifié | `0x3cead8`, `0x9a42ac` |
| `0x4182df` | Traduit / vérifié | `0x3ceae0`, `0x9a42b4` |
| `0x4182ec` | Traduit / vérifié | `0x3ceae8`, `0x9a42bc` |
| `0x4182ff` | Traduit / vérifié | `0x3ceaf0`, `0x9a42c4` |
| `0x418319` | Traduit / vérifié | `0x3ceaf8`, `0x9a42cc` |
| `0x41832c` | Traduit / vérifié | `0x3ceb00`, `0x9a42d4` |
| `0x418346` | Traduit / vérifié | `0x3ceb08`, `0x9a42dc` |
| `0x41835a` | Exception justifiée | Suffixe intérieur «ake?» sans pointeur ; seul le début 0x418346 est consommé. Pointeurs du texte propriétaire : 0x3ceb08, 0x9a42dc. |
| `0x41835f` | Traduit / vérifié | `0x3ceb10`, `0x9a42e4` |
| `0x418379` | Traduit / vérifié | `0x3ceb18`, `0x9a42ec` |
| `0x418392` | Traduit / vérifié | `0x3ceb20`, `0x9a42f4` |
| `0x4183a0` | Traduit / vérifié | `0x3ceb28`, `0x9a42fc` |
| `0x4183ba` | Conservé / vérifié | `0x3ceb30`, `0x9a4304` |
| `0x4183c5` | Traduit / vérifié | `0x3ceb38`, `0x9a430c` |
| `0x4183dd` | Traduit / vérifié | `0x3ceb48`, `0x9a431c` |
| `0x4183f0` | Traduit / vérifié | `0x9a4324` |
| `0x418408` | Traduit / vérifié | `0x9a432c` |
| `0x418419` | Traduit / vérifié | `0x9a4334` |
| `0x418433` | Traduit / vérifié | `0x3ceb68`, `0x9a433c` |
| `0x418443` | Traduit / vérifié | `0x3ceb70`, `0x9a4344` |
| `0x418452` | Traduit / vérifié | `0x3ceb78`, `0x9a434c` |
| `0x418468` | Traduit / vérifié | `0x3d353c`, `0x9a41b8` |
| `0x41846f` | Traduit / vérifié | `0x3d3540`, `0x9a41bc` |
| `0x418475` | Traduit / vérifié | `0x3d3544`, `0x9a41c0` |
| `0x41847e` | Traduit / vérifié | `0x3d354c`, `0x9a41c8` |
| `0x418484` | Traduit / vérifié | `0x3d3548`, `0x9a41c4` |
| `0x418489` | Traduit / vérifié | `0x3d3550`, `0x9a41cc` |
| `0x41848f` | Traduit / vérifié | `0x3d3554`, `0x9a41d0` |
| `0x418497` | Traduit / vérifié | `0x3d3558`, `0x9a41d4` |
| `0x41849f` | Traduit / vérifié | `0x3d355c`, `0x9a41d8` |
| `0x4184a4` | Traduit / vérifié | `0x3d3568`, `0x9a41e4` |
| `0x4184a9` | Traduit / vérifié | `0x3d3560`, `0x9a41dc` |
| `0x4184ae` | Traduit / vérifié | `0x3d3564`, `0x9a41e0` |
| `0x4184b8` | Traduit / vérifié | `0x3d356c`, `0x9a41e8` |
| `0x4184bd` | Traduit / vérifié | `0x3d3570`, `0x3d3574`, `0x9a41ec`, `0x9a41f0` |
| `0x4184c2` | Traduit / vérifié | `0x3d3578`, `0x9a41f4` |
| `0x4184c9` | Traduit / vérifié | `0x9a41f8` |
| `0x4184cd` | Conservé / vérifié | `0x3d3580`, `0x9a41fc` |
| `0x4184d2` | Traduit / vérifié | `0x3d3584`, `0x9a4200` |
| `0x4184dc` | Traduit / vérifié | `0x3d3588`, `0x9a4204` |
| `0x4184e6` | Traduit / vérifié | `0x3d358c`, `0x9a4208` |
| `0x4184f0` | Traduit / vérifié | `0x3d3590`, `0x9a420c` |
| `0x4184f9` | Traduit / vérifié | `0x3d3594`, `0x9a4210` |
| `0x418500` | Traduit / vérifié | `0x3d3598`, `0x9a4214` |
| `0x418505` | Traduit / vérifié | `0x3d359c`, `0x9a4218` |
| `0x41850c` | Traduit / vérifié | `0x3d35a0`, `0x9a421c` |
| `0x418514` | Traduit / vérifié | `0x3d35a4`, `0x9a4220` |
| `0x418519` | Traduit / vérifié | `0x3d35a8`, `0x9a4224` |
| `0x418521` | Traduit / vérifié | `0x3d35ac`, `0x9a4228` |
| `0x418526` | Traduit / vérifié | `0x3d35b0`, `0x9a422c` |
| `0x41852b` | Traduit / vérifié | `0x3d35b4`, `0x9a4230` |
| `0x418531` | Traduit / vérifié | `0x3d35b8`, `0x9a4234` |
| `0x41853a` | Traduit / vérifié | `0x3d35bc`, `0x9a4238` |
| `0x418540` | Traduit / vérifié | `0x3d35c0`, `0x9a423c` |
| `0x418544` | Traduit / vérifié | `0x9a4240` |
| `0x41854a` | Traduit / vérifié | `0x9a4244` |
| `0x418555` | Traduit / vérifié | `0x9a4248` |
| `0x41855b` | Traduit / vérifié | `0x3d35d0`, `0x9a424c` |
| `0x41856c` | Traduit / vérifié | `0x3cda30` |
| `0x41857d` | Traduit / vérifié | `0x3cda38` |
| `0x41858d` | Traduit / vérifié | `0x3cda20` |
| `0x41859a` | Traduit / vérifié | `0x3cda28` |
| `0x4185a5` | Traduit / vérifié | `0x3cda40` |
| `0x4185ad` | Traduit / vérifié | `0x3cda34` |
| `0x4185e2` | Traduit / vérifié | `0x3cda3c` |
| `0x418611` | Traduit / vérifié | `0x3cda24` |
| `0x418642` | Traduit / vérifié | `0x3cda2c` |
| `0x418681` | Traduit / vérifié | `0x3cda44` |
| `0x418690` | Traduit / vérifié | `0x8c594` |
| `0x4186b0` | Traduit / vérifié | `0x8c560` |
| `0x4186cd` | Traduit / vérifié | `0x8c850` |
| `0x4186d1` | Traduit / vérifié | `0x43f2b4`, `0x43f38c` |
| `0x4186ef` | Traduit / vérifié | `0x43f2b8` |
| `0x418706` | Traduit / vérifié | `0x43f2cc`, `0x43f2e4`, `0x43f2fc` |
| `0x418725` | Traduit / vérifié | `0x43f2d0`, `0x43f2e8`, `0x43f300` |
| `0x418745` | Traduit / vérifié | `0x43f35c` |
| `0x418763` | Traduit / vérifié | `0x43f360` |
| `0x418780` | Traduit / vérifié | `0x43f314`, `0x43f32c` |
| `0x41879e` | Traduit / vérifié | `0x43f318`, `0x43f330` |
| `0x4187b2` | Traduit / vérifié | `0x43f344` |
| `0x4187d1` | Traduit / vérifié | `0x43f348` |
| `0x4187ee` | Traduit / vérifié | `0x43f390` |
| `0x41880e` | Traduit / vérifié | `0x43f2bc` |
| `0x41881b` | Traduit / vérifié | `0x43f2d4` |
| `0x41883e` | Traduit / vérifié | `0x43f2ec` |
| `0x41885f` | Traduit / vérifié | `0x43f304` |
| `0x418881` | Traduit / vérifié | `0x43f364`, `0x43f394` |
| `0x41888c` | Traduit / vérifié | `0x43f31c` |
| `0x4188ac` | Traduit / vérifié | `0x43f34c` |
| `0x4188b9` | Traduit / vérifié | `0x43f374` |
| `0x4188d6` | Traduit / vérifié | `0x43f378` |
| `0x4188f0` | Traduit / vérifié | `0x43f37c` |
| `0x418902` | Traduit / vérifié | `0x43f2c0`, `0x43f2d8`, `0x43f2f0`, `0x43f308`, `0x43f320`, `0x43f350`, `0x43f368`, `0x43f380`, `0x43f398` |
| `0x418937` | Traduit / vérifié | `0xffe00` |
| `0x418956` | Traduit / vérifié | `0xffe04` |
| `0x4189e0` | Traduit / vérifié | `0xffdf0` |
| `0x4189ee` | Traduit / vérifié | `0xffde0` |
| `0x418a2b` | Traduit / vérifié | `0x43f2b0` |
| `0x418a33` | Traduit / vérifié | `0x43f2c8` |
| `0x418a4a` | Traduit / vérifié | `0x43f2e0` |
| `0x418a61` | Traduit / vérifié | `0x43f2f8` |
| `0x418a77` | Traduit / vérifié | `0x43f340` |
| `0x418a87` | Traduit / vérifié | `0x43f370` |
| `0x418aa1` | Traduit / vérifié | `0x43f358` |
| `0x418c1b` | Traduit / vérifié | `0x1154d0` |
| `0x418c83` | Traduit / vérifié | `0xf51fc` |
| `0x418cd9` | Traduit / vérifié | `0xf5278` |
| `0x418e09` | Traduit / vérifié | `0xf525c` |
| `0x418e47` | Traduit / vérifié | `0x3e2464` |
| `0x418e52` | Traduit / vérifié | `0x3e2470` |
| `0x418e5c` | Traduit / vérifié | `0x3e247c` |
| `0x418e69` | Traduit / vérifié | `0x3e2488` |
| `0x418e77` | Traduit / vérifié | `0x9fb64` |
| `0x418e8d` | Traduit / vérifié | `0xc06a4`, `0xc1e74`, `0xc285c` |
| `0x418e95` | Traduit / vérifié | `0xc06fc`, `0xc50c0` |
| `0x418e9e` | Traduit / vérifié | `0xc1b28` |
| `0x418ea7` | Traduit / vérifié | `0xc06d8`, `0xc12e4` |
| `0x418eb0` | Conservé / vérifié | `0xc0fd4`, `0xc1698`, `0xc4ffc`, `0xc50e8` |
| `0x418eb5` | Traduit / vérifié | `0xc05d8`, `0xc12e0`, `0xc283c`, `0xc4fe8` |
| `0x418ebc` | Traduit / vérifié | `0xc1110` |
| `0x418ec3` | Traduit / vérifié | `0xc191c`, `0xc1958`, `0x1ec1dd0`, `0x1ec1dfc` |
| `0x418ecb` | Traduit / vérifié | `0x3f1b44` |
| `0x418f3a` | Traduit / vérifié | `0x3f1b50` |
| `0x418fb8` | Traduit / vérifié | `0x3f1b5c` |
| `0x41901c` | Traduit / vérifié | `0x3f1b68` |
| `0x41908e` | Traduit / vérifié | `0x3f1b74` |
| `0x419103` | Traduit / vérifié | `0x3f1b80` |
| `0x41917d` | Traduit / vérifié | `0x3f1b8c` |
| `0x419201` | Traduit / vérifié | `0x3f1b98` |
| `0x41926d` | Traduit / vérifié | `0x3f1ba4` |
| `0x4192e2` | Traduit / vérifié | `0x3f1bb0` |
| `0x41935b` | Traduit / vérifié | `0x3f1bbc` |
| `0x4193d5` | Traduit / vérifié | `0x3f1bc8` |
| `0x419444` | Traduit / vérifié | `0x3f1bd4` |
| `0x4194c9` | Traduit / vérifié | `0x3f1be0` |
| `0x41953f` | Traduit / vérifié | `0x3f1bec` |
| `0x4195ac` | Traduit / vérifié | `0x3f1bf8` |
| `0x419629` | Traduit / vérifié | `0x3f1c04` |
| `0x41969d` | Traduit / vérifié | `0x3f1c10` |
| `0x41971a` | Traduit / vérifié | `0x3f1c1c` |
| `0x419782` | Traduit / vérifié | `0x137820` |
| `0x41979d` | Traduit / vérifié | `0x1377e8` |
| `0x4197b8` | Traduit / vérifié | `0x1376bc`, `0x1377cc`, `0x1378dc` |
| `0x4197ed` | Traduit / vérifié | `0x1376b0`, `0x1377c0`, `0x1378d0` |
| `0x419822` | Traduit / vérifié | `0x137714` |
| `0x419841` | Traduit / vérifié | `0x1376d8` |
| `0x419860` | Traduit / vérifié | `0x1378b8`, `0x137934` |
| `0x41988a` | Traduit / vérifié | `0x1378f8` |
| `0x4198b4` | Traduit / vérifié | `0x137698` |
| `0x4198d5` | Traduit / vérifié | `0x13768c` |
| `0x41992f` | Traduit / vérifié | `0x137678` |
| `0x41996d` | Traduit / vérifié | `0x13766c` |
| `0x4199ab` | Traduit / vérifié | `0x1378a4` |
| `0x4199f4` | Traduit / vérifié | `0x137898` |
| `0x419a3d` | Traduit / vérifié | `0x463ed4` |
| `0x419a6e` | Exception justifiée | Ancienne origine œuf du voyageur sans pointeur ; remplacée dans la table œufs par le texte cadeau hors lot. Cible vivante 0x1f054ee, pointeur 0x463edc. |
| `0x419aa2` | Traduit / vérifié | `0x463ee4` |
| `0x419ade` | Traduit / vérifié | `0x463ee8` |
| `0x419b18` | Traduit / vérifié | `0x463ed8`, `0x463ee0`, `0x463eec` |
| `0x419b44` | Traduit / vérifié | `0x463ec4` |
| `0x419b7b` | Traduit / vérifié | `0x463ec8` |
| `0x419bae` | Traduit / vérifié | `0x463ecc` |
| `0x419bdb` | Traduit / vérifié | `0x463ed0` |
| `0x419c0b` | Traduit / vérifié | `0x137660`, `0x13788c` |
| `0x419c13` | Exception justifiée | Somewhere sans pointeur ; le résumé charge unknown location via le littéral 0x137618 (instruction LDR 0x13760a). Cible vivante 0xa4cab0, pointeur 0x137618. |
| `0x419c1d` | Traduit / vérifié | `0x137d78` |
| `0x419c2a` | Traduit / vérifié | `0x137d9c` |
| `0x419c39` | Traduit / vérifié | `0x134ff0`, `0x135320`, `0x137db4`, `0x137ddc`, `0x137e1c` |
| `0x419c45` | Traduit / vérifié | `0x1350e0`, `0x1353a8`, `0x137e00`, `0x137e24` |
| `0x419c4d` | Exception justifiée | Treize octets 00 de remplissage devant Confirm ; le consommateur 0x3cc32c vise 0x419c5a. Pointeurs du texte propriétaire : 0x3cc32c. |
| `0x419c5a` | Traduit / vérifié | `0x3cc32c` |
| `0x419c62` | Traduit / vérifié | `0x137d80` |
| `0x419c72` | Traduit / vérifié | `0x137d88` |
| `0x419c7b` | Traduit / vérifié | `0x137da0` |
| `0x419c82` | Traduit / vérifié | `0x135324`, `0x137db8` |
| `0x419c92` | Traduit / vérifié | `0x135000`, `0x137de8` |
| `0x419ca2` | Traduit / vérifié | `0x13500c`, `0x137dfc` |
| `0x419ca9` | Traduit / vérifié | `0x137e20` |
| `0x419cb9` | Traduit / vérifié | `0x139708` |
| `0x419cda` | Traduit / vérifié | `0x89f54` |
| `0x419ce1` | Traduit / vérifié | `0x89fcc`, `0x1ed8e84` |
| `0x419ce7` | Exception justifiée | Money sans pointeur ; la Carte utilise Wallet hors lot, références 0x8a07c et 0x8a0dc. Cible vivante 0x1f21c78, pointeur 0x8a07c. |
| `0x419cef` | Conservé / vérifié | `0x8a1ac`, `0x8a224` |
| `0x419cfd` | Traduit / vérifié | `0x8a2d4`, `0x8a3ac` |
| `0x419d0a` | Traduit / vérifié | `0x8a4f8` |
| `0x419d1a` | Traduit / vérifié | `0x8a6c0` |
| `0x419d2f` | Traduit / vérifié | `0x3cd944` |
| `0x419d3c` | Traduit / vérifié | `0x3cd948` |
| `0x419d4f` | Traduit / vérifié | `0x8a750` |
| `0x419d57` | Traduit / vérifié | `0x8a848` |
| `0x419d66` | Traduit / vérifié | `0x8a9e4` |
| `0x419d7d` | Conservé / vérifié | `0x8a914` |
| `0x419d89` | Traduit / vérifié | `0x893b0` |
| `0x419dcc` | Traduit / vérifié | `0x88c08` |
| `0x419dd3` | Traduit / vérifié | `0x3cc314` |
| `0x419dde` | Traduit / vérifié | `0x3cc318` |
| `0x419deb` | Traduit / vérifié | `0x3cc31c`, `0x1fb393c` |
| `0x419df8` | Traduit / vérifié | `0x3cc320` |
| `0x419dfe` | Traduit / vérifié | `0x3cc324` |
| `0x419e0a` | Traduit / vérifié | `0x3cc328`, `0x1ebc42c`, `0x1fb37dc` |
| `0x419e17` | Traduit / vérifié | `0x3cc330` |
| `0x419e1c` | Traduit / vérifié | `0x3cc334` |
| `0x419e20` | Traduit / vérifié | `0x3cc338` |
| `0x419e25` | Traduit / vérifié | `0x3cc33c` |
| `0x419e28` | Traduit / vérifié | `0x3cc340` |
| `0x419e2c` | Traduit / vérifié | `0x3cc344`, `0x1fb3a28` |
| `0x419e32` | Traduit / vérifié | `0x3cc348`, `0x1fb3a2c` |
| `0x419e36` | Conservé / vérifié | `0x3cc34c`, `0x1fb3a6c` |
| `0x419e3b` | Traduit / vérifié | `0x3cc350`, `0x1fb3a70` |
| `0x419e46` | Traduit / vérifié | `0x3cc354` |
| `0x419e4b` | Conservé / vérifié | `0x3cc35c`, `0x1fb3a64` |
| `0x419e4f` | Conservé / vérifié | `0x3cc358` |
| `0x419e52` | Traduit / vérifié | `0x88af8` |
| `0x419e57` | Traduit / vérifié | `0x886cc` |
| `0x419f54` | Traduit / vérifié | `0x54100`, `0x6fc74`, `0xf2214`, `0x14d148`, `0x155acc`, `0x9f2508` |
| `0x419f76` | Traduit / vérifié | `0x3a7394` |
| `0x419fbb` | Traduit / vérifié | `0x3a7398` |
| `0x41a001` | Traduit / vérifié | `0x3a739c` |
| `0x41a049` | Traduit / vérifié | `0x3a73a0`, `0x3a73b4` |
| `0x41a06f` | Traduit / vérifié | `0x3a73a4` |
| `0x41a0b7` | Traduit / vérifié | `0x3a73a8` |
| `0x41a0f9` | Traduit / vérifié | `0x3a73ac` |
| `0x41a111` | Traduit / vérifié | `0x3a73b0` |
| `0x41a155` | Traduit / vérifié | `0x111128` |
| `0x41a16f` | Traduit / vérifié | `0x113f7c` |
| `0x41a193` | Traduit / vérifié | `0x11437c` |
| `0x41a1cd` | Traduit / vérifié | `0x1142e0` |

## Validation reproductible

```sh
make build-pt
python3 -m pytest tests/unit/pt/test_batch_pt13.py tests/unit/test_translation_integrity.py -q
python3 -m pytest tests/e2e/pt/test_batch_pt13_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt13.config.ts
```

## Non vérifié

La preuve visuelle ciblée ne certifie pas tous les parcours, les fonctions Link
avec un second joueur ou le jeu complet. La certification globale appartient à
T-848. Aucun push, aucune publication et aucun pipeline distant ne sont lancés.
