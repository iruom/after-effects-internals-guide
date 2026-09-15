from pathlib import Path
import re, csv
from collections import Counter
ROOT = Path(r"D:\Developer\After Effects Internals Guide")
FINDINGS = ROOT / "research" / "findings"
rows = []
for p in sorted(FINDINGS.glob("F-*.md")):
    m = re.match(r"(F-[A-Z0-9]+-\d+)-(.+)\.md$", p.name)
    if not m:
        rows.append({"id":"","file":p.name,"title":"","has_frontmatter":False,"status":"bad-filename"})
        continue
    text = p.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff")
    title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), "")
    has_frontmatter = text.startswith("---\n") or text.startswith("---\r\n")
    rows.append({"id":m.group(1),"file":p.name,"title":title,"has_frontmatter":has_frontmatter,"status":"ok"})
counts = Counter(r["id"] for r in rows if r["id"])
dups = {k:v for k,v in counts.items() if v > 1}
out = ROOT / "datasets" / "finding-registry-audit.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id","file","title","has_frontmatter","status"])
    w.writeheader(); w.writerows(rows)
missing = [r["file"] for r in rows if not r["has_frontmatter"]]
print("findings", len(rows), "duplicate_ids", len(dups), "missing_frontmatter", len(missing))
for fid, n in sorted(dups.items()): print("DUP", fid, n, [r["file"] for r in rows if r["id"] == fid])
for name in missing: print("NO_FRONTMATTER", name)
print("wrote", out)
