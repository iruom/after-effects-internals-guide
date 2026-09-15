from pathlib import Path
import csv
from collections import Counter
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
SRC=ROOT/"datasets"/"ae-api-surface-deltas.csv"
OUT=ROOT/"datasets"/"ae-sdk-lineage-cs6-cc2014-25_6.csv"
STATUS=ROOT/"docs"/"reference"/"sdk-lineage-status.md"
with SRC.open(encoding="utf-8",newline="") as f: src=list(csv.DictReader(f))

def b(r,k): return r.get(k)=="True"
def klass(c6,c14,c25):
    table={(1,1,1):"stable-cs6-through-25.6",(0,1,1):"introduced-by-cc2014-retained",
           (0,1,0):"cc2014-only-transient",(1,1,0):"removed-after-cc2014",
           (1,0,0):"cs6-only",(0,0,1):"introduced-after-cc2014",
           (1,0,1):"absent-cc2014-reappeared",(0,0,0):"outside-three-sdk-corpora"}
    return table[(int(c6),int(c14),int(c25))]
rows=[]
for r in src:
    c6=b(r,"in_cs6_raw"); c14=b(r,"in_cc2014_raw"); c25=b(r,"in_sdk_25_6_raw")
    rows.append({"symbol":r["symbol"],"cs6_raw":c6,"cc2014_raw":c14,"sdk_25_6_raw":c25,
                 "guide_26_5":b(r,"in_guide_26_5"),"lineage_class":klass(c6,c14,c25)})
fields=list(rows[0])
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
counts=Counter(r["lineage_class"] for r in rows)
lines=["---","status: generated","last_verified: 2026-09-15","---","# SDK Lineage Status","",
       "Three-point raw-token lineage across CS6/11.0, CC2014/13.0 and distributed SDK 25.6.","",
       "| Presence class | Identifiers |","|---|---:|"]
for k,v in sorted(counts.items()): lines.append(f"| `{k}` | {v} |")
lines += ["","Presence continuity is not ABI-equivalence proof; struct layout, selector integers and semantics still require per-suite/version evidence."]
STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("rows",len(rows),"classes",dict(sorted(counts.items())))
print("wrote",OUT); print("wrote",STATUS)