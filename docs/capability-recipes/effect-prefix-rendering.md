---
status: active
last_verified: 2026-09-16
evidence: AEGP_StreamSuite7 render-stage contract + LayerRenderOptions + Canvas receipt prefix semantics + canonical EXP-CACHE-002 design
---
# Recipe: Render a Layer at a Specific Effect Stage

## Goal
Obtain a layer at a controlled point in its render pipeline: raw source, source with masks, through effect `N`, or through the entire effect stack — without treating the final layer output as the only addressable image.

This is a **render-stage identity** problem, not merely a layer-selection problem.

## Current public route: StreamSuite7 (AE 26.5)
`AEGP_StreamSuite7` adds independent render-stage state to a `PF_Param_LAYER` stream. The layer parameter now carries two independent values:

- source layer identity (`AEGP_StreamValue2::layer_id`);
- `AEGP_LayerParamStage` describing where that source is sampled.

Stage values are:
- `SOURCE = 0`: source pixels before masks/effects;
- `ONLY_MASKS = -2`: masks applied, effects skipped;
- `ALL_EFFECTS = -1`: complete effect stack;
- positive `1..N`: render through effect index `N`, 1-based.

This is one of the clearest public confirmations that **Layer != Layer Render Stage**.

## Atomic layer + stage mutation
`AEGP_SetStreamLayerParamAndStageValue` can set source layer and stage together as one undo step. Use the atomic form when changing both; two independent UI/project edits can otherwise expose an intermediate semantic state.

Any returned `AEGP_StreamValue2` still follows normal ownership/disposal rules; stage values themselves do not require disposal.

## Cycle-safe upper bound is dynamic
`AEGP_GetStreamInputStageCycleSafeLimit` returns the highest stage that will not introduce a render cycle for the current project state. `SOURCE` is always safe.

The Guide explicitly requires re-querying before use because the limit can change when:
- effects are added;
- effects are removed;
- effects are reordered;
- source layer changes.

Do **not** cache the safe maximum as a permanent property of the effect instance.

This implies that legality is a function of current dependency topology, not merely `N <= number_of_effects`.

## Older public route: LayerRenderOptions
Before StreamSuite7, AEGP Layer Render Options provided a different route. Requests can be built from a layer, upstream of a chosen effect, or downstream including that effect, then passed to layer-frame rendering.

This surface remains important for compatibility and for understanding that effect-stage rendering existed long before the stage became an independently stored layer-parameter value.

## Canvas receipt prefix semantics
The Artisan Canvas API also exposes effect-prefix semantics through `AEGP_NumEffectsToRenderType`. `AEGP_GenerateRenderReceipt` can generate a receipt as if the first `num_effectsS` effects have been rendered, and `AEGP_CheckRenderReceipt` tests validity for the requested prefix/context.

This supports a long-lived architectural model:

`layer source -> masks -> effect prefix 1..N -> final layer output`.

But **do not equate integer encodings across APIs**.

Keep separate:
- StreamSuite7 stage value `N`;
- LayerRenderOptions chosen effect relation;
- Canvas `num_effectsS` count/type;
- internal BEE/RG fields.

The semantics overlap; ABI and numeric representation are not proven identical.

## Receipt completeness model
The canonical `EXP-CACHE-002` experiment treats generated and requested effect prefixes as a partial-result relation. The locked prospective model predicts that a receipt generated for prefix `k` is complete for requested prefix `n` when `k >= n`, and incomplete when `k < n`.

That experiment is intentionally kept separate from the public API description until runtime observation confirms or refutes the exact status behavior.

## Failure modes
- use `ALL_EFFECTS` when the desired algorithm needs pre-effect source -> recursive/self-influenced result;
- cache cycle-safe stage after topology edit -> newly illegal dependency cycle;
- use effect index as persistent identity -> wrong stage after reorder;
- change layer then stage in two separate edits -> intermediate inconsistent state/undo history;
- use synchronous non-render-time checkout for passive custom UI -> UI stalls; prefer async where appropriate;
- assume masks are equivalent to stage 0 -> wrong: `ONLY_MASKS` is distinct from raw source.

## Practical selection strategy
For AE 26.5+:
1. acquire the `PF_Param_LAYER` stream;
2. resolve/set source layer;
3. query cycle-safe limit immediately before selecting a positive stage;
4. set layer+stage atomically if both change;
5. treat topology changes as invalidating cached stage assumptions.

For earlier hosts, construct `AEGP_LayerRenderOptionsH` at the required upstream/downstream effect position and use the corresponding Render Suite path.

## Internal correlation — not a supported shortcut
BEE runtime symbols expose layer render options and effect-inclusion decisions, while RG/receipt evidence exposes stage-sensitive cache validity. These strengthen the internal model but do not authorize direct calls or memory mutation of private BEE structures.

## Unknown frontier
Still unresolved:
- exact mapping from StreamSuite7 stage values to internal RG node boundaries;
- whether masks/effect prefixes correspond to reusable stable subgraphs or request-time planning only;
- how track mattes, adjustment layers and Collapse Transformations alter stage topology;
- current relation between stage-specific Render GUIDs and Canvas receipts.

Related: `F-EVAL-002`, `F-EVAL-003`, `docs/render-graph/layer-pipeline-stages.md`, `docs/render-graph/frame-checkout.md`, `docs/state-model/streams-properties.md`.
