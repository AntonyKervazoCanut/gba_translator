# PT-26 — Lost Tunnel, Thundercap et Ruins of Void

Périmètre fermé : les **288 offsets explicites** de PT-26, sans élargir
l'intervalle. Prérequis F-758 et F-759 intégrés (ascendance Git contrôlée).

## Livraison et bilan par offset

Le bilan exhaustif est `languages/pt/data/pt26_audit.json` : pour chaque offset,
anglais du corpus, comparaison française au même offset, préimage binaire complète,
pointeurs EN à tous alignements avec contexte, décision et justification.
Les 276 consommateurs traduits ont aussi leurs octets encodés et largeurs de ligne.
Les 12 exceptions restent absentes du combined ; aucune traduction préexistante
n'est retirée. Le fichier existant est conservé octet pour octet avant les ajouts.

Domaines réels : Lost Tunnel, capture de Moltres et Zapdos, Thundercap Mountain,
Tarmigan Mansion/Mega Ring, routes et plage, Dehara et Looker, Ruins of Void,
libération de Hoopa et Judgement Zone. Les noms propres, espèces, mouvements
non attestés et objets comme Mega Ring/Prison Bottle restent anglais selon F-759.
Les raccourcis SES et KBT ne sont pas confondus.

| Offset excepté | Preuve / décision |
| --- | --- |
| 0x7c6e34 | Le référent 0xb6d534 pointe un script événement ; opcode 0x0f à 0x7c6e36, pointeur texte 0x7c6e38 vers 0x7c6e51, traduit. Aucune écriture sur le script. |
| 0x7c77bd | Préfixe 0xaa sans pointeur ; texte vivant 0x7c77be traduit. |
| 0x7c7c9b | Préfixe 0xaa sans pointeur ; texte vivant 0x7c7c9c traduit. |
| 0x7c83c5 | Préfixe 0xaa sans pointeur ; texte réel 0x7c83c6, référent 0x7e6ff9, hors manifeste. |
| 0x7c8981 | Queue « a secret! » sans pointeur autonome ; ne pas écrire. |
| 0x7c8aae | Suffixe « ific nightmares » sans pointeur ; consommateur 0x7c89e2 traduit. |
| 0x7c8b61 | Copie sans pointeur ; copie vivante 0x7c8ba6 traduite (référent 0x78c214). |
| 0x7c93e0 | Préfixe 0xaa sans pointeur ; texte réel 0x7c93e1, référent 0x7c8c54, hors manifeste. |
| 0x7ce3d9 | Préfixe 0xaa sans pointeur ; texte vivant 0x7ce3da traduit. |
| 0x7ce573 | Préfixe 0xaa sans pointeur ; texte vivant 0x7ce574 traduit. |
| 0x7cfa6a | Fragment « Hoopa. » sans pointeur ; cri vivant 0x7cfa71 traduit. |
| 0x7d35e9 | Préfixe 0xaa sans pointeur ; texte réel 0x7d35ea, référent 0x7e70be, hors manifeste. |

Les dialogues 0x7c8456, 0x7cfd04 et 0x7d4abb dépassent la fin du texte
consigné dans le corpus anglais : leur fin est traduite depuis la ROM EN complète,
sans reprendre les omissions ou contresens du FR.

## Injection et contrôles reproductibles

`batch_26` est exécuté après les réparations et repointages génériques. Il réutilise
`BorriusTextPatch` et `StructuredTextPatch` sans modifier le code partagé : contrôle
de la préimage, de chaque référence, des commandes et des budgets ; allocation
bornée en espace libre ; repointage de tous les consommateurs ; vérification des
cibles et chevauchements ; sauvegarde `.bak` et application atomique/idempotente.
Aucune table à cellules fixes n'est présente parmi ces 276 consommateurs : les
références de scripts, textes de combat et tampons sont recensées dans l'audit.
Aucune entrée n'est revendiquée injectée sur la seule présence dans le combined.

Les variables FD, couleurs FC01, sauts FA et pages FB sont conservés exactement
en ordre. Seuls les retours souples FE sont rééquilibrés, avec deux lignes par
page et une seule ligne par scroll. Mesures conservatrices des variables (neuf
larges glyphes) ; test supplémentaire des cinq tables de largeur de la ROM finale.

```sh
python3 -m pytest tests/unit/pt/test_batch_pt26.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt26_rom.py -q -m rom
npx playwright test --config tests/e2e-playwright/playwright.pt26.config.ts
```

La preuve Playwright lance mGBA avec Qt `offscreen`, sur copie temporaire de la
ROM et sauvegarde copiée, sans sauvegarder en jeu. Deux vrais pointeurs finaux
(0x7c73cf et 0x7cdec1) alimentent une msgbox native sans réécrire les textes,
polices ou fenêtres. Playwright vérifie les octets, puis le texte complet de ces
deux messages par OCR, avant de capturer la preuve hors dépôt dans le dossier
temporaire de l'OS. Cette sonde ne revendique pas une navigation naturelle dans
les 276 dialogues ni le parcours complet des cinématiques ; toutes les autres
pages sont contrôlées en binaire aux pointeurs vivants.
