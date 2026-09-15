import csv
from pathlib import Path
p=Path(r"D:\Developer\After Effects Internals Guide\datasets\aeig-domain-coverage.csv")
rows=list(csv.DictReader(p.open(encoding="utf-8-sig")))
for r in rows:
    if r["domain"]=="gpu":
        r["current_level"]="L3"
        r["next_evidence"]="CPU/GPU parity fixture; queue/fence completion timing; cache identity correlation"
    if r["domain"]=="three-d":
        r["current_level"]="L3"
        r["next_evidence"]="resource-cache invalidation matrix; Advanced3D quality/camera/light/material runtime correlation"
with p.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print("updated",p)
