# ES-002 — traitement et validation (F-852)

## Sources et périmètre

D-849 et F-850 consultés terminés avant traduction. Le lot contractuel de
`lots.json` comporte 374 offsets ; aucun calcul par plage ni `--skip-existing`.
Le rapport machine [es002_traitement.json](es002_traitement.json) contient une
ligne logique par offset : décision, justification, octets EN complets,
correspondance ES de l’offset map, octets communautaires alignés, référents,
commandes complètes, traduction et vérification ROM.

322 traductions, 3 imports communautaires relus, 41 noms/cris ou chaînes de secours conservés,
8 exclusions : les 374 décisions sont couvertes sans doublon. Les trois imports
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
  le cri 1A6448 est conservé. Pour les quatre autres phrases, les traductions sont préparées sous la clé
  contractuelle ; la résolution explicite vers +1 attend le prérequis technique
  réutilisant B-1030. Aucun ajout de clé hors contrat et aucune écriture sur AA.
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

**Préparation livrée, certification bloquée : ne pas clôturer F-852.**

- `make build-es-maint BUILD_NUMBER=0` réussit, sans prouver le bon acheminement.
- `make test-python` : 4 749 passed, 3 skipped préexistants, 2 662 deselected.
- Hooks actifs du commit initial : 4 607 tests Python rapides et 68 tests Vitest
  réussis ; builds FR/IT/DE réussis. Le premier essai a rencontré une ROM DE
  absente dans le worktree pendant un sous-make dry-run ; les artefacts locaux
  ont été préparés, puis le hook complet a été rejoué, sans contournement.
- `python3 -m ruff check` sur les deux nouveaux tests Python et
  `npx tsc --noEmit -p tsconfig.playwright.json` réussissent.
- Playwright headless : 1 test réussi, huit consommateurs natifs avec assertions
  OCR es-ES, capture attachée à F-852 : ab1a1922-96c4-4c16-bb51-9bb01a9603e8.
  L’OCR est normalisé pour les accents, les octets accentués étant contrôlés
  séparément par les assertions ROM. Aucune sauvegarde en jeu. Cette preuve
  concerne les textes acheminés ; elle ne certifie pas les branches bloquées.
- FR reconstruite aux mêmes sources/paramètres avant import et par les hooks :
  comparaison octet par octet réussie, SHA-256
  `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
- Baseline es-maint sans traduction reconstruite avec les étapes mécaniques
  F-850 : SHA-256 `43504c10e47ff2ff655d0fcecf5cbc5030c1b30902d7c549ca4b9cdd194c33c0`,
  identique au témoin F-850. ROM ES provisoire du lot avant résolution des alias :
  `dcf139884ed1e0af92649b4514064cbe95fa92f876bc24673c3f69eef3c2177e`.
  Ce hash identifie un artefact de diagnostic, pas une ROM distribuable.

## Blocages et reprise obligatoire

Le rapport ROM identifie 312 textes conformes et **13 entrées non certifiées** :
quatre alias contractuels (1A5AD5, 1B1D7C, 1BC310, 1C27E6), quatre paginations
altérées (1A552B, 1BC4CE, 1BC7E2, 1BDBF8) et cinq classes (23E565, 23E57F,
23E58C, 23E599, 23E5A6) restant EN. Les 41 conservations et huit exclusions
restent documentées. Les gardes ROM échouent volontairement sur ces défauts ;
aucun skip/xfail ni neutralisation de commande n’est ajouté.

B-1030 fournit la résolution des alias contractuels. B-1032, créé après
consultation du catalogue et de B-1031, traite le complément technique ES-002 :
étendre les quatre alias sans dupliquer le moteur ; préserver les pages de ces
consommateurs système ; réutiliser la passe existante des classes indexées.
B-1031 reste le propriétaire de la correction de layout des descriptions d’objets
ES-003. Aucune traduction n’est déléguée à ces prérequis.

La comparaison différentielle à la baseline ES relève aussi **neuf octets hors
plages autorisées**, immédiatement après les anciens slots de textes relocalisés :
1A6041, 1A63D6–D7, 1BC572–573, 1BCA7F, 1C0DD4–DD5, 237503. Le dernier est le H
de Hawlucha, explicitement exclu du lot. Plusieurs autres sont des données non
textuelles, pas du padding. La passe inline réécrit vraisemblablement l’ancien
slot après relocalisation ; le diagnostic et les préimages sont transmis à B-1032,
sans modifier cette infrastructure dans ES-002. Une garde ROM vérifie chacun de
ces neuf octets par rapport à EN. La certification impose zéro octet hors périmètre.

Preuves jointes : préimages des 13 entrées a6078e76-6e44-4318-8f08-1cb7ba8c3bc4 ;
audit de voisinage ce54b1f2-835c-439a-bfd2-82113b7ab55e. Les prérequis peuvent
tester leurs mécanismes avec des sentinelles temporaires et ces préimages,
sans dépendre des sources provisoires de ce worktree.

Après intégration des prérequis : rebase orchestré, rebuild es-maint, tests ROM
complets du lot (y compris voisins), nouveau témoin FR sur les sources intégrées,
make test-python, puis nouvelles preuves Playwright pour les surfaces corrigées.
Les zones carte précises des scripts partagés et le multijoueur à plusieurs
consoles ne sont pas certifiés par la sonde. Aucun push ni pipeline distant déclenché.


## Passe ROM globale de diagnostic

`make -o materialize-test-roms test-rom` teste les reconstructions locales sans
réappliquer les anciens BPS par-dessus le témoin FR : 2 420 passed, 32 skipped,
28 failed, 4 943 deselected. Vingt-deux échecs sont les gardes ES-002 attendues
(13 entrées et neuf octets voisins). Les six autres concernent une ROM PT absente,
quatre attentes DE distinctes des sources/contenus actuels (rival, deux gardes
F-601 et dialogues-09) et la garde de hash global Corps Gel FR qui exige
c6031984… au lieu du témoin reconstruit 2c2f602e… . Aucune source ou attente DE/FR
n’a été modifiée dans ES-002 pour masquer ces écarts.

La cible PT a ensuite été construite localement ; le test de police PT repasse
(1 passed). Pas de deuxième passe globale inutile tant que les défauts ES-002
restent ouverts. Le test unitaire ciblé final du lot donne 376 passed.
Les 185 référents relocalisés inspectés ciblent exclusivement du padding 00/FF
dans la baseline ES ; aucune cible allouée ne remplace de données occupées.

Les sources EN/ES référence/FR et les deux ROM sources ont gardé leurs empreintes
consignées dans le rapport. Les modifications du combined sont exclusivement les
325 clés ES-002 préparées ; les autres lots ne sont ni traduits ni normalisés.
La préparation et les preuves sont conservées en commits locaux, sans push.
F-852 attend B-1030 et B-1032 et doit reprendre toutes les gardes ROM après leur
intégration avant toute déclaration de réussite.
