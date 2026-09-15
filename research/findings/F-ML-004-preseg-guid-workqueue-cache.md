---
status: confirmed-local-symbols
last_verified: 2026-09-15
---
# F-ML-004 — Pre-segmentation is keyed by AE render state and scheduled asynchronously

AE 2025 `AfterFXLib.dll` exposes these signatures/identifiers in `ObjectSelectionTool`:
- `GetPreSegGuid(BEE_AVLayer*, T_Time, BEE_LayerRenderOptions*)`
- `PreSegResultExists(Guid, ...)`
- `GetPreSegResult(Guid)` / `SetPreSegResult(Guid, ...)`
- `SetPreSegResultMRU(Guid)`
- `FramePreSeg::Get/SetCheckoutLayerFrameWorkQueueID()`
- `FramePreSeg::Get/SetComputeFuture(Future<PreSegmentationResult>)`

## Consequence
The pre-segmentation analysis is not keyed only by source pixels or frame number. Its identity construction explicitly receives AE's layer object, time, and layer-render options, then uses a GUID to index reusable asynchronous analysis state.
## Independent local corroboration
Retained AE 26.0 and 26.3 Debug Database.txt files expose DVACompute.ShouldUseObjectSelectionAsync = true. AE 26.3 Trace Database.txt separately exposes RotoBrush4 and RotobrushSpanView. These artifacts independently support the model that object-selection/pre-segmentation participates in host-managed asynchronous work, while not proving that every later Object Matte phase follows the same path.
