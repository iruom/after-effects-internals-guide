from pathlib import Path
from datetime import date
import csv, hashlib

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"
MAN=DATA/"aeig-static-rc-manifest.csv"
OUT=DATA/"aeig-static-rc-fingerprint.txt"
DOC=ROOT/"docs"/"reference"/"static-rc-fingerprint.md"

with MAN.open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
rows=sorted(rows,key=lambda r:(r["path"],r["role"],r["sha256"]))
canonical="\n".join(
    f'{r["path"]}\t{r["role"]}\t{r["bytes"]}\t{r["sha256"]}' for r in rows
)+"\n"
fingerprint=hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()
OUT.write_text(fingerprint+"\n",encoding="utf-8")
lines=[
    "---","status: generated",f"last_verified: {date.today().isoformat()}","---",
    "# AEIG Static RC Fingerprint","",
    f"Frozen artifacts: **{len(rows)}**.",
    f"Canonical aggregate SHA-256: `{fingerprint}`.","",
    "The fingerprint is calculated from sorted `path / role / bytes / sha256` rows in",
    "`datasets/aeig-static-rc-manifest.csv`.","",
    "It is a convenience digest, not a replacement for per-artifact verification.",
    "`verify_aeig_static_rc.py` remains the authoritative fail-closed verifier.",
]
DOC.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("static_rc_fingerprint",fingerprint)
print("artifacts",len(rows))
print("wrote",OUT)
print("wrote",DOC)
