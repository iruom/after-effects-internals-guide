from pathlib import Path
import csv, re

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
SDK = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples")
OUT = ROOT / "datasets" / "ae-sdk-25.6-distributed-support-identifiers.csv"
PREFIX = r"(?:AEGP|AEIO|AEFX|AE_|A_|PF|DRAWBOT|PrSDK|PrPixelFormat|PR_|kAEGP|kAEIO|kPF|kPr|SP|kSP|FIEL|PT|PICA|PiPL)"
IDENT = re.compile(r"\b(" + PREFIX + r"[A-Za-z0-9_]*)\b")
TEXT_EXT = {".h", ".hpp", ".c", ".cpp", ".r", ".rr", ".rc", ".txt",
            ".vcxproj", ".props", ".targets", ".xcconfig", ".plist"}

def category(rel: Path) -> str:
    parts = {p.lower() for p in rel.parts}
    if "headers" in parts: return "header"
    if "util" in parts: return "utility"
    if rel.suffix.lower() in {".r", ".rr", ".rc"}: return "resource"
    if rel.suffix.lower() in {".vcxproj", ".props", ".targets", ".xcconfig", ".plist"}: return "build-config"
    return "sample-source"

rows = []
for p in sorted(SDK.rglob("*")):
    if not p.is_file() or p.suffix.lower() not in TEXT_EXT: continue
    rel = p.relative_to(SDK)
    text = p.read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(text.splitlines(), 1):
        for symbol in set(IDENT.findall(line)):
            rows.append({"symbol": symbol, "surface_category": category(rel),
                         "source": str(rel), "line": i})
uniq = {(r["symbol"], r["surface_category"], r["source"], r["line"]): r for r in rows}
rows = sorted(uniq.values(), key=lambda r:(r["symbol"], r["surface_category"], r["source"], r["line"]))
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["symbol", "surface_category", "source", "line"])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print("rows", len(rows), "unique", len({r['symbol'] for r in rows}))
print("categories", dict(Counter(r["surface_category"] for r in rows)))
print("wrote", OUT)
