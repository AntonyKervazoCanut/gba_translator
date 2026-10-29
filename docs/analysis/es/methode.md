# Reproduction de l’instantané ES (A-663)

Ce programme d’analyse ne modifie aucun `combined`, aucune ROM et aucun descripteur.
Il produit uniquement les trois artefacts `docs/analysis/es/{inventaire.csv,lots.json,mesures.json}`.
Les sources doivent correspondre aux SHA-256 du rapport ; les lots publiés restent figés
même si les sources avancent. Exécuter depuis la racine, avec une ROM FR témoin présente
à `output/roms/GenedRom-fr.gba`. Copier le bloc dans un fichier temporaire puis lancer
`PYTHONPATH=. python3 /tmp/audit_es_a663.py`. Ne jamais recalculer les limites des lots
en filtrant les entrées déjà traitées.

```python
from pathlib import Path
from collections import Counter,defaultdict
import csv,hashlib,json,math,re
from scripts.audit_translation_coverage import parse_combined
from src.core.text_codec import TextEncoder
from src.core.fixed_tables import FIXED_TABLE_RANGES
root=Path.cwd(); out=root/'docs/analysis/es';out.mkdir(parents=True,exist_ok=True)
maps={c:parse_combined(root/f'languages/{c}/combined_{c}.txt') for c in ['en','es','fr']}
en,es,fr=[maps[c] for c in ['en','es','fr']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def domain(o):
 for a,b,d in FIXED_TABLE_RANGES:
  if a<=o<b:return {'engine text-printer font tables':'polices_non_textuelles','species names':'noms_especes','species info / Pokédex category':'categories_pokedex','attack names':'noms_attaques'}[d]
 if o<0x700000:return 'banques_basses_systeme_et_dialogues'
 if o<0x1000000:return 'banques_centrales_monde_et_interface'
 return 'banques_etendues_dialogues_et_donnees'
def encoded(t):return TextEncoder.encode_pokemon(t.replace('\\n','\n').replace('\\l','<0xFA>').replace('\\p','<0xFB>'))[:-1]
markers=re.compile(r'<0x(?:FC|FD|F8|F9|F7|FA|FB)>|\{[^}]+\}')
rows=[];groups=defaultdict(list)
for o in sorted(fr.keys()|es.keys()):
 e,s=en.get(o),es.get(o)
 state='absent_es' if s is None else 'identique_en' if s==e else 'different_en'
 flags=[]
 if s is not None and e is not None:
  if len(encoded(s))>len(encoded(e)):flags.append('plus_long_en_octets')
  if markers.findall(s)!=markers.findall(e):flags.append('marqueurs_differents_a_verifier')
  if len(encoded(s))>=512:flags.append('plafond_extraction_512')
 if s is not None and '<out-of-range>' in s:flags.append('hors_rom')
 if s is not None and re.search(r'YOSOYKIKE|traduciendo|Diciembre de\\n2024',s,re.I):flags.append('promotion_ou_date_ajoutee')
 if e is None:flags.append('absent_reference_en')
 row={'offset':f'0x{o:08X}','domaine':domain(o),'etat':state,'alertes':';'.join(flags),'octets_en':len(encoded(e)) if e is not None else '', 'octets_es':len(encoded(s)) if s is not None else '', 'en':e or '', 'es':s or '', 'fr':fr.get(o,''),'lot':''}
 rows.append(row)
 if domain(o)!='polices_non_textuelles':groups[domain(o)].append(row)
batches=[]
for d,items in sorted(groups.items()):
 n=math.ceil(len(items)/400)
 for i in range(n):
  chunk=items[len(items)*i//n:len(items)*(i+1)//n];bid=f'ES-{len(batches)+1:03d}'
  for r in chunk:r['lot']=bid
  batches.append({'id':bid,'domaine':d,'count':len(chunk),'first':chunk[0]['offset'],'last':chunk[-1]['offset'],'states':dict(Counter(r['etat'] for r in chunk)),'offsets':[r['offset'] for r in chunk]})
with (out/'inventaire.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'lots.json').write_text(json.dumps(batches,ensure_ascii=False,indent=2)+'\n')
metrics={'sources':{c:{'path':f'languages/{c}/combined_{c}.txt','sha256':sha(root/f'languages/{c}/combined_{c}.txt'),'offsets':len(m)} for c,m in maps.items()},'es_identique_en':sum(en.get(o)==s for o,s in es.items()),'fr_absent_es':[f'0x{o:08X}' for o in sorted(fr.keys()-es.keys())],'es_absent_fr':[f'0x{o:08X}' for o in sorted(es.keys()-fr.keys())],'en_absent_es':len(en.keys()-es.keys()),'etats':dict(Counter(r['etat'] for r in rows)),'alertes':dict(Counter(flag for r in rows for flag in r['alertes'].split(';') if flag)),'domaines':dict(Counter(r['domaine'] for r in rows)),'lots':len(batches),'entrees_lots':sum(b['count'] for b in batches),'taille_lots':[min(b['count'] for b in batches),max(b['count'] for b in batches)],'glyphes':{c:encoded(c).hex() for c in 'áéíóúüñÁÉÍÓÚÜÑ¡¿'},'rom_fr_temoin':{'path':'output/roms/GenedRom-fr.gba','sha256':sha(Path('output/roms/GenedRom-fr.gba'))},'artefacts':{p:sha(out/p) for p in ['inventaire.csv','lots.json']}}
(out/'mesures.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in metrics.items() if k not in ['fr_absent_es','es_absent_fr']},ensure_ascii=False,indent=2))
```
