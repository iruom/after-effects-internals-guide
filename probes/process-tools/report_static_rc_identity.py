from pathlib import Path
from datetime import date
import csv, re

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"
OUT=ROOT/"docs"/"reference"/"static-rc-identity.md"

def rows(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

manifest=rows(DATA/"aeig-static-rc-manifest.csv")
lock=rows(DATA/"aeig-prediction-lock.csv")
text=(DATA/"aeig-static-rc-fingerprint.txt").read_text(encoding="utf-8-sig")
m=re.search(r"\b[0-9A-Fa-f]{64}\b",text)
fingerprint=m.group(0).upper() if m else "UNAVAILABLE"
lines=[
    "---","status: generated",f"last_verified: {date.today().isoformat()}","---",
    "# Static RC Identity","",
    f"AEIG 1.0 の operator run 前 Static RC は、`datasets/aeig-static-rc-manifest.csv` に列挙された **{len(manifest)} artifacts** で固定されている。","",
    "Canonical fingerprint:","",f"`{fingerprint}`","",
    "算出規則は manifest 行を `path / role / bytes / sha256` で canonical serialization し、UTF-8列へ SHA-256 を適用する。","",
    "このfingerprintは個々のartifact hashの代替ではなく、RC全体のsummary identityである。`verify_aeig_static_rc.py` は各artifact、prediction lock、aggregate fingerprintをすべてfail-closedで検証する。","",
    "## Prediction lock","",
    f"Prospective predictions は **{len(lock)}件**。観測後にstatus/evidenceは変化できるが、immutable予測本文は `datasets/aeig-prediction-lock.csv` で固定されている。",
]
OUT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("wrote",OUT)
print("fingerprint",fingerprint,"artifacts",len(manifest),"predictions",len(lock))
