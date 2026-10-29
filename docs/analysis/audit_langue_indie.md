# Audit de la langue « Indie »

Date : 29 octobre 2026. Ticket A-665 ; parent C-660. Dépôt : gba_translator, branche unbound.

## Décision et preuves

La cible historique est le **hindi**, actuellement en **translittération latine**. Rien ne justifie une conversion en indonésien ni un retrait de la langue.

- F-185 « Traductions Indie » introduit la cible générique, sans identifier précisément la langue ; commit `b2533048` (équivalent historique `1e1563cb`), 29 juin 2026 : les trois seeds étaient encore français.
- `f4d0ea34` (équivalent `6841bb3d`), 29 juin 2026, intitulé « add Hindi translations to seed entries », remplace ces seeds par `मैं तुम्हें बता रहा हूँ।`, `अभी तक नहीं!`, `तुम मुझे पीट देते हो।`. Cette modification explicite l'intention linguistique.
- T-226 audite la PR #1 et constate la conversion silencieuse du devanagari en points d'interrogation ; B-227 corrige ce défaut dans `8c2f5319` / `79539f2d` par romanisation. Les historiques dupliqués proviennent des références git disponibles ; ils ne constituent pas deux ajouts distincts.
- `languages/indie/combined_indie.txt` conserve cette explication et les trois phrases romanisées ; `tests/test_indie_seeds_encodable.py` protège leur encodabilité.

Recommandation : poursuivre en hindi romanisé simple, alphabet latin encodable, sans présenter cette convention comme une traduction officielle ni comme une norme Hunterian strictement validée. L'appellation Hunterian du commentaire historique doit être revue par le glossaire. Conserver provisoirement le code technique `indie` pour éviter de casser les consommateurs ; afficher « Hindi romanisé » dans les métadonnées/documentations. Une migration ultérieure vers `hi` demanderait un ticket séparé avec compatibilité des anciens chemins et assets. `id` désignerait une autre cible et ne doit pas remplacer cette langue.

Référence livrée par D-692 : [HI-LATIN-1 v1.0.0, glossaire et convention](01_HINDI_ROMANISE_REFERENCE.md).
Les lots HI-01 à HI-64 doivent appliquer cette convention et sa relecture des seeds.

## Faisabilité

Le pipeline générique existe (`build: generic`, `status: in_progress`, `version_label: IN.2.1.0`). La police est celle du FR. `src/text/charmap_data.py` ne définit aucun caractère devanagari ; `TextEncoder.encode_pokemon` utilise le fallback `?` (`0xAC`). Les trois seeds actuels sont encodables, mais cela ne prouve ni leur justesse linguistique ni la qualité du rendu complet.

Le latin simple est immédiatement compatible avec cette charmap ; il faut néanmoins contrôler les tokens positionnels, budgets d'octets, cellules fixes, coupures, largeur et pointeurs vivants. Ne pas utiliser de signes de translittération savante absents de la charmap.

Une police devanagari seule ne suffit pas : il faudrait définir un encodage et la sélection des glyphes, traiter matras, réordonnancement et conjonctions, adapter le rendu et les métriques, tenir compte des octets réservés aux contrôles, synchroniser les codecs Python/TypeScript, puis tester les différentes polices de l'interface et les graphismes. C'est une étude moteur dédiée, sans garantie de faisabilité dans le moteur actuel. Ne pas lancer les lots en devanagari. Aucun patch global de police ou de charmap n'est recommandé pour cette première campagne.

## Volumétrie reproductible

Comptage des lignes correspondant à `^\s*(0x[0-9a-fA-F]+):\s*(.*)` ; résolution par offset entier, dernière occurrence gagnante.

| Source | Lignes de données | Offsets uniques |
|---|---:|---:|
| `languages/indie/combined_indie.txt` | 3 | 3 |
| `languages/fr/combined_fr.txt` | 25 231 | 24 164 |
| `languages/en/combined_en.txt` | 25 524 | 25 524 |

Les trois seeds représentent 0,0118 % du corpus EN recensé ; 25 521 offsets EN restent à traiter. Ce pourcentage mesure des entrées sources, pas la couverture effective de la ROM : tables fixes, graphismes, données dédiées et textes non extraits nécessitent un inventaire supplémentaire. Le fichier FR n'est pas une source anglaise ni un dénominateur exhaustif.

Snapshot EN SHA-256 : `65e93f43b9f92f19ba011fb4971aea6f44d9cd419363d7b51d9dbe094235af19`.

## Plan et partition exhaustive du corpus recensé

1. Infrastructure : expliciter Hindi romanisé, protéger les trois seeds existants, vérifier l'absence de fallback sur toutes les entrées et les budgets ; inventorier les surfaces dédiées restant anglaises. Préserver les identifiants de release existants.
2. Glossaire : établir une convention de romanisation et une terminologie de référence, en citant toute source officielle disponible et en signalant les choix éditoriaux non officiels. Conserver noms Pokémon et toponymes EN par défaut ; fixer les conventions d'attaques, objets, talents, types et statuts. Ne pas inventer de terminologie « officielle ».
3. Lots ci-dessous : dépendance fonctionnelle aux deux préalables. Chaque lot sélectionne exclusivement les offsets du snapshot EN dans son intervalle inclusif, hors `0x1773FD`, `0x177489`, `0x183509`. Les intervalles sont disjoints et couvrent les 25 521 entrées restantes : 63 lots de 400 et un de 321.

Le domaine de cette partition est le **corpus textuel EN extrait**, ordonné par stockage ROM. Un intervalle n'est pas une zone géographique : aucune association ville/offset n'est inventée. Avant traduction, chaque lot doit classer ses entrées (dialogue, combat, interface, table) et vérifier le contexte EN vivant. Les entrées mortes ou mal extraites sont documentées comme exclues avec justification, jamais traduites aveuglément. Cette partition assure des lots indépendants malgré l'absence actuelle de cartographie sémantique exhaustive.

| Lot | Premier offset inclus | Dernier offset inclus | Entrées |
|---|---|---|---:|
| HI-01 | `0x28780` | `0x1A5301` | 400 |
| HI-02 | `0x1A532F` | `0x23E635` | 400 |
| HI-03 | `0x23E642` | `0x3D5D50` | 400 |
| HI-04 | `0x3D5D96` | `0x3E8A9A` | 400 |
| HI-05 | `0x3E8AA4` | `0x3EAF98` | 400 |
| HI-06 | `0x3EAF9F` | `0x3FB40D` | 400 |
| HI-07 | `0x3FB41A` | `0x3FD8D2` | 400 |
| HI-08 | `0x3FD8E8` | `0x4177AC` | 400 |
| HI-09 | `0x4177C5` | `0x419D57` | 400 |
| HI-10 | `0x419D66` | `0x41E0B9` | 400 |
| HI-11 | `0x41E0C0` | `0x44BD7D` | 400 |
| HI-12 | `0x44BDEB` | `0x458D75` | 400 |
| HI-13 | `0x458D78` | `0x486C55` | 400 |
| HI-14 | `0x486C95` | `0x75350F` | 400 |
| HI-15 | `0x753510` | `0x77FC48` | 400 |
| HI-16 | `0x77FC7B` | `0x7A36CA` | 400 |
| HI-17 | `0x7A3BDD` | `0x7BCAD5` | 400 |
| HI-18 | `0x7BCB14` | `0x7CEC72` | 400 |
| HI-19 | `0x7CED48` | `0x7E9D4B` | 400 |
| HI-20 | `0x7E9D68` | `0x7F79D5` | 400 |
| HI-21 | `0x7F79F9` | `0x87848C` | 400 |
| HI-22 | `0x8784B8` | `0x87CC90` | 400 |
| HI-23 | `0x87CCBC` | `0x8D0906` | 400 |
| HI-24 | `0x8D0933` | `0x922A91` | 400 |
| HI-25 | `0x922AAF` | `0xA35679` | 400 |
| HI-26 | `0xA35695` | `0xA37630` | 400 |
| HI-27 | `0xA37641` | `0xA3E5C8` | 400 |
| HI-28 | `0xA3E600` | `0xA417FA` | 400 |
| HI-29 | `0xA41807` | `0xA42C57` | 400 |
| HI-30 | `0xA42C64` | `0xA449FB` | 400 |
| HI-31 | `0xA44A6C` | `0xA46E75` | 400 |
| HI-32 | `0xA46E9D` | `0xA4B460` | 400 |
| HI-33 | `0xA4B480` | `0xA4ED28` | 400 |
| HI-34 | `0xA4ED2F` | `0xEB487E` | 400 |
| HI-35 | `0xEB48E0` | `0x14BE863` | 400 |
| HI-36 | `0x14BED6B` | `0x166529C` | 400 |
| HI-37 | `0x16652FE` | `0x166B0FB` | 400 |
| HI-38 | `0x166B106` | `0x166C328` | 400 |
| HI-39 | `0x166C333` | `0x166D458` | 400 |
| HI-40 | `0x166D463` | `0x19101CC` | 400 |
| HI-41 | `0x19101DD` | `0x1A83755` | 400 |
| HI-42 | `0x1A83F93` | `0x1EE7B08` | 400 |
| HI-43 | `0x1EE7B47` | `0x1EF0E7A` | 400 |
| HI-44 | `0x1EF0EE4` | `0x1EFA4E5` | 400 |
| HI-45 | `0x1EFA503` | `0x1F03358` | 400 |
| HI-46 | `0x1F033D5` | `0x1F0D840` | 400 |
| HI-47 | `0x1F0D8AA` | `0x1F15BED` | 400 |
| HI-48 | `0x1F15C54` | `0x1F2189B` | 400 |
| HI-49 | `0x1F218AC` | `0x1F2BB7E` | 400 |
| HI-50 | `0x1F2BB96` | `0x1F35405` | 400 |
| HI-51 | `0x1F3541D` | `0x1F42926` | 400 |
| HI-52 | `0x1F429A1` | `0x1F4DC32` | 400 |
| HI-53 | `0x1F4DC3A` | `0x1F5755D` | 400 |
| HI-54 | `0x1F575B8` | `0x1F5E859` | 400 |
| HI-55 | `0x1F5E890` | `0x1F662DB` | 400 |
| HI-56 | `0x1F6632D` | `0x1F6F0F4` | 400 |
| HI-57 | `0x1F6F164` | `0x1F78BB5` | 400 |
| HI-58 | `0x1F78CE2` | `0x1F81D65` | 400 |
| HI-59 | `0x1F81D6A` | `0x1F8907A` | 400 |
| HI-60 | `0x1F890AB` | `0x1F941E6` | 400 |
| HI-61 | `0x1F941F3` | `0x1F99C0F` | 400 |
| HI-62 | `0x1F99C2A` | `0x1F9F553` | 400 |
| HI-63 | `0x1F9F59C` | `0x1FA92E8` | 400 |
| HI-64 | `0x1FA92F7` | `0x1FD23BE` | 321 |

## Critères communs aux tickets

- `combined_*.txt` : éditions chirurgicales, dernière occurrence gagnante ; jamais de régénération, tri ou sed global.
- Chaque ligne ajoutée doit avoir son entrée dans `protected_entries.yaml`, dans le même commit.
- Le hash de la ROM FR ne doit pas changer ; exécuter `make test-python` complet.
- Commits en français : `type(scope): description` ; hooks activés.
- Avant/après : vérifier encodage sans fallback, tokens, budgets et décodage de la ROM cible. Pour les changements visibles, preuve Playwright headless et capture attachée au ticket. Aucun push ni déclenchement de pipeline distant.

## Limites et non vérifié

Cet audit ne modifie aucune traduction, police, configuration de build ou ROM. Il ne certifie pas les trois phrases sur le plan linguistique et ne valide pas un rendu devanagari. La cartographie exhaustive des zones et des surfaces graphiques reste au préalable infrastructure. Le catalogue MCP annonce kanban-board, mais `kanban_create_ticket` n'est pas exposé parmi les outils appelables de cette session ; utiliser l'outil de suivi d'orchestration disponible pour matérialiser le backlog et conserver les références retournées dans le compte rendu du ticket.
