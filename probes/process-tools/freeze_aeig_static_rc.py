from pathlib import Path
import csv, hashlib
ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; PKG=ROOT/"experiments"/"user-run"/"AEIG-1.0-L5"
MAN=DATA/"aeig-static-rc-manifest.csv"; LOCK=DATA/"aeig-prediction-lock.csv"
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def rel(p): return p.relative_to(ROOT).as_posix()
# Immutable prospective-prediction fields; status/evidence are intentionally excluded.
with (DATA/'aeig-prediction-log.csv').open(encoding='utf-8-sig',newline='') as f:
    preds=[r for r in csv.DictReader(f) if r.get('mode')=='prospective']
lock_fields=['prediction_id','mode','domain','source_experiment','prediction','falsified_by','locked_before_run']
locked_now=[{k:r.get(k,'') for k in lock_fields} for r in preds]
if LOCK.exists():
    with LOCK.open(encoding='utf-8-sig',newline='') as f:
        locked_existing=[{k:r.get(k,'') for k in lock_fields} for r in csv.DictReader(f)]
    if locked_existing != locked_now:
        raise SystemExit('prediction lock mismatch: refusing to overwrite pre-observation immutable fields')
else:
    with LOCK.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=lock_fields); w.writeheader(); w.writerows(locked_now)
items=[]
def add(p,role): items.append((p,role))
for p in sorted(PKG.rglob('*')):
    if p.is_file(): add(p,'canonical-operator-package')
tool_names=[
 'analyze_plugin_host_experiment.py','analyze_receipt_experiment.py','analyze_rg_trace_experiment.py',
 'analyze_scripting_reflection.py','verify_aeig_l5_user_run.py','finalize_aeig_l5_user_run.py',
 'diagnose_aeig_l5_user_run.py','status_aeig_l5_operator_run.py','complete_aeig_1_0_after_operator_run.py',
 'audit_aeig_l5_package.py','audit_pre_operator_readiness.py','selftest_aeig_release_pipeline.py','selftest_aeig_analyzers.py',
 'aeig_promotion_gate.py','selftest_aeig_promotion_success.py','selftest_aeig_promotion_transaction.py',
 'aeig_prediction_semantics.py','selftest_aeig_prediction_semantics.py',
 'selftest_aeig_prediction_lock_integrity.py',
 'aeig_file_transaction.py','selftest_aeig_file_transaction.py',
 'selftest_aeig_finalizer_success.py',
 'aeig_operator_session.py','selftest_aeig_operator_session.py',
 'report_prediction_status.py','audit_release_readiness.py','audit_repository_integrity.py',
 'report_roadmap_progress.py','promote_aeig_1_0.py','verify_aeig_static_rc.py','freeze_aeig_static_rc.py',
 'prepare_aeig_l5_user_run.py','build_master_surface_registry.py','preflight_aeig_l5_operator_run.py',
 'compute_static_rc_fingerprint.py','report_static_rc_fingerprint.py','report_static_release_candidate.py',
 'report_static_rc_identity.py','report_static_rc_status.py','generate_site_config.py',
 'audit_page_depth.py','build_bug_quirk_registry.py','patch_artie_observation_v2.py','patch_artie_observation_v3.py','patch_artie_observation_v4.py',
]
for n in tool_names: add(ROOT/'probes'/'process-tools'/n,'l5-analysis-or-promotion-tool')
for n in ['AEIG-L5-PREPARE.cmd','AEIG-L5-STATUS.cmd','AEIG-L5-FINISH.cmd']:
    add(ROOT/'experiments'/'user-run'/n,'canonical-operator-wrapper')
for n in [
 'ae-api-completeness-classification.csv','ae-api-guide-relation-classification.csv',
 'ae-master-surface-registry.csv','aeig-corpus-coverage-manifest.csv',
 'ae-plugin-capability-frontier.csv','ae-suite-negotiation-matrix.csv']:
    add(DATA/n,'static-evidence-index')
add(ROOT/'docs'/'reference'/'aeig-1.0-final-operator-run.md','canonical-operator-runbook')
add(ROOT/'research'/'bug-quirks.csv','documentation-quality-source')
add(DATA/'aeig-bug-quirk-registry.csv','documentation-quality-index')
add(LOCK,'prospective-prediction-lock')
for n in ['ROADMAP.md','mkdocs.yml','requirements-docs.txt','.github/workflows/docs.yml','docs/stylesheets/extra.css']:
    add(ROOT/n,'release-configuration')
rows=[]
for p,role in items:
    if not p.exists(): raise SystemExit(f'missing RC artifact: {p}')
    rows.append({'path':rel(p),'role':role,'bytes':p.stat().st_size,'sha256':sha(p)})
with MAN.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['path','role','bytes','sha256']); w.writeheader(); w.writerows(rows)
print('prediction lock',len(preds),'rows verified',LOCK)
print('static RC artifacts',len(rows),'manifest',MAN)
