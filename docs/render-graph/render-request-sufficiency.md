---
status: active
last_verified: 2026-09-16
evidence: AEGP_RenderOptionsSuite4 + AEGP_RenderSuite4 sufficiency/timestamp/speculative-render contracts
---
# Render Request Sufficiency

A rendered frame is reusable only relative to a **render request contract**. AE exposes this directly through `AEGP_IsRenderedFrameSufficient(rendered_options, proposed_options)` rather than forcing plug-ins to guess cache-key equality.

## Render request is a structured semantic object
`AEGP_RenderOptionsSuite4` exposes request dimensions including render time, time step, field mode, world type/depth, independent X/Y downsample, ROI, matte mode, channel order, guide-layer inclusion and footage decode quality.

Time step is especially important because motion blur and temporal sampling can depend on it even when nominal render time is unchanged.

A useful model is:

`R = (item, time, time_step, field, world_type, downsample_xy, ROI, matte, channels, guide_layers, decode_quality, ...)`.

The ellipsis is deliberate: AEIG does not assume the public fields are the entire internal identity.

## Sufficiency is not equality
`AEGP_IsRenderedFrameSufficient(A,B)` asks whether pixels rendered under request `A` are still valid for proposed request `B`.

Define `S(A,B) -> bool`. There is no reason to assume `S(A,B) == S(B,A)`.

This matters for dimensions with natural containment. A full-frame render may or may not satisfy a smaller ROI request; a higher-quality decode may or may not satisfy a lower-quality request; full-resolution pixels may or may not satisfy a downsampled request without an explicit conversion step. Only experiment or public contract should decide.

## Request sufficiency, frame receipts and cache
`AEGP_RenderAndCheckoutFrame` returns a frame receipt, while `AEGP_GetReceiptGuid` exposes a GUID for a rendered frame. These objects are adjacent to request sufficiency but are not the same concept.

A cached result can be semantically reusable because `S(A,B)` is true even if request objects are not byte-identical. Conversely, matching item/time alone is insufficient when ROI, field, downsample, depth or decode semantics differ.

## Project timestamp is another axis
`AEGP_GetCurrentTimestamp()` advances when project state changes in a way that affects rendering. `AEGP_HasItemChangedSinceTimestamp()` checks whether an item's **video** changed over an interval; the Guide explicitly notes that this does not track audio.

Thus request sufficiency and project-state validity are separate questions:

1. are these two request contracts compatible?
2. has the underlying render-relevant project state changed since the cached result?

## Speculative rendering uses both request and freshness policy
`AEGP_IsItemWorthwhileToRender()` is intended to be used with project timestamps. Adobe recommends speculative renderers check it twice: before expensive external rendering and again after completion, before checking the result into AE's cache.

This exposes a first-class **obsolescence window**: a request can be worthwhile when launched and stale by the time work finishes.

## Reconstruction experiment
For each public request dimension, construct A/B pairs differing in exactly one field. Test both `S(A,B)` and `S(B,A)`, then repeat pairwise combinations after single-axis behavior is understood.

Record request fields, sufficiency result, receipt GUID, rendered region, output hash and whether AE reuses or rerenders. This can reveal equivalence classes, strict containment edges and dimensions that require exact equality.

High-value axes: ROI containment, X/Y downsample independently, field mode, world type/depth, guide-layer inclusion, decode quality and time-step with motion blur enabled/disabled.

## Failure modes
- cache only by `(item,time)` and ignore request semantics;
- assume sufficiency is symmetric;
- assume larger ROI/full resolution always satisfies smaller/lower-resolution requests;
- reuse a video timestamp test for audio validity even though the public API excludes audio;
- launch speculative work once and check it in after the project changed;
- confuse receipt GUID equality with the sufficiency predicate.

## Unknown frontier
Still unresolved: exact internal predicate used by `AEGP_IsRenderedFrameSufficient`, relationship between public RenderOptions and BEE/RG request identity, which request dimensions participate directly in Render GUID construction, and whether sufficiency forms a stable partial order across versions.

Related: `docs/render-graph/render-context.md`, `docs/render-graph/render-tasks.md`, `docs/state-model/object-identity.md`, `docs/temporal-system/temporal-dependencies.md`.
