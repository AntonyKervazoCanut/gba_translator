# PT-28 — Dehara, Great Desert, Vivill et base Light of Ruin (F-787)

## Périmètre et prérequis

Les 288 offsets proviennent exclusivement de la liste PT-28 du manifeste.
F-758 (c5b5e0b9) et F-759 (dcc6ce5d) sont intégrés et ancêtres de la base.
Les noms propres, espèces, attaques et objets non officiellement localisés
restent anglais selon le glossaire ; les mots communs sont traduits en PT-BR.

L'anglais identifie Dehara Gym, Dehara Department Store, le casino,
Great Desert, Gurun Town, Vivill Woods, Routes 4 et 14, Vivill Town
et la base Light of Ruin. Le domaine provisoire « Zones Borrius » recouvrait
également des menus de prix, un ascenseur et la séquence du mot de passe.

## Bilan exhaustif et injection

`languages/pt/data/pt28_audit.json` contient les 288 fiches dans l'ordre
exact du manifeste : anglais, comparaison FR, préimage ROM, pointeurs avec
contexte binaire, statut et justification. Les 277 entrées traduites indiquent
la valeur protégée exacte, le budget encodé et les largeurs calculées.
La comparaison FR existe pour 254 offsets ; les 34 absences sont explicites
(valeur nulle) et la traduction repose alors sur l’anglais et la ROM. Les
277 entrées vivantes totalisent 334 références ; le plus long texte encodé
compte 397 octets, terminateur compris.
Les 11 exceptions détaillent chaque offset sans pointeur direct, les vrais
débuts de message et leurs références quand ils existent. Aucun fragment
n'est ajouté artificiellement au combined et aucune traduction existante
n'est supprimée.

La passe finale `batch_28` réutilise `BorriusTextPatch` / `StructuredTextPatch`.
Elle valide préimages, références et commandes, puis relocalise atomiquement
les messages et repointe leurs consommateurs réels. Elle ne modifie pas les
cellules voisines, les tableaux de choix ou les scripts au-delà des quatre
octets de chaque référence. Les deux tables de prix d'objets (références
0x1a7aef et suivantes et 0x7ec376 et suivantes) sont toutes deux mises à jour.
Les noms de prix et les commandes FC 13 (position X) / FC 06 (police)
restent structurés ; seules les devises deviennent « Fichas ».

Les pages FA/FB et commandes FC/FD sont conservées en ordre exact.
Les retours souples sont adaptés à la largeur ; une page initiale comporte
au plus deux lignes, et un scroll FA une seule nouvelle ligne. Les espaces
de cadrage des intertitres Antes/Agora sont encodés explicitement en 00 pour
survivre au chargement du combined. Le panneau 0x7ef622 contient dans la
source le littéral erroné « h7B » : il devient la flèche gauche 7B, cohérente
avec l'autre panneau Route 14, sans changer les destinations.

Le mot de passe conserve les lettres A, K, L, O, V, E, leur ordre et leurs
couleurs. Les récompenses (Lapras, Ditto, cinq Hard Stones / Pearl String),
les coûts du casino et les variantes de genre restent couverts par les tests.

## Vérification reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_pt28.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt28_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt28.config.ts
```

Les tests ROM comparent tous les pointeurs et octets finaux, les cinq polices
vivantes, l'absence de chevauchements, les limites d'écriture, l'idempotence
et l'atomicité en cas de préimage incorrecte. La sonde Playwright démarre
mGBA hors écran sur une copie temporaire, appelle deux msgbox avec les
pointeurs réellement injectés et vérifie leur texte complet par OCR avant
capture. Les textes et glyphes restent ceux de la ROM construite.

## Non vérifié

La sonde n'est pas une navigation complète dans les 277 messages ni une
certification de tous les écrans du casino ou des branches de scénario.
Ces consommateurs sont vérifiés en binaire et en budgets de polices.
Les onze exceptions ne sont pas revendiquées injectées. Le patch BPS distribué
n'est pas actualisé ; la certification complète et la release relèvent de T-848.
Aucun push ni lancement de pipeline distant.
