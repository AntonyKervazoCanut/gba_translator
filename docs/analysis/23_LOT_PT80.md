# PT-80 — Tarmigan, Tehl Town et Thundercap Mt.

F-839 couvre exclusivement les 300 clés explicites du manifeste PT-80. Les
prérequis F-758 (glyphes) et F-759 (glossaire) sont intégrés. L'anglais est lu
jusqu'au terminateur ROM, y compris les dialogues de Maxima et du sculpteur
tronqués dans le corpus d'extraction ; le français au même offset est une
référence secondaire. Les noms propres, objets et mouvements non attestés
restent anglais conformément au glossaire.

Le bilan exhaustif, dans l'ordre du manifeste, est
`languages/pt/data/pt80_audit.json` : texte anglais intégral, comparaison FR,
préimage, pointeurs et contexte, traduction, nombre d'octets, largeurs,
classification et justification de chaque offset. 296 consommateurs sont
traduits ou conservés explicitement comme noms. Chaque valeur vivante est
protégée exactement dans `protected_entries.yaml`.

Quatre exceptions n'ajoutent aucune traduction fictive :

| Offset | Justification et pointeur |
| --- | --- |
| `0x1f7cb8c` | Réplique ancienne du Name Rater, aucun pointeur 32 bits dans la ROM source. |
| `0x1f7e03b` | Octet de bourrage sans pointeur ; le nom vivant commence à `0x1f7e03c`, avec cinq références consignées dans l'audit. |
| `0x1f7ecef` | Suffixe interne du dialogue `0x1f7ec6c`, livré via son pointeur `0x1e9657f`. Le seul match autonome est du PCM. |
| `0x1f7ecf1` | Autre suffixe du même dialogue ; deux matches autonomes PCM, aucun lecteur texte. |

Sept coïncidences de pointeur dans les échantillons PCM sont prouvées par leur
en-tête, taille et pointeur d'instrument dans l'audit. Le finaliseur PT-80
restaure ces quatre octets avant de finaliser les seuls lecteurs texte, puis
vérifie les cibles finales. Il réutilise l'allocateur transactionnel partagé,
sans modification du cœur ni des scripts partagés. Les tables de noms de
carte sont traitées par leurs vrais pointeurs, pas déclarées injectées parce
qu'une ligne existe dans le combined.

Les pages FB, défilements FA, couleurs, pauses et tampons gardent exactement
leur séquence anglaise. Les retours FE sont adaptés aux deux lignes du
msgbox ; un défilement ne reçoit qu'une nouvelle ligne. Les missions restent
sur trois lignes de 172 pixels ; descriptions de carte sur quatre lignes.
L'inscription du défi garde trois lignes majuscules de onze caractères au
maximum. Les tests ROM mesurent les cinq polices réelles et réservent dix
W par tampon dynamique, au lieu de se limiter aux estimations de source.

## Vérification reproductible

```sh
make build-pt
python3 -m pytest -q tests/unit/pt/test_batch_pt80.py tests/unit/test_translation_integrity.py
python3 -m pytest -q tests/e2e/pt/test_batch_pt80_rom.py -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt80.config.ts
```

La sonde Playwright démarre mGBA hors écran sur une copie temporaire de la
ROM finale, vérifie les octets via les pointeurs vivants, puis appelle le
véritable msgbox du moteur. L'OCR contrôle le texte portugais de la barrière
et les mouvements requis pour l'énigme. La sauvegarde fixture reste intacte.
Les captures sont produites dans le dossier temporaire de l'OS et jointes au
ticket, jamais versionnées. Cette sonde valide le rendu de ces répliques ;
elle ne revendique pas un parcours manuel complet des zones.
