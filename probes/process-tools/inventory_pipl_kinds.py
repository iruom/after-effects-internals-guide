from pathlib import Path
import csv, struct, sys
import pefile

ROOTS = [
    ("ae25.6", Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")),
    ("ae26.3", Path(r"D:\Adobe\Adobe After Effects 2026\Support Files")),
]
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets\ae-pipl-kind-inventory.csv")

def pipl_blobs(pe):
    r = getattr(pe, "DIRECTORY_ENTRY_RESOURCE", None)
    if not r: return []
    out=[]
    for typ in r.entries:
        name = typ.name.string.decode(errors="ignore") if typ.name else ""
        if name.upper() != "PIPL": continue
        for ent in typ.directory.entries:
            for lang in ent.directory.entries:
                d=lang.data.struct; off=pe.get_offset_from_rva(d.OffsetToData)
                out.append(pe.__data__[off:off+d.Size])
    return out
def parse_props(blob):
    if len(blob) < 10: return []
    try: count = struct.unpack_from("<I", blob, 6)[0]
    except struct.error: return []
    pos=10; props=[]
    for _ in range(min(count,128)):
        if pos+16>len(blob): break
        vendor=blob[pos:pos+4]; key=blob[pos+4:pos+8]
        prop_id,length=struct.unpack_from("<II",blob,pos+8); pos+=16
        if length>len(blob)-pos: break
        val=blob[pos:pos+length]; pos+=length
        props.append((vendor,key,prop_id,val))
    return props

def fourcc_le(val):
    if len(val)<4: return ""
    b=val[:4]
    try: return b[::-1].decode("latin1")
    except Exception: return b.hex()

def pascal(val):
    if not val: return ""
    n=val[0]
    return val[1:1+n].decode("utf-8",errors="replace")
rows=[]
for label,root in ROOTS:
    files=list(root.rglob("*.aex"))
    print(label,"aex",len(files))
    for path in files:
        try:
            pe=pefile.PE(str(path), fast_load=True)
            pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"]])
            blobs=pipl_blobs(pe)
        except Exception as e:
            continue
        for i,blob in enumerate(blobs):
            vals={}
            for vendor,key,pid,val in parse_props(blob):
                k=key[::-1].decode("latin1",errors="replace")
                vals.setdefault(k,[]).append(val)
            kind=fourcc_le(vals.get("kind",[b""])[0])
            name=pascal(vals.get("name",[b""])[0])
            cat=pascal(vals.get("catg",[b""])[0])
            rows.append({"host":label,"path":str(path),"pipl_index":i,
                         "kind":kind,"name":name,"category":cat,
                         "blob_bytes":len(blob)})

OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open("w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print("rows",len(rows),"out",OUT)
from collections import Counter
for label,_ in ROOTS:
    c=Counter(r["kind"] for r in rows if r["host"]==label)
    print(label,"kinds",c.most_common())
    print(label,"AEgx",[(r['name'],r['path']) for r in rows if r['host']==label and r['kind']=='AEgx'][:20])


