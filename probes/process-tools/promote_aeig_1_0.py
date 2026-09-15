from pathlib import Path
from datetime import datetime
import csv, json, shutil, subprocess, sys
from aeig_promotion_gate import evaluate_promotion_gate

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; TOOLS=ROOT/"probes"/"process-tools"
COVER=DATA/"aeig-domain-coverage.csv"
DEC=DATA/"aeig-l5-domain-decisions.csv"
PRED=DATA/"aeig-prediction-log.csv"
CORE={"state-identity","cache","render-graph","plugin-host"}
RELEASE_DATE=datetime.now().date().isoformat()

def rows(path):
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def truth(v): return str(v).lower() in {"true","1","yes"}
def write(path,data,fields):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)
def run(name):
    p=subprocess.run([sys.executable,str(TOOLS/name)],capture_output=True,text=True,encoding="utf-8",errors="replace")
    print(f"[{name}] exit={p.returncode}")
    if p.stdout: print(p.stdout.rstrip())
    if p.stderr: print(p.stderr.rstrip(),file=sys.stderr)
    return p

if run("verify_aeig_static_rc.py").returncode:
    raise SystemExit("static RC hash/prediction lock verification failed")

if not DEC.exists(): raise SystemExit("missing L5 domain decisions; run finalizer first")
decision_rows=rows(DEC); pred=rows(PRED)
manifest_statuses={}
for exp in ("EXP-CACHE-002","EXP-PLUGIN-001","EXP-RG-001"):
    p=ROOT/"experiments"/"observatory"/"manifests"/f"{exp}.json"
    m=json.loads(p.read_text(encoding="utf-8-sig")); manifest_statuses[exp]=m.get("status","")
gate=evaluate_promotion_gate(decision_rows,pred,manifest_statuses)
if not gate["ok"]:
    raise SystemExit("promotion gate failed: "+"; ".join(gate["errors"]))
pros=[r for r in pred if r.get("mode")=="prospective"]
confirmed=gate["confirmed"]

if run("audit_repository_integrity.py").returncode:
    raise SystemExit("repository integrity failed before promotion")

stamp=datetime.now().strftime("%Y%m%d-%H%M%S")
hist=DATA/"history"; hist.mkdir(parents=True,exist_ok=True)
backup=hist/f"aeig-domain-coverage-pre-1.0-{stamp}.csv"
shutil.copy2(COVER,backup)
coverage=rows(COVER); fields=list(coverage[0])
next_text={
 "state-identity":"EXP-CACHE-002 + EXP-RG-001 observed receipt/identity trace evidence",
 "cache":"EXP-CACHE-002 + EXP-RG-001 observed cache-validity/runtime trace evidence",
 "render-graph":"EXP-RG-001 observed BEE/RG/TDB trace correlation",
 "plugin-host":"EXP-PLUGIN-001 observed 48-family x selector-1..32 runtime negotiation matrix",
}
for r in coverage:
    if r["domain"] in CORE:
        r["current_level"]="L5"; r["next_evidence"]=next_text[r["domain"]]
write(COVER,coverage,fields)
run("report_roadmap_progress.py")
release=run("audit_release_readiness.py")
if release.returncode:
    shutil.copy2(backup,COVER)
    run("report_roadmap_progress.py")
    run("audit_release_readiness.py")
    raise SystemExit("post-promotion release audit failed; coverage rolled back")

progress=rows(DATA/"aeig-roadmap-progress.csv")
met=sum(truth(r["meets_1_0_target"]) for r in progress)
counts={f"L{n}":sum(r["current_level"]==f"L{n}" for r in progress) for n in range(1,8)}
if met!=len(progress):
    shutil.copy2(backup,COVER); run("report_roadmap_progress.py")
    raise SystemExit(f"coverage did not reach 27/27: {met}/{len(progress)}")

readme=ROOT/"README.md"
index_path=ROOT/"docs"/"index.md"
readme_backup=hist/f"README-pre-1.0-{stamp}.md"
index_backup=hist/f"docs-index-pre-1.0-{stamp}.md"
shutil.copy2(readme,readme_backup); shutil.copy2(index_path,index_backup)
s=readme.read_text(encoding="utf-8-sig")
import re
s=re.sub(r'As of \d{4}-\d{2}-\d{2}, \*\*\d+/27\*\* tracked domains meet the AEIG 1\.0 minimum\. Distribution: [^\n]+',
         f'As of {RELEASE_DATE}, **27/27** tracked domains meet the AEIG 1.0 minimum. Distribution: L2={counts["L2"]}, L3={counts["L3"]}, L4={counts["L4"]}, L5={counts["L5"]}.',s)
s=s.replace('## Current priorities\n1. Run the canonical `experiments/user-run/AEIG-1.0-L5` package once in a disposable full AE session to close the four remaining core L5 gates.',
'''## Current priorities\n1. Preserve AEIG 1.0 evidence and rerun the canonical Observatory suite against new AE releases.''')
readme.write_text(s,encoding="utf-8")

idx=index_path
s=idx.read_text(encoding="utf-8-sig")
s=re.sub(r'Current work should preferentially deepen[^\n]+',
         'AEIG 1.0 minimum coverage is complete at 27/27 domains; subsequent work extends version lineage, replication and capability depth without weakening the 1.0 evidence gates.',s)
idx.write_text(s,encoding="utf-8")
(ROOT/"VERSION").write_text("1.0\n",encoding="utf-8")
# Replace the pre-release priority queue with post-1.0 maintenance work.
s=readme.read_text(encoding="utf-8-sig")
s=re.sub(r'## Current priorities\n.*?\n## Completeness is corpus-scoped',
'''## Current priorities
1. Preserve and replicate AEIG 1.0 evidence against each new AE release.
2. Extend historical SDK coverage through the remaining 11.x -> 23.x gap.
3. Expand Capability Recipes and out-of-sample predictions beyond the 1.0 minimum.
4. Grow AEP/AEPX/FFX differential corpora and CPU/GPU/media parity experiments.
5. Keep public Guide, distributed headers, runtime surfaces and hidden diagnostics version-scoped.

## Completeness is corpus-scoped''',s,flags=re.S)
readme.write_text(s,encoding="utf-8")

run("report_prediction_status.py")
release_page=ROOT/"docs"/"reference"/"aeig-1.0-release.md"
release_page.write_text("\n".join([
 "---","status: release",f"last_verified: {RELEASE_DATE}","version: AEIG-1.0","---",
 "# AEIG 1.0 Release Evidence","",
 f"- Domain targets: **{met}/{len(progress)}**.",
 f"- Coverage distribution: `{ {k:v for k,v in counts.items() if v} }`.",
 f"- Prospective predictions confirmed: **{confirmed}/{len(pros)}**; no pending or unrevised refutation.",
 f"- C++ API surface classification: **{len(rows(DATA/'ae-api-completeness-classification.csv'))} identifiers, 0 open surface gaps**.",
 f"- Master Surface Registry: **{len(rows(DATA/'ae-master-surface-registry.csv'))} rows**.",
 f"- Corpus manifest: **{len(rows(DATA/'aeig-corpus-coverage-manifest.csv'))} corpora**.",
 f"- Finding registry: **{len(rows(DATA/'finding-registry-audit.csv'))} findings**, duplicate IDs and missing frontmatter zero.",
 "- Guide/Header relation review: **113/113 reviewed**.",
 "- Canonical L5 operator package and repository-integrity audit were green at promotion.","",
 f"Coverage backup before promotion: `{backup.relative_to(ROOT)}`.",
 "AEIG 1.0 is corpus-scoped: non-distributed Adobe private source/layout remains an explicit unknown frontier, not silently inferred as complete.",
])+"\n",encoding="utf-8")
final_rc=run("verify_aeig_static_rc.py")
if final_rc.returncode:
    shutil.copy2(backup,COVER)
    shutil.copy2(readme_backup,readme)
    shutil.copy2(index_backup,index_path)
    (ROOT/"VERSION").unlink(missing_ok=True)
    release_page.unlink(missing_ok=True)
    run("report_roadmap_progress.py")
    run("report_prediction_status.py")
    raise SystemExit("static RC changed during promotion; release state rolled back")
integrity=run("audit_repository_integrity.py")
final_release=run("audit_release_readiness.py")
if integrity.returncode or final_release.returncode:
    shutil.copy2(backup,COVER)
    shutil.copy2(readme_backup,readme)
    shutil.copy2(index_backup,index_path)
    (ROOT/"VERSION").unlink(missing_ok=True)
    release_page.unlink(missing_ok=True)
    run("report_roadmap_progress.py")
    run("report_prediction_status.py")
    run("audit_release_readiness.py")
    raise SystemExit("final release audit failed; coverage and docs rolled back")

print("AEIG 1.0 PROMOTION: PASS")
print("coverage",met,"/",len(progress),counts)
print("prospective predictions confirmed",confirmed,"/",len(pros))
print("release page",release_page)
print("coverage backup",backup)
