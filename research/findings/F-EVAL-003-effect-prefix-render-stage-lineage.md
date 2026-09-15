---
status: strong-cross-version-correlation
last_verified: 2026-09-15
evidence: Guide-26.5 + AE-25.6-headers + old-headers + AE-2025-binary-surface
---
# F-EVAL-003 — Effect-prefix render stage has a long cross-surface lineage

AE 26.5 `AEGP_StreamSuite7` makes a `PF_Param_LAYER` carry two independent public values: source layer identity and `AEGP_LayerParamStage`.

The stage domain includes source-before-masks/effects, masks-only, all-effects, and positive 1..N values meaning render through effect N. The API also exposes a dynamic cycle-safe upper bound.

This public feature has strong predecessors rather than appearing from nowhere.

## Layer Render Options predecessor
AE 25.6 `AEGP_LayerRenderOptionsSuite2` can create requests from a layer, upstream of a selected effect, or downstream including the selected effect's output. Its comments explicitly describe an internal `EffectsToRender` dimension.
## Canvas receipt predecessor
Legacy Canvas receipt APIs accept `num_effectsS`, and `AEGP_GenerateRenderReceipt` generates a receipt as if the first N effects have been rendered. Historical headers show this effect-count dimension was added to receipt checking in the AE 7.0 transition.

Thus a prefix of the effect stack has been a first-class render/cache-validity coordinate for many generations.

## Installed AE 2025 correlation
`BEE.dll` exports:
- `BEE_GetEffectIncludedInRender(effect, time, LayerRenderOptions)`;
- `BEE_GenerateArtisanReceipt(..., short, LayerRenderOptions, rect)`;
- `BEE_CheckArtisanReceipt(..., LayerRenderOptions, ..., short, ...)`;
- `BEE_GetLayerROForArtisan` and receipt-bearing Artisan render paths.

The demangled binary signatures preserve both `BEE_LayerRenderOptions` and short integer fields at the Artisan receipt boundary. This is structurally consistent with the public effect-prefix contracts, although symbol signatures alone do not name those integer parameters.
## Strongest justified conclusion
The effect subset/stage is best modelled as a long-lived render-request coordinate, not a StreamSuite7-specific convenience. StreamSuite7 appears to expose independently a dimension that older layer-render and receipt APIs already needed internally.

This does **not** prove that `AEGP_LayerParamStage`, legacy `num_effectsS`, `EffectsToRender` and any BEE field are the same integer or share storage. The contracts differ in representation and context.

## Integer-domain caution
Current StreamSuite7 uses positive **1..N** for "through effect N", while legacy receipt APIs speak in counts and LayerRenderOptions comments use an effect index/selected-effect construction. AEIG must not silently equate those integer domains or assume an off-by-one mapping without a behavioral test.

Useful abstract coordinate:
`EffectStage = Source | MasksOnly | Prefix(N) | AllEffects`, with API-specific encoding kept outside the semantic model.

## Cross-system implication
Effect-stage identity links three concerns that should remain connected in AEIG: cycle avoidance when checking out a layer parameter, render-request identity/sufficiency, and partial receipt/cache validity. A stage can therefore be meaningful even when no final frame is materialized yet.

## Next experiment
For an E1→E2→E3 chain, compare StreamSuite7 stage N, LayerRenderOptions upstream/downstream requests and Canvas receipt prefix N under edits before/after the boundary. Record returned pixels, receipt status/GUID and any BEE/RG trace/cache reuse. Agreement would support one semantic coordinate with multiple encodings; disagreement would reveal distinct stage domains.

Related experiment: `experiments/canvas-receipt-prefix-status.md`. Related model page: `docs/render-graph/layer-input-stage.md`.
