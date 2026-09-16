---
status: active
last_verified: 2026-09-16
---
# Querying the Master Surface Registry

`datasets/ae-master-surface-registry.csv` is the cross-surface search index for AEIG.
The current frozen registry contains **53,728 rows / 13 surface classes** spanning public C++, historical headers, scripting, expressions, CEP/UXP, diagnostics, runtime exports, suite negotiation and capability rows.

```powershell
python probes/process-tools/query_master_surface.py RenderGuid
python probes/process-tools/query_master_surface.py "GuideSuite" --kind callback --limit 30
python probes/process-tools/query_master_surface.py "^BEE_" --regex --surface diagnostic-observability
python probes/process-tools/query_master_surface.py --capability-only --facets
python probes/process-tools/query_master_surface.py RenderGuid --format json --limit 0
```

Filters are available for `--surface`, `--support`, `--host`, `--version`, `--kind`, `--contract`, `--source`, `--name`, and `--exact-name`.
Use `--count` for a machine-friendly match count, `--facets` to inspect result composition, and `--format csv|json|tsv` for downstream tooling.

Treat `support_class` and `contract_boundary` as mandatory context. A matching runtime export is not automatically a supported third-party API.
## What the registry is internally
The registry is a normalization/join layer over heterogeneous corpora. Rows from public headers, scripting docs, diagnostic vocabulary, runtime exports, extension substrates and capability records are intentionally searchable together, but their evidence strength is preserved in columns such as surface/support/contract/source/version.

It is **not** a flattened list of callable AE APIs.

The same concept may appear as multiple rows because separate evidence classes observed it. That duplication is useful: cross-surface convergence can be stronger than one isolated match.

## Query strategy
Start broad to discover vocabulary, inspect facets, then narrow by support class and contract boundary. For a developer question, a good sequence is:
1. name/regex search;
2. facet by surface/support/host/version;
3. inspect exact source rows;
4. follow the row back to its primary dataset/document;
5. only then decide whether the surface is usable, internal or merely diagnostic.

Use `--exact-name` when comparing ABI/API names; use regex for families such as `BEE_` or suite generations. `--limit 0` is useful for machine processing but can produce large outputs.## Failure modes
The most dangerous mistake is seeing a runtime export/private string and treating it as a supported third-party entry point. The second is ignoring version/host context and assuming the same name means the same contract forever.

Normalization can also collapse formatting differences intentionally; if byte/ABI spelling matters, return to the source dataset/header instead of relying on the normalized display name.

A zero-result query means “not present in the indexed retained corpora”, not “does not exist anywhere in After Effects”.

## Validation and experiments
Use known positive controls from each surface class when changing the registry builder/query tool. Compare facet totals and exact row counts before/after normalization changes so filtering improvements do not silently erase evidence.

For research, search a concept such as render identity across public hash/receipt APIs, Debug/Trace vocabulary and runtime exports, then write the claim only at the strongest level jointly supported by those rows.

## Unknown frontier
The registry is corpus-scoped. Non-distributed private source, encrypted/stripped symbols, dynamically generated names and uncollected versions remain outside it unless another evidence source adds them.

Cross-links: `master-surface-registry-filtering-note.md`, `corpus-coverage-status.md`, `../foundations/evidence-model.md`, and `../../datasets/ae-master-surface-registry.csv`.