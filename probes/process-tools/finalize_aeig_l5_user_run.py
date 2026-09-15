from pathlib import Path
import csv, json, subprocess, sys, hashlib, io
from collections import defaultdict
from aeig_prediction_semantics import pred004,pred005,pred006,pred007,pred008,pred009,pred010
from aeig_file_transaction import FileTransaction, atomic_write_text, recover_file_transaction

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"
DATA=ROOT/"datasets"
RUNS=ROOT/"experiments"/"observatory"/"runs"
PRED=DATA/"aeig-prediction-log.csv"
DEC=DATA/"aeig-l5-domain-decisions.csv"
SUMMARY=ROOT/"docs"/"reference"/"l5-user-run-finalization.md"
VERIFY_JSON=DATA/"aeig-l5-user-run-verification.json"
JOURNAL=DATA/".aeig-finalizer-transaction"
recovery=recover_file_transaction(JOURNAL)
if recovery["status"]!="none": print("finalizer transaction recovery",recovery)

def read_csv(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields=None):
    if fields is None: fields=list(rows[0]) if rows else []
    buf=io.StringIO(newline="")
    w=csv.DictWriter(buf,fieldnames=fields); w.writeheader(); w.writerows(rows)
    atomic_write_text(path,buf.getvalue())

def truth(v): return str(v).lower() in {"true","1","yes"}
static=subprocess.run([sys.executable,str(TOOLS/"verify_aeig_static_rc.py")],capture_output=True,text=True,encoding="utf-8",errors="replace")
print(static.stdout,end="")
if static.stderr: print(static.stderr,file=sys.stderr,end="")
if static.returncode:
    raise SystemExit("Static RC verification failed; refusing L5 finalization.")
verify=subprocess.run([sys.executable,str(TOOLS/"verify_aeig_l5_user_run.py")],capture_output=True,text=True,encoding="utf-8",errors="replace")
print(verify.stdout,end="")
if verify.stderr: print(verify.stderr,file=sys.stderr,end="")
verification=json.loads(VERIFY_JSON.read_text(encoding="utf-8")) if VERIFY_JSON.exists() else {}
fixture_ok=bool(verification.get("all_required_checks_passed",False))
capture_complete=bool(verification.get("capture_complete",fixture_ok))
semantic_ok=bool(verification.get("semantic_checks_passed",fixture_ok))

receipt=read_csv(DATA/"exp-cache-002-receipt-matrix.csv")
attempts=[r for r in receipt if r.get("kind")=="CHECK"]
checks=[r for r in attempts if r.get("error")=="0"]
by_pass=defaultdict(lambda:defaultdict(set))
for r in attempts:
    key=(r.get("generated"),r.get("requested"),r.get("geometry_check"))
    by_pass[r.get("pass")][key].add((r.get("error"),r.get("status")))
prefix_ok=bool(attempts) and {"A","B"}.issubset(by_pass) and all(truth(r.get("matches_prefix_prediction")) for r in attempts)
receipt_stable=(bool(attempts) and {"A","B"}.issubset(by_pass) and set(by_pass["A"])==set(by_pass["B"]) and
                all(by_pass["A"][k]==by_pass["B"][k] for k in by_pass["A"]))

rg=read_csv(DATA/"exp-rg-001-trace-summary.csv")
RG_CATS=["RenderNode.RG_CacheNodeBase","RenderNode.RG_XformNode"]
ID_CATS=["MixHashGuid","TDB_StreamBase","BEE_Eval"]
CACHE_CATS=["BEE_Cache","BEE_CacheLog","BEE_WorkQueue","DiskCache"]
agg={p:{c:0 for c in RG_CATS+ID_CATS+CACHE_CATS} for p in ("A","B")}
trace_fp={p:{"identity":[],"rg_cache":[],"all":[]} for p in ("A","B")}
for r in rg:
    p=r.get("pass")
    if p not in agg: continue
    for c in agg[p]: agg[p][c]+=int(r.get(c,0) or 0)
    if r.get("identity_sha256"): trace_fp[p]["identity"].append(r["identity_sha256"])
    if r.get("rg_cache_sha256"): trace_fp[p]["rg_cache"].append(r["rg_cache_sha256"])
    if r.get("all_target_sha256"): trace_fp[p]["all"].append(r["all_target_sha256"])
rg_present={p:sum(agg[p][c] for c in RG_CATS)>0 for p in agg}
bee_present={p:sum(agg[p][c] for c in ("BEE_Eval","BEE_Cache","BEE_CacheLog","BEE_WorkQueue"))>0 for p in agg}
guid_present={p:agg[p]["MixHashGuid"]>0 for p in agg}
tdb_present={p:agg[p]["TDB_StreamBase"]>0 for p in agg}
eval_present={p:agg[p]["BEE_Eval"]>0 for p in agg}
id_present={p:(guid_present[p] and tdb_present[p] and eval_present[p]) for p in agg}
cache_present={p:sum(agg[p][c] for c in ("BEE_Cache","BEE_CacheLog","DiskCache"))>0 for p in agg}
workqueue_present={p:agg[p]["BEE_WorkQueue"]>0 for p in agg}
rg_cache_present={p:(rg_present[p] and cache_present[p] and workqueue_present[p]) for p in agg}
target_present={p:sum(agg[p].values())>0 for p in agg}
target_groups_complete={p:(bee_present[p] and rg_present[p] and tdb_present[p] and guid_present[p]) for p in agg}
id_count_diff=tuple(agg["A"][c] for c in ID_CATS)!=tuple(agg["B"][c] for c in ID_CATS)
rg_count_diff=tuple(agg["A"][c] for c in RG_CATS+CACHE_CATS)!=tuple(agg["B"][c] for c in RG_CATS+CACHE_CATS)
id_content_diff=tuple(sorted(trace_fp["A"]["identity"]))!=tuple(sorted(trace_fp["B"]["identity"]))
rg_content_diff=tuple(sorted(trace_fp["A"]["rg_cache"]))!=tuple(sorted(trace_fp["B"]["rg_cache"]))
id_diff=all(id_present.values()) and (id_count_diff or id_content_diff)
rg_diff=all(rg_cache_present.values()) and (rg_count_diff or rg_content_diff)

plugin=read_csv(DATA/"exp-plugin-001-suite-acquisition.csv")
sets=defaultdict(set)
for r in plugin:
    if truth(r.get("success")): sets[r.get("label")].add(int(r.get("selector",0)))
labels={r.get("label") for r in plugin if r.get("label")}
patterns={tuple(sorted(sets.get(label,set()))) for label in labels}
plugin_complete=len(plugin)==1536 and len(labels)==48
family_specific=plugin_complete and len(patterns)>1
plugin_success=plugin_complete and any(sets.values())

preds=read_csv(PRED)
updates={
 "PRED-004":(pred004(prefix_ok),f"prefix_ok={prefix_ok}; attempts={len(attempts)}; successful={len(checks)}"),
 "PRED-005":(pred005(receipt_stable),f"receipt_stable={receipt_stable}"),
 "PRED-006":(pred006(target_groups_complete,target_present),f"target_groups_complete={target_groups_complete}; target_present={target_present}; bee={bee_present}; rg={rg_present}; tdb={tdb_present}; guid={guid_present}"),
 "PRED-007":(pred007(id_present,id_diff),f"identity_complete={id_present}; identity_counts={agg}; identity_fingerprints={trace_fp}"),
 "PRED-008":(pred008(rg_cache_present,rg_diff),f"rg_cache_workqueue_complete={rg_cache_present}; rg_cache_counts={agg}; rg_cache_fingerprints={trace_fp}"),
 "PRED-009":(pred009(plugin_complete,family_specific),f"patterns={len(patterns)} labels={len(labels)}"),
 "PRED-010":(pred010(plugin_complete,family_specific),f"patterns={len(patterns)}"),
}
receipt_ready=verification.get("receipt_analysis",{}).get("exit")==0
rg_ready=verification.get("rg_analysis",{}).get("exit")==0
plugin_ready=verification.get("plugin_analysis",{}).get("exit")==0 and plugin_complete
if not receipt_ready:
    updates.pop("PRED-004",None); updates.pop("PRED-005",None)
if not rg_ready:
    for k in ("PRED-006","PRED-007","PRED-008"): updates.pop(k,None)
if not plugin_ready:
    updates.pop("PRED-009",None); updates.pop("PRED-010",None)

if capture_complete:
    for r in preds:
        if r["prediction_id"] in updates:
            r["status"],r["evidence"]=updates[r["prediction_id"]]
else:
    print("canonical evidence commit skipped: capture incomplete")

pred_status={r["prediction_id"]:r["status"] for r in preds}
def refuted(ids): return any(pred_status.get(i)=="refuted" for i in ids)

decisions=[
 {"domain":"state-identity","evidence_ready":receipt_ready and rg_ready and all(id_present.values()),"model_revision_required":refuted(["PRED-004","PRED-007"]),"reason":f"receipt_captured={receipt_ready}; prefix_ok={prefix_ok}; identity_complete={id_present}; identity_footprint_diff={id_diff}"},
 {"domain":"cache","evidence_ready":receipt_ready and rg_ready and all(cache_present.values()),"model_revision_required":refuted(["PRED-005"]),"reason":f"receipt_captured={receipt_ready}; receipt_stable={receipt_stable}; cache_trace={cache_present}; workqueue={workqueue_present}"},
 {"domain":"render-graph","evidence_ready":rg_ready and all(rg_present.values()),"model_revision_required":refuted(["PRED-006","PRED-008"]),"reason":f"rg_trace={rg_present}; mutation_count_diff={rg_diff}"},
 {"domain":"plugin-host","evidence_ready":plugin_ready and plugin_success,"model_revision_required":refuted(["PRED-009","PRED-010"]),"reason":f"attempts={len(plugin)} labels={len(labels)} patterns={len(patterns)}"},
]
decision_out=DEC if capture_complete else DATA/"aeig-l5-domain-decisions-preview.csv"
if not capture_complete:
    write_csv(decision_out,decisions,["domain","evidence_ready","model_revision_required","reason"])

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest().upper()

def write_hashes(run_dir,names):
    hashes={}
    for name in names:
        p=run_dir/name
        if p.exists() and p.is_file(): hashes[name]=sha(p)
    (run_dir/"sha256.txt").write_text("".join(f"{v}  {k}\n" for k,v in hashes.items()),encoding="utf-8")
    return hashes

cache_run=RUNS/"EXP-CACHE-002"; plugin_run=RUNS/"EXP-PLUGIN-001"
rg_run=RUNS/"EXP-RG-001"; script_run=RUNS/"EXP-SCRIPT-001"
env=cache_run/"environment.txt"; hashes={}; env_data={}
if capture_complete:
    if env.exists():
        import shutil
        for d in (plugin_run,rg_run,script_run):
            d.mkdir(parents=True,exist_ok=True); shutil.copy2(env,d/"environment.txt")
    hashes={
     "EXP-CACHE-002":write_hashes(cache_run,["receipt-matrix.tsv","fixture-script.log","fixture-output-A.avi","fixture-output-B.avi","environment.txt"]),
     "EXP-PLUGIN-001":write_hashes(plugin_run,["suite-acquisition.tsv","environment.txt"]),
     "EXP-RG-001":write_hashes(rg_run,["host-trace.log","trace-control.tsv","environment.txt"]),
     "EXP-SCRIPT-001":write_hashes(script_run,["runtime-reflection.tsv","environment.txt"]),
    }
    if env.exists():
        for line in env.read_text(encoding="utf-8-sig",errors="replace").splitlines():
            if "=" in line:
                k,v=line.split("=",1); env_data[k.strip()]=v.strip()

def stage_manifest(exp_id,ready,conclusion):
    p=ROOT/"experiments"/"observatory"/"manifests"/f"{exp_id}.json"
    if not p.exists() or not (ready and capture_complete): return None
    m=json.loads(p.read_text(encoding="utf-8-sig"))
    m["status"]="observed"
    if env_data:
        m.setdefault("environment",{})["ae_version"]=env_data.get("app.version",m.get("environment",{}).get("ae_version",""))
        m["environment"]["os"]=env_data.get("os",m.get("environment",{}).get("os",""))
        m["environment"]["captured_build_number"]=env_data.get("app.buildNumber","")
        m["environment"]["captured_build_name"]=env_data.get("app.buildName","")
        m["environment"]["captured_gpu_accel_type"]=env_data.get("gpuAccelType","")
    m["result"]={"conclusion":conclusion,"raw_hashes":hashes.get(exp_id,{}),"finalized_by":"finalize_aeig_l5_user_run.py"}
    return p,m

script_ready=verification.get("script_analysis",{}).get("exit")==0
staged=[x for x in [
    stage_manifest("EXP-CACHE-002",receipt_ready,f"prefix_ok={prefix_ok}; receipt_stable={receipt_stable}; attempts={len(attempts)}; successful={len(checks)}"),
    stage_manifest("EXP-PLUGIN-001",plugin_ready,f"attempts={len(plugin)}; families={len(labels)}; selector_patterns={len(patterns)}"),
    stage_manifest("EXP-RG-001",rg_ready,f"rg_present={rg_present}; id_present={id_present}; cache_present={cache_present}; diff_rg={rg_diff}; diff_identity={id_diff}"),
    stage_manifest("EXP-SCRIPT-001",script_ready,"Runtime Reflection capture parsed and compared with the scripting documentation atlas."),
] if x is not None]
canonical_committed=False
if capture_complete:
    canonical_paths=[PRED,DEC]+[p for p,_ in staged]
    with FileTransaction(canonical_paths,journal_dir=JOURNAL):
        write_csv(PRED,preds,list(preds[0]) if preds else None)
        write_csv(DEC,decisions,["domain","evidence_ready","model_revision_required","reason"])
        for path,manifest in staged:
            atomic_write_text(path,json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    canonical_committed=True
    subprocess.run([sys.executable,str(TOOLS/"report_prediction_status.py")],check=False)

pros=[r for r in preds if r.get("mode")=="prospective"]
confirmed=sum(r.get("status")=="confirmed" for r in pros)
pending=sum(r.get("status")=="pending" for r in pros)
refuted_count=sum(r.get("status")=="refuted" for r in pros)
all_evidence=all(truth(r["evidence_ready"]) for r in decisions)
revision_due=any(truth(r["model_revision_required"]) for r in decisions)
from datetime import date
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---","# L5 User-Run Finalization","",
       f"Capture completeness: **{'PASS' if capture_complete else 'INCOMPLETE'}**.",
       f"Semantic gate: **{'PASS' if semantic_ok else 'FAILED/INCONCLUSIVE'}**.",
       f"Canonical evidence commit: **{'YES' if canonical_committed else 'NO'}**.",
       f"Core-domain evidence ready: **{sum(truth(r['evidence_ready']) for r in decisions)}/4**.",
       f"Prospective predictions: confirmed **{confirmed}**, pending **{pending}**, refuted-unrevised **{refuted_count}**.","",
       "| Domain | Evidence ready | Model revision required | Reason |","|---|---|---|---|"]
for r in decisions:
    lines.append(f"| `{r['domain']}` | {r['evidence_ready']} | {r['model_revision_required']} | {r['reason'].replace('|','/')} |")
lines += ["","## Promotion rule","This finalizer does not silently promote domain coverage. Promotion requires all four evidence gates, no unrevised refutation for the affected model, and the separate AEIG 1.0 promotion guard."]
SUMMARY.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("decisions",decisions)
print("prospective confirmed",confirmed,"pending",pending,"refuted",refuted_count)
print("canonical transaction",("COMMIT" if canonical_committed else "SKIP")); print("wrote",decision_out); print("wrote",SUMMARY)
ready=fixture_ok and all_evidence and not revision_due
raise SystemExit(0 if ready else 3)
