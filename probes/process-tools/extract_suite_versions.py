from pathlib import Path
import re, csv

ROOT = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
FILES = [ROOT / "AE_GeneralPlug.h", ROOT / "AE_GeneralPlugOld.h"]
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets\ae-sdk-25.6-suite-versions.csv")

pat = re.compile(r"#define\s+(k[A-Za-z0-9_]*SuiteVersion(?P<gen>\d+)?)\s+(?P<num>\d+)(?:\s*/\*(?P<comment>.*?)\*/)?")
rows = []
for path in FILES:
    text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), 1):
        m = pat.search(line)
        if not m:
            continue
        macro = m.group(1)
        base = re.sub(r"Version\d*$", "", macro)
        rows.append({"suite_macro_base": base, "version_macro": macro,
                     "generation": m.group("gen") or "", "pica_version": int(m.group("num")),
                     "comment": (m.group("comment") or "").strip(),
                     "source": path.name, "line": lineno})
rows.sort(key=lambda r: (r["suite_macro_base"], r["pica_version"]))
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows -> {OUT}")
for key in ("kAEGPCompSuite", "kAEGPLayerSuite", "kAEGPItemSuite", "kAEGPStreamSuite"):
    print("\n", key)
    for r in rows:
        if r["suite_macro_base"] == key:
            print(r["generation"], r["pica_version"], r["comment"], r["source"], r["line"])
