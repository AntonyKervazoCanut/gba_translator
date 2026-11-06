# PT-86 — Battle Ring et missions des gangs d'Antisis

Le périmètre est la liste explicite des 299 clés de PT-86 dans
`languages/pt/translation_batches.json`, de `0x1f9b04d` à `0x1fa243b`.
Le bilan exhaustif, dans cet ordre, est `languages/pt/data/pt86_audit.json` :
anglais exporté, référence FR au même offset, texte anglais binaire complet,
préimages, pointeurs et contextes, exceptions, PT, octets et largeurs.

295 entrées vivantes sont ajoutées et protégées exactement. Les noms de
mouvements et identifiants d'espèces restent anglais selon F-759. Aucun
combined existant n'est réécrit ; aucune traduction antérieure n'est supprimée.
F-758 et F-759 sont intégrés avant ce travail.

## Domaine réel

- Tuteurs et échanges contre BP au Battle Frontier.
- Antisis Ring Challenge : règles, équipes, types de mouvements interdits,
  records, interruptions et confrontations avec Big Mo.
- Missions de la fillette emportée par le vent et de Willy sur la Route 8.
- Black Emboar, James et installation à Antisis City.
- Missions des chaussettes, du pont, du trafic au port (20h–0h), de la
  scientifique et assaut contre les Black Ferrothorn.

Les dialogues `0x1f9b484`, `0x1f9b689` et `0x1fa0db8` sont tronqués dans
l'export anglais. Leur traduction utilise le texte complet de la ROM jusqu'au
terminateur, sans recopier les erreurs de la référence française : notamment
Stall, les interdictions du Ring Challenge et les objets/noms de Pokémon.

## Injection et budgets

Le finalisateur `languages/pt/patches/batch_86.py` réutilise les classes
existantes et s'exécute après les réparations génériques et la police. Il
vérifie les préimages et réinjecte le texte exact aux lecteurs audités.
Les cellules de classes CFRU à `0x23e676` et `0x23e6aa` sont des pointeurs
vers les noms Black Ferrothorn et Chefe Black Ferrothorn : seuls ces pointeurs
sont finalisés, sans débordement dans les cellules adjacentes.

Les dialogues gardent deux lignes initiales, puis une ligne par défilement.
Les descriptions de missions gardent au plus trois lignes de 172 pixels.
Les contrôles FC/FD/F8 et les sauts FA/FB restent dans l'ordre binaire source.
Les prix des tuteurs conservent leurs positions FC13 et leurs valeurs BP.
Les tests ROM mesurent les textes et les tampons dans les cinq polices réelles.

Les tampons anglais de certaines répliques nécessitent une préparation locale,
limitée aux appels du lot. La logique des routines partagées et les chaînes des autres lots
restent intactes ; les appels modifiés, leurs préimages, leurs allocations et
leur idempotence font partie des tests ROM.

- Big Mo : un appel local prépare `você`, utilisé deux fois par FD04.
- Missions de la scientifique : neuf appels préparent le vocatif neutre
  `colega`, sans déterminant masculin imposé.
- Mère et fillette : deux appels copient le branchement de genre et préparent
  `senhor` ou `senhora`. Le branchement partagé reste identique ; son pointeur
  féminin `0x1ea5f42` est néanmoins finalisé comme lecteur de l’entrée 69
  `0x1f9ca98` du présent lot, conformément au manifeste.
- Les tampons `ele`/`ela` et `cara`/`mana` déjà traduits par les lots antérieurs
  sont réutilisés sans modification.

## Quatre exceptions

| Offset | Justification et pointeur |
| --- | --- |
| `0x1f9cef7` | Suffixe de `0x1f9cedd`. Le motif à `0xa13785` chevauche des instructions Thumb BL/LSLS ; aucun lecteur texte. |
| `0x1f9eff3` | Suffixe de `0x1f9efae`. Le motif à `0x1328f36` est dans le PCM WaveData `0x1328014`, référencé par l'instrument `0x104fcbc`. |
| `0x1f9fff7` | Suffixe de `0x1f9ffdb`. Le motif à `0x1edca8f` chevauche des instructions Thumb BL/LSLS ; aucun lecteur texte. |
| `0x1fa02ea` | Libellé Sailor sans aucune référence 32 bits dans la ROM EN, contrairement aux libellés voisins. Aucun consommateur démontré ; non injecté. |

Ces clés ne sont pas ajoutées au combined. Les trois dialogues parents sont
traduits. Les motifs audio/code sont exclus des lecteurs et restaurés après
le repointage générique ; les préimages et frontières PCM sont documentées
par entrée dans l'audit et contrôlées par les tests.

## Vérification reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_pt86.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt86_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt86.config.ts
```

La sonde Playwright utilise mGBA hors écran et une copie temporaire de ROM.
Elle compare les octets aux pointeurs vivants, appelle de vraies msgbox et
vérifie leur texte par OCR avant capture. Les captures restent dans le dossier
temporaire du système et sont jointes au ticket, jamais au dépôt.

## Non vérifié

La sonde de dialogues ne constitue pas une partie complète : les parcours
naturels de toutes les missions, toutes les branches et tous les états des
menus relèvent aussi de la certification T-848. Aucun code partagé n'est
modifié ; aucun rebuild FR/IT/DE supplémentaire n'est revendiqué au-delà des
contrôles réellement exécutés par les hooks. Aucun push ni pipeline distant.
