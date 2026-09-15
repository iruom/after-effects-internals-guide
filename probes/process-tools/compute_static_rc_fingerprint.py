from pathlib import Path
import csv, hashlib

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
MAN = ROOT / "datasets" / "aeig-static-rc-manifest.csv"
OUT = ROOT / "datasets" / "aeig-static-rc-fingerprint.txt"

with MAN.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
rows = sorted(rows, key=lambda r: (r["path"], r["role"], r["sha256"]))
canonical = "\n".join(
    f'{r["path"]}\t{r["role"]}\t{r["bytes"]}\t{r["sha256"]}' for r in rows
) + "\n"
fingerprint = hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper()
OUT.write_text(fingerprint + "\n", encoding="utf-8")
print("artifacts", len(rows))
print("sha256", fingerprint)
print("wrote", OUT)
