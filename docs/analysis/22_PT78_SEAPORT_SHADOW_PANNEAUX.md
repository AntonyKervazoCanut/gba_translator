# PT-78 — Seaport City, Shadow Base et panneaux de Borrius

Le manifeste PT-78 fait seul autorité : 299 offsets, de `0x1f6ae93` à
`0x1f716cf`. Les prérequis F-758 et F-759 sont intégrés. La ROM anglaise source
est identifiée par SHA256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.

## Livraison et bilan individuel

`languages/pt/data/pt78_audit.json` contient **une fiche par offset**, dans
l'ordre exact du manifeste : références EN et FR, anglais ROM intégral,
préimage binaire, pointeurs consommateurs et leur contexte, texte PT-BR,
commandes, longueur encodée, mesures des cinq polices et tampons développés,
statut et justification.

- 247 textes traduits : services et missions de Seaport, reproduction,
  Nursery, ADM/minage, S.S. Marine, Camomons, Shadow Base, Zeph et panneaux.
- 50 chaînes conservées et vérifiées : noms propres, espèces, objets et
  panneaux purement directionnels, conformément au glossaire F-759. Les noms
  de Plates ne reçoivent pas de traduction officielle inventée.
- Deux exceptions, détaillées ci-dessous. Aucune traduction existante supprimée.
- Les 297 valeurs vivantes ajoutées ont leur protection exacte dans le même
  manifeste YAML ; 320 références textuelles sont couvertes.

L'anglais intégral de `0x1f700f5` inclut la fin sur les combats Pokémon, tronquée
dans le corpus. La traduction couvre cette fin. Les noms et destinations des
panneaux sont contrôlés contre la ROM source, en complément des corpus EN/FR.

Les pages FB, défilements FA, couleurs FC, boutons F8 et tampons FD sont
conservés dans l'ordre. Seuls les retours souples FE sont redisposés pour tenir
dans les fenêtres. Les descriptions de missions et de lieu conservent leur
fenêtre de trois lignes ; les dialogues ont deux lignes initiales au plus,
puis une ligne par défilement. Le tampon natif FD0C des Shards ajoute ses
propres FA : le retour initial avant ce tampon reste explicite.

## Exceptions et faux pointeurs

| Offset | Justification binaire |
| --- | --- |
| `0x1f6b931` | Réplique Pumpkaboo sans aucune référence dans la ROM. Le script utilise `0x1f6b8ae` via `0x1e8e8f0`, puis le sélecteur de Pokémon ; le refus utilise `0x1f6b959` via `0x1e8e95c`. Pas d'invention de consommateur. |
| `0x1f70877` | Octet de bourrage `00` précédant le vrai début `0x1f70878`. Aucun pointeur vers le bourrage ; lecteur du panneau `0x1e93055` vers `0x1f70878`, traduit et vérifié dans le même lot. |

Trois occurrences binaires de valeurs ressemblant à des pointeurs sont des
échantillons PCM, et ne doivent jamais être repointées :

| Texte apparent | Faux pointeur | Début PCM | Taille échantillons | Pointeur d'instrument |
| --- | --- | --- | --- | --- |
| `0x1f6dde6` | `0x13084d0` | `0x13022a0` | 33016 octets | `0x104c440` |
| `0x1f6f1f9` | `0x117b3b6` | `0x117914c` | 10042 octets | `0x10501b4` |
| `0x1f6f602` | `0xb21c48` | `0xb2148c` | 4342 octets | `0x48ee14` |

Les tests vérifient les en-têtes, les instruments, l'appartenance aux échantillons
et leur préservation intégrale après build.

## Injection et budgets

Le finaliseur local `languages/pt/patches/batch_78.py` utilise le mécanisme
transactionnel existant de PT-63/PT-29. Il passe après les réparations, la police
et le repointage générique. Il réinjecte les valeurs exactes, y compris celles
ignorées ou réenveloppées par le constructeur générique, et restaure les trois
faux pointeurs PCM. Aucune modification du moteur partagé.

Les menus des Plates, choix de starters, titres de missions et libellés d'étages
ont des **pointeurs**, pas des cellules de caractères fixes : le finaliseur
couvre leurs consommateurs réels sans écrire dans un voisin. Aucun offset de
table fixe ignoré n'est revendiqué comme traduit. Le libellé du rez-de-chaussée
est borné à 32 pixels par prudence.

Les cinq polices natives sont mesurées après application du patch PT, avec
expansion des noms et des nombres ; budget maximal 192 pixels. Les fenêtres
fixes de missions sont limitées à trois lignes et 172 pixels, sans FA/FB.
Le tampon des
Shards est reconstruit selon les routines `0x1ec9640` et `0x1ec69f0` : quantité,
espace, nom d'objet, pluriel puis FA entre éléments ; suffixes source à
`0x1fb542c`. Les objectifs d'éclosion sont 10, 50 et 100 ; les compteurs courants
sont également éprouvés à 65535. Les tailles en octets sont consignées dans
l'audit ; la relocalisation permet de dépasser la longueur EN sans toucher
les chaînes voisines.

## Recette locale

```sh
python3 -m pytest tests/unit/pt/test_batch_pt78.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt78_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt78.config.ts
```

La preuve Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen` et Chromium
headless. Trois messages sont lus depuis les pointeurs de la ROM finale et
appelés par le moteur natif sur une copie temporaire. Les assertions OCR
vérifient leurs premières lignes, les octets exacts sont comparés avant rendu
et la sauvegarde temporaire doit rester inchangée. La capture finale est dans
le répertoire temporaire de l'OS et jointe au ticket ; aucune capture dans Git.

## Limites de vérification

Cette sonde n'est pas une navigation complète dans les 299 situations de jeu.
Les autres pages et les 320 références sont contrôlées en binaire, pas revendiquées
comme parcourues à l'écran. La certification complète du parcours et de la
release demeure le périmètre de T-848.
