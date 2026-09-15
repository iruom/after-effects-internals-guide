from __future__ import annotations
import csv, glob, re, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from pathlib import Path

REPO=Path(r"D:\Developer\After Effects Internals Guide")
AE=Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
OUT=REPO/"datasets"/"ae-2025-runtime-export-atlas.csv"
SUMMARY=REPO/"docs"/"reference"/"runtime-export-atlas-status.md"
cands=glob.glob(r"C:\Program Files\Microsoft Visual Studio\2022\*\VC\Tools\MSVC\*\bin\Hostx64\x64\dumpbin.exe")
if not cands: raise SystemExit("dumpbin.exe not found")
DUMPBIN=sorted(cands)[-1]
PE_EXT={".dll",".exe",".aex",".prm"}
RX=re.compile(r"^\s*(\d+)\s+([0-9A-F]+)\s+([0-9A-F]+)\s+(.+?)\s*$",re.I)

def category(s:str)->str:
    u=s.upper()
    for key in ("BEE_","RG_","TDB_","AEGP_","AEIO_","PF_","TXT_","OM_","COR_","AGM","DVA","MF::","BE::","GF::"):
        if key in u: return key.rstrip(":_").lower()
    return "other"
def scan(path:Path):
    p=subprocess.run([DUMPBIN,"/exports",str(path)],capture_output=True,text=True,errors="replace")
    if p.returncode not in (0,): return (path,[],f"dumpbin rc={p.returncode}")
    rows=[]
    for line in p.stdout.splitlines():
        m=RX.match(line)
        if not m: continue
        ordinal,hint,rva,name=m.groups()
        if name.lower().startswith("summary"): continue
        forwarded=""
        if " = " in name:
            name,forwarded=name.split(" = ",1)
        rows.append(dict(module=str(path.relative_to(AE)),module_name=path.name,extension=path.suffix.lower(),
                         ordinal=ordinal,hint=hint,rva=rva,symbol=name.strip(),forwarded_to=forwarded.strip(),
                         category=category(name),visibility="runtime-exported-internal-or-shared"))
    return (path,rows,"")

def main():
    files=sorted(p for p in AE.rglob("*") if p.is_file() and p.suffix.lower() in PE_EXT)
    all_rows=[]; failures=[]; with_exports=0
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(scan,p):p for p in files}
        for fut in as_completed(futs):
            path,rows,err=fut.result()
            if err: failures.append((str(path.relative_to(AE)),err))
            if rows: with_exports+=1; all_rows.extend(rows)
    all_rows.sort(key=lambda r:(r["module"].lower(),int(r["ordinal"]),r["symbol"]))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    if all_rows:
        with OUT.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(all_rows[0])); w.writeheader(); w.writerows(all_rows)
    cats=Counter(r["category"] for r in all_rows); mods=Counter(r["module_name"] for r in all_rows)
    lines=["---","status: generated","last_verified: 2026-09-15","---","# Runtime Export Atlas Status","",
           f"Scanned PE modules: **{len(files)}**.",f"Modules with exports: **{with_exports}**.",
           f"Export rows: **{len(all_rows)}**.",f"dumpbin failures: **{len(failures)}**.","",
           "These are runtime-visible PE exports, not supported plug-in APIs. Presence is evidence of a callable/linkable binary surface only; ABI stability, ownership, threading and semantic safety remain unknown until separately established.","",
           "## High-signal categories",""]
    for k,v in sorted(cats.items(), key=lambda kv:(-kv[1],kv[0])):
        if k!="other": lines.append(f"- `{k}`: {v}")
    lines += ["","## Largest export surfaces",""]
    for k,v in mods.most_common(30): lines.append(f"- `{k}`: {v}")
    if failures:
        lines += ["","## Scanner failures",""]+[f"- `{m}` — {e}" for m,e in failures[:50]]
    SUMMARY.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print("scanned",len(files),"modules; with exports",with_exports,"rows",len(all_rows),"failures",len(failures))
    print("wrote",OUT); print("wrote",SUMMARY)

if __name__=="__main__": main()
