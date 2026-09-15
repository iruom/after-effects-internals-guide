from pathlib import Path
from datetime import date
import csv, subprocess, sys

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"; TOOLS=ROOT/"probes"/"process-tools"
OUT=ROOT/"docs"/"reference"/"static-rc-status.md"

def rows(name):
    with (DATA/name).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def run(name):
    p=subprocess.run([sys.executable,str(TOOLS/name)],capture_output=True,text=True,
                     encoding="utf-8",errors="replace")
    return p.returncode,(p.stdout+p.stderr).strip()

release=rows("aeig-release-readiness.csv")
blocked=[r for r in release if r.get("status")=="BLOCKER"]
coverage=rows("aeig-roadmap-progress.csv")
met=sum(r.get("meets_1_0_target","").lower() in {"true","1","yes"} for r in coverage)
fingerprint=(DATA/"aeig-static-rc-fingerprint.txt").read_text(encoding="utf-8").strip()
manifest=rows("aeig-static-rc-manifest.csv")
master=rows("ae-master-surface-registry.csv")
pre_code,pre_text=run("preflight_aeig_l5_operator_run.py")
lines=[
    "---","status: generated",f"last_verified: {date.today().isoformat()}","---",
    "# AEIG 1.0 Static RC Status","",
    f"- Domain target: **{met}/{len(coverage)}**.",
    f"- Frozen artifacts: **{len(manifest)}**.",
    f"- Static RC SHA-256: `{fingerprint}`.",
    f"- Master Surface Registry: **{len(master)} rows**.",
    f"- Operator preflight: **{'PASS' if pre_code==0 else 'BLOCKED'}**.",
    f"- Release blockers: **{len(blocked)}**.","",
    "## Release blockers",
]
for r in blocked:
    lines.append(f"- `{r['check']}` — {r['detail']}")
lines += ["","## Operator preflight","```text",pre_text,"```","",
          "Static RC files are immutable for the operator run. Post-run result files and promotion state are intentionally mutable."]
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("wrote",OUT)
print("blockers",len(blocked),"preflight",pre_code,"coverage",met,"/",len(coverage))
