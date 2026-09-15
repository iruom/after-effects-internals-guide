from pathlib import Path
import csv, re
from difflib import SequenceMatcher

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DATA = ROOT / "datasets"
CLASS = DATA / "ae-api-completeness-classification.csv"
ATLAS = DATA / "ae-api-symbol-atlas.csv"
OUT = DATA / "ae-api-guide-alias-suggestions.csv"


def read(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def basic(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())

classified = read(CLASS)
atlas = read(ATLAS)
headers = sorted({r["symbol"] for r in atlas if r["surface"] == "sdk-25.6"})
by_basic = {}
for s in headers:
    by_basic.setdefault(basic(s), []).append(s)

semantic_classes = {"guide-only-no-header-match", "guide-alias-to-header", "guide-near-match-header"}
unresolved = [r["symbol"] for r in classified if r["completeness_class"] in semantic_classes]
rows = []
for symbol in unresolved:
    key = basic(symbol)
    candidates = by_basic.get(key, [])
    kind = "exact-normalized" if candidates else ""
    if not candidates and symbol.endswith("Suite"):
        candidates = [s for s in headers if basic(s).startswith(key) and re.search(r"Suite\d+$", s)]
        if candidates:
            kind = "suite-family"
    if not candidates:
        type_key = key + "t"
        t_candidates = by_basic.get(type_key, [])
        if t_candidates:
            candidates = t_candidates
            kind = "typedef-t-suffix-omitted"
    if candidates:
        confidence = "high" if kind in {"exact-normalized", "typedef-t-suffix-omitted"} else "high-family"
        rows.append({"guide_symbol": symbol, "match_kind": kind, "confidence": confidence,
                     "candidate_count": len(candidates), "candidates": ";".join(candidates),
                     "fuzzy_score": ""})
        continue
    scored = []
    for h in headers:
        score = SequenceMatcher(None, key, basic(h)).ratio()
        if score >= 0.88:
            scored.append((score, h))
    scored.sort(reverse=True)
    top = scored[:5]
    margin = (top[0][0] - top[1][0]) if len(top) > 1 else (top[0][0] if top else 0)
    rows.append({"guide_symbol": symbol, "match_kind": "fuzzy-review" if top else "no-candidate",
                 "confidence": "review", "candidate_count": len(top),
                 "candidates": ";".join(h for _, h in top),
                 "fuzzy_score": f"{top[0][0]:.4f};margin={margin:.4f}" if top else ""})

fields = ["guide_symbol", "match_kind", "confidence", "candidate_count", "candidates", "fuzzy_score"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

from collections import Counter
print("unresolved", len(unresolved), "suggestions", len(rows))
print(Counter(r["match_kind"] for r in rows))
print("wrote", OUT)
