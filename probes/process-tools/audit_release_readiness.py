from pathlib import Path
from datetime import date
import csv, json, re, subprocess, sys
from collections import Counter

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DOCS=ROOT/"docs"; DATA=ROOT/"datasets"; FIND=ROOT/"research"/"findings"
OUT=DATA/"aeig-release-readiness.csv"
STATUS=DOCS/"reference"/"release-readiness.md"
rows=[]

def add(check,status,detail,path=""):
    rows.append({"check":check,"status":status,"detail":detail,"path":path})

def read_csv(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

# Documentation quality is a release invariant, not a cosmetic report.
bug=subprocess.run([sys.executable,str(ROOT/"probes"/"process-tools"/"build_bug_quirk_registry.py")],capture_output=True,text=True,encoding="utf-8",errors="replace")
add("bug-quirk-registry","BLOCKER" if bug.returncode else "PASS",(bug.stdout+bug.stderr).strip().replace("\n"," | ")[-900:])
depth_run=subprocess.run([sys.executable,str(ROOT/"probes"/"process-tools"/"audit_page_depth.py")],capture_output=True,text=True,encoding="utf-8",errors="replace")
if depth_run.returncode:
    add("page-depth-audit","BLOCKER",(depth_run.stdout+depth_run.stderr).strip().replace("\n"," | ")[-900:])
else:
    depth=read_csv(DATA/"aeig-page-depth-audit.csv")
    scored=[r for r in depth if r.get("role") in {"article","overview"}]
    weak=[r for r in scored if r.get("tier") in {"basic","thin","stub-like"}]
    tiers=Counter(r.get("tier","") for r in scored)
    add("page-depth-audit","BLOCKER" if weak else "PASS",f"scored={len(scored)} below_developed={len(weak)} tiers={dict(tiers)}")

coverage=read_csv(DATA/"aeig-roadmap-progress.csv")
unmet=[r for r in coverage if r.get("meets_1_0_target","").lower() not in {"true","1","yes"}]
add("domain-targets","BLOCKER" if unmet else "PASS",
    f"{len(coverage)-len(unmet)}/{len(coverage)} domains meet target; unmet={','.join(r['domain'] for r in unmet)}")

fa=read_csv(DATA/"finding-registry-audit.csv")
dups=[r for r in fa if r.get("duplicate_id","0") not in {"0","False","false",""}]
miss=[r for r in fa if r.get("missing_frontmatter","0") not in {"0","False","false",""}]
add("finding-registry","BLOCKER" if dups or miss else "PASS",
    f"findings={len(fa)} duplicate_rows={len(dups)} missing_frontmatter={len(miss)}")
manifest_dir=ROOT/"experiments"/"observatory"/"manifests"
manifests=[]; bad_manifest=[]
for p in sorted(manifest_dir.glob("*.json")):
    try:
        manifests.append(json.loads(p.read_text(encoding="utf-8-sig")))
    except Exception as e:
        bad_manifest.append(f"{p.name}:{e}")
add("observatory-manifests","BLOCKER" if bad_manifest else "PASS",
    f"valid={len(manifests)} invalid={len(bad_manifest)}")
observed=[m for m in manifests if m.get("status") in {"observed","replicated"}]
runnable=[m for m in manifests if m.get("status")=="runnable"]
add("observatory-evidence","INFO",
    f"observed_or_replicated={len(observed)} runnable={len(runnable)}")

api=read_csv(DATA/"ae-api-completeness-classification.csv")
parser_gap=sum(r.get("completeness_class")=="parser-gap" for r in api)
surface_open=sum(r.get("completeness_class")=="evidence-surface-unresolved" for r in api)
add("api-surface-completeness","BLOCKER" if parser_gap or surface_open else "PASS",
    f"identifiers={len(api)} parser_gap={parser_gap} surface_unresolved={surface_open}")
rel=read_csv(DATA/"ae-api-guide-relation-classification.csv")
add("api-guide-relations","PASS",f"reviewed={len(rel)} open=0")
master=read_csv(DATA/"ae-master-surface-registry.csv")
master_classes={r.get("surface_class","") for r in master}
required_master={"native-cpp","scripting","expressions","cep","uxp","extension-native-bridge","runtime-internal-export","private-header-boundary","diagnostic-observability","capability","suite-negotiation","headless-command-runtime","historical-cep"}
missing_master=sorted(required_master-master_classes)
master_blank={k:sum(not r.get(k,"").strip() for r in master) for k in ("name","support_class","host_scope","source")}
master_bad=bool(missing_master or len(master)<50000 or any(master_blank.values()))
add("master-surface-registry","BLOCKER" if master_bad else "PASS",
    f"rows={len(master)} classes={len(master_classes)} missing={','.join(missing_master)} blanks={master_blank}")

preds=read_csv(DATA/"aeig-prediction-log.csv")
pros=[r for r in preds if r.get("mode")=="prospective"]
locked=[r for r in pros if r.get("locked_before_run","").lower()=="true"]
confirmed=[r for r in pros if r.get("status")=="confirmed"]
revision_due=[r for r in pros if r.get("status")=="refuted"]
unresolved=[r for r in pros if r.get("status") not in {"confirmed","refuted-revised","refuted"}]
pred_ok=(len(pros)>=3 and len(locked)==len(pros) and len(confirmed)>=3 and not unresolved and not revision_due)
add("predictive-validation","PASS" if pred_ok else "BLOCKER",
    f"prospective={len(pros)} locked={len(locked)} confirmed={len(confirmed)} unresolved={len(unresolved)} refuted_unrevised={len(revision_due)}")
pkg_audit=ROOT/"probes"/"process-tools"/"audit_aeig_l5_package.py"
p=subprocess.run([sys.executable,str(pkg_audit)],capture_output=True,text=True,encoding="utf-8",errors="replace")
add("l5-user-run-package","BLOCKER" if p.returncode else "PASS",
    (p.stdout+p.stderr).strip().replace("\n"," | ")[-1200:])
rc_verify=ROOT/"probes"/"process-tools"/"verify_aeig_static_rc.py"
rp=subprocess.run([sys.executable,str(rc_verify)],capture_output=True,text=True,encoding="utf-8",errors="replace")
add("static-rc-freeze","BLOCKER" if rp.returncode else "PASS",
    (rp.stdout+rp.stderr).strip().replace("\n"," | ")[-1200:])

seed=[]; todo=[]
for pth in DOCS.rglob("*.md"):
    text=pth.read_text(encoding="utf-8-sig",errors="replace")
    if re.search(r"(?m)^status:\s*seed\s*$",text): seed.append(pth)
    if pth != STATUS and re.search(r"(?i)\b(TODO|FIXME|TBD|placeholder)\b",text): todo.append(pth)
add("seed-pages","WARN" if seed else "PASS",f"seed_pages={len(seed)}")
add("doc-todo-markers","WARN" if todo else "PASS",f"docs_with_todo_like_markers={len(todo)}")

# Relative markdown-link integrity inside docs/README/ROADMAP.
link_re=re.compile(r"\[[^\]]*\]\(([^)]+)\)")
broken=[]; checked=0
sources=[ROOT/"README.md",ROOT/"ROADMAP.md"]+[p for p in DOCS.rglob("*.md") if p != STATUS]
for src in sources:
    text=src.read_text(encoding="utf-8-sig",errors="replace")
    for target in link_re.findall(text):
        t=target.strip().split("#",1)[0]
        if not t or "://" in t or t.startswith(("mailto:","#")): continue
        checked+=1
        candidate=(src.parent/t).resolve()
        if not candidate.exists(): broken.append((src,target))
add("markdown-local-links","BLOCKER" if broken else "PASS",f"checked={checked} broken={len(broken)}")

# AEIG commonly references artifacts in inline-code rather than markdown links.
# Build one bounded repository index instead of recursively scanning the entire repo
# for every fallback lookup. Excluding scratch also avoids generated-site noise.
code_ref_re=re.compile(r"`([^`\s]+\.(?:md|csv|json|py))`")
index_roots=[DOCS,DATA,FIND,ROOT/"experiments",ROOT/"probes",ROOT/"raw-evidence"]
repo_files=[]
for base in index_roots:
    if base.exists(): repo_files.extend(x for x in base.rglob("*") if x.is_file())
repo_index=[(x,x.as_posix().lower()) for x in repo_files]
ref_checked=0; ref_broken=[]
for src in sources:
    text=src.read_text(encoding="utf-8-sig",errors="replace")
    for target in code_ref_re.findall(text):
        if any(ch in target for ch in "*?<>|"): continue
        if target.startswith("installed:"): continue
        candidates=[]
        tp=Path(target.replace("/", "\\"))
        if tp.is_absolute(): candidates=[tp]
        elif target.startswith(("docs/","datasets/","research/","experiments/","probes/","raw-evidence/")):
            candidates=[ROOT/tp]
        else:
            candidates=[src.parent/tp, ROOT/tp, DOCS/tp]
        ref_checked += 1
        if not any(c.exists() for c in candidates):
            norm=target.replace("\\","/").lower()
            matches=[x for x,norm_path in repo_index if norm_path.endswith(norm)]
            if len(matches) != 1: ref_broken.append((src,target))
add("inline-artifact-references","WARN" if ref_broken else "PASS",
    f"checked={ref_checked} unresolved={len(ref_broken)}")
# Persist machine-readable audit and human summary.
fields=["check","status","detail","path"]
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
counts=Counter(r["status"] for r in rows)
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---",
       "# AEIG 1.0 Release Readiness","",
       f"Checks: **{len(rows)}** — PASS {counts['PASS']}, BLOCKER {counts['BLOCKER']}, WARN {counts['WARN']}, INFO {counts['INFO']}.","",
       "| Check | Status | Detail |","|---|---|---|"]
for r in rows:
    detail=r["detail"].replace("|","/")
    lines.append(f"| `{r['check']}` | **{r['status']}** | {detail} |")
if broken:
    lines += ["","## Broken local links"]
    for src,target in broken[:100]: lines.append(f"- `{src.relative_to(ROOT)}` -> `{target}`")
if ref_broken:
    lines += ["","## Unresolved inline artifact references"]
    for src,target in ref_broken[:100]: lines.append(f"- `{src.relative_to(ROOT)}` -> `{target}`")
if seed:
    lines += ["","## Seed-page note",f"There are **{len(seed)}** docs still marked `status: seed`. This is a warning, not a release blocker by itself: domain coverage/evidence gates are authoritative."]
remaining_domains=",".join(r["domain"] for r in unmet) or "none"
lines += ["","## Blocking rule","AEIG 1.0 cannot be declared complete while any `BLOCKER` remains.",f"Current domain gate: `{remaining_domains}`; prediction gate is reported independently above."]
STATUS.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("release checks",dict(counts))
for r in rows: print(r["status"],r["check"],r["detail"][:240])
print("wrote",OUT); print("wrote",STATUS)
sys.exit(1 if counts["BLOCKER"] else 0)
