# PT-40 — Noms de capacités conservés selon F-759

Les 283 offsets explicites du manifeste sont des cellules de noms de capacités
de 13 octets, et non des descriptions. Le bilan exhaustif est versionné dans
`languages/pt/data/pt40_audit.json` : offset, identifiant de capacité, cellule
binaire source, comparaison EN/FR, nom attendu, budget et justification.

Le corpus `languages/en/combined_en.txt` est périmé dans cette zone : il contient
des fragments français de descriptions Pokédex ou des valeurs vides. La ROM
anglaise propre, identifiée par SHA256 dans l'audit, contient les noms anglais.
Le pointeur moteur à `0x308A4` désigne `0xA40A10` ; chaque capacité est accessible
par `base + identifiant × 13`. L'audit enregistre aussi tous les matches du
pointeur de base, vérifiés dans la ROM finale. Il ne déduit pas la mort d'une
cellule de l'absence d'un pointeur individuel.

F-758 et F-759 sont intégrés. La politique figée `categories.moves.fallback`
impose `preserve_english`, y compris pour les noms du lot explicitement cités
dans le glossaire (Rock Smash, Dive, Aerial Ace). Les 283 entrées ont donc le
statut `verified_retained`. Aucune entrée morte ou corrompue n'est invoquée,
aucun nom portugais ni abréviation non attestée n'est inventé.

Ni `combined_pt.txt` ni les protections ne changent : aucune ligne de traduction
n'est ajoutée, supprimée ou remplacée. Aucun patch de table fixe n'est nécessaire
pour conserver les cellules anglaises déjà présentes. Le test ROM contrôle les
13 octets de chacune des 283 cellules après `make build-pt`, les pointeurs de
base et les largeurs dans les cinq polices moteur (budget 80 pixels). Le test
unitaire verrouille le manifeste, la comparaison des corpus, l'encodage et le
glossaire ; une future traduction contradictoire fait échouer ce contrat.

Le rendu ne change pas. Une capture Playwright n'est donc pas requise pour ce
lot de conservation ; aucune preuve de parcours en jeu n'est revendiquée.
