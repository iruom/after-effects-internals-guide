from __future__ import annotations
import argparse, csv, re
from pathlib import Path

EXTS={'.h','.hpp','.c','.cpp','.r','.rc','.py','.cl','.cu','.chlsl'}
KW={'internal':8,'private':7,'deprecated':7,'obsolete':6,'legacy':5,'frozen':6,'confusing':9,'workaround':8,'race':8,'deadlock':9,'thread safe':6,'not thread safe':9,'cache':4,'guid':6,'receipt':7,'render state':7,'flatten':6,'unflatten':7,'async':4,'speculative':7,'invalidate':6,'timestamp':5,'dependency':5,'must not':6,'do not':4,'todo':5,'fixme':6}
SUITE=re.compile(r'\b(?:k[A-Za-z0-9_]*Suite[A-Za-z0-9_]*|[A-Za-z0-9_]*Suite(?:Version)?\d*)\b')
FLAG=re.compile(r'\b(?:PF_OutFlag2?_[A-Za-z0-9_]+|PF_Cmd_[A-Za-z0-9_]+|AEGP_[A-Za-z0-9_]+|PrSDK[A-Za-z0-9_]+)\b')
COMMENT_LINE=re.compile(r'^\s*(?://|/\*|\*|\*\*)\s?(.*)')

def read_text(p):
    for enc in ('utf-8-sig','utf-8','cp1252','cp932'):
        try: return p.read_text(encoding=enc)
        except UnicodeDecodeError: pass
    return p.read_text(encoding='utf-8', errors='replace')

def mine(root):
    files=[]; comments=[]; usages=[]
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in EXTS: continue
        text=read_text(p); rel=str(p.relative_to(root)); lines=text.splitlines()
        score=0; suites=set(); flags=set(); ch=[]
        for no,line in enumerate(lines,1):
            suites.update(SUITE.findall(line)); flags.update(FLAG.findall(line))
            m=COMMENT_LINE.match(line)
            if not m: continue
            body=m.group(1).strip(); low=body.lower()
            s=sum(w for k,w in KW.items() if k in low)
            if s: score+=s; ch.append((s,no,body[:700]))
        files.append({'path':rel,'lines':len(lines),'comment_score':score,
                      'suite_count':len(suites),'flag_count':len(flags),
                      'internal_count':text.count('INTERNAL')+text.count('_Private.h')})
        for s,no,body in sorted(ch,reverse=True):
            comments.append({'path':rel,'line':no,'score':s,'text':body})
        for x in sorted(suites): usages.append({'path':rel,'kind':'suite','symbol':x})
        for x in sorted(flags): usages.append({'path':rel,'kind':'api','symbol':x})
    return files,comments,usages

def research_score(x):
    raw=x['comment_score']+x['internal_count']*10+x['suite_count']*2+x['flag_count']
    return raw/max(1,x['lines']**0.55)

def write(root,out,label):
    files,comments,usages=mine(root); out.mkdir(parents=True,exist_ok=True)
    files.sort(key=research_score,reverse=True)
    tables=[('deep_file_scores.csv',files,list(files[0])),
            ('developer_comment_leads.csv',comments,list(comments[0])),
            ('api_usage.csv',usages,list(usages[0]))]
    for name,rows,fields in tables:
        with (out/name).open('w',newline='',encoding='utf-8-sig') as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    md=[f'# {label} Deep Mining Queue','',f'- Files: {len(files)}',
        f'- Scored developer-comment leads: {len(comments)}',
        f'- API/Suite usage records: {len(usages)}','',
        '## Top research targets','']
    for x in files[:50]:
        md.append(f"- score {research_score(x):7.2f} | comment {x['comment_score']:4d} | "
                  f"internal {x['internal_count']:3d} | suites {x['suite_count']:3d} | "
                  f"flags {x['flag_count']:3d} | {x['lines']:5d} lines | `{x['path']}`")
    md += ['', '## Highest-scoring developer comments', '']
    for x in sorted(comments,key=lambda y:y['score'],reverse=True)[:100]:
        md.append(f"- {x['score']:2d} | `{x['path']}:{x['line']}` | {x['text']}")
    (out/'deep_research_queue.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(label, 'files',len(files),'comments',len(comments),'usage',len(usages))
    for x in files[:12]: print(f"{research_score(x):7.2f} {x['path']}")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',required=True)
    ap.add_argument('--out',required=True); ap.add_argument('--label',required=True)
    a=ap.parse_args(); write(Path(a.root),Path(a.out),a.label)

if __name__=='__main__': main()
