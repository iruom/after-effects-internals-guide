from pathlib import Path
from datetime import datetime
import hashlib, shutil, subprocess, sys
from aeig_operator_session import build_session_values, write_session

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
RUNS=ROOT/"experiments"/"observatory"/"runs"
DATA=ROOT/"datasets"
SESSION=DATA/"aeig-l5-operator-session.env"
FINGER=DATA/"aeig-static-rc-fingerprint.txt"
stamp=datetime.now().strftime("%Y%m%d-%H%M%S-%f")

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest().upper()

# Refuse archival while AE or the temporary probe may be live. The outer wrapper also checks this,
# but this script is safe when invoked directly from 00_PREPARE_RESULTS.cmd.
try:
    task=subprocess.run(["tasklist","/FO","CSV","/NH"],capture_output=True,text=True,encoding="utf-8",errors="replace")
    procs=task.stdout.lower()
except Exception as e:
    raise SystemExit(f"process query failed: {type(e).__name__}")
active=[exe for exe in ("afterfx.exe","afterfx.com","aerender.exe") if exe in procs]
probe=Path(r"D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\AEIG-Probes\AEIGReceiptArtie.aex")
if active: raise SystemExit("refusing archival while AE process is active: "+",".join(active))
if probe.exists(): raise SystemExit("refusing archival while temporary AEIG probe is installed")
verify=subprocess.run([sys.executable,str(ROOT/"probes"/"process-tools"/"verify_aeig_static_rc.py")],capture_output=True,text=True,encoding="utf-8",errors="replace")
if verify.returncode:
    raise SystemExit("refusing session issuance because Static RC verification failed: "+(verify.stdout+verify.stderr).strip().replace("\n"," | "))
fingerprint=FINGER.read_text(encoding="utf-8-sig",errors="replace").strip() if FINGER.exists() else ""
if len(fingerprint)!=64:
    raise SystemExit("refusing session issuance because Static RC fingerprint is missing/invalid")
aex=ROOT/"experiments"/"user-run"/"AEIG-1.0-L5"/"plugin"/"AEGP"/"AEIGReceiptArtie.aex"
if not aex.exists(): raise SystemExit("canonical AEX missing")
aex_hash=sha256(aex)
targets={
 "EXP-CACHE-002":["receipt-matrix.tsv","fixture-script.log","fixture-output-A.avi","fixture-output-B.avi","environment.txt","analysis-summary.md","sha256.txt"],
 "EXP-PLUGIN-001":["suite-acquisition.tsv","analysis-summary.md","sha256.txt","environment.txt"],
 "EXP-RG-001":["host-trace.log","trace-control.tsv","current-pass.txt","analysis-summary.md","sha256.txt","environment.txt"],
 "EXP-SCRIPT-001":["runtime-reflection.tsv","analysis-summary.md","sha256.txt","environment.txt"],
}
moved=[]
for exp,names in targets.items():
    base=RUNS/exp; archive=base/"prior-runs"/stamp
    for name in names:
        src=base/name
        if not src.exists(): continue
        archive.mkdir(parents=True,exist_ok=True)
        dst=archive/name; shutil.move(str(src),str(dst)); moved.append((src,dst))

# Derived run state is archived separately so stale verification cannot masquerade as a new run.
derived=[
 "aeig-l5-user-run-verification.json","aeig-l5-user-run-diagnostic.json",
 "aeig-l5-domain-decisions.csv","aeig-l5-domain-decisions-preview.csv","aeig-l5-operator-status.json",
 "exp-cache-002-receipt-matrix.csv","exp-plugin-001-suite-acquisition.csv",
 "exp-rg-001-trace-summary.csv","exp-script-001-runtime-reflection.csv",
 "aeig-l5-operator-session.env",
]
derived_archive=DATA/"history"/"l5-user-runs"/stamp
derived_moved=[]
for name in derived:
    src=DATA/name
    if not src.exists(): continue
    derived_archive.mkdir(parents=True,exist_ok=True)
    dst=derived_archive/name; shutil.move(str(src),str(dst)); derived_moved.append((src,dst))
summary=ROOT/"docs"/"reference"/"l5-user-run-finalization.md"
if summary.exists():
    derived_archive.mkdir(parents=True,exist_ok=True)
    dst=derived_archive/"l5-user-run-finalization.md"
    shutil.move(str(summary),str(dst)); derived_moved.append((summary,dst))

print("archive_stamp",stamp)
print("raw_archived",len(moved))
for src,dst in moved: print(src.name,"->",dst)
print("derived_archived",len(derived_moved))
for src,dst in derived_moved: print(src.name,"->",dst)

session_values=build_session_values(fingerprint,aex_hash)
write_session(SESSION,session_values)
print("operator_session",session_values["session_id"])
print("operator_session_fingerprint",session_values["static_rc_fingerprint"])
print("operator_session_file",SESSION)
