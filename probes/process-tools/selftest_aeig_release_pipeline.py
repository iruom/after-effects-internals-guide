from pathlib import Path
from datetime import date
import hashlib, json, subprocess, sys

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"; DATA=ROOT/"datasets"; DOCS=ROOT/"docs"/"reference"
OUT=DATA/"aeig-release-pipeline-selftest.json"; PAGE=DOCS/"release-pipeline-selftest.md"
protected=[
 DATA/"aeig-prediction-log.csv", DATA/"aeig-domain-coverage.csv", DATA/"aeig-l5-domain-decisions.csv",
 ROOT/"experiments"/"observatory"/"manifests"/"EXP-CACHE-002.json",
 ROOT/"experiments"/"observatory"/"manifests"/"EXP-PLUGIN-001.json",
 ROOT/"experiments"/"observatory"/"manifests"/"EXP-RG-001.json",
 ROOT/"experiments"/"observatory"/"manifests"/"EXP-SCRIPT-001.json",
 ROOT/"README.md", ROOT/"docs"/"index.md", ROOT/"VERSION", DOCS/"aeig-1.0-release.md",
]

def digest(path):
    if not path.exists(): return "MISSING"
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def run(name):
    return subprocess.run([sys.executable,str(TOOLS/name)],capture_output=True,text=True,
                          encoding="utf-8",errors="replace")

def snap(): return {str(p):digest(p) for p in protected}
def doc_status(path):
    if not path.exists(): return "missing"
    for line in path.read_text(encoding="utf-8-sig",errors="replace").splitlines()[:12]:
        if line.startswith("status:"): return line.split(":",1)[1].strip()
    return "unknown"

rc0=run("verify_aeig_static_rc.py")
if rc0.returncode:
    print(rc0.stdout); print(rc0.stderr,file=sys.stderr)
    raise SystemExit("self-test requires a valid Static RC")
raw_files=[
 ROOT/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"/"receipt-matrix.tsv",
 ROOT/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"/"fixture-script.log",
 ROOT/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"/"fixture-output-A.avi",
 ROOT/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"/"fixture-output-B.avi",
 ROOT/"experiments"/"observatory"/"runs"/"EXP-PLUGIN-001"/"suite-acquisition.tsv",
 ROOT/"experiments"/"observatory"/"runs"/"EXP-RG-001"/"host-trace.log",
 ROOT/"experiments"/"observatory"/"runs"/"EXP-SCRIPT-001"/"runtime-reflection.tsv",
]
probe=Path(r"D:\Adobe\Adobe After Effects 2026\Support Files\Plug-ins\AEIG-Probes\AEIGReceiptArtie.aex")
if any(p.exists() for p in raw_files) or probe.exists():
    raise SystemExit("self-test requires no live operator capture and no installed temporary probe")
before=snap()
final=run("finalize_aeig_l5_user_run.py")
promote=run("promote_aeig_1_0.py")
after=snap()
changed=[p for p in before if before[p]!=after[p]]
rc=run("verify_aeig_static_rc.py")
checks={
 "finalizer_rejects_missing_capture": final.returncode != 0,
 "promotion_rejects_unready_state": promote.returncode != 0,
 "protected_state_unchanged": not changed,
 "static_rc_still_valid": rc.returncode == 0,
 "version_not_created": not (ROOT/"VERSION").exists(),
 "release_page_not_promoted": doc_status(DOCS/"aeig-1.0-release.md")!="release",
}
passed=all(checks.values())
payload={"status":"PASS" if passed else "FAIL","date":date.today().isoformat(),"checks":checks,
         "changed_protected_paths":changed,"finalizer_exit":final.returncode,"promotion_exit":promote.returncode}
OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---","# Release Pipeline Self-Test","",
       f"State: **{payload['status']}**.","","| Check | Result |","|---|---|"]
for k,v in checks.items(): lines.append(f"| `{k}` | **{'PASS' if v else 'FAIL'}** |")
if changed:
    lines += ["","## Unexpected protected mutations"]+[f"- `{p}`" for p in changed]
lines += ["","This test intentionally exercises the no-capture finalizer and blocked-promotion paths. Generated diagnostics/previews may change; prediction/model/release state must not."]
PAGE.write_text("\n".join(lines)+"\n",encoding="utf-8")
for k,v in checks.items(): print("PASS" if v else "FAIL",k)
print("finalizer_exit",final.returncode,"promotion_exit",promote.returncode,"changed",len(changed))
print("AEIG RELEASE PIPELINE SELFTEST:",payload["status"])
raise SystemExit(0 if passed else 2)
