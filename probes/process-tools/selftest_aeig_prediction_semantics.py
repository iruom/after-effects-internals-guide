from aeig_prediction_semantics import pred004,pred005,pred006,pred007,pred008,pred009,pred010

cases=[
    ("PRED-004-confirm",pred004(True),"confirmed"),
    ("PRED-004-refute",pred004(False),"refuted"),
    ("PRED-005-confirm",pred005(True),"confirmed"),
    ("PRED-005-refute",pred005(False),"refuted"),
    ("PRED-006-confirm",pred006({"A":True,"B":True},{"A":True,"B":True}),"confirmed"),
    ("PRED-006-refute-zero",pred006({"A":False,"B":False},{"A":False,"B":False}),"refuted"),
    ("PRED-006-partial",pred006({"A":False,"B":False},{"A":True,"B":False}),"inconclusive"),
    ("PRED-007-confirm",pred007({"A":True,"B":True},True),"confirmed"),
    ("PRED-007-refute",pred007({"A":True,"B":True},False),"refuted"),
    ("PRED-007-missing",pred007({"A":True,"B":False},False),"inconclusive"),
]
cases += [
    ("PRED-008-confirm",pred008({"A":True,"B":True},True),"confirmed"),
    ("PRED-008-refute",pred008({"A":True,"B":True},False),"refuted"),
    ("PRED-008-missing",pred008({"A":False,"B":True},False),"inconclusive"),
    ("PRED-009-confirm",pred009(True,True),"confirmed"),
    ("PRED-009-refute",pred009(True,False),"refuted"),
    ("PRED-009-incomplete",pred009(False,False),"inconclusive"),
    ("PRED-010-confirm",pred010(True,True),"confirmed"),
    ("PRED-010-refute",pred010(True,False),"refuted"),
    ("PRED-010-incomplete",pred010(False,False),"inconclusive"),
]
passed=True
for name,got,want in cases:
    ok=got==want; passed &= ok
    print("PASS" if ok else "FAIL",name,"got=",got,"want=",want)
print("AEIG PREDICTION SEMANTICS SELFTEST:","PASS" if passed else "FAIL")
raise SystemExit(0 if passed else 2)
