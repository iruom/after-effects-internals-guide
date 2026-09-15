---
id: F-ABI-019
status: confirmed
evidence: distributed-header-lineage
last_verified: 2026-09-15
---
# Product version is not the PF Effect API version

## Finding
The After Effects 25.6 `AE_Effect.h` retains 36 historical `PF_AE*_PLUG_IN_VERSION/SUBVERS` markers from AE 3.1 through AE 23.5.

The current 25.6 aliases still resolve to the AE 23.5 marker: API major `13`, subversion `29`. Product releases therefore do not define a monotonic one-to-one PF API version sequence.

Examples include AE 15.0 and 15.1 sharing subversion 15, and the jump from AE 18.4 subversion 26 to AE 22.0 subversion 27. Newer capabilities may also arrive through independently versioned PICA suites without changing the PF API pair.

## Consequence
Compatibility logic must use the actual host/plugin API fields and exact suite negotiation contracts, not the marketing/product version alone. See `datasets/ae-pf-api-version-lineage.csv` and `F-ABI-013-suite-negotiation-is-a-two-key-contract.md`.
