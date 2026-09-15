from pathlib import Path
import csv, sys
from collections import Counter, defaultdict
import os

ROOT=Path(os.environ.get("AEIG_ROOT",r"D:\Developer\After Effects Internals Guide"))
RUN=ROOT/"experiments"/"observatory"/"runs"/"EXP-CACHE-002"
LOG=RUN/"receipt-matrix.tsv"; OUT=ROOT/"datasets"/"exp-cache-002-receipt-matrix.csv"
SUMMARY=RUN/"analysis-summary.md"; STATUS={0:"INVALID",1:"VALID",2:"VALID_BUT_INCOMPLETE"}

if not LOG.exists(): print("not-run: missing",LOG); raise SystemExit(2)
rows=[]; malformed=0
for line in LOG.read_text(encoding="utf-8-sig",errors="replace").splitlines():
    parts=line.split("\t")
    if len(parts)==9:
        pid,run_pass,kind,count,generated,requested,geom,status,err=parts
    elif len(parts)==8:
        pid,kind,count,generated,requested,geom,status,err=parts; run_pass="?"
    else:
        malformed+=1; continue
    try:
        r={"pid":pid,"pass":run_pass,"kind":kind,"num_effects":int(count),"generated":int(generated),
           "requested":int(requested),"geometry_check":int(geom),"status":int(status),"error":int(err)}
    except ValueError:
        malformed+=1; continue
    rows.append(r)

for r in rows:
    if r["kind"]=="CHECK":
        g=r["num_effects"] if r["generated"]==-1 else r["generated"]
        n=r["num_effects"] if r["requested"]==-1 else r["requested"]
        predicted=1 if g>=n else 2
        r["status_name"]=STATUS.get(r["status"],f"UNKNOWN_{r['status']}") if r["error"]==0 else "API_ERROR"
        r["prefix_prediction"]=STATUS[predicted]
        r["matches_prefix_prediction"]=(r["error"]==0 and r["status"]==predicted)
    else:
        r["status_name"]=STATUS.get(r["status"],"") if r["status"]>=0 else ""
        r["prefix_prediction"]=""; r["matches_prefix_prediction"]=""
fields=list(rows[0]) if rows else ["pid","pass","kind","num_effects","generated","requested","geometry_check","status","error","status_name","prefix_prediction","matches_prefix_prediction"]
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

attempts=[r for r in rows if r["kind"]=="CHECK"]
success=[r for r in attempts if r["error"]==0]
matched=[r for r in attempts if r["matches_prefix_prediction"] is True]
mismatch=[r for r in attempts if r["matches_prefix_prediction"] is False]
api_errors=[r for r in attempts if r["error"]!=0]
counts=Counter(r["status_name"] for r in attempts)
by_pass=defaultdict(lambda:{"attempts":0,"success":0,"matches":0,"keys":set(),"counts":set(),"statuses":Counter()})
for r in attempts:
    x=by_pass[r["pass"]]; x["attempts"]+=1; x["success"]+=int(r["error"]==0); x["matches"]+=int(r["matches_prefix_prediction"] is True)
    x["keys"].add((r["generated"],r["requested"],r["geometry_check"])); x["counts"].add(r["num_effects"]); x["statuses"][r["status_name"]]+=1

# The canonical fixture has exactly three effects. Each receipt matrix attempts 5x5x2 = 50 keys:
# prefixes 0,1,2,3 plus ALL_EFFECTS(-1), for both generation and check, with geometry off/on.
expected_values={-1,0,1,2,3}; expected_keys={(g,n,geom) for g in expected_values for n in expected_values for geom in (0,1)}
coverage={p:{"effect_counts":sorted(x["counts"]),"unique_keys":len(x["keys"]),"missing_keys":len(expected_keys-x["keys"])} for p,x in by_pass.items()}
mechanical_ok=(malformed==0 and {"A","B"}.issubset(by_pass) and all(by_pass[p]["counts"]=={3} and by_pass[p]["keys"]==expected_keys and by_pass[p]["attempts"]==len(expected_keys) for p in ("A","B")))

lines=["# EXP-CACHE-002 analysis","",
 f"- Parsed rows: **{len(rows)}**",f"- Malformed rows: **{malformed}**",f"- CHECK attempts: **{len(attempts)}**",
 f"- Successful checks: **{len(success)}**",f"- API-error checks: **{len(api_errors)}**",
 f"- Prefix-model matches: **{len(matched)}/{len(attempts)}**",f"- Prefix-model non-matches/errors: **{len(mismatch)}**",
 f"- Mechanical matrix coverage: **{'PASS' if mechanical_ok else 'INCOMPLETE'}**",f"- Outcome counts: `{dict(counts)}`","","## Passes",""]
for p,x in sorted(by_pass.items()):
    lines.append(f"- `{p}`: attempts={x['attempts']}, success={x['success']}, prefix_matches={x['matches']}, effect_counts={sorted(x['counts'])}, unique_keys={len(x['keys'])}, missing_keys={len(expected_keys-x['keys'])}, statuses={dict(x['statuses'])}")
lines += ["","A CHECK API error is retained as an observed outcome rather than discarded. Mechanical completeness is based on attempted key coverage, while prediction truth is evaluated separately.",
 "Prefix prediction: `ALL_EFFECTS (-1)` normalizes to `num_effects`; generated-prefix >= requested-prefix predicts VALID, generated-prefix < requested-prefix predicts VALID_BUT_INCOMPLETE."]
if mismatch:
    lines += ["","## Non-matching outcomes",""]
    for r in mismatch[:100]:
        lines.append(f"- pass={r['pass']} k={r['generated']} n={r['requested']} geom={r['geometry_check']} error={r['error']} got={r['status_name']} expected={r['prefix_prediction']}")
SUMMARY.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"rows={len(rows)} attempts={len(attempts)} success={len(success)} errors={len(api_errors)} matches={len(matched)} nonmatches={len(mismatch)} malformed={malformed}")
print("coverage",coverage,"mechanical_ok",mechanical_ok); print("wrote",OUT); print("wrote",SUMMARY)
if not rows or not attempts: raise SystemExit(3)
if not mechanical_ok: raise SystemExit(4)
raise SystemExit(0)
