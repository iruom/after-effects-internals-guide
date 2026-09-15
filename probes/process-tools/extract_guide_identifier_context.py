from pathlib import Path
import csv, html, re
ROOT = Path(r"D:\Developer\After Effects Internals Guide")
HTML = ROOT / "research" / "external-sources" / "guide-26.5" / "print_page.html"
CLS = ROOT / "datasets" / "ae-api-completeness-classification.csv"
OUT = ROOT / "datasets" / "ae-api-guide-unresolved-context.csv"
raw = HTML.read_text(encoding="utf-8", errors="replace")
plain = html.unescape(re.sub(r"<[^>]+>", " ", raw))
plain = re.sub(r"\s+", " ", plain)
with CLS.open(encoding="utf-8", newline="") as f:
    symbols = [r["symbol"] for r in csv.DictReader(f) if r["completeness_class"] in {"guide-only-no-header-match", "guide-near-match-header"}]
rows = []
for symbol in symbols:
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(symbol) + r"(?![A-Za-z0-9_])")
    matches = list(pat.finditer(plain))
    contexts = []
    for m in matches[:4]:
        lo, hi = max(0, m.start()-180), min(len(plain), m.end()+220)
        contexts.append(plain[lo:hi].strip())
    rows.append({"symbol":symbol,"occurrences":len(matches),"contexts":" || ".join(contexts)})
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["symbol","occurrences","contexts"])
    w.writeheader(); w.writerows(rows)
print("symbols", len(rows), "with_context", sum(int(r['occurrences'])>0 for r in rows), "wrote", OUT)

