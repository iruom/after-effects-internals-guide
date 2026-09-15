from pathlib import Path
import csv

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DATA = ROOT / "datasets"
CLASS = DATA / "ae-api-completeness-classification.csv"
RAW = DATA / "ae-api-unresolved-raw-candidates.csv"
CTX = DATA / "ae-api-guide-unresolved-context.csv"
OUT = DATA / "ae-api-guide-relation-review.csv"


def read(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

classes = read(CLASS)
raw = {r["guide_symbol"]: r for r in read(RAW)}
ctx = {r["symbol"]: r for r in read(CTX)}
queue = [r for r in classes if r["completeness_class"] in
         {"guide-only-no-header-match", "guide-near-match-header"}]
rows = []
for r in queue:
    s = r["symbol"]
    rr = raw.get(s, {})
    cc = ctx.get(s, {})
    rows.append({
        "guide_symbol": s,
        "current_class": r["completeness_class"],
        "prefix_candidates": rr.get("prefix_candidates", ""),
        "containment_candidates": rr.get("containment_candidates", ""),
        "fuzzy_candidates": rr.get("fuzzy_candidates", ""),
        "occurrences": cc.get("occurrences", ""),
        "context": cc.get("contexts", ""),
        "review_relation": "",
        "review_target": "",
        "review_confidence": "",
        "review_note": "",
    })

fields = list(rows[0]) if rows else []
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)
print("relation_queue", len(rows))
print("with_context", sum(bool(r["context"]) for r in rows))
print("wrote", OUT)
