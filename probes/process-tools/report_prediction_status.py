from pathlib import Path
from datetime import date
import csv
from collections import Counter

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
SRC=ROOT/"datasets"/"aeig-prediction-log.csv"
OUT=ROOT/"docs"/"reference"/"prediction-status.md"
with SRC.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
mode=Counter(r["mode"] for r in rows)
status=Counter(r["status"] for r in rows)
pros=[r for r in rows if r["mode"]=="prospective"]
confirmed=[r for r in pros if r["status"]=="confirmed"]
locked=[r for r in pros if r["locked_before_run"].lower()=="true"]
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---","# Prediction Status","",
       f"Predictions: **{len(rows)}**. Prospective: **{len(pros)}**; locked before run: **{len(locked)}/{len(pros)}**; prospectively confirmed: **{len(confirmed)}**.","",
       f"Modes: `{dict(mode)}`. Statuses: `{dict(status)}`.","",
       "| ID | Mode | Domain | Experiment | Status | Prediction |","|---|---|---|---|---|---|"]
for r in rows:
    pred=r["prediction"].replace("|","/")
    lines.append(f"| `{r['prediction_id']}` | {r['mode']} | `{r['domain']}` | `{r['source_experiment']}` | **{r['status']}** | {pred} |")
lines += ["","## Release rule","AEIG 1.0 requires the prospective predictions to be frozen before observation, at least three prospectively confirmed predictions, and no unresolved `pending`, `inconclusive`, or unknown result from the canonical L5 operator run. A refutation is acceptable only after the affected model is explicitly revised and the row is marked `refuted-revised`."]
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("predictions",len(rows),"prospective",len(pros),"locked",len(locked),"confirmed_prospective",len(confirmed),"status",dict(status))
print("wrote",OUT)
