# B-680 — Qualification du lot dialogues-08

Les 300 offsets exclusifs sont décrits individuellement dans
`680_DIALOGUES_08_DE.json` : valeurs EN/FR/DE gagnantes, texte ROM complet,
octets source, références originales, scène, registre, genre, décision,
budget encodé et largeur. Aucun audit global n'a été relancé.

## Sources et décisions

La ROM EN canonique est `input/roms/englishrom.gba`, SHA-256
`7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`
(`docs/roms_baseline.json`, inchangé). Les extractions EN contiennent parfois
une fin tronquée : les dialogues ont été confrontés à la chaîne ROM jusqu'au
terminateur FF. Les commandes FC/FD/F8 ont été consommées atomiquement ;
notamment FC 08 20 est une pause complète, pas une lettre « î » imprimable.

265 valeurs sont corrigées, dont 156 oublis et 109 entrées existantes
(sens, commandes, terminologie ou mise en boîte). Les 35 autres décisions
sont : 23 valeurs déjà correctes/cris/interjections légitimes, 11 noms propres
conservés et une variante sans référence vers son début (`0x1F4B6D9`).
Aucune nouvelle entrée n'est insérée pour cette dernière.

Les noms de lieux et d'espèces restent EN suivant le contrat du build.
Ainsi Moltres, Articuno, Houndoom et Redwood Village remplacent les intrusions
FR/DE erronées de ces noms dans les dialogues concernés. Les cris Skull,
Dile, Hoopa et les onomatopées de radio restent légitimes ; ils ne sont pas
des oublis à traduire mécaniquement. « Whoa », « Hmm » et « Lalalala » sont
également acceptés. Le lot ne contient ni fiche Pokédex ni `0x7A823B` : aucun
changement Electabuzz/Elekid/Elektek n'est autorisé ici.

Les principaux correctifs de sens sont la **propre** force que le rival veut
montrer (`0x1F374A2`), Arthur secouru avec l'aide de Jax (`0x1F30C2D`), les VM
utilisables sans être apprises, la restitution des Pokémon, et les conditions
des salles des Top 4. Les deux effets défensifs d'Elias exigent les KP pleins ;
le bonus de Penny concerne les attaques des Pokémon Dragon, pas seulement
les attaques de type Dragon. Les attaques suivent le référentiel local figé
`languages/de/data/move_names_de_official.json` et
`official_terminology.yaml` : Zertrümmerer, Erdkräfte, Bodyguard, Delegator,
Schutzschild et Zerschneider. Prison Bottle devient Bannflasche.
Le [document Nintendo allemand](https://www.nintendo.com/eu/media/downloads/country_support_4/de_23/Pokemon_Swan_Zine_A4_DE_F_1.pdf)
confirme la graphie Konnex-Klub pour les échanges sans fil.

## Protections et limites

Les seules modifications de texte sont des substitutions des dernières
occurrences dans `languages/de/combined_de.txt`, ou des ajouts en fin de
fichier pour les oublis vérifiés vivants. Les anciennes occurrences,
l'ordre et les fins de ligne sont conservés. Chaque valeur modifiée possède
sa protection exacte dans `protected_entries.yaml`, contrôlée par le test
partagé d'intégrité, dans le même commit. La matrice de parité n'ajoute que
l'enregistrement du nouveau test, sans revendiquer de patch supplémentaire.

Les suites de commandes FC/FD/F8 et les pages FB sont comparées à la ROM,
dans leur ordre. Les retours FE/FA sont répartis selon le budget de 192 px,
avec une cible de repli à 180 px pour laisser une marge aux icônes. Les buffers
sont mesurés avec le budget conservateur du moteur de mise en ligne.
Les apostrophes avec FD02 sont formulées sans accord masculin imposé : les
deux occurrences manquantes de `0x1F4C2ED` sont restaurées dans leur ordre.

**Patch séparé : B-1016.** La chaîne source `0x1F4C2ED` fait 1061 octets avec
FF et dépasse le plafond d'extraction de 1000. Le site `0x1E6D700` doit être
réacheminé par B-1016. Le texte DE est corrigé et protégé ici ; aucun patch,
aucune ressource FR/IT et aucun hash FR ne sont modifiés par ce lot.

## Validation locale

Les résultats du build, de la suite Python et de la sonde native sont consignés
après exécution dans les métadonnées binaires JSON et le compte rendu du ticket.
La sonde Playwright est exécutée headless, mGBA avec `QT_QPA_PLATFORM=offscreen`,
sur une copie temporaire de la ROM finale. Elle déclenche l'imprimante native
avec les adresses lues dans les pointeurs finaux ; ses assertions OCR portent
sur Erdkräfte, Zertrümmerer, Quak et la confirmation des options. La capture
reste dans le dossier temporaire de l'OS et est attachée au ticket.

## Non vérifié

La sonde ne rejoue pas naturellement les 300 scènes et ne certifie pas tous
les états de progression. L'acheminement du dialogue long attend B-1016.
Les pointeurs et octets de toutes les références recensées sont contrôlés
séparément, sans présenter le corpus seul comme une preuve d'injection.
