from pathlib import Path
import csv

ROOT = Path(r"D:\Developer\After Effects Internals Guide")
DATA = ROOT / "datasets"
VERSIONS = DATA / "ae-sdk-25.6-suite-versions.csv"
AEGP_COMPAT = DATA / "ae-sdk-25.6-suite-prefix-compat.csv"
PF_COMPAT = DATA / "ae-sdk-25.6-effect-suite-prefix-compat.csv"
OUT = DATA / "ae-suite-negotiation-matrix.csv"


def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

versions = rows(VERSIONS)
aegp = rows(AEGP_COMPAT)
pf = rows(PF_COMPAT)

compat = {}
for r in aegp:
    family = r["family"]
    old_gen = r["older"].split("Suite")[-1]
    new_gen = r["newer"].split("Suite")[-1]
    compat[(family, old_gen, new_gen)] = (r["older_is_prefix"], r["first_difference"])
for r in pf:
    compat[(r["family"], r["older_generation"], r["newer_generation"])] = (
        r["older_is_prefix"], r["first_difference"])


def family_name(base):
    name = base[1:] if base.startswith("k") else base
    if name.startswith("AEGP"):
        return "AEGP_" + name[4:]
    return name

uniq = {}
for r in versions:
    key = (r["suite_macro_base"], r["generation"], r["pica_version"])
    uniq.setdefault(key, r)

out = []
by_family = {}
for r in uniq.values():
    by_family.setdefault(r["suite_macro_base"], []).append(r)

for base, items in sorted(by_family.items()):
    items.sort(key=lambda x: int(x["generation"] or 0))
    fam = family_name(base)
    prev = None
    for r in items:
        gen = r["generation"]
        pica = int(r["pica_version"])
        relation = "first"
        prefix = ""
        first_diff = ""
        if prev:
            pp = int(prev["pica_version"])
            relation = "increase" if pica > pp else ("same" if pica == pp else "reset/decrease")
            prefix, first_diff = compat.get((fam, prev["generation"], gen), ("unknown", ""))
        rule = "exact-name+exact-version"
        if prefix == "True":
            rule += "; adjacent-table prefix-safe only"
        elif prefix == "False":
            rule += "; aliasing to adjacent generation unsafe"
        elif relation == "reset/decrease":
            rule += "; numeric ordering is explicitly non-generational"
        out.append({
            "suite_macro_base": base,
            "family": fam,
            "generation": gen,
            "pica_version": pica,
            "previous_generation": prev["generation"] if prev else "",
            "previous_pica": prev["pica_version"] if prev else "",
            "pica_relation": relation,
            "adjacent_prefix_safe": prefix,
            "first_difference": first_diff,
            "source": r["source"],
            "header_comment": r["comment"],
            "recommended_dispatch": rule,
        })
        prev = r

# Add effect-side suite generations from the compatibility dataset.
pf_nodes = {}
for r in pf:
    fam = r["family"]
    pf_nodes[(fam, r["older_generation"])] = int(r["older_pica_version"])
    pf_nodes[(fam, r["newer_generation"])] = int(r["newer_pica_version"])
for fam in sorted({k[0] for k in pf_nodes}):
    gens = sorted((int(g), p) for (f, g), p in pf_nodes.items() if f == fam)
    prev = None
    for gen_i, pica in gens:
        gen = str(gen_i)
        relation = "first" if prev is None else ("increase" if pica > prev[1] else ("same" if pica == prev[1] else "reset/decrease"))
        prefix = ""; first_diff = ""
        if prev is not None:
            prefix, first_diff = compat.get((fam, str(prev[0]), gen), ("unknown", ""))
        rule = "exact-name+exact-version"
        if prefix == "True": rule += "; adjacent-table prefix-safe only"
        elif prefix == "False": rule += "; aliasing to adjacent generation unsafe"
        if relation == "reset/decrease": rule += "; numeric ordering is explicitly non-generational"
        out.append({"suite_macro_base": "", "family": fam, "generation": gen, "pica_version": pica,
                    "previous_generation": str(prev[0]) if prev else "", "previous_pica": prev[1] if prev else "",
                    "pica_relation": relation, "adjacent_prefix_safe": prefix, "first_difference": first_diff,
                    "source": "ae-sdk-25.6-effect-suite-prefix-compat.csv", "header_comment": "", "recommended_dispatch": rule})
        prev = (gen_i, pica)

fields = list(out[0])
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(out)

families = len({r['family'] for r in out})
resets = sum(r["pica_relation"] == "reset/decrease" for r in out)
unsafe = sum(r["adjacent_prefix_safe"] == "False" for r in out)
safe = sum(r["adjacent_prefix_safe"] == "True" for r in out)
unknown = sum(r["adjacent_prefix_safe"] == "unknown" for r in out)
print(f"rows={len(out)} families={families} resets={resets} prefix_safe={safe} prefix_unsafe={unsafe} prefix_unknown={unknown}")
print("wrote", OUT)
