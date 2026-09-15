from __future__ import annotations
import csv, html, re, urllib.request
from pathlib import Path

REPO=Path(r"D:\Developer\After Effects Internals Guide")
OUT=REPO/"datasets"/"ae-script-expression-api-atlas.csv"
SOURCES=[
 ("scripting-docs","https://ae-scripting.docsforadobe.dev/print_page/","community-maintained-adobe-derived"),
 ("expression-docs","https://ae-expressions.docsforadobe.dev/print_page/","community-maintained-adobe-derived"),
]
GENERIC={"description","parameters","returns","return","type","example","examples","methods","method","attributes","attribute","objects","object","page contents","introduction","general","resources","note","notes","warning","warnings","properties","property"}
HEAD_RE=re.compile(r"<h([1-6])[^>]*>(.*?)</h[1-6]>",re.S|re.I)
TAG_RE=re.compile(r"<[^>]+>")
API_RE=re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)*(?:\([^)]*\))?$")

def clean(x:str)->str:
    x=html.unescape(TAG_RE.sub("",x)).strip().replace("¶","").replace("�","")
    return re.sub(r"\s+"," ",x).strip()
def scan(surface,url,evidence):
    raw=urllib.request.urlopen(url,timeout=30).read().decode("utf-8","replace")
    stack=[""]*7; rows=[]
    for m in HEAD_RE.finditer(raw):
        level=int(m.group(1)); title=clean(m.group(2))
        if not title: continue
        stack[level]=title
        for i in range(level+1,7): stack[i]=""
        low=title.lower().rstrip(":")
        is_api=bool(API_RE.fullmatch(title)) and low not in GENERIC
        if not is_api: continue
        ancestors=[stack[i] for i in range(level-1,0,-1) if stack[i] and stack[i].lower().rstrip(":") not in GENERIC]
        container=ancestors[0] if ancestors else ""
        kind="method" if "(" in title else "member-or-class"
        rows.append(dict(surface=surface,evidence=evidence,source=url,heading_level=level,
                         container=container,kind=kind,symbol=title))
    return rows

def main():
    rows=[]
    for surface,url,evidence in SOURCES: rows.extend(scan(surface,url,evidence))
    uniq={tuple(r.values()):r for r in rows}
    rows=sorted(uniq.values(),key=lambda r:(r["surface"],r["container"],r["symbol"]))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    for surface,_,_ in SOURCES:
        sub=[r for r in rows if r["surface"]==surface]
        print(surface,len(sub),"unique scoped API headings")
    print("wrote",OUT,"rows",len(rows))

if __name__=="__main__": main()
