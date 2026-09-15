from pathlib import Path
import json, sys

TOOLS=Path(__file__).resolve().parent
sys.path.insert(0,str(TOOLS))
from aeig_promotion_gate import CORE, REQUIRED_EXPERIMENTS, evaluate_promotion_gate


def decisions(*, ready=True, revision=False):
    return [{"domain":d,"evidence_ready":str(ready),"model_revision_required":str(revision)} for d in sorted(CORE)]

def predictions(statuses=None, unlocked=None):
    statuses=statuses or ["confirmed"]*7; unlocked=unlocked or set()
    return [{"prediction_id":f"PRED-{i:03d}","mode":"prospective","status":status,
             "locked_before_run":"false" if i in unlocked else "true"}
            for i,status in enumerate(statuses,1)]

def manifests(status="observed"):
    return {e:status for e in REQUIRED_EXPERIMENTS}
cases=[]
def case(name, expect_ok, d=None, p=None, m=None):
    result=evaluate_promotion_gate(d or decisions(),p or predictions(),m or manifests())
    ok=result["ok"] is expect_ok
    cases.append((name,ok,result))

case("all-confirmed-success",True)
case("refuted-revised-success",True,p=predictions(["confirmed"]*3+["refuted-revised"]*4))
case("missing-domain-fails",False,d=decisions()[:-1])
case("evidence-not-ready-fails",False,d=decisions(ready=False))
case("revision-required-fails",False,d=decisions(revision=True))
case("unlocked-prediction-fails",False,p=predictions(unlocked={2}))
case("pending-prediction-fails",False,p=predictions(["confirmed"]*6+["pending"]))
case("raw-refutation-fails",False,p=predictions(["confirmed"]*6+["refuted"]))
case("manifest-not-observed-fails",False,m=manifests("runnable"))

passed=all(ok for _,ok,_ in cases)
for name,ok,result in cases:
    print("PASS" if ok else "FAIL",name,"gate_ok=",result["ok"],"errors=",result["errors"])
print("AEIG PROMOTION GATE SELFTEST:","PASS" if passed else "FAIL")
raise SystemExit(0 if passed else 2)
