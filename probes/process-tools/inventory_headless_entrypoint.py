from __future__ import annotations
import csv, re, subprocess
from pathlib import Path

AE = Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files")
AERENDER = AE / "aerender.exe"
AFTERFX = AE / "AfterFX.exe"
DUMPBIN = Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\dumpbin.exe")
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets\ae-2025-headless-entrypoint.csv")

rows: list[dict[str, str]] = []
for exe in (AERENDER, AFTERFX):
    cp = subprocess.run([str(DUMPBIN), "/dependents", str(exe)], capture_output=True, text=True, errors="replace")
    for raw in cp.stdout.splitlines():
        line = raw.strip()
        if line.lower().endswith(".dll"):
            rows.append({"source": exe.name, "relation": "static-dependent", "entry": line})

help_cp = subprocess.run([str(AERENDER), "-help"], capture_output=True, text=True, errors="replace")
help_text = (help_cp.stdout or "") + (help_cp.stderr or "")
for line in help_text.splitlines():
    clean = line.strip()
    if re.search(r"already running instance|new instance|reuse|mem_usage|Multi-Frame Rendering|continueOnMissingFootage|preferences", clean, re.I):
        rows.append({"source": "aerender.exe", "relation": "runtime-help", "entry": clean})

ver_cp = subprocess.run([str(AERENDER), "-version"], capture_output=True, text=True, errors="replace")
version_text = ((ver_cp.stdout or "") + (ver_cp.stderr or "")).strip()
if version_text:
    rows.append({"source": "aerender.exe", "relation": "runtime-version", "entry": version_text})

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["source", "relation", "entry"])
    writer.writeheader(); writer.writerows(rows)
print(f"wrote {OUT} rows {len(rows)}")
for relation in sorted({r["relation"] for r in rows}):
    print(relation, sum(r["relation"] == relation for r in rows))
