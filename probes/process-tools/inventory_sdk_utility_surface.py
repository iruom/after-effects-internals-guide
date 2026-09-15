from pathlib import Path
import csv, re
ROOT = Path(r"D:\Developer\After Effects Internals Guide")
UTIL = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Util")
OUT = ROOT / "datasets" / "ae-sdk-25.6-utility-identifiers.csv"
PREFIX = r"(?:AEGP|AEIO|AEFX|AE_|A_|PF|DRAWBOT|PrSDK|PrPixelFormat|PR_|kAEGP|kAEIO|kPF|kPr|SP|kSP|FIEL|PT|PICA|PiPL)"
IDENT = re.compile(r"\b(" + PREFIX + r"[A-Za-z0-9_]*)\b")
rows = []
for p in sorted(UTIL.rglob("*.h")):
    text = p.read_text(encoding="utf-8", errors="ignore")
    rel = str(p.relative_to(UTIL))
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        names = set(IDENT.findall(line))
        for name in names:
            kind = "raw-token"
            if re.search(r"^\s*#\s*define\s+" + re.escape(name) + r"\b", line): kind = "macro"
            elif re.search(r"\b(?:class|struct|enum)\s+" + re.escape(name) + r"\b", line): kind = "type"
            elif re.search(r"\b" + re.escape(name) + r"\s*\(", line): kind = "callable-or-ctor"
            rows.append({"symbol":name,"source":rel,"line":i,"kind":kind,"surface":"sdk-25.6-util"})
uniq = {(r["symbol"],r["source"],r["line"],r["kind"]):r for r in rows}
rows = sorted(uniq.values(), key=lambda r:(r["symbol"],r["source"],r["line"]))
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["symbol","source","line","kind","surface"])
    w.writeheader(); w.writerows(rows)
print("rows", len(rows), "unique", len({r['symbol'] for r in rows}), "wrote", OUT)
