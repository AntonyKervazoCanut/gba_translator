# 26 — Lot PT-20 : Borrius, menus historiques et dialogues

Le manifeste `languages/pt/translation_batches.json` fait autorité : 288 offsets,
0x719a3b–0x754cd4. F-758 et F-759 étaient terminés et intégrés avant traduction.

## Couverture

Le bilan détaillé, dans l'ordre du manifeste, est
`languages/pt/data/pt20_audit.json`. Chaque ligne donne la préimage binaire EN,
les sources EN/FR comparées, tous les pointeurs absolus trouvés dans les 32 Mio,
leur contexte, le statut et la justification. Les textes injectés ajoutent la valeur
PT, le nombre d'octets encodés et les largeurs de chaque ligne.

- 169 entrées traduites ou normalisées en représentation explicite des commandes.
- 32 noms propres ou cris conservés suivant F-759.
- 87 exceptions : absence de référence absolue, anciens blocs, suffixes, faux départs
  dans des structures ou scripts. Aucune traduction de ces exceptions n'est revendiquée.
  29 ont une copie binaire identique référencée ailleurs, également indiquée au bilan.

La présence d'une phrase dans le fichier nommé EN ne suffit pas à établir son activité.
Les copies anciennes de l'introduction sont distinguées des trois textes réellement
référencés à 0x71a8d7, 0x71a8e5 et 0x71a92b. Les fragments de dialogues ayant encore
un véritable consommateur msgbox sont traités individuellement et relogés séparément.

## Injection et sécurité

`languages/pt/patches/batch_20.py` utilise l'allocateur et l'injection atomique partagés
`StructuredTextPatch`. Il valide les préimages et chaque référence avant d'allouer un
texte complet, puis ne modifie que ces références et les nouvelles plages. Les tables
de noms de lieux utilisent leurs pointeurs à 0x3f1cxx–0x3f1exx ; aucune cellule voisine
n'est écrasée. Le patch est exécuté après les réparations et repointages génériques.
Les noms propres restent anglais ; KBT Expressway et SES Expressway restent distincts.

0x721340 est une fausse chaîne extraite au milieu de MapConnections Route 3
(0x72132c–0x72134b, en-tête de carte 0x777c00). Elle ne doit jamais être injectée.
0x74037d et 0x745132 sont des destinations de scripts, pas des textes : seuls leurs
vrais dialogues 0x74037f et 0x74513b sont traduits. Les tests vérifient les opcodes
préservés et la connexion sud vers Dresco Town dans la ROM finale.

Chaque ligne ajoutée au combined a une protection exacte dans le même commit.
Le combined existant est préservé octet pour octet avant le bloc ajouté ; aucun offset
hors PT-20 n'est modifié. Les commandes FC/FD et leurs arguments, ainsi que FA/FB,
sont conservés dans le même ordre. Seuls les sauts de ligne souples FE peuvent être
repositionnés pour le budget de rendu. Toutes les lignes dialogue restent dans 192 px,
avec deux lignes au plus avant une attente ou un défilement ; description objet : trois
lignes, 232 px. Les variables sont comptées avec leur réserve de largeur par le moteur.

## Vérification

Les tests unitaires contrôlent le périmètre, les protections exactes, les commandes,
les largeurs, les pages et les faits du récit. Les tests ROM rescannent toutes les
références, vérifient les 201 cibles finales, l'isolation binaire, l'idempotence et le
refus atomique d'une préimage corrompue.

La preuve Playwright hors écran lance mGBA avec une copie temporaire de la ROM PT
finale et une sauvegarde fixture copiée. La sonde exécute une msgbox native pointant
sur deux chaînes réellement livrées (0x7451d0 et 0x75106d), sans remplacer le texte ou
les polices. L'OCR asserte les lignes portugaises rendues ; la capture du test est
stockée dans le répertoire temporaire système et jointe au ticket.

## Non vérifié

La sonde visuelle ne constitue pas une navigation complète de toutes les zones ou
branches de scénario. L'absence de référence absolue est une preuve de scan, pas une
preuve formelle d'inaccessibilité par tout calcul d'adresse possible ; aucune entrée
non référencée n'est annoncée comme traduite. Le parcours complet et la certification
PT restent du ressort de T-848. Aucune ROM distribuée, publication, push ou exécution
de pipeline distant dans ce lot.
