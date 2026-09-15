from __future__ import annotations
import csv, re, subprocess
from pathlib import Path

AE = Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
DUMPBIN = Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\dumpbin.exe")
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets\ae-2025-memory-pressure-symbols.csv")
MODULES = ["AfterFXLib.dll", "MediaFoundation.dll", "GPUFoundation.dll", "BEE.dll", "VideoFrame.dll"]
PAT = re.compile(
    r"Purge|Memory(Control|Pressure|Footprint|Pool|Cache)|WorkingSet|Allocation|Allocator|"
    r"AssetCache|CacheGuard|ManagedMemoryCache|AdapterBudget|Evict|Resident|Residency|"
    r"RecycledMemory|Purgeable|DiskCacheManager|CacheHit|CheckoutCached",
    re.I,
)

def run(args: list[str]) -> str:
    return subprocess.run(args, capture_output=True, text=True, errors="replace", check=False).stdout

rows: list[dict[str, str]] = []
for module in MODULES:
    path = AE / module
    if not path.exists():
        continue
    for relation, switch in (("export", "/exports"), ("import", "/imports")):
        for raw in run([str(DUMPBIN), switch, str(path)]).splitlines():
            line = raw.strip()
            if line and PAT.search(line):
                rows.append({"module": module, "relation": relation, "entry": line})
    for raw in run([str(DUMPBIN), "/dependents", str(path)]).splitlines():
        line = raw.strip()
        if line.lower().endswith(".dll") and re.search(r"Media|GPU|Frame|BEE|dvacore|Allocator", line, re.I):
            rows.append({"module": module, "relation": "dependent", "entry": line})

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["module", "relation", "entry"])
    writer.writeheader(); writer.writerows(rows)
print(f"wrote {OUT} rows {len(rows)}")
for module in MODULES:
    print(module, sum(r["module"] == module for r in rows))
