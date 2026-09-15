---
status: confirmed-reimplementation-risk
last_verified: 2026-09-15
evidence: AE-25.6-distributed-headers + AexExecutor + aexlo
---
# F-ABI-006 — Independent hosts expose three distinct Suite-dispatch failure classes

Reviewing AexExecutor and `potistudio/aexlo` against the distributed AE 25.6 headers separates host-emulation failure into at least three layers.

## 1. Capability-presence fabrication
AexExecutor dispatches implemented suites primarily by name and does not use the requested integer to select a version-specific table. For broad Adobe-looking names it can return a 1024-slot generic table whose entries all point to `unknown_suite_fn`, which returns `A_Err_NONE`.

Acquisition success therefore does not prove that the requested capability, output initialization, ownership, or semantics exist.

## 2. ABI aliasing
`aexlo` is substantially stricter: it dispatches on `(name, version)` ranges and uses typed vtables for many suites. However, several ranges alias multiple requested versions to one table without a valid Adobe prefix-compatibility proof.

Confirmed hazards include:
- `PF AE App Suite`: aexlo accepts `1..=6` as `PFAppSuite6`; Adobe maps PICA 6 to Suite4, 7 to Suite5, and 1 to Suite6.
- `PF Param Utils Suite`: PICA 2 is the old Suite1 layout, which is not prefix-compatible with Suite3/PICA 3.
- `PF Utility Suite`: Adobe explicitly requires a separate v4 table because `GetClipName` was versioned incorrectly.- `AEGP Utility Suite`: aexlo accepts `1..=18` but returns one hand-built `CompatV11` offset table. AE 25.6 publishes only PICA 3, 5, 7, 10, 11, and 13 for UtilitySuite1..6, and the historical layouts are not universally prefix-compatible.

The AEGP Utility mechanical comparison finds two concrete layout breaks:
- Suite3 → Suite4: first mismatch at index 5 (`AEGP_StartUndoGroup` → `AEGP_GetLastErrorMessage`).
- Suite5 → Suite6: first mismatch at index 1 (`AEGP_GetDriverPluginInitFuncVersion` → `AEGP_ReportInfoUnicode`).

## 3. Semantic-success stubbing
Even when the table shape is callable, a callback that simply returns success can violate the contract if required outputs are not populated or host state is not changed.

AexExecutor's generic table makes this explicit. `aexlo` also has typed `stub_log!` callbacks that return `PF_Err_NONE`; those must be audited separately from vtable layout correctness.

## Negative controls: aliases that do survive header review
Not every aexlo alias is wrong. Header comparison supports:
- `PF Iterate8 Suite` v1 → v2;
- `PF iterate16 Suite` v1 → v2;
- `PF iterateFloat Suite` v1 → v2;
- `PF Pixel Data Suite` v1 → v2, where the GPU accessor is appended.

This is important: prefix compatibility is a property to prove per transition, not a property to assume or reject globally.
## Host rule reconstructed from the comparison
Treat `(suite name, requested PICA integer)` as an exact ABI key. A compatibility alias is admissible only when all of the following are established:
1. the requested integer is a published/observed version for that suite name;
2. the returned table preserves the requested function order and size prefix;
3. overlapping function signatures remain ABI-compatible;
4. overlapping callbacks preserve required semantics, outputs, ownership and lifetime;
5. acquisition/release behavior matches the advertised capability.

A callable vtable is therefore weaker than an ABI-compatible vtable, and ABI compatibility is weaker than host-semantic compatibility.

## Reproducible artifacts
- `probes/process-tools/audit_aexlo_suite_dispatch.py`
- `datasets/aexlo-suite-dispatch-audit.csv`
- `probes/process-tools/analyze_effect_suite_compat.py`
- `probes/process-tools/analyze_suite_prefix_compat.py`
- `datasets/ae-sdk-25.6-effect-suite-prefix-compat.csv`
- `datasets/ae-sdk-25.6-suite-prefix-compat.csv`

These comparisons are evidence about the reviewed independent-host snapshots and Adobe header contracts. They are not evidence that real After Effects internally aliases suites in the same way.
## 2026-09-15 semantic-stub audit refinement
`probes/process-tools/audit_semantic_success_stubs.py` now makes failure class 3 measurable. In the reviewed aexlo snapshot it finds 48 `stub_log!` callbacks; 44 have mutable/explicit output arguments yet the macro writes none of them before returning `PF_Err_NONE`. Four more are setter/dependency-style no-op successes. AexExecutor contributes a separate generic 1024-slot success fallback.

See `datasets/independent-host-semantic-success-stubs.csv` and `F-ABI-008-success-stubs-fabricate-host-semantics.md`.
