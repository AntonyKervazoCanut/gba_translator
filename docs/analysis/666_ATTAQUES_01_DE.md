# B-666 — Qualification du lot attaques-01

Périmètre fermé : 47 offsets, dernières occurrences des trois fichiers et ROM EN
canonique. `combined_en` contient des valeurs françaises historiques pour les
descriptions ; la ROM EN fait foi. Les espaces initiaux des noms appartiennent
aux cellules fixes. Les champs séparés par `/` représentent les retours à la ligne.

La table Trainer Tower est référencée par le littéral `0x15DD24 → 0x4827B4` ;
voir aussi `docs/analysis/23_PT18_MENUS_SYSTEMES.md`. Les deux extractions
STARMIE débutent dans des métadonnées, pas au début d’une chaîne. Le glossaire
`official_terminology.yaml` donne Mild pour la nature Mild. Les alphabets sont
des caractères de saisie. Aucun dialogue, genre ou registre n’est en jeu.

| Offset | ROM EN canonique | Dernier EN | Dernier FR | Dernier DE | Décision |
|---|---|---|---|---|---|
| `0x463E25` | Mild | Mild | Doux | Mild | Nature officielle Mild, identique EN/DE. |
| `0x4716B4` | hii?xzz / xzz / xzz | hii<0xFD>xzz / xzz / xzz | hii{STRING}xzz / xzz / xzz | — | Faux texte binaire, FD EC ; aucun pointeur direct. |
| `0x475638` | ABCDEFG | ABCDEFG | ABCDEFG | — | Lettres de saisie, conservées. |
| `0x47AAC1` | ABCDE | ABCDE | ABCDE | — | Lettres de saisie, conservées. |
| `0x47AAC7` | FGHIJ | FGHIJ | FGHIJ | — | Lettres de saisie, conservées. |
| `0x47AACD` | KLMNO | KLMNO | KLMNO | — | Lettres de saisie, conservées. |
| `0x47AAD3` | PQRST | PQRST | PQRST | — | Lettres de saisie, conservées. |
| `0x47AAD9` | UVWXY | UVWXY | UVWXY | — | Lettres de saisie, conservées. |
| `0x47AAFD` | abcde | abcde | abcde | — | Lettres de saisie, conservées. |
| `0x47AB03` | fghij | fghij | fghij | — | Lettres de saisie, conservées. |
| `0x47AB09` | klmno | klmno | klmno | — | Lettres de saisie, conservées. |
| `0x47AB0F` | pqrst | pqrst | pqrst | — | Lettres de saisie, conservées. |
| `0x47AB15` | uvwxy | uvwxy | uvwxy | — | Lettres de saisie, conservées. |
| `0x47B898` | JOS & ANNE | JOS & ANNE | JOS & ANNE | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47BC78` | EMY & ALEK | EMY & ALEK | EMY & ALEK | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47C058` | JO & HALEY | JO & HALEY | JO & HALEY | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47C432` |       ERNEST |       ERNEST | ERNEST | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47C57A` |       GABRIEL |       GABRIEL | GABRIEL | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47C818` | REBECCA | REBECCA | RÉBECCA | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47C960` | NICOLAS | NICOLAS | NICOLAS | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47D798` | RIC & RENE | RIC & RENE | RIC & RENE | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47DB78` | JEN & KIRA | JEN & KIRA | JEN & KIRA | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47DF58` | ISAC & MAG | ISAC & MAG | ISAC & MAG | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47E277` | EŒ   STARMIE | EŒ   STARMIE | EŒ   STAROSS | EŒ   STARMIE | Extraction de métadonnées de Pokémon, ne pas traduire. |
| `0x47E338` | TRENTON | TRENTON | TRENTON | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47E480` | ALBERT | ALBERT | ALBERT | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47E718` | NATALIA | NATALIA | NATALIE | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47E860` | KATHLEEN | KATHLEEN | KATHLÉEN | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47EDEB` | EÔ   STARMIE | EÔ   STARMIE | EÔ   STAROSS | EÔ   STARMIE | Extraction de métadonnées de Pokémon, ne pas traduire. |
| `0x47F698` | KAT & KIPP | KAT & KIPP | KAT & KIPP | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47FA78` | GEB&MEGAN | GEB&MEGAN | GEB&MÉGAN | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x47FE58` | LISA&LEAH | LISA&LEAH | LISA&LÉAH | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x480234` |     CHARLOTTE |     CHARLOTTE | CHARLOTTE | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x480380` | SHANIA | SHANIA | SHANIA | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x480618` | KADEN | KADEN | KADEN | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x480760` | EMANUEL | EMANUEL | EMANUEL | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x481598` | NIA & CARL | NIA & CARL | NIA & CARL | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x481978` | AXE & REN | AXE & REN | AXE & REN | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x481D58` | KATI & GEB | KATI & GEB | KATI & GEB | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x482138` | CAMDEN | CAMDEN | CAMDEN | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x482280` | ZACKERY | ZACKERY | ZACKER | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x482518` | MIKAELA | MIKAELA | MIKAÉLA | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x482660` | FLINT | FLINT | SILEX | — | Nom propre dans la table fixe Trainer Tower, conservé. |
| `0x482834` | A physical attack / delivered with a / long tail or a / foreleg, etc. | Écrase l'ennemi avec / les pattes avant, la / queue, etc. | — | Physischer Angriff / mit langem Schweif / oder Vorderbein / usw. | Corrigé et protégé ; voir les pointeurs ci-dessous. |
| `0x483C22` | A cloud of toxic / dust is scattered. / It may poison the / foe. | Une poudre toxique / empoisonne l'ennemi. | Un nuage de poussière / toxique est dispersé. Il / peut empoisonner l'ennemi / . | Giftstaub wird / verstreut. Er kann / das Ziel / vergiften. | Corrigé et protégé ; voir les pointeurs ci-dessous. |
| `0x48493B` | The foe is hit with / an intense flame. / It may leave the / target with a burn. | Un déluge de flammes / ardentes submerge / l'ennemi. Peut aussi / le brûler. | L'ennemi est frappé par / une flamme intense. Il / peut laisser la cible / brûlée. | Eine starke Flamme / trifft das Ziel und / kann es / verbrennen. | Corrigé et protégé ; voir les pointeurs ci-dessous. |
| `0x4853BE` | An attack that is / used only if there / is no PP. It also / hurts the user. |  | Une attaque qui n'est utilisée / que s'il n'y a aucun PP. Cela / également blesse / l'utilisateur. | Nur bei fehlenden AP / setzt der Anwender / diese Attacke ein. Er / nimmt dabei Schaden. | Corrigé et protégé ; voir les pointeurs ci-dessous. |

Les sites de la table des attaques sont respectivement `0x99F194`, `0x99F2C4`,
`0x99F388` et `0x99F424` ; la fiche CT à `0x879A1C` partage la troisième
description. La source EN confirme ces cinq références. Les quatre textes
comportent trois ruptures `FE`, aucun autre contrôle ni placeholder, et
quatre lignes dont la largeur maximale est respectivement 100, 98, 102 et
115 pixels, pour un budget de 122 pixels en résumé et 144 pixels en CT.

Les espaces et les noms de Trainer Tower restent en place. Les chaînes
d'alphabet ont des pointeurs dans la table de saisie. Le fragment `0x4716B4`
est une extraction de données binaires et n'a pas de pointeur direct. Les
comparaisons d'octets des exclusions ont été faites dans la ROM DE disponible ;
les descriptions doivent être vérifiées dans une ROM reconstruite par leurs
pointeurs, et le test Playwright de la fiche CT constitue une preuve ciblée,
non une validation visuelle de toutes les attaques.
