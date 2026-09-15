---
status: active
last_verified: 2026-09-16
evidence: CanvasSuite/Artisan distributed contract + local BEE/RG runtime evidence
---
# Render Context: Request-Scoped Topology, Time, Geometry and Cache State

`PR_RenderContextH` is a render-side context object passed to Artisans. It is not equivalent to an `AEGP_CompH`, a project layer list or a framebuffer.

The public Canvas/Artisan contract makes this concrete: the context exposes the composition being rendered, an ordered set of render-layer contexts, render time/time-step, destination buffer, ROI, field mode, downsample factor, layer transforms/bounds/opacity/activity, texture/layer materialization, track-matte context, render receipts and 2D/3D bins.

## Context expands the project tree
`AEGP_GetNumLayersToRender()` + `AEGP_GetNthLayerContextToRender()` enumerate **render-layer contexts**, not simply `comp.numLayers`.

A render-layer context can map to:
- an ordinary layer;
- a layer plus sublayer;
- a different root-comp top layer under collapsed geometrics;
- a track-matte relationship exposed through a separate context.
This is direct public evidence that render topology is a context-dependent expansion/rewrite of the editable project graph.

## Geometry is evaluated in context
Canvas APIs query layer-to-world transforms, rendered bounds, opacity and active state **at a specified composition time within a render context**.

Therefore:

`layer transform property != final render transform`

because collapse, parent/precomp context, renderer partitioning, time remap and context-specific state can alter the effective mapping.

## Time is request state
`AEGP_GetCompRenderTime()` provides the current render time/time-step. Additional Canvas APIs expose shutter timing and comp-to-layer time mapping.

A renderer should consume context time rather than reconstructing it from project-layer assumptions.

## Materialization is host policy
The context can request textures or rendered layers, and `AEGP_ArtisanMustRenderAsLayer()` lets the host determine when layer materialization is required.

This is important for optimization: whether an intermediate image exists is not solely a plug-in decision.
## Receipts bind validity to context
`AEGP_RenderTextureWithReceipt()` and `AEGP_RenderLayerPlusWithReceipt()` return `AEGP_RenderReceiptH`; `AEGP_CheckRenderReceipt()` validates an old receipt against a **current render context + current layer context + effect-prefix/geometry policy**.

This makes receipt validity relational rather than intrinsic to the receipt object.

A useful abstraction is:

`Validity = V(old receipt, current render context, current layer context, requested effect prefix, geometry check)`

The canonical `EXP-CACHE-002` operator experiment exists to test exactly this prefix/context behavior.

## Render bins
CanvasSuite exposes explicit render bins and bin type (`2D` / `3D`). Do not assume a bin is one RG subgraph; it is public evidence of render partitioning, not proof of internal node ownership.

## Threading and progress caveat
The retained Artisan contract explicitly warns that one progress-reporting path is not thread-safe on macOS and should only be used on thread ID 0. This is a concrete example of why render-context APIs must still be treated as thread-qualified host calls.

## Runtime relation
Local evidence places `U_RenderContext`, BEE render options/state, BEE Render GUID formation and RG graph/cache execution adjacent to this public context model. The exact object conversion path is not yet proven.

## Unknown frontier
- lifetime/ownership of `PR_RenderContextH` outside callback scope;
- exact mapping to `U_RenderContext` and BEE render state;
- whether bins correspond to stable RG partitions;
- which context fields mix into BEE/RG identity;
- collapse/matte/adjustment-layer rewrite rules at context-construction time.

Cross-links: `render-graph-model.md`, `render-tasks.md`, `frame-checkout.md`, `../host-integration/artisans/render-context-and-interactive-policy.md`, `../cache-system/state-identity.md`.