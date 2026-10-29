# PT-38 — Descriptions de mouvements

Le manifeste fermé contient 283 offsets (0xa3878c–0xa3dfd8). Tous sont des
textes vivants de la table des descriptions de mouvements 0x99f190 ; aucune
exception, entrée morte ou cellule de nom fixe n'est revendiquée comme traduite.
Les 283 lignes sont ajoutées sans supprimer les traductions précédentes.

`languages/pt/data/pt38_audit.json` fournit le bilan exhaustif dans l'ordre du
manifeste : préimage ROM, anglais décodé, extraction anglaise, comparaison FR,
traduction PT-BR, identifiants de mouvements, adresses de tous les pointeurs,
octets encodés, largeur des lignes, état et justification. La source anglaise
combinée est souvent vide : la préimage anglaise réellement pointée est alors
l'autorité. Les références supplémentaires vivantes sont 35 descriptions des objets CT.
Le motif non aligné `0x1b48719` vers `0xa3babd` appartient à l'échantillon
audio WaveData type 1 `0x1b4696c`, référencé par `0x19eba44` et `0x19ef6ec`.
Il est exclu des écritures et documenté dans `non_text_evidence` ; un test
vérifie la préimage de l'en-tête, l'étendue DPCM et la conservation du bloc.

Les noms sans attestation restent anglais suivant F-759 (Insomnia, Simple,
Levitate, Plus, Minus, Water/Grass/Fire Pledge, Light Screen, Reflect, Plate,
Drive, Grassy Terrain, Eternal Flower). Les six statistiques utilisent le
glossaire, PS compris. « Os Ataques / as Defesas » et « atributos especiais »
permettent de désigner les deux statistiques concernées sans abréviation inventée
quand la fenêtre de quatre lignes l'exige. Nocauteado remplace Desmaiado.
« Ulceração por frio » décrit l'effet anglais frostbite propre au moteur ; cette
traduction descriptive n'est pas présentée comme une nomenclature officielle.

Le français n'est pas repris aveuglément : Rock Climb mentionne l'escalade,
les crocs de glace et Freeze-Dry suivent frostbite, Chatter garantit la
confusion et Ice Burn conserve sa possibilité de brûler.

Le patch PT `batch_38` réutilise `StructuredTextPatch`. Il valide les préimages,
les consommateurs, le nombre exact de retours à la ligne et les commandes avant
toute écriture. Chaque texte est relocalisé dans l'espace libre final et ses
pointeurs sont mis à jour ; aucune table fixe n'est agrandie. La vérification
contrôle les octets finaux, terminateurs et chevauchements. Les descriptions
respectent le cadre de cinq lignes / 122 pixels, avec le nombre de lignes source
conservé pour chaque entrée. Il n'y a ni placeholder ni saut de page dans ce lot.
Aucun code partagé n'est modifié.

## Vérifications reproductibles

Après détection des processus de test :

```sh
python3 -m pytest tests/unit/pt/test_batch_pt38.py tests/unit/test_translation_integrity.py -q
make build-pt
python3 -m pytest tests/e2e/pt/test_batch_pt38_rom.py -m rom -q
npx playwright test --config tests/e2e-playwright/playwright.pt38.config.ts
```

Les tests ROM contrôlent toutes les préimages, la liste complète des références,
les octets réellement livrés, les cinq polices, l'isolation des écritures,
l'atomicité sur préimage invalide et l'idempotence.

Playwright lance mGBA avec `QT_QPA_PLATFORM=offscreen`. Quatre descriptions
représentatives sont lues depuis leurs pointeurs livrés puis raccordées au panneau
CT56 d'une copie temporaire. Le test contrôle le texte en ROM, le dessin de la
dernière ligne, la marge droite et une navigation aller-retour. Les captures
restent dans le répertoire temporaire du système. Cette sonde vérifie un panneau
réel ; elle ne revendique ni parcours naturel des 283 mouvements ni capture de
l'écran résumé à cinq lignes. Les budgets complets de ce dernier sont contrôlés
sur les cinq polices de la ROM finale.
