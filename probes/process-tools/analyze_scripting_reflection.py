from pathlib import Path
import csv, re, sys
import os

ROOT = Path(os.environ.get("AEIG_ROOT",r"D:\Developer\After Effects Internals Guide"))
RUN = ROOT / "experiments" / "observatory" / "runs" / "EXP-SCRIPT-001"
RAW = RUN / "runtime-reflection.tsv"
DOCS = ROOT / "datasets" / "ae-script-expression-api-atlas.csv"
OUT = ROOT / "datasets" / "exp-script-001-runtime-reflection.csv"
SUMMARY = RUN / "analysis-summary.md"

MAP = {
    "Application": ("Application object", "app"),
    "Project": ("Project object", "Project"),
    "CompItem": ("CompItem object", "CompItem"),
    "AVLayer": ("AVLayer object", "AVLayer"),
    "RenderQueue": ("RenderQueue object", "RenderQueue"),
    "RenderQueueItem": ("RenderQueueItem object", "RenderQueueItem"),
    "OutputModule": ("OutputModule object", "OutputModule"),
}

def member(symbol):
    s = symbol.rsplit(".", 1)[-1]
    return re.sub(r"\(\)$", "", s)

if not RAW.exists():
    print("not-run: missing", RAW); sys.exit(2)
with RAW.open(encoding="utf-8-sig", errors="replace") as f:
    runtime = list(csv.DictReader(f, delimiter="\t"))
with DOCS.open(encoding="utf-8", newline="") as f:
    docs_all = list(csv.DictReader(f))

doc_members = {}
for label, (container, prefix) in MAP.items():
    vals = set()
    for r in docs_all:
        if r["surface"] == "scripting-docs" and r["container"] == container:
            vals.add(member(r["symbol"]))
    doc_members[label] = vals

rows = []
for r in runtime:
    label = r.get("label", "")
    if label not in MAP: continue
    name = r.get("name", "")
    rows.append({**r, "documented_member_name": name in doc_members[label]})

fields = list(rows[0]) if rows else []
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
lines = ["# EXP-SCRIPT-001 analysis", ""]
for label in MAP:
    rr = [r for r in rows if r["label"] == label]
    runtime_names = {r["name"] for r in rr if r["name"]}
    docs = doc_members[label]
    overlap = runtime_names & docs
    lines += [
        f"## {label}", "",
        f"- Runtime Reflection members: **{len(runtime_names)}**",
        f"- Documented member names: **{len(docs)}**",
        f"- Name overlap: **{len(overlap)}**",
        f"- Runtime-only names: **{len(runtime_names-docs)}**",
        f"- Docs-only names: **{len(docs-runtime_names)}**", "",
    ]
lines += [
    "Runtime-only does not automatically mean supported hidden API; docs-only does not automatically mean absent runtime capability.",
    "Reflection visibility, inheritance, conditional members and host state can all affect the observed set.",
]
SUMMARY.write_text("\n".join(lines)+"\n", encoding="utf-8")
present_labels={r.get("label","") for r in rows}
missing_labels=sorted(set(MAP)-present_labels)
print("runtime_rows", len(runtime), "compared_rows", len(rows), "missing_labels", missing_labels)
print("wrote", OUT); print("wrote", SUMMARY)
if not rows:
    raise SystemExit(3)
if missing_labels:
    raise SystemExit(4)
