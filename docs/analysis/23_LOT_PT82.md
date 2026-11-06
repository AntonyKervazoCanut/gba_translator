# PT-82 — échanges, Vivill Warehouse, Zygarde et Battle Frontier

## Périmètre et décisions

F-841 porte exclusivement sur les 300 offsets explicites de PT-82 dans
`languages/pt/translation_batches.json`. F-758 et F-759 sont intégrés. L'anglais
et le français au même offset ont été comparés ; les préimages anglaises de la
ROM font autorité pour les discours tronqués par le corpus texte.

Les zones réelles sont les échanges avec les habitants de Borrius, les indices
et dialogues de Vivill Warehouse, Vivill Woods, la recherche de Zygfried/Zygardia,
les 100 descriptions de cellules de Zygarde, puis Battle Circus et Battle Mine.
Les noms d'espèces, surnoms reçus, mouvements non attestés et noms propres de
Borrius restent anglais selon F-759. Les statistiques, Habilidade, movimentos,
Treinador et Batalha Individual/Dupla suivent le glossaire. Les lettres de la
senha restent A/K/L/O/V ; l'indice « commence par A » reste distinct.

## Bilan exhaustif

`languages/pt/data/pt82_audit.json` contient une ligne par offset, dans l'ordre du
manifeste : préimage complète, comparaison française, références texte et non
texte, statut, justification, texte PT exact et budgets mesurés. Les 297 entrées
vivantes sont protégées exactement : 274 traductions et 23 noms/cris conservés.
Aucune traduction existante n'est supprimée ou modifiée hors du lot.

Trois exceptions ne sont pas ajoutées au combined :

| Offset | Justification vérifiable |
| --- | --- |
| `0x1f85dfe` | Chaîne autonome sans pointeur vers le début ni l'intérieur. |
| `0x1f879ab` | Variante météo sans pointeur vers le début ni l'intérieur. |
| `0x1f88900` | Fragment de `0x1f8888d`, déjà traduit intégralement ; seul match à `0xeff2cb` dans les pixels 4bpp du sprite vivant `0xefee08`, pas un consommateur texte. |

Le match `0x1e4ae86` vers `0x1f857a5` est situé dans la wave delta-PCM vivante
`0x1e49744`. Le patch final restaure ces quatre octets si le repointage générique
les a pris pour une adresse. Les tests comparent toute la wave et tout le frame
sprite avec la source, ainsi que leurs tables consommatrices et empreintes.

## Livraison et contraintes

Le finaliseur `languages/pt/patches/batch_82.py` réutilise le patch transactionnel
existant et s'exécute après les réparations, le repointage et la police PT. Il
valide toutes les préimages, commandes et références avant de reloger les textes
et de repointer les seuls consommateurs audités, y compris les cellules de
pointeurs des listes fixes. Il n'écrase pas les anciens emplacements qui peuvent
être partagés. Il garantit aussi les discours complets dépassant le plafond de
l'extracteur. Aucun script partagé ni code `src/core` n'est modifié.

Les codes FC/FD et leur ordre, les pauses, les sauts de page FB et défilements FA
sont conservés exactement. Les sauts FE sont rééquilibrés dans chaque segment,
sans déplacer de texte entre les pages ou les défilements. Les listes de réglages
gardent une option par ligne. Limite conservatrice : 192 pixels par ligne, trois
lignes pour les descriptions de cellules et deux pour les messages ; après FA,
une seule nouvelle ligne. Les deux descriptions de mission respectent la fenêtre
de trois lignes à 172 pixels ; la description de Vivill Warehouse conserve sa
fenêtre de quatre lignes. Les cinq polices moteur sont mesurées avec tildes et
tampons développés. Les étages 1F/2F/3F/B1F/B2F/B3F et les directions sont conservés.

## Validation et limites

Les tests unitaires couvrent l'égalité manifeste/protections, les contrôles,
les budgets et les règles métier : échanges et surnoms, mots de passe, seuils
10/50 %, formes temporaires/permanentes de Zygarde, règles complètes du cirque
et de la mine. Les tests ROM vérifient les 297 consommateurs après `make build-pt`,
les octets exacts avec terminateur, les préimages, les cinq polices, l'idempotence,
l'atomicité et les écritures strictement bornées.

Le tampon FD0C de l'annonce du cirque contient un effet entier avec ses propres
pages. Le préfixe PT se termine donc par FE avant le tampon. Le test d'expansion
suit les 32 pointeurs du lot PT-43 déjà traduit, sans modifier ces chaînes ; le
préfixe et leur première ligne tiennent à 192 pixels. Les corps préexistants PT-43
restent contrôlés à leur budget de 208 pixels. Le tampon de la question de
catégorie reçoit Cave/Mountain/Pebble Format ; Mountain Format sert de borne.

La spec Playwright `pt82-scenario.spec.ts` lance mGBA hors écran sur une copie
éphémère de la ROM construite et utilise la msgbox native aux pointeurs vivants.
Elle compare les octets puis reconnaît par OCR les premières pages de trois
textes (échanges, cellule Zygarde, Paula). Elle vérifie que la sauvegarde reste
identique et capture le montage dans le répertoire temporaire de l'OS. Il s'agit
de sondes de rendu natives, pas d'un parcours complet des zones ni d'une preuve
de toutes les pages. Les captures ne sont pas conservées dans le dépôt.

Résultats de reprise F-841 : 334 tests unitaires/intégrité réussis,
`make build-pt` réussi, huit tests ROM réussis et un test Playwright hors écran
réussi (trois pages natives avec assertions OCR et sauvegarde inchangée).
La capture est jointe au ticket, hors dépôt. Ruff ciblé et `git diff --check`
réussissent. Aucun fichier partagé, aucune ROM source et aucun autre lot modifié.

Non vérifié : parcours complet en jeu des zones, toutes les pages et toutes les
combinaisons de tampons possibles ; les sondes visuelles couvrent trois premières
pages, complétées par les vérifications binaires exhaustives du lot.
