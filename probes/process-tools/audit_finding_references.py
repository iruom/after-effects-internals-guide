from pathlib import Path
import csv, re, sys

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; DOCS=ROOT/"docs"; RESEARCH=ROOT/"research"
REG=DATA/"finding-registry-audit.csv"
OUT=DATA/"finding-reference-audit.csv"
STATUS=DOCS/"reference"/"finding-reference-status.md"
with REG.open(encoding="utf-8-sig",newline="") as f:
    known={r["id"] for r in csv.DictReader(f)}
rows=[]
pat=re.compile(r"\bF-[A-Z0-9]+-\d+\b")
for base in (DOCS,RESEARCH):
    for p in base.rglob("*.md"):
        text=p.read_text(encoding="utf-8-sig",errors="replace")
        for m in pat.finditer(text):
            rid=m.group(0)
            rows.append({"finding_id":rid,"source":p.relative_to(ROOT).as_posix(),"resolved":rid in known})
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["finding_id","source","resolved"]); w.writeheader(); w.writerows(rows)
missing=sorted({r["finding_id"] for r in rows if not r["resolved"]})
unique={r["finding_id"] for r in rows}
lines=["---","status: generated","last_verified: 2026-09-15","---","# Finding Reference Status","",
       f"- Registry IDs: **{len(known)}**.",f"- Reference occurrences: **{len(rows)}**.",
       f"- Unique referenced IDs: **{len(unique)}**.",f"- Unresolved IDs: **{len(missing)}**."]
if missing:
    lines += ["","## Unresolved"]+[f"- `{x}`" for x in missing]
STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("registry",len(known),"refs",len(rows),"unique",len(unique),"missing",len(missing))
print("wrote",OUT); print("wrote",STATUS)
raise SystemExit(1 if missing else 0)
