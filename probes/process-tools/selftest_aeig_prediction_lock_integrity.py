from pathlib import Path
from datetime import date
import csv, hashlib, json, shutil, subprocess, sys

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"; DATA=ROOT/"datasets"; DOCS=ROOT/"docs"/"reference"
CLONE=ROOT/"scratch"/"prediction-lock-selftest"
OUT=DATA/"aeig-prediction-lock-selftest.json"; PAGE=DOCS/"prediction-lock-selftest.md"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "MISSING"
def run(root,name):
    return subprocess.run([sys.executable,str(root/"probes"/"process-tools"/name)],cwd=str(root),
        capture_output=True,text=True,encoding="utf-8",errors="replace")
def read_rows(path):
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def write_rows(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

if CLONE.exists(): shutil.rmtree(CLONE)
(CLONE/"datasets").mkdir(parents=True)
shutil.copytree(TOOLS,CLONE/"probes"/"process-tools")
shutil.copytree(ROOT/"experiments"/"user-run",CLONE/"experiments"/"user-run")
for p in DATA.iterdir():
    if p.is_file(): shutil.copy2(p,CLONE/"datasets"/p.name)
for name in ("ROADMAP.md","mkdocs.yml","requirements-docs.txt"):
    shutil.copy2(ROOT/name,CLONE/name)
old=str(ROOT); new=str(CLONE)
for p in (CLONE/"probes"/"process-tools").glob("*.py"):
    text=p.read_text(encoding="utf-8-sig",errors="replace")
    p.write_text(text.replace(old,new),encoding="utf-8")

lock=CLONE/"datasets"/"aeig-prediction-lock.csv"
pred=CLONE/"datasets"/"aeig-prediction-log.csv"
lock_before=digest(lock)
baseline=run(CLONE,"freeze_aeig_static_rc.py")
lock_after_baseline=digest(lock)

rows=read_rows(pred)
for r in rows:
    if r.get("prediction_id")=="PRED-004":
        r["status"]="confirmed" if r.get("status")!="confirmed" else "pending"
        r["evidence"]="synthetic mutable-field change"
write_rows(pred,rows)
mutable=run(CLONE,"freeze_aeig_static_rc.py")
lock_after_mutable=digest(lock)

rows=read_rows(pred)
for r in rows:
    if r.get("prediction_id")=="PRED-004":
        r["prediction"]=r.get("prediction","")+" [tampered]"
write_rows(pred,rows)
immutable=run(CLONE,"freeze_aeig_static_rc.py")
lock_after_immutable=digest(lock)
checks={
    "baseline_freeze_pass":baseline.returncode==0,
    "baseline_lock_unchanged":lock_before==lock_after_baseline,
    "mutable_fields_allowed":mutable.returncode==0,
    "mutable_fields_do_not_relock":lock_before==lock_after_mutable,
    "immutable_change_rejected":immutable.returncode!=0 and "prediction lock mismatch" in (immutable.stdout+immutable.stderr),
    "immutable_rejection_preserves_lock":lock_before==lock_after_immutable,
}
passed=all(checks.values())
payload={"status":"PASS" if passed else "FAIL","date":date.today().isoformat(),"checks":checks,
         "immutable_exit":immutable.returncode}
OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---",
       "# Prediction Lock Integrity Self-Test","",f"State: **{payload['status']}**.","",
       "| Check | Result |","|---|---|"]
for name,ok in checks.items(): lines.append(f"| `{name}` | **{'PASS' if ok else 'FAIL'}** |")
lines += ["","Status/evidence are mutable post-observation fields. Prediction text and other immutable preregistration fields cannot be silently re-locked by the freeze tool."]
PAGE.write_text("\n".join(lines)+"\n",encoding="utf-8")
for name,ok in checks.items(): print("PASS" if ok else "FAIL",name)
if not passed: print((immutable.stdout+immutable.stderr)[-2500:])
print("AEIG PREDICTION LOCK SELFTEST:",payload["status"])
shutil.rmtree(CLONE,ignore_errors=True)
raise SystemExit(0 if passed else 2)
