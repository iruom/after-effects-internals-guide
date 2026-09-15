---
id: F-ABI-021
status: confirmed
evidence: replicated-host-runtime-probe
last_verified: 2026-09-15
---
# Runtime suite negotiation is family-scoped

## Finding
`EXP-PLUGIN-001` probed 48 AEGP suite families across selectors 1..32 in After Effects 26.3, producing all **1,536/1,536** expected attempts.

The host accepted **147** acquisitions and exposed **26 distinct selector-acceptance patterns** across the 48 suite families. Therefore PICA selector integers are scoped to suite name; they do not form one global monotonic generation namespace.

Nine successful selectors were not in the distributed 25.6 suite-version table, including `AEGPCompSuite` 27, `AEGPGuideSuite` 1/2 and `AEGPItemViewSuite` 2. These are runtime observations, not automatically supported 25.6 contracts.

Three published 25.6 selectors failed in this Artisan entry context (`AEGPCanvasSuite` 4/6 and `AEGPRenderQueueMonitorSuite` 1). Contextual acquisition failure is not evidence of capability removal.

## Consequence
Independent hosts and compatibility layers must dispatch on **suite name + exact selector + context**. Returning one latest table for every selector can produce ABI aliasing even when the integer appears newer.

Evidence: `experiments/observatory/runs/EXP-PLUGIN-001/suite-acquisition.tsv` and `datasets/exp-plugin-001-suite-acquisition.csv`.
