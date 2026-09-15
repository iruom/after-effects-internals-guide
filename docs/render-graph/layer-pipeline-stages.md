---
status: active
last_verified: 2026-09-16
evidence: AEGP_StreamSuite7 (26.5) + LayerRenderOptions + Canvas receipt lineage
---
# Layer Pipeline Stages

A layer reference and a rendered layer image are not the same object. AE 26.5 makes this explicit by giving `PF_Param_LAYER` references an independent **render stage** in `AEGP_StreamSuite7`.

A layer input therefore has at least two semantic coordinates:

`LayerInput = (source layer identity, render stage)`

and the stage determines *where in the source layer's pipeline* pixels are sampled.

## Public stage model in 26.5
`AEGP_LayerParamStage` exposes:
- `SOURCE = 0`: source pixels before masks/effects;
- `ONLY_MASKS = -2`: source plus masks, effects skipped;
- `ALL_EFFECTS = -1`: masks plus full effect stack;
- `1..N`: source rendered through effect index N, 1-based.

The source layer and stage can be changed independently, or atomically as one undo step.
## Cycle safety is topology-dependent
`AEGP_GetStreamInputStageCycleSafeLimit()` asks the host for the highest stage that can be sampled without introducing a render cycle **for the current project state**.

Adobe explicitly requires re-querying this limit when:
- effects are added/removed/reordered;
- the source layer changes;
- topology changes in a way that can alter dependency reachability.

`SOURCE` is always safe; deeper stages may not be.

This is strong public evidence that render-stage references participate in a dependency graph whose legality depends on current topology, not merely on parameter type.

## Historical stage surfaces
The same concept appears in older APIs under different forms:
- `AEGP_LayerRenderOptionsSuite1::AEGP_NewFromUpstreamOfEffect()` creates render options upstream of a chosen effect;
- Canvas receipts encode the number of effects considered rendered;
- `AEGP_GenerateRenderReceipt()` can synthesize a receipt as if the first N effects had been rendered;
- historical post-effect cache APIs expose another intermediate pipeline boundary.

The naming differs, but the semantic axis is stable: **layer identity and computational stage are separate**.
## Better internal abstraction
A more faithful render reference is:

`LayerInputRef(layer_id, comp_time, layer_time, stage, render_context, ROI/quality)`

rather than a bare `AEGP_LayerH` or `PF_Param_LAYER` value.

Different stage values can produce different pixels, bounds, dependency sets, receipts and cache identities even when the selected source layer is unchanged.

## Failure modes
- treating `PF_Param_LAYER` as if it already contains pixels;
- assuming “selected layer” always means final post-effect output;
- using a stale cycle-safe limit after an effect reorder;
- caching derived work by layer ID while ignoring stage;
- assuming effect index is a stable semantic identifier across reorder/edit operations;
- equating Canvas effect-prefix count with a universal RG node index.

## Experiment design
Construct a layer with three visually distinct effects and sample stages 0, masks-only, 1, 2, 3 and all-effects. Reorder effects without changing parameters, then change source layer and test the cycle-safe limit after each topology mutation.

Correlate stage changes with Canvas receipt status, output hashes and BEE/RG trace identity. This directly links the new 26.5 public stage model to AEIG's existing receipt/render-graph model.

## Unknown frontier
The exact mapping from public effect-prefix stage to internal BEE/RG node/materialization boundaries remains unproven. Multiple public stages could map to fused graph regions, and one stage could expand into several RG nodes.

Cross-links: `frame-checkout.md`, `render-context.md`, `render-graph-model.md`, `../state-model/receipt-taxonomy.md`, `../evaluation/dirty-invalidation.md`.