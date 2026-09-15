from pathlib import Path
import csv, re

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DATA = ROOT / "datasets"
SRC = DATA / "ae-api-guide-relation-review.csv"
ALIASES = DATA / "ae-api-guide-alias-suggestions.csv"
OUT = DATA / "ae-api-guide-relation-classification.csv"


def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

alias = {r["guide_symbol"]: r for r in read(ALIASES)}
SPECIAL = {
    "AEGP_GetDefaultCamera": ("guide-doc-truncation", "AEGP_GetDefaultCameraDistanceToImagePlane", "current Guide tokenization truncates the documented camera function name"),
    "AEGP_GetIndProject": ("guide-doc-row-label-alias", "AEGP_GetProjectByIndex", "Guide row label differs from the distributed function name"),
    "AEGP_GetProjectProjectByIndex": ("guide-doc-signature-typo", "AEGP_GetProjectByIndex", "Guide signature duplicates Project; 25.6 header defines AEGP_GetProjectByIndex"),
    "AEGP_GetNthLayerIndexToRender": ("guide-doc-signature-typo", "AEGP_GetCompRenderTime", "Guide places this signature under AEGP_GetCompRenderTime; header defines AEGP_GetCompRenderTime"),
    "AEGP_InSpecGetRational": ("guide-doc-truncation", "AEGP_InSpecGetRationalDimensions", "Guide row token is a truncated form of the distributed function"),
    "AEGP_GetNewMaskOpacity": ("guide-stale-specialized-callable", "AEGP_GetNewMaskStream", "Guide retains specialized opacity accessor while distributed StreamSuite uses AEGP_GetNewMaskStream with AEGP_MaskStream_OPACITY"),
    "AEGP_GetDriverSpecVersion": ("guide-signature-no-header", "", "current Guide documents a callable signature absent from all inventoried header corpora"),
    "PF_HasParamChanged": ("guide-historical-removed-callable", "PF_HasParamChangedObsolete", "Guide says removed/no longer supported; old header retains obsolete table slot"),
    "AE_Effect_Description": ("guide-cross-host-premiere-only", "", "26.5 Guide explicitly scopes this PiPL property to Premiere Pro Beta 27.0, not After Effects"),
    "AE_Effect_Search_Keywords": ("guide-cross-host-premiere-only", "", "26.5 Guide explicitly scopes this PiPL property to Premiere Pro Beta 27.0, not After Effects"),
    "PF_REGISTER_EFFECT_EXT3": ("guide-cross-host-premiere-only", "", "26.5 Guide ties this registration macro path to Premiere Pro Beta 27.0 Effects-panel metadata"),
}
rows = []
for r in read(SRC):
    s, ctx = r["guide_symbol"], r["context"]
    a = alias.get(s, {})
    if s in SPECIAL:
        relation, target, note = SPECIAL[s]
        confidence = "high"
    elif r["current_class"] == "guide-near-match-header":
        relation = "reviewed-guide-alias"
        target = a.get("candidates", "")
        confidence = "high"
        note = "unique >=0.93 fuzzy candidate; manually reviewed notation/typo/handle/plural/version relation"
    elif re.search(r'(?<![A-Za-z0-9_])' + re.escape(s) + r'\s*\(', ctx):
        relation = "guide-signature-no-header"
        target = ""
        confidence = "high"
        note = "Guide contains an explicit callable-style signature; no exact token exists in 25.6, retained pre-25.6, CS6, or SDK utility corpora"
    elif r["prefix_candidates"]:
        relation = "guide-prefix-relation"
        target = r["prefix_candidates"]
        confidence = "high"
        note = "Guide token is a strict prefix/family shorthand for one or more distributed header identifiers"
    else:
        relation = "guide-token-no-header"
        target = ""
        confidence = "high"
        note = "Guide vocabulary is inventoried exactly, but no exact distributed/historical header identifier matches; treat as documentation vocabulary until a stronger semantic relation is proven"
    rows.append({**r, "review_relation": relation, "review_target": target,
                 "review_confidence": confidence, "review_note": note})

fields = list(rows[0])
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)
from collections import Counter
counts = Counter(r["review_relation"] for r in rows)
STATUS = ROOT / "docs" / "reference" / "api-guide-relation-status.md"
lines = [
    "---", "status: generated", "last_verified: 2026-09-15", "---",
    "# Guide/Header Relation Status", "",
    f"Reviewed Guide-only/near-match relation queue: **{len(rows)} / {len(rows)}**.",
    "", "| Relation class | Count |", "|---|---:|",
]
for k, v in sorted(counts.items()):
    lines.append(f"| `{k}` | {v} |")
lines += ["", "Surface coverage and semantic equivalence are separate questions.",
          "`guide-signature-no-header` is a documentation/distribution inconsistency class, not permission to synthesize an ABI.",
          "`guide-token-no-header` preserves exact Guide vocabulary without pretending it maps to a distributed C identifier."]
STATUS.write_text("\n".join(lines)+"\n", encoding="utf-8")
print("rows", len(rows), dict(sorted(counts.items())))
print("wrote", OUT); print("wrote", STATUS)
