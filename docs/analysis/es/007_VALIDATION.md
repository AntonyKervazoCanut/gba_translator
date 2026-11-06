# ES-007 — validation du travail indépendant et reprise F-881

Le lot n'est pas clôturé : les intensificateurs extrêmes d'ES-031 restent un
prérequis réel. Aucun offset de ce lot voisin n'est modifié par ES-007.

## Contenu livré localement

Le rapport `007_TRAITEMENT.json` couvre les 374 clés contractuelles :
332 traductions protégées, neuf noms ou identifiants conservés, quatre buffers
sans texte littéral, dix fragments exclus et dix-neuf préimages conservées faute
de consommateur direct identifié. L'absence de pointeur n'est pas présentée
comme une preuve d'inaccessibilité dynamique.

Les 332 valeurs ont été vérifiées à leurs 364 pointeurs vivants. Les commandes
et arguments complets, l'ordre des FD, FA/FB, les terminateurs, le plafond de
512 octets et les largeurs sont contrôlés. Le faux pointeur audio de FLATTEN
reste intact. Les textes Canto Mortal et Rabia ont été relus selon le guide
Nintendo cité dans `007_PREPARATION.md`.

Les éditions du combined préservent son préfixe historique ; la relecture finale
ne change que 0x3FC0EE, 0x3FC483 et 0x3FC4AB dans le bloc ajouté. Chaque valeur a
sa protection exacte dans le même commit. Aucun code partagé, glossaire,
descripteur de langue, source ES de référence ou source FR n'est modifié.

## Résultats locaux avant intégration

Avec les données de `9d23199d`, Python 3.14 et BUILD_NUMBER=0 :

- `make build-es-maint` : réussi.
- `make test-python` : 9673 réussis, six skips, zéro échec ; 96 sous-tests.
- `pytest tests/e2e/es -m rom -q` : 394 réussis, dix désélectionnés.
- Gardes ciblées de périmètre, contenu et protection : 414 réussies.
- `tsc --noEmit` et Ruff des tests Python : réussis.
- Hooks actifs des commits : 9532 tests rapides réussis, quatre skips, 80 tests
  Vitest réussis et builds FR/IT/DE réussis.
- Playwright headless et mGBA offscreen : un test réussi, 336 états natifs
  (332 textes et quatre compositions statistiques), dix OCR représentatifs,
  sauvegarde source et sauvegarde temporaire inchangées.

Les mots métier sont lus par Vision en espagnol dans la boîte de dialogue.
Les formes très courtes utilisent le mode littéral : sur cette police, Vision
confond parfois ó avec á/ã/ô. Le mot et le codepoint 0x23 restent indépendamment
vérifiés dans la ROM ; aucun remplacement n'est effectué dans les pixels ni
dans les données du jeu pour faciliter l'OCR.

ROM es-maint :
`1a8d814cb3376fb5e268d034ce147c87165b8cf9ceec32c0497518ec143baaa0`.
Témoin FR avant/après sur les mêmes sources et paramètres :
`2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
Le contrôle FR est une preuve de cette opération, pas un verrou permanent sur
les futures corrections françaises autorisées. Les deux ROM sources auditées
restent, elles, des fixtures immuables.

## Profil ROM global non certifié

Les six langues ont été reconstruites localement. Le profil
`make -o materialize-test-roms test-rom` garde ces reconstructions au lieu de les
remplacer par d'anciens BPS. Il a donné 4158 réussis, 51 skips et douze échecs,
tous hors des données ES modifiées : PT-04/22/48/57/69/72 ; rival DE ; gardes
F-601 et dialogues-09 DE ; garde de hash historique FR Corps Gel. Les logs sont
conservés au ticket. Aucun attendu n'est changé pour les masquer ; ni release
globale ni certification de ces corpus n'est revendiquée.

## Reprise obligatoire après F-881 / ES-031

1. Consulter son état et son intégration. Réutiliser F-881 ; ne pas créer de
   doublon pour les deux offsets dont il est déjà propriétaire.
2. Vérifier 0xA4C603 (ID 0x186, hausse extrême) et 0xA4C610 (ID 0x185, baisse
   extrême). La construction ES-007 attend un séparateur initial explicite,
   par exemple `<0x00>muchísimo`, sans espace avant le suffixe `!`.
3. Suivre les vrais pointeurs de la routine CFRU : littéraux 0x9A32EC et
   0x9A32F0, pas la table originale prolongée artificiellement. La preuve et les
   préimages sont dans `007_PREUVE_ASSEMBLAGE_STATS.json`.
4. Valider les phrases complètes à ±1, ±2, ±3 et ±6, y compris les effets
   doublés, les deux propriétaires et le gabarit objet de hausse. Conserver
   l'ordre des FD ; aucun patch moteur n'est nécessaire pour les neuf entrées
   ES-007 déjà adaptées par les seules données.
5. Rebuild ES, contrôles aux pointeurs, tests et Playwright, comparaison FR
   avant/après aux mêmes sources, puis file de commits/pull et vérification
   après rebase avant clôture. Ne jamais pousser ou déclencher une CI distante.

## Non vérifié

Parcours naturels des 332 situations, fenêtres natives Easy Chat/carte,
expansions maximales de tous les buffers et variantes extrêmes avant F-881.
La sonde imprime les textes avec le moteur natif et développe les FD uniquement
sur une copie temporaire ; elle ne prétend pas avoir déclenché tous les combats
et menus naturels. La certification complète demeure réservée à T-914.
