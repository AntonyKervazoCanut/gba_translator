# PT-BR — PT-10 : combat, statistiques et capture

## Périmètre et décisions

Les 282 offsets explicites du manifeste sont couverts : 260 textes vivants traités (252 valeurs localisées et huit valeurs volontairement identiques : cinq ponctuations, Magnitude et deux noms de statistiques conservés pour leur budget) et 22 exceptions justifiées. Le domaine réel est le combat (effets, changements de statistiques, envoi/rappel, capture et fuite), et non un lot de menus génériques.

Chaque traduction possède sa valeur exacte dans `protected_entries.yaml`. Les 22 exceptions ne sont pas ajoutées au combined. Aucun offset extérieur à PT-10 n’est traduit.

## Injection et contrôles

Les 260 textes possèdent des pointeurs absolus énumérés dans `languages/pt/data/pt10_audit.json` : table de combat `0x3fdf3c`, littéraux Thumb du moteur, tables CFRU et tableaux de noms de statistiques. Aucun n’appartient aux tables fixes indexées interdites par `fixed_tables.py`. Le patch PT `batch_10.py` réutilise `StructuredTextPatch` : validation de toutes les préimages, commandes et ruptures avant écriture, allocation hors cellules voisines, puis repointage des seuls consommateurs recensés. Cette finalisation évite de revendiquer une traduction ignorée ou remaniée par le constructeur générique.

Les octets FD et FC (avec tous leurs arguments), FA, FB et FE gardent leur ordre exact. Les budgets en octets ci-dessous comprennent le terminateur FF. Les textes relocalisables ne sont pas limités artificiellement à leur longueur anglaise. Les fenêtres de combat ont un budget de 224 pixels par ligne. Pour les deux textes défilants `0x3fca49` et `0x3fcaaa`, la limite de normalisation cumulée est 448 pixels car ce composant ne sépare pas FA ; le test ROM mesure séparément chaque ligne FE/FA/FB à 224 pixels.

## Statistiques et limites des variables

Les huit libellés retenus mesurent 12 à 57 pixels dans la police normale ; `Velocidade` mesure 57 pixels, soit trois de plus que l’estimation générique de 54 pixels par variable. Les templates de hausse/baisse sont donc contrôlés avec le véritable libellé. Avec le préfixe anglais encore vivant `The opposing ` et un surnom de dix W, la première ligne des quatre templates de statistiques atteint 202 pixels, sous la limite de 224.

Le séparateur avant FD01 reste dans le template pour ne pas coller les modificateurs hors lot. Les buffs de hausse/baisse normale et forte sont assemblés avec les vrais buffers PT (`!` et `muito`, avec espace séparateur dans le template). Le modificateur extrême `0xa4c603` est hors lot et demeure anglais : son intégration grammaticale n’est pas une traduction revendiquée par PT-10. Les noms et préfixes chargés depuis les autres lots peuvent eux aussi rester anglais. La variante objet place le verbe sur sa première ligne afin que la seconde supporte aussi le préfixe adverse, dix W et le modificateur extrême anglais. Les cas +1/+2/+3 sont mesurés pour les cinq templates, sans présumer si la branche objet peut effectivement atteindre +3. Une mesure sur les seuls glyphes littéraux ne prouve pas que toutes les expansions possibles des variables sont bornées ; les tests métier et la preuve visuelle doivent être lus avec cette limite.

## Noms de statistiques conservés

Conformément à la clause de budget du glossaire F-759, `0x3fd5a8` et `0x3fd5b0` conservent exactement `Sp. Atk` et `Sp. Def`. Les formes complètes Ataque Especial (85 px) et Defesa Especial (84 px) produiraient 230 et 229 pixels avec un nom adverse maximal dans les templates partagés, au-delà des 224 disponibles. Aucune abréviation PT improvisée n’est introduite. Ces deux entrées restent vivantes, protégées et vérifiées ; ce ne sont pas des exceptions mortes.

## Exceptions vérifiées à la source

Douze anciennes chaînes ont des consommateurs explicitement redirigés vers des remplacements hors lot. Les noms de slots ont été rapprochés de la [source FireRed de référence](https://github.com/pret/pokefirered/blob/master/src/battle_message.c), puis chaque pointeur et cible a été contrôlé dans la ROM Unbound locale. Les dix autres offsets sont des suffixes isolés, dans ou immédiatement après des cellules complètes : absence de pointeur propre et pointeurs du propriétaire consignés dans le JSON. Aucun de ces fragments n’est injecté séparément.

## État de validation

Validation locale réussie :

- `make build-pt` : 260 entrées vérifiées par la finalisation, dont 71 relocalisées pour retrouver exactement les textes et ruptures attendus.
- `python3 -m pytest tests/e2e/pt/test_batch_pt10_rom.py -m rom -q` : cinq tests réussis ; 305 pointeurs contrôlés, préimages, commandes, exceptions, atomicité, idempotence et budgets réels des cinq polices.
- `python3 -m pytest tests/unit/pt/test_batch_pt10.py tests/unit/test_translation_integrity.py -q` : 34 tests réussis. Le test de périmètre vérifie aussi la concordance du texte et du budget en octets consignés dans le JSON.
- `npx playwright test --config tests/e2e-playwright/playwright.pt10.config.ts` : un test réussi, mGBA et navigateur hors écran. Combat réel contre Rattata : « Griknot usou Metal Claw! », puis « Griknot: Ataque aumentou ! ». La troisième scène rend « Está chovendo. » via le pointeur vivant dans une msgbox. Les textes ne sont pas injectés en RAM : le moteur développe ses propres paramètres FD.
- Capture jointe au ticket F-769 (identifiant `9354c029-d5ac-4661-aca7-a769da010e93`), conservée hors dépôt.
- Hooks actifs : 5 035 tests Python réussis, un skip préexistant ; 68 tests Vitest réussis ; builds FR/IT/DE réussis. Aucun code partagé modifié, aucun push ni lancement de pipeline distant.
- Lint Python ciblé et `git diff --check` réussis.

### Non vérifié

La preuve visuelle couvre trois scènes représentatives, pas chaque message en situation de jeu. Les 260 entrées sont toutes vérifiées au niveau binaire. Les noms, préfixes et le modificateur extrême `0xa4c603` relevant d'autres lots peuvent rester anglais ; leur traduction appartient à ces lots et à T-848. Les deux noms de statistiques conservés pour budget sont détaillés plus haut.

## Bilan offset par offset

| Offset | État | EN → PT (source canonique) | Octets EN / PT | Pointeurs ou exception |
| --- | --- | --- | --- | --- |
| `0x3fbebe` | traduit/vérifié | `The Substitute took damage\nfor <0xFD><0x10>!<0xFB>` → `O substituto sofreu dano\npor <0xFD><0x10>!<0xFB>` | 36 / 34 | 0x3fe10c |
| `0x3fbee2` | traduit/vérifié | `<0xFD><0x10>'s\nSubstitute faded!<0xFB>` → `O substituto de <0xFD><0x10>\ndesapareceu!<0xFB>` | 24 / 33 | 0x3fe110 |
| `0x3fbefa` | traduit/vérifié | `<0xFD><0x0F> must\nrecharge!` → `<0xFD><0x0F> precisa\nrecarregar!` | 18 / 23 | 0x3fe114 |
| `0x3fbf0c` | traduit/vérifié | `<0xFD><0x10>'s Rage\nis building!` → `A fúria de <0xFD><0x10>\nestá crescendo!` | 23 / 30 | 0x3fe118 |
| `0x3fbf23` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x00>\nwas disabled!` → `<0xFD><0x10>: <0xFD><0x00>\nfoi desativado!` | 22 / 23 | 0x3fe11c |
| `0x3fbf39` | traduit/vérifié | `<0xFD><0x0F> is disabled\nno more!` → `<0xFD><0x0F> não está\nmais desativado!` | 24 / 29 | 0x3fe124 |
| `0x3fbf51` | traduit/vérifié | `<0xFD><0x10> got\nan Encore!` → `<0xFD><0x10> recebeu\num Encore!` | 18 / 22 | 0x3fe128 |
| `0x3fbf63` | traduit/vérifié | `<0xFD><0x0F>'s Encore\nended!` → `O Encore de <0xFD><0x0F>\nacabou!` | 19 / 23 | 0x3fe12c |
| `0x3fbf76` | traduit/vérifié | `<0xFD><0x0F> took aim\nat <0xFD><0x10>!` → `<0xFD><0x0F> mirou\nem <0xFD><0x10>!` | 19 / 16 | 0x3fe130 |
| `0x3fbf89` | traduit/vérifié | `<0xFD><0x0F> Sketched\n<0xFD><0x00>!` → `<0xFD><0x0F> copiou\n<0xFD><0x00>!` | 16 / 14 | 0x3fe134 |
| `0x3fbf99` | traduit/vérifié | `<0xFD><0x0F> is trying\nto take its foe with it!` → `<0xFD><0x0F> tenta levar\no inimigo consigo!` | 38 / 34 | 0x3fe138 |
| `0x3fbfbf` | traduit/vérifié | `<0xFD><0x10> took\n<0xFD><0x0F> with it!` → `<0xFD><0x10> levou\n<0xFD><0x0F> consigo!` | 20 / 21 | 0x3fe13c |
| `0x3fbfd3` | traduit/vérifié | `Reduced <0xFD><0x10>'s\n<0xFD><0x00> by <0xFD><0x01>!` → `Para <0xFD><0x10>,\n<0xFD><0x00> perdeu <0xFD><0x01> PP!` | 23 / 26 | 0x3fe140 |
| `0x3fbfea` | traduit/vérifié | `<0xFD><0x0F> stole\n<0xFD><0x10>'s <0xFD><0x16>!` → `<0xFD><0x0F> roubou de\n<0xFD><0x10> o item <0xFD><0x16>!` | 18 / 27 | 0x3fe144 |
| `0x3fc011` | traduit/vérifié | `<0xFD><0x10> fell into\na Nightmare!` → `<0xFD><0x10> caiu em\num pesadelo!` | 26 / 24 | 0x3fe14c |
| `0x3fc02b` | traduit/vérifié | `<0xFD><0x0F> is locked\nin a Nightmare!` → `<0xFD><0x0F> está preso\nnum pesadelo!` | 29 / 28 | 0x3fe150 |
| `0x3fc048` | traduit/vérifié | `<0xFD><0x0F> cut its own HP\nand laid a Curse on<0xFA><0xFD><0x10>!` → `<0xFD><0x0F> perdeu PS\ne amaldiçoou<0xFA><0xFD><0x10>!` | 42 / 30 | 0x3fe154 |
| `0x3fc072` | traduit/vérifié | `<0xFD><0x0F> is afflicted\nby the Curse!` → `<0xFD><0x0F> sofre\ncom a maldição!` | 30 / 25 | 0x3fe158 |
| `0x3fc090` | traduit/vérifié | `Spikes were scattered all around\nthe opposing team!` → `Spikes espalhados ao redor\nda equipe adversária!` | 52 / 49 | 0x271afc, 0x3fe15c |
| `0x3fc0dc` | traduit/vérifié | `<0xFD><0x0F> identified\n<0xFD><0x10>!` → `<0xFD><0x0F> identificou\n<0xFD><0x10>!` | 18 / 19 | 0x3fe164 |
| `0x3fc0ee` | traduit/vérifié | `<0xFD><0x0F>'s Perish count\nfell to <0xFD><0x00>!` → `A contagem de <0xFD><0x0F>\ncaiu para <0xFD><0x00>!` | 30 / 31 | 0x3fe168 |
| `0x3fc10c` | traduit/vérifié | `<0xFD><0x0F> braced\nitself!` → `<0xFD><0x0F> se\npreparou!` | 18 / 16 | 0x3fe16c |
| `0x3fc11e` | traduit/vérifié | `<0xFD><0x10> endured\nthe hit!` → `<0xFD><0x10> resistiu\nao golpe!` | 20 / 22 | 0x3fe170 |
| `0x3fc132` | traduit/vérifié | `Magnitude <0xFD><0x00>!` → `Magnitude <0xFD><0x00>!` | 14 / 14 | 0x3fe174 |
| `0x3fc140` | traduit/vérifié | `<0xFD><0x0F> cut its own HP\nand maximized Attack!` → `<0xFD><0x0F> perdeu PS\ne maximizou seu Ataque!` | 40 / 37 | 0x3fe178 |
| `0x3fc168` | traduit/vérifié | `<0xFD><0x0F> copied\n<0xFD><0x10>'s stat changes!` → `<0xFD><0x0F> copiou de\n<0xFD><0x10> as mudanças de stats!` | 29 / 38 | 0x3fe17c |
| `0x3fc185` | traduit/vérifié | `<0xFD><0x0F> got free of\n<0xFD><0x10>'s <0xFD><0x00>!` → `<0xFD><0x0F> se livrou de\n<0xFD><0x10>: <0xFD><0x00>!` | 24 / 24 | 0x3fe180 |
| `0x3fc19d` | traduit/vérifié | `<0xFD><0x0F> shed\nLeech Seed!` → `<0xFD><0x0F> se livrou\nde Leech Seed!` | 20 / 28 | 0x3fe184 |
| `0x3fc1c6` | traduit/vérifié | `<0xFD><0x0F> fled from\nbattle!` → `<0xFD><0x0F> fugiu\nda batalha!` | 21 / 21 | 0x3fe18c |
| `0x3fc1db` | traduit/vérifié | `<0xFD><0x0F> foresaw\nan attack!` → `<0xFD><0x0F> previu\num ataque!` | 22 / 21 | 0x3fe190 |
| `0x3fc1f1` | traduit/vérifié | `<0xFD><0x10> took the\n<0xFD><0x00> attack!` → `<0xFD><0x10> sofreu\no ataque <0xFD><0x00>!` | 23 / 23 | 0x3fe194 |
| `0x3fc208` | traduit/vérifié | `<0xFD><0x0F> chose\n<0xFD><0x14> as its destiny!` → `<0xFD><0x0F> escolheu\n<0xFD><0x14> como destino!` | 28 / 29 | 0x3fe448 |
| `0x3fc224` | traduit/vérifié | `<0xFD><0x00>'s attack!` → `Ataque de <0xFD><0x00>!` | 13 / 14 | 0x3fe198 |
| `0x3fc231` | traduit/vérifié | `<0xFD><0x10> became the\ncenter of attention!` → `<0xFD><0x10> virou\no centro das atenções!` | 35 / 32 | 0x3fe19c |
| `0x3fc254` | traduit/vérifié | `<0xFD><0x0F> began\ncharging power!` → `<0xFD><0x0F> começou\na acumular energia!` | 25 / 31 | 0x3fe1a0 |
| `0x3fc26d` | traduit/vérifié | `Nature Power turned into\n<0xFD><0x14>!` → `Nature Power virou\n<0xFD><0x14>!` | 29 / 23 | 0x3fe1a4 |
| `0x3fc28a` | traduit/vérifié | `<0xFD><0x0F>'s status\nreturned to normal!` → `O estado de <0xFD><0x0F>\nvoltou ao normal!` | 32 / 33 | 0x3fe1a8 |
| `0x3fc2aa` | traduit/vérifié | `<0xFD><0x10> was subjected\nto Torment!` → `<0xFD><0x10> sofreu\num Torment!` | 29 / 22 | 0x3fe1b0 |
| `0x3fc2c7` | traduit/vérifié | `<0xFD><0x0F> is tightening\nits focus!` → `<0xFD><0x0F> está\nse concentrando!` | 28 / 25 | 0x3fe1b8 |
| `0x3fc2e3` | traduit/vérifié | `<0xFD><0x10> fell for\nthe Taunt!` → `<0xFD><0x10> caiu\nno Taunt!` | 23 / 18 | 0x3fe1bc |
| `0x3fc2fa` | traduit/vérifié | `<0xFD><0x0F> is ready to\nhelp <0xFD><0x10>!` → `<0xFD><0x0F> vai\najudar <0xFD><0x10>!` | 24 / 18 | 0x3fe1c4 |
| `0x3fc312` | traduit/vérifié | `<0xFD><0x0F> switched\nitems with its opponent!` → `<0xFD><0x0F> trocou\nitens com o oponente!` | 37 / 32 | 0x3fe1c8 |
| `0x3fc337` | traduit/vérifié | `<0xFD><0x0F> obtained\n<0xFD><0x00>.` → `<0xFD><0x0F> obteve\n<0xFD><0x00>.` | 16 / 14 | 0x3fe4a4 |
| `0x3fc347` | traduit/vérifié | `<0xFD><0x10> obtained\n<0xFD><0x01>.` → `<0xFD><0x10> obteve\n<0xFD><0x01>.` | 16 / 14 | 0x3fe4a8 |
| `0x3fc357` | traduit/vérifié | `<0xFD><0x0F> obtained\n<0xFD><0x00>.<0xFB><0xFD><0x10> obtained\n<0xFD><0x01>.` → `<0xFD><0x0F> obteve\n<0xFD><0x00>.<0xFB><0xFD><0x10> obteve\n<0xFD><0x01>.` | 32 / 28 | 0x3fe4ac |
| `0x3fc377` | traduit/vérifié | `<0xFD><0x0F> copied\n<0xFD><0x10>'s <0xFD><0x19>!` → `<0xFD><0x0F> copiou de\n<0xFD><0x10> a Habilidade <0xFD><0x19>!` | 19 / 33 | 0x3fe1cc |
| `0x3fc38a` | traduit/vérifié | `<0xFD><0x0F> made a Wish!` → `<0xFD><0x0F> fez um pedido!` | 16 / 18 | 0x3fe1d0 |
| `0x3fc39a` | traduit/vérifié | `<0xFD><0x00>'s Wish\ncame true!` → `O pedido de <0xFD><0x00>\nse realizou!` | 21 / 28 | 0x3fe1d4 |
| `0x3fc3af` | traduit/vérifié | `<0xFD><0x0F> planted its\nroots!` → `<0xFD><0x0F> criou\nraízes!` | 22 / 17 | 0x3fe1d8 |
| `0x3fc3c5` | traduit/vérifié | `<0xFD><0x0F> absorbed\nnutrients with its roots!` → `<0xFD><0x0F> absorveu\nnutrientes pelas raízes!` | 38 / 37 | 0x3fe1dc |
| `0x3fc3eb` | traduit/vérifié | `<0xFD><0x10> anchored\nitself with its roots!` → `<0xFD><0x10> se firmou\ncom suas raízes!` | 35 / 30 | 0x3fe1e0 |
| `0x3fc40e` | traduit/vérifié | `<0xFD><0x0F> made\n<0xFD><0x10> drowsy!` → `<0xFD><0x0F> deixou\n<0xFD><0x10> com sono!` | 19 / 23 | 0x3fe1e4 |
| `0x3fc421` | traduit/vérifié | `<0xFD><0x0F> knocked off\n<0xFD><0x10>'s <0xFD><0x16>!` → `<0xFD><0x0F> tirou de\n<0xFD><0x10> o item <0xFD><0x16>!` | 24 / 26 | 0x3fe1e8 |
| `0x3fc439` | traduit/vérifié | `<0xFD><0x0F> swapped\nabilities with its opponent!` → `<0xFD><0x0F> trocou\nHabilidades com o oponente!` | 40 / 38 | 0x3fe1ec |
| `0x3fc461` | traduit/vérifié | `<0xFD><0x0F> sealed the\nopponent's move(s)!` → `<0xFD><0x0F> selou os\nmovimentos do oponente!` | 34 / 36 | 0x3fe1f0 |
| `0x3fc483` | traduit/vérifié | `<0xFD><0x0F> wants the\nopponent to bear a Grudge!` → `<0xFD><0x0F> quer que o\noponente sofra um Grudge!` | 40 / 40 | 0x3fe1f8 |
| `0x3fc4ab` | traduit/vérifié | `<0xFD><0x0F>'s <0xFD><0x00>\nlost all its PP due to the Grudge!` → `<0xFD><0x0F>: <0xFD><0x00>\nperdeu todos os PP por Grudge!` | 43 / 38 | 0x3fe1fc |
| `0x3fc4d6` | traduit/vérifié | `<0xFD><0x0F> shrouded\nitself in <0xFD><0x14>!` → `<0xFD><0x0F> se envolveu\nem <0xFD><0x14>!` | 26 / 22 | 0x3fe200 |
| `0x3fc4f0` | traduit/vérifié | `<0xFD><0x0F>'s <0xFD><0x14>\nwas bounced back by Magic Coat!` → `<0xFD><0x0F>: <0xFD><0x14>\nfoi refletido por Magic Coat!` | 40 / 37 | 0x3fe204 |
| `0x3fc518` | traduit/vérifié | `<0xFD><0x0F> waits for its foe\nto make a move!` → `<0xFD><0x0F> espera\no inimigo agir!` | 37 / 26 | 0x3fe208 |
| `0x3fc53d` | traduit/vérifié | `<0xFD><0x10> Snatched\n<0xFD><0x13>'s move!` → `<0xFD><0x10> roubou\no movimento de <0xFD><0x13>!` | 23 / 29 | 0x3fe20c |
| `0x3fc554` | traduit/vérifié | `Electricity's power was\nweakened!` → `O poder da eletricidade\nfoi reduzido!` | 34 / 38 | 0x3fe3f8 |
| `0x3fc576` | traduit/vérifié | `Fire's power was\nweakened!` → `O poder do fogo\nfoi reduzido!` | 27 / 30 | 0x3fe3fc |
| `0x3fc591` | traduit/vérifié | `<0xFD><0x0F> found\none <0xFD><0x16>!` → `<0xFD><0x0F> achou\num <0xFD><0x16>!` | 17 / 16 | 0x3fe40c |
| `0x3fc5a2` | traduit/vérifié | `A soothing aroma wafted\nthrough the area!` → `Um aroma suave se espalhou\npela área!` | 42 / 38 | 0x3fe414 |
| `0x3fc5cc` | traduit/vérifié | `Items can't be used now.<0xFC><0x08><0x40>` → `Não pode usar itens agora.<0xFC><0x08><0x40>` | 28 / 30 | 0x3fe418 |
| `0x3fc5e8` | traduit/vérifié | `For <0xFD><0x13>,\n<0xFD><0x16> <0xFD><0x00>` → `Para <0xFD><0x13>,\n<0xFD><0x16> <0xFD><0x00>` | 14 / 15 | 0x3fe41c |
| `0x3fc60c` | traduit/vérifié | `<0xFD><0x0F> lost its\nfocus and couldn't move!` → `<0xFD><0x0F> perdeu o foco\ne não pôde agir!` | 37 / 34 | 0x3fe44c |
| `0x3fc631` | traduit/vérifié | `<0xFD><0x10> was\ndragged out!<0xFB>` → `<0xFD><0x10> foi\nforçado a sair!<0xFB>` | 21 / 24 | 0x3fe45c |
| `0x3fc646` | traduit/vérifié | `The wall shattered!` → `A barreira se quebrou!` | 20 / 23 | 0x3fe494, 0xa0a518 |
| `0x3fc65a` | traduit/vérifié | `But it had no effect!` → `Mas não teve efeito!` | 22 / 21 | 0x3fe4b0 |
| `0x3fc670` | traduit/vérifié | `<0xFD><0x12> has no\nmoves left!<0xFB>` → `<0xFD><0x12> está\nsem movimentos!<0xFB>` | 23 / 25 | 0x3fe1ac |
| `0x3fc687` | traduit/vérifié | `<0xFD><0x12>'s <0xFD><0x14>\nis disabled!<0xFB>` → `<0xFD><0x12>: <0xFD><0x14>\nestá desativado!<0xFB>` | 22 / 25 | 0x3fe120 |
| `0x3fc69d` | traduit/vérifié | `<0xFD><0x12> can't use the same\nmove in a row due to the Torment!<0xFB>` → `<0xFD><0x12> não pode repetir\no movimento por Torment!<0xFB>` | 57 / 46 | 0x3fe1b4 |
| `0x3fc6d6` | traduit/vérifié | `<0xFD><0x12> can't use\n<0xFD><0x14> after the Taunt!<0xFB>` → `<0xFD><0x12> não pode usar\n<0xFD><0x14> após Taunt!<0xFB>` | 34 / 33 | 0x3fe1c0 |
| `0x3fc6f8` | traduit/vérifié | `<0xFD><0x12> can't use the\nsealed <0xFD><0x14>!<0xFB>` → `<0xFD><0x12> não pode usar\no selado <0xFD><0x14>!<0xFB>` | 29 / 31 | 0x3fe1f4 |
| `0x3fc715` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\nmade it rain!` → `<0xFD><0x13>: <0xFD><0x1A>\nfez chover!` | 22 / 19 | 0x3fe210 |
| `0x3fc72b` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\nraised its Speed!` → `<0xFD><0x13>: <0xFD><0x1A>\naumentou sua Velocidade!` | 26 / 32 | 0x3fe214 |
| `0x3fc745` | traduit/vérifié | `<0xFD><0x10> was protected\nby <0xFD><0x19>!` → `<0xFD><0x10> foi protegido\npor <0xFD><0x19>!` | 24 / 25 | 0x3fe218 |
| `0x3fc75d` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nprevents <0xFD><0x0F><0xFA>from using <0xFD><0x14>!` → `<0xFD><0x10>: <0xFD><0x19>\nimpede <0xFD><0x0F><0xFA>de usar <0xFD><0x14>!` | 35 / 29 | 0x3fe21c |
| `0x3fc780` | traduit/vérifié | `<0xFD><0x10> restored HP\nusing its <0xFD><0x19>!` → `<0xFD><0x10> recuperou PS\ncom <0xFD><0x19>!` | 29 / 24 | 0x3fe220 |
| `0x3fc79d` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nmade <0xFD><0x14> useless!` → `<0xFD><0x10>: <0xFD><0x19>\nanulou <0xFD><0x14>!` | 25 / 18 | 0x3fe428 |
| `0x3fc7b6` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nmade it the <0xFD><0x00> type!` → `<0xFD><0x10>: <0xFD><0x19>\ndeu-lhe o tipo <0xFD><0x00>!` | 29 / 26 | 0x3fe224 |
| `0x3fc7d3` | traduit/vérifié | `<0xFD><0x11>'s <0xFD><0x19>\nprevents paralysis!` → `<0xFD><0x11>: <0xFD><0x19>\nimpede paralisia!` | 28 / 25 | 0x3fe228 |
| `0x3fc7ef` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nprevents romance!` → `<0xFD><0x10>: <0xFD><0x19>\nimpede a paixão!` | 26 / 24 | 0x3fe22c |
| `0x3fc809` | traduit/vérifié | `<0xFD><0x11>'s <0xFD><0x19>\nprevents poisoning!` → `<0xFD><0x11>: <0xFD><0x19>\nimpede envenenamento!` | 28 / 29 | 0x3fe230 |
| `0x3fc825` | exception justifiée | `<0xFD><0x10>'s <0xFD><0x19>\nprevents confusion!` → — | 28 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4b312 via 0x3fe234, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fc841` | exception justifiée | `<0xFD><0x10>'s <0xFD><0x19>\nraised its Fire power!` → — | 31 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa37a4d via 0x3fe238, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fc860` | traduit/vérifié | `<0xFD><0x10> anchors\nitself!` → `<0xFD><0x10> se\nfirmou!` | 19 / 14 | 0x3fe23c |
| `0x3fc873` | exception justifiée | `ith <0xFD><0x19>!` → — | 8 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fc860. Le consommateur vise cette cellule complète, pas 0x3fc873; écriture autonome interdite. |
| `0x3fc87b` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\ncuts <0xFD><0x10>'s Attack!` → `<0xFD><0x13>: <0xFD><0x1A>\nreduz o Ataque de <0xFD><0x10>!` | 26 / 29 | 0x3fe240 |
| `0x3fc895` | exception justifiée | `<0xFD><0x13>'s <0xFD><0x1A>\nprevents stat loss!` → — | 28 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4b2dc via 0x3fe244, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fc8b1` | exception justifiée | `<0xFD><0x10>'s <0xFD><0x19>\nhurt <0xFD><0x0F>!` → — | 17 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa37be3 via 0x3fe248, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fc8c2` | traduit/vérifié | `<0xFD><0x13> traced\n<0xFD><0x00>'s <0xFD><0x01>!` → `<0xFD><0x13> copiou de\n<0xFD><0x00> a Habilidade <0xFD><0x01>!` | 19 / 33 | 0x3fe24c |
| `0x3fc8d5` | traduit/vérifié | `<0xFD><0x11>'s <0xFD><0x1B>\nprevents burns!` → `<0xFD><0x11>: <0xFD><0x1B>\nimpede queimaduras!` | 24 / 27 | 0x3fe3d0 |
| `0x3fc8ed` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nblocks <0xFD><0x14>!` → `<0xFD><0x10>: <0xFD><0x19>\nbloqueia <0xFD><0x14>!` | 19 / 20 | 0x3fe3d4 |
| `0x3fc900` | exception justifiée | `<0xFD><0x13>'s <0xFD><0x1A>\nblocks <0xFD><0x14>!` → — | 19 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4b32e via 0x3fe484, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fc913` | traduit/vérifié | `<0xFD><0x0F>'s <0xFD><0x18>\nrestored its HP!` → `<0xFD><0x0F>: <0xFD><0x18>\nrecuperou seus PS!` | 25 / 26 | 0x3fe3d8 |
| `0x3fc92c` | exception justifiée | ` little!` → — | 9 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fc913. Le consommateur vise cette cellule complète, pas 0x3fc92c; écriture autonome interdite. |
| `0x3fc935` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\nwhipped up a sandstorm!` → `<0xFD><0x13>: <0xFD><0x1A>\ncriou tempestade de areia!` | 32 / 34 | 0x3fe3dc |
| `0x3fc955` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\nintensified the sun's rays!` → `<0xFD><0x13>: <0xFD><0x1A>\nintensificou a luz do sol!` | 36 / 34 | 0x3fe438 |
| `0x3fc979` | exception justifiée | `<0xFD><0x13>'s <0xFD><0x1A>\nprevents <0xFD><0x00> loss!` → — | 26 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4b2f9 via 0x3fe3e0, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fc993` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\ninfatuated <0xFD><0x0F>!` → `<0xFD><0x10>: <0xFD><0x19>\napaixonou <0xFD><0x0F>!` | 23 / 21 | 0x3fe3e4 |
| `0x3fc9aa` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nmade <0xFD><0x14> ineffective!` → `<0xFD><0x10>: <0xFD><0x19>\nanulou <0xFD><0x14>!` | 29 / 18 | 0x3fe3e8 |
| `0x3fc9c7` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\ncured its <0xFD><0x00> problem!` → `<0xFD><0x13>: <0xFD><0x1A>\ncurou seu problema de <0xFD><0x00>!` | 30 / 33 | 0x3fe3ec |
| `0x3fc9e5` | traduit/vérifié | `It sucked up the\nLiquid Ooze!` → `Ele absorveu o\nLiquid Ooze!` | 30 / 28 | 0x3fe3f0 |
| `0x3fca03` | traduit/vérifié | `<0xFD><0x13> transformed!` → `<0xFD><0x13> se transformou!` | 16 / 19 | 0x3fe3f4 |
| `0x3fca13` | traduit/vérifié | `<0xFD><0x10> took the\nattack!` → `<0xFD><0x10> recebeu\no ataque!` | 20 / 21 | 0x3fe444 |
| `0x3fca27` | exception justifiée | `ack!` → — | 5 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fca13. Le consommateur vise cette cellule complète, pas 0x3fca27; écriture autonome interdite. |
| `0x3fca2c` | traduit/vérifié | `<0xFD><0x00>'s <0xFD><0x17>\nprevents switching!<0xFB>` → `<0xFD><0x00>: <0xFD><0x17>\nimpede a troca!<0xFB>` | 29 / 24 | 0x443ec |
| `0x3fca49` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x19>\nprevented <0xFD><0x13>'s<0xFA><0xFD><0x00> from working!` → `<0xFD><0x10>: <0xFD><0x19>\nimpediu <0xFD><0x13>:<0xFA><0xFD><0x00> não funciona!` | 40 / 36 | 0x3fe460 |
| `0x3fca71` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\nmade it ineffective!` → `<0xFD><0x13>: <0xFD><0x1A>\nanulou o efeito!` | 29 / 24 | 0x3fe474 |
| `0x3fca8e` | traduit/vérifié | `<0xFD><0x11>'s <0xFD><0x1B>\nprevents flinching!` → `<0xFD><0x11>: <0xFD><0x1B>\nimpede recuos!` | 28 / 22 | 0x3fe478 |
| `0x3fcaaa` | traduit/vérifié | `<0xFD><0x0F>'s <0xFD><0x18>\nprevents <0xFD><0x10>'s<0xFA><0xFD><0x19> from working!` → `<0xFD><0x0F>: <0xFD><0x18>\nimpede <0xFD><0x10>:<0xFA><0xFD><0x19> não funciona!` | 39 / 35 | 0x3fe498 |
| `0x3fcad1` | exception justifiée | `<0xFD><0x13>'s <0xFD><0x1A>\ncured its <0xFD><0x00> problem!` → — | 30 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa37a75 via 0x3fe49c, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fcaef` | traduit/vérifié | `<0xFD><0x13>'s <0xFD><0x1A>\nhad no effect on <0xFD><0x11>!` → `<0xFD><0x13>: <0xFD><0x1A>\nnão afetou <0xFD><0x11>!` | 29 / 22 | 0x3fe4b4 |
| `0x3fcb0c` | traduit/vérifié | `<0xFD><0x0F> is too scared to move!` → `<0xFD><0x0F> tem medo de agir!` | 26 / 21 | 0x3fe4f4 |
| `0x3fcb26` | traduit/vérifié | `Ghost: Get out"" Get out""` → `Fantasma: Fora... Fora...` | 27 / 26 | 0x3fe4f8 |
| `0x3fcb41` | traduit/vérifié | `sharply ` → `muito` | 9 / 6 | 0x3fe250 |
| `0x3fcb4a` | traduit/vérifié | `rose!` → `!` | 6 / 2 | 0x42d9c, 0x3fe254 |
| `0x3fcb4b` | exception justifiée | `ose!` → — | 5 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fcb4a. Le consommateur vise cette cellule complète, pas 0x3fcb4b; écriture autonome interdite. |
| `0x3fcb50` | traduit/vérifié | `harshly ` → `muito` | 9 / 6 | 0x3fe258 |
| `0x3fcb59` | traduit/vérifié | `fell!` → `!` | 6 / 2 | 0x3fe25c |
| `0x3fcb5f` | traduit/vérifié | `<0xFD><0x0F>'s <0xFD><0x00>\n<0xFD><0x01>` → `<0xFD><0x0F>: <0xFD><0x00>\naumentou <0xFD><0x01>` | 11 / 19 | 0x3fe260 |
| `0x3fcb6a` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x00>\n<0xFD><0x01>` → `<0xFD><0x10>: <0xFD><0x00>\naumentou <0xFD><0x01>` | 11 / 19 | 0x42da0, 0x3fe264, 0xa0ce4c |
| `0x3fcb75` | traduit/vérifié | `Using <0xFD><0x16>, the <0xFD><0x00> of\n<0xFD><0x13> <0xFD><0x01>` → `<0xFD><0x16> elevou <0xFD><0x00> de\n<0xFD><0x13> <0xFD><0x01>` | 26 / 22 | 0x3fe420 |
| `0x3fcb8f` | traduit/vérifié | `<0xFD><0x0F>'s <0xFD><0x00>\n<0xFD><0x01>` → `<0xFD><0x0F>: <0xFD><0x00>\ndiminuiu <0xFD><0x01>` | 11 / 19 | 0x3fe268 |
| `0x3fcb9a` | traduit/vérifié | `<0xFD><0x10>'s <0xFD><0x00>\n<0xFD><0x01>` → `<0xFD><0x10>: <0xFD><0x00>\ndiminuiu <0xFD><0x01>` | 11 / 19 | 0x3fe26c |
| `0x3fcba5` | traduit/vérifié | `<0xFD><0x0F>'s stats won't\ngo any higher!` → `Os stats de <0xFD><0x0F>\nnão podem subir mais!` | 32 / 37 | 0x3fdf70 |
| `0x3fcbc5` | traduit/vérifié | `<0xFD><0x10>'s stats won't\ngo any lower!` → `Os stats de <0xFD><0x10>\nnão podem cair mais!` | 31 / 36 | 0x3fe480 |
| `0x3fcbe4` | exception justifiée | `A critical hit!` → — | 16 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4a98c via 0x3fe270, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fcbf4` | traduit/vérifié | `It's a one-hit KO!` → `Nocaute em um só golpe!` | 19 / 24 | 0x3fe274 |
| `0x3fcc07` | traduit/vérifié | `<0xFC><0x08><0x20>1, <0xFC><0x08><0x0F>2, and<0xFC><0x08><0x0F>" <0xFC><0x08><0x0F>" <0xFC><0x08><0x0F>" <0xFC><0x08><0x0F><0xFC><0x10><0x31><0x00>Poof!<0xFB>` → `<0xFC><0x08><0x20>1, <0xFC><0x08><0x0F>2, e<0xFC><0x08><0x0F>... <0xFC><0x08><0x0F>... <0xFC><0x08><0x0F>... <0xFC><0x08><0x0F><0xFC><0x10><0x31><0x00> Puf!<0xFB>` | 44 / 48 | 0x3fe278 |
| `0x3fcc33` | traduit/vérifié | `And"<0xFB>` → `E...<0xFB>` | 6 / 6 | 0x3fe27c |
| `0x3fcc39` | traduit/vérifié | `HM moves can't be\nforgotten now.<0xFB>` → `Movimentos HM não podem\nser esquecidos agora.<0xFB>` | 34 / 47 | 0x3fe408 |
| `0x3fcc5b` | traduit/vérifié | `It's not very effective"` → `Não é muito eficaz...` | 25 / 22 | 0x3fe280 |
| `0x3fcc74` | traduit/vérifié | `It's super effective!` → `É supereficaz!` | 22 / 15 | 0x3fe284 |
| `0x3fcc8a` | traduit/vérifié | `<0xFC><0x10><0x11><0x00>Got away safely!<0xFB>` → `<0xFC><0x10><0x11><0x00> Fugiu em segurança!<0xFB>` | 22 / 26 | 0xd7698, 0x3fe288, 0x9be140 |
| `0x3fcca0` | traduit/vérifié | `<0xFC><0x10><0x11><0x00><0xFD><0x0F> fled\nusing its <0xFD><0x16>!<0xFB>` → `<0xFC><0x10><0x11><0x00> <0xFD><0x0F> fugiu\nusando <0xFD><0x16>!<0xFB>` | 27 / 26 | 0x3fe454 |
| `0x3fccbb` | traduit/vérifié | `<0xFC><0x10><0x11><0x00><0xFD><0x0F> fled\nusing <0xFD><0x18>!<0xFB>` → `<0xFC><0x10><0x11><0x00> <0xFD><0x0F> fugiu\nusando <0xFD><0x18>!<0xFB>` | 23 / 26 | 0x3fe458 |
| `0x3fccd2` | traduit/vérifié | `<0xFC><0x10><0x11><0x00>Wild <0xFD><0x00> fled!` → `<0xFC><0x10><0x11><0x00> <0xFD><0x00> selvagem fugiu!` | 18 / 24 | 0x3fe28c |
| `0x3fcce4` | traduit/vérifié | `Player defeated\n<0xFD><0x20>!` → `Você venceu\n<0xFD><0x20>!` | 20 / 16 | 0xd77a4, 0x9be114 |
| `0x3fcce5` | exception justifiée | `layer defeated\n<0xFD><0x20>!` → — | 19 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fcce4. Le consommateur vise cette cellule complète, pas 0x3fcce5; écriture autonome interdite. |
| `0x3fccf8` | traduit/vérifié | `Player beat <0xFD><0x20>\nand <0xFD><0x21>!` → `Você venceu <0xFD><0x20>\ne <0xFD><0x21>!` | 23 / 21 | 0xd7724, 0x9be14c |
| `0x3fcd0f` | traduit/vérifié | `Player lost against\n<0xFD><0x20>!` → `Você perdeu para\n<0xFD><0x20>!` | 24 / 21 | 0xd77ac, 0x9be118 |
| `0x3fcd27` | traduit/vérifié | `Player lost to <0xFD><0x20>\nand <0xFD><0x21>!` → `Você perdeu para <0xFD><0x20>\ne <0xFD><0x21>!` | 26 / 26 | 0xd772c, 0x9be148 |
| `0x3fcd41` | traduit/vérifié | `Player battled to a draw against\n<0xFD><0x20>!` → `Você empatou com\n<0xFD><0x20>!` | 37 / 21 | 0xd77b4, 0x9be150 |
| `0x3fcd66` | traduit/vérifié | `Player battled to a draw against\n<0xFD><0x20> and <0xFD><0x21>!` → `Você empatou com\n<0xFD><0x20> e <0xFD><0x21>!` | 44 / 26 | 0xd7734, 0x9be100 |
| `0x3fcd92` | traduit/vérifié | `<0xFC><0x10><0x11><0x00><0xFD><0x20> fled!` → `<0xFC><0x10><0x11><0x00> <0xFD><0x20> fugiu!` | 13 / 15 | 0xd76cc |
| `0x3fcd9f` | traduit/vérifié | `<0xFC><0x10><0x11><0x00><0xFD><0x20> and\n<0xFD><0x21> fled!` → `<0xFC><0x10><0x11><0x00> <0xFD><0x20> e\n<0xFD><0x21> fugiram!` | 20 / 22 | 0xd76b0, 0x9be144 |
| `0x3fcdb3` | traduit/vérifié | `No! There's no running\nfrom a Trainer battle!<0xFB>` → `Não! Não pode fugir de\nbatalhas com Treinadores!<0xFB>` | 47 / 50 | 0x3fe290 |
| `0x3fcde2` | traduit/vérifié | `Can't escape!<0xFB>` → `Não pode fugir!<0xFB>` | 15 / 17 | 0x3fe294 |
| `0x3fcdf2` | traduit/vérifié | `But nothing happened!` → `Mas nada aconteceu!` | 22 / 20 | 0x3fe29c |
| `0x3fcdf3` | exception justifiée | `ut nothing happened!` → — | 21 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fcdf2. Le consommateur vise cette cellule complète, pas 0x3fcdf3; écriture autonome interdite. |
| `0x3fce08` | traduit/vérifié | `But it failed!` → `Mas falhou!` | 15 / 12 | 0x3fe2a0 |
| `0x3fce17` | traduit/vérifié | `It hurt itself in its\nconfusion!` → `Feriu a si mesmo\nna confusão!` | 33 / 30 | 0x3fe2a4 |
| `0x3fce38` | traduit/vérifié | `The Mirror Move failed!` → `Mirror Move falhou!` | 24 / 20 | 0x3fe2a8 |
| `0x3fce50` | traduit/vérifié | `It started to rain!` → `Começou a chover!` | 20 / 18 | 0x3fe2ac |
| `0x3fce64` | traduit/vérifié | `A downpour started!` → `Começou um temporal!` | 20 / 21 | 0x3fe2b0 |
| `0x3fce78` | traduit/vérifié | `Rain continues to fall.` → `A chuva continua caindo.` | 24 / 25 | 0x3fe2b4 |
| `0x3fce90` | traduit/vérifié | `The downpour continues.` → `O temporal continua.` | 24 / 21 | 0x3fe2b8 |
| `0x3fcea8` | traduit/vérifié | `The rain stopped.` → `A chuva parou.` | 18 / 15 | 0x3fe2bc |
| `0x3fceba` | traduit/vérifié | `A sandstorm brewed!` → `Começou uma tempestade de areia!` | 20 / 33 | 0x3fe2c0 |
| `0x3fcece` | traduit/vérifié | `The sandstorm rages.` → `A tempestade de areia continua.` | 21 / 32 | 0x3fe2c4 |
| `0x3fcee3` | traduit/vérifié | `The sandstorm subsided.` → `A tempestade de areia passou.` | 24 / 30 | 0x3fe2c8 |
| `0x3fcefb` | traduit/vérifié | `The sunlight got bright!` → `A luz do sol ficou forte!` | 25 / 26 | 0x3fe2cc |
| `0x3fcf14` | traduit/vérifié | `The sunlight is strong.` → `A luz do sol está forte.` | 24 / 25 | 0x3fe2d0 |
| `0x3fcf2c` | traduit/vérifié | `The sunlight faded.` → `A luz do sol enfraqueceu.` | 20 / 26 | 0x3fe2d4 |
| `0x3fcf40` | traduit/vérifié | `It started to hail!` → `Começou a cair granizo!` | 20 / 24 | 0x3fe2d8 |
| `0x3fcf54` | traduit/vérifié | `Hail continues to fall.` → `O granizo continua caindo.` | 24 / 27 | 0x3fe2dc |
| `0x3fcf6c` | traduit/vérifié | `The hail stopped.` → `O granizo parou.` | 18 / 17 | 0x3fe2e0 |
| `0x3fcf7e` | traduit/vérifié | `But it failed to Spit Up\na thing!` → `Mas não conseguiu usar\nSpit Up!` | 34 / 32 | 0x3fe2e4 |
| `0x3fcfa0` | traduit/vérifié | `But it failed to Swallow\na thing!` → `Mas não conseguiu usar\nSwallow!` | 34 / 32 | 0x3fe2e8 |
| `0x3fcfc2` | traduit/vérifié | `The wind turned into a\nHeat Wave!` → `O vento virou uma\nHeat Wave!` | 34 / 29 | 0x3fe2ec |
| `0x3fcfe4` | traduit/vérifié | `All stat changes were\neliminated!` → `Todas as mudanças de stats\nforam anuladas!` | 34 / 43 | 0x3fe2f0 |
| `0x3fcfe5` | exception justifiée | `ll stat changes were\neliminated!` → — | 33 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fcfe4. Le consommateur vise cette cellule complète, pas 0x3fcfe5; écriture autonome interdite. |
| `0x3fd006` | traduit/vérifié | `Coins scattered everywhere!` → `Moedas espalhadas por toda parte!` | 28 / 34 | 0x3fe2f4 |
| `0x3fd022` | traduit/vérifié | `It was too weak to make\na Substitute!` → `Estava fraco demais para\ncriar um substituto!` | 38 / 46 | 0x3fe2f8 |
| `0x3fd048` | traduit/vérifié | `The battlers shared\ntheir pain!` → `Os combatentes dividiram\nsua dor!` | 32 / 34 | 0x3fe2fc |
| `0x3fd068` | traduit/vérifié | `A bell chimed!` → `Um sino tocou!` | 15 / 15 | 0x3fe300 |
| `0x3fd077` | traduit/vérifié | `All affected Pokémon will\nfaint in three turns!` → `Todos os Pokémon afetados\nserão nocauteados em 3 turnos!` | 48 / 57 | 0x3fe304 |
| `0x3fd0a7` | traduit/vérifié | `There's no PP left for\nthis move!<0xFB>` → `Não há mais PP para\neste movimento!<0xFB>` | 35 / 37 | 0x3fe308 |
| `0x3fd0ca` | traduit/vérifié | `But there was no PP left\nfor the move!` → `Mas não havia mais PP\npara o movimento!` | 39 / 40 | 0x3fe30c |
| `0x3fd0f1` | traduit/vérifié | `<0xFD><0x0F> ignored\norders while asleep!` → `<0xFD><0x0F> ignorou\nordens enquanto dormia!` | 32 / 35 | 0x3fe358 |
| `0x3fd111` | traduit/vérifié | `<0xFD><0x0F> ignored\norders!` → `<0xFD><0x0F> ignorou\nas ordens!` | 19 / 22 | 0x3fe35c |
| `0x3fd124` | traduit/vérifié | `<0xFD><0x0F> began to nap!` → `<0xFD><0x0F> foi cochilar!` | 17 / 17 | 0x3fe360 |
| `0x3fd135` | traduit/vérifié | `<0xFD><0x0F> is\nloafing around!` → `<0xFD><0x0F> está\nfazendo corpo mole!` | 22 / 28 | 0x3fe364 |
| `0x3fd14b` | traduit/vérifié | `<0xFD><0x0F> won't\nobey!` → `<0xFD><0x0F> não vai\nobedecer!` | 15 / 21 | 0x3fe368 |
| `0x3fd15a` | traduit/vérifié | `<0xFD><0x0F> turned away!` → `<0xFD><0x0F> virou o rosto!` | 16 / 18 | 0x3fe36c |
| `0x3fd16a` | traduit/vérifié | `<0xFD><0x0F> pretended\nnot to notice!` → `<0xFD><0x0F> fingiu\nnão perceber!` | 28 / 24 | 0x3fe370 |
| `0x3fd186` | traduit/vérifié | `<0xFD><0x1C> <0xFD><0x1D> is\nabout to use <0xFD><0x01>.<0xFB>Will <0xFD><0x23> change\nPokémon?` → `<0xFD><0x1C> <0xFD><0x1D> vai\nusar <0xFD><0x01>.<0xFB><0xFD><0x23> vai trocar\nde Pokémon?` | 50 / 45 | 0x3fe374 |
| `0x3fd1b8` | traduit/vérifié | `<0xFD><0x0F> learned\n<0xFD><0x00>!` → `<0xFD><0x0F> aprendeu\n<0xFD><0x00>!` | 15 / 16 | 0x3fdf64 |
| `0x3fd1c7` | traduit/vérifié | `You defeated\n<0xFD><0x1C> <0xFD><0x1D>!<0xFB>` → `Você venceu\n<0xFD><0x1C> <0xFD><0x1D>!<0xFB>` | 21 / 20 | 0xd776c, 0x3fe410, 0x9be104 |
| `0x3fd1df` | traduit/vérifié | `<0xFD><0x23> threw a ROCK\nat the <0xFD><0x06>!` → `<0xFD><0x23> jogou uma PEDRA\nem <0xFD><0x06>!` | 27 / 26 | 0x3fe378 |
| `0x3fd1fa` | traduit/vérifié | `<0xFD><0x23> threw some Bait\nat the <0xFD><0x06>!` → `<0xFD><0x23> jogou isca\npara <0xFD><0x06>!` | 30 / 23 | 0x3fe37c |
| `0x3fd218` | traduit/vérifié | `<0xFD><0x06> is watching\ncarefully!` → `<0xFD><0x06> observa\ncom atenção!` | 26 / 24 | 0x3fe380 |
| `0x3fd232` | traduit/vérifié | `<0xFD><0x06> is angry!` → `<0xFD><0x06> está com raiva!` | 13 / 19 | 0x3fe384 |
| `0x3fd23f` | traduit/vérifié | `<0xFD><0x06> is eating!` → `<0xFD><0x06> está comendo!` | 14 / 17 | 0x3fe388 |
| `0x3fd24d` | traduit/vérifié | `<0xFC><0x10><0x42><0x00>Announcer: You're out of\nSafari Balls! Game over!<0xFB>` → `<0xFC><0x10><0x42><0x00> Locutor: Suas Safari Balls\nacabaram! Fim de jogo!<0xFB>` | 55 / 56 | 0x3fe394 |
| `0x3fd284` | exception justifiée | `Wild <0xFD><0x06> appeared!<0xFB>` → — | 19 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0x8bd140 via 0xd7420, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fd297` | traduit/vérifié | `Wild <0xFD><0x06> appeared!<0xFB>` → `Um <0xFD><0x06> selvagem apareceu!<0xFB>` | 19 / 26 | 0xd73f8 |
| `0x3fd2aa` | traduit/vérifié | `Wild <0xFD><0x06> appeared!<0xFC><0x08><0x7F>` → `Um <0xFD><0x06> selvagem apareceu!<0xFC><0x08><0x7F>` | 21 / 28 | 0xd7424 |
| `0x3fd2bf` | traduit/vérifié | `Wild <0xFD><0x06> and\n<0xFD><0x08> appeared!<0xFB>` → `<0xFD><0x06> e\n<0xFD><0x08> selvagens apareceram!<0xFB>` | 26 / 31 | 0xd7408 |
| `0x3fd2d9` | traduit/vérifié | `The Ghost appeared!<0xFB>Darn!\nThe Ghost can't be ID'd!<0xFB>` → `O fantasma apareceu!<0xFB>Droga!\nNão dá para identificá-lo!<0xFB>` | 52 / 56 | 0xd73e0 |
| `0x3fd30d` | traduit/vérifié | `The Ghost appeared!<0xFB>` → `O fantasma apareceu!<0xFB>` | 21 / 22 | 0xd73e4 |
| `0x3fd322` | traduit/vérifié | `Silph Scope unveiled the Ghost's\nidentity!` → `Silph Scope revelou a\nidentidade do fantasma!` | 43 / 46 | 0x3fe4fc |
| `0x3fd34d` | traduit/vérifié | `The Ghost was <0xFD><0x06>!<0xFB>\n` → `O fantasma era <0xFD><0x06>!<0xFB>\n` | 20 / 21 | 0x3fe500 |
| `0x3fd361` | exception justifiée | `k!<0xFB>\n` → — | 5 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fd34d. Le consommateur vise cette cellule complète, pas 0x3fd361; écriture autonome interdite. |
| `0x3fd366` | exception justifiée | `<0xFD><0x1C> <0xFD><0x1D>\nwould like to battle!<0xFB>` → — | 29 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0x8854b0 via 0xd73c0, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fd383` | traduit/vérifié | `<0xFD><0x20>\nwants to battle!` → `<0xFD><0x20>\nquer batalhar!` | 20 / 18 | 0xd73bc |
| `0x3fd397` | traduit/vérifié | `<0xFD><0x20> and <0xFD><0x21>\nwant to battle!` → `<0xFD><0x20> e <0xFD><0x21>\nquerem batalhar!` | 26 / 25 | 0xd73a0 |
| `0x3fd3b1` | traduit/vérifié | `<0xFD><0x1C> <0xFD><0x1D> sent\nout <0xFD><0x06>!<0xFC><0x08><0x3C>` → `<0xFD><0x1C> <0xFD><0x1D> mandou\n<0xFD><0x06>!<0xFC><0x08><0x3C>` | 22 / 20 | 0xd74c4 |
| `0x3fd3c7` | traduit/vérifié | `<0xFD><0x1C> <0xFD><0x1D> sent\nout <0xFD><0x06> and <0xFD><0x08>!<0xFC><0x08><0x3C>` → `<0xFD><0x1C> <0xFD><0x1D> mandou\n<0xFD><0x06> e <0xFD><0x08>!<0xFC><0x08><0x3C>` | 29 / 25 | 0xd7498 |
| `0x3fd3e4` | traduit/vérifié | `<0xFD><0x1C> <0xFD><0x1D> sent\nout <0xFD><0x00>!` → `<0xFD><0x1C> <0xFD><0x1D> mandou\n<0xFD><0x00>!` | 19 / 17 | 0xd75ec, 0x9be0c8 |
| `0x3fd3f7` | traduit/vérifié | `<0xFD><0x20> sent out\n<0xFD><0x06>!` → `<0xFD><0x20> mandou\n<0xFD><0x06>!` | 16 / 14 | 0xd74c0, 0x9bde24 |
| `0x3fd407` | traduit/vérifié | `<0xFD><0x20> sent out\n<0xFD><0x06> and <0xFD><0x08>!` → `<0xFD><0x20> mandou\n<0xFD><0x06> e <0xFD><0x08>!` | 23 / 19 | 0xd749c, 0x9bde20 |
| `0x3fd41e` | traduit/vérifié | `<0xFD><0x20> sent out <0xFD><0x0A>!\n<0xFD><0x21> sent out <0xFD><0x0C>!` → `<0xFD><0x20> mandou <0xFD><0x0A>!\n<0xFD><0x21> mandou <0xFD><0x0C>!` | 32 / 28 | 0xd7484, 0x9be124 |
| `0x3fd43e` | traduit/vérifié | `<0xFD><0x20> sent out\n<0xFD><0x00>!` → `<0xFD><0x20> mandou\n<0xFD><0x00>!` | 16 / 14 | 0xd75e8, 0x9be0cc |
| `0x3fd44e` | traduit/vérifié | `<0xFD><0x22> sent out\n<0xFD><0x00>!` → `<0xFD><0x22> mandou\n<0xFD><0x00>!` | 16 / 14 | 0xd75cc, 0x9be138 |
| `0x3fd45e` | traduit/vérifié | `Go! <0xFD><0x05>!` → `Vai, <0xFD><0x05>!` | 8 / 9 | 0xd7464, 0x9bde18 |
| `0x3fd466` | traduit/vérifié | `Go! <0xFD><0x05> and\n<0xFD><0x07>!` → `Vão, <0xFD><0x05> e\n<0xFD><0x07>!` | 15 / 14 | 0xd7458, 0x9bde10 |
| `0x3fd475` | traduit/vérifié | `Go! <0xFD><0x00>!` → `Vai, <0xFD><0x00>!` | 8 / 9 | 0xd758c, 0x9be130 |
| `0x3fd47d` | traduit/vérifié | `Do it! <0xFD><0x00>!` → `Vamos, <0xFD><0x00>!` | 11 / 11 | 0xd7598, 0x9be134 |
| `0x3fd488` | traduit/vérifié | `Go for it, <0xFD><0x00>!` → `Vai com tudo, <0xFD><0x00>!` | 15 / 18 | 0xd75ac, 0x9be0b8 |
| `0x3fd497` | traduit/vérifié | `Your foe's weak!\nGet 'em, <0xFD><0x00>!` → `O inimigo está fraco!\nVai, <0xFD><0x00>!` | 30 / 31 | 0xd75a8 |
| `0x3fd4b5` | traduit/vérifié | `<0xFD><0x1F> sent out <0xFD><0x0B>!\nGo! <0xFD><0x09>!` → `<0xFD><0x1F> mandou <0xFD><0x0B>!\nVai, <0xFD><0x09>!` | 24 / 23 | 0xd745c, 0x9be120 |
| `0x3fd4cd` | traduit/vérifié | `<0xFD><0x00>, that's enough!\nCome back!` → `<0xFD><0x00>, já chega!\nVolte!` | 30 / 21 | 0xd74ec, 0x9be128 |
| `0x3fd4eb` | traduit/vérifié | `<0xFD><0x00>, come back!` → `<0xFD><0x00>, volte!` | 15 / 11 | 0xd7508, 0x9be12c |
| `0x3fd4fa` | traduit/vérifié | `<0xFD><0x00>, OK!\nCome back!` → `<0xFD><0x00>, OK!\nVolte!` | 19 / 15 | 0xd751c, 0x9bddac |
| `0x3fd50d` | traduit/vérifié | `<0xFD><0x00>, good!\nCome back!` → `<0xFD><0x00>, muito bem!\nVolte!` | 21 / 22 | 0xd7518 |
| `0x3fd522` | traduit/vérifié | `<0xFD><0x1C> <0xFD><0x1D>\nwithdrew <0xFD><0x00>!` → `<0xFD><0x1C> <0xFD><0x1D>\nrecolheu <0xFD><0x00>!` | 19 / 19 | 0xd7554, 0x9be0a4 |
| `0x3fd535` | traduit/vérifié | `<0xFD><0x20> withdrew\n<0xFD><0x00>!` → `<0xFD><0x20> recolheu\n<0xFD><0x00>!` | 16 / 16 | 0xd7548 |
| `0x3fd545` | traduit/vérifié | `<0xFD><0x22> withdrew\n<0xFD><0x00>!` → `<0xFD><0x22> recolheu\n<0xFD><0x00>!` | 16 / 16 | 0xd754c, 0x9be098 |
| `0x3fd555` | exception justifiée | `Wild ` → — | 6 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4c636 via 0xd7ca0, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fd55b` | exception justifiée | `Foe ` → — | 5 / — | Ancienne chaîne sans référent absolu. Son consommateur charge désormais 0xa4c61a via 0xd7ca4, hors PT-10 ; ne pas traduire cette copie morte. |
| `0x3fd560` | traduit/vérifié | `Foe` → `Inimigo` | 4 / 8 | 0xd8360 |
| `0x3fd561` | exception justifiée | `oe` → — | 3 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fd560. Le consommateur vise cette cellule complète, pas 0x3fd561; écriture autonome interdite. |
| `0x3fd564` | traduit/vérifié | `Ally` → `Aliado` | 5 / 7 | 0xd8364, 0x9bda34 |
| `0x3fd569` | traduit/vérifié | `Foe` → `Inimigo` | 4 / 8 | 0xd8338 |
| `0x3fd56d` | traduit/vérifié | `Ally` → `Aliado` | 5 / 7 | 0xd833c, 0x9bda40 |
| `0x3fd572` | traduit/vérifié | `Foe` → `Inimigo` | 4 / 8 | 0xd83d8 |
| `0x3fd576` | traduit/vérifié | `Ally` → `Aliado` | 5 / 7 | 0xd83dc, 0x9bda48 |
| `0x3fd57b` | traduit/vérifié | `<0xFD><0x0F> used\n<0xFD><0x01>` → `<0xFD><0x0F> usou\n<0xFD><0x01>` | 11 / 11 | 0xd7650, 0x9be13c |
| `0x3fd586` | traduit/vérifié | `!` → `!` | 2 / 2 | 0xd8784 |
| `0x3fd588` | traduit/vérifié | `!` → `!` | 2 / 2 | 0xd878c |
| `0x3fd58a` | traduit/vérifié | `!` → `!` | 2 / 2 | 0xd8794 |
| `0x3fd58c` | traduit/vérifié | `!` → `!` | 2 / 2 | 0xd87a4 |
| `0x3fd58e` | traduit/vérifié | `!` → `!` | 2 / 2 | 0xd87b8 |
| `0x3fd590` | traduit/vérifié | `HP` → `PS` | 3 / 3 | 0x3fd5d0, 0x1fb233c |
| `0x3fd593` | traduit/vérifié | `Attack` → `Ataque` | 7 / 7 | 0x3fd5d4, 0x1fb2340 |
| `0x3fd59a` | traduit/vérifié | `Defense` → `Defesa` | 8 / 7 | 0x3fd5d8, 0x1fb2344 |
| `0x3fd5a2` | traduit/vérifié | `Speed` → `Velocidade` | 6 / 11 | 0x3fd5dc, 0x3fe808, 0x1fb2350 |
| `0x3fd5a8` | traduit/vérifié | `Sp. Atk` → `Sp. Atk` | 8 / 8 | 0x3fd5e0, 0x1fb2348 |
| `0x3fd5b0` | traduit/vérifié | `Sp. Def` → `Sp. Def` | 8 / 8 | 0x3fd5e4, 0x1fb234c |
| `0x3fd5b8` | traduit/vérifié | `accuracy` → `Precisão` | 9 / 9 | 0x3fd5e8 |
| `0x3fd5c1` | traduit/vérifié | `evasiveness` → `Evasão` | 12 / 7 | 0x3fd5ec |
| `0x3fd5ff` | traduit/vérifié | `was too dry!` → `estava seco demais!` | 13 / 20 | 0x3fd640 |
| `0x3fd60c` | traduit/vérifié | `was too sweet!` → `estava doce demais!` | 15 / 20 | 0x3fd644 |
| `0x3fd61b` | traduit/vérifié | `was too bitter!` → `estava amargo demais!` | 16 / 22 | 0x3fd648 |
| `0x3fd62b` | traduit/vérifié | `was too sour!` → `estava azedo demais!` | 14 / 21 | 0x3fd64c |
| `0x3fd650` | traduit/vérifié | `<0xFD><0x23> used\n<0xFD><0x16>!` → `<0xFD><0x23> usou\n<0xFD><0x16>!` | 12 / 12 | 0x3fe310 |
| `0x3fd65c` | traduit/vérifié | `The old man used\n<0xFD><0x16>!` → `O senhor usou\n<0xFD><0x16>!` | 21 / 18 | 0x3fe314 |
| `0x3fd671` | traduit/vérifié | `The Poké Dude used\n<0xFD><0x16>!` → `O Poké Dude usou\n<0xFD><0x16>!` | 23 / 21 | 0x3fe4d8 |
| `0x3fd688` | traduit/vérifié | `<0xFD><0x1C> <0xFD><0x1D>\nused <0xFD><0x16>!` → `<0xFD><0x1C> <0xFD><0x1D>\nusou <0xFD><0x16>!` | 15 / 15 | 0x3fe468 |
| `0x3fd697` | traduit/vérifié | `The Trainer blocked the Ball!` → `O Treinador bloqueou a Poké Ball!` | 30 / 34 | 0x3fe318 |
| `0x3fd6b5` | traduit/vérifié | `Don't be a thief!` → `Não roube!` | 18 / 11 | 0x3fe31c |
| `0x3fd6c7` | traduit/vérifié | `It dodged the thrown Ball!\nThis Pokémon can't be caught!` → `Desviou da Poké Ball!\nEste Pokémon não é capturável!` | 57 / 53 | 0x3fe320 |
| `0x3fd700` | traduit/vérifié | `You missed the Pokémon!` → `Você errou o Pokémon!` | 24 / 22 | 0x3fe324 |
| `0x3fd718` | traduit/vérifié | `Oh, no!\nThe Pokémon broke free!` → `Ah, não!\nO Pokémon escapou!` | 32 / 28 | 0x3fe328 |
| `0x3fd738` | traduit/vérifié | `Aww!\nIt appeared to be caught!` → `Ah!\nParecia estar capturado!` | 31 / 29 | 0x3fe32c |
| `0x3fd757` | traduit/vérifié | `Aargh!\nAlmost had it!` → `Argh!\nQuase pegou!` | 22 / 19 | 0x3fe330 |
| `0x3fd76d` | traduit/vérifié | `Shoot!\nIt was so close, too!` → `Droga!\nFaltou tão pouco!` | 29 / 25 | 0x3fe334 |
| `0x3fd7a2` | traduit/vérifié | `Gotcha!\n<0xFD><0x3A> was caught!<0xFC><0x0A><0xFC><0x0B><0x42><0x01><0xFB>` → `Pegou!\n<0xFD><0x3A> foi capturado!<0xFC><0x0A><0xFC><0x0B><0x42><0x01><0xFB>` | 30 / 32 | 0x3fe338 |
| `0x3fd7c0` | traduit/vérifié | `Gotcha!\n<0xFD><0x3A> was caught!<0xFC><0x0A><0xFC><0x0B><0x42><0x01><0xFC><0x08><0x7F>` → `Pegou!\n<0xFD><0x3A> foi capturado!<0xFC><0x0A><0xFC><0x0B><0x42><0x01><0xFC><0x08><0x7F>` | 32 / 34 | 0x3fe33c |
| `0x3fd7e0` | traduit/vérifié | `Give a nickname to the\ncaptured <0xFD><0x3A>?` → `Dar um apelido ao\n<0xFD><0x3A> capturado?` | 36 / 32 | 0x3fe340 |
| `0x3fd804` | traduit/vérifié | `<0xFD><0x06> was sent to\n<0xFD><0x27> PC.` → `<0xFD><0x06> foi enviado\nao PC de <0xFD><0x27>.` | 22 / 28 | 0x3fe344 |
| `0x3fd81a` | traduit/vérifié | `someone's` → `alguém` | 10 / 7 | 0xd8310, 0x9bda24 |
| `0x3fd824` | traduit/vérifié | `Bill's` → `Bill` | 7 / 5 | 0xd8314 |
| `0x3fd82b` | traduit/vérifié | `<0xFD><0x3A>'s data was\nadded to the Pokédex.<0xFB>` → `Os dados de <0xFD><0x3A> foram\nadicionados à Pokédex.<0xFB>` | 37 / 45 | 0x3fe348 |
| `0x3fd850` | traduit/vérifié | `It is raining.` → `Está chovendo.` | 15 / 15 | 0x3fe34c |
| `0x3fd851` | exception justifiée | `t is raining.` → — | 14 / — | Fragment sans référent absolu, suffixe dans/après la cellule 0x3fd850. Le consommateur vise cette cellule complète, pas 0x3fd851; écriture autonome interdite. |
| `0x3fd85f` | traduit/vérifié | `A sandstorm is raging.` → `Há uma tempestade de areia.` | 23 / 28 | 0x3fe350 |
