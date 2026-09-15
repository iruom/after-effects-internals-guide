def read_kv(path):
    out={}
    if not path.exists(): return out
    for line in path.read_text(encoding="utf-8-sig",errors="replace").splitlines():
        if "=" in line:
            k,v=line.split("=",1); out[k.strip()]=v.strip()
    return out

def evaluate_session(values,current_fingerprint,expected_aex):
    errors=[]
    if values.get("schema")!="AEIG-L5-SESSION-v1": errors.append("schema")
    if not values.get("session_id"): errors.append("session_id")
    try: issued=int(values.get("issued_unix_ms","0"))
    except ValueError: issued=0
    if issued<=0: errors.append("issued_unix_ms")
    if not current_fingerprint or values.get("static_rc_fingerprint")!=current_fingerprint: errors.append("static_rc_fingerprint")
    if values.get("canonical_aex_sha256")!=expected_aex: errors.append("canonical_aex_sha256")
    return {"ok":not errors,"errors":errors,"issued_unix_ms":issued,"session_id":values.get("session_id",""),
            "fingerprint":values.get("static_rc_fingerprint",""),"aex_hash":values.get("canonical_aex_sha256","")}

def evaluate_raw_times(paths,issued_unix_ms,tolerance_ms=2000):
    files={}
    for name,path in paths.items():
        mtime_ms=int(path.stat().st_mtime*1000) if path.exists() else 0
        files[name]={"exists":path.exists(),"mtime_unix_ms":mtime_ms,
                     "after_session_issue":bool(path.exists() and issued_unix_ms>0 and mtime_ms>=issued_unix_ms-tolerance_ms)}
    return {"tolerance_ms":tolerance_ms,"files":files,"all_after_issue":all(x["after_session_issue"] for x in files.values())}

from datetime import datetime, timezone
import time, uuid

def build_session_values(fingerprint,aex_hash,issued_unix_ms=None,session_id=None):
    issued=int(time.time()*1000) if issued_unix_ms is None else int(issued_unix_ms)
    sid=session_id or (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:12].upper())
    return {"schema":"AEIG-L5-SESSION-v1","session_id":sid,
            "issued_utc":datetime.now(timezone.utc).isoformat(),"issued_unix_ms":str(issued),
            "static_rc_fingerprint":fingerprint,"canonical_aex_sha256":aex_hash}

def write_session(path,values):
    order=("schema","session_id","issued_utc","issued_unix_ms","static_rc_fingerprint","canonical_aex_sha256")
    path.write_text("\n".join(f"{k}={values.get(k,'')}" for k in order)+"\n",encoding="utf-8")
