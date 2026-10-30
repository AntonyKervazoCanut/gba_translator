# PT-71 — Cube Space, Cinder Volcano et Vivill Town

Lot F-830 : seuls les 300 offsets explicites du manifeste PT-71 sont concernés.
Prérequis F-758 et F-759 intégrés. Terminologie : noms propres, organisations,
objets et mouvements sans attestation brésilienne conservés en anglais selon F-759.
Les noms des lieux ne sont pas repris du français.

## Couverture et contrat

294 entrées vivantes sont traduites ou conservées conformément au glossaire
(Aros et le mot de passe `aklov`), chacune avec sa protection exacte.
`languages/pt/data/pt71_audit.json` constitue le bilan exhaustif ordonné : anglais
complet lu en ROM, comparaison française, préimage binaire, références et contexte,
traduction, taille encodée et largeurs. Les quatre répliques longues 0x1f3c04d,
0x1f3d2fd, 0x1f3ef60 et 0x1f41d4c dépassent les 500 octets de l'extraction EN.
Leur traduction utilise la totalité du dialogue source.

Les FC, FD, FA et FB sont conservés octet pour octet et dans le même ordre.
Les FE souples sont replacés pour respecter les deux lignes initiales puis une
ligne par défilement. L'ellipse est le glyphe natif B0. Les noms runtime sont
budgétés à dix glyphes larges, selon la marge PT-68 intégrée au rebase. Les tests ROM mesurent les cinq polices réelles.
Les cellules de nom Aros, les buffers fils/fille et la comparaison `aklov` ont des
pointeurs de script explicites ; aucune table fixe sans pointeur n'est présente.

Le finaliseur `batch_71` réutilise le moteur structuré déjà partagé par les lots PT.
Il vérifie les préimages et commandes, alloue un bloc neuf pour chaque texte qui
n'est pas déjà correct et repointe uniquement les références auditées. Il couvre
les longs dialogues omis ou altérés par les limites du pipeline générique. Les sept faux hits binaires des entrées vivantes sont
restaurés après les passes génériques ; seuls 323 consommateurs texte confirmés
sont repointés. Il est atomique et idempotent ; aucune modification du cœur ou des scripts partagés.

## Exceptions

| Offset | Justification et pointeur |
|---|---|
| 0x1f3e0ea | Fragment intérieur de 0x1f3e057. Faux mot de pointeur à 0x4bdde6 dans des données binaires, pas un consommateur texte. Autre faux hit intérieur vers 0x1f3e0f7 à 0xd9356b. Le dialogue complet est traduit à son vrai pointeur 0x1e599fc. |
| 0x1f3e5f0 | Fragment intérieur de 0x1f3e5b3. Faux mot de pointeur à 0x13598fa dans des données binaires. Le dialogue complet est traduit à son vrai pointeur 0x1e59cc7. |
| 0x1f434e7 | Source explicitement marquée « No longer used ». Aucun pointeur direct ou intérieur. |
| 0x1f434f9 | Carton « Moments Ago » inutilisé : aucun pointeur direct ou intérieur. |
| 0x1f43508 | Ancienne annonce administrateur : aucun pointeur direct ou intérieur. |
| 0x1f4362f | Ancienne consigne des gardes : aucun pointeur direct ou intérieur. |

Les fragments internes partagent le stockage de leurs dialogues parents : le
pipeline générique peut réécrire ces octets devenus sans consommateur. Le test
contrôle leur appartenance au parent, les vrais textes finaux et les faux
pointeurs binaires, sans imposer l’identité physique d’un fragment mort.

Les six clés restent absentes du combined et des protections. Les faux pointeurs
binaires restent intacts. Les adresses et contextes exacts figurent dans l'audit ;
les tests les confrontent à la ROM EN réelle. Aucune traduction existante supprimée.

## Vérification reproductible

- `python3 -m pytest tests/unit/pt/test_batch_pt71.py tests/unit/test_translation_integrity.py -q`
- `make build-pt`
- `python3 -m pytest tests/e2e/pt/test_batch_pt71_rom.py -m rom -q`
- `npx playwright test --config tests/e2e-playwright/playwright.pt71.config.ts`

La sonde Playwright ne simule pas le texte dans une page web : elle déclenche un
msgbox natif dans une copie temporaire de la ROM finale, avec le pointeur vivant
vérifié. OCR des lignes réelles et assertion sur les octets, puis capture hors dépôt.
Elle vérifie Rock Smash et l'ouverture de la porte après le mot de passe. Il ne
s'agit pas d'un parcours intégral de ces chapitres ni d'une certification T-848.
