# F-851 — ES-001

Les 373 clés contractuelles ont une décision individuelle dans
[0851_ES001_TRAITEMENT.json](0851_ES001_TRAITEMENT.json) : 350 traductions
depuis l’anglais reconstruit, sept fragments exclus, une chaîne vide exclue et
quinze préimages conservées sans consommateur textuel identifié. Aucune liste
de lot, source EN/ES référence/FR ou entrée de glossaire n’est modifiée.

## Livraison

Les 350 entrées sont ajoutées à la fin du combined es-maint ; son préfixe
préexistant reste identique octet par octet. Chaque valeur exacte est protégée
dans le même commit. Les dix alias réutilisent B-1030. Les 340 autres préimages
réutilisent le contrat `system_texts` de B-1032 : commandes et arguments,
ordre des buffers, FA/FB, plafond 512, absence de fallback et de troncature.
Aucun changement de code de production ou de comportement par défaut.

Les publicités de la télévision et de l’avis sont remplacées par le scénario
anglais ; le faux début AA voisin n’est pas traduit une deuxième fois. Les
crédits légitimes de l’équipe Unbound sont conservés et traduits. Les noms
propres du hack suivent D-849, dont Maxima, Galavan, Mel et Ruins of Void.

Les ressemblances de pointeurs dans des données ne sont pas toutes des
consommateurs. Les textes concernés restent dans leur budget de préimage ;
le test ROM vérifie explicitement que les sites suspects restent intacts.
Le test rapide interdit aussi qu'une traduction concernée dépasse sa préimage.
Deux occurrences de 0x180300 sont contenues dans des blocs LZ77 valides à
0x16C78DC (818 octets comprimés) et 0x176E300 (892 octets comprimés).

Le test unitaire ES-002 possède désormais son propre contrat figé de cinq
préimages, correspondant exactement à ses slices ROM. Un test supplémentaire
vérifie leur identité avec les données de production, sans interdire
l’extension du contrat par d’autres lots.

## Terminologie complémentaire

Sources Nintendo consultées le 29 octobre 2026, génération IV, localisation
espagnole de Pokémon Platine ; seuls les noms sont repris, pas les descriptions
ou valeurs d’effets des objets :

- [Objets clés](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/objetos_clave.html) :
  Caña Vieja, Caña Buena, Supercaña, Monedero, Buscapelea.
- [Objets de soin](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/objetos_medicinas.html) :
  Más PS, Calcio, Zinc, Carburante, Proteína, Hierro.
- [Objets généraux](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/objetos_items.html) :
  Escama Corazón.
- [Objets de combat](https://www.guiasnintendo.com/0_NINTENDO_DS/Pokemon_platino/Pokemon_platino_sp/objetos_batalla.html) :
  Ataque X.

Dowser et Medalla Fall conservent le noyau du nom du hack selon D-849 ; ce ne
sont pas des appellations officielles revendiquées. Les pouces restent des
`pulgadas` : les buffers numériques sont produits par le moteur en pouces ;
changer seulement le nom de l’unité en centimètres serait inexact. Le format
du chronomètre conserve les trois buffers et utilise `min.` et `s`.

À 0x1855E1, l’EN porte littéralement « Pokémon Sun ». L’identité du référent
n’étant pas établie, `Sun` reste inchangé selon D-849 ; aucune identification
comme titre officiel ou personnage n’est revendiquée. Cette exception de nom
propre reste visible pour T-914.

## Vérification reproductible

```sh
python3 -m pytest -q tests/unit/test_es001_contract.py tests/unit/test_es002_routing.py tests/unit/test_translation_integrity.py
make build-es-maint
python3 -m pytest -q tests/e2e/es/test_es001_delivery.py
npx playwright test --config tests/e2e-playwright/es001-delivery.config.ts
make test-python
```

Le test ROM passe par le vrai CSV et le JSON consommé par le builder. Il
contrôle les 350 valeurs complètes à tous leurs sites, les octets AA, les
ressemblances de pointeurs, les plages exactes d’écriture et la passe inline.
La sonde native déclenche les 349 textes de script sur une copie temporaire,
capture chaque première page et vérifie des surfaces représentatives par OCR.
Les trois progressions FA/FB choisies doivent afficher les mots de la suite.
Aucune sauvegarde en jeu.

Un contrôle complémentaire remplace les buffers de noms par dix `W`, les
compteurs et tailles numériques par la borne décimale uint32 et les trois
composantes du chronomètre par cinq chiffres. Les formulations sont bornées
à 192 pixels dans ces cas ; cela ne remplace pas une expansion en jeu réel.

## Non vérifié

La sonde synthétique ne constitue pas un parcours naturel des 349 scènes, ni
une attribution exhaustive des noms de cartes depuis leurs racines de scripts.
Les adresses des consommateurs et leurs contextes binaires sont consignés ;
aucune zone n’est déduite de la seule adresse ROM. Les buffers de la sonde sont
vides ; leur expansion exhaustive en situation réelle n’est pas certifiée.
Le texte de combat 0x28780 est vérifié par ses octets et commandes au référent
0x2874C ; la sonde de dialogues ne certifie pas son déclenchement en combat.

Les quinze préimages conservées n’ont pas de consommateur textuel identifié
après reconstruction et recherche de pointeurs. Cette décision évite une
injection spéculative ; elle ne prouve pas leur inaccessibilité dynamique.
Ces réserves et la certification globale des artefacts distribués restent
visibles pour T-914. Le statut de la langue reste `in_progress`.
