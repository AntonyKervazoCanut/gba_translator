# Audit et conception des releases BPS

## Conclusion révisée

Le premier passage adoptait le principe de publication de
`Simopich/unbound-translator` : des ROMs privées alimentaient encore la CI,
mais seuls les BPS en sortaient. Le suivi R-608 impose une contrainte plus
forte : **aucune ROM ne doit entrer dans la CI de build ou de release**.

Simopich ne satisfait pas cette contrainte. Son workflow télécharge une ROM
Unbound anglaise complète depuis `UNBOUND_ENGLISH_ROM_URL`, l'injecte, puis
supprime la cible temporaire après création du BPS. Notre flux devient donc
« patch-first » :

1. les quatre BPS validés sont versionnés avec leur manifeste et leurs
   checksums sous `patches/` ;
2. GitHub Actions vérifie et publie ce bundle sans secret, téléchargement ou
   création de ROM ;
3. les ROMs de test sont matérialisées uniquement en local en appliquant les
   BPS à une ROM anglaise obtenue légalement ;
4. la reconstruction complète et la promotion d'un nouveau bundle restent une
   opération mainteneur locale avec round-trip byte-perfect.

Le format IPS historique n'est pas adapté : son champ d'offset sur 24 bits ne
peut pas atteindre les modifications situées au-delà de `0xFFFFFF`, tandis que
Pokémon Unbound et ses traductions occupent 32 Mio. BPS adresse toute la ROM,
embarque les tailles ainsi que les CRC32 source/cible/patch, et permet donc de
refuser une mauvaise ROM source.

## État audité

- Avant cette migration, `.github/workflows/release.yml` téléversait les ROMs
  générées en artefacts GitHub Actions puis publiait les fichiers `.gba` dans
  une release mutable `latest`.
- Avant cette migration, `scripts/package_release.py` copiait les ROMs
  complètes, les compressait en ZIP et inscrivait leurs empreintes dans le
  manifeste local.
- Avant cette migration, `input/roms/*.gba` et
  `output/roms/GenedRom-fr.gba` étaient suivis par Git.
- Le build FR dépend de `patchedfrenchrom.gba` et de la référence espagnole ;
  les builds génériques dépendent de `englishrom.gba` et de la référence
  espagnole. Supprimer toute ROM du calcul imposerait une refonte du moteur,
  mais les conserver comme entrées privées et éphémères suffit à ne plus les
  distribuer.

## Architecture initiale remplacée

1. Chaque descripteur de langue buildable déclare explicitement la ROM anglaise
   propre comme source de patch. La base française dédiée reste un intrant du
   builder FR, mais n'est pas demandée à l'utilisateur final.
2. Le packager génère un BPS déterministe, le réapplique en mémoire et refuse
   la livraison si le résultat ne reproduit pas exactement la ROM construite.
3. Le manifeste contient les noms, tailles et SHA-256 de la source, de la cible
   et du patch. Aucun `.gba` ni ZIP de ROM n'entre dans `output/release/`.
4. La CI télécharge les trois ROMs depuis des secrets URL, exécute
   `make verify-roms`, construit chaque langue, crée son BPS puis supprime la
   cible `.gba` avant l'upload de l'artefact.
5. Chaque build publie une release persistante `v2.1.<numéro>` et remplace la
   release roulante `latest` avec les mêmes patchs. Les quatre langues sont
   requises avant toute publication ; leurs manifests sont agrégés et vérifiés
   dans `RELEASE_MANIFEST.json` et `SHA256SUMS.txt`.
6. Un rerun ne modifie jamais une version existante : il compare son commit et
   tous ses assets, puis reprend uniquement le remplacement de `latest`.

Cette architecture est remplacée par celle ci-dessous : conserver des ROMs
privées « éphémères » dans GitHub Actions reste une ROM en entrée du build.

## Architecture patch-first

### Bundle canonique

`patches/` contient exactement :

- `pokemon_unbound_fr.bps`
- `pokemon_unbound_it.bps`
- `pokemon_unbound_de.bps`
- `pokemon_unbound_indie.bps`
- `RELEASE_MANIFEST.json`
- `SHA256SUMS.txt`

Le manifeste porte le numéro de build stable. Chaque entrée lie les tailles,
SHA-256 et CRC32 de la source, de la cible et du BPS. Une validation sans ROM
peut ainsi prouver l'intégrité du fichier BPS, la cohérence de son pied CRC et
la couverture exacte du registre de langues. Le round-trip vers la cible
reste une preuve locale, puisqu'il exige nécessairement la source.

### Publication sans ROM

Le workflow démarre à chaque push sur `unbound` ou `master`, ainsi que sur demande.
Il attribue le numéro de publication `44 + github.run_number` : 44 réserve les
versions historiques déjà publiées. Ce décalage est fixe et ne doit pas être
recalculé depuis le manifeste. Des numéros peuvent être sautés après un échec.
Une nouvelle exécution reçoit un nouveau numéro ; un rerun conserve le même.
Le workflow lit séparément le numéro de build du manifeste et valide le bundle suivi.
`scripts/stamp_release_patches.py` inscrit ensuite le numéro de publication dans
chaque patch, sans ROM : l'écran NOT FOR SALE affiche `<LANGUE>.2.1.<release_number>`
et l'octet de version de l'en-tête GBA (`0xBC`) vaut `release_number & 0xFF`.
Notre encodeur n'émet que `SourceRead`/`TargetRead` : les octets modifiés par le
build sont littéraux dans le patch. Le tileset LZ77 de l'écran d'intro est
recompressé en place ; les seuls octets `SourceRead` qu'il touche appartiennent à
une zone `0xFF` de la ROM source épinglée par SHA-256
(`PINNED_SOURCE_FREE_RANGES`, vérifiée par `tests/test_release_stamp_rom.py`).
Le CRC32 de la cible est recalculé par linéarité ; tout octet non déductible
fait échouer la publication.

Le workflow publie quatre patchs réécrits nommés
`pokemon_unbound_<langue>_v2.1.<release_number>.bps`, avec un
`RELEASE_MANIFEST.json` et un `SHA256SUMS.txt` qui les décrivent sous ces noms.
Le manifeste publié ajoute `release_number` et, par langue, `stamped_from`
(build, SHA-256 du patch et de la cible canoniques) ; sa cible ne porte que la
taille et le CRC32, le SHA-256 exigeant la ROM complète. Les fichiers
canoniques de `patches/` restent inchangés.
Le workflow ne contient aucun secret de ROM,
`curl`, appel au builder ou chemin `.gba`. La version immuable est
`v2.1.<release_number>` ; `latest` est mis à jour sur place avec les mêmes noms
versionnés. Un groupe de concurrence sérialise les publications et le
workflow refuse de faire régresser `latest` vers un numéro de publication ou de build inférieur.
Les notes indiquent le build embarqué : un nouveau numéro de publication change
la version affichée en jeu, mais ne reconstruit pas les traductions et
n’inclut pas les changements source tant qu’un nouveau bundle n’a pas été
promu localement.

La CI publique conserve les suites Python sans ROM, Vitest et la validation du
bundle. Les jobs Python ROM et Playwright hébergés disparaissent : reproduire
une ROM sur un runner GitHub contredirait la contrainte d'absence de ROM en
entrée.

### Travail et E2E locaux

Le développeur place seulement la ROM anglaise Unbound compatible dans
`input/roms/englishrom.gba`. La commande de matérialisation :

1. valide le bundle suivi ;
2. vérifie la taille, le SHA-256 et le CRC32 de la source locale ;
3. applique le BPS demandé ;
4. vérifie la taille, le SHA-256 et le CRC32 de la cible ;
5. écrit la ROM éphémère sous `output/roms/`.

`make test-rom` matérialise les quatre langues avant pytest. Les commandes
Playwright matérialisent automatiquement la langue concernée avant de démarrer
l'émulateur. Aucun fichier `.gba` n'est suivi ou publié.

### Mise à jour des patchs

Après une modification de traduction ou de pipeline, un mainteneur possédant
les entrées locales historiques exécute le build complet, le packaging BPS
avec un nouveau `BUILD_NUMBER`, les tests ROM/E2E, puis la promotion vers
`patches/`. La promotion refuse un numéro non positif, un bundle incomplet,
un patch corrompu ou une cible qui ne reproduit pas exactement le build local.
`make test-private-build` conserve séparément la preuve de déterminisme du
builder FR ; `make test-rom` valide l'artefact matérialisé depuis le bundle.

## Configuration CI requise

Aucun secret ou stockage privé de ROM n'est requis. Seul
`GITHUB_TOKEN`, fourni nativement au workflow avec la permission
`contents: write`, sert à publier les releases.

## Limite historique

Retirer les ROMs du nouvel état Git empêche toute nouvelle distribution, mais
ne les efface pas des anciens commits ni des anciennes releases. Une purge de
l'historique Git et des assets historiques demanderait une opération distante
destructive et coordonnée ; elle est volontairement hors de cette migration.
