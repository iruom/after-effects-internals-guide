from __future__ import annotations
import csv,re
from pathlib import Path

REPO=Path(r"D:\Developer\After Effects Internals Guide")
ROOT=Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
OUT=REPO/"datasets"/"ae-sdk-25.6-private-gates.csv"
GATES=("AEGP_INTERNAL","AE_INTERNAL","PF_INTERNAL")
rows=[]
for p in sorted(ROOT.glob("*.h")):
    text=p.read_text(encoding="utf-8",errors="ignore")
    lines=text.splitlines()
    for n,line in enumerate(lines,1):
        if not any(g in line for g in GATES):
            continue
        gate=next(g for g in GATES if g in line)
        window="\n".join(lines[n-1:min(len(lines),n+18)])
        includes=re.findall(r'#\s*include\s*[<"]([^>"]+)[>"]',window)
        opaque=re.findall(r'typedef\s+(?:const\s+)?struct\s+(_?[A-Za-z_]\w*)\s*\*{1,2}\s*([A-Za-z_]\w*)',window)
        rows.append(dict(header=p.name,line=n,gate=gate,directive=line.strip(),
                         private_includes="|".join(includes),opaque_public_types="|".join(f"{a}->{b}" for a,b in opaque),
                         context=" ".join(x.strip() for x in window.splitlines() if x.strip())[:1600]))
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("wrote",OUT,"rows",len(rows))
for r in rows: print(r['header'],r['line'],r['gate'],r['private_includes'],r['opaque_public_types'])
