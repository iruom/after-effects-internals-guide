---
status: active
last_verified: 2026-09-14
---
# Render Request Architecture History

AE's request-oriented render architecture predates MFR and the CC 2015 threading redesign by many years. Legacy suite headers preserve a useful chronology.

## AE 5.5.1: structured item requests and directional sufficiency already exist
`AEGP_RenderOptionsSuite1` and `AEGP_RenderSuite1` were frozen in AE 5.5.1. RenderOptions already carried time, frame time-step, field handling, world/depth type, independent X/Y downsample, ROI and matte mode.

Render Suite1 already returned Frame Receipts, exposed the read-only receipt world and rendered region, and—most importantly—already provided `AEGP_IsRenderedFrameSufficient(rendered_options, proposed_options)`.

Therefore the concept "an existing render may satisfy a different proposed request" is not a recent cache optimization. It is part of AE's old architectural substrate.
## AE 6.0–7.0: cacheable stage proofs appear in Canvas
Canvas Suite4, frozen in AE 6.0, adds Render Receipts specifically so an Artisan can skip re-rendering a cached layer texture. AE 7.0 then adds the number of effects rendered to receipt validation and permits generating a receipt for the first N effects.

This is a distinct mechanism from Frame Receipt checkout and demonstrates explicit intermediate/stage reuse.

## AE 6.5: generation validation and speculative cache admission
Render Suite2 adds a project render timestamp, interval-specific item-change queries, a "worthwhile to render" test, and external rendered-frame check-in.

The speculative contract requires validation before dispatch and again after expensive work completes. Check-in includes an approximate machine-local render cost in 60 Hz ticks as well as RenderOptions and generation timestamp.

This exposes four separable concerns unusually early: request meaning, generation validity, computation usefulness, and cache admission.
## AE 11.0: frame identity becomes explicitly observable
Render Suite3 adds `AEGP_GetReceiptGuid`, exposing a GUID associated with a checked-out frame receipt.

## AE 13.0–13.5: stage semantics migrate into request construction
13.0 Render Suite4 used `render_plain_layer_frameB` directly on the execution call. Adobe's 13.5 header calls this boolean "confusing" and "not the design we want going forward" and removes it from Render Suite5.

In parallel, Layer Render Options represent stage intent when the request is constructed: full layer, upstream of a named effect, and—by Suite2 in 13.5—downstream including the effect output.

This is a strong architectural migration from imperative execution flags toward semantic request objects.

## Interpretation
The CC 2015 rearchitecture should not be described as inventing demand/request rendering. It appears instead to have modernized threading, project isolation and async execution around much older request, receipt, sufficiency and cache-admission concepts.

## Source
Local AE 25.6 SDK legacy/current AEGP headers.
