# PT-08 — lexique Easy Chat

F-767 couvre exactement les 282 offsets du manifeste PT-08, pas toutes les
adresses comprises entre ses bornes. F-758 et F-759 sont intégrés dans la base.

Le domaine réel est le vocabulaire Easy Chat : qualificatifs, actions, vie
quotidienne, loisirs, temps et positions. Ce ne sont pas les commandes du menu
principal. L’anglais a été lu avec la comparaison française au même offset :
`Party` devient ainsi `Festa`, pas « équipe » ; `Skill` désigne `PERÍCIA`, pas
le talent Pokémon `Habilidade`. `FAINTED` suit le glossaire (`NOCAUTEADO`).
Les noms propres ne sont pas concernés. Dix mots restent identiques en portugais : NATURAL, Digital, Item, Popular,
ANIME, GOURMET, SOFTWARE, DESIGN, FESTIVAL et FINAL (270 valeurs modifiées).

## Bilan exhaustif

[languages/pt/data/pt08_audit.json](../../languages/pt/data/pt08_audit.json)
contient une ligne par offset avec anglais, comparaison FR, préimage ROM,
pointeurs, statut, taille encodée et largeurs des deux polices natives.
280 entrées sont localisées ou lexicalement identiques ; deux sont exclues de
l’injection, sans supprimer ni modifier de traduction existante :

- **0x3eb61b** : la ROM EN contient réellement `Ental` (`bfe2e8d5e0ff`),
  référencé par **0x3eb82c**. Source corrompue et sens indéterminé ; `Mental`
  dans la comparaison FR ne constitue pas une preuve. Octets et pointeur conservés.
- **0x3eb621** : `WorldD` (`d1e3e6e0d8beff`) ne possède aucun pointeur vers
  son début. Le pointeur **0x3eb838** vise **0x3eb622**, donc `orldD`, hors
  manifeste PT-08. Une réparation à cet autre offset violerait le périmètre.
  Octets et pointeur conservés. Cette exception reste à examiner lors de T-848.

## Contrat d’injection

Les mots possèdent des références dans des structures Easy Chat de 12 octets
(pointeur, ordre, disponibilité). Les textes sont repointables ; ce ne sont pas
des cellules de texte à stride fixe. Aucun patch de table fixe n’est nécessaire
si le constructeur générique satisfait les assertions sur les 280 pointeurs.
Les huit octets de métadonnées suivant chaque pointeur doivent rester identiques.
L’ordre alphabétique historique reste celui de la ROM ; ce lot ne réordonne pas
les structures du moteur.

Chaque nouvelle ligne combined a sa protection exacte. Aucun mot ne comporte de
placeholder, contrôle, saut de ligne ou saut de page, ni dans les préimages ni
dans les traductions. Les tests contrôlent l’encodage strict, le terminateur et
un budget conservateur de 88 pixels par mot, avec les largeurs réelles des
polices Normal et Short dans la ROM finale. La taille des mots relocalisés est
vérifiée par comparaison intégrale, terminateur compris, via chaque pointeur.

## Validation reproductible

```sh
python3 -m pytest tests/unit/pt/test_batch_08_pt.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_built_batch_08_pt.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt08.config.ts
```

La sonde Playwright lance mGBA hors écran sur une copie temporaire de la ROM
construite. Elle suit le pointeur Easy Chat de `AMANHÃ` et déclenche son rendu
par le moteur de texte, sans réécrire ce mot. Elle vérifie les pixels de chaque
glyphe contre la police native, le tilde compris, et l’absence de débordement.
La capture est produite dans le répertoire temporaire du système, jamais dans
le dépôt. Il s’agit d’une sonde de rendu du mot livré, pas d’une navigation
complète du compositeur Easy Chat ni d’une certification de toutes ses phrases.
