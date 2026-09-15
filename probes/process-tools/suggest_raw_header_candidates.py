from pathlib import Path
import csv, re, difflib
ROOT = Path(r"D:\Developer\After Effects Internals Guide")
HEADERS = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
SRC = ROOT / "datasets" / "ae-api-completeness-classification.csv"
OUT = ROOT / "datasets" / "ae-api-unresolved-raw-candidates.csv"
PREFIX = r"(?:AEGP|AEIO|AEFX|AE_|A_|PF|DRAWBOT|PrSDK|PrPixelFormat|PR_|kAEGP|kAEIO|kPF|kPr|SP|kSP|FIEL|PT|PICA|PiPL)"
RX = re.compile(r"\b(" + PREFIX + r"[A-Za-z0-9_]*)\b")
text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in HEADERS.rglob("*.h"))
tokens = sorted(set(RX.findall(text)))
with SRC.open(encoding="utf-8", newline="") as f:
    unresolved = [r["symbol"] for r in csv.DictReader(f) if r["completeness_class"] == "guide-only-unresolved"]
rows = []
for s in unresolved:
    prefix_hits = [t for t in tokens if t.startswith(s) and t != s][:8]
    contains_hits = [t for t in tokens if (s in t or t in s) and t != s][:8]
    close = difflib.get_close_matches(s, tokens, n=5, cutoff=0.70)
    rows.append({"guide_symbol":s,"prefix_candidates":";".join(prefix_hits),
                 "containment_candidates":";".join(contains_hits),"fuzzy_candidates":";".join(close)})
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print("unresolved", len(rows), "raw_tokens", len(tokens), "wrote", OUT)
for r in rows:
    if r["prefix_candidates"] or r["containment_candidates"]:
        print(r["guide_symbol"], "=>", r["prefix_candidates"] or r["containment_candidates"])
