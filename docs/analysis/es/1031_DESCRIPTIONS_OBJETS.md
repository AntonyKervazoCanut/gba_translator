# B-1031 — Descriptions d’objets absentes de l’extraction

## Contrat

`languages/es-maint/item_descriptions.json` fige les préimages EN et les
34 consommateurs des 17 descriptions de ce ticket. Les 13 absences EN sont
reconstruites sans modifier l’extraction, les listes contractuelles ni les
combined. Les quatre entrées déjà présentes reçoivent les mêmes métadonnées.
Le descripteur `item_descriptions` active ce mécanisme uniquement pour es-maint.

Le routage exige une correspondance exacte entre préimage et ROM source, ainsi
que la liste exhaustive des pointeurs (recherche à tous les alignements).
Chaque entrée possède un consommateur gItems validé : base `0x876074`, stride
44, champ description `+0x14`. Les doublons, chevauchements, consommateurs
manquants ou supplémentaires et JSON ambigus sont refusés.

Après la conversion CSV habituelle, `ItemDescriptionRoutes.enrich_json` enrichit
le JSON réellement passé au builder. Il reconstruit le texte avec le décodeur
existant, transmet les octets EN, tous les pointeurs et le budget exact sans
padding. Les identifiants restent inchangés. Aucune nouvelle insertion ni
allocation parallèle : normaliseur et SmartReinserter existants sont réutilisés.
Fallback et troncature sont désactivés pour ces entrées ; une vérification après
les patches contrôle les octets à chacun des consommateurs et les allocations.

La fenêtre gItems est fixe : trois lignes maximum, budget conservateur de
176 pixels par ligne. Les ruptures fournies sont conservées, sans rewrap ni
ajout FA/FB. `preserve_line_count: false` permet de passer d’une source de deux
lignes à une traduction de trois lignes ; les commandes FC/FD/F8/F9/F7, leurs
arguments, FA/FB et l’ordre des buffers restent strictement contrôlés par le
normaliseur commun. Les contrats de layout existants gardent leur comportement
strict par défaut (`preserve_line_count: true`).

B-1030 possède les alias vers des débuts décalés : aucun alias n’est créé ici.
Ses métadonnées restent indépendantes ; les routes de ce ticket ont exactement
le même identifiant contractuel et la même adresse vivante.

## Vérifications reproductibles

- `make build-es-maint` : build de production, sans import du lot provisoire.
- `make test-python` : suite multilingue, dont les gardes nouvelles sur tranches
  réelles dans `tests/unit/fixtures/item_descriptions_es.json`.
- `npx playwright test --config tests/e2e-playwright/item-description-routes.config.ts` :
  construit une ROM sentinelle via le vrai pipeline, vérifie les 34 consommateurs,
  ouvre le Cube natif mGBA hors écran et vérifie les trois lignes par OCR.
  Les substitutions D/O tolérées par l’OCR ne modifient pas les assertions exactes
  des octets. Capture après assertions dans le répertoire temporaire système.
  Aucune sauvegarde en jeu ; la fixture de sauvegarde est copiée.
- La sentinelle et les JSON/CSV de sonde sont temporaires et supprimés après
  construction ; seule la ROM dérivée reste sous `output/roms/` (ignorée par Git).
- Les tests de réinsertion utilisent 17 textes distincts plus longs que leur
  préimage : toutes les allocations et les voisins sont contrôlés. Un autre
  test exerce le vrai sous-processus CSV et le JSON final du driver.
- Contrôle FR avant/après aux mêmes sources et paramètres, builds IT/DE et hooks
  actifs. Les résultats détaillés et la capture sont attachés à B-1031.

## Limites

Aucun texte ES n’est livré, corrigé ni raccourci par ce prérequis. Le commit
provisoire `784b8817`, ses 216 valeurs et leur protection restent à F-853.
Le rendu de la sentinelle prouve le mécanisme et la fenêtre ; il ne certifie
ni les traductions finales ni les 374 entrées du lot.
