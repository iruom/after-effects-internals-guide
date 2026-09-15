from pathlib import Path
import re,csv
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
SOURCES={
 'cs6':ROOT/'research/external-sources/ae-sdk-cs6/Headers/AE_Effect.h',
 'cc2014':ROOT/'research/external-sources/ae-sdk-cc2014/Headers/AE_Effect.h',
 'sdk25.6':Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers\AE_Effect.h"),
}
rx=re.compile(r'^\s*#define\s+PF_AE(\d+)_PLUG_IN_(VERSION|SUBVERS)\s+([0-9]+)\s*(?://\s*(.*))?$',re.M)
def release(code):
    if code=='1101': return '11.0.1'
    if len(code)==2: return f'{int(code[0])}.{int(code[1])}'
    if len(code)==3: return f'{int(code[:-1])}.{int(code[-1])}'
    return code
parsed={}; comments={}
for key,p in SOURCES.items():
    text=p.read_text(encoding='utf-8-sig',errors='replace'); d={}
    for m in rx.finditer(text):
        code,kind,val,comment=m.groups(); d.setdefault(code,{})[kind]=int(val)
        if comment: comments[(key,code,kind)]=comment.strip()
    parsed[key]=d
codes=sorted(set().union(*(d.keys() for d in parsed.values())), key=lambda x:(float(release(x)) if x!='1101' else 11.001))
rows=[]
for c in codes:
    cur=parsed['sdk25.6'].get(c,{})
    rows.append([c,release(c),cur.get('VERSION',''),cur.get('SUBVERS',''),c in parsed['cs6'],c in parsed['cc2014'],c in parsed['sdk25.6'],comments.get(('sdk25.6',c,'VERSION'),''),comments.get(('sdk25.6',c,'SUBVERS'),'')])
out=ROOT/'datasets/ae-pf-api-version-lineage.csv'
with out.open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['macro_code','release','api_version','api_subversion','present_cs6','present_cc2014','present_sdk25_6','version_comment','subversion_comment']); w.writerows(rows)
print('rows',len(rows),'current latest',rows[-1]); print('releases',[r[1] for r in rows])
