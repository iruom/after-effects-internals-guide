---
status: active
last_verified: 2026-09-15
---
# Object Selection / Pre-Segmentation Pipeline

AE 25.x local binaries expose a pre-public object-selection subsystem that bridges AE project/render state to the shared DVACompute ML/tracking layer.

## AE-side integration surface
`AfterFXLib.dll` contains an `ObjectSelectionTool` with symbols for:
- pre-segmentation and marquee segmentation,
- object-ID lookup from cursor position,
- interactive boundary points,
- mask refinement,
- overlay-frame updates,
- model registration,
- layer-frame checkout completion,
- pre-segmentation GUID construction and result lookup,
- WorkQueue request IDs and asynchronous futures.

The same local region contains `ObjectSelectPreSeg`, `RegisterObjectSelectionModels`, `RotoBrush4`, `ObjectSelection`, and an AE-localized pre-segmentation failure string.
## Reconstructed request path
Direct symbol signatures strongly support a path like:

`BEE_AVLayer + T_Time + BEE_LayerRenderOptions`
→ `ObjectSelectionTool::GetPreSegGuid(...)`
→ GUID-keyed pre-segmentation lookup
→ layer-frame checkout / BEE WorkQueue task
→ `Future<PreSegmentationResult>`
→ DVACompute `IPreSegmentationWrapper`
→ result stored by GUID and promoted in an MRU structure
→ selection/refinement/UI consumption.

This is unusually strong evidence because the render-state inputs, cache identity, async scheduler handle, future, and result-cache functions are all exposed by symbol names in the same implementation boundary.
## DVACompute side
`AeCompute.dll` supplies the higher-level compute interfaces used by the AE tool:
- `ObjectSelectionWrapper` with detection from mask or boundary,
- `PreSegmentationWrapper::RunPreSegmentation` and `RefineMask`,
- `SmartMaskingUtils`,
- `DVAMLInferenceEngine`,
- `VectorSelectionTracker`,
- FastMask and optical-flow tracking components.

The implementation uses DVA async Future/Promise machinery. Script-object wrappers for Object Selection and Pre-Segmentation are also present, showing that this compute substrate was designed to be callable through a higher-level Adobe scripting/runtime layer, not only through the AE tool UI.

## Evidence boundary
Do not equate the AE 25.x internal `ObjectSelectionTool` or `RotoBrush4` label directly with the public AE 26.x Object Matte feature. Treat them as predecessor/shared-substrate evidence until a 26.x binary/runtime trace connects public Object Matte actions to these exact classes and model keys.
## Public Object Matte state machine in AE 26.5
The public Object Matte workflow adds a user-visible state machine above segmentation/tracking compute: initial object selection, temporal propagation, manual correction/refinement, then **Freeze** to lock the matte for downstream compositing.

AE 26.5 also changes propagated-result residency: propagated frames can persist on disk and survive project close/reopen even before Freeze. Earlier public behavior kept propagated frames in memory, so this is a real persistence/residency transition rather than a UI-only feature.

Keep three concepts separate:
- authored selection/refinement state and keyframes;
- propagated analysis results that may be RAM/disk resident;
- frozen/committed matte state consumed by compositing.

## Shared-technology evidence without class identity claims
Adobe states that Object Matte uses the same AI technology as Premiere's Object Mask workflow. That supports a shared model/inference substrate hypothesis, but it does not prove AE 26.5 calls the exact AE 25.x `ObjectSelectionTool`, `RotoBrush4`, or every DVACompute wrapper observed locally.

The 25.x local symbols remain valuable predecessor evidence because they expose the architecture shape: render-state-derived pre-segmentation GUID, asynchronous WorkQueue/Future, ML model wrapper, result lookup and refinement. A 26.5 runtime trace is still required to promote exact implementation continuity.

## Cache and invalidation questions
Disk persistence makes model/runtime version, source-content identity, selection/refinement state, propagation range and analysis options important cache-key candidates. A persistent analysis result must not silently survive a source or semantic selection change that invalidates it.

Green timeline cache markers are therefore residency/availability evidence, not proof that every stored result remains semantically valid under arbitrary project edits.

## Failure and regression evidence
Recent fixed issues show Object Matte crossing multiple architectural boundaries: aerender/headless rendering, application launch/model initialization and Undo/project-stream mutation. These symptoms are high-value leads for integration boundaries but are not root-cause proof for one private class.

## Controlled experiments
Propagate a short deterministic clip, then mutate one axis at a time: source pixels, layer transform, Object Matte selection keyframe, refinement option, effect ordering, project reopen, host restart and model/runtime version. Record disk artifacts, timeline cache markings, BEE/render GUID evidence and whether reuse occurs.

Repeat with Freeze before/after mutation to determine whether frozen state changes the persistence/invalidation contract.

## Unknown frontier
Unresolved: exact 26.5 binary classes behind Object Matte; cache file/key format; how model version enters identity; whether propagation result chunks are frame-, interval- or segment-addressed; relation between Object Matte disk cache and global Disk Cache; exact headless support boundary after fixed releases.

Related: `docs/ai-analysis/overview.md`, `docs/cache-system/state-identity.md`, `F-AI-001-object-matte-headless-boundary.md`, `F-CACHE-012-object-matte-analysis-disk-persistence.md`, `F-ML-004-preseg-guid-workqueue-cache.md`.
