from pathlib import Path
import os, tempfile, time
from aeig_operator_session import (evaluate_session, evaluate_raw_times,
    build_session_values, write_session, read_kv)

F="A"*64; AEX="B"*64
base={"schema":"AEIG-L5-SESSION-v1","session_id":"S1","issued_unix_ms":"1000",
      "static_rc_fingerprint":F,"canonical_aex_sha256":AEX}
cases=[]
def check(name,ok):
    cases.append((name,bool(ok))); print("PASS" if ok else "FAIL",name)

check("valid-session",evaluate_session(dict(base),F,AEX)["ok"])
for field,bad in (("schema","bad"),("session_id",""),("issued_unix_ms","x"),
                  ("static_rc_fingerprint","C"*64),("canonical_aex_sha256","D"*64)):
    v=dict(base); v[field]=bad
    check("reject-"+field,not evaluate_session(v,F,AEX)["ok"])

with tempfile.TemporaryDirectory() as td:
    root=Path(td); p1=root/"a"; p2=root/"b"
    p1.write_text("a"); p2.write_text("b")
    now_ms=int(time.time()*1000)
    os.utime(p1,(time.time(),time.time())); os.utime(p2,(time.time(),time.time()))
    check("raw-times-valid",evaluate_raw_times({"a":p1,"b":p2},now_ms-1000)["all_after_issue"])
    old=(now_ms-10000)/1000.0
    os.utime(p1,(old,old))
    check("raw-old-file-rejected",not evaluate_raw_times({"a":p1,"b":p2},now_ms)["all_after_issue"])
    missing=root/"missing"
    check("raw-missing-file-rejected",not evaluate_raw_times({"a":p2,"missing":missing},now_ms-1000)["all_after_issue"])

with tempfile.TemporaryDirectory() as td:
    sp=Path(td)/"session.env"
    vals=build_session_values(F,AEX,issued_unix_ms=123456,session_id="TEST-SESSION")
    write_session(sp,vals); reread=read_kv(sp)
    check("session-write-roundtrip",reread.get("session_id")=="TEST-SESSION" and reread.get("issued_unix_ms")=="123456" and evaluate_session(reread,F,AEX)["ok"])

passed=all(ok for _,ok in cases)
print("AEIG OPERATOR SESSION SELFTEST:","PASS" if passed else "FAIL")
raise SystemExit(0 if passed else 2)
