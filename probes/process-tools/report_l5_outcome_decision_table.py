from pathlib import Path
import csv

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; DOC=ROOT/"docs"/"reference"/"l5-outcome-decision-table.md"
OUT=DATA/"aeig-l5-outcome-decision-table.csv"
with (DATA/"aeig-prediction-lock.csv").open(encoding="utf-8-sig",newline="") as f:
    preds=list(csv.DictReader(f))
meta={
"PRED-004":("EXP-CACHE-002/receipt-matrix.tsv","all CHECK rows follow k<n => INCOMPLETE; k>=n => VALID","any controlled CHECK violates prefix rule","revise Canvas receipt-prefix semantics"),
"PRED-005":("EXP-CACHE-002/receipt-matrix.tsv","A/B matrices preserve the same prefix rule","mutation changes the abstract prefix rule","separate state mutation from receipt sufficiency model"),
"PRED-006":("EXP-RG-001/host-trace.log","RG target categories occur inside render window","successful render has no RG target trace","revise trace/provider assumptions or render-path model"),
"PRED-007":("EXP-RG-001/host-trace.log","identity/eval footprint changes after Blur mutation","confirmed mutation yields indistinguishable identity footprint","revise state-to-identity propagation model"),
"PRED-008":("EXP-RG-001/host-trace.log","RG/cache/work-queue footprint changes after mutation","confirmed mutation yields indistinguishable RG/cache footprint","revise invalidation/materialization model"),
"PRED-009":("EXP-PLUGIN-001/suite-acquisition.tsv","families exhibit different accepted selector sets","all 48 families share one global selector sequence","revise suite-scoped selector model"),
"PRED-010":("EXP-PLUGIN-001/suite-acquisition.tsv","runtime matrix cannot collapse to one latest-table alias","all families show universal latest-table behavior","revise exact-version dispatch requirement"),
}
rows=[]
for p in preds:
    raw,confirm,refute,revision=meta[p["prediction_id"]]
    rows.append({"prediction_id":p["prediction_id"],"domain":p["domain"],"raw_evidence":raw,
                 "confirm_if":confirm,"refute_if":refute,"inconclusive_if":"capture incomplete or evidence lacks discriminating detail",
                 "model_revision_if_refuted":revision})
fields=list(rows[0])
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
lines=["---","status: generated","last_verified: 2026-09-15","---","# L5 Outcome Decision Table","",
       "These criteria are derived from the immutable prediction lock before the operator run. They define how outcomes affect the model without changing the locked prediction text.","",
       "| Prediction | Domain | Raw evidence | Confirm if | Refute if | Model revision if refuted |","|---|---|---|---|---|---|"]
for r in rows:
    vals=[r[k].replace("|","/") for k in ("prediction_id","domain","raw_evidence","confirm_if","refute_if","model_revision_if_refuted")]
    lines.append("| "+" | ".join(vals)+" |")
lines += ["","An incomplete capture is `inconclusive`, not a confirmation. Promotion remains controlled by the separate finalizer and promotion guard."]
DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("rows",len(rows),"wrote",OUT); print("wrote",DOC)
