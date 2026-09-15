---
status: active
last_verified: 2026-09-14
---
# 3D System

Separate historical Artisan contracts from modern Advanced 3D implementation, but use the old contract as evidence for long-lived render boundaries.

## Explicit 2D/3D partition
`AEGP_CanvasSuite8` exposes multiple render bins classified as 2D or 3D. This is direct evidence that the host contract can partition a composition into renderer-specific segments.

## Transform surfaces
Canvas exposes both layer-to-world transforms and `AEGP_GetRenderLayerToWorldXform2D3D(... only_2dB ...)`, indicating that a layer's 2D contribution can be queried separately from the full world transform path.

## Collapse interaction
With collapsed geometrics, a render-layer context can belong to an inner layer while `AEGP_GetTopLayerFromLayerContext` points to the containing root-comp layer. This makes 3D/collapse a render-graph identity problem, not merely a project hierarchy feature.

## Modern bridge evidence
Local crash stacks show Advanced3D/AEGPDriver paths returning through BEE/RG. Module inventory adds RendererGPU, GPUFoundation, GPUKernels and USD/Hydra libraries in modern generations.

## Open questions
Determine exact materialization barriers between adjacent 2D/3D bins, how cameras/lights influence Render GUIDs, whether modern Advanced 3D preserves historical bin semantics, and how adaptive-quality/tile decisions interact with cache and RG nodes.
## Modern confirmation of the bin boundary
Adobe's 26.2 fixed-issue notes explicitly describe Essential Property values being shared across precomp instances in the same `3D bin` when Advanced 3D and Collapse Transformations were combined.

This wording is important because it connects the historical Canvas `2D/3D bin` contract to a current Advanced 3D failure domain. The exact implementation lineage is not proven, but the concept is clearly not only an obsolete Artisan term.

The failure is consistent with per-instance state being insufficiently isolated inside a bin-scoped render context or identity key. Treat that as a hypothesis, not the documented root cause.

## Ordering and topology clues
26.5 also fixed coplanar Advanced 3D layers so their render order matches Classic 3D, plus crashes involving collapsed nested comps and Draft 3D. These are useful probes for bin partitioning, graph rewrite and ordering/barrier rules.

## Modern AE3D resource layer
Installed `BEE.dll` exposes a dedicated `BEE_AE3D_*` resource layer beneath final frame rendering: model, mesh, texture, model-info, overridden-model, and ASM material resources each have GUID-keyed cache/lookup/release surfaces and `AE3D::CacheFlags`.

This is a stronger model than treating Advanced 3D as one monolithic renderer. Scene evaluation can materialize reusable intermediate resources independently of the final composition frame.

`Advanced3D.aex` directly depends on `PF.dll`, `BEE.dll`, and `PR.dll`, and imports BEE Artisan render-options/capsule helpers plus `PR_ExtractRenderRefcon`. This connects the modern renderer to the public Artisan render-context lineage while leaving resource ownership in BEE.

Working model: `TDB/BEE scene streams -> AE3D resource cache -> renderer/Artisan context -> layer/texture result -> BEE/RG composition`.

Reproducible inventory: `datasets/ae-2025-3d-runtime-surface.csv`. Finding: `F-3D-003`.
