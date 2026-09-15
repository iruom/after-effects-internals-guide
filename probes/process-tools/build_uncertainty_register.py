from pathlib import Path
import csv, re

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DOCS=ROOT/"docs"; DATA=ROOT/"datasets"
OUT=DATA/"aeig-uncertainty-register.csv"
DOC=DOCS/"reference"/"uncertainty-register.md"
rows=[]

for p in DOCS.rglob("*.md"):
    text=p.read_text(encoding="utf-8-sig",errors="replace")
    m=re.search(r"(?m)^status:\s*([^\r\n]+)",text)
    if not m: continue
    status=m.group(1).strip()
    if status not in {"researched-seed","active-hypothesis","seed-map"}: continue
    title=re.search(r"(?m)^#\s+(.+)$",text)
    rows.append({"class":"document-hypothesis","status":status,
                 "name":title.group(1).strip() if title else p.stem,
                 "source":p.relative_to(ROOT).as_posix(),
                 "scope":"model not promoted to confirmed implementation detail"})
