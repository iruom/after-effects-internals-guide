from pathlib import Path
from datetime import date
import csv, json, subprocess, sys
from collections import Counter

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"; DATA=ROOT/"datasets"; DOCS=ROOT/"docs"/"reference"
OUT=DATA/"aeig-pre-operator-readiness.json"; PAGE=DOCS/"pre-operator-readiness.md"
EXPECTED_REMAINING={"state-identity","render-graph","cache"}
EXPECTED_PENDING={"PRED-004","PRED-005","PRED-006","PRED-007","PRED-008"}
EXPECTED_CONFIRMED={"PRED-009","PRED-010"}
checks=[]
repo_checks=[]; env_checks=[]

def run(name):
    p=subprocess.run([sys.executable,str(TOOLS/name)],capture_output=True,text=True,
                     encoding="utf-8",errors="replace")
    return p

def add(name,ok,detail,scope="repository"):
    row={"check":name,"ok":bool(ok),"detail":str(detail),"scope":scope}; checks.append(row)
    (repo_checks if scope=="repository" else env_checks).append(row)
def rows(path):
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def truth(v): return str(v).lower() in {"true","1","yes"}

rc=run("verify_aeig_static_rc.py"); add("static-rc",rc.returncode==0,(rc.stdout+rc.stderr).strip().replace("\n"," | "))
pkg=run("audit_aeig_l5_package.py"); add("canonical-package",pkg.returncode==0,(pkg.stdout+pkg.stderr).strip().replace("\n"," | ")[-900:])
integ=run("audit_repository_integrity.py"); add("repository-integrity",integ.returncode==0,(integ.stdout+integ.stderr).strip().replace("\n"," | ")[-900:])
pre=run("preflight_aeig_l5_operator_run.py"); add("operator-preflight",pre.returncode==0,(pre.stdout+pre.stderr).strip().replace("\n"," | ")[-1200:],"environment")
status=run("status_aeig_l5_operator_run.py")
status_json=DATA/"aeig-l5-operator-status.json"
state=json.loads(status_json.read_text(encoding="utf-8")) if status_json.exists() else {}
add("operator-phase",state.get("phase")=="READY_NOT_STARTED",state.get("phase","missing"),"environment")

progress=rows(DATA/"aeig-roadmap-progress.csv")
unmet={r["domain"] for r in progress if not truth(r.get("meets_1_0_target"))}
add("expected-domain-gap",len(progress)==27 and unmet==EXPECTED_REMAINING,f"{len(progress)-len(unmet)}/{len(progress)}; remaining={sorted(unmet)}")
coverage={r["domain"]:r for r in rows(DATA/"aeig-domain-coverage.csv")}
add("plugin-host-l5",coverage.get("plugin-host",{}).get("current_level")=="L5",coverage.get("plugin-host",{}).get("current_level","missing"))

pred=rows(DATA/"aeig-prediction-log.csv"); pros=[r for r in pred if r.get("mode")=="prospective"]
locked={r["prediction_id"] for r in pros if r.get("locked_before_run","").lower()=="true"}
pending={r["prediction_id"] for r in pros if r.get("status") in {"pending","inconclusive"}}
confirmed={r["prediction_id"] for r in pros if r.get("status")=="confirmed"}
refuted={r["prediction_id"] for r in pros if r.get("status")=="refuted"}
add("prediction-baseline",len(pros)==7 and locked=={r["prediction_id"] for r in pros} and pending==EXPECTED_PENDING and EXPECTED_CONFIRMED.issubset(confirmed) and not refuted,
    f"pros={len(pros)} locked={len(locked)} pending={sorted(pending)} confirmed={sorted(confirmed)} refuted={sorted(refuted)}")

release=run("audit_release_readiness.py")
rr=rows(DATA/"aeig-release-readiness.csv") if (DATA/"aeig-release-readiness.csv").exists() else []
blockers={r["check"] for r in rr if r.get("status")=="BLOCKER"}; warns={r["check"] for r in rr if r.get("status")=="WARN"}
add("expected-release-blockers",blockers=={"domain-targets","predictive-validation"} and not warns,
    f"blockers={sorted(blockers)} warnings={sorted(warns)} audit_exit={release.returncode}")
add("not-released",not (ROOT/"VERSION").exists() and not (DOCS/"aeig-1.0-release.md").exists(),
    f"VERSION={(ROOT/'VERSION').exists()} release_page={(DOCS/'aeig-1.0-release.md').exists()}")

selftest=run("selftest_aeig_release_pipeline.py"); add("release-pipeline-selftest",selftest.returncode==0,(selftest.stdout+selftest.stderr).strip().replace("\n"," | ")[-900:])
promotest=run("selftest_aeig_promotion_success.py"); add("promotion-gate-selftest",promotest.returncode==0,(promotest.stdout+promotest.stderr).strip().replace("\n"," | ")[-900:])
promotion_tx=run("selftest_aeig_promotion_transaction.py"); add("promotion-transaction-selftest",promotion_tx.returncode==0,(promotion_tx.stdout+promotion_tx.stderr).strip().replace("\n"," | ")[-900:])
predtest=run("selftest_aeig_prediction_semantics.py"); add("prediction-semantics-selftest",predtest.returncode==0,(predtest.stdout+predtest.stderr).strip().replace("\n"," | ")[-900:])
locktest=run("selftest_aeig_prediction_lock_integrity.py"); add("prediction-lock-selftest",locktest.returncode==0,(locktest.stdout+locktest.stderr).strip().replace("\n"," | ")[-900:])
sessiontest=run("selftest_aeig_operator_session.py"); add("operator-session-selftest",sessiontest.returncode==0,(sessiontest.stdout+sessiontest.stderr).strip().replace("\n"," | ")[-900:])
txtest=run("selftest_aeig_file_transaction.py"); add("file-transaction-selftest",txtest.returncode==0,(txtest.stdout+txtest.stderr).strip().replace("\n"," | ")[-900:])
analyzer_test=run("selftest_aeig_analyzers.py"); add("analyzer-selftest",analyzer_test.returncode==0,(analyzer_test.stdout+analyzer_test.stderr).strip().replace("\n"," | ")[-900:])

finger=(DATA/"aeig-static-rc-fingerprint.txt").read_text(encoding="utf-8-sig",errors="replace").strip() if (DATA/"aeig-static-rc-fingerprint.txt").exists() else ""
add("fingerprint-present",len(finger)==64 and all(c in "0123456789ABCDEF" for c in finger),finger or "missing")
repository_ready=all(c["ok"] for c in repo_checks)
environment_ready=all(c["ok"] for c in env_checks)
ready=repository_ready and environment_ready
state_name="READY_FOR_OPERATOR" if ready else ("REPOSITORY_READY_ENV_PENDING" if repository_ready else "BLOCKED")
payload={"status":state_name,"repository_ready":repository_ready,"operator_environment_ready":environment_ready,"date":date.today().isoformat(),"static_rc_fingerprint":finger,"checks":checks}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
counts=Counter("PASS" if c["ok"] else "BLOCK" for c in checks)
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---","# Pre-Operator Readiness","",
       f"State: **{payload['status']}**. Repository ready: **{repository_ready}**; operator environment ready: **{environment_ready}**. PASS **{counts['PASS']}**, BLOCK **{counts['BLOCK']}**.",
       f"Static RC fingerprint: `{finger}`.","","| Check | Scope | Result | Detail |","|---|---|---|---|"]
for c in checks: lines.append(f"| `{c['check']}` | {c['scope']} | **{'PASS' if c['ok'] else 'BLOCK'}** | {c['detail'].replace('|','/')} |")
lines += ["","A READY result means the repository is intentionally pre-release: exactly three core domains and five locked predictions remain for the canonical AE operator observation. This tool never installs the probe or starts After Effects."]
PAGE.write_text("\n".join(lines)+"\n",encoding="utf-8")
for c in checks: print(("PASS" if c["ok"] else "BLOCK"),c["check"],c["detail"][:280])
print("AEIG PRE-OPERATOR READINESS:",payload["status"])
print("wrote",OUT); print("wrote",PAGE)
raise SystemExit(0 if repository_ready else 2)
