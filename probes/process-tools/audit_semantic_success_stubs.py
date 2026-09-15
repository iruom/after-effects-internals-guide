from __future__ import annotations
import csv, re
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
AEXLO = ROOT / r"research\external-sources\aexlo\crates\aexlo\src\suites"
AEXEXEC = Path(r"D:\Developer\AexExecutor\src\aex_host.cpp")
OUT = ROOT / r"datasets\independent-host-semantic-success-stubs.csv"

STUB_RE = re.compile(r"stub_log!\(\s*(\w+)\s*,(.*?)\);", re.S)
ARG_RE = re.compile(r"(\w+)\s*:\s*([^,\n]+)")
rows: list[dict[str, str]] = []

for path in AEXLO.rglob("*.rs"):
    text = path.read_text(encoding="utf-8", errors="replace")
    for m in STUB_RE.finditer(text):
        fn, body = m.group(1), m.group(2)
        args = ARG_RE.findall(body)
        mut_ptrs = [name for name, ty in args if "*mut" in ty]
        out_named = [name for name, _ in args if name.lower().startswith("out_") or "result" in name.lower()]
        setters = fn.startswith(("set_", "effect_depends", "effect_wants"))
        if mut_ptrs or out_named:
            risk = "success-with-unwritten-output"
        elif setters:
            risk = "success-with-no-semantic-effect"
        else:
            risk = "success-stub"
        rows.append({
            "implementation": "aexlo",
            "source": str(path.relative_to(ROOT)),
            "function": fn,
            "risk": risk,
            "mutable_pointer_args": ";".join(mut_ptrs),
            "output_named_args": ";".join(out_named),
            "behavior": "stub_log returns PF_Err_NONE and does not touch arguments",
        })

if AEXEXEC.exists():
    text = AEXEXEC.read_text(encoding="utf-8", errors="replace")
    if "return 0; // A_Err_NONE" in text and "s_unknown_suite[1024]" in text:
        rows.append({
            "implementation": "AexExecutor",
            "source": str(AEXEXEC),
            "function": "unknown_suite_fn / s_unknown_suite[1024]",
            "risk": "broad-success-fabrication",
            "mutable_pointer_args": "unknown",
            "output_named_args": "unknown",
            "behavior": "1024 generic slots call a function returning A_Err_NONE without writing outputs",
        })

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)
print("rows", len(rows))
for risk in sorted({r["risk"] for r in rows}):
    print(risk, sum(r["risk"] == risk for r in rows))
