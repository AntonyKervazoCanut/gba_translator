# PT-74 — Guides TM, journal Missions, raids et Redwood

## Périmètre et sources

F-833 traite exclusivement les 300 offsets explicites PT-74 de
`languages/pt/translation_batches.json` (0x1f550b4–0x1f5a5c2).
F-758 (polices) et F-759 (glossaire) sont intégrés. L'anglais intégral est lu dans
la ROM source, comparé à `languages/en/combined_en.txt` et au français au même
offset. Les descriptions de Dynamax tronquées dans le corpus sont complétées
depuis la ROM. Les titres de missions déjà localisés restent cohérents avec les
lots précédents, notamment «Coleta de Honey» et «Duro na queda».

Le bilan machine, offset par offset, est `languages/pt/data/pt74_audit.json` :
287 textes localisés, neuf noms propres/variantes de lieu/cris conservés et
vérifiés, quatre exceptions. Il contient les préimages complètes, références,
texte PT, octets encodés, largeurs des cinq polices, valeurs de tampons utilisées
pour les budgets et justification individuelle. Les 296 entrées retenues sont
ajoutées sans modifier les traductions antérieures et protégées exactement.

## Consommateurs et contraintes natives

Les guides TM et Raid Den ne sont pas des descriptions d'objet dans la Boîte TM :
ce sont des fiches de mission, tables de records de 16 octets. La description est
le champ +4. Les 71 pointeurs TM sont 0x1e80614 + 16 × index ; ceux des raids
commencent à 0x1e613b4. Le lecteur 0x1ebee0c indexe la fiche à 0x1ebef60, charge
la description à 0x1ebef82 et l'imprime à 0x1ebefe0–0x1ebeff4.

`InitWindows` à 0x1ec0cbc utilise les templates à 0x1fb4174. La fenêtre 5
(template 0x1fb419c) mesure 25 × 6 tuiles, soit 200 × 48 pixels. Police 1,
x=0, y=3 : trois lignes de texte explicites, sans défilement. Les objectifs
principaux utilisent la même fenêtre. Le lot impose une marge de 192 pixels.
Les guides TM atteignent 169 pixels, les guides de raids 165 pixels ; les
objectifs restent sous 192 pixels. Mesures issues des tables de police réelles.

Le bandeau de catégorie dispose de 148 pixels, l'indication Type de 43 pixels.
La colonne de statut, fenêtre 3, ne dispose que de **32 pixels en police Small**.
«Ativ.» (24 px), «Prêmio» (29 px), «Capt.» (25 px), «Achado» (30 px),
«Feito» (24 px) et «Lido» (19 px) respectent cette contrainte.
Les deux lecteurs d'Active (statut 0x1ebffc8 et filtre 0x1fb40b8) gardent ainsi
une abréviation commune, sans modifier le code natif.

Le suffixe anglais « Missions » à 0x1f56040 est concaténé après la catégorie.
Comme dans le correctif français, il est rendu vide afin d'afficher des catégories
PT autonomes : «Todas», «Inativas», «Ativ.», «Prêmio», «Concluídas».
Le marqueur source explicite `<0xFF>` permet la protection d'une chaîne vide ;
l'encodeur produit son terminateur puis le terminateur automatique, sans texte
perdu. Le pointeur vivant 0x1ebe988 est contrôlé dans la ROM finale.

L'entrée 0x1f5609f est absente du corpus EN (la valeur Python `None` ne désigne
pas un texte anglais). Les vrais octets ROM et le lecteur 0x1ebe978 donnent
**All**, traduit «Todas». Type conserve exactement F8 03. Le préfixe Restante
conserve le saut de ligne et l'espace final via `<0x00>`.

Le patch `languages/pt/patches/batch_74.py` réutilise `ScenarioTextPatch` après
les réparations, la police et le repointage générique. Il encode les textes
verbatim et relocalise via les cellules vivantes auditées, ce qui évite le rewrap
inadapté aux tables de fiches. Il refuse une ROM source différente par SHA256,
vérifie toutes les préimages et commandes et restaure uniquement les quatre
octets du faux pointeur DPCM propre à ce lot.

## Exceptions justifiées

| Offset | Justification et consommateur réel |
|---|---|
| 0x1f56b77 | Octet 00 avant 0x1f56b78 ; aucune référence au préfixe. Le vrai texte est lu par 0x1e80c17, 0x1e80ef6, 0x1e8108b et traduit à +1. |
| 0x1f57e87 | Octet 00 avant Redwood Forest à 0x1f57e88 ; six pointeurs visent +1, dont 0x1e93c1c et 0x1fb3f0c. Nom propre conservé et livré à +1. |
| 0x1f58e33 | Octet 00 avant Redwood Village à 0x1f58e34 ; le lecteur 0x1eafec4 vise +1. Nom propre conservé et livré à +1. |
| 0x1f58899 | Ancien barrage annonçant une future version. Aucun pointeur 32 bits, aligné ou non, dans la ROM complète. Les scripts voisins utilisent 0x1f5888b via 0x1e81823 et 0x1f58957 via 0x1e81834. Texte laissé intact, sans prétendre qu'il est affiché. |

Le match 0x1d877d8 vers 0x1f565eb n'est pas un lecteur de dialogue. Il appartient
à un échantillon DPCM type 1 à 0x1d86fcc, en-tête
`010000000040a40000000000b12e0000`. Les 11953 échantillons occupent
ceil(11953 / 64) × 33 = 6171 octets après l'en-tête. Les instruments
0x19ec80c et 0x19f04b4 pointent cet échantillon. Le seul lecteur texte est
0x1ebfacc. Le test ROM exige l'identité de tout le bloc audio.

## Vérifications prévues et limites

Les tests unitaires contrôlent le manifeste fermé, les protections exactes,
l'ordre complet des commandes et sauts de ligne, les contraintes des fenêtres,
ainsi que les règles métier : trois tours Dynamax, boucliers, cinq équipes
préconfigurées, conditions Shedinja, trente Magikarp, horaires de garde,
accélération des Ovos et distinction vente individuelle/équipe/Caixa.

Les tests ROM contrôlent chaque pointeur vivant, chaque texte complet encodé,
les cinq polices avec tampons développés, l'intégrité du PCM et des fenêtres,
l'atomicité, l'idempotence et les bornes exactes du patch.

La preuve Playwright utilise mGBA avec `QT_QPA_PLATFORM=offscreen` et Chromium
headless. Une copie temporaire de la ROM reçoit uniquement un déclencheur de
script. Le menu Missions est ouvert par son véritable `callnative 0x09ec0eb5` :
fenêtres, catégories et objectif viennent de la ROM livrée. Les touches R
parcourent Toutes/Inactives/Actives. Une autre sonde affiche trois dialogues
natifs de Redwood aux pointeurs livrés. Les assertions OCR vérifient le texte ;
les contrôles binaires garantissent les accents, codes et pages complets.
Aucune sauvegarde en jeu ; les sauvegardes temporaires sont comparées octet par
octet après les sondes. Les captures restent dans le répertoire temporaire OS.

La sonde ne revendique pas un parcours manuel des 300 offsets ni le déroulement
complet des missions. Les textes des autres lots visibles dans le menu ne sont
pas modifiés par PT-74. Aucun code partagé, pipeline distant ou push.
