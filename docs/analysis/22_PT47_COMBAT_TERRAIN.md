# PT-47 — Terrain, Cube, combat et types CFRU

Le manifeste PT-47 contient exactement 283 clés. Le bilan exhaustif, dans le même
ordre, est `languages/pt/data/pt47_audit.json` : anglais du corpus, comparaison FR,
octets source, offset réellement consommé, pointeurs, décision, octets PT et pixels.

- 162 traductions PT-BR ; 50 valeurs identiques/noms conservés selon F-759.
- 71 exceptions sans ajout au combined : 66 extractions binaires non linguistiques
  de 0xa95c4d à 0xaf36d2 ; deux libellés Exit sans pointeur (0xa4e504/0xa4e50d),
  l'ancien avertissement démo (0xa4ec59), Random (0xa4ed42), et la fausse clé
  0xa4ead2 (préfixe C0 46 de Normal, dont la vraie cellule 0xa4ead4 est traitée).
  Chaque exception enregistre ses octets et le résultat vide du scan des pointeurs
  32 bits, toutes positions comprises. L'absence de consommateur établi justifie
  de ne pas écrire dans ces données ; ce n'est pas une traduction revendiquée.
- Trois clés commencent avant leur texte : 0xa4e43e → 0xa4e440 (niveau recommandé),
  0xa4e4b5 → 0xa4e4b8 (DexNav), 0xa4ee0a → 0xa4ee0c (Breakneck Blitz).
  Le patch utilise les pointeurs vers le texte, jamais les préfixes.

La table des types commence à 0xa4ead4, cellules de sept octets. Le lecteur
0xa0944c charge 7 et multiplie l'index à 0xa09450 ; son littéral de base est à
0xa09478. Trois autres lecteurs utilisent cette base : 0xd8510, 0x11972c,
0x11977c. Le patch conserve ces bases et écrit uniquement les 23 cellules du
manifeste. La cellule ??? à 0xa4eb13 est hors lot et reste intacte.

Abréviations éditoriales limitées à cette table : Lutad. (Lutador), Venen.
(Venenoso), Terr. (Terrestre), Fant. (Fantasma), Elétr. (Elétrico), Psíq.
(Psíquico), Sombr. (Sombrio). Les autres termes suivent F-759 sans abréviation.
Les cinq cellules « - » sont conservées. Aucun nom de mouvement Z n'est inventé
à partir du français : la politique F-759 conserve l'anglais sans attestation BR.
Cube Corp., Hidden Grottos, Battle Mine et Ring Challenge restent les noms anglais.

Les contrôles FD/FC/F8 sont écrits en hexadécimal explicite, dans l'ordre source.
Les FA/FB sont conservés exactement. Des retours de ligne sont ajoutés lorsque
nécessaires pour les noms développés. Les espaces initiaux/finaux significatifs
sont `<0x00>` : les chargeurs du combined suppriment les espaces de bord littéraux.
Les ellipses source B0 restent `<0xB0>`, un seul octet.

Le patch PT réutilise BorriusTextPatch/StructuredTextPatch pour les 189 textes à
pointeurs. Il valide les préimages et les contrôles avant une application atomique,
relit les cibles finales, conserve les cellules fixes et est idempotent. Aucune
modification du moteur partagé ou des autres langues.

Les tests unitaires couvrent le manifeste, les protections, les commandes, les
budgets, les invariants métier (baies, Habilidade, essaim, fin de combat), les bornes,
l'atomicité et l'idempotence. Les tests ROM vérifient les préimages, tous les
pointeurs et les octets finaux, puis les cinq polices avec tampons développés.
La sonde Playwright hors écran utilise les vrais pointeurs et textes de la ROM
finale dans une msgbox native sur une copie temporaire. Elle vérifie par OCR
le retour à la surface avec l'ADM et une réplique de combat contenant ã.
Elle ne revendique pas un parcours de toutes les scènes ni un combat complet.
