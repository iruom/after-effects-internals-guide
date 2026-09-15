from pathlib import Path
from datetime import date
import csv, re, statistics
from collections import Counter, defaultdict

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DOCS=ROOT/"docs"; DATA=ROOT/"datasets"
OUT=DATA/"aeig-page-depth-audit.csv"
PAGE=DOCS/"reference"/"page-depth-audit.md"

DIMENSIONS={
 "internals": r"(?i)\b(internal|architecture|model|pipeline|lifetime|identity|dependency|graph|state|ownership)\b",
 "evidence": r"(?i)\b(evidence|source|observed|distributed|binary|trace|header|finding|dataset)\b",
 "version": r"(?i)\b(version|lineage|histor|deprecated|removed|CS6|CC ?20|AE ?1[1-9]|AE ?2[0-9]|26\.)\b",
 "api_context": r"(?i)\b(API|SDK|suite|AEGP|AEIO|PF_|scripting|expression|host|thread|context)\b",
 "failure_bug": r"(?i)\b(fail|failure|bug|quirk|regression|crash|hazard|pitfall|invalid|unsupported|caveat)\b",
 "experiment": r"(?i)\b(experiment|probe|fixture|test|reproduc|falsif|measure|capture|differential)\b",
 "unknowns": r"(?i)\b(unknown|open question|hypothesis|unresolved|provisional|not yet|frontier|limitation|falsif)\b",
 "crosslinks": r"\[[^\]]+\]\([^)]+\)|`(?:docs|datasets|research|experiments|probes)/[^`]+`",
}
NON_ARTICLE={"generated","reference-generated","index","seed-map"}
def frontmatter(text):
    m=re.match(r"^---\s*\n(.*?)\n---\s*\n",text,re.S)
    meta={}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k,v=line.split(":",1); meta[k.strip()]=v.strip()
    return meta

def body_without_frontmatter(text):
    return re.sub(r"^---\s*\n.*?\n---\s*\n","",text,count=1,flags=re.S)

def word_count(text):
    return len(re.findall(r"[A-Za-z0-9_][A-Za-z0-9_./:+-]*|[\u3040-\u30ff\u3400-\u9fff]+",text))

def page_role(path,status):
    if status in NON_ARTICLE: return status
    if path.name=="index.md": return "index"
    if path.name=="overview.md": return "overview"
    return "article"

def density_tier(score,words,missing):
    if score>=8 and words>=550: return "deep"
    if score>=6 and words>=300: return "developed"
    if score>=4 and words>=180: return "basic"
    if words<120 or score<=2: return "stub-like"
    return "thin"
rows=[]
for path in sorted(DOCS.rglob("*.md")):
    text=path.read_text(encoding="utf-8-sig",errors="replace")
    meta=frontmatter(text); status=meta.get("status","")
    role=page_role(path,status); body=body_without_frontmatter(text)
    words=word_count(body); chars=len(body); headings=len(re.findall(r"(?m)^#{1,6}\s+",body))
    dims={name:bool(re.search(pattern,body)) for name,pattern in DIMENSIONS.items()}
    # Content volume is useful but cannot by itself make a page deep.
    volume=2 if words>=600 else 1 if words>=300 else 0
    structural=sum(dims.values()); score=structural+volume
    missing=[k for k,v in dims.items() if not v]
    tier=density_tier(score,words,missing) if role in {"article","overview"} else "not-scored"
    rows.append({
        "path":path.relative_to(ROOT).as_posix(),"status":status,"role":role,
        "words":words,"chars":chars,"headings":headings,"depth_score":score,"tier":tier,
        **{f"has_{k}":v for k,v in dims.items()},"missing_dimensions":";".join(missing),
    })

fields=list(rows[0])
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

scored=[r for r in rows if r["role"] in {"article","overview"}]
active=[r for r in scored if r["status"]=="active"]
tiers=Counter(r["tier"] for r in active)
by_section=defaultdict(list)
for r in active:
    parts=Path(r["path"]).parts
    section=parts[1] if len(parts)>2 else "root"
    by_section[section].append(r)
ranked=sorted(active,key=lambda r:(r["depth_score"],r["words"],r["path"]))
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---",
       "# AEIG Page Depth Audit","",
       f"Scored active article/overview pages: **{len(active)}**. Median words: **{int(statistics.median(r['words'] for r in active)) if active else 0}**.",
       f"Depth tiers: `{dict(tiers)}`.","",
       "A page is not promoted by word count alone. The score checks implementation/model detail, evidence, version lineage, API/host context, failure/bug knowledge, experiments, explicit unknowns/falsification, and cross-links; content volume contributes at most two points.","",
       "## Highest-priority thin pages","",
       "| Page | Score | Words | Tier | Missing dimensions |","|---|---:|---:|---|---|"]
for r in ranked[:40]:
    lines.append(f"| `{r['path']}` | {r['depth_score']}/10 | {r['words']} | {r['tier']} | {r['missing_dimensions'].replace(';',', ')} |")
lines += ["","## Section health","","| Section | Pages | Median score | Median words | Below developed |","|---|---:|---:|---:|---:|"]
for section,items in sorted(by_section.items(),key=lambda kv:(statistics.median(x["depth_score"] for x in kv[1]),kv[0])):
    weak=sum(x["tier"] in {"basic","thin","stub-like"} for x in items)
    lines.append(f"| `{section}` | {len(items)} | {statistics.median(x['depth_score'] for x in items):.1f} | {statistics.median(x['words'] for x in items):.0f} | {weak} |")
lines += ["","## Editorial rule","",
          "AEIG 1.0 requires every article/overview page to reach at least `developed`; `basic`, `thin`, and `stub-like` are explicit documentation debt. Expansion must preserve evidence grading: unsupported internals are written as hypotheses or unknowns, not filled with plausible-sounding prose.",
          "The machine-readable audit is `datasets/aeig-page-depth-audit.csv`."]
PAGE.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("pages",len(rows),"active_scored",len(active),"tiers",dict(tiers))
print("median_words",statistics.median(r["words"] for r in active) if active else 0)
print("priority")
for r in ranked[:20]: print(r["depth_score"],r["words"],r["tier"],r["path"],r["missing_dimensions"])
print("wrote",OUT); print("wrote",PAGE)
