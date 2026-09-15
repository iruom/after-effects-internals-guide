from pathlib import Path
import re, csv

ROOT = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
TEXT = "\n".join((ROOT/f).read_text(encoding="utf-8", errors="replace")
                 for f in ("AE_GeneralPlugOld.h", "AE_GeneralPlug.h"))
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets\ae-sdk-25.6-suite-prefix-compat.csv")
families = ["AEGP_CompSuite", "AEGP_LayerSuite", "AEGP_ItemSuite", "AEGP_StreamSuite", "AEGP_UtilitySuite"]
rows=[]
for family in families:
    structs=[]
    for m in re.finditer(r"typedef\s+struct\s+("+re.escape(family)+r"(\d+))\s*\{(.*?)\}\s*\1\s*;", TEXT, re.S):
        name, gen, body = m.group(1), int(m.group(2)), m.group(3)
        funcs=re.findall(r"\(\*\s*([A-Za-z0-9_]+)\s*\)", body)
        structs.append((gen,name,funcs))
    structs.sort()
    for i,(gen,name,funcs) in enumerate(structs):
        if i == 0: continue
        pgen,pname,pfuncs=structs[i-1]
        prefix=funcs[:len(pfuncs)] == pfuncs
        first_diff=""
        if not prefix:
            for j,(a,b) in enumerate(zip(pfuncs, funcs)):
                if a != b: first_diff=f"index {j}: {a} -> {b}"; break
            if not first_diff and len(funcs)<len(pfuncs): first_diff="new table shorter"
        rows.append(dict(family=family, older=pname, newer=name, older_count=len(pfuncs),
                         newer_count=len(funcs), older_is_prefix=prefix, first_difference=first_diff))
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
print("wrote", OUT)
