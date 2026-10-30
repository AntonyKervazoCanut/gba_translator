# PT-79 — Panneaux, conseils, S.S. Marine, Stat Scanner et Tarmigan

## Périmètre et prérequis

F-838 reprend exclusivement les 300 offsets explicites de PT-79 dans
`languages/pt/translation_batches.json`. F-758 (glyphes) et F-759 (glossaire)
sont intégrés. Les noms sans localisation attestée restent anglais selon le
glossaire, y compris les titres musicaux Tarmigan Town D/N et SS Marine.

299 lignes sont ajoutées chirurgicalement au combined, chacune avec sa protection
exacte. Aucune ligne existante n'est supprimée ou réécrite. Le code partagé et
les autres langues ne sont pas modifiés.

## Bilan individuel et lecteurs

`languages/pt/data/pt79_audit.json` constitue le bilan ordonné des 300 offsets :
source anglaise complète décodée depuis la ROM, références EN/FR du corpus,
préimage binaire, scène, pointeurs, texte PT-BR, commandes, taille encodée,
largeurs et substitutions des tampons dynamiques. Les sources du corpus
tronquées sont complétées par la véritable chaîne ROM, notamment pour les
conseils de capture et le récit de Zeph.

Le patch `languages/pt/patches/batch_79.py` réutilise la transaction partagée
existante pour finaliser les 299 consommateurs textuels audités après le pipeline
générique. Il vérifie la préimage SHA256 et les références avant écriture,
sauvegarde la ROM et conserve les références non textuelles. Les fenêtres fixes
(ascenseur, Continuer/Quitter, aides et catégories du Scanner, catalogue musical)
sont couvertes explicitement : aucune entrée ignorée par le constructeur générique
n'est considérée comme livrée sans contrôle de ses octets au pointeur final.

Les sept aides du Scanner utilisent font0 et un budget de 212 pixels, conforme
à la fenêtre native de 27 tuiles avec retrait de 4 pixels. Les catégories gardent
leur réserve à droite pour le niveau. Les tests vérifient les templates natifs,
les cinq polices réelles et les tampons développés. Les dialogues gardent l'ordre
des contrôles, substitutions et changements de page ; seuls les retours à la ligne
sont adaptés à leur largeur.

## Exception

`0x1f77c91–0x1f77cc5` : message « Only Pokémon from this save file can be
modified. », sans pointeur direct vers aucun octet de cette plage dans la ROM
source. Il reste intact et n'est pas ajouté au combined. Les lecteurs voisins
à `0x1ed2c9c` et `0x1fb6b00` sont consignés dans l'audit ; les tests vérifient
leurs cibles distinctes `0x1f77c71` et `0x1f77cf5`. Cette entrée n'est pas
revendiquée comme traduite ni comme visible.

## Validation reproductible

- `make build-pt`
- `python3 -m pytest tests/unit/pt/test_batch_pt79.py tests/unit/test_translation_integrity.py -q`
- `python3 -m pytest tests/e2e/pt/test_batch_pt79_rom.py -q`
- `npx playwright test -c tests/e2e-playwright/playwright.pt79.config.ts`

La sonde Playwright lance mGBA et Chromium hors écran sur une copie temporaire
de la ROM finale. Elle lit trois pointeurs livrés (panneau Dehara, message de
reproduction du Scanner, tutorat Fire Punch), déclenche une véritable msgbox,
vérifie les deux premières lignes par OCR puis capture les trois rendus.
Les tampons RAM attendus par le tuteur sont initialisés pour cette sonde.
Elle ne modifie aucun texte ROM, glyphe ou template et vérifie que la sauvegarde
reste intacte. La capture est écrite dans le répertoire temporaire du système,
jointe au ticket et absente du dépôt.

Résultats de la reprise F-838 : build PT réussi (299 consommateurs vérifiés,
149 relocalisations), 33 tests ciblés d'intégrité réussis, 4 tests ROM réussis,
3 456 tests unitaires PT réussis et 1 test Playwright réussi sur trois scènes.
Le contrôle TypeScript et le lint Python ciblé passent également.

## Non vérifié

La sonde n'est pas une navigation naturelle dans tous les lieux du jeu. Les
pages suivantes et les autres consommateurs sont contrôlés en binaire et par
mesure des polices, sans prétendre à une capture individuelle des 299 chaînes.
L'absence de pointeur direct de l'exception ne constitue pas une preuve générale
contre tout adressage calculé ; aucun consommateur vivant n'a été identifié.
