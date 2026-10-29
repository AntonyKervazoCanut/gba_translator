# Police PT-BR — audit F-758

## Allocation

`ã=0x60`, `õ=0x61`, `Ã=0x62`, `Õ=0x63`. Aucun alias ne translittère ces
caractères. Python et les deux charmap TypeScript sont synchronisés par Make.

Audit des consommateurs : `src/core/text_codec.py`, `src/text/charmap_data.py`,
`src/core/dialogue_linewrap.py`, `src/core/pokedex.py`, `scripts/sync_charmap.py`, les deux TS et les
patchs de langues. Une table locale obsolète dans les catégories Pokédex IT
attribuait encore 0x60–0x65 aux umlauts : elle importe maintenant la table
partagée. Les umlauts restent en 0xF1–0xF6. Le filtre des descriptions
Pokédex accepte également les quatre nouveaux caractères.

Les occurrences `FC 13 60` et `FC 13 63` dans les traductions sont des paramètres
de contrôle de positionnement, pas des glyphes : aucun remplacement d'octets.
Les indices `0x60` des sprites de types ne sont pas des caractères. Les quelques
préfixes binaires extraits dans combined EN ne prouvent pas un usage imprimable.
Aucune traduction ni protection n'est modifiée dans ce ticket.

## Tables réellement utilisées

Désassemblage des routines Thumb du moteur : le caractère indexe une table
Latin brute 2bpp (décalage de 5 ou 6 bits), distincte des tables japonaises.

| Police | Littéral glyphes | Base EN | Stride | Littéral largeurs | Base largeurs EN |
|---|---|---|---|---|---|
| Small | 0x64C4 | 0x1EAF00 | 32 | 0x64CC | 0x1EEF00 |
| Normal | 0x658C | 0x1F3100 | 64 | 0x6594 | 0x1FB100 |
| 2 | 0x66EC | 0x1FF300 | 64 | 0x66F4 | 0x207300 |
| 4 | 0x6920 | 0x20F618 | 64 | 0x6928 | 0x217618 |
| 5 | 0x6A8C | 0x21F930 | 64 | 0x6A94 | 0x227930 |

Dans les cinq tables EN, les slots 60–63 sont vides : zéro dans les grandes
polices, fond opaque sans encre dans Small. Les corps de A/O/a/o restent intacts.
Les deux rangées du tilde sont copiées depuis Ñ/ñ : octets 2:6 pour Small
majuscule, 0:4 pour les grandes majuscules, 6:10 pour toutes les minuscules.
Les 20 largeurs sont copiées depuis la base, y compris la table Small que le
patch DE historique ne traitait pas.

Le patch résout les pointeurs moteur à chaque application, donc traite les blocs
vivants même après relocalisation. Les tests sur extraits binaires réels déplacent
les cinq tables et vérifient que les copies mortes ne changent pas. Ils vérifient
également l'idempotence et que seuls les 20 glyphes et leurs largeurs changent.

## Pourquoi ne pas recopier le patch DE

L'heuristique LZ77 du patch DE retient six blocs vers 0x3BFBE4 dont les pseudo
lettres A/O sont du bruit. Le bloc 0x40C650 a même O et ñ vides ; son pointeur
0xF44B4 est utilisé par une routine graphique BG. Leur densité ne suffit pas
à en faire des polices de texte. Ils ne sont pas modifiés ici. Les primitives
réutilisables de résolution des tables et composition sont dans
`src/core/font_glyphs.py`, sans copie du patch DE.

## Validation

- `make sync-charmap sync-charmap-check`
- `make test-python` et tests PT sur les cinq extraits binaires réels.
- `make build-pt build-it build-de` ; test `tests/e2e/pt/test_built_font_pt.py` sur
  les pointeurs vivants de la ROM finale après toutes les réparations.
- Build FR avant/après avec les mêmes entrées, comparaison SHA256.
- Playwright hors écran : vraie intro et vraie boîte de dialogue mGBA ; chaîne
  de sonde injectée uniquement dans une copie temporaire, jamais dans combined.

SHA256 FR du rebuild de référence avant extension, identique après extension :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Le contrôle porte sur deux builds locaux avec les mêmes sources et paramètres,
pas sur une comparaison avec une publication antérieure.

Exécution locale F-758 : `make test-python` = 2 199 réussis, 2 ignorés par les
conditions préexistantes (pont émulateur/contenu FD), 832 exclus par marqueurs.
Aucun skip n'est ajouté par F-758. Les tests PT sur la ROM finale passent,
ainsi que TypeScript Playwright et le lint ciblé. La sonde Playwright échoue
sur la ROM EN sans patch (glyphe vide), puis passe sur le build PT final.

Le `make test-rom` supplémentaire matérialise le bundle BPS suivi, sans le
reconstruire : 643 succès, 32 skips préexistants et deux échecs déjà présents
(CT05 FR sur cinq lignes, panneau DE 0x1F7128C encore référencé). CT05 échoue
identiquement avec le codec pré-F-758 ; l'assertion DE lit directement un
pointeur du bundle inchangé. Les correctifs source correspondent à B-659 et
F-605. Aucun bundle ni contenu FR/DE n'est modifié par F-758. Cette limite du
bundle est distincte des builds locaux et de la preuve PT.
