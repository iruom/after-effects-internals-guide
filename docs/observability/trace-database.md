---
status: active
last_verified: 2026-09-14
---
# Trace Database

`Trace Database.txt` is one of the highest-value internal observability artifacts found so far.

Characteristic recent categories:
- `BEE_Eval`, `BEE_Cache`, `BEE_Project`, `BEE_Undo`, `BEE_WorkQueue`
- `RenderNode.RG_CacheNodeBase`, `RenderNode.RG_XformNode`
- `RenderTaskManager`, `RenderThreadExecutor`
- `CheckoutItemFrameAsync`, `StaticCheckoutItemFrameAsync`
- `MixHashGuid`
- `DataCacheInFilesystem`, `DiskCache`
- `TDB_StreamBase`
- `U_Context`, `U_RenderContext`, `U_THREADS`
- `GPU Render Pipeline`, `GPUFoundation`, `PF_GPU`

Next phase: enable/collect trace output safely and map category activation to controlled operations.

## Replicated runtime threshold experiment
`EXP-OBS-002` upgrades the Trace Database model from static archaeology to observed runtime policy. In AE 25.6's installed `dvacore.dll`, `TraceEnabled` responds to both the master trace volume and the category volume.

For a category whose observed volume is 5:
- master 3: levels 2/4/6 -> `true/false/false`
- master 10: levels 2/4/6 -> `true/true/false`

The experiment was repeated in two fresh processes with identical decision stdout. Conditional trace emission produced the expected level-2-only marker at master 3 and an additional level-4 marker at master 10.

### Implementation boundary
`Trace()` is a low-level emitter and does not itself enforce the threshold. The observable contract is `TraceEnabled(...)` followed by conditional emission. This distinction matters when building probes: calling `Trace()` directly can create output that normal host code would have filtered.

Raw evidence is preserved under `experiments/observatory/runs/EXP-OBS-002/`; the validated manifest is `experiments/observatory/manifests/EXP-OBS-002.json`.

## 25.6 -> 26.3 trace ABI drift
The trace vocabulary survives across the installed 25.6 and 26.3 runtimes, but category-volume access is not ABI-stable. Export archaeology shows `GetTraceVolume` / `SetTraceVolume` changing from `const std::string_view&` in 25.6 to `std::string_view` by value in 26.3.

Master-handler and master-volume exports retain their decorated form across the same two binaries. AEIG therefore treats the trace system as a versioned private ABI: semantic name continuity is weaker evidence than decorated-signature continuity.

The canonical L5 user-run probe resolves both category-volume ABIs dynamically, redirects the master trace handler to stderr only for the render window, then restores the original handler, master volume, category volumes and stderr handle.

Dataset: `datasets/ae-dvacore-trace-abi-lineage.csv`.
Finding: `F-ABI-014-dvacore-trace-string-view-abi-drift.md`.
