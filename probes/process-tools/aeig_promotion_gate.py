CORE={"state-identity","cache","render-graph","plugin-host"}
REQUIRED_EXPERIMENTS=("EXP-CACHE-002","EXP-PLUGIN-001","EXP-RG-001")

def truth(v): return str(v).lower() in {"true","1","yes"}

def evaluate_promotion_gate(decision_rows,prediction_rows,manifest_statuses):
    errors=[]; dec={r.get("domain",""):r for r in decision_rows}
    if set(dec)!=CORE:
        errors.append(f"decision domains mismatch: {sorted(dec)}")
    else:
        missing=[d for d in sorted(CORE) if not truth(dec[d].get("evidence_ready"))]
        revision=[d for d in sorted(CORE) if truth(dec[d].get("model_revision_required"))]
        if missing: errors.append("not all core L5 evidence gates are ready: "+",".join(missing))
        if revision: errors.append("model revision required before promotion: "+",".join(revision))
    pros=[r for r in prediction_rows if r.get("mode")=="prospective"]
    unlocked=[r.get("prediction_id","") for r in pros if r.get("locked_before_run","").lower()!="true"]
    confirmed=sum(r.get("status")=="confirmed" for r in pros)
    refuted=sum(r.get("status")=="refuted" for r in pros)
    unresolved=[r.get("prediction_id","") for r in pros if r.get("status") not in {"confirmed","refuted-revised","refuted"}]
    if len(pros)<3: errors.append("too few prospective predictions")
    if unlocked: errors.append("unlocked prospective prediction exists: "+",".join(unlocked))
    if confirmed<3 or unresolved or refuted:
        errors.append(f"prediction gate failed: confirmed={confirmed} unresolved={len(unresolved)} refuted={refuted}")
    bad_exp=[e for e in REQUIRED_EXPERIMENTS if manifest_statuses.get(e) not in {"observed","replicated"}]
    if bad_exp: errors.append("experiment is not observed/replicated: "+",".join(bad_exp))
    return {"ok":not errors,"errors":errors,"prospective":len(pros),"confirmed":confirmed,
            "refuted":refuted,"unresolved":unresolved,"unlocked":unlocked,"bad_experiments":bad_exp}
