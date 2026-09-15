from pathlib import Path
import csv
import hashlib
import json
from collections import defaultdict, Counter

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
CACHE_RUN = ROOT / "experiments" / "observatory" / "runs" / "EXP-CACHE-002"
PLUGIN_RUN = ROOT / "experiments" / "observatory" / "runs" / "EXP-PLUGIN-001"
DATA = ROOT / "datasets"

RECEIPT = CACHE_RUN / "receipt-matrix.tsv"
SUITES = PLUGIN_RUN / "suite-acquisition.tsv"
STATUS_NAME = {0: "INVALID", 1: "VALID", 2: "VALID_BUT_INCOMPLETE"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def parse_int(text: str) -> int:
    return int(text.strip(), 0)


def analyze_receipts():
    if not RECEIPT.exists():
        print("receipt: MISSING", RECEIPT)
        return False
    rows = []
    with RECEIPT.open("r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) != 8:
                continue
            rows.append({"pid": p[0], "kind": p[1], "num_effects": parse_int(p[2]),
                         "generated": parse_int(p[3]), "requested": parse_int(p[4]),
                         "geom": parse_int(p[5]), "status": parse_int(p[6]), "err": parse_int(p[7])})
    checks = [r for r in rows if r["kind"] == "CHECK"]
    out = DATA / "exp-cache-002-receipt-matrix-summary.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        fields = ["pid", "num_effects", "generated", "requested", "geom", "status", "status_name", "err"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in checks:
            w.writerow({**r, "status_name": STATUS_NAME.get(r["status"], f"UNKNOWN_{r['status']}")})
    counts = Counter((r["status"], r["err"]) for r in checks)
    print("receipt:", len(rows), "rows;", len(checks), "checks; sha256", sha256(RECEIPT))
    print("receipt status/error counts:", dict(counts))
    unique = defaultdict(set)
    for r in checks:
        unique[(r["generated"], r["requested"], r["geom"])].add((r["status"], r["err"]))
    unstable = {k: v for k, v in unique.items() if len(v) > 1}
    print("receipt inconsistent matrix cells:", len(unstable))
    return True


def analyze_suites():
    if not SUITES.exists():
        print("suites: MISSING", SUITES)
        return False
    rows = []
    with SUITES.open("r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            p = line.rstrip("\r\n").split("\t")
            if len(p) != 8:
                continue
            rows.append({"pid": p[0], "host_major": p[1], "host_minor": p[2],
                         "label": p[3], "suite_name": p[4], "selector": parse_int(p[5]),
                         "err": parse_int(p[6]), "ptr": p[7]})
    success = [r for r in rows if r["err"] == 0 and r["ptr"].lower() not in {"0x0000000000000000", "0x0", "(nil)", "0000000000000000"}]
    out = DATA / "exp-plugin-001-suite-acquisition.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        fields = ["pid", "host_major", "host_minor", "label", "suite_name", "selector", "err", "ptr"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(success)
    by_suite = defaultdict(list)
    for r in success:
        by_suite[(r["label"], r["suite_name"])].append(r["selector"])
    print("suites:", len(rows), "attempts;", len(success), "successful acquisitions; sha256", sha256(SUITES))
    for (label, name), selectors in sorted(by_suite.items()):
        print(f"  {label}: {sorted(set(selectors))} ({name})")
    return True


def main():
    receipt_ok = analyze_receipts()
    suite_ok = analyze_suites()
    fixture = CACHE_RUN / "fixture-script.log"
    if fixture.exists():
        print("fixture log:")
        print(fixture.read_text(encoding="utf-8-sig", errors="replace"))
    else:
        print("fixture: MISSING", fixture)
    if receipt_ok and suite_ok:
        print("USER CORE PROBES: captures present")
        return 0
    print("USER CORE PROBES: incomplete")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
