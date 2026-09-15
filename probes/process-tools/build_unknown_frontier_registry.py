from pathlib import Path
import csv, re

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; DOCS=ROOT/"docs"
OUT=DATA/"aeig-unknown-frontier.csv"; STATUS=DOCS/"reference"/"unknown-frontier.md"
rows=[]

def add(kind,subject,state,evidence,next_action):
    rows.append({"frontier_type":kind,"subject":subject,"state":state,"evidence":evidence,"next_action":next_action})

with (DATA/"aeig-corpus-coverage-manifest.csv").open(encoding="utf-8-sig",newline="") as f:
    for r in csv.DictReader(f):
        note=r.get("unresolved","").strip()
        if note:
            add("corpus-boundary",r["corpus_id"],"explicit-open-boundary",note,"resolve only with stronger/original/additional corpus evidence")

for p in DOCS.rglob("*.md"):
    text=p.read_text(encoding="utf-8-sig",errors="replace")
    m=re.search(r"(?m)^status:\s*([^\r\n]+)",text)
    status=m.group(1).strip() if m else ""
    if status in {"researched-seed","seed-map","active-hypothesis"}:
        title=re.search(r"(?m)^#\s+(.+)$",text)
        add("model-frontier",p.relative_to(ROOT).as_posix(),status,title.group(1) if title else "","promote only with additional evidence or falsification tests")
with (DATA/"ae-plugin-capability-frontier.csv").open(encoding="utf-8-sig",newline="") as f:
    for r in csv.DictReader(f):
        if r.get("status") in {"internal-observation","unknown-current-contract","firstparty-runtime-confirmed"}:
            add("capability-boundary",r["capability"],r["status"],r.get("internal_evidence","") or r.get("public_route",""),r.get("next_probe",""))

fields=["frontier_type","subject","state","evidence","next_action"]
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
from collections import Counter
counts=Counter(r["frontier_type"] for r in rows)
lines=["---","status: generated","last_verified: 2026-09-15","---","# AEIG Unknown Frontier","",
       f"Tracked explicit unknown/open boundaries: **{len(rows)}**.",""]
for k,v in sorted(counts.items()): lines.append(f"- `{k}`: **{v}**")
lines += ["","These rows are not release failures by themselves. They are the explicit frontier beyond the corpus-scoped AEIG 1.0 claims.",
          "A visible runtime symbol, a first-party-only bridge, or a hypothesis page does not become a supported third-party contract merely by being cataloged.","",
          "Machine-readable source: `datasets/aeig-unknown-frontier.csv`."]
STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("rows",len(rows),"classes",dict(counts)); print("wrote",OUT); print("wrote",STATUS)
