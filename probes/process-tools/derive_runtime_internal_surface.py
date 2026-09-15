from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path

REPO=Path(r"D:\Developer\After Effects Internals Guide")
SRC=REPO/"datasets"/"ae-2025-runtime-export-atlas.csv"
OUT=REPO/"datasets"/"ae-2025-runtime-internal-surface.csv"
CORE={"bee","tdb","rg","aegp","aeio","pf","txt","om","cor","agm"}
rows=[]
with SRC.open(encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["category"] in CORE:
            rows.append(r)
rows.sort(key=lambda r:(r["category"],r["module"].lower(),r["symbol"]))
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
counts=Counter(r["category"] for r in rows)
print("wrote",OUT,"rows",len(rows))
for k,v in sorted(counts.items()): print(k,v)
