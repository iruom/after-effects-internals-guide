from pathlib import Path
import csv, sys
from collections import Counter
import os

ROOT = Path(os.environ.get("AEIG_ROOT",r"D:\Developer\After Effects Internals Guide"))
RUN = ROOT / "experiments" / "observatory" / "runs" / "EXP-PLUGIN-001"
LOG = RUN / "suite-acquisition.tsv"
VERSIONS = ROOT / "datasets" / "ae-sdk-25.6-suite-versions.csv"
NAMES = ROOT / "datasets" / "ae-sdk-25.6-suite-names.csv"
OUT = ROOT / "datasets" / "exp-plugin-001-suite-acquisition.csv"
SUMMARY = RUN / "analysis-summary.md"

if not LOG.exists():
    print("not-run: missing", LOG)
    sys.exit(2)

with VERSIONS.open(encoding="utf-8", newline="") as f:
    version_rows = list(csv.DictReader(f))
known = {}
for r in version_rows:
    label = r["suite_macro_base"].removeprefix("k")
    known.setdefault(label, set()).add(int(r["pica_version"]))

with NAMES.open(encoding="utf-8", newline="") as f:
    name_rows = list(csv.DictReader(f))
expected_labels = {r["suite_macro"].removeprefix("k") for r in name_rows}
rows = []
seen = Counter(); malformed = 0
with LOG.open(encoding="utf-8-sig", errors="replace") as f:
    for line in f:
        parts = line.rstrip("\r\n").split("\t")
        if len(parts) != 8:
            malformed += 1; continue
        pid, major, minor, label, suite_name, selector, err, ptr = parts
        try:
            selector_i = int(selector); err_i = int(err)
        except ValueError:
            malformed += 1; continue
        success = err_i == 0 and ptr not in {"0", "0x0", "0000000000000000", "(nil)", ""}
        published = selector_i in known.get(label, set())
        row = {
            "pid": pid, "host_major": major, "host_minor": minor,
            "label": label, "suite_name": suite_name,
            "selector": selector_i, "error": err_i, "suite_ptr": ptr,
            "success": success, "published_25_6_selector": published,
            "unexpected_success": success and not published,
            "published_but_failed": published and not success,
        }
        rows.append(row); seen[(label, selector_i)] += 1

fields = list(rows[0]) if rows else []
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

success_rows = [r for r in rows if r["success"]]
unexpected = [r for r in rows if r["unexpected_success"]]
failed_published = [r for r in rows if r["published_but_failed"]]
missing_labels = sorted(expected_labels - {r["label"] for r in rows})
host_versions = sorted({(r["host_major"], r["host_minor"]) for r in rows})
lines = [
    "# EXP-PLUGIN-001 analysis", "",
    f"- Rows parsed: **{len(rows)}**",
    f"- Successful acquisitions: **{len(success_rows)}**",
    f"- Published 25.6 selectors that failed: **{len(failed_published)}**",
    f"- Successful selectors not published in the 25.6 version table: **{len(unexpected)}**",
    f"- Suite families missing from the log: **{len(missing_labels)}**",
    f"- Host version fields observed: `{host_versions}`", "",
    "## Interpretation rules", "",
    "A successful non-25.6 selector is a runtime observation, not automatically a supported public API; it may be a newer public generation, compatibility alias, or internal/host-specific table.",
    "A published selector failure must be interpreted in host context: some suites are context/host scoped and may not be available to an Artisan AEGP entry point.",
    "Pointer equality across successful selectors does not establish ABI equivalence; table layout remains version-specific unless separately proven.", "",
]
if failed_published:
    lines += ["## Published selectors that failed", ""]
    for r in failed_published[:100]:
        lines.append(f"- `{r['label']}` selector {r['selector']} err={r['error']}")
if unexpected:
    lines += ["", "## Unexpected successful selectors", ""]
    for r in unexpected[:100]:
        lines.append(f"- `{r['label']}` selector {r['selector']} ptr={r['suite_ptr']}")
SUMMARY.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(f"rows={len(rows)} success={len(success_rows)} unexpected={len(unexpected)} published_failed={len(failed_published)} missing_labels={len(missing_labels)}")
print("wrote", OUT); print("wrote", SUMMARY)

# Capture-completeness gate: acquisition may fail, but every name/selector attempt must be logged.
expected_attempts={(label,selector) for label in expected_labels for selector in range(1,33)}
missing_attempts=sorted(expected_attempts-set(seen))
duplicate_attempts=sorted((k,n) for k,n in seen.items() if n!=1)
print("expected_labels",len(expected_labels),"expected_attempts",len(expected_attempts),"missing_attempts",len(missing_attempts),"duplicate_attempts",len(duplicate_attempts),"malformed",malformed)
if not rows:
    sys.exit(3)
if len(expected_labels)!=48 or malformed or missing_labels or missing_attempts or duplicate_attempts:
    if missing_attempts: print("first missing attempts",missing_attempts[:20])
    if duplicate_attempts: print("first duplicate attempts",duplicate_attempts[:20])
    sys.exit(4)
