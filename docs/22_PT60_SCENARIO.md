# 22 — PT-60 : scénario étendu, tenues, missions et crédits

F-819. Prérequis F-758 et F-759 intégrés. Source anglaise ROM vierge, comparaison FR au même offset ; glossaire officiel PT-BR figé respecté.

Le manifeste explicite de 299 offsets reste la seule frontière du lot. Les domaines réels sont Blizzard City, Cinder Volcano, Cootes Bog, Crystal Peak, Crater Town et son histoire/les quêtes ADM, les tenues et les crédits.

296 entrées sont livrées ou conservées. Trois exceptions ne sont pas ajoutées au combined : deux textes de déverrouillage de tenue sans consommateur référencé (le menu utilise le message voisin), et un remplissage d’alignement Thumb avant Crater Town. Les références témoins figurent ci-dessous et dans le bilan JSON.

Les extractions 0x1eedcfb, 0x1eee8be et 0x1eeeccc sont tronquées à environ 512 octets. Le texte ROM complet est traduit, sans copier les omissions ou erreurs FR. Les nombres, recettes, trois Carbink et trois Light Clay, noms propres anglais et attributions sont préservés.

Le finaliseur batch_60 conserve exactement toutes les pages, pauses, couleurs et variables ainsi que le nombre de sauts souples. Il réutilise StructuredTextPatch via BorriusTextPatch. Il écrit le titre des tenues dans sa cellule fixe de 13 octets, conserve son espace initial et son pointeur vers +1. Les motifs de pointeurs dans les échantillons audio PCM sont exclus et restaurés si le build générique les a modifiés. Aucun code partagé ni texte hors lot modifié.

Le JSON languages/pt/data/pt60_audit.json est le bilan détaillé : préimage binaire complète, pointeurs, exceptions, texte live, octets encodés, pixels et statut pour chaque offset. Les tests relisent ces données contre la source et la ROM reconstruite.

La preuve Playwright utilise trois messages aux pointeurs de la ROM finale dans une copie temporaire mGBA, sans changer les textes ni les polices. Elle vérifie les premières lignes via OCR et conserve le fichier de sauvegarde inchangé. Elle ne prétend pas jouer les 296 entrées ni parcourir le générique des crédits.

| Offset | Décision | Pointeurs vivants / témoins | Justification |
|---|---|---|---|
| `0x1eea2fe` | Traduit / vérifié | `0x1e57166`, `0x1e57231` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea32f` | Traduit / vérifié | `0x1e57189` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea374` | Traduit / vérifié | `0x1e571b9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea459` | Traduit / vérifié | `0x1e571d4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea4d4` | Traduit / vérifié | `0x1e572a9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea4ed` | Traduit / vérifié | `0x1e572b4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea55d` | Traduit / vérifié | `0x1e572bf` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea61b` | Traduit / vérifié | `0x1e572d3` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea6f9` | Traduit / vérifié | `0x1e576ba` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea727` | Traduit / vérifié | `0x1e576c9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea777` | Traduit / vérifié | `0x1e576d7` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eea888` | Traduit / vérifié | `0x1e572e0`, `0x1e573aa`, `0x1e5744d` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eea892` | Traduit / vérifié | `0x1e572f0`, `0x1e57491`, `0x1e57541` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eea89c` | Traduit / vérifié | `0x1e57300`, `0x1e5757c`, `0x1e57635` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eea8a9` | Traduit / vérifié | `0x1e572ec` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eea909` | Traduit / vérifié | `0x1e572fc` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eea96a` | Traduit / vérifié | `0x1e5730c` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eea9d0` | Traduit / vérifié | `0x1e57384` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaa17` | Traduit / vérifié | `0x1e5746b`, `0x1e57556` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaa60` | Traduit / vérifié | `0x1e573b6` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaa8c` | Traduit / vérifié | `0x1e5739d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeab6e` | Traduit / vérifié | `0x1e57484` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeac10` | Traduit / vérifié | `0x1e5756f` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeac9d` | Traduit / vérifié | `0x1e57459` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeacda` | Traduit / vérifié | `0x1e573f5`, `0x1e574e4`, `0x1e575d9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eead21` | Traduit / vérifié | `0x1e57413`, `0x1e57507`, `0x1e57601` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eead3d` | Traduit / vérifié | `0x1e57427`, `0x1e5751b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeada2` | Traduit / vérifié | `0x1e5760f` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeae25` | Traduit / vérifié | `0x1e57641` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeae85` | Traduit / vérifié | `0x1e5737b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaee2` | Conservé / vérifié | `0x1e57397`, `0x1e573bf`, `0x1e5740d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaf0d` | Conservé / vérifié | `0x1e5747e`, `0x1e5749e`, `0x1e57501` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaf4d` | Conservé / vérifié | `0x1e57569`, `0x1e57588`, `0x1e575fb` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeaf9c` | Traduit / vérifié | `0x1e57421` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeafa5` | Traduit / vérifié | `0x1e57515` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeafa9` | Traduit / vérifié | `0x1e57705` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb03c` | Traduit / vérifié | `0x1e57712` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb152` | Traduit / vérifié | `0x1e57720` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb1ce` | Traduit / vérifié | `0x1e57733` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb2fe` | Traduit / vérifié | `0x1e5779b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb33a` | Traduit / vérifié | `0x1e577a8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb3ae` | Traduit / vérifié | `0x1e577b5` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb420` | Traduit / vérifié | `0x1e5776c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb463` | Traduit / vérifié | `0x1e5778e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb4c3` | Traduit / vérifié | `0x1e577ef` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb532` | Traduit / vérifié | `0x1e577f9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb5c5` | Traduit / vérifié | `0x1e5780c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb63c` | Traduit / vérifié | `0x1e5783e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb67a` | Traduit / vérifié | `0x1e57860` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb6cf` | Traduit / vérifié | `0x1e57876` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb752` | Traduit / vérifié | `0x1e5794c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb784` | Traduit / vérifié | `0x1e57985` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb7b0` | Traduit / vérifié | `0x1e578eb` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb86c` | Traduit / vérifié | `0x1e579bc` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb88b` | Traduit / vérifié | `0x1e579cd` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb8a5` | Traduit / vérifié | `0x1e579da` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeb8c0` | Conservé / vérifié | `0x1fb3e4c`, `0x1fb46f8` | Nom propre anglais conservé selon F-759, pointeurs vérifiés. |
| `0x1eeb8ce` | Traduit / vérifié | `0x1fb46fc` | Description de lieu sur quatre lignes ; pointeur de la table carte vérifié. |
| `0x1eeb940` | Conservé / vérifié | `0x1e61520`, `0x1e76cd4`, `0x1e93a4c`, `0x1eaf9a4`, `0x1eaf9b4`, `0x1eaf9c4`, `0x1fb3e1c`, `0x1fb46b0` | Nom propre anglais conservé selon F-759, pointeurs vérifiés. |
| `0x1eeb94f` | Traduit / vérifié | `0x1fb46b4` | Description de lieu sur quatre lignes ; pointeur de la table carte vérifié. |
| `0x1eeb9bb` | Conservé / vérifié | `0x1e589cd` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eeb9c5` | Conservé / vérifié | `0x1e582fe`, `0x1e58375` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eeb9db` | Conservé / vérifié | `0x1e5a007` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eeb9ec` | Traduit / vérifié | `0x1e58254` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeba2a` | Traduit / vérifié | `0x1e58a22`, `0x1e6e1a1`, `0x1e97d77` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeba3f` | Traduit / vérifié | `0x1e58353`, `0x1e583ca` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeba5e` | Traduit / vérifié | `0x1e5a05c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeba7c` | Traduit / vérifié | `0x1e58993`, `0x1e6e112`, `0x1e97ce8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeba8c` | Conservé / vérifié | `0x1e589a6` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eeba9f` | Traduit / vérifié | `0x1e59f9f` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebadf` | Traduit / vérifié | `0x1e58173` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebaf4` | Traduit / vérifié | `0x1e58192` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebb48` | Traduit / vérifié | `0x1e5819f` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebbe5` | Traduit / vérifié | `0x1e59832` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebc4f` | Traduit / vérifié | `0x1e59845` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebc81` | Traduit / vérifié | `0x1e59857`, `0x1e9be9b`, `0x1e9c8c0` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebcd1` | Traduit / vérifié | `0x1e5a076` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebd06` | Traduit / vérifié | `0x1e5a07a` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebd2b` | Traduit / vérifié | `0x1e5a080` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebd7f` | Traduit / vérifié | `0x1e5a08d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebdb7` | Traduit / vérifié | `0x1e5a091` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebddf` | Traduit / vérifié | `0x1e5a097` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebe40` | Traduit / vérifié | `0x1e5a0a4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebea2` | Traduit / vérifié | `0x1e5a0a8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebecc` | Traduit / vérifié | `0x1e5a0ae` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebeed` | Traduit / vérifié | `0x1e5a0bb` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebf12` | Traduit / vérifié | `0x1e5a0c5` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebf47` | Traduit / vérifié | `0x1e5a0d2` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebf71` | Traduit / vérifié | `0x1e5a0d6` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebf99` | Traduit / vérifié | `0x1e5a0dc` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eebfe5` | Traduit / vérifié | `0x1e5a0e9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec04a` | Traduit / vérifié | `0x1e5a0ed` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec073` | Traduit / vérifié | `0x1e5a0f3` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec0ef` | Traduit / vérifié | `0x1e5a100` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec140` | Traduit / vérifié | `0x1e5a104` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec160` | Traduit / vérifié | `0x1e5a10a` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec1a7` | Traduit / vérifié | `0x1e5a117` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec1f4` | Traduit / vérifié | `0x1e5a11b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec211` | Traduit / vérifié | `0x1e5a121` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec24d` | Traduit / vérifié | `0x1e5a12e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec26f` | Traduit / vérifié | `0x1e5a132` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec292` | Traduit / vérifié | `0x1e5a138` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec2c0` | Traduit / vérifié | `0x1e5a145` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec2da` | Traduit / vérifié | `0x1e5a149` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec300` | Traduit / vérifié | `0x1e5a14f` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec33b` | Traduit / vérifié | `0x1e5a15c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec37e` | Traduit / vérifié | `0x1e5a160` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec393` | Traduit / vérifié | `0x1e5a166` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec40e` | Traduit / vérifié | `0x1e5a17d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec44b` | Traduit / vérifié | `0x1e5a191` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec465` | Traduit / vérifié | `0x1e5a1a0` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec4cf` | Traduit / vérifié | `0x1e5a1c2` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec53e` | Traduit / vérifié | `0x1e5a23c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec628` | Traduit / vérifié | `0x1e5a1e9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec6ad` | Traduit / vérifié | `0x1e5a202` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec6e6` | Traduit / vérifié | `0x1e5a211` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec6f1` | Traduit / vérifié | `0x1e5a233` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec787` | Traduit / vérifié | `0x1e5a738`, `0x1e5a78a`, `0x1e5a7df` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eec79b` | Traduit / vérifié | `0x1e5a744` | Titre ou objectif de mission ; noms des ingrédients anglais conservés suivant F-759. |
| `0x1eec801` | Traduit / vérifié | `0x1e5a76a` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec8f1` | Traduit / vérifié | `0x1e5a7eb` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec98e` | Traduit / vérifié | `0x1e5a77d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eec9fa` | Traduit / vérifié | `0x1e5a7f4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeca40` | Traduit / vérifié | `0x1e5a7a4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecaac` | Traduit / vérifié | `0x1e5a7c3` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecad0` | Traduit / vérifié | `0x1e5a7d1` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecb0d` | Traduit / vérifié | `0x1e5a7fd` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecb70` | Traduit / vérifié | `0x1e5a806` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecbb6` | Traduit / vérifié | `0x1e5a813`, `0x1e5a83a` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecc0a` | Traduit / vérifié | `0x1e5a817`, `0x1e5a83e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecc46` | Traduit / vérifié | `0x1e5a82d`, `0x1e5a844` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeccbe` | Traduit / vérifié | `0x1e5a851`, `0x1e5a878` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeccf4` | Traduit / vérifié | `0x1e5a855`, `0x1e5a87c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecd36` | Traduit / vérifié | `0x1e5a86b`, `0x1e5a882` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecd76` | Traduit / vérifié | `0x1e5a88f`, `0x1e5a8b6` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecdb7` | Traduit / vérifié | `0x1e5a893`, `0x1e5a8ba` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eece02` | Traduit / vérifié | `0x1e5a8a9`, `0x1e5a8c0` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eece4e` | Traduit / vérifié | `0x1e5a8cd`, `0x1e5a8f4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eece8a` | Traduit / vérifié | `0x1e5a8d1`, `0x1e5a8f8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeceaf` | Traduit / vérifié | `0x1e5a8e7`, `0x1e5a8fe` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecee9` | Traduit / vérifié | `0x1e5a90b`, `0x1e5a932` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecf35` | Traduit / vérifié | `0x1e5a90f`, `0x1e5a936` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecf69` | Traduit / vérifié | `0x1e5a925`, `0x1e5a93c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecfbc` | Traduit / vérifié | `0x1e5a949`, `0x1e5a970` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eecfee` | Traduit / vérifié | `0x1e5a94d`, `0x1e5a974` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed011` | Traduit / vérifié | `0x1e5a963`, `0x1e5a97a` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed046` | Traduit / vérifié | `0x1e5a987`, `0x1e5a9ae` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed07f` | Traduit / vérifié | `0x1e5a98b`, `0x1e5a9b2` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed0c2` | Traduit / vérifié | `0x1e5a9a1`, `0x1e5a9b8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Occurrences dans les échantillons audio PCM exclues des consommateurs et préservées octet pour octet. |
| `0x1eed116` | Traduit / vérifié | `0x1e5a9c5`, `0x1e5a9ec` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed148` | Traduit / vérifié | `0x1e5a9c9`, `0x1e5a9f0` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed170` | Traduit / vérifié | `0x1e5a9df`, `0x1e5a9f6` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed1b3` | Traduit / vérifié | `0x1eb25b4` | Titre costume : cellule fixe 13 octets, espace initial préservé ; pointeur vivant vers +1 à 0x1eb25b4. |
| `0x1eed1c0` | Traduit / vérifié | `0x1eb25c0` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Occurrences dans les échantillons audio PCM exclues des consommateurs et préservées octet pour octet. |
| `0x1eed1d8` | Traduit / vérifié | `0x1eb20ec` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed1fd` | Exception | `0x1eb20ec` | Ancienne description de costume sans pointeur direct ou intérieur. La branche verrouillée 0x1eb2026 charge exclusivement le littéral 0x1eb20ec vers 0x1eed1d8 ; rendu sans calcul d’adresse. La table costumes 0x1fb0d08 (5 cellules de 28 octets) ne comporte pas de description. |
| `0x1eed247` | Exception | `0x1eb20ec` | Ancienne description de costume sans pointeur direct ou intérieur. La branche verrouillée 0x1eb2026 charge exclusivement le littéral 0x1eb20ec vers 0x1eed1d8 ; rendu sans calcul d’adresse. La table costumes 0x1fb0d08 (5 cellules de 28 octets) ne comporte pas de description. |
| `0x1eed28a` | Traduit / vérifié | `0x1eb20f8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed2ce` | Traduit / vérifié | `0x1eb1c90` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Occurrences dans les échantillons audio PCM exclues des consommateurs et préservées octet pour octet. |
| `0x1eed30f` | Traduit / vérifié | `0x1eb1f3c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed316` | Traduit / vérifié | `0x1eb1f40` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed323` | Conservé / vérifié | `0x1e869f5`, `0x1fb0d8c` | Nom propre anglais conservé selon F-759, pointeurs vérifiés. |
| `0x1eed329` | Conservé / vérifié | `0x1e86a81`, `0x1fb0d90` | Nom propre anglais conservé selon F-759, pointeurs vérifiés. |
| `0x1eed32e` | Exception | `0x1eaf544`, `0x1eaf9e4` | Artefact d’extraction : les deux octets C0 46 forment le NOP Thumb MOV r8,r8 qui aligne Crater Town à 0x1eed330 après Lyra/FF. Les scripts 0x1eaf544 et 0x1eaf9e4 lisent ce nom propre à +2. Aucun texte dans le préfixe ; aucun offset hors lot modifié. |
| `0x1eed33c` | Conservé / vérifié | `0x1fb3cfc` | Nom propre anglais conservé selon F-759, pointeurs vérifiés. |
| `0x1eed34a` | Conservé / vérifié | `0x1fb3d04` | Nom propre anglais conservé selon F-759, pointeurs vérifiés. |
| `0x1eed358` | Traduit / vérifié | `0x1e5acaf` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed448` | Traduit / vérifié | `0x1e5acb9` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed4eb` | Traduit / vérifié | `0x1e5accc` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed690` | Traduit / vérifié | `0x1e5acd5` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed7f3` | Traduit / vérifié | `0x1e5acea` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed84f` | Traduit / vérifié | `0x1e5acf7` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed8f7` | Traduit / vérifié | `0x1e5ad01` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed972` | Traduit / vérifié | `0x1e5ad1d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eed9fd` | Traduit / vérifié | `0x1e5ad14`, `0x1e5ad30` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeda20` | Traduit / vérifié | `0x1e5ad39` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeda3f` | Traduit / vérifié | `0x1e5ad42` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeda96` | Traduit / vérifié | `0x1e5ad80`, `0x1e5add3`, `0x1e5ae42` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eedaa2` | Traduit / vérifié | `0x1e5ad98` | Objectif ADM : portes effondrées, nombre dynamique de Carbink ; trois lignes de mission. |
| `0x1eedb03` | Traduit / vérifié | `0x1e5ae57` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eedc0b` | Traduit / vérifié | `0x1e5adb3` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eedcfb` | Traduit / vérifié | `0x1e5adc6` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Source EN extraite tronquée : traduction du texte complet de la ROM, vérifiée contre FR. |
| `0x1eedf0b` | Traduit / vérifié | `0x1e5ae60` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eedf8d` | Traduit / vérifié | `0x1e5ae0b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee174` | Traduit / vérifié | `0x1e5ae14` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee1c7` | Traduit / vérifié | `0x1e5ae35`, `0x1e5ae4e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee265` | Conservé / vérifié | `0x1e78476` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eee277` | Conservé / vérifié | `0x1e78507`, `0x1e7857e` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eee292` | Traduit / vérifié | `0x1e7855c`, `0x1e785d3` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee2af` | Traduit / vérifié | `0x1e5aeb0` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee2f8` | Traduit / vérifié | `0x1e5aece` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee34b` | Traduit / vérifié | `0x1e5aeec` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee39e` | Traduit / vérifié | `0x1e5af0a` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee3dd` | Traduit / vérifié | `0x1e5af13` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee413` | Traduit / vérifié | `0x1e5b0cd`, `0x1eaa542`, `0x1eaa576` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee417` | Traduit / vérifié | `0x1e5b0fc`, `0x1eaa49b`, `0x1eaa50b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee420` | Traduit / vérifié | `0x1e5b000` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee478` | Traduit / vérifié | `0x1e5b013` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee4d9` | Traduit / vérifié | `0x1e5b01c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Occurrences dans les échantillons audio PCM exclues des consommateurs et préservées octet pour octet. |
| `0x1eee521` | Traduit / vérifié | `0x1e5b03c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee5e3` | Traduit / vérifié | `0x1e5b049` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee5ef` | Traduit / vérifié | `0x1e5b050` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee606` | Traduit / vérifié | `0x1e5b090` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee6ed` | Traduit / vérifié | `0x1e5b0d8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee728` | Traduit / vérifié | `0x1e5b107` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee778` | Traduit / vérifié | `0x1e5b114` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee7ce` | Traduit / vérifié | `0x1e5b14b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee807` | Traduit / vérifié | `0x1e5b158` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee85d` | Traduit / vérifié | `0x1e5b165` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee896` | Traduit / vérifié | `0x1e5b179` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee8a0` | Traduit / vérifié | `0x1fb553c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee8a5` | Traduit / vérifié | `0x1fb5540` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee8aa` | Traduit / vérifié | `0x1fb5544` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee8b0` | Traduit / vérifié | `0x1fb5548` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee8b7` | Traduit / vérifié | `0x1fb554c` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eee8be` | Traduit / vérifié | `0x1e5b206` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Source EN extraite tronquée : traduction du texte complet de la ROM, vérifiée contre FR. |
| `0x1eeeccc` | Traduit / vérifié | `0x1e5b1cb` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. Source EN extraite tronquée : traduction du texte complet de la ROM, vérifiée contre FR. |
| `0x1eeef16` | Traduit / vérifié | `0x1e5b214` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeef5b` | Traduit / vérifié | `0x1e5b1de` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eeef6d` | Traduit / vérifié | `0x1e5b1f8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef037` | Traduit / vérifié | `0x1e5b222` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef11e` | Traduit / vérifié | `0x1e5b230` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef1ff` | Traduit / vérifié | `0x1e5b23e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef27e` | Traduit / vérifié | `0x1e5b260` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef29d` | Traduit / vérifié | `0x1e5b294` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef2de` | Traduit / vérifié | `0x1e5b326` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef3a9` | Traduit / vérifié | `0x1e5b356`, `0x1ea1d7b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef402` | Traduit / vérifié | `0x1e5b3e4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef422` | Traduit / vérifié | `0x1e5b369`, `0x1ea1d8e`, `0x1ea1e50` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef440` | Traduit / vérifié | `0x1e5b399`, `0x1ea1dc1` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef45b` | Traduit / vérifié | `0x1e5b3b5`, `0x1ea1ddd` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef488` | Traduit / vérifié | `0x1e5b3bd`, `0x1ea1de8` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef4ca` | Traduit / vérifié | `0x1e5b42e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef507` | Traduit / vérifié | `0x1e5b3ca`, `0x1ea1df8`, `0x1ea1ec3`, `0x1ea1f56` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef540` | Traduit / vérifié | `0x1e5b3d7`, `0x1ea1e08`, `0x1ea1ed0`, `0x1ea1f66` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef587` | Traduit / vérifié | `0x1e5b450` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef5dd` | Traduit / vérifié | `0x1e5b47e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef6d0` | Traduit / vérifié | `0x1e5b487` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef808` | Traduit / vérifié | `0x1e5b490` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eef903` | Traduit / vérifié | `0x1e5b45e` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefa68` | Traduit / vérifié | `0x1e5b499` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefaab` | Conservé / vérifié | `0x1e5b4c8` | Cri de Pokémon ou formule propre au scénario conservé ; pointeur de script vivant. |
| `0x1eefab6` | Traduit / vérifié | `0x1e5b521` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefaca` | Traduit / vérifié | `0x1e5b52b` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefbb4` | Traduit / vérifié | `0x1e5b545` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefc99` | Traduit / vérifié | `0x1e5b559` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefcc9` | Traduit / vérifié | `0x1e5b58d` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefd15` | Traduit / vérifié | `0x1e5b5b4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefd30` | Traduit / vérifié | `0x1e5b5d7` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefd4a` | Traduit / vérifié | `0x1e5b5e7` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefd94` | Traduit / vérifié | `0x1e5b5f4` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefddb` | Traduit / vérifié | `0x1e5b605` | Dialogue/scénario : pointeurs de scripts vivants, commandes et pages préservées. |
| `0x1eefe60` | Conservé / vérifié | `0x1fb0dc0` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eefe8c` | Conservé / vérifié | `0x1fb0dcc` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eefebf` | Conservé / vérifié | `0x1fb0dd8` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eeff0b` | Traduit / vérifié | `0x1fb0dec` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eeff2a` | Conservé / vérifié | `0x1fb0df0` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eeff67` | Conservé / vérifié | `0x1fb0dfc` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eeff9b` | Conservé / vérifié | `0x1fb0e08` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eeffc2` | Traduit / vérifié | `0x1fb0e10` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1eeffde` | Conservé / vérifié | `0x1fb0e14` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0021` | Conservé / vérifié | `0x1fb0e20` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0081` | Conservé / vérifié | `0x1fb0e2c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef00d4` | Conservé / vérifié | `0x1fb0e38` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0122` | Conservé / vérifié | `0x1fb0e44` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0156` | Conservé / vérifié | `0x1fb0e50` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0194` | Conservé / vérifié | `0x1fb0e5c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef01d4` | Conservé / vérifié | `0x1fb0e68` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0237` | Conservé / vérifié | `0x1fb0e74` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef027d` | Conservé / vérifié | `0x1fb0e80` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef02c4` | Conservé / vérifié | `0x1fb0e8c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef02e2` | Conservé / vérifié | `0x1fb0e94` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0301` | Conservé / vérifié | `0x1fb0e98` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0335` | Conservé / vérifié | `0x1fb0ea0` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0354` | Conservé / vérifié | `0x1fb0ea4` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef03a1` | Conservé / vérifié | `0x1fb0eac` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef03c0` | Conservé / vérifié | `0x1fb0eb0` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef03f7` | Conservé / vérifié | `0x1fb0eb8` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. Occurrences dans les échantillons audio PCM exclues des consommateurs et préservées octet pour octet. |
| `0x1ef042d` | Traduit / vérifié | `0x1fb0ec4` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef044b` | Conservé / vérifié | `0x1fb0ec8` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0482` | Traduit / vérifié | `0x1fb0ed0` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef04a0` | Conservé / vérifié | `0x1fb0ed4` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef04d2` | Traduit / vérifié | `0x1fb0edc` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef04f0` | Conservé / vérifié | `0x1fb0ee0` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0546` | Conservé / vérifié | `0x1fb0eec` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef05db` | Conservé / vérifié | `0x1fb0ef8` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0621` | Conservé / vérifié | `0x1fb0f04` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0673` | Conservé / vérifié | `0x1fb0f10` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef06c7` | Conservé / vérifié | `0x1fb0f1c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef070f` | Conservé / vérifié | `0x1fb0f28` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0754` | Traduit / vérifié | `0x1fb0f30` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0770` | Conservé / vérifié | `0x1fb0f34` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef07b6` | Traduit / vérifié | `0x1fb0f3c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef07f5` | Conservé / vérifié | `0x1fb0f4c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef083b` | Conservé / vérifié | `0x1fb0f58` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0884` | Conservé / vérifié | `0x1fb0f64` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef08e2` | Conservé / vérifié | `0x1fb0f7c` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef0937` | Conservé / vérifié | `0x1fb0f88` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
| `0x1ef096a` | Conservé / vérifié | `0x1fb0f94` | Crédits : attributions et noms de projets conservés ; seuls les intitulés de fonction sont traduits, sauts exacts. |
