# PT-50 — Descriptions Pokédex et faux positifs binaires

F-809 : manifeste fermé de 299 offsets. F-758 et F-759 intégrés et vérifiés dans l’ascendance Git.

182 descriptions Pokédex (indices internes 386 à 567) traduites depuis les octets anglais propres. Les références EN historiques et FR sont conservées dans `languages/pt/data/pt50_audit.json` pour chaque offset ; elles divergent souvent de la ROM. 117 fragments non linguistiques ne sont pas traduits : recherche exhaustive du pointeur 32 bits little-endian sans résultat, octets et contexte consignés. Cela ne signifie pas que leurs données binaires sont inutilisées. Aucun texte ne doit y être injecté.

Les noms propres non attestés restent anglais (Prinplup, Odd Keystone, Distortion World, Mini-Noses, etc.) suivant F-759. Les unités sont converties : 160 pieds > 48 m, 30 mph ≈ 48 km/h, 25 mph ≈ 40 km/h, 3 600 °F ≈ 2 000 °C, 1 100 °F ≈ 593 °C.

Le finaliseur `batch_50` réutilise StructuredTextPatch après les réparations : validation des préimages, allocation bornée, repointage des seuls consommateurs audités, contrôle des octets et des chevauchements. La table Pokédex indexée garde ses cellules de 36 octets et tous ses autres champs. Aucune écriture de nom/catégorie fixe. Les textes gardent exactement leurs deux ou trois lignes et aucun code supplémentaire. Budget de 224 pixels, contrôlé dans les cinq polices réelles et dans le calcul conservateur partagé.

## Bilan par offset

| Offset | Résultat | Pointeur(s) source | Octets PT | Largeur maximale |
|---|---|---|---|---|
| `0x1018e38` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1018e5c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x101a69c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x101f052` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x101f779` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x101f887` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1021176` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x102418c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x102d087` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1036838` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10368bc` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1038706` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x103a8b8` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x103c3a2` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x103c46e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x103c47d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x103c585` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1045f85` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1047444` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1047a14` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1047a26` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1047d0a` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1048ed1` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x104909e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x105bf39` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x106eb5a` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x108dee1` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1091f80` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10aebdd` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10c91f2` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10cd523` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10d15e6` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10eb46c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10f8f66` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x10fac56` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1103a2b` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x111d947` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1125db6` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x112a266` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1132c28` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1138743` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x115596d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x115a8d8` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1162b4a` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1167875` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x117e141` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11860dd` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11863b6` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1193e36` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1196153` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11964b8` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11aa6e9` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11ab2f8` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11ad055` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11b67a4` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11ce32e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11d5e2f` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11efdd4` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x11eff12` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12017ae` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x120cb55` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12183be` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1219b39` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x121b310` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x123efe4` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1267f34` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1268287` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12689e4` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1269152` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1269a5c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1281603` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x128162d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x129e4fc` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12a1d5f` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12b3ed3` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12bdb8b` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12e1a20` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x12fb310` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x135fd8d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x136360c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x136585d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x136de87` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x137aa85` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x138f78e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1391579` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x139bc5d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13a67c8` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13a8b8e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13b9d73` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13bb7cd` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13bc448` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13c1515` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13c3db2` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13c521e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13c8958` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13ccf84` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13cda1d` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13d79bb` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x13fd83f` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x140d6b4` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14410e8` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x144491e` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1451c4c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1460f88` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x146e103` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x1478d4c` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14794f0` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x148ccb4` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14900e3` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14a4ec0` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14a79c5` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14b8901` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14b9021` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14b9372` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14bac23` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14be863` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x14bed6b` | Exception : fragment binaire non linguistique | Aucun pointeur direct ; contexte et préimage dans l’audit JSON | — | — |
| `0x165c2b6` | Traduit ; contrôle source/ROM automatisé | `0x1a38e48` | 71 | 141 px |
| `0x165c310` | Traduit ; contrôle source/ROM automatisé | `0x1a38e6c` | 73 | 139 px |
| `0x165c35e` | Traduit ; contrôle source/ROM automatisé | `0x1a38e90` | 68 | 150 px |
| `0x165c3ac` | Traduit ; contrôle source/ROM automatisé | `0x1a38eb4` | 74 | 147 px |
| `0x165c408` | Traduit ; contrôle source/ROM automatisé | `0x1a38ed8` | 67 | 139 px |
| `0x165c461` | Traduit ; contrôle source/ROM automatisé | `0x1a38efc` | 83 | 158 px |
| `0x165c4c4` | Traduit ; contrôle source/ROM automatisé | `0x1a38f20` | 90 | 178 px |
| `0x165c527` | Traduit ; contrôle source/ROM automatisé | `0x1a38f44` | 86 | 161 px |
| `0x165c586` | Traduit ; contrôle source/ROM automatisé | `0x1a38f68` | 80 | 152 px |
| `0x165c5de` | Traduit ; contrôle source/ROM automatisé | `0x1a38f8c` | 76 | 144 px |
| `0x165c631` | Traduit ; contrôle source/ROM automatisé | `0x1a38fb0` | 88 | 168 px |
| `0x165c685` | Traduit ; contrôle source/ROM automatisé | `0x1a38fd4` | 72 | 151 px |
| `0x165c6d7` | Traduit ; contrôle source/ROM automatisé | `0x1a38ff8` | 69 | 140 px |
| `0x165c732` | Traduit ; contrôle source/ROM automatisé | `0x1a3901c` | 89 | 179 px |
| `0x165c790` | Traduit ; contrôle source/ROM automatisé | `0x1a39040` | 57 | 165 px |
| `0x165c7db` | Traduit ; contrôle source/ROM automatisé | `0x1a39064` | 77 | 152 px |
| `0x165c836` | Traduit ; contrôle source/ROM automatisé | `0x1a39088` | 89 | 171 px |
| `0x165c891` | Traduit ; contrôle source/ROM automatisé | `0x1a390ac` | 93 | 175 px |
| `0x165c8ee` | Traduit ; contrôle source/ROM automatisé | `0x1a390d0` | 84 | 178 px |
| `0x165c93f` | Traduit ; contrôle source/ROM automatisé | `0x1a390f4` | 80 | 163 px |
| `0x165c99f` | Traduit ; contrôle source/ROM automatisé | `0x1a39118` | 89 | 172 px |
| `0x165c9f8` | Traduit ; contrôle source/ROM automatisé | `0x1a3913c` | 85 | 174 px |
| `0x165ca48` | Traduit ; contrôle source/ROM automatisé | `0x1a39160` | 83 | 159 px |
| `0x165caa4` | Traduit ; contrôle source/ROM automatisé | `0x1a39184` | 73 | 144 px |
| `0x165cb04` | Traduit ; contrôle source/ROM automatisé | `0x1a391a8` | 91 | 185 px |
| `0x165cb59` | Traduit ; contrôle source/ROM automatisé | `0x1a391cc` | 84 | 176 px |
| `0x165cbaf` | Traduit ; contrôle source/ROM automatisé | `0x1a391f0` | 76 | 147 px |
| `0x165cc00` | Traduit ; contrôle source/ROM automatisé | `0x1a39214` | 54 | 154 px |
| `0x165cc43` | Traduit ; contrôle source/ROM automatisé | `0x1a39238` | 91 | 176 px |
| `0x165cc98` | Traduit ; contrôle source/ROM automatisé | `0x1a3925c` | 76 | 146 px |
| `0x165ccec` | Traduit ; contrôle source/ROM automatisé | `0x1a39280` | 80 | 156 px |
| `0x165cd4b` | Traduit ; contrôle source/ROM automatisé | `0x1a392a4` | 90 | 172 px |
| `0x165cda8` | Traduit ; contrôle source/ROM automatisé | `0x1a392c8` | 88 | 170 px |
| `0x165ce04` | Traduit ; contrôle source/ROM automatisé | `0x1a392ec` | 72 | 130 px |
| `0x165ce5f` | Traduit ; contrôle source/ROM automatisé | `0x1a39310` | 79 | 162 px |
| `0x165cec2` | Traduit ; contrôle source/ROM automatisé | `0x1a39334` | 50 | 145 px |
| `0x165cefb` | Traduit ; contrôle source/ROM automatisé | `0x1a39358` | 64 | 183 px |
| `0x165cf3e` | Traduit ; contrôle source/ROM automatisé | `0x1a3937c` | 65 | 188 px |
| `0x165cf86` | Traduit ; contrôle source/ROM automatisé | `0x1a393a0` | 70 | 130 px |
| `0x165cfe1` | Traduit ; contrôle source/ROM automatisé | `0x1a393c4` | 78 | 149 px |
| `0x165d03d` | Traduit ; contrôle source/ROM automatisé | `0x1a393e8` | 90 | 167 px |
| `0x165d09d` | Traduit ; contrôle source/ROM automatisé | `0x1a3940c` | 70 | 199 px |
| `0x165d0df` | Traduit ; contrôle source/ROM automatisé | `0x1a39430` | 90 | 182 px |
| `0x165d138` | Traduit ; contrôle source/ROM automatisé | `0x1a39454` | 50 | 148 px |
| `0x165d185` | Traduit ; contrôle source/ROM automatisé | `0x1a39478` | 91 | 173 px |
| `0x165d1df` | Traduit ; contrôle source/ROM automatisé | `0x1a3949c` | 72 | 141 px |
| `0x165d23d` | Traduit ; contrôle source/ROM automatisé | `0x1a394c0` | 85 | 163 px |
| `0x165d299` | Traduit ; contrôle source/ROM automatisé | `0x1a394e4` | 61 | 179 px |
| `0x165d2e2` | Traduit ; contrôle source/ROM automatisé | `0x1a39508` | 84 | 167 px |
| `0x165d342` | Traduit ; contrôle source/ROM automatisé | `0x1a3952c` | 83 | 161 px |
| `0x165d392` | Traduit ; contrôle source/ROM automatisé | `0x1a39550` | 84 | 164 px |
| `0x165d3ed` | Traduit ; contrôle source/ROM automatisé | `0x1a39574` | 85 | 164 px |
| `0x165d44b` | Traduit ; contrôle source/ROM automatisé | `0x1a39598` | 91 | 168 px |
| `0x165d4a4` | Traduit ; contrôle source/ROM automatisé | `0x1a395bc` | 88 | 180 px |
| `0x165d4f8` | Traduit ; contrôle source/ROM automatisé | `0x1a395e0` | 87 | 165 px |
| `0x165d54c` | Traduit ; contrôle source/ROM automatisé | `0x1a39604` | 84 | 158 px |
| `0x165d5a3` | Traduit ; contrôle source/ROM automatisé | `0x1a39628` | 91 | 173 px |
| `0x165d601` | Traduit ; contrôle source/ROM automatisé | `0x1a3964c` | 89 | 177 px |
| `0x165d659` | Traduit ; contrôle source/ROM automatisé | `0x1a39670` | 78 | 157 px |
| `0x165d6ae` | Traduit ; contrôle source/ROM automatisé | `0x1a39694` | 80 | 159 px |
| `0x165d702` | Traduit ; contrôle source/ROM automatisé | `0x1a396b8` | 99 | 187 px |
| `0x165d75b` | Traduit ; contrôle source/ROM automatisé | `0x1a396dc` | 68 | 133 px |
| `0x165d7ad` | Traduit ; contrôle source/ROM automatisé | `0x1a39700` | 75 | 146 px |
| `0x165d804` | Traduit ; contrôle source/ROM automatisé | `0x1a39724` | 89 | 169 px |
| `0x165d854` | Traduit ; contrôle source/ROM automatisé | `0x1a39748` | 78 | 157 px |
| `0x165d8ad` | Traduit ; contrôle source/ROM automatisé | `0x1a3976c` | 93 | 175 px |
| `0x165d90b` | Traduit ; contrôle source/ROM automatisé | `0x1a39790` | 86 | 159 px |
| `0x165d95b` | Traduit ; contrôle source/ROM automatisé | `0x1a397b4` | 90 | 176 px |
| `0x165d9ac` | Traduit ; contrôle source/ROM automatisé | `0x1a397d8` | 90 | 189 px |
| `0x165da0f` | Traduit ; contrôle source/ROM automatisé | `0x1a397fc` | 80 | 151 px |
| `0x165da5e` | Traduit ; contrôle source/ROM automatisé | `0x1a39820` | 89 | 181 px |
| `0x165daba` | Traduit ; contrôle source/ROM automatisé | `0x1a39844` | 90 | 179 px |
| `0x165db0c` | Traduit ; contrôle source/ROM automatisé | `0x1a39868` | 88 | 171 px |
| `0x165db60` | Traduit ; contrôle source/ROM automatisé | `0x1a3988c` | 89 | 189 px |
| `0x165dbc0` | Traduit ; contrôle source/ROM automatisé | `0x1a398b0` | 91 | 176 px |
| `0x165dc13` | Traduit ; contrôle source/ROM automatisé | `0x1a398d4` | 84 | 161 px |
| `0x165dc69` | Traduit ; contrôle source/ROM automatisé | `0x1a398f8` | 95 | 184 px |
| `0x165dccb` | Traduit ; contrôle source/ROM automatisé | `0x1a3991c` | 86 | 166 px |
| `0x165dd29` | Traduit ; contrôle source/ROM automatisé | `0x1a39940` | 88 | 169 px |
| `0x165dd7c` | Traduit ; contrôle source/ROM automatisé | `0x1a39964` | 94 | 177 px |
| `0x165ddce` | Traduit ; contrôle source/ROM automatisé | `0x1a39988` | 99 | 183 px |
| `0x165de2f` | Traduit ; contrôle source/ROM automatisé | `0x1a399ac` | 82 | 165 px |
| `0x165de84` | Traduit ; contrôle source/ROM automatisé | `0x1a399d0` | 104 | 197 px |
| `0x165dee1` | Traduit ; contrôle source/ROM automatisé | `0x1a399f4` | 83 | 152 px |
| `0x165df3e` | Traduit ; contrôle source/ROM automatisé | `0x1a39a18` | 72 | 144 px |
| `0x165df9e` | Traduit ; contrôle source/ROM automatisé | `0x1a39a3c` | 91 | 185 px |
| `0x165e001` | Traduit ; contrôle source/ROM automatisé | `0x1a39a60` | 94 | 185 px |
| `0x165e05b` | Traduit ; contrôle source/ROM automatisé | `0x1a39a84` | 95 | 188 px |
| `0x165e0b8` | Traduit ; contrôle source/ROM automatisé | `0x1a39aa8` | 85 | 170 px |
| `0x165e110` | Traduit ; contrôle source/ROM automatisé | `0x1a39acc` | 69 | 213 px |
| `0x165e15d` | Traduit ; contrôle source/ROM automatisé | `0x1a39af0` | 72 | 202 px |
| `0x165e1a7` | Traduit ; contrôle source/ROM automatisé | `0x1a39b14` | 101 | 206 px |
| `0x165e209` | Traduit ; contrôle source/ROM automatisé | `0x1a39b38` | 94 | 173 px |
| `0x165e267` | Traduit ; contrôle source/ROM automatisé | `0x1a39b5c` | 87 | 179 px |
| `0x165e2d0` | Traduit ; contrôle source/ROM automatisé | `0x1a39b80` | 90 | 182 px |
| `0x165e329` | Traduit ; contrôle source/ROM automatisé | `0x1a39ba4` | 97 | 196 px |
| `0x165e38c` | Traduit ; contrôle source/ROM automatisé | `0x1a39bc8` | 87 | 168 px |
| `0x165e3e1` | Traduit ; contrôle source/ROM automatisé | `0x1a39bec` | 89 | 169 px |
| `0x165e43d` | Traduit ; contrôle source/ROM automatisé | `0x1a39c10` | 97 | 191 px |
| `0x165e4a0` | Traduit ; contrôle source/ROM automatisé | `0x1a39c34` | 73 | 142 px |
| `0x165e4f2` | Traduit ; contrôle source/ROM automatisé | `0x1a39c58` | 89 | 166 px |
| `0x165e554` | Traduit ; contrôle source/ROM automatisé | `0x1a39c7c` | 83 | 162 px |
| `0x165e5b3` | Traduit ; contrôle source/ROM automatisé | `0x1a39ca0` | 92 | 188 px |
| `0x165e61a` | Traduit ; contrôle source/ROM automatisé | `0x1a39cc4` | 55 | 155 px |
| `0x165e667` | Traduit ; contrôle source/ROM automatisé | `0x1a39ce8` | 88 | 188 px |
| `0x165e6c2` | Traduit ; contrôle source/ROM automatisé | `0x1a39d0c` | 87 | 190 px |
| `0x165e720` | Traduit ; contrôle source/ROM automatisé | `0x1a39d30` | 77 | 148 px |
| `0x165e775` | Traduit ; contrôle source/ROM automatisé | `0x1a39d54` | 74 | 161 px |
| `0x165e7d8` | Traduit ; contrôle source/ROM automatisé | `0x1a39d78` | 89 | 163 px |
| `0x165e838` | Traduit ; contrôle source/ROM automatisé | `0x1a39d9c` | 89 | 183 px |
| `0x165e899` | Traduit ; contrôle source/ROM automatisé | `0x1a39dc0` | 87 | 176 px |
| `0x165e8f9` | Traduit ; contrôle source/ROM automatisé | `0x1a39de4` | 80 | 155 px |
| `0x165e957` | Traduit ; contrôle source/ROM automatisé | `0x1a39e08` | 95 | 191 px |
| `0x165e9c1` | Traduit ; contrôle source/ROM automatisé | `0x1a39e2c` | 76 | 150 px |
| `0x165ea0d` | Traduit ; contrôle source/ROM automatisé | `0x1a39e50` | 81 | 160 px |
| `0x165ea71` | Traduit ; contrôle source/ROM automatisé | `0x1a39e74` | 64 | 174 px |
| `0x165eab9` | Traduit ; contrôle source/ROM automatisé | `0x1a39e98` | 85 | 172 px |
| `0x165eb20` | Traduit ; contrôle source/ROM automatisé | `0x1a39ebc` | 90 | 175 px |
| `0x165eb86` | Traduit ; contrôle source/ROM automatisé | `0x1a39ee0` | 88 | 179 px |
| `0x165ebdf` | Traduit ; contrôle source/ROM automatisé | `0x1a39f04` | 89 | 177 px |
| `0x165ec47` | Traduit ; contrôle source/ROM automatisé | `0x1a39f28` | 77 | 149 px |
| `0x165ec98` | Traduit ; contrôle source/ROM automatisé | `0x1a39f4c` | 82 | 156 px |
| `0x165ecf3` | Traduit ; contrôle source/ROM automatisé | `0x1a39f70` | 91 | 178 px |
| `0x165ed54` | Traduit ; contrôle source/ROM automatisé | `0x1a39f94` | 82 | 165 px |
| `0x165edb5` | Traduit ; contrôle source/ROM automatisé | `0x1a39fb8` | 99 | 194 px |
| `0x165ee1a` | Traduit ; contrôle source/ROM automatisé | `0x1a39fdc` | 80 | 158 px |
| `0x165ee6c` | Traduit ; contrôle source/ROM automatisé | `0x1a3a000` | 78 | 154 px |
| `0x165eebd` | Traduit ; contrôle source/ROM automatisé | `0x1a3a024` | 79 | 157 px |
| `0x165ef0e` | Traduit ; contrôle source/ROM automatisé | `0x1a3a048` | 83 | 163 px |
| `0x165ef72` | Traduit ; contrôle source/ROM automatisé | `0x1a3a06c` | 94 | 181 px |
| `0x165efd1` | Traduit ; contrôle source/ROM automatisé | `0x1a3a090` | 77 | 154 px |
| `0x165f031` | Traduit ; contrôle source/ROM automatisé | `0x1a3a0b4` | 74 | 157 px |
| `0x165f08a` | Traduit ; contrôle source/ROM automatisé | `0x1a3a0d8` | 93 | 199 px |
| `0x165f0f0` | Traduit ; contrôle source/ROM automatisé | `0x1a3a0fc` | 64 | 133 px |
| `0x165f144` | Traduit ; contrôle source/ROM automatisé | `0x1a3a120` | 88 | 173 px |
| `0x165f1a1` | Traduit ; contrôle source/ROM automatisé | `0x1a3a144` | 92 | 174 px |
| `0x165f202` | Traduit ; contrôle source/ROM automatisé | `0x1a3a168` | 95 | 185 px |
| `0x165f261` | Traduit ; contrôle source/ROM automatisé | `0x1a3a18c` | 84 | 180 px |
| `0x165f2b6` | Traduit ; contrôle source/ROM automatisé | `0x1a3a1b0` | 85 | 164 px |
| `0x165f316` | Traduit ; contrôle source/ROM automatisé | `0x1a3a1d4` | 94 | 183 px |
| `0x165f36f` | Traduit ; contrôle source/ROM automatisé | `0x1a3a1f8` | 72 | 197 px |
| `0x165f3b8` | Traduit ; contrôle source/ROM automatisé | `0x1a3a21c` | 94 | 189 px |
| `0x165f421` | Traduit ; contrôle source/ROM automatisé | `0x1a3a240` | 86 | 180 px |
| `0x165f474` | Traduit ; contrôle source/ROM automatisé | `0x1a3a264` | 94 | 182 px |
| `0x165f4de` | Traduit ; contrôle source/ROM automatisé | `0x1a3a288` | 84 | 163 px |
| `0x165f53c` | Traduit ; contrôle source/ROM automatisé | `0x1a3a2ac` | 94 | 191 px |
| `0x165f5a1` | Traduit ; contrôle source/ROM automatisé | `0x1a3a2d0` | 78 | 154 px |
| `0x165f5f5` | Traduit ; contrôle source/ROM automatisé | `0x1a3a2f4` | 86 | 176 px |
| `0x165f651` | Traduit ; contrôle source/ROM automatisé | `0x1a3a318` | 72 | 149 px |
| `0x165f6a6` | Traduit ; contrôle source/ROM automatisé | `0x1a3a33c` | 79 | 160 px |
| `0x165f6fa` | Traduit ; contrôle source/ROM automatisé | `0x1a3a360` | 93 | 189 px |
| `0x165f759` | Traduit ; contrôle source/ROM automatisé | `0x1a3a384` | 91 | 175 px |
| `0x165f7b8` | Traduit ; contrôle source/ROM automatisé | `0x1a3a3a8` | 85 | 171 px |
| `0x165f81d` | Traduit ; contrôle source/ROM automatisé | `0x1a3a3cc` | 85 | 168 px |
| `0x165f883` | Traduit ; contrôle source/ROM automatisé | `0x1a3a3f0` | 90 | 182 px |
| `0x165f8e3` | Traduit ; contrôle source/ROM automatisé | `0x1a3a414` | 55 | 163 px |
| `0x165f91c` | Traduit ; contrôle source/ROM automatisé | `0x1a3a438` | 99 | 191 px |
| `0x165f97c` | Traduit ; contrôle source/ROM automatisé | `0x1a3a45c` | 96 | 184 px |
| `0x165f9de` | Traduit ; contrôle source/ROM automatisé | `0x1a3a480` | 82 | 154 px |
| `0x165fa3c` | Traduit ; contrôle source/ROM automatisé | `0x1a3a4a4` | 84 | 166 px |
| `0x165faa5` | Traduit ; contrôle source/ROM automatisé | `0x1a3a4c8` | 102 | 194 px |
| `0x165fb0d` | Traduit ; contrôle source/ROM automatisé | `0x1a3a4ec` | 86 | 171 px |
| `0x165fb72` | Traduit ; contrôle source/ROM automatisé | `0x1a3a510` | 76 | 154 px |
| `0x165fbdb` | Traduit ; contrôle source/ROM automatisé | `0x1a3a534` | 89 | 177 px |
| `0x165fc39` | Traduit ; contrôle source/ROM automatisé | `0x1a3a558` | 93 | 184 px |
| `0x165fc98` | Traduit ; contrôle source/ROM automatisé | `0x1a3a57c` | 89 | 181 px |
| `0x165fcfa` | Traduit ; contrôle source/ROM automatisé | `0x1a3a5a0` | 90 | 179 px |
| `0x165fd57` | Traduit ; contrôle source/ROM automatisé | `0x1a3a5c4` | 88 | 168 px |
| `0x165fdbc` | Traduit ; contrôle source/ROM automatisé | `0x1a3a5e8` | 94 | 186 px |
| `0x165fe23` | Traduit ; contrôle source/ROM automatisé | `0x1a3a60c` | 83 | 164 px |
| `0x165fe7e` | Traduit ; contrôle source/ROM automatisé | `0x1a3a630` | 83 | 157 px |
| `0x165fed6` | Traduit ; contrôle source/ROM automatisé | `0x1a3a654` | 89 | 182 px |
| `0x165ff31` | Traduit ; contrôle source/ROM automatisé | `0x1a3a678` | 66 | 125 px |
| `0x165ff8f` | Traduit ; contrôle source/ROM automatisé | `0x1a3a69c` | 79 | 148 px |
| `0x165ffef` | Traduit ; contrôle source/ROM automatisé | `0x1a3a6c0` | 91 | 175 px |
| `0x1660052` | Traduit ; contrôle source/ROM automatisé | `0x1a3a6e4` | 65 | 183 px |
| `0x166009a` | Traduit ; contrôle source/ROM automatisé | `0x1a3a708` | 99 | 201 px |
| `0x1660100` | Traduit ; contrôle source/ROM automatisé | `0x1a3a72c` | 70 | 198 px |
| `0x166014c` | Traduit ; contrôle source/ROM automatisé | `0x1a3a750` | 94 | 192 px |
| `0x16601a9` | Traduit ; contrôle source/ROM automatisé | `0x1a3a774` | 86 | 159 px |
| `0x16601f8` | Traduit ; contrôle source/ROM automatisé | `0x1a3a798` | 65 | 137 px |
| `0x1660251` | Traduit ; contrôle source/ROM automatisé | `0x1a3a7bc` | 91 | 185 px |

## Validation

Les résultats des commandes et la preuve Playwright sont consignés dans le bilan du ticket. La sonde Playwright réutilise les pointeurs finaux dans une boîte native mGBA et contrôle par OCR les deux premières lignes de deux descriptions. Les trois lignes et les 182 consommateurs sont contrôlés par les tests binaires. La sonde ne revendique pas une navigation complète des 182 fiches Pokédex.
