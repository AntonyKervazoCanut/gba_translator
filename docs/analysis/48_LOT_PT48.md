# PT-48 — descriptions d’objets et noms de zones

Le manifeste explicite contient 282 offsets. Le domaine réel comprend 137
 descriptions d’objets gItems, 36 noms de zones et 109 faux positifs ou départs
sans consommateur texte. Les prérequis F-758 et F-759 sont intégrés.

Le bilan offset par offset est `languages/pt/data/pt48_audit.json` : anglais du
manifeste, français au même offset, octets de la ROM propre, références entrantes,
statut et justification, texte livré, octets encodés et largeurs. Sa somme source
identifie la ROM examinée. Les 173 lignes ajoutées ont leur protection exacte.
Aucune traduction existante n’est supprimée et aucun autre lot n’est édité.

## Sources réelles et sens

La ROM propre est prioritaire sur les libellés périmés du corpus :
`0xeb23f0–0xeb25be` décrit les objets X, pas des vitamines ; `0xeb23b6`, vide dans
le corpus anglais, contient le remède contre les gelures. `0xb3ff00` est vide
(FF sans pointeur) dans cette ROM, malgré une ancienne description française.
La description `0xeb26cd` contient bien un saut de ligne après « remove ».
Les noms propres complets de lieux, mouvements et objets restent anglais selon
F-759. PS, Ataque, Defesa, Velocidade, Precisão, Habilidade et movimento suivent
le glossaire. Atq. Esp./Def. Esp. sont des abréviations éditoriales de largeur.

## Consommateurs et injection

Les descriptions sont référencées dans gItems à `0x876074`, pas 44, champ +20.
Chaque identifiant d’objet et chaque pointeur sont listés dans l’audit ; les neuf
consommateurs de Natural Gift sont vérifiés. Les noms de zones sont atteints par
les pointeurs nommés explicitement dans la table `0x3f1cxx–0x3f1exx`.
Le patch dédié `batch_48`, en dernière passe PT, réutilise l’injecteur structuré
existant. Il ne modifie aucune cellule fixe gItems ni les voisins des noms : il
alloue si nécessaire puis repointe uniquement les champs audités. Préimages,
commandes et budgets sont validés avant écriture atomique ; application répétée
sans changement. Aucun changement du code partagé.

Les descriptions gardent exactement leurs deux ou trois lignes et le contrôle
F8 02 de la machine de minage. Budget maximal : 192 pixels par ligne. Les tests
ROM mesurent aussi les cinq tables de largeurs réelles après patch police et
vérifient chaque cible vivante et chaque terminateur. Les longueurs encodées sont
consignées par entrée ; la relocation évite de tronquer aux budgets originaux.

## Exceptions

106 entrées n’ont aucun pointeur entrant : motifs binaires sans anglais
exploitable, chaîne vide `0xb3ff00`, ou faux départs `0xb5009f` et `0xb535bc`.
Ces derniers précèdent les noms réellement référencés `0xb500a0` (Gurun Town)
et `0xb535c8` (Fullmoon Island), tous deux traités. Le bilan conserve leurs
préimages et exige leur identité dans la ROM finale, sans injecter de traduction.

Trois entrées ont des pointeurs de ressources graphiques et ne sont pas du texte :
`0xd28cf0`, `0xd28e80`, `0xd29f90` sont des flux LZ77, en-tête 10 et taille
valide. L’audit donne tous les pointeurs, la longueur consommée, la taille
décompressée et son SHA256. Les tests redécompressent ces flux et vérifient
l’identité des octets et pointeurs dans la ROM finale. Aucune exception ne compte
comme traduction livrée.

## Vérification reproductible

- `python3 -m pytest -q tests/unit/pt/test_batch_pt48.py tests/unit/test_translation_integrity.py`
- `make build-pt`
- `python3 -m pytest -q tests/e2e/pt/test_batch_pt48_rom.py -m rom`
- `npx playwright test --config tests/e2e-playwright/playwright.pt48.config.ts`

La preuve Playwright hors écran utilise mGBA et le vrai Cube, avec trois
consommateurs de descriptions : Ability Capsule, X Accuracy et Griseous Orb.
Seule une copie temporaire échange les champs de l’objet sélectionné de la
fixture. Les octets du texte livré sont vérifiés avant lancement, puis l’OCR
vérifie les trois lignes affichées. Aucun texte artificiel n’est dessiné. Les
captures restent dans le répertoire temporaire du système, hors dépôt.

## Non vérifié

Cette recette ciblée ne constitue pas un parcours intégral du jeu ni une
certification de tous les autres lots PT. Les noms de zones sont vérifiés aux
pointeurs et en octets ; leur visite exhaustive relève de T-848.
