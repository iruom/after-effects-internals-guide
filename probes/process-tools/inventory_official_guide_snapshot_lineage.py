from pathlib import Path
import csv, re
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
EXT=ROOT/"research"/"external-sources"/"ae-guide-history"
CUR=ROOT/"scratch"/"after-effects-plugin-guide-history"/"docs"/"intro"/"compatibility-across-multiple-versions.md"
OUT=ROOT/"datasets"/"ae-official-guide-api-version-snapshots.csv"
STATUS=ROOT/"docs"/"reference"/"official-guide-snapshot-lineage.md"
SOURCES=[
 ("2018-initial",EXT/"2018-initial"/"compatibility-across-multiple-versions.rst","b4bb8e33349c15af0f29875647722898c30c7ab3"),
 ("2021-ae22",EXT/"2021-ae22"/"compatibility-across-multiple-versions.rst","27e401cd011452ff0e8b2ef8c3eae0a90a8927a8"),
 ("2026-current",CUR,"6d9b285"),
]
release_re=re.compile(r"^(?:\d+(?:\.\d+)?|CC|CS\d|\d\.\d,)")
def parse(path):
    rows=[]
    for line in path.read_text(encoding="utf-8-sig",errors="replace").splitlines():
        s=line.strip()
        if not (s.startswith("|") and s.count("|")>=4): continue
        cells=[c.strip(" *`") for c in s.strip("|").split("|")]
        if len(cells)<3 or not release_re.match(cells[0]): continue
        if cells[0].lower().startswith("release"): continue
        m=re.match(r"([0-9]+\.[0-9]+)",cells[1])
        rows.append((cells[0],m.group(1) if m else cells[1],cells[2]))
    return rows
all_rows=[]; by_snapshot={}
for label,path,commit in SOURCES:
    parsed=parse(path); by_snapshot[label]={r[0]:(r[1],r[2]) for r in parsed}
    for release,effect,aegp in parsed:
        all_rows.append({"snapshot":label,"commit":commit,"release":release,"effect_api":effect,"aegp_api":aegp,"source":str(path.relative_to(ROOT)).replace('\\','/')})
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["snapshot","commit","release","effect_api","aegp_api","source"])
    w.writeheader(); w.writerows(all_rows)
releases=sorted(set().union(*(set(v) for v in by_snapshot.values())))
lines=["---","status: generated","last_verified: 2026-09-15","---","# Official Guide API-Version Snapshot Lineage","",
       "Historical Guide snapshots are preserved separately from SDK-header corpora.","",
       "| Release | 2018 | 2021 | 2026/current |","|---|---|---|---|"]
for rel in releases:
    vals=[]
    for label in ("2018-initial","2021-ae22","2026-current"):
        v=by_snapshot[label].get(rel); vals.append(f"`{v[0]}` / `{v[1] or '—'}`" if v else "—")
    lines.append(f"| {rel} | {vals[0]} | {vals[1]} | {vals[2]} |")
lines += ["","The table records documentation presence only. Absence from a snapshot does not prove the API did not exist; exact ABI requires a matching distributed-header or runtime corpus."]
STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("snapshot rows",len(all_rows),"unique releases",len(releases))
for label in by_snapshot: print(label,len(by_snapshot[label]))
print("wrote",OUT); print("wrote",STATUS)
