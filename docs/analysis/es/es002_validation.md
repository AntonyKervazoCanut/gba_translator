# ES-002 — traitement et validation (F-852)

## Livraison et périmètre

D-849, F-850, B-1030 et B-1032 sont terminés et intégrés. Les 374 offsets
contractuels de `lots.json` sont couverts exactement une fois par
[es002_traitement.json](es002_traitement.json) : 322 traductions, trois imports
communautaires relus, 41 conservations justifiées et huit exclusions.
Les sources EN/ES référence/FR, le glossaire et les autres lots sont préservés.
Les 325 valeurs ES-002 ont leur protection exacte dans le manifeste.

La reprise a détecté la perte des deux fichiers de données ES-002 au rebase :
le commit rejoué avait conservé uniquement le rapport et les tests. Les 325 lignes
et protections ont été restaurées par ajouts ciblés depuis dfba97ca, sans réécrire
le préfixe existant du combined ni les entrées ES-003 intégrées entre-temps.
Les gardes ont reproduit les clés absentes avant restauration.

Les formulations communautaires importées concernent la commode, le réfrigérateur
et les lumières clignotantes. La publicité KFC est remplacée par le sens EN.
Les récompenses du Pokédex et les informations supprimées dans ES sont rétablies.

## Reconstruction et consommateurs

Le rapport détaille pour chaque offset la décision, les octets EN complets,
l’alignement ES, les référents, commandes, traduction et octets de la ROM finale.
Les surfaces sont attribuées aux scripts et tables, sans inventer de zone carte.

- Quatre alias contractuels sont injectés à +1 par B-1030/B-1032 : 1A5AD5,
  1B1D7C, 1BC310 et 1C27E6. Les AA restent intacts. Les faux débuts dont le vrai
  début est déjà dans le lot sont exclus, sans seconde traduction concurrente.
- Les suffixes 1BDF08 et 1C59F7 sont exclus. La description orpheline 23700C
  n’est pas confondue avec la Plaque Herbe vivante à EB396F. L’ancienne offre
  Hawlucha 237503 reste exclue ; le Casino utilise 7EC795 via 7EC45E.
- Les 33 noms proposés et le cri Gyaoo! restent EN. Sept chaînes sans référent
  direct sont conservées sans injection ; leur accessibilité reste à T-914.
- Les textes 1BD966 et 1BDBF8 sont reconstruits jusqu’au FF : 542 et 742 octets
  utiles EN ; les traductions complètes font 501 et 475 octets utiles.
- Les scripts 9B de 1BC59E et 1BC7E2 sont contrôlés aux vrais consommateurs.
- Les cinq classes utilisent la passe existante `trainer_class_names_it` et les
  cellules de 13 octets de gTrainerClassNames, sans déplacer la table.

B-1032 fournit le routage des quatre paginations initialement bloquées et la
préservation des anciens slots après relocation. La certification finale a trouvé
un cinquième message dont le FA disparaissait : 1A561A, consommateur 1BB879.
Sa préimage et ses consommateurs sont ajoutés aux seules données `system_texts`,
avec fixture ROM réelle et garde d’ensemble des cinq routes. Le contrat existant
`preserve_control_flow` est réutilisé, sans changement du moteur partagé.

## Preuves finales

- `make build-es-maint BUILD_NUMBER=0` réussi ; SHA-256 final :
  `26853164e749dd8be03b9b2cf455604e8481fb0eba1cb7a612706bb962eed2ff`.
- Gardes de couverture/commandes/budgets et injection : **759 réussies**.
  Les 374 décisions sont vérifiées, ainsi que les neuf octets voisins auparavant
  écrasés. Aucun fallback, argument perdu ou commande FA/FB supprimée accepté.
- Routage système sur préimages réelles : **13 tests réussis**.
- Comparaison intégrale avec la baseline F-850 (43504c10…33c0) : zéro octet
  hors des sources, consommateurs et cibles vivantes autorisés pour l’union
  ES-002 et ES-003 déjà intégré ; 797 référents inspectés et aucune cible relocalisée
  dans des données occupées (uniquement 00/FF dans la baseline). Ce contrôle porte
  sur cette union ; il ne prétend
  pas attribuer les modifications ES-003 à ES-002. L’ancien audit à neuf écarts
  reste conservé dans `audit_voisinage_preliminaire` à titre historique.
- Playwright headless : **deux tests réussis**, huit surfaces générales et
  quatorze rendus des routes/classes, avec assertions OCR et trois progressions
  FA/FB. Les pointeurs proviennent de la ROM finale ; seuls les scripts de
  déclenchement sont ajoutés aux copies temporaires. Aucune sauvegarde en jeu.
- Captures attachées : 3ec5df21-5751-4dfe-bcc4-403e221ced0c (quatorze rendus),
  et seconde capture des huit surfaces générales jointe au ticket.
- `make test-python` : **5 881 réussis**, trois skips préexistants, 4 088 deselected.
- TypeScript Playwright et Ruff des tests Python réussis.
- Témoin FR reconstruit avec les mêmes sources et BUILD_NUMBER=0 :
  `2c2f602edcbb11e07acad7f078991d22bb742c94388e93b0fd8651259e11c863`.
  La comparaison intégrale avec `/tmp/es002-fr-before.gba` réussit après
  reconstruction FR par les hooks.

## Non vérifié

La sonde emploie l’imprimante native ; elle ne certifie pas tous les parcours
naturels, les buffers maximaux en situation réelle ni le multijoueur à plusieurs
consoles. Les zones carte propriétaires de tous les scripts partagés restent
indéterminées. Ces limites ne sont pas présentées comme des parcours réussis.
La certification globale du jeu appartient à T-914 ; es-maint reste in_progress.
Aucun push, pipeline distant ou package publié.

L’audit ROM global antérieur avait identifié des attentes FR/DE incompatibles
avec les témoins inchangés et une ROM PT absente. Aucun attendu hors périmètre
n’est modifié pour masquer ces écarts. Le journal de la reprise globale est joint
au ticket, séparément des gardes ES-002.
