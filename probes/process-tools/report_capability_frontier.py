from pathlib import Path
import csv
from collections import Counter
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
SRC=ROOT/"datasets"/"ae-plugin-capability-frontier.csv"
OUT=ROOT/"docs"/"reference"/"capability-frontier-status.md"
with SRC.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
status=Counter(r["status"] for r in rows); risk=Counter(r["risk"] for r in rows); maturity=Counter(r["maturity"] for r in rows)
lines=["---","status: generated","last_verified: 2026-09-15","---","# Capability Frontier Status","",f"Tracked capabilities: **{len(rows)}**.","","## By status","","| Status | Count |","|---|---:|"]
for k,v in sorted(status.items()): lines.append(f"| `{k}` | {v} |")
lines += ["","## By maturity","","| Maturity | Count |","|---|---:|"]
for k,v in sorted(maturity.items()): lines.append(f"| `{k}` | {v} |")
lines += ["","## By risk","","| Risk | Count |","|---|---:|"]
for k,v in sorted(risk.items()): lines.append(f"| `{k}` | {v} |")
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print('capabilities',len(rows),'status',dict(status),'risk',dict(risk),'maturity',dict(maturity))
print('wrote',OUT)
