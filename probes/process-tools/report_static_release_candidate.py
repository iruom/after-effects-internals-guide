from pathlib import Path
from datetime import date
import csv, re

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"
OUT=ROOT/"docs"/"reference"/"static-release-candidate.md"

def rows(name):
    p=DATA/name
    if not p.exists(): return []
    with p.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def truth(v): return str(v).lower() in {"true","1","yes"}
manifest=rows("aeig-static-rc-manifest.csv")
lock=rows("aeig-prediction-lock.csv")
coverage=rows("aeig-roadmap-progress.csv")
master=rows("ae-master-surface-registry.csv")
api=rows("ae-api-completeness-classification.csv")
findings=rows("finding-registry-audit.csv")
cap=rows("ae-plugin-capability-frontier.csv")
met=sum(truth(r.get("meets_1_0_target")) for r in coverage)
remaining=[r.get("domain","") for r in coverage if not truth(r.get("meets_1_0_target"))]
fp_text=(DATA/"aeig-static-rc-fingerprint.txt").read_text(encoding="utf-8-sig")
m=re.search(r"\b[0-9A-Fa-f]{64}\b",fp_text)
fingerprint=m.group(0).upper() if m else "UNAVAILABLE"
surface_classes=len({r.get("surface_class","") for r in master if r.get("surface_class")})
lines=[
    "---","status: generated",f"last_verified: {date.today().isoformat()}",
    "release_state: AEIG-1.0-static-rc","---",
    "# AEIG 1.0 Static Release Candidate","",
    "The static side of AEIG 1.0 is frozen before the final operator experiment.","",
    "## Frozen identity","",
    "- Static RC manifest: `datasets/aeig-static-rc-manifest.csv`",
    "- Immutable prediction lock: `datasets/aeig-prediction-lock.csv`",
    f"- Frozen artifacts: **{len(manifest)}**",
    f"- Prospective predictions locked: **{len(lock)}**",
    f"- RC fingerprint: `{fingerprint}`",
    "- Fingerprint record: `datasets/aeig-static-rc-fingerprint.txt`","",
    "`verify_aeig_static_rc.py` validates every frozen artifact, the immutable prediction fields, and the aggregate fingerprint before promotion.","",
    "## Static completeness snapshot","",
    f"- Domain target: **{met}/{len(coverage)}** before the remaining operator evidence.",
    f"- Remaining below target: **{', '.join(remaining) if remaining else 'none'}**.",
    f"- C++ identifier inventory: **{len(api):,}** rows in the completeness classification.",
    f"- Master Surface Registry: **{len(master):,} rows / {surface_classes} surface classes**.",
    f"- Findings audited: **{len(findings)}**.",
    f"- Capability Frontier: **{len(cap)} capabilities**.",
]
lines += [
    "","## Master Surface Registry query","",
    "Use `probes/process-tools/query_master_surface.py` for cross-surface search.","",
    "```powershell",
    "python probes/process-tools/query_master_surface.py RenderGuid --kind bee",
    "python probes/process-tools/query_master_surface.py BEE_Cache --facets",
    "python probes/process-tools/query_master_surface.py --capability-only --format json",
    "```","",
    "Treat `support_class`, `host_scope`, `version`, `evidence` and `contract_boundary` as mandatory context; runtime visibility is not a supported third-party contract.","",
    "## Remaining promotion gates","",
    "AEIG 1.0 remains unreleased while any required domain is below target, any locked prediction is pending, or any refutation remains unrevised.","",
    "## Operator handoff","",
    "`experiments/user-run/AEIG-L5-PREPARE.cmd` performs static verification, archives mutable prior captures, re-runs clean preflight, and installs the temporary probe.",
    "The user then starts AE 26.3, uses a disposable empty project, runs `AEIG-1.0-L5/01_RUN_IN_AE.jsx` once, and closes AE.",
    "`experiments/user-run/AEIG-L5-FINISH.cmd` removes the probe and invokes verification/finalization.",
]
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("wrote",OUT)
print("coverage",met,"/",len(coverage),"remaining",remaining)
print("fingerprint",fingerprint)
print("master",len(master),"surface_classes",surface_classes)
