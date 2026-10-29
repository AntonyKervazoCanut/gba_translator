# ES-002 — traitement et validation (F-852)

## Sources et périmètre

D-849 et F-850 consultés terminés avant traduction. Le lot contractuel de
`lots.json` comporte 374 offsets ; aucun calcul par plage ni `--skip-existing`.
Le rapport machine [es002_traitement.json](es002_traitement.json) contient une
ligne logique par offset : décision, justification, octets EN complets,
correspondance ES de l’offset map, octets communautaires alignés, référents,
commandes complètes, traduction et vérification ROM.

318 traductions, 3 imports communautaires relus, 41 noms/cris ou chaînes de secours conservés,
12 exclusions : les 374 décisions sont couvertes sans doublon. Les trois imports
sont les formulations fidèles de la commode, du réfrigérateur rempli et des
lumières clignotantes. Les autres formulations ont été retraduites/corrigées.
Le texte de cuisine publicitaire KFC est remplacé par le sens EN. Les récompenses
du Pokédex et les informations supprimées dans ES sont rétablies.

Les éditions du combined sont des ajouts ciblés ; son préfixe préexistant est
inchangé. Chaque valeur est protégée exactement dans le même commit. Ni le
glossaire ni l’infrastructure commune, ni ES référence ni FR ne sont édités.

## Reconstruction et exclusions

- Préfixes parasites 0xAA : 1A5AD5, 1A5BC5, 1A6196, 1A6447, 1A6CA2,
  1B1D7C, 1BC310 et 1C27E6. Le texte réellement référencé commence à +1.
  Les vrais offsets 1A5BC6, 1A6197 et 1A6CA3 sont traduits dans le lot ;
  le cri 1A6448 est conservé. Les quatre autres vrais débuts ne sont pas ajoutés
  hors contrat ; ils doivent entrer dans l’examen complémentaire de T-914.
- 1BDF08 : suffixe de 1BDEDF, pas une chaîne autonome ; la référence brute
  1BDF64 chevauche un vrai pointeur 1BDF61 vers 1BDF76.
- 1C59F7 : suffixe intérieur de 1C59D5, sans référent.
- 23700C : ancienne description Bug orpheline. Ne pas importer Planta sur la
  seule foi de la référence ES. La description de la Plaque Herbe (ID515) est
  réellement à EB396F via le champ 87B90C ; celle de la Plaque Insecte (ID510)
  est 236E2A via 87B830.
- 1BD966 et 1BDBF8 : EN reconstruits jusqu’au FF (542 et 742 octets utiles),
  et non depuis le CSV tronqué à 512. Les traductions complètes tiennent dans
  501 et 475 octets utiles, avec toutes les pages et commandes dans l’ordre.
- 1BC59E et 1BC7E2 : vrais scripts opcode 9B aux sites 1BBF89 et 1BB9F3,
  que le filtre générique `plausible_sites` ne reconnaît pas. Traductions
  volontairement inférieures au budget EN ; aucun changement au filtre partagé.

L’ancienne offre Hawlucha à 500 Fiches (237503) est aussi exclue : la table
Casino utilise 7EC795 via 7EC45E, à 1 000 Fiches. Les sept chaînes de secours
sans aucun référent direct sont conservées EN sans injection plutôt que de
fabriquer un consommateur. Leur non-accessibilité complète n’est pas revendiquée.

Les 33 propositions de noms de joueur/rival restent exactement celles de EN,
conformément à D-849. Le cri Gyaoo! n’est pas une phrase à inventer.
Les classes de dresseur sont des cellules de 13 octets de gTrainerClassNames
à 23E558 ; l’accès par indice explique l’absence de pointeurs individuels.
Les chaînes sans référent direct sont vérifiées in-place et signalées dans
le rapport, sans prétendre qu’une recherche de pointeurs prouve leur accessibilité.

## Référents et surfaces

Les surfaces sont attribuées aux consommateurs réels : scripts de soins
(site 1A6588), démarrage du PC (168CFA), évaluation Pokédex (1A6A90),
inspection des livres (1A7608), pension (171969), descripteurs d’objets
(87B6D0, 87B830), tables de menus (237420, 238D00), et classes indexées.
Ce sont des textes système réutilisables, pas une zone déduite de leur banque ROM.
Aucun nom de carte précis n’est inventé : le dépôt ne fournit pas de résolution
exhaustive des cartes propriétaires des scripts partagés.

## Budgets et preuves

`test_es002_contract.py` vérifie l’ensemble exact des 374 décisions, les arguments
FC/FD/F8/F9/F7 et FA/FB sur les octets EN, le plafond de 512 avec FF,
192 pixels maximum par ligne et les cellules de classes de 13 octets.
Les descriptions de plaques tiennent sur trois lignes ; les buffers conservent
leur ordre. Les messages d’objets et mouvements longs ont des sauts explicites.
`test_es002_injection.py` vérifie chaque consommateur dans la ROM construite :
texte complet, arguments, cible relocalisée et absence de fallback.

Le test Playwright `es002.spec.ts` utilise mGBA offscreen sur une copie temporaire,
l’imprimante native et huit pointeurs de la ROM finale. Il n’enregistre jamais la
partie. Les assertions OCR es-ES précèdent la capture. La sonde démontre le rendu
moteur des textes ; elle ne prétend pas rejouer toutes les branches d’un échange
multijoueur nécessitant plusieurs consoles.

## Résultats locaux

Validation en cours ; les résultats finaux et empreintes seront consignés après
les builds et les vérifications ROM. Aucun push ni pipeline distant déclenché.
