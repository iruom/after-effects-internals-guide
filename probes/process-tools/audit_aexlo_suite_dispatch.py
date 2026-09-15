from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
OUT = ROOT / "datasets" / "aexlo-suite-dispatch-audit.csv"
EFFECT = ROOT / "datasets" / "ae-sdk-25.6-effect-suite-prefix-compat.csv"
VERSIONS = ROOT / "datasets" / "ae-sdk-25.6-suite-versions.csv"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

effect = read_csv(EFFECT)
versions = read_csv(VERSIONS)

def compat(family: str, old_pica: str, new_pica: str) -> str:
    for row in effect:
        if (row["family"] == family and row["older_pica_version"] == old_pica
                and row["newer_pica_version"] == new_pica):
            return row["older_is_prefix"]
    return "not-in-dataset"

aegp_utility_versions = sorted({
    int(r["pica_version"]) for r in versions
    if r["suite_macro_base"] == "kAEGPUtilitySuite"
})
rows: list[dict[str, str]] = []
def add(suite: str, accepted: str, returned: str, verdict: str, evidence: str, note: str) -> None:
    rows.append(dict(suite=suite, aexlo_accepts=accepted, returned_table=returned,
                     verdict=verdict, evidence=evidence, note=note))

add("PF Iterate8 Suite", "1..=2", "PF_Iterate8Suite2", "compatible",
    "AE_EffectCBSuites.h; prefix dataset",
    f"v1->v2 prefix={compat('PF_Iterate8Suite', '1', '2')}; ordered public slots unchanged")
add("PF iterate16 Suite", "1..=2", "PF_iterate16Suite2", "compatible-header-review",
    "AE_EffectCBSuites.h",
    "v1/v2 expose the same three ordered callbacks; spelling/case differs in typedef names")
add("PF iterateFloat Suite", "1..=2", "PF_iterateFloatSuite2", "compatible-header-review",
    "AE_EffectCBSuites.h",
    "v1/v2 expose the same three ordered callbacks")
add("PF Pixel Data Suite", "1..=2", "PF_PixelDataSuite2", "compatible",
    "AE_EffectCBSuites.h; prefix dataset",
    f"v1->v2 prefix={compat('PF_PixelDataSuite', '1', '2')}; v2 appends GPU accessor")
add("PF AE App Suite", "1..=6", "PFAppSuite6", "incompatible",
    "AE_EffectSuitesOld.h; AE_EffectSuites.h; prefix dataset",
    "PICA v6 selects Suite4, v7 selects Suite5, v1 selects Suite6; Suite4->5 inserts a slot")
add("PF Param Utils Suite", "1..=3", "PF_ParamUtilsSuite3", "incompatible",
    "AE_EffectSuitesOld.h; AE_EffectSuites.h; prefix dataset",
    f"published PICA v2 old table -> v3 prefix={compat('PF_ParamUtilsSuite', '2', '3')}; obsolete state slots were replaced")
add("PF Utility Suite", "1..=18", "PF_UtilitySuite", "incompatible-at-v4",
    "PrSDKAESupport.h",
    "Adobe explicitly gives v4 a separate table because GetClipName was versioned incorrectly")
add("AEGP Utility Suite", "1..=18", "AEGPUtilitySuiteCompatV11", "unsafe-range-alias",
    "AE_GeneralPlugOld.h; AE_GeneralPlug.h; aexlo utility.rs",
    "published 25.6 PICA versions are " + ",".join(map(str, aegp_utility_versions)) +
    "; aexlo returns one hand-built v11-offset table for the whole numeric range")

fields = ["suite", "aexlo_accepts", "returned_table", "verdict", "evidence", "note"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

for row in rows:
    print(f"{row['verdict']:24} {row['suite']:28} {row['aexlo_accepts']} -> {row['returned_table']}")
print("wrote", OUT)