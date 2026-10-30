# PT-76 — Routes 17–18, 2–6 et missions

F-835 concerne exclusivement les 299 offsets explicites du manifeste PT-76.
F-758 (polices) et F-759 (glossaire) sont intégrés. Le domaine provisoire
« Scénario étendu » correspond aux routes 17, 18, 2, 3, 4–5, 6–7, à Challenge
Road, aux tutoriels de combat et aux missions Hero of the Hall et Leg Day.
Les noms propres restent anglais selon le glossaire ; aucun nom français de
lieu, d'objet ou de mouvement n'est importé.

## Bilan exhaustif et injection

`languages/pt/data/pt76_audit.json` est le bilan ordonné des 299 offsets :
préimage EN complète, texte anglais disponible, comparaison FR au même offset,
références et contextes binaires, statut, justification, texte PT, nombre
d'octets encodés et largeurs. Il couvre 295 entrées vivantes traduites ou
conservées selon F-759, avec 295 protections exactes et 561 références texte vivantes. Les noms Snivy, Tepig et
le label Route 3, absents du combined anglais, sont vérifiés dans la ROM EN.

Les commandes FC, FD, FA et FB restent identiques et dans le même ordre ;
seules les coupures FE sont adaptées. Le finaliseur `batch_76` encode les textes
verbatim après les réparations et la police, pour préserver aussi les boîtes de
mission (trois lignes, sans défilement). Les dialogues ont deux lignes initiales,
puis une ligne par FA. Limites : 180 pixels pour les dialogues et 172 pour les
missions ; dix glyphes larges par tampon runtime. FD08 est le suffixe pluriel
`s`, limité à un glyphe. Les tests mesurent également les cinq polices réelles
aux pointeurs finaux et vérifient tous les octets, terminateurs et chevauchements.

Les quatre clés à préfixe non textuel (0x1f5f052, 0x1f5fe97, 0x1f61aba,
0x1f646f7) sont résolues à leur vrai consommateur, avec conservation des préfixes
C046 ou 00. Les trois choix Snivy/Tepig/Oshawott et les entrées de mission sont
des tables de pointeurs, pas des cellules fixes à écraser. Aucun offset du lot
n'appartient aux tables fixes protégées. Le patch dédié reloge uniquement les
textes différents et repointe exclusivement les consommateurs audités.
Il réutilise le moteur structuré existant ; aucun code partagé n'est modifié.

Treize motifs de faux pointeurs de 0x1f62908 sont des opcodes `setflag`
consécutifs, pas des références au dialogue « Nadando, é claro! ». Seules les
références trainerbattle 0x1e8738d et 0x1e873b4 sont utilisées. Un motif graphique
supplémentaire vers 0x1f60af5 à 0x1066007 est également exclu. Le finaliseur
restaure ces quatorze mots après le pipeline générique et les teste octet par
octet. Il est atomique, idempotent et borné aux chaînes allouées et pointeurs.

## Exceptions

| Offset | Justification et preuve de pointeur |
|---|---|
| 0x1f5f3f1 | Suffixe interne de 0x1f5f3dd, sans lecteur texte. Le motif 0x127d725 est graphique. Le dialogue parent complet est traduit via 0x1e85e8f ; les contextes et motifs intérieurs sont dans l'audit. |
| 0x1f5f713 | Suffixe interne de 0x1f5f705, sans lecteur texte. Le motif 0x1339abd est graphique. Le dialogue parent complet est traduit via 0x1e85fec. |
| 0x1f62ebf | Alias avec bourrage 00, sans pointeur. Le label vivant 0x1f62ec0 figure lui-même au manifeste et possède quatre références, dont 0x1fb3fcc. Il est vérifié une seule fois. |
| 0x1f6375a | Dialogue Lapras d'attente sans référence au début ni consommateur intérieur dans la ROM EN. Le script vivant appelle 0x1f63747 par msgbox à 0x1e87bf1, ainsi qu'à 0x1e74035, 0x1e740b9 et 0x1e7420f. Aucune cellule fixe identifiée ; aucune injection autonome revendiquée. |

Ces quatre clés restent absentes du combined et des protections. Aucune
traduction existante n'est supprimée. Les suffixes morts partagent le stockage
du parent ; leur identité physique après injection n'est pas une exigence,
contrairement à l'intégrité des faux pointeurs graphiques.

## Vérification reproductible

- `python3 -m pytest tests/unit/pt/test_batch_pt76.py tests/unit/test_translation_integrity.py -q`
- `make build-pt`
- `python3 -m pytest tests/e2e/pt/test_batch_pt76_rom.py -m rom -q`
- `npx playwright test --config tests/e2e-playwright/playwright.pt76.config.ts`

Playwright utilise mGBA natif hors écran sur une copie temporaire de la ROM
finale. Le test vérifie les octets aux pointeurs vivants et les lignes affichées
par OCR, puis produit sa capture dans le répertoire temporaire système. Il ne
sauvegarde jamais en jeu. Les scènes choisies sont le dialogue de la route 17
et la proposition de soin de la route 2.

## Non vérifié

La sonde visuelle ne constitue pas un parcours intégral des routes ni une
vérification visuelle de chaque page ou des deux missions. La vérification
exhaustive des 295 consommateurs est binaire et métrique. La certification du
parcours complet et du registre reste du ressort de T-848.

## Résultats de reprise F-835

- Tests unitaires PT-76 : 5 réussis, dont comparaison exhaustive EN/FR.
- Intégrité générique : 30 réussis ; 295 protections exactes ajoutées.
- `make build-pt` : réussi ; 5 tests ROM PT-76 réussis sur la ROM finale.
- Playwright/mGBA hors écran : 1 test réussi, deux dialogues reconnus par OCR ;
  capture jointe au ticket F-835, hors dépôt.
- Ruff ciblé, TypeScript et `git diff --check` : réussis.
- Diff du combined : 295 ajouts, aucun retrait ni offset hors manifeste PT-76.

La reprise a aussi révélé que la garde pré-commit reparsait le manifeste pour
chaque traduction du lot. `check_staged_translation_tests.py` met désormais en
cache le manifeste et le combined pendant une seule validation, sans changer
les règles de protection. Un test vérifie une seule lecture par lot ainsi que
la prise en compte des valeurs modifiées à la validation suivante. Les 16 tests
de la garde passent ; ses diagnostics Ruff historiques sont inchangés.

Validation du script partagé : `make test-python` complet, 8 341 réussis,
3 skips préexistants configurés (pont émulateur, sonde FD FR, CSV dynamique ES),
aucun échec. Aucun skip ajouté par ce ticket.

Hooks actifs : 8 200 tests Python rapides réussis (1 skip existant),
80 tests Vitest réussis. Rebuild FR et IT réussis ; hash FR inchangé :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
