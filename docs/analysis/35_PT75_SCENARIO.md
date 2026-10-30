# 35 — PT-75 : Redwood, ruines des Regis et routes de Borrius

Le manifeste PT-75 délimite exactement 300 offsets, de `0x1f5a677` à
`0x1f5ef5e`. F-758 et F-759 sont intégrés avant ce lot. Les scènes réelles
comprennent Redwood Village, les inscriptions des Regis, Rift Cave, le tutoriel
de capture de Route 1 et les routes 10 à 16. Le glossaire figé conserve les noms
propres, objets, capacités et talents non attestés en portugais.

## Sources et livraison

`languages/pt/data/pt75_audit.json` constitue le bilan **offset par offset**, dans
l'ordre du manifeste : anglais intégral et référence extraite, comparaison FR,
texte PT, scène, statut, justification, préimage encodée, taille en octets,
largeurs, pointeurs et contexte binaire. Les 296 entrées actives (280 traductions et 16 textes conservés) sont ajoutées
sans suppression ni réécriture des traductions précédentes ; chacune possède
sa protection exacte dans `protected_entries.yaml`.

`batch_75` finalise les consommateurs après les réparations et la police.
Il réutilise le mécanisme de patch existant ; aucun code partagé n'est modifié.
Les noms de carte dont l'offset extrait commence sur un préfixe binaire sont
résolus au véritable début du nom, en préservant ce préfixe. Les tables de
pointeurs conservent leurs cellules ; les chaînes relocalisées sont vérifiées
à travers tous les consommateurs audités. Aucun succès n'est déduit du seul
texte présent dans combined.

Les contrôles non textuels, l'ordre des tampons, les sauts de page et défilements
sont conservés. Les retours de ligne sont adaptés aux polices réelles, avec
192 pixels maximum et dix glyphes larges réservés par tampon. Les inscriptions
braille gardent leurs 4/4/5 lignes, majuscules ASCII, et le budget natif de
14 cellules. La description de Rift Cave conserve quatre lignes.

## Exceptions justifiées

| Offset | Preuve et traitement |
|---|---|
| `0x1f5ae13` | Bourrage sans pointeur exact ; le nom Route 1 commence à `0x1f5ae14`, traité dans le lot. Ses trois lecteurs sont enregistrés dans l'audit. |
| `0x1f5bcfb` | Bourrage sans pointeur exact ; Route 11 commence à `0x1f5bcfc`, traité dans le lot avec ses cinq lecteurs. |
| `0x1f5cfc5` | « Route 13 - 15 » orphelin : aucun pointeur exact ni intérieur détecté. Octets laissés intacts. |
| `0x1f5e5ef` | Suffixe inclus dans le dialogue propriétaire `0x1f5e5e5`, livré via son lecteur `0x1e85530`. Le match exact à `0xcaa4cf` appartient à un échantillon PCM, pas à un lecteur texte ; il reste intact. |

L'audit fournit aussi l'en-tête de chaque échantillon PCM et son pointeur
d'instrument : les faux pointeurs des entrées 230, 258, 284 et 288 ne sont
jamais repointés. Les correspondances intérieures du suffixe ne sont pas des
lecteurs autonomes.

## Vérifications reproductibles

- `make build-pt`
- `python3 -m pytest tests/unit/pt/test_batch_pt75.py tests/e2e/pt/test_batch_pt75_rom.py tests/unit/test_translation_integrity.py -q`
- `npx playwright test -c tests/e2e-playwright/playwright.pt75.config.ts`

Les tests ROM vérifient la préimage EN, les références, les 296 chaînes finales,
l'atomicité, l'idempotence, les écritures bornées, les polices finales et les
zones PCM exclues. Le test Playwright lance mGBA avec Qt hors écran sur une
copie temporaire de la ROM construite. Il invoque deux vrais msgbox aux
pointeurs finaux, compare les octets, reconnaît le texte rendu par OCR et
vérifie que la sauvegarde temporaire reste inchangée. La capture résultante
est stockée hors dépôt puis jointe au ticket.

## Non vérifié

La sonde visuelle couvre deux dialogues ; elle ne certifie pas un parcours
manuel complet des 300 entrées ni la résolution en jeu des trois énigmes.
La certification globale et le parcours PT complet restent du ressort de T-848.
