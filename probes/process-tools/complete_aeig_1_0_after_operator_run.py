from pathlib import Path
import json, subprocess, sys
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"; DATA=ROOT/"datasets"

def run(name):
    p=subprocess.run([sys.executable,str(TOOLS/name)],capture_output=True,text=True,
                     encoding="utf-8",errors="replace")
    print(f"[{name}] exit={p.returncode}")
    if p.stdout: print(p.stdout.rstrip())
    if p.stderr: print(p.stderr.rstrip(),file=sys.stderr)
    return p

def verification():
    p=DATA/"aeig-l5-user-run-verification.json"
    if not p.exists(): return {}
    try: return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception: return {}

if run("verify_aeig_static_rc.py").returncode:
    raise SystemExit("Static RC changed; refusing post-run completion.")
run("diagnose_aeig_l5_user_run.py")
raw=ROOT/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"/"fixture-script.log"
if not raw.exists(): raise SystemExit("No operator raw capture yet; finalizer was not run.")
final=run("finalize_aeig_l5_user_run.py")
v=verification(); complete=bool(v.get("capture_complete",False))
if not complete:
    raise SystemExit("Operator capture is mechanically incomplete. Preserve raw evidence; diagnose before any rerun.")
if final.returncode:
    raise SystemExit("Capture is complete, but an evidence/prediction/model gate blocked promotion. Do not discard or rerun automatically; review the committed observation.")
promote=run("promote_aeig_1_0.py")
if promote.returncode:
    raise SystemExit("Promotion guard refused AEIG 1.0 after a complete observation. Repository should remain pre-1.0; inspect prediction/model gates.")
integ=run("audit_repository_integrity.py"); release=run("audit_release_readiness.py")
if integ.returncode or release.returncode:
    raise SystemExit("Post-promotion audit failed; promotion guard should have rolled back release state.")
version=ROOT/"VERSION"
if not version.exists() or version.read_text(encoding="utf-8-sig").strip()!="1.0":
    raise SystemExit("Promotion returned success but VERSION is not 1.0.")
print("AEIG 1.0 COMPLETION ORCHESTRATOR: PASS")
print("VERSION",version.read_text(encoding="utf-8-sig").strip())
