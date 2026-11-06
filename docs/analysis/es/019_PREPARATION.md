# ES-019 — préparation et blocage d’acheminement

F-869, 6 novembre 2026. **Lot non livré : aucune traduction ni exclusion finale
certifiée.** Projet gba_translator confirmé par A-663 ; D-849 et F-850 terminés
et intégrés. Aucun combined, protection, glossaire ou contrat partagé modifié.

## Relevé exhaustif

`019_PREPARATION.json` conserve les 393 clés exactes et ordonnées de `lots.json` :
385 identiques à EN, 7 différentes et 1 absente ES dans l’inventaire historique.
Chaque clé possède les textes historiques EN/ES/FR, alertes, préimage EN intégrale,
commandes et arguments, occurrences absolues LE32 à tous alignements avec contexte,
références intérieures et correspondances ES issues exclusivement de l’offset map.
Les empreintes sources et des fichiers préservés sont consignées dans ce JSON.

375 clés ont une occurrence directe ; 18 n’en ont pas. 40 préimages contiennent
une référence intérieure. Ces occurrences ne certifient pas un consommateur texte.
Les zones restent à qualifier depuis les scripts, jamais depuis l’adresse.
L’absence de référence directe n’est pas une preuve de texte mort.

Reproduction, avec le lecteur existant sans modification :

```sh
python3 scripts/audit_es016_preparation.py --lot ES-019
python3 scripts/audit_es016_preparation.py --lot ES-019 --probe-routing
python3 -m pytest tests/unit/test_es019_preparation.py -q
```

Les tailles de commandes utilisées sont celles du pipeline actuel ; FA/FB restent
explicites et FE représente une nouvelle ligne. Ce diagnostic ne remplace pas la
qualification de la grammaire de chaque consommateur.

## Blocage reproduit

Six clés commencent par AA sans référence à ce préfixe ; leur début à +1 est
référencé et possède une correspondance ES explicite. Aucun alias ne les couvre.

| Clé contractuelle | Début référencé | Site | Début également contractuel |
|---|---|---|---|
| 0x007CE3D9 | 0x007CE3DA | 0x007763B2 | non |
| 0x007CE573 | 0x007CE574 | 0x00166DB1 | non |
| 0x007D35E9 | 0x007D35EA | 0x007E70BE | non |
| 0x007DE55F | 0x007DE560 | 0x007DE7E0 | oui |
| 0x007E6B88 | 0x007E6B89 | 0x0078198D | oui |
| 0x007E6C2E | 0x007E6C2F | 0x0078098B | non |

`019_ROUTES.json` contient les préimages, contextes et correspondances ES.
`019_ACHEMINEMENT_REPRO.json` fige la sonde négative : sentinelles temporaires aux
quatre clés dont le début est hors liste, vraie conversion
`build_language.generate_translation_json`, quatre absences de l’extraction EN,
zéro ligne CSV ajoutée et zéro entrée JSON, sans erreur. Aucun combined de
production ni ROM sentinelle n’est écrit. Importer maintenant ces quatre clés
donnerait un build vert sans prouver leur injection.

Les deux paires déjà contractuelles exigent une stratégie canonique empêchant une
double injection. AA n’est pas un chiffre espagnol à importer. Le catalogue et
F-1046 ont été consultés : les contrats B-1030/B-1032/F-1035/F-1037/F-1041 et les
prérequis ES-013/014/015/016/017 ne couvrent pas ces clés. Le ticket interdit de
modifier l’infrastructure partagée : un prérequis distinct est nécessaire pour
qualifier ces consommateurs et étendre les contrats opt-in existants.

## Sources à traiter intégralement à la reprise

Quatre préimages dépassent le plafond historique de 512 octets, FF inclus :
7CFD04 = 596, 7D4ABB = 569, 7DDA44 = 520, 7DDC4C = 529. Elles ne sont pas
tronquées dans le relevé ; pagination, fenêtres et acheminement restent à vérifier.
L’entrée absente ES 7E6816 est reconstruite depuis la ROM EN et sa référence :
réception de Snivy, Tepig et Oshawott avec six commandes FC 01 complètes.
Les sept différences communautaires restent à relire linguistiquement.

Les fragments et préimages contenant des scripts (notamment 7D808F, 7DE806,
7E85FC) ne sont ni traduits ni exclus arbitrairement. Identifier leurs lecteurs,
reconstruire les vrais débuts et ne jamais inventer une phrase depuis l’inventaire.

Après le prérequis, reprendre la qualification des zones, les 393 décisions finales,
les traductions/protections exactes et les contrôles de budgets, commandes, buffers,
FA/FB et pointeurs vivants. Valider les surfaces changées par assertions Playwright
headless en émulateur et capture attachée. Cette préparation ne change aucun
affichage et ne revendique aucune preuve visuelle de traduction.
