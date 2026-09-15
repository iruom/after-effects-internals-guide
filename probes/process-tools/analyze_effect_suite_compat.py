from __future__ import annotations
import csv, re
from pathlib import Path

SDK = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
OUT = Path(r"D:\Developer\After Effects Internals Guide\datasets")
FILES = ["AE_EffectCBSuites.h", "AE_EffectSuitesOld.h", "AE_EffectSuites.h", "PrSDKAESupport.h"]
texts = {name: (SDK / name).read_text(encoding="utf-8", errors="ignore") for name in FILES}

struct_re = re.compile(r"typedef\s+struct\s+([A-Za-z_]\w*?)(\d+)\s*\{(.*?)\}\s*\1\2\s*;", re.S | re.I)
field_re = re.compile(r"\(\*\s*([A-Za-z_]\w*)\s*\)")
macro_re = re.compile(r"#define\s+(k\w+SuiteVersion)(\d+)\s+([^\s/]+)")

structs: dict[tuple[str, int], dict] = {}
for header, text in texts.items():
    for m in struct_re.finditer(text):
        base, gen, body = m.group(1), int(m.group(2)), m.group(3)
        funcs = field_re.findall(body)
        if funcs:
            structs[(base, gen)] = {"header": header, "functions": funcs}

versions: dict[tuple[str, int], tuple[str, str]] = {}
for header, text in texts.items():
    for m in macro_re.finditer(text):
        versions[(m.group(1), int(m.group(2)))] = (m.group(3), header)
def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower().removeprefix("k"))

version_by_norm: dict[tuple[str, int], tuple[str, str, str]] = {}
for (macro_base, gen), (value, header) in versions.items():
    version_by_norm[(norm(macro_base.removesuffix("Version")), gen)] = (value, header, macro_base)

rows = []
for (base, gen), info in sorted(structs.items()):
    v = version_by_norm.get((norm(base), gen))
    rows.append({
        "family": base,
        "generation": gen,
        "pica_version": v[0] if v else "",
        "struct_header": info["header"],
        "version_header": v[1] if v else "",
        "function_count": len(info["functions"]),
        "functions": "|".join(info["functions"]),
    })

with (OUT / "ae-sdk-25.6-effect-suite-layouts.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)

compat = []
by_family: dict[str, list[dict]] = {}
for r in rows:
    by_family.setdefault(r["family"], []).append(r)
for family, fam_rows in sorted(by_family.items()):
    fam_rows.sort(key=lambda r: r["generation"])
    for old, new in zip(fam_rows, fam_rows[1:]):
        a = old["functions"].split("|") if old["functions"] else []
        b = new["functions"].split("|") if new["functions"] else []
        prefix = len(b) >= len(a) and b[:len(a)] == a
        first = ""
        if not prefix:
            if len(b) < len(a) and b == a[:len(b)]:
                first = "new table shorter"
            else:
                for i, (x, y) in enumerate(zip(a, b)):
                    if x != y:
                        first = f"index {i}: {x} -> {y}"
                        break
                if not first and len(a) != len(b):
                    first = f"length {len(a)} -> {len(b)}"
        compat.append({
            "family": family,
            "older_generation": old["generation"],
            "older_pica_version": old["pica_version"],
            "newer_generation": new["generation"],
            "newer_pica_version": new["pica_version"],
            "older_count": len(a),
            "newer_count": len(b),
            "older_is_prefix": prefix,
            "first_difference": first,
        })

with (OUT / "ae-sdk-25.6-effect-suite-prefix-compat.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=compat[0].keys())
    w.writeheader(); w.writerows(compat)

focus = {"PF_Iterate8Suite", "PF_PixelDataSuite", "PFAppSuite", "PF_ParamUtilsSuite"}
for r in rows:
    if r["family"] in focus:
        print(r)
for r in compat:
    if r["family"] in focus:
        print("COMPAT", r)
