---
status: active
last_verified: 2026-09-15
---
# Layer Input Stage as a Render-Graph Address

AE 26.5 AEGP_StreamSuite7 exposes the render stage of a PF_Param_LAYER stream independently from the selected source layer. This makes explicit a distinction that older APIs, layer-param UI, Canvas receipts, and layer-render options had already implied: selecting a layer does not fully specify which image state is requested.

## Public stage domain
AEGP_LayerParamStage_SOURCE = 0 requests source pixels before masks/effects. ONLY_MASKS = -2 requests masks applied but effects skipped. ALL_EFFECTS = -1 requests masks plus the full effect stack. Positive values 1..N request the source layer through effect index N.

Conceptually the input address is therefore at least (source layer, render stage), and at evaluation time must additionally be combined with time, render context/options, resolution/ROI and project generation.

## Cycle safety is dynamic
AEGP_GetStreamInputStageCycleSafeLimit() returns the highest stage that does not introduce a render cycle in the current project state. Adobe explicitly requires re-querying because the limit can change when effects are added, removed, reordered, or when the source layer changes. Source stage 0 is always safe.

This is direct public evidence that effect-stack stage references participate in dependency-cycle analysis. The dependency graph cannot be modeled only at layer granularity.

## Relationship to older surfaces
The layer-param UI has exposed Source / Masks / Effects & Masks since CC 2017.1. Canvas receipts can represent the first N effects, and LayerRenderOptions can request upstream/downstream states around an effect. StreamSuite7 unifies the same underlying concept into an independently addressable property value.

## Internal model
Treat a layer input as a graph address rather than a pointer: LayerInputAddress = LayerIdentity × Stage × Time × RenderContext. Stage is not merely display metadata; it selects a different upstream subgraph/materialization point.

## Developer implications
- Do not cache only layer_id for a layer parameter; stage changes alter render semantics without changing the source layer.
- Do not assume effect index is a stable semantic identity across effect insertion/reordering. Persist the host-supported stage representation and revalidate cycle safety after topology edits.
- An input-stage mutation is render-relevant state and must participate in cache/dependency identity.
- A host emulator that always returns the fully rendered layer for PF_Param_LAYER hides real dependency semantics and can create false success.

## Experiments
Create A→B layer dependencies and sweep the selected stage from source through each effect prefix. Record cycle-safe limits while inserting, removing and reordering effects. Compare Render GUID/receipt/cache invalidation for stage-only changes. Build deliberate near-cycles to determine whether cycle rejection occurs at set-time, evaluation-time, or both.

## CompNodeAE generalization
Represent references to computational nodes as (node identity, output stage/port, semantic view) rather than only node IDs. Make cycle safety a graph query over the exact addressed stage. This allows intermediate-stage reuse without pretending that a node has only one image output state.

## Stage identity and cycle analysis are distinct
A stage value selects what upstream materialization is requested; `GetStreamInputStageCycleSafeLimit()` answers whether that selection is currently legal. Do not encode "legal now" into persistent identity as if it were immutable. Topology can change while the authored stage value remains the same.

The atomic layer+stage setter is also semantically important: changing source and stage together as one undo step prevents consumers from observing a transient pair that was never intended as a stable project state.

## Failure modes
- persist positive effect index then reorder effects -> stage now names different computation;
- cache cycle-safe limit across topology mutation -> accept a dependency that has become cyclic;
- treat `ONLY_MASKS` as raw source -> wrong pixels/dependency graph;
- emulate every layer parameter as `ALL_EFFECTS` -> false compatibility while hiding source/mask/prefix semantics;
- use project-layer parentage to infer effective render context under Collapse Transformations -> wrong upstream state.

## Receipt/identity experiment
For a fixed source layer, sweep SOURCE, ONLY_MASKS, each positive effect prefix and ALL_EFFECTS while changing no other project state. Capture output hashes, BEE/TDB Render GUID categories and Canvas receipt behavior. Then reorder two effects without changing their parameter values and repeat.

This discriminates whether identity follows numeric stage position, effect semantic identity, realized upstream graph, or some combination.

## Version boundary
StreamSuite7 is a new public exposure in AE 26.5. Older hosts still support related effect-prefix requests through LayerRenderOptions/Canvas surfaces, but code must negotiate capability rather than assuming the stored layer-param stage exists.

## Unknown frontier
Unresolved: exact persistence encoding of stage state in AEP/AEPX; behavior when a saved positive stage exceeds the current cycle-safe limit after project mutation/version migration; mapping to internal BEE effect-inclusion fields and RG subgraph boundaries; how adjustment layers, track mattes and 3D/collapse contexts modify stage legality.

Related: `docs/capability-recipes/effect-prefix-rendering.md`, `docs/render-graph/render-request-sufficiency.md`, `F-EVAL-002-layer-param-cycle-safe-stage.md`, `F-EVAL-003-effect-prefix-render-stage-lineage.md`.
