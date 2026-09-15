---
id: F-ABI-013
status: confirmed-distribution
confidence: high
evidence: [E0-H, E1-L]
version_scope: "AE 25.6 distributed AEGP/PF headers plus retained old-suite tables"
last_verified: 2026-09-15
---
# F-ABI-013 — Suite negotiation is a two-key ABI contract

The host contract is keyed by **suite name + requested PICA version**. Suite generation names and numeric PICA versions are not interchangeable ordinals.

The generated `ae-suite-negotiation-matrix.csv` contains 158 generation rows across 54 AEGP/PF suite families. Among transitions whose layouts have been mechanically compared, 26 are prefix-safe and 20 are not.

`PFAppSuite5 -> PFAppSuite6` also demonstrates a numeric reset: PICA version `7 -> 1` while the C table generation increases. Numeric greater-than/less-than tests therefore cannot represent generation ordering.

## Host-emulator consequence
A host must dispatch on the exact requested pair and return a table compatible with that exact ABI. Returning one modern vtable across a numeric range is only justified after a per-transition compatibility proof.

Known unsafe transitions include major Comp, Item, Stream, Utility, `PFAppSuite`, `PF_ParamUtilsSuite`, and `PF_WorldSuite` changes. Some Item generations even shrink or reorder tables.

## Boundary of this finding
The matrix proves distributed ABI layout/version relationships, not which versions a particular installed AE build will successfully acquire at runtime. That runtime acceptance matrix remains the user-run Plugin Host experiment.

Machine source: `probes/process-tools/build_suite_negotiation_matrix.py`.
Dataset: `datasets/ae-suite-negotiation-matrix.csv`.
