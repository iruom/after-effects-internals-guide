---
status: active
last_verified: 2026-09-16
evidence: SDK history + current SmartFX contract + retained AE 9 preference/debug vocabulary
---
# SmartFX Archaeology: From AE 7/9 to the Modern Render Graph

SmartFX predates MFR by many years and already forced AE to separate dependency planning, bounds, temporal state and pixel execution.

The SDK history records SmartFX documentation as present by After Effects 7.0-era documentation (December 2005). Retained AE 9 configuration vocabulary then exposes host concerns such as `Max SmartEffects Stack Usage`, `Alternate SmartFX Time Comparison`, `Cache TLW Stream Paths`, and `Unflatten sequence data before NewContext`.

These names are archaeological evidence of concerns, not public contracts and not proof that current AE uses the same private implementation.

## The durable public architecture
Modern SmartFX still exposes a two-phase protocol:

`requested output -> SMART_PRE_RENDER dependency/bounds planning -> optional upstream materialization -> SMART_RENDER pixel execution`.

A PreRender may have no corresponding Render at all. AE can ask only for bounds/dependencies, or later discover that the branch contributes nothing. This makes SmartFX an early public example of declarative graph planning before execution.## Why the AE 9 keys matter
`Alternate SmartFX Time Comparison` suggests that temporal-equivalence policy was independently tunable or experimentally variable. `Cache TLW Stream Paths` suggests path/dependency discovery itself could be cached. `Unflatten sequence data before NewContext` ties instance serialization/materialization to render-context creation. `Max SmartEffects Stack Usage` shows SmartFX had its own stack/resource concern.

Do not decode more semantics from the names than they support. Their value is to establish **lower bounds in architectural history**: these problems existed before the modern render-project split and before MFR.

## Historical bug evidence
The current SmartFX Guide preserves a versioned defect note: in an older release, `checkout_layer()` during `PF_Cmd_SMART_PRE_RENDER` could return empty rectangles and callers were advised to repeat the call; the workaround was no longer needed in 11.0.1.

This is valuable because it demonstrates that dependency/bounds discovery itself has had host-side correctness bugs. A historical workaround must therefore be scoped to the affected host generation rather than fossilized into permanent plug-in logic.

## GPU-era extension
From AE 16.0-era SmartFX GPU support onward, PreRender also negotiates whether GPU rendering is possible for the current parameters/render settings and device. AE may retry PreRender with another GPU framework or with no GPU.

The planning phase therefore evolved from bounds/dependency declaration into a broader execution-feasibility negotiation without collapsing into pixel execution.## Continuity without claiming implementation identity
AEIG records continuity at three levels:
- **contract continuity**: public SmartFX still separates planning and execution;
- **problem continuity**: temporal comparison, stream/dependency paths and context state remain relevant;
- **implementation continuity**: only claimed where versioned binary/header/runtime evidence directly supports it.

A preference key disappearing does not prove the subsystem disappeared; it may have become unconditional, renamed, moved to another configuration layer, or been replaced entirely.

## Experiments
Across archived AE versions, run one SmartFX fixture that varies only time, ROI, layer bounds, sequence data and GPU feasibility. Record selector counts/order, PreRender rectangles, checkout IDs, whether Render follows, and state serialization callbacks.

A particularly useful regression corpus is a bounds-only request, a branch eliminated after PreRender, and a source whose bounds change after upstream effects. These stress the exact boundary where historical host bugs have occurred.

## Unknown frontier
The mapping from historical `SmartEffects` private vocabulary to current TDB/BEE/RG classes is unresolved. Similar vocabulary is not enough to claim class lineage.

Cross-links: `../render-graph/frame-checkout.md`, `../render-graph/render-graph-model.md`, `../mfr/overview.md`, `../host-integration/cpp-sdk/state-api-evolution.md`.