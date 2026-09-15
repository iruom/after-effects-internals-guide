---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G 26.5
---
# F-EVAL-002 — AE exposes dynamic cycle analysis for layer-parameter render stages

AEGP_StreamSuite7 adds `AEGP_GetStreamInputStageCycleSafeLimit` for `PF_Param_LAYER` streams. It returns the highest render stage that will not introduce a render cycle in the current project state.

Adobe requires callers to re-query the limit because it changes when effects are added, removed or reordered, or when the selected source layer changes. Source stage 0 is always safe.

## Internal implication
Cycle validity is not a static property of a parameter declaration. It depends on current graph topology and effect ordering.

This is direct public evidence that AE performs graph-aware dependency validation for intra-layer stage references.

## Research direction
Compare the public cycle-safe limit with SmartFX checkout behavior, expression self/cross-layer cycles, and runtime BEE/RG dependency traces. Determine whether they share one graph service or independent cycle detectors.
