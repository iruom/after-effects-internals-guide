from pathlib import Path
import csv, hashlib, re, sys

ROOT=Path(r"D:\Developer\After Effects Internals Guide")
DATA=ROOT/"datasets"
MAN=DATA/"aeig-static-rc-manifest.csv"
LOCK=DATA/"aeig-prediction-lock.csv"
PRED=DATA/"aeig-prediction-log.csv"
FP=DATA/"aeig-static-rc-fingerprint.txt"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def read(path):
    with path.open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def canonical_fingerprint(rows):
    ordered=sorted(rows,key=lambda r:(r["path"],r["role"],r["sha256"]))
    payload="\n".join(
        f'{r["path"]}\t{r["role"]}\t{r["bytes"]}\t{r["sha256"]}' for r in ordered
    )+"\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
if not MAN.exists() or not LOCK.exists():
    raise SystemExit("static RC is not frozen")
errors=[]
manifest=read(MAN)
for r in manifest:
    p=ROOT/Path(r["path"])
    if not p.exists():
        errors.append(f"missing:{r['path']}")
        continue
    if str(p.stat().st_size)!=r["bytes"]:
        errors.append(f"size:{r['path']}")
    elif sha(p)!=r["sha256"]:
        errors.append(f"sha256:{r['path']}")

lock_fields=["prediction_id","mode","domain","source_experiment",
             "prediction","falsified_by","locked_before_run"]
locked=read(LOCK)
current=[r for r in read(PRED) if r.get("mode")=="prospective"]
normalize=lambda rows:[{k:r.get(k,"") for k in lock_fields} for r in rows]
if normalize(current)!=normalize(locked):
    errors.append("prediction-lock-mismatch")

expected_fp=canonical_fingerprint(manifest)
if not FP.exists():
    errors.append("fingerprint-missing")
else:
    text=FP.read_text(encoding="utf-8-sig",errors="replace")
    m=re.search(r"\b([0-9A-Fa-f]{64})\b",text)
    actual_fp=m.group(1).upper() if m else ""
    if actual_fp!=expected_fp:
        errors.append(f"fingerprint-mismatch:{actual_fp or 'unparseable'}")

if errors:
    print("AEIG static RC verification: FAIL")
    for e in errors: print(e)
    sys.exit(1)
print("AEIG static RC verification: PASS")
print("artifacts",len(manifest),"predictions",len(locked))
print("fingerprint",expected_fp)
