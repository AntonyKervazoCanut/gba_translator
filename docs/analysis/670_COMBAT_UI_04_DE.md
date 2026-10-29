# B-670 — Qualification DE de combat_ui-04

Périmètre exclusif : 300 offsets du ticket, sans relance de l’audit global.
149 descriptions effectivement corrigées en ROM et 3 réservées à un patch technique
séparé. Les 152 textes DE protégés couvrent 120 absences, une entrée trop longue
et 31 descriptions G-Max
avec noms d’espèces EN et effets reformulés ; 148 noms déjà traités par le patch
`move_names`, donc aucune traduction ajoutée artificiellement à ces cellules.

La comparaison complète EN/FR/DE, le texte canonique décodé depuis la ROM EN,
les adresses des références et les valeurs attendues sont conservés dans
`combat_ui-04_de.json`. Les valeurs EN extraites sont parfois vides ou des
fragments de Pokédex FR périmés : elles ne remplacent jamais le canon ROM.

## Contrôles et exclusions motivées

- Chaque description est atteinte par un ou plusieurs pointeurs de la table
  `0x99F190` (index CFRU conservés, y compris descriptions G-Max partagées).
- Les 148 noms sont des cellules de 13 octets de la table `0xA40A10` ;
  le pointeur moteur `0x308A4` détermine sa base vivante. L’absence de pointeur
  individuel ne signifie donc pas chaîne morte. Les références supplémentaires
  de capacités de terrain sont conservées dans le relevé JSON.
- Texte uniquement dans `combined_de.txt`, entrées gagnantes relues ; aucune
  modification des patches, du glossaire, des données officielles, de FR ou IT.
- Glossaire figé `official_terminology.yaml` : KP/AP, Angriff, Verteidigung,
  Spezialangriff, Spezialverteidigung, Initiative, types et champs ; Lichtschild,
  Reflektor, Wassersäulen/Pflanzensäulen/Feuersäulen, Schwebe, Plus, Minus,
  Wankelmut conformes. Espèces EN volontairement conservées.
- Toutes les descriptions de ce lot sont sans buffer ni commande multioctet,
  sans `\l`/`\p`. Les `\n` sont des retours de mise en page de descriptions,
  réajustés à cinq lignes et 122 pixels. Aucun dialogue de zone, genre
  Sohn/Tochter ou registre de personnage à modifier ; `dir` de Célébration gardé.
- Pas de fragment mort déclaré à partir du seul corpus texte ; aucune entrée
  omise. Les effets sont ceux décrits par Unbound, même quand la formulation
  diffère des jeux officiels (gaz corrosif, Repli Tactique, etc.).

## Décisions par offset

## Limites d’insertion constatées après build

Les extractions EN ne contiennent pas les 120 nouvelles descriptions : elles passent
par l’étape inline. Le premier build réussissait mais 35 valeurs différaient encore.
31 textes ont été raccourcis au budget natif et un texte a été aligné sur le
rééquilibrage de ses cinq lignes. Trois descriptions ne peuvent passer sans modifier
les patches : les bornes internes 0xA3D33A, 0xA3DE52 et 0xA3E6A3 limitent
respectivement les cellules à 21, 19 et 41 octets. La table des descriptions ne vise aucune de ces bornes ; des occurrences
binaires candidates existent ailleurs (0x472A0E/0x47616A, 0x1B75323,
0xB93AF5) et doivent être qualifiées avant de changer la politique de bornage.
Les débuts des descriptions sont bien vivants via 0x99FB6C, 0x99FBF0 et
0x99FC64.
Les traductions complètes sont conservées et protégées ; ces trois exceptions sont
explicitement contrôlées en anglais en ROM en attendant leur suivi technique,
sans raccourci qui dénaturerait les effets. Aucun patch modifié dans ce lot.

| Offset | Décision | Index CFRU | Références ROM EN | Valeur DE attendue / motif |
|---|---|---|---|---|
| 0xA3C9C6 | corrigé | 603 | `0x99FAFC` | Feuert starke Laser\nmit Prismenkraft ab.\nDer Anwender setzt\nin der nächsten\nRunde aus. — Absence DE |
| 0xA3CA1F | corrigé | 604 | `0x99FB00` | Beißt mit Psycho-\nKraft zu. Zerstört\ndabei Lichtschild\nund Reflektor\ndes Ziels. — Absence DE |
| 0xA3CA7C | corrigé | 605 | `0x99FB04` | Heilt den Status\ndes Ziels. Gelingt\ndies, erhält auch\nder Anwender\nKP zurück. — Absence DE |
| 0xA3CAD9 | corrigé | 606 | `0x99FB08` | Greift mit einem\nwilden Tanz an.\nDer Typ der Attacke\nentspricht dem Typ\ndes Anwenders. — Absence DE |
| 0xA3CB38 | corrigé | 607 | `0x99FB0C` | Trifft mit einem\nGeisterknochen.\nSenkt eventuell\ndie Verteidigung\ndes Gegners. — Absence DE |
| 0xA3CB88 | corrigé | 608 | `0x99FB10` | Legt eine Falle.\nWird der Anwender\nphysisch getroffen,\nexplodiert\ndiese Falle. — Absence DE |
| 0xA3CBE2 | corrigé | 609 | `0x99FB14` | Heilt bis zur Hälfte\nder maximalen KP.\nIm Sandsturm\nwerden mehr\nKP geheilt. — Absence DE |
| 0xA3CC78 | corrigé | 611 | `0x99FB1C` | Sammelt in Runde 1\nLicht und lädt eine\nKlinge damit auf.\nGreift in Runde 2\nmit der Klinge an. — Absence DE |
| 0xA3CCD7 | corrigé | 612 | `0x99FB20` | Singt und erzeugt\ndabei Blasen.\nHeilt Verbrennungen\naller betroffenen\nPokémon. — Absence DE |
| 0xA3CD80 | corrigé | 614 | `0x99FB28` | Tauscht Initiative\nmit der des Ziels. — Absence DE |
| 0xA3CE5A | corrigé | 617 | `0x99FB34` | Die Stärke wird\nverdoppelt, falls\ndie vorige Attacke\nfehlgeschlagen ist. — Absence DE |
| 0xA3CEA3 | corrigé | 618 | `0x99FB38` | Entzieht dem Ziel KP\nin Höhe seines\nAngriffswerts.\nSenkt außerdem\nseinen Angriff. — Absence DE |
| 0xA3CF56 | corrigé | 620 | `0x99FB40` | Rührt das Ziel\nmit Tränen.\nSenkt dessen\nAngriff und\nSpezialangriff. — Absence DE |
| 0xA3CFB3 | corrigé | 621 | `0x99FB44` | Trifft die Kehle\ndes Ziels. Es kann\nzwei Runden lang\nkeine Lärm-Attacken\neinsetzen. — Absence DE |
| 0xA3D06D | corrigé | 623 | `0x99FB4C` | Trifft mit einem\ntropischen Tritt.\nSenkt außerdem den\nAngriff des Ziels. — Absence DE |
| 0xA3D0B9 | corrigé | 624 | `0x99FB50` | Ein starker Blitz\ntrifft das Ziel.\nLässt es eventuell\nzurückschrecken. — Absence DE |
| 0xA3D10E | corrigé | 625 | `0x99FB54` | Elektrofeld für\nfünf Runden. Stärkt\nElektro-Attacken\nund verhindert\nEinschlafen. — Absence DE |
| 0xA3D16C | corrigé | 626 | `0x99FB58` | Grasfeld für\nfünf Runden. Stärkt\nPflanzen-Attacken\nund stellt\nKP wieder her. — Absence DE |
| 0xA3D1C9 | corrigé | 627 | `0x99FB5C` | Nebelfeld für fünf\nRunden. Halbiert\nDrachen-Attacken\nund verhindert\nStatusprobleme. — Absence DE |
| 0xA3D228 | corrigé | 628 | `0x99FB60` | Psychofeld für\nfünf Runden. Stärkt\nPsycho-Attacken\nund blockiert\nPrioritätsattacken. — Absence DE |
| 0xA3D286 | corrigé | 629 | `0x99FB64` | Mit Wassersäulen\nsteigt die Stärke\nund es entsteht\nein großer Sumpf. — Absence DE |
| 0xA3D2D5 | corrigé | 630 | `0x99FB68` | Mit Pflanzensäulen\nsteigt die Stärke\nund es entsteht\nein Flammenmeer. — Absence DE |
| 0xA3D325 | besoin de patch séparé | 631 | `0x99FB6C` | Mit Feuersäulen\nsteigt die Stärke\nund es entsteht\nein Regenbogen. — Borne interne extraite 0xA3D33A, budget artificiel 21 octets ; texte DE protégé mais rejeté en ROM, relocalisation dédiée nécessaire |
| 0xA3D370 | corrigé | 632 | `0x99FB70` | Erzeugt einen Raum,\nin dem langsamere\nPokémon fünf Runden\nlang zuerst\nzum Zug kommen. — Absence DE |
| 0xA3D3CA | corrigé | 633 | `0x99FB74` | Erzeugt einen Raum,\nin dem getragene\nItems fünf Runden\nlang ihre Wirkung\nverlieren. — Absence DE |
| 0xA3D424 | corrigé | 634 | `0x99FB78` | Tauscht für fünf\nRunden Verteidigung\nund Spezial-\nverteidigung aller\nPokémon im Kampf. — Absence DE |
| 0xA3D47D | corrigé | 635 | `0x99FB7C` | Magische\nKraft schützt\nAnwender und\nMitstreiter vor\nStatus-Attacken. — Absence DE |
| 0xA3D4D0 | corrigé | 636 | `0x99FB80` | Schützt den Anwender\nund seine Mitstreiter\nmit einer Matte\nvor schädigenden\nAttacken. — Absence DE |
| 0xA3D530 | corrigé | 637 | `0x99FB84` | Schützt Anwender\nund Mitstreiter vor\nPrioritätsattacken. — Absence DE |
| 0xA3D56D | corrigé | 638 | `0x99FB88` | Schützt Anwender\nund Mitstreiter vor\ngroßflächigen\nAttacken. — Absence DE |
| 0xA3D652 | corrigé | 641 | `0x99FB94` | Ein Rülpser trifft\ndas Ziel. Zuvor muss\nder Anwender eine\ngetragene Beere\ngefressen haben. — Absence DE |
| 0xA3D703 | corrigé | 643 | `0x99FB9C` | Wirft das getragene\nItem auf das Ziel.\nStärke und Wirkung\nder Attacke hängen\nvom Item ab. — Absence DE |
| 0xA3D7C1 | corrigé | 645 | `0x99FBA4` | Mehr Schwerkraft\nfür fünf Runden.\nVerhindert Flug-\nmanöver und hebt\nSchwebe auf. — Absence DE |
| 0xA3D81D | corrigé | 646 | `0x99FBA8` | Teilt Verteidigung\nund Spezial-\nverteidigung mit dem\nZiel und gleicht\ndie Werte an. — Absence DE |
| 0xA3D87A | corrigé | 647 | `0x99FBAC` | Verhindert fünf\nRunden lang, dass\ndas gegnerische Team\nKP wiederherstellt. — Absence DE |
| 0xA3D8C9 | corrigé | 648 | `0x99FBB0` | Verteilt elektrisch\ngeladene Teilchen.\nNormal-Attacken\nwerden dadurch zu\nElektro-Attacken. — Absence DE |
| 0xA3D926 | corrigé | 649 | `0x99FBB4` | Ein Zauberspruch\nverhindert fünf\nRunden lang\nVolltreffer durch\ndie Gegner. — Absence DE |
| 0xA3D983 | corrigé | 650 | `0x99FBB8` | Lässt den Anwender\nmittels Magnetkraft\nfünf Runden lang\nschweben. — Absence DE |
| 0xA3D9CD | corrigé | 651 | `0x99FBBC` | Erhöht Verteidigung\nund Spezial-\nverteidigung von\nMitstreitern mit\nPlus oder Minus. — Absence DE |
| 0xA3DA2C | corrigé | 652 | `0x99FBC0` | Bedeckt das Ziel\nmit Puder, der\nexplodiert, wenn es\neine Feuer-Attacke\neinsetzt. — Absence DE |
| 0xA3DA7E | corrigé | 653 | `0x99FBC4` | Teilt Angriff und\nSpezialangriff mit\ndem Ziel und\ngleicht die\nWerte an. — Absence DE |
| 0xA3DB26 | corrigé | 655 | `0x99FBCC` | Eine Psycho-Welle\nändert die\nFähigkeit\ndes Ziels zu\nWankelmut. — Absence DE |
| 0xA3DBCA | corrigé | 657 | `0x99FBD4` | Lässt das Ziel\nschweben. Es ist\ndrei Runden lang\nleichter zu treffen. — Absence DE |
| 0xA3DC2B | corrigé | 658 | `0x99FBD8` | Lädt das Ziel zum\nzuckersüßen Spuk ein.\nEs erhält zusätzlich\nden Typ Geist. — Absence DE |
| 0xA3DC7C | corrigé | 659 | `0x99FBDC` | Gift senkt bei\nvergifteten Zielen\nAngriff, Spezial-\nangriff und Initiative. — Absence DE |
| 0xA3DCD8 | corrigé | 660 | `0x99FBE0` | Ein Fluch des Waldes\ntrifft das Ziel.\nEs erhält\nzusätzlich den\nTyp Pflanze. — Absence DE |
| 0xA3DD2A | corrigé | 661 | `0x99FBE4` | Lässt den Kopf\nexplodieren und\ntrifft alle ringsum.\nSchadet auch\ndem Anwender. — Absence DE |
| 0xA3DD88 | corrigé | 662 | `0x99FBE8` | Eine Lichtsäule\ntrifft physisch oder\nspeziell, je nach\ndem höheren Wert\ndes Anwenders. — Absence DE |
| 0xA3DDE1 | corrigé | 663 | `0x99FBEC` | Trifft mit elektrisch\ngeladenen Fäusten.\nNormal-Attacken\nwerden dadurch zu\nElektro-Attacken. — Absence DE |
| 0xA3DE3F | besoin de patch séparé | 664 | `0x99FBF0` | Wird das Ziel vor\nseiner Attacke\nelektrisiert,\nerhält seine Attacke\nden Typ Elektro. — Borne interne extraite 0xA3DE52, budget artificiel 19 octets ; texte DE protégé mais rejeté en ROM, relocalisation dédiée nécessaire |
| 0xA3DE9D | corrigé | 665 | `0x99FBF4` | Das Ziel kann keine\nItems nutzen. Sein\nTrainer kann keine\nauf es anwenden. — Absence DE |
| 0xA3DF4D | corrigé | 667 | `0x99FBFC` | Feuert einen starken\nLichtstrahl aus der\nEwigen Blüte ab.\nSchadet auch\ndem Anwender. — Absence DE |
| 0xA3DFA5 | corrigé | 668 | `0x99FC00` | Weniger AP machen\ndiese Attacke\nstärker. — Absence DE |
| 0xA3DFD8 | corrigé | 669 | `0x99FC04` | Hilft dem Ziel,\nseine Attacke direkt\nnach dem Anwender\neinzusetzen. — Absence DE |
| 0xA3E022 | corrigé | 670 | `0x99FC08` | Weist das Ziel an,\nseine letzte Attacke\nerneut einzusetzen. — Absence DE |
| 0xA3E0EA | corrigé | 673 | `0x99FC14` | Richtet Mutter aus,\ntrifft mit Armen\nzweimal. Lässt Ziel\nevtl. zurückschrecken. — Absence DE |
| 0xA3E140 | corrigé | 674 | `0x99FC18` | Nur einsetzbar, wenn\nalle anderen Attacken\nim Kampf bereits\neingesetzt wurden. — Absence DE |
| 0xA3E195 | corrigé | 675 | `0x99FC1C` | Hebt das Ziel\nhoch. Es kann\nnicht angreifen\nund fällt nächste\nRunde zu Boden. — Absence DE |
| 0xA3E1E6 | corrigé | 676 | `0x99FC20` | Das Pokémon\ngratuliert\ndir zum\nbesonderen Tag! — Absence DE |
| 0xA3E219 | corrigé | 677 | `0x99FC24` | Hält mit einem\nMitstreiter Händchen.\nDas macht sie froh. — Absence DE |
| 0xA3E256 | corrigé | 678 | `0x99FC28` | Ein starker Strahl\ntrifft das Ziel.\nDoppelter Schaden\nbei Dynamax-Zielen. — Absence DE |
| 0xA3E2A6 | corrigé | 679 | `0x99FC2C` | Ignoriert Attacken\nund Fähigkeiten,\ndie Attacken\nauf sich lenken. — Absence DE |
| 0xA3E2EE | corrigé | 680 | `0x99FC30` | Beißt sich fest.\nDer Anwender und\ndas Ziel können\nnicht auswechseln. — Absence DE |
| 0xA3E338 | corrigé | 681 | `0x99FC34` | Frisst seine Beere\nund erhöht die\neigene Verteidigung\nstark. — Absence DE |
| 0xA3E37B | corrigé | 682 | `0x99FC38` | Erhöht alle eigenen\nWerte. Verhindert\ndanach Flucht und\nAuswechseln. — Absence DE |
| 0xA3E3C8 | corrigé | 683 | `0x99FC3C` | Klebriger Teer senkt\ndie Initiative und\nmacht das Ziel für\nFeuer anfälliger. — Absence DE |
| 0xA3E416 | corrigé | 684 | `0x99FC40` | Magischer Puder\nändert den Typ\ndes Ziels\nzu Psycho. — Absence DE |
| 0xA3E462 | corrigé | 685 | `0x99FC44` | Greift zweimal an.\nGibt es zwei Ziele,\nwird jedes\neinmal getroffen. — Absence DE |
| 0xA3E4A6 | corrigé | 686 | `0x99FC48` | Alle Pokémon halten\nTeestunde und fressen\nihre getragene Beere. — Absence DE |
| 0xA3E4EF | corrigé | 687 | `0x99FC4C` | Fängt das Ziel.\nVerteidigung und\nSpezialverteidigung\nsinken jede Runde. — Absence DE |
| 0xA3E538 | corrigé | 688 | `0x99FC50` | Doppelte Stärke,\nwenn der Anwender\nvor dem Ziel\nzum Zug kommt. — Absence DE |
| 0xA3E580 | corrigé | 689 | `0x99FC54` | Doppelte Stärke,\nwenn der Anwender\nvor dem Ziel\nzum Zug kommt. — Absence DE |
| 0xA3E5C8 | corrigé | 690 | `0x99FC58` | Tauscht die Effekte\nbeider Seiten\ndes Kampffeldes. — Absence DE |
| 0xA3E600 | corrigé | 691 | `0x99FC5C` | Erhöht alle eigenen\nWerte auf Kosten\neines Teils der KP. — Absence DE |
| 0xA3E63A | corrigé | 692 | `0x99FC60` | Je höher die eigene\nVerteidigung, desto\ngrößer ist\nder Schaden. — Absence DE |
| 0xA3E67A | besoin de patch séparé | 693 | `0x99FC64` | Dekoriert das Ziel.\nErhöht dessen\nAngriff und\nSpezialangriff stark. — Borne interne extraite 0xA3E6A3, budget artificiel 41 octets ; texte DE protégé mais rejeté en ROM, relocalisation dédiée nécessaire |
| 0xA3E6C4 | corrigé | 694 | `0x99FC68` | Greift mit einem\nTrommelschlag an.\nSenkt die Initiative\ndes Ziels. — Absence DE |
| 0xA3E70B | corrigé | 695 | `0x99FC6C` | Hält das Ziel\nvier bis fünf\nRunden lang in\neiner Fangeisenfalle. — Absence DE |
| 0xA3E74D | corrigé | 696 | `0x99FC70` | Schleudert einen\nFeuerball auf\ndas Ziel. Kann es\nauch verbrennen. — Absence DE |
| 0xA3E795 | corrigé | 697 | `0x99FC74` | Wird zum Schwert\nund greift an.\nDoppelter Schaden\nbei Dynamax-Zielen. — Absence DE |
| 0xA3E7DF | corrigé | 698 | `0x99FC78` | Wird zum Schild\nund greift an.\nDoppelter Schaden\nbei Dynamax-Zielen. — Absence DE |
| 0xA3E82A | corrigé | 699 | `0x99FC7C` | Morpeko greift an,\nerhöht Initiative.\nDer Typ hängt\nvon seiner Form ab. — Absence DE |
| 0xA3E876 | corrigé | 700 | `0x99FC80` | Schwingt den Schweif\nund trifft die Gegner.\nSenkt dabei\nihren Angriff. — Absence DE |
| 0xA3E8C4 | corrigé | 701 | `0x99FC84` | Sticht das Ziel\nmit einem\nspitzen Ast. — Absence DE |
| 0xA3E904 | corrigé | 702 | `0x99FC88` | Zupft seine Gitarre.\nErzeugt ein Echo\nund starke\nSchwingungen. — Absence DE |
| 0xA3E94C | corrigé | 703 | `0x99FC8C` | Säure aus sauren\nÄpfeln senkt die\nSpezialverteidigung\ndes Ziels. — Absence DE |
| 0xA3E998 | corrigé | 704 | `0x99FC90` | Lässt einen Apfel\nauf das Ziel fallen.\nSenkt dessen\nVerteidigung. — Absence DE |
| 0xA3E9E4 | corrigé | 705 | `0x99FC94` | Seelenbrechende\nKraft senkt den\nSpezialangriff\ndes Ziels. — Absence DE |
| 0xA3EA30 | corrigé | 706 | `0x99FC98` | Greift mit Dampf an.\nVerwirrt das Ziel\neventuell auch. — Absence DE |
| 0xA3EA7B | corrigé | 707 | `0x99FC9C` | Versprüht Wasser.\nHeilt eigene KP\nund die KP\nder Mitstreiter. — Absence DE |
| 0xA3EAC2 | corrigé | 708 | `0x99FCA0` | Schützt den Anwender.\nSenkt bei Kontakt\ndie Verteidigung\ndes Ziels stark. — Absence DE |
| 0xA3EB0D | corrigé | 709 | `0x99FCA4` | Verbeugt sich und\nsticht mit dem Haar\nzu. Trifft immer. — Absence DE |
| 0xA3EB9C | corrigé | 711 | `0x99FCAC` | Eternatus' stärkste\nAttacke. Anwender\nsetzt in der\nnächsten Runde aus. — Absence DE |
| 0xA3EBE3 | corrigé | 712 | `0x99FCB0` | Ein Stahlstrahl\naus dem Körper\ntrifft. Schadet\nauch dem Anwender. — Absence DE |
| 0xA3EC26 | corrigé | 713 | `0x99FCB4` | Wird im Psychofeld\nstärker und trifft\nalle gegnerischen\nZiele. — Absence DE |
| 0xA3EC76 | corrigé | 714 | `0x99FCB8` | Greift an und hebt\ndas Feld auf.\nOhne Feld schlägt\ndie Attacke fehl. — Absence DE |
| 0xA3ECC8 | corrigé | 715 | `0x99FCBC` | Trifft zwei- bis\nfünfmal. Initiative\nsteigt, Verteidigung\nsinkt. — Absence DE |
| 0xA3ED0E | corrigé | 716 | `0x99FCC0` | Sammelt in Runde 1\nWeltraumenergie und\nerhöht dabei den\nSpezialangriff. — Absence DE |
| 0xA3ED59 | corrigé | 717 | `0x99FCC4` | Trifft physisch oder\nspeziell, je nachdem,\nwas wirksamer ist.\nKann vergiften. — Absence DE |
| 0xA3EDA8 | corrigé | 718 | `0x99FCC8` | Der Anwender\nexplodiert und wird\nbesiegt. Stärker\nim Nebelfeld. — Absence DE |
| 0xA3EDF3 | corrigé | 719 | `0x99FCCC` | Gleitet zum Angriff\nüber den Boden.\nHat im Grasfeld\nPriorität. — Absence DE |
| 0xA3EE3A | corrigé | 720 | `0x99FCD0` | Greift mit Spannung\naus dem Boden an.\nDoppelte Stärke\nim Elektrofeld. — Absence DE |
| 0xA3EE8A | corrigé | 721 | `0x99FCD4` | Typ und Stärke\nder Attacke hängen\nvom aktiven Feld\nim Kampf ab. — Absence DE |
| 0xA3EED5 | corrigé | 722 | `0x99FCD8` | Huscht hinter das\nZiel und greift an.\nSenkt dessen\nSpezialangriff. — Absence DE |
| 0xA3EF25 | corrigé | 723 | `0x99FCDC` | Verbrennt Ziele,\nderen Statuswerte\nin dieser Runde\nerhöht wurden. — Absence DE |
| 0xA3EF73 | corrigé | 724 | `0x99FCE0` | Doppelte Stärke,\nwenn eigene Werte\nin dieser Runde\ngesenkt wurden. — Absence DE |
| 0xA3EFBD | corrigé | 725 | `0x99FCE4` | Greift mit dem Item\ndes Ziels an.\nSchlägt fehl, wenn\ndas Ziel keines hat. — Absence DE |
| 0xA3F00D | corrigé | 726 | `0x99FCE8` | Ätzendes Gas löst\ndas getragene Item\ndes Ziels auf. — Absence DE |
| 0xA3F059 | corrigé | 727 | `0x99FCEC` | Trainiert einen\nMitstreiter. Erhöht\ndessen Angriff\nund Verteidigung. — Absence DE |
| 0xA3F0A1 | corrigé | 728 | `0x99FCF0` | Greift an und\nwechselt dann mit\neinem Pokémon\naus dem Team. — Absence DE |
| 0xA3F0E1 | corrigé | 729 | `0x99FCF4` | Drei Tritte, die\nmit jedem Treffer\nstärker werden. — Absence DE |
| 0xA3F172 | corrigé | 731 | `0x99FCFC` | Wirft glühenden Sand\nauf das Ziel.\nKann es außerdem\nverbrennen. — Absence DE |
| 0xA3F1BC | corrigé | 732 | `0x99FD00` | Heilt eigene KP\nund Statusprobleme\nsowie die eines\nMitstreiters. — Absence DE |
| 0xA3F202 | corrigé | 733 | `0x99FD04` | Ein heftiger Schlag\ntrifft das Ziel.\nLandet immer\neinen Volltreffer. — Absence DE |
| 0xA3F24A | corrigé | 734 | `0x99FD08` | Trifft dreimal\nhintereinander.\nLandet dabei immer\nVolltreffer. — Absence DE |
| 0xA3F2E3 | corrigé | 736 | `0x99FD10` | Ein heftiger Tritt\ntrifft das Ziel.\nSenkt dessen\nVerteidigung. — Absence DE |
| 0xA3F32A | corrigé | 737 | `0x99FD14` | Dunkle, heftige\nFlammen treffen.\nLässt das Ziel evtl.\nzurückschrecken. — Absence DE |
| 0xA3F377 | corrigé | 738 | `0x99FD18` | Greift mit Psycho-\nKraft an. Zieht der\nletzten Attacke\ndes Ziels 3 AP ab. — Absence DE |
| 0xA3F3C7 | corrigé | 739 | `0x99FD1C` | Ein Elektrokäfig\nhält das Ziel\nvier bis fünf\nRunden lang fest. — Absence DE |
| 0xA3F410 | corrigé | 740 | `0x99FD20` | Je mehr KP der\nAnwender hat,\ndesto stärker\nist diese Attacke. — Absence DE |
| 0xA3F5BF | corrigé | 746 | `0x99FD38` | Trifft mit einer Axt\nund hinterlässt\nSplitter. Hohe\nVolltrefferquote. — Budget et Volltrefferquote |
| 0xA40110 | corrigé | 857,858 | `0x99FEF4`, `0x99FEF8` | G-Max Venusaur:\nFügt über vier\nRunden Schaden zu. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40151 | corrigé | 859,860 | `0x99FEFC`, `0x99FF00` | G-Max Charizard:\nFügt über vier\nRunden Schaden zu. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40193 | corrigé | 861,862 | `0x99FF04`, `0x99FF08` | G-Max Blastoise:\nFügt über vier\nRunden Schaden zu. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA401D5 | corrigé | 863,864 | `0x99FF0C`, `0x99FF10` | G-Max Butterfree:\nKann lähmen,\neinschläfern\noder vergiften. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4021F | corrigé | 865,866 | `0x99FF14`, `0x99FF18` | G-Max Pikachu:\nLähmt das Ziel. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40258 | corrigé | 867,868 | `0x99FF1C`, `0x99FF20` | G-Max Meowth:\nVerwirrt den Gegner\nund erzeugt Geld. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4029E | corrigé | 869,870 | `0x99FF24`, `0x99FF28` | G-Max Machamp:\nErhöht die Chance\nauf Volltreffer. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA402E5 | corrigé | 871,872 | `0x99FF2C`, `0x99FF30` | G-Max Gengar:\nVerhindert, dass\nder Gegner flieht. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40327 | corrigé | 873,874 | `0x99FF34`, `0x99FF38` | G-Max Kingler:\nSenkt die Initiative\ndes Ziels stark. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4036D | corrigé | 875,876 | `0x99FF3C`, `0x99FF40` | G-Max Lapras:\nVerringert den\nSchaden für\nfünf Runden. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA403AE | corrigé | 877,878 | `0x99FF44`, `0x99FF48` | G-Max Eevee:\nBezaubert das Ziel. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA403E6 | corrigé | 879,880 | `0x99FF4C`, `0x99FF50` | G-Max Snorlax:\nStellt verzehrte\nBeeren wieder her. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4042B | corrigé | 881,882 | `0x99FF54`, `0x99FF58` | G-Max Garbodor:\nVergiftet das Ziel. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40463 | corrigé | 883,884 | `0x99FF5C`, `0x99FF60` | G-Max Melmetal:\nVerhindert, dass\nder Gegner seine\nAttacken wiederholt. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA404AE | corrigé | 885,886 | `0x99FF64`, `0x99FF68` | G-Max Rillaboom:\nTrifft trotz der\nFähigkeit des Ziels. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA404FF | corrigé | 887,888 | `0x99FF6C`, `0x99FF70` | G-Max Cinderace:\nTrifft trotz der\nFähigkeit des Ziels. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40550 | corrigé | 889,890 | `0x99FF74`, `0x99FF78` | G-Max Inteleon:\nTrifft trotz der\nFähigkeit des Ziels. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA405A0 | corrigé | 891,892 | `0x99FF7C`, `0x99FF80` | G-Max Corviknight:\nHebt die Effekte\nvon Wällen auf. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA405EB | corrigé | 893 | `0x99FF84`, `0x99FF88` | G-Max Orbeetle:\nVerändert die\nSchwerkraft für\nfünf Runden. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4062F | corrigé |  | `0x99FF8C`, `0x99FF90` | G-Max Drednaw:\nVerstreut Felsbrocken\nauf dem Feld. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40673 | corrigé |  | `0x99FF94`, `0x99FF98` | G-Max Coalossal:\nFügt über vier\nRunden Schaden zu. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA406B5 | corrigé |  | `0x99FF9C`, `0x99FFA0` | G-Max Flapple:\nSenkt den Fluchtwert\ndes Gegners. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA406F7 | corrigé |  | `0x99FFA4`, `0x99FFA8` | G-Max Appletun:\nHeilt den Status\nseiner Verbündeten. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4073B | corrigé |  | `0x99FFAC`, `0x99FFB0` | G-Max Sandaconda:\nFängt den Gegner für\nvier bis fünf Runden. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40787 | corrigé |  | `0x99FFB4`, `0x99FFB8` | G-Max Toxtricity:\nLähmt oder vergiftet\ndie Gegner. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA407CD | corrigé |  | `0x99FFBC`, `0x99FFC0` | G-Max Centiskorch:\nFängt den Gegner für\nvier bis fünf Runden. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4081A | corrigé |  | `0x99FFC4`, `0x99FFC8` | G-Max Hatterene:\nVerwirrt das Ziel. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40854 | corrigé |  | `0x99FFCC`, `0x99FFD0` | G-Max Grimmsnarl:\nMacht den Gegner\nschläfrig. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA4089B | corrigé |  | `0x99FFD4`, `0x99FFD8` | G-Max Alcremie:\nHeilt die KP seiner\nVerbündeten. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA408DB | corrigé |  | `0x99FFDC`, `0x99FFE0` | G-Max Copperajah:\nVerteilt Stahlsplitter\nauf dem Feld. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40923 | corrigé |  | `0x99FFE4`, `0x99FFE8` | G-Max Duraludon:\nSenkt die AP\nder zuletzt\neingesetzten Attacke. — Nom propre EN et boîte ≤5 lignes / 122 px |
| 0xA40A1D | déjà patché | 1 | table indexée | Klaps — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A2A | déjà patché | 2 | table indexée | Karateschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A37 | déjà patché | 3 | table indexée | Duplexhieb — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A44 | déjà patché | 4 | table indexée | Kometenhieb — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A51 | déjà patché | 5 | table indexée | Megahieb — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A5E | déjà patché | 6 | table indexée | Zahltag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A6B | déjà patché | 7 | table indexée | Feuerschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A78 | déjà patché | 8 | table indexée | Eishieb — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A85 | déjà patché | 9 | table indexée | Donnerschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A92 | déjà patché | 10 | table indexée | Kratzer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40A9F | déjà patché | 11 | table indexée | Klammer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AAC | déjà patché | 12 | table indexée | Guillotine — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AB9 | déjà patché | 13 | table indexée | Klingensturm — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AC6 | déjà patché | 14 | table indexée | Schwerttanz — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AD3 | déjà patché | 15 | `0xA6CABC` | Zerschneider — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AE0 | déjà patché | 16 | table indexée | Windstoß — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AED | déjà patché | 17 | table indexée | Flügelschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40AFA | déjà patché | 18 | table indexée | Wirbelwind — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B14 | déjà patché | 20 | table indexée | Klammergriff — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B21 | déjà patché | 21 | table indexée | Slam — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B2E | déjà patché | 22 | table indexée | Rankenhieb — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B3B | déjà patché | 23 | table indexée | Stampfer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B48 | déjà patché | 24 | table indexée | Doppelkick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B55 | déjà patché | 25 | table indexée | Megakick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B62 | déjà patché | 26 | table indexée | Sprungkick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B6F | déjà patché | 27 | table indexée | Fegekick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B7C | déjà patché | 28 | table indexée | Sandwirbel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B89 | déjà patché | 29 | table indexée | Kopfnuss — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40B96 | déjà patché | 30 | table indexée | Hornattacke — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BA3 | déjà patché | 31 | table indexée | Furienschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BB0 | déjà patché | 32 | table indexée | Hornbohrer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BBD | déjà patché | 33 | table indexée | Tackle — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BCA | déjà patché | 34 | table indexée | Bodyslam — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BD7 | déjà patché | 35 | table indexée | Wickel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BE4 | déjà patché | 36 | table indexée | Bodycheck — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BF1 | déjà patché | 37 | table indexée | Fuchtler — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40BFE | déjà patché | 38 | table indexée | Risikotackle — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C0B | déjà patché | 39 | table indexée | Rutenschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C18 | déjà patché | 40 | table indexée | Giftstachel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C25 | déjà patché | 41 | table indexée | Duonadel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C32 | déjà patché | 42 | table indexée | Nadelrakete — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C3F | déjà patché | 43 | table indexée | Silberblick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C4C | déjà patché | 44 | table indexée | Biss — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C59 | déjà patché | 45 | table indexée | Heuler — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C66 | déjà patché | 46 | table indexée | Brüller — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C73 | déjà patché | 47 | table indexée | Gesang — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C80 | déjà patché | 48 | table indexée | Superschall — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C8D | déjà patché | 49 | table indexée | Ultraschall — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40C9A | déjà patché | 50 | table indexée | Aussetzer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CA7 | déjà patché | 51 | table indexée | Säure — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CB4 | déjà patché | 52 | table indexée | Glut — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CC1 | déjà patché | 53 | table indexée | Flammenwurf — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CCE | déjà patché | 54 | table indexée | Weißnebel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CDB | déjà patché | 55 | table indexée | Aquaknarre — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CE8 | déjà patché | 56 | table indexée | Hydropumpe — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40CF5 | déjà patché | 57 | `0xA6CAD4` | Surfer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D02 | déjà patché | 58 | table indexée | Eisstrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D0F | déjà patché | 59 | table indexée | Blizzard — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D1C | déjà patché | 60 | table indexée | Psystrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D29 | déjà patché | 61 | table indexée | Blubbstrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D36 | déjà patché | 62 | table indexée | Aurorastrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D43 | déjà patché | 63 | table indexée | Hyperstrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D50 | déjà patché | 64 | table indexée | Pikser — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D5D | déjà patché | 65 | table indexée | Bohrschnabel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D6A | déjà patché | 66 | table indexée | Überroller — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D77 | déjà patché | 67 | table indexée | Fußkick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D84 | déjà patché | 68 | table indexée | Konter — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D91 | déjà patché | 69 | table indexée | Geowurf — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40D9E | déjà patché | 70 | `0xA6CACC` | Stärke — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DAB | déjà patché | 71 | table indexée | Absorber — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DB8 | déjà patché | 72 | table indexée | Megasauger — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DC5 | déjà patché | 73 | table indexée | Egelsamen — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DD2 | déjà patché | 74 | table indexée | Wachstum — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DDF | déjà patché | 75 | table indexée | Rasierblatt — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DEC | déjà patché | 76 | table indexée | Solarstrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40DF9 | déjà patché | 77 | table indexée | Giftpuder — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E06 | déjà patché | 78 | table indexée | Stachelspore — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E13 | déjà patché | 79 | table indexée | Schlafpuder — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E20 | déjà patché | 80 | table indexée | Blättertanz — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E2D | déjà patché | 81 | table indexée | Fadenschuss — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E3A | déjà patché | 82 | table indexée | Drachenwut — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E47 | déjà patché | 83 | table indexée | Feuerwirbel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E54 | déjà patché | 84 | table indexée | Donnerschock — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E61 | déjà patché | 85 | table indexée | Donnerblitz — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E6E | déjà patché | 86 | table indexée | Donnerwelle — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E7B | déjà patché | 87 | table indexée | Donner — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E88 | déjà patché | 88 | table indexée | Steinwurf — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40E95 | déjà patché | 89 | table indexée | Erdbeben — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40EA2 | déjà patché | 90 | table indexée | Geofissur — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40EBC | déjà patché | 92 | table indexée | Toxin — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40EC9 | déjà patché | 93 | table indexée | Konfusion — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40ED6 | déjà patché | 94 | table indexée | Psychokinese — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40EE3 | déjà patché | 95 | table indexée | Hypnose — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40EF0 | déjà patché | 96 | table indexée | Meditation — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40EFD | déjà patché | 97 | table indexée | Agilität — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F0A | déjà patché | 98 | table indexée | Ruckzuckhieb — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F17 | déjà patché | 99 | table indexée | Raserei — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F24 | déjà patché | 100 | `0xA6CAEC` | Teleport — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F31 | déjà patché | 101 | table indexée | Nachtnebel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F3E | déjà patché | 102 | table indexée | Mimikry — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F4B | déjà patché | 103 | table indexée | Kreideschrei — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F58 | déjà patché | 104 | table indexée | Doppelteam — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F65 | déjà patché | 105 | table indexée | Genesung — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F72 | déjà patché | 106 | table indexée | Härtner — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F7F | déjà patché | 107 | table indexée | Komprimator — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F8C | déjà patché | 108 | table indexée | Rauchwolke — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40F99 | déjà patché | 109 | table indexée | Konfusstrahl — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40FA6 | déjà patché | 110 | table indexée | Panzerschutz — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40FB3 | déjà patché | 111 | table indexée | Einigler — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40FCD | déjà patché | 113 | table indexée | Lichtschild — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40FDA | déjà patché | 114 | table indexée | Dunkelnebel — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40FE7 | déjà patché | 115 | table indexée | Reflektor — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA40FF4 | déjà patché | 116 | table indexée | Energiefokus — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41001 | déjà patché | 117 | table indexée | Geduld — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4100E | déjà patché | 118 | table indexée | Metronom — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4101B | déjà patché | 119 | table indexée | Spiegeltrick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41028 | déjà patché | 120 | table indexée | Finale — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41035 | déjà patché | 121 | table indexée | Eierbombe — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41042 | déjà patché | 122 | table indexée | Schlecker — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4104F | déjà patché | 123 | table indexée | Smog — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4105C | déjà patché | 124 | table indexée | Schlammbad — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41069 | déjà patché | 125 | table indexée | Knochenkeule — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41076 | déjà patché | 126 | table indexée | Feuersturm — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41083 | déjà patché | 127 | `0xA6CAE4` | Kaskade — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41090 | déjà patché | 128 | table indexée | Schnapper — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4109D | déjà patché | 129 | table indexée | Sternschauer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410AA | déjà patché | 130 | table indexée | Schädelwumme — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410B7 | déjà patché | 131 | table indexée | Dornkanone — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410C4 | déjà patché | 132 | table indexée | Umklammerung — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410D1 | déjà patché | 133 | table indexée | Amnesie — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410DE | déjà patché | 134 | table indexée | Psykraft — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410EB | déjà patché | 135 | `0xA6CB04` | Weichei — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA410F8 | déjà patché | 136 | table indexée | Turmkick — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41105 | déjà patché | 137 | table indexée | Schlangenbl. — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41112 | déjà patché | 138 | table indexée | Traumfresser — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4111F | déjà patché | 139 | table indexée | Giftwolke — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4112C | déjà patché | 140 | table indexée | Stakkato — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41139 | déjà patché | 141 | table indexée | Blutsauger — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41146 | déjà patché | 142 | table indexée | Todeskuss — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41153 | déjà patché | 143 | table indexée | Himmelsfeger — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41160 | déjà patché | 144 | table indexée | Wandler — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4116D | déjà patché | 145 | table indexée | Blubber — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA4117A | déjà patché | 146 | table indexée | Irrschlag — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41187 | déjà patché | 147 | table indexée | Pilzspore — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA41194 | déjà patché | 148 | `0xA6CAB4` | Blitz — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA411A1 | déjà patché | 149 | table indexée | Psywelle — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA411AE | déjà patché | 150 | table indexée | Platscher — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
| 0xA411BB | déjà patché | 151 | table indexée | Säurepanzer — Patch move_names : index CFRU, glossaire officiel, cellule 13 octets ; absence combined légitime |
