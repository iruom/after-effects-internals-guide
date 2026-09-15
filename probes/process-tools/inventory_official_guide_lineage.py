from pathlib import Path
import csv, re, subprocess
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
CLONE=ROOT/"scratch"/"after-effects-plugin-guide-history"
SRC=CLONE/"docs"/"intro"/"compatibility-across-multiple-versions.md"
OUT=ROOT/"datasets"/"ae-official-api-version-lineage.csv"
COMMITS=ROOT/"datasets"/"ae-official-guide-history-milestones.csv"
DOC=ROOT/"docs"/"archaeology"/"official-api-version-lineage.md"
text=SRC.read_text(encoding="utf-8-sig")
rows=[]; in_table=False
for line in text.splitlines():
    if line.strip().startswith("|        Release"):
        in_table=True; continue
    if not in_table or not line.strip().startswith("|"): continue
    if set(line.replace("|","").replace("-","").replace(" ",""))==set(): continue
    cells=[c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells)<3 or cells[0].startswith("---"): continue
    effect=re.match(r"([0-9]+\.[0-9]+)",cells[1])
    rows.append({"release":cells[0],"effect_api":effect.group(1) if effect else cells[1],"aegp_api":cells[2],"evidence":"official-current-guide-history-table","source":"docs/intro/compatibility-across-multiple-versions.md"})
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["release","effect_api","aegp_api","evidence","source"])
    w.writeheader(); w.writerows(rows)
patterns=[
    ("2018-initial-guide","4da9a2b"),
    ("2020-mfr","49caa75"),
    ("2021-mfr-sequence-compute-cache","aa72147"),
    ("2021-ae22","27e401c"),
    ("2023-ocio-color-suite5","1ae6dd3"),
    ("2025-ae25_2","d70d6a8"),
    ("2025-ae25_6","94e85b0"),
    ("2026-ae26_5","6d9b285"),
]
commit_rows=[]
for label,sha in patterns:
    out=subprocess.check_output(["git","show","-s","--date=short","--format=%H\t%ad\t%s",sha],cwd=CLONE,text=True,encoding="utf-8").strip()
    full,date,title=out.split("\t",2)
    commit_rows.append({"milestone":label,"commit":full,"date":date,"title":title,"evidence":"official-guide-git-history"})
with COMMITS.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["milestone","commit","date","title","evidence"])
    w.writeheader(); w.writerows(commit_rows)
lines=["---","status: generated","last_verified: 2026-09-15","---","# Official API Version Lineage","",
       "This page keeps official historical-document evidence separate from distributed-header evidence.","",
       f"API-version rows recovered from the current official Guide: **{len(rows)}**.","",
       "| Release | Effect API | AEGP API |","|---|---:|---:|"]
for r in rows:
    lines.append(f"| {r['release']} | `{r['effect_api']}` | `{r['aegp_api'] or '—'}` |")
lines += ["","## Git-history milestones","","| Date | Milestone | Commit subject |","|---|---|---|"]
for r in commit_rows:
    lines.append(f"| {r['date']} | `{r['milestone']}` | {r['title']} |")
lines += ["","These rows do not substitute for missing SDK header snapshots. They provide official documentation lineage for releases where a distributed historical SDK corpus has not yet been recovered."]
DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("api version rows",len(rows))
print("git milestones",len(commit_rows))
print("wrote",OUT); print("wrote",COMMITS); print("wrote",DOC)
