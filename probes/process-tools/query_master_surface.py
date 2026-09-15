from pathlib import Path
import argparse, csv, json, re, sys
from collections import Counter

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DATA = ROOT / "datasets" / "ae-master-surface-registry.csv"
SEARCH_FIELDS = ("name", "container", "source", "evidence", "notes", "contract_boundary")
DEFAULT_FIELDS = ("surface_class", "support_class", "host_scope", "version", "name", "kind", "source")
FACET_FIELDS = ("surface_class", "support_class", "host_scope", "version", "kind", "contract_boundary")


def load():
    with DATA.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def contains(text, needle):
    return needle.lower() in (text or "").lower()


def regex_match(text, pattern):
    return bool(pattern.search(text or ""))


def clean(value):
    return (value or "").replace("\t", " ").replace("\r", " ").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser(description="Query the AEIG Master Surface Registry")
    ap.add_argument("query", nargs="?", default="", help="text across name/container/source/evidence/notes/contract")
    ap.add_argument("--surface", default="", help="surface_class substring")
    ap.add_argument("--support", default="", help="support_class substring")
    ap.add_argument("--host", default="", help="host_scope substring")
    ap.add_argument("--version", default="", help="version substring")
    ap.add_argument("--kind", default="", help="kind substring")
    ap.add_argument("--contract", default="", help="contract_boundary substring")
    ap.add_argument("--source", default="", help="source substring")
    ap.add_argument("--name", default="", help="substring in name only")
    ap.add_argument("--exact-name", default="", help="case-insensitive exact name")
    ap.add_argument("--regex", action="store_true", help="treat query as case-insensitive regular expression")
    ap.add_argument("--capability-only", action="store_true", help="restrict to surface_class=capability")
    ap.add_argument("--limit", type=int, default=50, help="maximum rows to emit; 0 means all")
    ap.add_argument("--json", action="store_true", help="legacy alias for --format json")
    ap.add_argument("--format", choices=("tsv", "json", "csv"), default="tsv")
    ap.add_argument("--count", action="store_true", help="print match count only")
    ap.add_argument("--facets", action="store_true", help="print value counts for major registry dimensions")
    a = ap.parse_args()
    if a.limit < 0:
        ap.error("--limit must be >= 0")

    pattern = None
    if a.regex and a.query:
        try:
            pattern = re.compile(a.query, re.IGNORECASE)
        except re.error as e:
            ap.error(f"invalid --regex query: {e}")

    rows = load()
    out = []
    for r in rows:
        if a.capability_only and r.get("surface_class") != "capability":
            continue
        filters = (
            ("surface_class", a.surface), ("support_class", a.support),
            ("host_scope", a.host), ("version", a.version), ("kind", a.kind),
            ("contract_boundary", a.contract), ("source", a.source), ("name", a.name),
        )
        if any(needle and not contains(r.get(field, ""), needle) for field, needle in filters):
            continue
        if a.exact_name and (r.get("name", "") or "").casefold() != a.exact_name.casefold():
            continue
        blob = " ".join(r.get(k, "") or "" for k in SEARCH_FIELDS)
        if a.query:
            if pattern is not None:
                if not regex_match(blob, pattern):
                    continue
            elif not contains(blob, a.query):
                continue
        out.append(r)

    if a.count:
        print(len(out))
        return

    if a.facets:
        print(f"matches={len(out)} of {len(rows)}")
        for field in FACET_FIELDS:
            counts = Counter(r.get(field, "") or "<empty>" for r in out)
            print(f"[{field}]")
            for value, count in counts.most_common(30):
                print(f"{count}\t{clean(value)}")
        return
    fmt = "json" if a.json else a.format
    selected = out if a.limit == 0 else out[:a.limit]
    if fmt == "json":
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return
    if fmt == "csv":
        w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]) if rows else list(DEFAULT_FIELDS))
        w.writeheader()
        w.writerows(selected)
        return

    print(f"matches={len(out)} of {len(rows)}")
    for r in selected:
        print("\t".join(clean(r.get(k, "")) for k in DEFAULT_FIELDS))
    if a.limit and len(out) > a.limit:
        print(f"... {len(out) - a.limit} more; use --limit 0 for all rows")


if __name__ == "__main__":
    main()
