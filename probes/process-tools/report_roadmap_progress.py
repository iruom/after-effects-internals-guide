from __future__ import annotations
import csv, re
from pathlib import Path
from datetime import date

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
SRC = ROOT / r"datasets\aeig-domain-coverage.csv"
OUT = ROOT / r"datasets\aeig-roadmap-progress.csv"
STATUS = ROOT / r"docs\reference\roadmap-status.md"
CORE = {"evaluation", "render-graph", "cache", "state-identity", "plugin-host", "observability"}

def level_num(value: str) -> int:
    m = re.match(r"L(\d+)", value.strip())
    return int(m.group(1)) if m else 0

with SRC.open(encoding="utf-8-sig", newline="") as f:
    domains = list(csv.DictReader(f))

rows = []
for d in domains:
    current = level_num(d["current_level"])
    target = 5 if d["domain"] in CORE else (3 if d["priority"] in {"high", "critical"} else 2)
    rows.append({**d, "target_level": f"L{target}", "level_gap": max(target-current, 0), "meets_1_0_target": current >= target})

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)

counts = {n: sum(level_num(r["current_level"]) == n for r in rows) for n in range(8)}
met = sum(bool(r["meets_1_0_target"]) for r in rows)
open_rows = sorted((r for r in rows if not r["meets_1_0_target"]), key=lambda r: (-int(r["level_gap"]), r["domain"]))

lines = [
    "---", "status: generated", f"last_verified: {date.today().isoformat()}", "---",
    "# Roadmap Status", "",
    f"Domains meeting the AEIG 1.0 minimum: **{met}/{len(rows)}**.", "",
    "## Current coverage distribution", "",
]
for n, count in counts.items():
    if count:
        lines.append(f"- L{n}: {count} domains")

lines += ["", "## Largest gaps", "", "| Domain | Current | Target | Gap | Next evidence |", "|---|---:|---:|---:|---|"]
for r in open_rows[:15]:
    next_evidence = r["next_evidence"].replace("|", "/")
    lines.append(f"| {r['domain']} | {r['current_level']} | {r['target_level']} | {r['level_gap']} | {next_evidence} |")
lines += [
    "", "This page is generated from `datasets/aeig-domain-coverage.csv` by `report_roadmap_progress.py`.",
    "The target rule is intentionally conservative: core domains L5, other high/critical domains L3, all others L2.",
]
STATUS.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"domains {len(rows)} met {met}")
print("coverage", {f"L{k}": v for k, v in counts.items() if v})
print(f"wrote {OUT}")
print(f"wrote {STATUS}")
