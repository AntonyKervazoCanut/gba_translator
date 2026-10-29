# Plan de traduction PT-BR

Code retenu : `pt`, locale brésilienne exclusivement. Seed minimal : 0x238d6a → Voltar, protégé au même commit. Aucun travail de masse.

## Charmap et police

Les accents PT-BR sont encodés, dont `ã=0x60`, `õ=0x61`, `Ã=0x62`, `Õ=0x63`
(F-758). Les slots DE 0xF1–0xF6 et contrôles 0xF7–0xFF restent inchangés.
Le patch PT compose les tildes natifs de Ñ/ñ dans les cinq polices latines 2bpp,
via leurs pointeurs vivants, puis copie les largeurs de a/o/A/O. Il ne modifie
pas les blocs LZ77 détectés par l'ancienne heuristique DE, qui donne des faux
positifs graphiques. Détails d'allocation et preuves : `docs/22_POLICE_PT_BR.md`.
B-211 impose toujours font APRÈS repair_lz77 et repair_localized_lz77.

Les abréviations PSN/QMD/CNG/PAR/DRM/DES sont des valeurs de départ à confirmer
avec des sources officielles brésiliennes par le ticket glossaire, sans inventer
de noms à partir du portugais européen.

## Volumétrie et lots

Union des offsets de combined_en et combined_fr ; doublons résolus dernière
occurrence gagnante. Découpage numérique reproductible, sans modifier les sources.
Les domaines sont des plages techniques provisoires : chaque lot doit vérifier
la zone réelle dans le texte EN et les pointeurs avant traduction. Le manifeste
`languages/pt/translation_batches.json` fige la liste exacte des offsets ; aucun
lot ne doit déborder dans celui du voisin.

| Domaine | Entrées uniques | Lots |
|---|---:|---:|
| Tables et interface | 1 | 1 |
| Dialogue historique | 1107 | 4 |
| Menus et systèmes | 4223 | 15 |
| Zones Borrius | 4608 | 16 |
| Combat et descriptions | 3954 | 14 |
| Scénario étendu | 11685 | 39 |

| Lot | Domaine | Entrées | Bornes incluses |
|---|---|---:|---|
| PT-01 | Dialogue historique et entrée isolée | 277 | 0x028780–0x196db7 |
| PT-02 | Dialogue historique | 277 | 0x196df8–0x1bdf08 |
| PT-03 | Dialogue historique | 277 | 0x1bdf94–0x23e7a1 |
| PT-04 | Dialogue historique | 277 | 0x23e7af–0x2f9af8 |
| PT-05 | Menus et systèmes | 281 | 0x353f9e–0x3d987a |
| PT-06 | Menus et systèmes | 282 | 0x3d98dc–0x3e8fb8 |
| PT-07 | Menus et systèmes | 281 | 0x3e8fc8–0x3eaad6 |
| PT-08 | Menus et systèmes | 282 | 0x3eaae2–0x3ec2a6 |
| PT-09 | Menus et systèmes | 281 | 0x3ec2ae–0x3fbea1 |
| PT-10 | Menus et systèmes | 282 | 0x3fbebe–0x3fd85f |
| PT-11 | Menus et systèmes | 281 | 0x3fd876–0x416a1e |
| PT-12 | Menus et systèmes | 282 | 0x416a3a–0x417fcc |
| PT-13 | Menus et systèmes | 281 | 0x417fd0–0x41a1cd |
| PT-14 | Menus et systèmes | 282 | 0x41a1e7–0x41d546 |
| PT-15 | Menus et systèmes | 281 | 0x41d56b–0x446dff |
| PT-16 | Menus et systèmes | 282 | 0x446e63–0x44de55 |
| PT-17 | Menus et systèmes | 281 | 0x44dec7–0x4586d0 |
| PT-18 | Menus et systèmes | 282 | 0x4586f8–0x4841e9 |
| PT-19 | Menus et systèmes | 282 | 0x48422e–0x6c0b90 |
| PT-20 | Zones Borrius | 288 | 0x719a3b–0x754cd4 |
| PT-21 | Zones Borrius | 288 | 0x754f11–0x7735c5 |
| PT-22 | Zones Borrius | 288 | 0x773613–0x78c2fe |
| PT-23 | Zones Borrius | 288 | 0x78c364–0x7a8ca4 |
| PT-24 | Zones Borrius | 288 | 0x7a8d51–0x7bb685 |
| PT-25 | Zones Borrius | 288 | 0x7bb75c–0x7c6c15 |
| PT-26 | Zones Borrius | 288 | 0x7c6c97–0x7d617a |
| PT-27 | Zones Borrius | 288 | 0x7d61ad–0x7eab8a |
| PT-28 | Zones Borrius | 288 | 0x7eac5c–0x7f5158 |
| PT-29 | Zones Borrius | 288 | 0x7f518d–0x876258 |
| PT-30 | Zones Borrius | 288 | 0x876284–0x879590 |
| PT-31 | Zones Borrius | 288 | 0x8795bc–0x87c8c8 |
| PT-32 | Zones Borrius | 288 | 0x87c8f4–0x8bf360 |
| PT-33 | Zones Borrius | 288 | 0x8bf460–0x920284 |
| PT-34 | Zones Borrius | 288 | 0x920285–0x922fa4 |
| PT-35 | Zones Borrius | 288 | 0x922fc6–0x9a436f |
| PT-36 | Combat et descriptions | 282 | 0xa34f4c–0xa369d6 |
| PT-37 | Combat et descriptions | 282 | 0xa369e7–0xa3874a |
| PT-38 | Combat et descriptions | 283 | 0xa3878c–0xa3dfd8 |
| PT-39 | Combat et descriptions | 282 | 0xa3e022–0xa410eb |
| PT-40 | Combat et descriptions | 283 | 0xa410f8–0xa41f4a |
| PT-41 | Combat et descriptions | 282 | 0xa41f57–0xa42da9 |
| PT-42 | Combat et descriptions | 283 | 0xa42db6–0xa43d29 |
| PT-43 | Combat et descriptions | 282 | 0xa43d50–0xa4519d |
| PT-44 | Combat et descriptions | 282 | 0xa451a4–0xa479e4 |
| PT-45 | Combat et descriptions | 283 | 0xa479fa–0xa4ae43 |
| PT-46 | Combat et descriptions | 282 | 0xa4ae61–0xa4d7fc |
| PT-47 | Combat et descriptions | 283 | 0xa4d80a–0xaf36d2 |
| PT-48 | Combat et descriptions | 282 | 0xaf374b–0xeb48e0 |
| PT-49 | Combat et descriptions | 283 | 0xeb4946–0xffd884 |
| PT-50 | Scénario étendu | 299 | 0x1018e38–0x1660251 |
| PT-51 | Scénario étendu | 300 | 0x16602a4–0x166741c |
| PT-52 | Scénario étendu | 299 | 0x1667474–0x166b035 |
| PT-53 | Scénario étendu | 300 | 0x166b040–0x166be16 |
| PT-54 | Scénario étendu | 300 | 0x166be21–0x166cafa |
| PT-55 | Scénario étendu | 299 | 0x166cb05–0x166d7d3 |
| PT-56 | Scénario étendu | 300 | 0x166d7de–0x1904b98 |
| PT-57 | Scénario étendu | 299 | 0x1904ed5–0x1a3791e |
| PT-58 | Scénario étendu | 300 | 0x1a37942–0x1edf771 |
| PT-59 | Scénario étendu | 300 | 0x1edf7a0–0x1eea2d9 |
| PT-60 | Scénario étendu | 299 | 0x1eea2fe–0x1ef096a |
| PT-61 | Scénario étendu | 300 | 0x1ef09b5–0x1ef779a |
| PT-62 | Scénario étendu | 300 | 0x1ef77f7–0x1efe6f7 |
| PT-63 | Scénario étendu | 299 | 0x1efe70a–0x1f052aa |
| PT-64 | Scénario étendu | 300 | 0x1f052dc–0x1f0ca42 |
| PT-65 | Scénario étendu | 299 | 0x1f0ca4b–0x1f130dc |
| PT-66 | Scénario étendu | 300 | 0x1f13208–0x1f1a4df |
| PT-67 | Scénario étendu | 300 | 0x1f1a524–0x1f22f9d |
| PT-68 | Scénario étendu | 299 | 0x1f2300b–0x1f2b4eb |
| PT-69 | Scénario étendu | 300 | 0x1f2b5f0–0x1f317d8 |
| PT-70 | Scénario étendu | 299 | 0x1f317f2–0x1f3ad0f |
| PT-71 | Scénario étendu | 300 | 0x1f3ad8b–0x1f4445a |
| PT-72 | Scénario étendu | 300 | 0x1f44584–0x1f4da8a |
| PT-73 | Scénario étendu | 299 | 0x1f4da97–0x1f55075 |
| PT-74 | Scénario étendu | 300 | 0x1f550b4–0x1f5a5c2 |
| PT-75 | Scénario étendu | 300 | 0x1f5a677–0x1f5ef5e |
| PT-76 | Scénario étendu | 299 | 0x1f5ef99–0x1f649fb |
| PT-77 | Scénario étendu | 300 | 0x1f64a2f–0x1f6adb0 |
| PT-78 | Scénario étendu | 299 | 0x1f6ae93–0x1f716cf |
| PT-79 | Scénario étendu | 300 | 0x1f716ff–0x1f79893 |
| PT-80 | Scénario étendu | 300 | 0x1f7992c–0x1f80127 |
| PT-81 | Scénario étendu | 299 | 0x1f80178–0x1f855f0 |
| PT-82 | Scénario étendu | 300 | 0x1f855ff–0x1f8c6d7 |
| PT-83 | Scénario étendu | 299 | 0x1f8c7c5–0x1f9432d |
| PT-84 | Scénario étendu | 300 | 0x1f9433e–0x1f9869a |
| PT-85 | Scénario étendu | 300 | 0x1f986c0–0x1f9b035 |
| PT-86 | Scénario étendu | 299 | 0x1f9b04d–0x1fa243b |
| PT-87 | Scénario étendu | 300 | 0x1fa2470–0x1fa9941 |
| PT-88 | Scénario étendu | 300 | 0x1fa998a–0x1fd23be |

## Dépendances et acceptation

Infrastructure et glossaire précèdent tous les lots ; les lots sont indépendants.
La certification finale dépend de tous les lots, vérifie la couverture, les tables
fixes, les images, le boot et le gameplay avant de passer status à complete.

Dans chaque ticket : combined édité chirurgicalement, dernière occurrence gagnante,
jamais régénéré/trié/sed global. Toute ligne ajoutée est protégée dans
protected_entries.yaml au même commit. Toute modification partagée exige make
test-python complet, rebuild IT/DE et hash FR inchangé. Commits français
`type(scope): description`. Vérifier le texte réellement injecté, les contrôles,
les budgets et les pointeurs ; une entrée non traduisible doit être justifiée.

L’entrée isolée 0x028780 est rattachée au premier lot du manifeste, qui fait autorité
sur les identifiants définitifs (88 lots ; aucun lot inférieur à 150 entrées).
