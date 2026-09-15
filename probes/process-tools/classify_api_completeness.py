from pathlib import Path
import csv, re

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
SRC = ROOT / "datasets" / "ae-api-surface-deltas.csv"
OUT = ROOT / "datasets" / "ae-api-completeness-classification.csv"
STATUS = ROOT / "docs" / "reference" / "api-completeness-status.md"
ALIAS = ROOT / "datasets" / "ae-api-guide-alias-suggestions.csv"
UTILITY = ROOT / "datasets" / "ae-sdk-25.6-utility-identifiers.csv"

utility_symbols = set()
if UTILITY.exists():
    with UTILITY.open(encoding="utf-8", newline="") as f:
        utility_symbols = {r["symbol"] for r in csv.DictReader(f)}

alias_map = {}
near_alias_map = {}
if ALIAS.exists():
    with ALIAS.open(encoding="utf-8", newline="") as f:
        for a in csv.DictReader(f):
            if a["match_kind"] in {"exact-normalized", "suite-family", "typedef-t-suffix-omitted"}:
                alias_map[a["guide_symbol"]] = a
            elif a["match_kind"] == "fuzzy-review" and a["candidate_count"] == "1":
                score = float(a["fuzzy_score"].split(";", 1)[0] or 0)
                if score >= 0.93:
                    near_alias_map[a["guide_symbol"]] = a

NEW_265 = re.compile(
    r"^(AEGP_CompSuite13|AEGP_StreamSuite7|AEGP_ItemViewSuite2|"
    r"AEGP_Guide|kAEGPGuideSuiteVersion|AEGP_Add(?:Item|Layer)Guide|AEGP_Remove(?:Item|Layer)Guide|AEGP_Set(?:Item|Layer)Guide|"
    r"AEGP_Get(?:Item|Layer)(?:Guide|NumGuides)|AEGP_GetItemViewGuides|AEGP_SetItemViewGuides|kAEGPItemViewSuiteVersion2|"
    r"AEGP_LayerParamStage|AEGP_(?:Get|Set)Stream.*Stage|"
    r"AEGP_CreateParametricMeshLayerInComp|AEGP_ParametricMeshType|"
    r"AEGP_ObjectType_3D_PARAMETRIC_MESH)"
)

def b(row, key):
    return row.get(key) == "True"

def classify(r):
    s = r["symbol"]
    if b(r, "parser_gap_25_6"):
        return "parser-gap", "high", "declared in raw 25.6 header but structured parser missed it"
    if b(r, "ae135_only"):
        return "historical-13_5-only", "high", "present in AE 13.5-era raw/header snapshot, absent from CC2014 and SDK 25.6"
    if b(r, "disappeared_ae135_to_25_6") and b(r, "in_cc2014_raw") and b(r, "in_cs6_raw"):
        return "historical-cs6-through-13_5-removed", "high", "present from CS6 through the 13.5 snapshot but absent from SDK 25.6"
    if b(r, "disappeared_ae135_to_25_6") and b(r, "in_cc2014_raw"):
        return "historical-cc2014-through-13_5-removed", "high", "present in CC2014 and the 13.5 snapshot but absent from SDK 25.6"
    if b(r, "disappeared_ae135_to_25_6"):
        return "historical-13_5-era-removed", "high", "present in the 13.5 snapshot but absent from SDK 25.6"
    if b(r, "cc2014_only"):
        return "historical-cc2014-only", "high", "present in CC2014 raw/header corpus, absent from CS6 and SDK 25.6"
    if b(r, "disappeared_cc2014_to_25_6") and b(r, "in_cs6_raw"):
        return "historical-cs6-through-cc2014-removed", "high", "present in CS6 and CC2014 raw corpora but absent from SDK 25.6"
    if b(r, "cs6_only"):
        return "historical-cs6-only", "high", "present in CS6 raw corpus but absent from CC2014 and SDK 25.6"
    if b(r, "disappeared_from_25_6") and b(r, "in_local_pre25_6"):
        return "historical-pre25.6-only", "high", "present in retained pre-25.6 header corpus but absent from distributed 25.6 and current Guide"
    if b(r, "raw_reference_only_25_6"):
        return "header-reference-only", "high", "token occurs in 25.6 header but is not an independently extracted declaration"
    if b(r, "guide_only") and NEW_265.search(s):
        return "guide-26.5-version-gap", "high", "matches independently verified 26.5 Guide vs 25.6 header gap family"
    if b(r, "guide_only") and s in alias_map:
        a = alias_map[s]
        return "guide-alias-to-header", "high", a["match_kind"] + ": " + a["candidates"]
    if b(r, "guide_only") and s in utility_symbols:
        return "guide+sdk-utility", "high", "exact token is distributed in SDK 25.6 Examples/Util rather than host ABI Headers"
    if b(r, "guide_only") and s in near_alias_map:
        a = near_alias_map[s]
        return "guide-near-match-header", "medium", "unique fuzzy header candidate: " + a["candidates"] + " (" + a["fuzzy_score"] + ")"
    if b(r, "guide_only"):
        return "guide-only-no-header-match", "high", "Guide token is inventoried but absent from 25.6, retained pre-25.6, CS6 and SDK-utility identifier corpora; semantic relation remains open"
    if b(r, "header_only_25_6"):
        if b(r, "introduced_after_ae135"):
            return "distributed-header-only-post-13_5", "high", "25.6 declaration is absent from the AE 13.5-era snapshot and not independently indexed by Guide headings"
        if b(r, "introduced_after_cc2014"):
            return "distributed-header-only-post-cc2014", "high", "25.6 declaration is absent from CC2014 and not independently indexed by Guide headings"
        if b(r, "introduced_after_cs6"):
            return "distributed-header-only-post-cs6", "high", "25.6 declaration is absent from CS6 and not independently indexed by Guide headings"
        return "distributed-header-only", "high", "25.6 declaration is not independently indexed by Guide headings"
    if b(r, "in_guide_26_5") and b(r, "in_sdk_25_6"):
        return "guide+distributed-header", "high", "identifier is independently present in both current Guide and 25.6 structured header inventory"
    if b(r, "in_sdk_25_6"):
        return "distributed-header", "high", "structured 25.6 declaration"
    if b(r, "in_cs6"):
        return "historical-cs6", "high", "structured CS6 declaration"
    return "evidence-surface-unresolved", "open", "not covered by deterministic surface-presence rules"

with SRC.open(encoding="utf-8", newline="") as f:
    source = list(csv.DictReader(f))
rows = []
for r in source:
    klass, confidence, reason = classify(r)
    rows.append({**r, "completeness_class": klass, "classification_confidence": confidence, "classification_reason": reason})

fields = list(rows[0])
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)
from collections import Counter
counts = Counter(r["completeness_class"] for r in rows)
coverage_open = counts["parser-gap"] + counts["evidence-surface-unresolved"]
relation_total = counts["guide-only-no-header-match"] + counts["guide-near-match-header"]
REL = ROOT / "datasets" / "ae-api-guide-relation-classification.csv"
relation_reviewed = 0
if REL.exists():
    with REL.open(encoding="utf-8-sig", newline="") as f:
        relation_reviewed = sum(1 for _ in csv.DictReader(f))
relation_open = max(0, relation_total - relation_reviewed)
lines = [
    "---", "status: generated", "last_verified: 2026-09-15", "---",
    "# API Completeness Status", "",
    f"C++ identifier union: **{len(rows)}**.",
    f"Deterministically surface-classified: **{len(rows)-coverage_open}**.",
    f"Open surface-classification queue: **{coverage_open}**.",
    f"Guide/Header relation rows reviewed: **{relation_reviewed}/{relation_total}**.",
    f"Open semantic-relation review queue: **{relation_open}**.", "",
    "| Class | Count |", "|---|---:|",
]
for key, value in sorted(counts.items()):
    lines.append(f"| `{key}` | {value} |")
lines += [
    "", "`parser-gap` must be zero before AEIG 1.0.",
    "`guide-only-no-header-match` is a semantic-relation review queue, not an unclassified coverage hole and not evidence that an API is missing from the host.",
    "Header-only declarations remain first-class inventory entries even when the prose Guide does not index them.",
    "Runtime-internal, scripting/expression, extension-substrate, private-gate and diagnostic surfaces are tracked in separate datasets and are not collapsed into this C++ identifier table.",
]
STATUS.write_text("\n".join(lines)+"\n", encoding="utf-8")
print("rows", len(rows), "surface_open", coverage_open, "relation_reviewed", relation_reviewed, "relation_open", relation_open, "classes", dict(sorted(counts.items())))
print("wrote", OUT)
print("wrote", STATUS)

