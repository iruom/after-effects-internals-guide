---
status: active
last_verified: 2026-09-15
---
# Bounds Cache

Bounds are a separate planning product from rendered pixels. AEIG therefore does not model a bounds cache as merely a smaller pixel cache.

## Confirmed surfaces
- Retained Debug Database vocabulary includes `AE.VectorBoundsCache`.
- SmartFX PreRender can answer dependency/bounds questions without a matching Render call.
- Installed AE exposes `BEE_VectorArt::GetBounds(... RenderExtentMode)` independently from `BEE_VectorLayer::Rasterize2DGraph(...)`.
- RG exposes an explicit pre-render traversal before graph pixel execution.

These surfaces support a pipeline in which geometry/extent information can be materialized and reused before final image materialization.

## Working model
`stream/property state -> evaluated geometry/vector state -> extent/bounds -> request pruning/ROI -> pixel graph`.

A valid pixel result implies some spatial coverage, but the reverse is not true: valid bounds do not imply valid pixels. Bounds identity may also omit state that only changes color while including transforms, path geometry, stroke expansion, blur/effect extents and render-context topology.

## Important boundary
The exact key of `AE.VectorBoundsCache` is unknown. Current evidence does **not** prove whether it is keyed directly by stream GUID, BEE render GUID, RG node identity, time, resolution, renderer, or a combination.

Collapsed transformations are a high-risk case because project parentage and effective render context can diverge.

## Discriminating experiment
Hold pixels semantically different while preserving geometry, then hold geometry different while preserving appearance. Compare bounds/ROI traces, RG pre-render activity and pixel-cache reuse. Repeat across time, downsample and Collapse Transformations.

Related: `F-RG-003-prerender-graph-phase`, `F-GUID-003-collapsed-context-cache-key`, `docs/image-pipeline/roi-bounds.md`.

## Version and failure boundary
Bounds/extent semantics have existed across classic Effect API, SmartFX and modern RG/vector paths, but the internal bounds cache observed in current debug/runtime evidence is version-specific. Do not assume historical hosts used the same key or invalidation policy.

Typical failure classes are under-expansion (clipped blur/style/DOF output), stale bounds after transform/operator mutation, over-expansion that destroys ROI efficiency, and context errors under Collapse Transformations or alternate render stages.

A bounds hit can still be wrong for current pixels if color/effect state changed without affecting geometry; conversely a pixel cache miss need not invalidate reusable geometry/bounds.

## Practical probe matrix
Vary geometry-only state, appearance-only state, transform, time, downsample and renderer independently. Record requested/result rects, SmartFX PreRender callbacks, vector bounds traces and final pixel hashes.

The desired distinction is whether bounds identity tracks only spatial coverage while pixel identity tracks the full render-relevant state.

Related: `docs/image-pipeline/roi-bounds.md`, `docs/render-graph/render-nodes.md`, `docs/render-graph/render-context.md`, `F-RG-003-prerender-graph-phase.md`, `F-GUID-003-collapsed-context-cache-key.md`.
