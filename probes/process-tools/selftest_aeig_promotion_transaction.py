from pathlib import Path
from datetime import date
import csv, hashlib, json, shutil, subprocess, sys

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"; DATA=ROOT/"datasets"
DOCS=ROOT/"docs"/"reference"
CLONE=ROOT/"scratch"/"promotion-transaction-selftest"
OUT=DATA/"aeig-promotion-transaction-selftest.json"
PAGE=DOCS/"promotion-transaction-selftest.md"

def digest(p):
    if not p.exists(): return "MISSING"
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def run(root,name):
    return subprocess.run([sys.executable,str(root/"probes"/"process-tools"/name)],
        cwd=str(root),capture_output=True,text=True,encoding="utf-8",errors="replace")

def rows(p):
    with p.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))

def write_rows(p,data,fields):
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(data)
protected=[
    DATA/"aeig-domain-coverage.csv", DATA/"aeig-prediction-log.csv",
    ROOT/"README.md", ROOT/"docs"/"index.md", ROOT/"VERSION",
    DOCS/"aeig-1.0-release.md", DATA/"aeig-static-rc-manifest.csv",
    DATA/"aeig-static-rc-fingerprint.txt",
]
source_before={str(p):digest(p) for p in protected}

if CLONE.exists(): shutil.rmtree(CLONE)
(CLONE/"datasets").mkdir(parents=True)
for p in DATA.iterdir():
    if p.is_file(): shutil.copy2(p,CLONE/"datasets"/p.name)
shutil.copytree(ROOT/"docs",CLONE/"docs")
shutil.copytree(TOOLS,CLONE/"probes"/"process-tools")
shutil.copytree(ROOT/"experiments"/"user-run",CLONE/"experiments"/"user-run")
shutil.copytree(ROOT/"experiments"/"observatory"/"manifests",
                CLONE/"experiments"/"observatory"/"manifests")
if (ROOT/"research"/"findings").exists():
    shutil.copytree(ROOT/"research"/"findings",CLONE/"research"/"findings")
for name in ("README.md","ROADMAP.md","mkdocs.yml","requirements-docs.txt"):
    shutil.copy2(ROOT/name,CLONE/name)

old1=str(ROOT); old2=old1.replace("\\","\\\\")
new1=str(CLONE); new2=new1.replace("\\","\\\\")
for p in (CLONE/"probes"/"process-tools").glob("*.py"):
    text=p.read_text(encoding="utf-8-sig",errors="replace")
    p.write_text(text.replace(old2,new2).replace(old1,new1),encoding="utf-8")
pred_path=CLONE/"datasets"/"aeig-prediction-log.csv"
preds=rows(pred_path); pred_fields=list(preds[0])
for r in preds:
    if r.get("mode")=="prospective":
        r["status"]="confirmed"; r["evidence"]="synthetic promotion transaction self-test"
write_rows(pred_path,preds,pred_fields)

dec_path=CLONE/"datasets"/"aeig-l5-domain-decisions.csv"
dec=[{"domain":d,"evidence_ready":"True","model_revision_required":"False","reason":"synthetic self-test"}
     for d in ("state-identity","cache","render-graph","plugin-host")]
write_rows(dec_path,dec,["domain","evidence_ready","model_revision_required","reason"])
for exp in ("EXP-CACHE-002","EXP-PLUGIN-001","EXP-RG-001","EXP-SCRIPT-001"):
    p=CLONE/"experiments"/"observatory"/"manifests"/f"{exp}.json"
    m=json.loads(p.read_text(encoding="utf-8-sig")); m["status"]="observed"
    p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

steps=[]
for name in ("freeze_aeig_static_rc.py","compute_static_rc_fingerprint.py",
             "verify_aeig_static_rc.py","promote_aeig_1_0.py"):
    p=run(CLONE,name); steps.append({"script":name,"exit":p.returncode,
        "tail":(p.stdout+p.stderr)[-3000:]})
    if p.returncode: break

version=(CLONE/"VERSION").read_text(encoding="utf-8-sig").strip() if (CLONE/"VERSION").exists() else ""
progress=rows(CLONE/"datasets"/"aeig-roadmap-progress.csv") if (CLONE/"datasets"/"aeig-roadmap-progress.csv").exists() else []
met=sum(str(r.get("meets_1_0_target","")).lower() in {"true","1","yes"} for r in progress)
post_rc=run(CLONE,"verify_aeig_static_rc.py") if steps and steps[-1]["exit"]==0 else None
post_rel=run(CLONE,"audit_release_readiness.py") if post_rc and post_rc.returncode==0 else None
source_after={str(p):digest(p) for p in protected}
source_unchanged=source_before==source_after
checks={
    "all_steps_passed":len(steps)==4 and all(s["exit"]==0 for s in steps),
    "version_1_0":version=="1.0",
    "coverage_27_27":len(progress)==27 and met==27,
    "post_static_rc":bool(post_rc and post_rc.returncode==0),
    "post_release_audit":bool(post_rel and post_rel.returncode==0),
    "source_repository_unchanged":source_unchanged,
}
passed=all(checks.values())
payload={"status":"PASS" if passed else "FAIL","date":date.today().isoformat(),
         "checks":checks,"steps":steps,"version":version,"coverage":f"{met}/{len(progress)}"}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---",
       "# Promotion Transaction Self-Test","",f"State: **{payload['status']}**.","",
       "| Check | Result |","|---|---|"]
for k,v in checks.items(): lines.append(f"| `{k}` | **{'PASS' if v else 'FAIL'}** |")
lines += ["",f"Clone result: VERSION `{version or 'missing'}`, coverage **{met}/{len(progress)}**.",
          "The success path runs only inside `scratch/promotion-transaction-selftest`; live prediction, coverage, README, VERSION, release page and Static RC files are digest-checked for non-mutation."]
PAGE.write_text("\n".join(lines)+"\n",encoding="utf-8")
for k,v in checks.items(): print("PASS" if v else "FAIL",k)
for s in steps: print("STEP",s["script"],"exit",s["exit"])
print("clone VERSION",version or "missing","coverage",met,"/",len(progress))
print("AEIG PROMOTION TRANSACTION SELFTEST:",payload["status"])
raise SystemExit(0 if passed else 2)
