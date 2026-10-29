# B-681 — Qualification du lot allemand dialogues-09

Périmètre exclusif : les 300 offsets du ticket, de `0x1F54752` à `0x1F8E271`.
Aucun audit global relancé. `0x7A823B` n'appartient pas à ce lot.
Bilan : **120 corrigés en ROM**, **8 déjà corrects**, **5 déjà patchés**,
**160 noms/cris/termes légitimes**, **5 fragments non vivants**,
**2 besoins de patch séparé**. Le corpus comporte 121 corrections protégées :
120 injectables et le texte Battle Sands préparé pour son futur patch.

La qualification exhaustive est dans [681_DIALOGUES_09_DE.json](681_DIALOGUES_09_DE.json) :
valeurs EN/FR/DE, source canonique complète, commandes atomiques, scène, décision,
références de pointeurs et résultats binaires. Aucun descriptif Pokédex d'espèce
ne figure dans ce lot ; les noms d'espèces et lieux EN sont intentionnels.

## Méthode et sources

- ROM EN canonique : SHA-256 `7aa25bbf568f7cfcf6ee1cf2e9e6ff637350b3d0705c2375cabb6baa7d9739f7`.
- Les corpus EN/FR servent de comparaison, jamais de preuve binaire. L'EN est
  incomplet et ses descriptions de plus de 500 caractères sont tronquées ; le
  terminateur de la ROM donne notamment les règles complètes Circus et Sands.
- Valeur DE gagnante relue au moment de l'édition. Une modification ciblée par
  offset, sans tri ni régénération. Comparaison octet à octet des blocs hors lot.
- Terminologie : `languages/de/data/official_terminology.yaml`, ressources DE
  locales des attaques/objets et noms officiels. Le [guide officiel des
  Mega-Steine](https://assets.pokemon.com/assets/cms2-de-de/pdf/video-game/pokemon-xy/MegaStone_Collection_Guide_LowRes_DE.pdf)
  confirme Mega-Stein et Ruhmeshalle. Espèces et toponymes EN conservés selon la
  politique du build ; aucune substitution automatique depuis la FR.
- Les commandes FC/FD/F8 sont décodées atomiquement. Les alias tels que
  `{SE_SHOP}` ou `{COLOR}É` ne sont pas nécessairement erronés : comparaison avec
  les octets canoniques, puis commandes explicites pour les corrections.
- Largeur des dialogues bornée, avec glyphes allemands, ellipse B0, icônes et
  réserve pour buffers. Les descriptions CT restent sur trois lignes au plus,
  sans défilement. Les pages FB canoniques sont préservées ; FE/FA sont répartis
  selon les mots allemands pour respecter les boîtes.

## Corrections et exclusions

Les corrections portent sur les oublis réellement référencés, les faux sens,
les termes officiels, le registre et les boîtes trop larges. Notamment :

- `0x1F7B371` : les six lignes physiques de continuation étaient ignorées par
  `_load_combined`. Une seule entrée physique contient désormais tout le texte
  de Méga-Évolution, les couleurs, le bouton START et les deux pauses `FC 08 18`.
- `0x1F74B42` : Schwerball, Timerball, Turboball et Finsterball ; restitution de
  quatre couleurs omises, distinction entre Initiative de base et valeur réelle.
- `0x1F6348B` : Wertehalter, et non Klebekörper ; l'effet facilite la pêche.
- `0x1F7441F` : Lockduft, et non Duftnote. `0x1F7496C` : défilement du texte,
  et non course automatique. Suppression du français résiduel « sur ».
- `0x1F59FA3` : accélérer l'éclosion, sans promettre une éclosion immédiate.
- `0x1F81EAA/EB6/ED3/EDF` : déjà pris en charge par `time_format.py`
  (März, Mai, Okt., Dez.). Leur absence du corpus est protégée.
- `0x1F5609F` : déjà traité par `mission_tab_labels.py` (All → Alle).
  Le patch exige une préimage EN intacte ; absence du corpus protégée.
- Le vouvoiement hiérarchique des subordonnés de Marlon est conservé. Son fils
  Zeph Jr. reste son fils ; la fille de la garde d'enfants laisse bien son fils.
  La formule autour du buffer « lad/lass » n'impose plus un article masculin.

Les cris, surnoms des échanges, noms d'espèces et lieux ne sont pas des oublis.
Les termes communs identiques, notamment Name, Winter, Show ou Dynamax, restent.

Cinq fragments ne doivent pas être insérés indépendamment :

| Offset | Conteneur hors lot | Motif |
|---|---|---|
| 0x1F5E5EF | 0x1F5E5E5 | Suffixe de page ; occurrence de pointeur dans un échantillon sonore |
| 0x1F7ECEF | 0x1F7EC6C | Début au milieu de « challenge », hit binaire dans un échantillon sonore |
| 0x1F7ECF1 | 0x1F7EC6C | Autre suffixe du même mot, hits dans un échantillon sonore |
| 0x1F80400 | 0x1F803F0 | Début au milieu de mot, hit non-script |
| 0x1F88900 | 0x1F8888D | Suffixe Zygarde ; hit 0xEFF2CB non-script, vrai msgbox vers le conteneur |

L'absence absolue de tout accès calculé ne peut pas être démontrée par un scan
statique ; les scripts parents et les références retenues sont consignés.

`0x1F80B7B` nécessite un périmètre séparé : aide UI préfixée sans pointeur exact,
avec suffixe vivant à `0x1F80B7C` hors lot. Ne pas raccourcir le préfixe en place
au risque de faire commencer le suffixe dans une commande. Aucun patch ni
ressource de données de jeu n'a été modifié.

`0x1F8E271` exige aussi un patch distinct : la chaîne canonique de 1045 octets
n'entre pas dans l'extraction utilisée par le build. Le texte DE intégral est
corrigé et protégé, mais le pointeur `0x1E9FA40` atteint encore l'anglais.
Le JSON conserve cette sortie, sans la présenter comme une correction injectée.

## Validation locale

Les 300 décisions sont couvertes par `tests/unit/test_dialogues_09_de.py`.
Les comparaisons ROM suivent 484 sites directs et les références des suffixes
préfixés ; elles comparent les chaînes cibles, les commandes ordonnées, les pages
et les budgets. Les retours FE/FA recalculés par le moteur sont neutralisés pour
la comparaison des mots, mais les pixels de la sortie réelle sont vérifiés.
Les adresses de relogement peuvent changer sans modifier le texte attendu.

La seconde passe raccourcit dix formulations dont le rewrap du moteur dépassait
192 pixels après ajout des icônes ou du glyphe B0. Les deux aides Safari sont
bornées à 232 pixels (avec une réserve de buffer supérieure au compteur réel).
Les tests existants F-601 ont leurs seules attentes du lot mises à jour ; la
matrice de parité ajoute uniquement le nouveau test DE exigé par le hook.

Commandes locales :

```sh
make build-de
make test-python
make lint
python3 -m pytest tests/unit/test_dialogues_09_de.py tests/unit/test_translation_integrity.py -q
python3 -m pytest tests/unit/de/test_f601_content_batches_de.py -q
npx playwright test --config tests/e2e-playwright/playwright.dialogues-09-de.config.ts
```

Les hooks restent activés : garde d'intégrité, périmètre DE, tests Python,
Vitest et builds locaux FR/IT/DE. Les logs finaux, la lecture des pointeurs et la
capture Playwright sont joints au ticket. Le test visuel appelle l'imprimante
native avec quatre chaînes accessibles dans la ROM reconstruite et affirme par
OCR Saugnapf/Wertehalter, Schwerball, Mega-Entwicklung et vollständig/geheilt.
La capture est créée dans le répertoire temporaire système, jamais versionnée.

## Non vérifié

Le parcours manuel de chacune des scènes n'est pas revendiqué. La preuve visuelle
utilise les pointeurs de la ROM finale et l'imprimante native mGBA, déclenchés par
un script temporaire ; elle ne démontre pas le parcours complet de chaque quête.
Aucun push, aucune exécution distante, aucun changement de source FR/IT.
