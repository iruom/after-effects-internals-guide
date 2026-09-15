---
status: active
last_verified: 2026-09-16
evidence: current Adobe Artisan contract + CanvasSuite8 + AEIG receipt/render-context experiments
---
# Artisan Render Context and Interactive Policy

An Artisan is not a generic effect renderer. The public contract lets a plug-in replace After Effects' 3D rendering for a composition while AE continues to own project state, layer/effect evaluation, render-context construction and all 2D-layer rendering around that boundary.

Adobe explicitly describes the API as large and specialized: there is one selected Artisan per composition, and the renderer asks AE for composition elements through host suites rather than owning the project model itself.

## Standard vs interactive Artisan
A standard Artisan renders the composition's 3D environment. An interactive Artisan has a different policy: it may handle all layers for onscreen display, but it is not used for final output; final rendering falls through to the normal/default renderer path.

That distinction means "which renderer produced what I see in the Comp panel" and "which renderer produced the final frame" are separate questions. Bugs that appear only in interactive view cannot automatically be attributed to the final render path.

## Host-owned render context
CanvasSuite8 exposes a host-created context containing composition time, ROI, downsample state, destination/world information, ordered render-layer contexts, 2D/3D binning, transforms, camera/light access and interactive display policy.

The useful mental model is:

`project/effect evaluation -> host render-context expansion -> layer contexts/bins -> Artisan 3D work -> AE 2D/composite/output`

An Artisan therefore sees an already-interpreted render topology, not a raw copy of the timeline tree.

## Layer materialization is host policy
`AEGP_ArtisanMustRenderAsLayer()` asks AE whether a layer context must be materialized through a layer-render path instead of a texture-style path. This is an important boundary: legal materialization cannot be inferred from layer type alone, because effects, masks, collapse/continuously-rasterize behavior, track mattes, 2D/3D binning and host renderer policy can force different paths.

Do not build a renderer assuming `timeline layer == one texture == one render node`. Canvas render-layer contexts and AEIG's RG evidence both show richer one-to-many/many-to-one relationships.

## Time, transforms and motion blur
The render context owns the time mapping used by the renderer. `AEGP_MapCompToLayerTime()` applies layer time-remapping semantics; `AEGP_GetCompShutterTime()` exposes shutter start/duration. Camera, light, geometry and layer transforms must therefore be evaluated at render-context time, not inferred from UI timeline coordinates or cached once per layer.

Transform access also distinguishes render-layer/world mappings from project-layer transform properties. Collapsed geometry and renderer-specific context can change the mapping even when the visible project hierarchy is unchanged.

## Interactive display state
Interactive Artisan queries include viewport scale/origin/rect, checkerboard state, display channel, exposure, color-transform identity, interactive output buffers and cached interactive buffers. These are renderer-facing inputs, not merely decorations painted after a final-quality frame.

That is why viewer parity tests should separate:
- scene/render state;
- interactive presentation state;
- final-output renderer selection;
- display color/exposure/channel state.

A screenshot mismatch can come from any of these layers.

## Effects and renderer communication
Adobe's Artisan contract allows effects written to cooperate with an Artisan, but the direction matters: effects do not simply seize renderer control. Several suites become meaningful only once AE has applied effects and established a render context. Treat renderer/effect communication as host-mediated context, not an arbitrary back-channel between two plug-ins.

## Failure and compatibility traps
Typical renderer mistakes include caching project-layer pointers beyond their valid lifetime, using project time instead of mapped render time, assuming every layer can be sampled as one texture, ignoring ROI/downsample, using interactive viewport state in final output, retaining context-owned handles, or treating a receipt as proof that a full pixel world is materialized.

Renderer bugs can also masquerade as effect bugs because the Artisan receives already-evaluated state. Always localize the boundary: project state -> effect result -> layer context -> renderer materialization -> final composite.

## Investigation strategy
For deterministic fixtures, vary one dimension at a time: 2D/3D, collapse transformations, track matte, effect-prefix count, time remap, shutter interval, ROI, downsample and interactive/final mode. Record render-layer context ordering, bin type, receipt status, trace window and output hash.

AEIG's canonical Receipt Artisan deliberately uses this boundary as an observation surface; it does not imply that the research probe reproduces AE's production 3D renderer.

## Version and unknown frontier
The public Artisan model is old and stable enough to expose important architecture, but it is not a specification of modern internal renderer implementations such as Advanced 3D. Private RG/BEE node topology, materialization heuristics and GPU scheduling remain separate evidence domains.

Sources: Adobe C++ SDK Guide `Artisans` / `Artisan Data Types`, distributed CanvasSuite8 headers, `docs/render-graph/render-graph-model.md`, `docs/state-model/receipt-taxonomy.md`, and the AEIG Observatory receipt experiments.
