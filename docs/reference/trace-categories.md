---
status: reference-generated
last_verified: 2026-09-15
evidence: ae-debug-trace-lineage.csv + EXP-OBS-002
---
# Trace Categories

The canonical trace-category inventory is generated from retained `Trace Database.txt` profiles across multiple AE generations.

Current corpus summary:
- stable-channel unique trace categories: **405**;
- beta-channel unique trace categories: **221**;
- categories observed in both channels: **212**;
- stable-only vocabulary in the retained corpus: **193**.

Examples relevant to AEIG's core model include `BEE_Eval`, `BEE_Cache`, `BEE_WorkQueue`, `MixHashGuid`, `TDB_StreamBase`, `RenderNode.RG_CacheNodeBase`, `RenderNode.RG_XformNode`, `DiskCache`, GPU categories and render-task categories.

`EXP-OBS-002` proves that trace volume/threshold policy is live at runtime in `dvacore`, not merely archival text. Category presence still does not guarantee that the corresponding provider is registered in a standalone process.

Version lineage matters: the same category name may persist while the private C++ ABI used to configure tracing changes, as observed for `Get/SetTraceVolume` between 25.6 and 26.3.

Treat category names as observability vocabulary, not ABI contracts.

Canonical data: `datasets/ae-debug-trace-lineage.csv`; ABI drift: `datasets/ae-dvacore-trace-abi-lineage.csv`; runtime semantics: `EXP-OBS-002`.