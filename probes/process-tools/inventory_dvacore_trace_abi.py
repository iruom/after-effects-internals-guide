from pathlib import Path
import csv, re, subprocess

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DUMPBIN = Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.44.35207\bin\Hostx64\x64\dumpbin.exe")
TARGETS = {
    "25.6": Path(r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\dvacore.dll"),
    "26.3": Path(r"D:\Adobe\Adobe After Effects 2026\Support Files\dvacore.dll"),
}
OUT = ROOT / "datasets" / "ae-dvacore-trace-abi-lineage.csv"
TOKENS = ("GetMasterTraceHandler", "InstallMasterTraceHandler", "RemoveMasterTraceHandler",
          "MasterTraceToStdErr", "GetMasterTraceVolume", "SetMasterTraceVolume",
          "GetTraceVolume", "SetTraceVolume")
rows = []
for version, dll in TARGETS.items():
    text = subprocess.check_output([str(DUMPBIN), "/exports", str(dll)], text=True,
                                   encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if not any(t in line for t in TOKENS): continue
        m = re.search(r"\s+\d+\s+[0-9A-F]+\s+[0-9A-F]+\s+(\?.+)$", line)
        if not m: continue
        decorated = m.group(1).strip()
        symbol = next(t for t in TOKENS if t in decorated)
        if "AEBV?$basic_string_view" in decorated:
            abi = "const-ref-string_view"
        elif "V?$basic_string_view" in decorated:
            abi = "by-value-string_view"
        else:
            abi = "stable-non-string-view"
        rows.append({"ae_version": version, "dll": str(dll), "symbol": symbol,
                     "abi_form": abi, "decorated_export": decorated})
fields = ["ae_version", "dll", "symbol", "abi_form", "decorated_export"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
print("rows", len(rows))
for symbol in TOKENS:
    s = [r for r in rows if r["symbol"] == symbol]
    if s:
        print(symbol, [(r["ae_version"], r["abi_form"]) for r in s])
print("wrote", OUT)
