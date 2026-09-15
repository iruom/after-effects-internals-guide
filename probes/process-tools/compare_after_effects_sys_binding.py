from __future__ import annotations
import csv, re, subprocess
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
BIND = ROOT / "research" / "external-sources" / "after-effects-rs" / "after-effects-sys" / "bindings_win.rs"
HDR = Path(r"E:\ae25.6_61.64bit.AfterEffectsSDK\Examples\Headers")
OUT = ROOT / "datasets" / "ae-after-effects-sys-binding-corroboration.csv"
STATUS = ROOT / "docs" / "reference" / "binding-corroboration-status.md"

bind = BIND.read_text(encoding="utf-8", errors="ignore")
headers = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in HDR.rglob("*.h"))

# Numeric API/version selectors are the strongest bindgen/header comparison surface.
name_rx = re.compile(r"^(?:PF_AE\d+_PLUG_IN_(?:SUBVERS|VERSION)|k[A-Za-z0-9_]*Suite(?:_?Version|Version)[A-Za-z0-9_]*)$")

def parse_int(text: str):
    text = text.strip().rstrip("uUlL")
    try: return int(text, 0)
    except ValueError: return None
hvals = {}
for m in re.finditer(r"^\s*#\s*define\s+([A-Za-z_]\w*)\s+([^\s/]+)", headers, re.M):
    name, raw = m.group(1), m.group(2)
    if name_rx.match(name):
        value = parse_int(raw)
        if value is not None: hvals[name] = value

bvals = {}
for m in re.finditer(r"^pub const ([A-Za-z_]\w*):[^=]+?=\s*([^;]+);", bind, re.M):
    name, raw = m.group(1), m.group(2)
    if name_rx.match(name):
        value = parse_int(raw)
        if value is not None: bvals[name] = value

names = sorted(set(hvals) | set(bvals))
rows = []
for name in names:
    hv, bv = hvals.get(name), bvals.get(name)
    rows.append({
        "symbol": name,
        "header_25_6_value": "" if hv is None else hv,
        "binding_value": "" if bv is None else bv,
        "in_header_25_6": hv is not None,
        "in_binding": bv is not None,
        "value_equal": hv is not None and bv is not None and hv == bv,
    })
fields = list(rows[0]) if rows else []
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(rows)

both = [r for r in rows if r["in_header_25_6"] and r["in_binding"]]
equal = [r for r in both if r["value_equal"]]
mismatch = [r for r in both if not r["value_equal"]]
header_only = [r for r in rows if r["in_header_25_6"] and not r["in_binding"]]
binding_only = [r for r in rows if r["in_binding"] and not r["in_header_25_6"]]

repo = ROOT / "research" / "external-sources" / "after-effects-rs"
commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
commit_date = subprocess.check_output(["git", "-C", str(repo), "show", "-s", "--format=%cI", "HEAD"], text=True).strip()
ansi_comment = "PF_ANSICallbacksSuite2" in headers
ansi_binding = "PF_ANSICallbacksSuite2" in bind

lines = ["---", "status: generated", "last_verified: 2026-09-15", "---",
         "# after-effects-sys Binding Corroboration", "",
         f"Snapshot commit: `{commit}` ({commit_date}).", "",
         f"Numeric API/suite version names compared: **{len(rows)}**.",
         f"Present in both: **{len(both)}**; exact numeric matches: **{len(equal)}**; mismatches: **{len(mismatch)}**.",
         f"Header-only numeric selectors: **{len(header_only)}**; binding-only: **{len(binding_only)}**.", "",
         "This is independent generated-binding evidence, not an Adobe SDK authority and not a historical SDK substitute.",
         f"`PF_ANSICallbacksSuite2` token in 25.6 header corpus: **{ansi_comment}**; generated binding symbol: **{ansi_binding}**."]
STATUS.write_text("\n".join(lines)+"\n", encoding="utf-8")
print("rows", len(rows), "both", len(both), "equal", len(equal), "mismatch", len(mismatch), "header_only", len(header_only), "binding_only", len(binding_only))
print("mismatch symbols", [(r['symbol'], r['header_25_6_value'], r['binding_value']) for r in mismatch])
print("header-only", [r['symbol'] for r in header_only])
print("binding-only", [r['symbol'] for r in binding_only])
print("wrote", OUT); print("wrote", STATUS)
