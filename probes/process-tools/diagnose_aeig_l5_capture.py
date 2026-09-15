from pathlib import Path
import json

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
RUNS=ROOT/"experiments"/"observatory"/"runs"

EXPECTED={
 "EXP-CACHE-002":["receipt-matrix.tsv","fixture-script.log","fixture-output-A.avi","fixture-output-B.avi","environment.txt"],
 "EXP-PLUGIN-001":["suite-acquisition.tsv"],
 "EXP-RG-001":["host-trace.log","trace-control.tsv"],
 "EXP-SCRIPT-001":["runtime-reflection.tsv"],
}

rows=[]
for exp,names in EXPECTED.items():
    base=RUNS/exp
    for name in names:
        p=base/name
        rows.append((exp,name,p.exists(),p.stat().st_size if p.exists() else 0))

print("AEIG L5 capture diagnostics (read-only)")
for exp,name,exists,size in rows:
    print(f"{'OK' if exists else 'MISSING'}\t{exp}\t{name}\t{size}")

missing=[r for r in rows if not r[2]]
print(f"summary expected={len(rows)} present={len(rows)-len(missing)} missing={len(missing)}")
