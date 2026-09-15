from pathlib import Path
from datetime import date
import csv, json, os, shutil, subprocess, sys, tempfile

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
TOOLS=ROOT/"probes"/"process-tools"; DATA=ROOT/"datasets"; DOCS=ROOT/"docs"/"reference"
OUT=DATA/"aeig-analyzer-selftest.json"; PAGE=DOCS/"analyzer-selftest.md"

def run(name,temp):
    env=os.environ.copy(); env["AEIG_ROOT"]=str(temp)
    return subprocess.run([sys.executable,str(TOOLS/name)],env=env,capture_output=True,text=True,
                          encoding="utf-8",errors="replace")
def write(path,text): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding="utf-8")
def check(name,ok,detail=""): return {"check":name,"ok":bool(ok),"detail":detail}

def receipt_text(api_error=False,drop_last=False):
    vals=(-1,0,1,2,3); lines=[]
    for rp in ("A","B"):
        for g in vals:
            for n in vals:
                for geom in (0,1):
                    gg=3 if g==-1 else g; nn=3 if n==-1 else n; status=1 if gg>=nn else 2; err=0
                    if api_error and rp=="B" and g==0 and n==1 and geom==0: status=-99; err=123
                    lines.append(f"1\t{rp}\tCHECK\t3\t{g}\t{n}\t{geom}\t{status}\t{err}")
    if drop_last: lines.pop()
    return "\n".join(lines)+"\n"
checks=[]
with tempfile.TemporaryDirectory(prefix="aeig-analyzer-selftest-",dir=str(ROOT/"scratch")) as td:
    T=Path(td); D=T/"datasets"; D.mkdir(parents=True)
    for name in ("ae-sdk-25.6-suite-versions.csv","ae-sdk-25.6-suite-names.csv","ae-script-expression-api-atlas.csv"):
        shutil.copy2(DATA/name,D/name)

    cache=T/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"
    log=cache/"receipt-matrix.tsv"; write(log,receipt_text())
    p=run("analyze_receipt_experiment.py",T)
    rows=list(csv.DictReader((D/"exp-cache-002-receipt-matrix.csv").open(encoding="utf-8-sig",newline=""))) if (D/"exp-cache-002-receipt-matrix.csv").exists() else []
    checks.append(check("receipt-complete",p.returncode==0 and len([r for r in rows if r.get("kind")=="CHECK"])==100,p.stdout[-500:]))
    write(log,receipt_text(api_error=True)); p=run("analyze_receipt_experiment.py",T)
    rows=list(csv.DictReader((D/"exp-cache-002-receipt-matrix.csv").open(encoding="utf-8-sig",newline="")))
    checks.append(check("receipt-api-error-is-semantic",p.returncode==0 and sum(r.get("status_name")=="API_ERROR" for r in rows)==1,p.stdout[-500:]))
    write(log,receipt_text(drop_last=True)); p=run("analyze_receipt_experiment.py",T)
    checks.append(check("receipt-missing-key-rejected",p.returncode!=0,p.stdout[-500:]))
    dup_lines=receipt_text().splitlines(); write(log,"\n".join(dup_lines+[dup_lines[0]])+"\n")
    p=run("analyze_receipt_experiment.py",T)
    checks.append(check("receipt-duplicate-key-rejected",p.returncode!=0,p.stdout[-500:]))

    plugin=T/"experiments"/"observatory"/"runs"/"EXP-PLUGIN-001"; plugin.mkdir(parents=True)
    with (D/"ae-sdk-25.6-suite-names.csv").open(encoding="utf-8",newline="") as f:
        labels=sorted({r["suite_macro"].removeprefix("k") for r in csv.DictReader(f)})
    plines=[]
    for label in labels:
        for selector in range(1,33):
            err=0 if selector==1 else 1; ptr="0x1" if err==0 else "0"
            plines.append(f"1\t26\t3\t{label}\t{label}\t{selector}\t{err}\t{ptr}")
    write(plugin/"suite-acquisition.tsv","\n".join(plines)+"\n")
    p=run("analyze_plugin_host_experiment.py",T)
    checks.append(check("plugin-grid-complete",p.returncode==0 and len(labels)==48,p.stdout[-500:]))
    write(plugin/"suite-acquisition.tsv","\n".join(plines+[plines[0]])+"\n")
    p=run("analyze_plugin_host_experiment.py",T)
    checks.append(check("plugin-duplicate-rejected",p.returncode!=0,p.stdout[-500:]))

    rg=T/"experiments"/"observatory"/"runs"/"EXP-RG-001"; rg.mkdir(parents=True)
    trace=[]; ctl=[]
    cats=["BEE_Eval","BEE_Cache","BEE_WorkQueue","MixHashGuid","RenderNode.RG_CacheNodeBase","RenderNode.RG_XformNode","TDB_StreamBase","DiskCache"]
    for seq,rp in ((1,"A"),(2,"B")):
        trace.append(f"AEIG_TRACE_BEGIN\tseq={seq}\tpass={rp}\tpid=1")
        trace += [f"{c}\tsemantic={rp}" for c in cats]
        trace.append(f"AEIG_TRACE_END\tseq={seq}\tpass={rp}\tpid=1")
        ctl += [f"1\t{seq}\t{rp}\tBEGIN\t-\t1",f"1\t{seq}\t{rp}\tEND\t-\t1"]
    write(rg/"host-trace.log","\n".join(trace)+"\n"); write(rg/"trace-control.tsv","\n".join(ctl)+"\n")
    p=run("analyze_rg_trace_experiment.py",T)
    checks.append(check("rg-complete",p.returncode==0 and "target_category_lines" in p.stdout,p.stdout[-500:]))
    with (T/"datasets"/"exp-rg-001-trace-summary.csv").open(encoding="utf-8",newline="") as f:
        rg_rows=list(csv.DictReader(f))
    byp={r["pass"]:r for r in rg_rows}
    fp_diff=(byp.get("A",{}).get("identity_sha256")!=byp.get("B",{}).get("identity_sha256") and
             byp.get("A",{}).get("rg_cache_sha256")!=byp.get("B",{}).get("rg_cache_sha256"))
    checks.append(check("rg-content-fingerprint-diff",fp_diff,str({p:(byp.get(p,{}).get("identity_sha256"),byp.get(p,{}).get("rg_cache_sha256")) for p in ("A","B")})))
    mismatched=list(trace); mismatched[0]=mismatched[0].replace("pid=1","pid=2")
    write(rg/"host-trace.log","\n".join(mismatched)+"\n"); p=run("analyze_rg_trace_experiment.py",T)
    checks.append(check("rg-trace-control-key-mismatch-rejected",p.returncode!=0,p.stdout[-500:]))
    zero=[]
    for seq,rp in ((1,"A"),(2,"B")):
        zero += [f"AEIG_TRACE_BEGIN\tseq={seq}\tpass={rp}\tpid=1","unrelated trace line",f"AEIG_TRACE_END\tseq={seq}\tpass={rp}\tpid=1"]
    write(rg/"host-trace.log","\n".join(zero)+"\n"); p=run("analyze_rg_trace_experiment.py",T)
    checks.append(check("rg-zero-category-is-semantic",p.returncode==0 and "semantic_observation absent" in p.stdout,p.stdout[-500:]))
    bad_trace=trace[:-1]
    write(rg/"host-trace.log","\n".join(bad_trace)+"\n"); p=run("analyze_rg_trace_experiment.py",T)
    checks.append(check("rg-incomplete-marker-rejected",p.returncode!=0,p.stdout[-500:]))

    script=T/"experiments"/"observatory"/"runs"/"EXP-SCRIPT-001"; script.mkdir(parents=True)
    labels=["Application","Project","CompItem","AVLayer","RenderQueue","RenderQueueItem","OutputModule"]
    header="label\tkind\tname\ttype\tdataType\tisReadOnly"
    rlines=[header]+[f"{label}\tproperty\tname\treadwrite\tstring\tfalse" for label in labels]
    write(script/"runtime-reflection.tsv","\n".join(rlines)+"\n")
    p=run("analyze_scripting_reflection.py",T)
    checks.append(check("reflection-complete",p.returncode==0,p.stdout[-500:]))
    write(script/"runtime-reflection.tsv","\n".join(rlines[:-1])+"\n")
    p=run("analyze_scripting_reflection.py",T)
    checks.append(check("reflection-missing-label-rejected",p.returncode!=0,p.stdout[-500:]))

passed=all(c["ok"] for c in checks)
payload={"status":"PASS" if passed else "FAIL","date":date.today().isoformat(),"checks":checks}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["---","status: generated",f"last_verified: {date.today().isoformat()}","---","# Analyzer Self-Test","",f"State: **{payload['status']}**.","","| Check | Result |","|---|---|"]
for c in checks: lines.append(f"| `{c['check']}` | **{'PASS' if c['ok'] else 'FAIL'}** |")
lines += ["","Synthetic evidence is executed under a temporary AEIG_ROOT; no live operator capture is modified."]
PAGE.write_text("\n".join(lines)+"\n",encoding="utf-8")
for c in checks: print("PASS" if c["ok"] else "FAIL",c["check"])
print("AEIG ANALYZER SELFTEST:",payload["status"])
raise SystemExit(0 if passed else 2)
