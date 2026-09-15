from pathlib import Path
import csv, re

ROOT = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets\ae-sdk-25.6-suite-names.csv")
FILES = [ROOT / "AE_GeneralPlug.h", ROOT / "AE_GeneralPlugOld.h"]
pat = re.compile(r'^\s*#define\s+(k[A-Za-z0-9_]*Suite)\s+"([^"]+)"')
rows = {}
for path in FILES:
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = pat.search(line)
        if not m:
            continue
        macro, value = m.groups()
        rows.setdefault((macro, value), {"suite_macro": macro, "suite_name": value,
                                         "source": path.name, "line": lineno})
# 26.x Guide-known family absent from the local 25.6 headers.
rows.setdefault(("kAEGPGuideSuite", "AEGP Guide Suite"),
                {"suite_macro": "kAEGPGuideSuite", "suite_name": "AEGP Guide Suite",
                 "source": "Guide-26.5-known-gap", "line": ""})
items = sorted(rows.values(), key=lambda r: (r["suite_name"], r["suite_macro"]))
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["suite_macro","suite_name","source","line"])
    w.writeheader(); w.writerows(items)
print("suite names", len(items), "wrote", OUT)
