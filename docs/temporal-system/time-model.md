---
status: active
last_verified: 2026-09-16
evidence: AEGP Layer/Canvas time contracts + render timestamp/state APIs
---
# Time Model

After Effects does not have one universal floating-point `t`. Public APIs expose multiple temporal coordinate systems and explicit mappings between them.

At minimum distinguish:
- composition time;
- layer time;
- source/footage time;
- time-remapped layer time;
- render request time + time step;
- transform/query time;
- view time;
- shutter interval/sample time;
- expression evaluation time;
- audio/sample-domain time.

Converting everything immediately to `double seconds` destroys exact rational relationships and can hide frame-boundary errors.
## Layer time and composition time are distinct
`AEGP_GetLayerCurrentTime`, in-point and duration APIs explicitly accept a layer-vs-comp time mode. Adobe notes that the two spaces differ when a layer starts away from comp time 0 or is stretched away from 100%.

For stretched layers, the SDK Guide even gives the offset relationship needed when reconstructing layer timing:

`offset = compIn - stretch * layerIn`

Treat this as evidence that time-space conversion is first-class state, not a display convenience.

## Old and new comp→layer mappings are not equivalent
`AEGP_ConvertCompToLayerTime()` maps composition time to layer/source-relative time, but the newer Canvas `AEGP_MapCompToLayerTime()` was added specifically to handle **time remapping with collapsed or nested compositions**.

Therefore one generic `comp_to_layer(t)` helper is insufficient unless it also carries render context/topology semantics.

A better model is:

`layer_time = Map(comp_time, layer offset/stretch, time remap, nesting/collapse, render context)`
## Current UI time is not render time
`AEGP_GetLayerCurrentTime()` is documented as the layer's current UI/project time and is explicitly **not updated during rendering**.

Render code should instead use selector/render-context time (`in_data->current_time`, render options, Canvas render time, etc.) appropriate to that API.

Confusing these domains can make an effect appear correct interactively and wrong in aerender/MFR/background rendering.

## View time vs transform time
Artisan query APIs distinguish transform time from view time. Transform time participates in shutter/scene evaluation; view time participates in view-dependent transforms.

That separation matters for motion blur, cameras and interactive renderers: the viewport can ask for geometry evaluated at a transform time while using another view-time coordinate.

## Time and invalidation
Temporal validity APIs also carry ranges, not just scalar time. Project timestamps plus `HasItemChangedSinceTimestamp(start,duration)` and wide-time effect dependencies demonstrate that cache invalidation can be localized to intervals.

The identity question is therefore often:

`what state was sampled over what temporal footprint?`

not merely `what frame number is this?`.
## Failure modes
- using UI current time inside render callbacks;
- converting rational `A_Time` to float too early;
- assuming layer time equals comp time after stretch/offset;
- using the older comp→layer mapping where collapse/time-remap semantics require render context;
- treating motion-blur sample time as the nominal frame time;
- caching temporal results by frame index while ignoring shutter/time-step/dependency span;
- assuming expression `valueAtTime()` creates the same dependency footprint as ordinary current-time evaluation.

## Probe matrix
Build a minimal comp with nonzero in-point, stretch, time remap, nested comp and Collapse Transformations. Query/record comp time, layer time, mapped layer time, source sample identity and output at rational times around frame boundaries.

Then add motion blur and a temporal effect to expose multi-time checkouts. Repeat under MFR and aerender to separate UI-current-time artifacts from true request time.

## Unknown frontier
The exact ordering of source interpretation, stretch, time-remap, nested-comp mapping, expression evaluation and frame blending remains partly subsystem-specific. AEIG will not force them into one universal equation until experiments connect those boundaries.

Cross-links: `motion-blur.md`, `../render-graph/render-context.md`, `../render-graph/frame-checkout.md`, `../evaluation/dirty-invalidation.md`, `../expression-engine/architecture.md`.