from pathlib import Path
import csv, re, hashlib
from collections import Counter
import os

ROOT=Path(os.environ.get("AEIG_ROOT",r"D:\Developer\After Effects Internals Guide"))
RUN=ROOT/"experiments"/"observatory"/"runs"/"EXP-RG-001"
TRACE=RUN/"host-trace.log"; CONTROL=RUN/"trace-control.tsv"
OUT=ROOT/"datasets"/"exp-rg-001-trace-summary.csv"
CATS=["BEE_Eval","BEE_Cache","BEE_CacheLog","BEE_WorkQueue","MixHashGuid",
      "RenderNode.RG_CacheNodeBase","RenderNode.RG_XformNode","TDB_StreamBase","DiskCache"]
IDENTITY_CATS={"MixHashGuid","TDB_StreamBase","BEE_Eval"}
RG_CACHE_CATS={"RenderNode.RG_CacheNodeBase","RenderNode.RG_XformNode","BEE_Cache","BEE_CacheLog","BEE_WorkQueue","DiskCache"}
def digest_lines(lines):
    if not lines: return ""
    payload="\n".join(line.strip() for line in lines).encode("utf-8",errors="replace")
    return hashlib.sha256(payload).hexdigest().upper()

def parse_blocks(text):
    blocks=[]; cur=None; incomplete=0
    for line in text.splitlines():
        if line.startswith("AEIG_TRACE_BEGIN"):
            if cur is not None: incomplete += 1
            mseq=re.search(r"seq=(\d+)",line); mpass=re.search(r"pass=([^\t ]+)",line); mpid=re.search(r"pid=(\d+)",line)
            cur={"pid":mpid.group(1) if mpid else "?","seq":int(mseq.group(1)) if mseq else -1,"pass":mpass.group(1) if mpass else "?","lines":[]}
        elif line.startswith("AEIG_TRACE_END"):
            if cur is None: incomplete += 1
            else: blocks.append(cur); cur=None
        elif cur is not None: cur["lines"].append(line)
    if cur is not None: incomplete += 1
    return blocks,incomplete

def parse_control(path):
    groups={}; malformed=0
    if not path.exists(): return groups,1
    for line in path.read_text(encoding="utf-8-sig",errors="replace").splitlines():
        parts=line.split("\t")
        if len(parts)!=6: malformed+=1; continue
        pid,seq,run_pass,phase,detail,value=parts
        key=(pid,seq,run_pass); groups.setdefault(key,Counter())[phase]+=1
    return groups,malformed

if not TRACE.exists(): print("trace missing",TRACE); raise SystemExit(2)
if not CONTROL.exists(): print("trace control missing",CONTROL); raise SystemExit(2)
blocks,incomplete=parse_blocks(TRACE.read_text(encoding="utf-8-sig",errors="replace"))
control,control_malformed=parse_control(CONTROL)
rows=[]
for b in blocks:
    c=Counter(); matched={cat:[] for cat in CATS}
    for line in b["lines"]:
        for cat in CATS:
            pattern=r"(?<![A-Za-z0-9_.])"+re.escape(cat)+r"(?![A-Za-z0-9_.])"
            if re.search(pattern,line,re.IGNORECASE):
                c[cat]+=1; matched[cat].append(line)
    identity_lines=[line for cat in CATS if cat in IDENTITY_CATS for line in matched[cat]]
    rg_cache_lines=[line for cat in CATS if cat in RG_CACHE_CATS for line in matched[cat]]
    all_target_lines=[line for cat in CATS for line in matched[cat]]
    row={"pid":b["pid"],"pass":b["pass"],"seq":b["seq"],"line_count":len(b["lines"]),"relevant_line_count":sum(c.values()),
         "identity_sha256":digest_lines(identity_lines),"rg_cache_sha256":digest_lines(rg_cache_lines),
         "all_target_sha256":digest_lines(all_target_lines)}
    row.update({cat:c[cat] for cat in CATS}); rows.append(row)
fields=["pid","pass","seq","line_count","relevant_line_count","identity_sha256","rg_cache_sha256","all_target_sha256"]+CATS
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
by_pass={}
for r in rows:
    p=r["pass"]; agg=by_pass.setdefault(p,Counter())
    agg["blocks"]+=1; agg["lines"]+=r["line_count"]; agg["relevant"]+=r["relevant_line_count"]
    for cat in CATS: agg[cat]+=r[cat]
control_bad=[(k,dict(v)) for k,v in control.items() if v["BEGIN"]!=1 or v["END"]!=1]
control_passes={k[2] for k in control if k[2] in {"A","B"}}
trace_keys=[(str(r["pid"]),str(r["seq"]),r["pass"]) for r in rows]
trace_key_set=set(trace_keys); control_key_set=set(control)
trace_duplicate_keys=len(trace_keys)!=len(trace_key_set)
orphan_trace=sorted(trace_key_set-control_key_set); orphan_control=sorted(control_key_set-trace_key_set)
print("blocks",len(rows),"passes",sorted(by_pass),"incomplete_markers",incomplete)
print("control_groups",len(control),"control_passes",sorted(control_passes),"malformed",control_malformed,"bad_groups",len(control_bad),"trace_duplicate_keys",trace_duplicate_keys,"orphan_trace",len(orphan_trace),"orphan_control",len(orphan_control))
for p,a in sorted(by_pass.items()):
    print("pass",p,"blocks",a["blocks"],"lines",a["lines"],"relevant",a["relevant"])
    print("  ",{cat:a[cat] for cat in CATS if a[cat]})
print("wrote",OUT)
if not rows: raise SystemExit(3)
if incomplete or control_malformed or control_bad or trace_duplicate_keys or orphan_trace or orphan_control: raise SystemExit(4)
if not {"A","B"}.issubset(by_pass) or not {"A","B"}.issubset(control_passes): raise SystemExit(4)
relevant=sum(a["relevant"] for a in by_pass.values())
print("target_category_lines",relevant,"semantic_observation",("present" if relevant else "absent"))
# Zero target-category lines is a valid semantic observation when A/B capture windows are complete.
raise SystemExit(0)
