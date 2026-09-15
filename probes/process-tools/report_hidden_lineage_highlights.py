from __future__ import annotations
import csv
from pathlib import Path
REPO=Path(r"D:\Developer\After Effects Internals Guide")
rows=list(csv.DictReader((REPO/"datasets"/"ae-debug-trace-lineage.csv").open(encoding="utf-8")))
patterns=["BEE","RG","TDB","Guid","WorkQueue","MFR","Multithread","UXP","MediaCore","MemoryControl","FastMask","Roto","Sparse Tracker","Compute"]
for pat in patterns:
    xs=[r for r in rows if r["channel"]=="stable" and pat.lower() in r["name"].lower()]
    print("\n##",pat,len(xs))
    for r in xs[:50]:
        print(r["kind"],r["name"],"|",r["first_seen"],"->",r["last_seen"],"n",r["version_count"])
