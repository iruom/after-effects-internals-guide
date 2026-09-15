from __future__ import annotations
import csv
import glob
import re
import subprocess
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
AE = Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
OUT = ROOT / "datasets" / "ae-2025-render-identity-symbols.csv"

candidates = glob.glob(
    r"C:\Program Files\Microsoft Visual Studio\2022\*\VC\Tools\MSVC\*\bin\Hostx64\x64\dumpbin.exe"
)
if not candidates:
    raise SystemExit("dumpbin.exe not found")
DUMPBIN = sorted(candidates)[-1]

patterns = {
    "work_queue": re.compile(r"WorkQueue.*RenderGuid|BEEp_WorkQueue_GetRenderGuidWithRO", re.I),
    "rg_cache_graph": re.compile(r"RG_CacheNode|RG_ExecuteGraph|PreRenderGraph", re.I),
    "identity": re.compile(r"RenderGuid|MixHashGuid|MixInGuid|MixInValueAtTime", re.I),
}

def dump(args: list[str]) -> list[str]:
    p = subprocess.run([DUMPBIN, *args], capture_output=True, text=True, errors="replace")
    p.check_returncode()
    return p.stdout.splitlines()
rows: list[dict[str, str]] = []
for dll_name in ("BEE.dll", "RG.dll"):
    dll = AE / dll_name
    for relation, args in (
        ("export", ["/exports", str(dll)]),
        ("import", ["/imports", str(dll)]),
    ):
        for line in dump(args):
            stripped = line.strip()
            for category, rx in patterns.items():
                if rx.search(stripped):
                    rows.append({
                        "module": dll_name,
                        "relation": relation,
                        "category": category,
                        "symbol_line": stripped,
                    })
                    break

# Deduplicate identical dump lines while preserving deterministic order.
unique: dict[tuple[str, str, str, str], dict[str, str]] = {}
for row in rows:
    key = tuple(row[k] for k in ("module", "relation", "category", "symbol_line"))
    unique[key] = row
rows = sorted(unique.values(), key=lambda r: (r["module"], r["relation"], r["category"], r["symbol_line"]))
fields = ["module", "relation", "category", "symbol_line"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

for category in patterns:
    subset = [r for r in rows if r["category"] == category]
    print(category, len(subset))
    for row in subset[:12]:
        print(" ", row["module"], row["relation"], row["symbol_line"])
print("wrote", OUT, "rows", len(rows))