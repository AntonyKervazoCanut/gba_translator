# Infrastructure du hindi romanisé

La cible est `indie` (Hindi romanisé), avec les chemins, assets et version `IN.2.1` historiques. Les trois seeds sont protégés par résolution de la dernière occurrence. Le contrôle strict couvre toutes les entrées vivantes : les tokens hexadécimaux et les points d'interrogation littéraux ne sont pas des fallbacks ; les marqueurs nommés sont réservés au remplacement par le builder, dont il faut vérifier le nombre et l'ordre contre la source EN lors de chaque lot. Un passage de ce contrôle ne garantit ni la présence des glyphes dans toutes les polices, ni la validité des tokens, pointeurs et budgets.

## Budgets et surfaces à traiter

Les trois seeds sont des dialogues ordinaires, respectivement 28, 15 et 23 octets de texte encodé, hors terminateur. Le build local a réinséré les trois seeds : deux relogés, un dans le padding, zéro troncature et zéro fallback ; la passe inline les ignore tous trois car trop longs sur place. Le builder peut reloger les dialogues ; chaque lot doit néanmoins vérifier les pointeurs vivants, les ruptures de page, largeur et hauteur à l'écran et l'espace disponible. Les cellules fixes ne peuvent pas être relogées comme des dialogues : inclure le terminateur dans le budget et vérifier le rendu. Les scripts FR sont des indices d'inventaire, pas des patchs à appliquer à Hindi.

| Surface / source technique | Budget ou contrainte | Travail futur borné |
|---|---|---|
| Espèces `species_names.py` | 11 octets par cellule à `0x166A997` | Vérifier les noms EN conservés et les pointeurs ; pas de traduction par défaut. |
| Attaques `move_names.py` | 13 octets, table historique `0xA40A10`, base vivante résolue par pointeur | Inventorier les entrées vivantes, choisir les noms du glossaire, mesurer et tester chaque cellule. |
| Talents `ability_names.py` | 17 octets à `0xA36398` | Inventorier et tester les cellules et leurs références. |
| Objets `item_names.py` | champ nom 14 octets, entrée de 44 à `0x876074` | Traduire dans une passe dédiée sans écraser les données ni pointeurs de description. |
| Classes de dresseur `trainer_class_names.py` | 13 octets à `0x23E558` | Mesurer cellules et largeur d'interface ; relever les noms non extraits. |
| Natures, types et tables fixes (`nature_names.py`, `cfru_type_names.py`, `fixed_table_names.py`) | Dépend de chaque table et de sa police | Cartographier bases vivantes, cellules et consommateurs avant traduction. |
| Descriptions attaques, CT et Pokédex | Pointeurs, lignes, boîtes et retours à la ligne spécifiques | Inventorier les copies, vérifier longueur et affichage par écran ; portage sélectif avec tests. |
| Missions, carte, noms de zones, PC, menus, résumé, boutique, DexNav | Multiples tables et textes inline ; certaines surfaces ne figurent pas dans combined EN | Relever chaque site et ses pointeurs, mesurer les boîtes et prévoir des patchs Hindi dédiés. |
| Icônes de types et badges de statut | Graphismes et blocs LZ77, pas de texte ordinaire | Inventorier les assets visibles, dessiner et tester les versions Hindi séparément. |
| Statuts, date, heure, argent, niveau, HP, genre et modèles de combat | Abréviations, ordre, buffers et largeurs propres | Décider par interface avec le glossaire ; tester les substitutions et limites en jeu. |
| Police et écran de version | Police FR partagée, version `IN.2.1` | Garder la compatibilité ; vérifier toutes les polices utilisées pour les caractères retenus. |

Les 64 lots couvrent les offsets du snapshot `combined_en`, pas ces surfaces supplémentaires. Certains offsets des tables peuvent aussi figurer dans le corpus : déterminer la cible vivante et éviter un double traitement. L'inventaire identifie les familles connues du pipeline FR, sans prétendre épuiser les textes non extraits ; chaque passe future doit produire sa liste vérifiée sur ROM EN et ses exclusions. La réparation LZ77 générique copie certains blocs localisés ES : examiner leur contenu et leur provenance avant toute localisation Hindi. Aucune police, aucun moteur ni encodage devanagari ne sont ajoutés ici.
