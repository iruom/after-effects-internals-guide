from __future__ import annotations
import csv,re
from collections import defaultdict
from pathlib import Path

REPO=Path(r"D:\Developer\After Effects Internals Guide")
ADOBE=Path.home()/"AppData"/"Roaming"/"Adobe"
OUT=REPO/"datasets"/"ae-debug-trace-vocabulary.csv"
LINEAGE=REPO/"datasets"/"ae-debug-trace-lineage.csv"
STATUS=REPO/"docs"/"reference"/"debug-trace-lineage-status.md"
ROOTS=[("stable",ADOBE/"After Effects"),("beta",ADOBE/"After Effects (Beta)")]

def version_tuple(label:str):
    m=re.match(r"(\d+)(?:\.(\d+))?",label)
    return (int(m.group(1)),int(m.group(2) or 0)) if m else (-1,-1)

def clean_line(s:str)->str:
    return s.strip("\ufeff\r\n")
rows=[]
for channel,root in ROOTS:
    if not root.exists():
        continue
    for vdir in sorted((p for p in root.iterdir() if p.is_dir()),key=lambda p:version_tuple(p.name)):
        ver=version_tuple(vdir.name)
        for fname,kind in (("Debug Database.txt","debug-key"),("Trace Database.txt","trace-category")):
            p=vdir/fname
            if not p.exists():
                continue
            text=p.read_text(encoding="utf-8",errors="replace")
            for line_no,line in enumerate(text.splitlines(),1):
                line=clean_line(line)
                if not line.strip():
                    continue
                parts=line.split("\t")
                name=parts[0].strip()
                if not name:
                    continue
                value=parts[1].strip() if len(parts)>1 else ""
                default=parts[2].strip() if len(parts)>2 else ""
                rows.append(dict(channel=channel,version_dir=vdir.name,version_major=ver[0],version_minor=ver[1],
                                 kind=kind,name=name,value=value,default=default,line=line_no,
                                 source=str(p)))
rows.sort(key=lambda r:(r["kind"],r["name"].lower(),r["channel"],int(r["version_major"]),int(r["version_minor"]),r["version_dir"]))
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
groups=defaultdict(list)
for r in rows:
    groups[(r["channel"],r["kind"],r["name"])].append(r)
lineage=[]
for (channel,kind,name),rs in groups.items():
    rs=sorted(rs,key=lambda r:(int(r["version_major"]),int(r["version_minor"]),r["version_dir"]))
    versions=[]; values=[]
    for r in rs:
        tag=r["version_dir"]
        if tag not in versions: versions.append(tag)
        vd=f"{r['value']}|{r['default']}"
        if vd not in values: values.append(vd)
    lineage.append(dict(channel=channel,kind=kind,name=name,first_seen=versions[0],last_seen=versions[-1],
                        version_count=len(versions),value_default_variant_count=len(values),
                        versions="|".join(versions),value_default_variants=" || ".join(values[:20])))
lineage.sort(key=lambda r:(r["kind"],r["name"].lower(),r["channel"]))
with LINEAGE.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(lineage[0])); w.writeheader(); w.writerows(lineage)

stable_debug=[r for r in lineage if r["channel"]=="stable" and r["kind"]=="debug-key"]
stable_trace=[r for r in lineage if r["channel"]=="stable" and r["kind"]=="trace-category"]
versions=sorted({r["version_dir"] for r in rows if r["channel"]=="stable"},key=version_tuple)
lines=["---","status: generated","last_verified: 2026-09-15","---","# Debug / Trace Lineage Status","",
       f"Stable AE version/profile directories scanned: **{len(versions)}** (`{'`, `'.join(versions)}`).",
       f"Raw vocabulary rows: **{len(rows)}**.",
       f"Stable unique debug keys: **{len(stable_debug)}**.",
       f"Stable unique trace categories: **{len(stable_trace)}**.","",
       "The databases are implementation/diagnostic vocabulary, not supported configuration APIs. A key/category name proves an instrumented concept exists; behavior must be established independently.","",
       "## Long-lived examples",""
]
long_debug=sorted(stable_debug,key=lambda r:(-int(r["version_count"]),r["name"]))[:30]
for r in long_debug: lines.append(f"- `{r['name']}` — {r['first_seen']} -> {r['last_seen']} ({r['version_count']} profiles)")
STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("wrote",OUT,"rows",len(rows)); print("wrote",LINEAGE,"entries",len(lineage)); print("wrote",STATUS)
print("stable debug",len(stable_debug),"stable trace",len(stable_trace),"stable profiles",len(versions))
