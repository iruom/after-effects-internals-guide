from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
MANIFESTS = ROOT / r"experiments\observatory\manifests"
VALID_STATUS = {"planned", "runnable", "observed", "replicated"}
REQUIRED = {"experiment_id", "title", "status", "domains", "question", "hypotheses", "environment", "captures"}

errors: list[str] = []
rows: list[tuple[str, str, bool]] = []
for path in sorted(MANIFESTS.glob("*.json")):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        continue
    missing = sorted(REQUIRED - data.keys())
    if missing:
        errors.append(f"{path.name}: missing {missing}")
    status = data.get("status", "")
    if status not in VALID_STATUS:
        errors.append(f"{path.name}: bad status {status!r}")
    result = data.get("result")
    l5_ready = False
    if status in {"observed", "replicated"}:
        if not isinstance(result, dict):
            errors.append(f"{path.name}: {status} requires result object")
        else:
            needed = [k for k in ("conclusion", "raw_outputs", "hashes") if not result.get(k)]
            if needed:
                errors.append(f"{path.name}: {status} result missing {needed}")
            else:
                l5_ready = True
    rows.append((data.get("experiment_id", path.stem), status, l5_ready))

print(f"manifests {len(rows)}")
for exp_id, status, ready in rows:
    print(f"{exp_id}: {status}; L5-evidence={'yes' if ready else 'no'}")
if errors:
    print("errors:")
    for err in errors:
        print(" -", err)
    raise SystemExit(1)
print("validation ok")
