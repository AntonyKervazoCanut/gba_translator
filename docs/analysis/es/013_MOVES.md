# ES-013 — Six descriptions de mouvements, réemploi de F-1042

Les six clés 482874, 4828BD, 4828FF, 482946, 482985 et 4829C9 correspondent
aux IDs 2 à 7 de la table active `99F190 + move_id*4`. Leurs 18 références
exhaustives sont trois cellules par clé : table active et miroirs historiques
`4886E8 + (move_id−1)*4`, `904000 + (move_id−1)*4`. Les racines historiques
ne sont pas des consommateurs moteur actuels ; leurs cellules sont néanmoins
repointées avec la table active, comme pour F-1042, pour ne conserver aucun
ancien pointeur vers ces chaînes vivantes.

Le contrat réutilise exclusivement `SystemTextRoutes`, sans réinserteur ni patch
supplémentaire. Les préimages complètes viennent de la ROM EN propre épinglée,
jamais des exports francisés ou absents. Les six correspondances offset map ES
sont uniques et leurs préimages vérifiées. Les empreintes et les références
figurent dans `013_MOVES.json`.

Les racines E5440/137BC8/9F3B64 et les routines F-1042 sont identiques à la ROM
propre. Les deux surfaces directes impriment en police 2 et 3, dont les largeurs
latines sont les mêmes (table 207300). Le contrat conserve cinq lignes FE,
122 pixels, et 512 octets avec terminateur. Aucun FA/FB, fallback ou rewrap
implicite n'est permis. Le scan exhaustif des pointeurs n'identifie aucune
référence gItems pour ces six clés ; la table des 128 CT/MO ne contient aucun
ID 2 à 7. L'intersection trois lignes du Cube F-1042 ne s'applique donc pas.

Les six guards F-1042 qui figeaient auparavant les cellules actives ES-013
99F198..99F1AC sont remplacés individuellement par les routes. Cela ne change
ni la sélection ES-014 ni ses fenêtres. Les racines et métriques restent gardées.
La fixture isolée ES-014 peut continuer à conserver ces cellules quand ES-013
n'est pas injecté ; son contrôle du manifeste doit reconnaître cette évolution
explicite des seules six cellules.

`tests/unit/test_es013_moves.py` teste la reconstruction du JSON obsolète/incomplet,
la relocation forcée vers les 18 pointeurs, l'égalité de tous les octets hors
allocations/pointeurs, les bornes, les contrôles cachés, les racines et les
correspondances uniques. Les tranches binaires autonomes proviennent de la ROM
propre et incluent les voisins. Les preuves de pipeline complet et d'affichage
natif sont à lire dans le bilan global F-1044 ; ce sous-rapport n'en revendique
pas une exécution indépendante. Aucune traduction de production n'est ajoutée.
