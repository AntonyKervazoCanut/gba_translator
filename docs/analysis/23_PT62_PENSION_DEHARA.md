# PT-62 — Pension, élevage et Dehara

Le manifeste `languages/pt/translation_batches.json` définit exactement 300 clés.
Le bilan exhaustif, dans le même ordre, est
`languages/pt/data/pt62_audit.json` : anglais, comparaison française, préimage
ROM complète, références, traduction, octets, largeurs et justification.

280 textes sont traduits ; 16 noms, cris ou prix sont conservés conformément à
F-759. Les 296 entrées livrées ont chacune une protection exacte. Les quatre
exceptions ci-dessous ne sont pas ajoutées au combined. Aucune ancienne ligne
ni traduction hors lot n'est supprimée ou modifiée.

## Consommateurs et exceptions

Le périmètre réel comprend la Pension, la reproduction avec Incense, le
transfert de mouvements de Ovo, Dehara et ses commerces, les missions
Pyukumuku et développeurs, et la Double Battle House. Le vocabulaire des
objets, mouvements et lieux sans équivalent figé reste anglais ; les types
Fogo/Terrestre et la terminologie système suivent F-759.

Les 354 références retenues se répartissent entre 266 `msgbox`, 14
`preparemsg`, 31 opérandes `trainerbattle` et 43 champs de tables ou tampons.
Les tables fixes de missions, d'amitié, de choix et de titres musicaux
contiennent des **pointeurs**, pas des cellules texte à élargir. Le finaliseur
dédié `batch_62` réutilise le contrat `BorriusTextPatch` et l'allocateur partagé :
préimages, commandes, budgets, allocation sans chevauchement, repointage des
champs exacts, vérification des octets et du terminateur. Il suit les passes
génériques, y compris les réparations et `repoint_stale`.

| Offset | Exception et preuves |
|---|---|
| `0x1efce1e` | Commentaire « Crim wants this once Aros is rescued », aucun pointeur direct. |
| `0x1efce46` | Brouillon Missingno non branché, aucun pointeur direct. |
| `0x1efcf02` | Réplique préfixée `Win:`, aucun pointeur direct. |
| `0x1efcf91` | Réplique préfixée `Lose:`, aucun pointeur direct. |

Les scripts actifs utilisent notamment `0x1e63d57 → 0x1efcc39`,
`0x1e63db1 → 0x1efcdb7`, puis `0x1e63e36 → 0x1efd04f` (Fuji).
Les tests comparent les préimages et les quatre brouillons inchangés après build.
L'absence de pointeur direct n'est pas assimilée à une preuve générale qu'un
texte est mort : ici elle accompagne le commentaire explicite de développement,
les libellés Win/Lose et les consommateurs voisins identifiés.

`0x1efbe01` est tronqué dans combined EN à 512 caractères. La ROM contient
607 octets, terminateur inclus, jusqu'à `0x1efc05f`. La traduction inclut la
condition finale : vaincre le Ginásio pour obtenir les Go-Goggles. Les contrôles
sont comparés à cette préimage complète et non à l'extrait tronqué.

## Faux pointeur sonore

La recherche brute trouve aussi `0xcbb02d → 0x1efdade`. Ce n'est pas un
consommateur texte : ces quatre octets appartiennent à l'échantillon PCM M4A
`[0xcb92f0, 0xcbe518)`. L'instrument à `0xcd777c` pointe par `0xcd7780` sur
la WaveData `0xcb92e0` ; son en-tête donne 21 032 échantillons.
Le vrai lecteur est l'opérande de `trainerbattle` à `0x1e641c3`.

Le finaliseur exclut cette coïncidence et restaure uniquement ses quatre octets
source si la passe générique les a repointés. Les tests vérifient l'en-tête,
le pointeur d'instrument, les bornes PCM, l'opérande de combat et la réparation
strictement bornée, sans modifier le code partagé.

## Contrôles reproductibles

```sh
python3 -m pytest -q tests/unit/pt/test_batch_pt62.py tests/unit/test_translation_integrity.py
make build-pt
python3 -m pytest -q tests/e2e/pt/test_batch_pt62_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt62.config.ts
```

Les tests vérifient les commandes dans leur ordre, les pages/scrolls, les
missions sur deux ou trois lignes de 172 pixels maximum et les autres textes
sur 208 pixels maximum. Les cinq polices natives sont mesurées avec les tampons
développés : noms de dix glyphes larges, objets de dix-neuf, noms de boîte de
huit, valeurs numériques bornées. Les prix de boissons conservent leurs
commandes de colonne et d'espacement. Les bornes en octets sont garanties par
l'allocation et l'absence de chevauchement, sans troncature.

La preuve Playwright exécute une copie temporaire de la ROM finale dans mGBA
hors écran et déclenche trois `msgbox` aux pointeurs livrés : équipe pleine à
la Pension, refus de jouer avec un Ovo, accueil de la Double Battle House.
Une assertion OCR valide la première page réelle de chaque message avant la
capture jointe au ticket. Aucun glyphe ni texte n'est remplacé dans la sonde ;
aucune sauvegarde en jeu, aucune capture dans le dépôt. Cela ne constitue pas
une navigation complète de toutes les missions et pages, qui reste du ressort
de la certification T-848.
