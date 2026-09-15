---
status: active
last_verified: 2026-09-16
evidence: deterministic Master Surface Registry build pipeline
---
# Master Registry Filtering and Normalization

The Master Surface Registry is an **index of meaningful discoverable surfaces**, not a lossless concatenation of every parser row. Raw corpora contain packaging metadata, binary-dump scaffolding, duplicate representations and evidence rows that are useful for provenance but are not themselves API/capability names.

Current normalized registry size: **53,728 rows** across 13 surface classes.

## Why filtering is necessary
For example, PE/dumpbin inventories can contain headings such as `Dump of file`, timestamp labels, Import Address Table metadata and forwarding-table scaffolding. Keeping these as named extension/native surfaces would inflate counts and make search results lie about what AE actually exposes.

Filtering therefore removes parser structure while preserving the original source dataset. The registry is a derived search/index layer; raw evidence remains available for audit.

## Normalization rule
Each row carries a surface class, support class, host/version scope, name/kind/container, source/evidence and an explicit contract boundary. The same spelling can legitimately appear more than once when evidence/support/version meaning differs.

Do **not** deduplicate solely by `name`. `Render`, `AcquireSuite`, an internal export and a documented public function with similar labels may be completely different contracts.

## Current source contribution
The build currently normalizes these retained source families:
- native C++: 28,917 rows;
- scripting + expressions: 1,021;
- runtime internal exports: 21,132;
- private header gates: 6;
- filtered extension substrate: 642;
- Debug/Trace lineage: 1,711;
- capability frontier: 24;
- headless entrypoints: 42;
- historical CEP: 75;
- suite negotiation: 158.

Their contribution sum reproduces the registry total exactly. Release audit also requires all expected surface classes and rejects blank `name`, `support_class`, `host_scope` or `source` fields.

## Derived labels
Some raw evidence has no natural API symbol name, especially manifest/runtime rows. In those cases the registry can use a clearly documented search label derived from the manifest directory/host or suite family. A derived label is an index key, not evidence that AE publishes that exact spelling as an API.

## Support-boundary rule
Runtime-visible exports remain `runtime-visible-unsupported`; trace keys remain diagnostic vocabulary; private header gates remain private-boundary evidence. Normalization must never upgrade support classification just to make the registry easier to query.

## Failure modes in registry construction
Bad normalization can create two opposite errors: **false surfaces** from parser scaffolding and **false completeness** from over-aggressive deduplication. Both are dangerous because downstream users may treat registry search as authoritative.

Every new corpus importer should therefore be tested with adversarial rows: headings, blank names, duplicate names from distinct versions, same symbol under different support classes, forwarded exports and manifest entries without UI entry points.

## Reproducibility
`probes/process-tools/build_master_surface_registry.py` rebuilds the registry deterministically from source datasets. `query_master_surface.py` provides surface/support/host/version/kind/contract/source/name filtering plus regex/facets/count output so users can inspect the normalized model without editing CSV manually.

When a row looks suspicious, follow its `source`/`evidence` back to the raw dataset before drawing implementation conclusions.

Related: `docs/reference/master-surface-registry.md`, `docs/reference/master-surface-query.md`, `datasets/ae-master-surface-registry.csv`, and the corpus-coverage/unknown-frontier pages.

## Unknown frontier
A normalized registry can only be complete against acquired corpora. Non-exported private implementation, unavailable historical packages and undiscovered first-party contracts remain outside the inventory and must stay explicit unknowns rather than being inferred absent.
