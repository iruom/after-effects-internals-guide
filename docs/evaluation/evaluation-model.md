---
status: active
last_verified: 2026-09-14
---
# Evaluation Model

Working hypothesis: AE combines **state invalidation** with **demand-driven evaluation**, while preserving prior state identities so previously rendered results can reappear after undo/redo or parameter reversion.

This is richer than a simple dirty-DAG model. Required measurements:
- state-change event
- dependency update
- render request
- checkout request
- callback execution
- cache reuse
- final pixel change

Each must be logged independently.

## Stronger historical model than the initial push/pull hypothesis
US7103839B1 explicitly contrasts push and pull invalidation. Its described approach stores local edit information and performs recursive validity checks when cached output is requested, giving concrete historical evidence for a pull-style validity architecture with time-aware local state.

This changes the research question. Instead of asking only "push or pull?", test which responsibilities are split among:
- edit-time state/version updates;
- dependency discovery;
- render-graph construction;
- cache-validity traversal;
- speculative scheduling;
- actual render execution.

The patent also describes **collateral dependencies**: semantic references such as expressions can create dependencies outside the ordinary compositing hierarchy. This directly motivates separate project/semantic and render dependency relations.

## Modern correlation targets
Local Trace Database categories `BEE_Eval`, `BEE_Project`, `BEE_Undo`, `BEE_WorkQueue`, `RenderNode.RG_*` and `MixHashGuid` should be correlated with controlled edits. Their names are not proof of structure, but they give precise instrumentation targets.

## Source
- https://patents.google.com/patent/US7103839B1

## Experiment-backed invariant: semantic state controls deterministic temporal output
`EXP-CORE-001` provides the first AEIG Observatory result directly validating part of this model on AE 26.3. A deterministic 120-frame fixture was evaluated twice without edits, then a single class of semantic state was changed: the midpoint Gaussian Blur keyframe on three layers.

The unchanged A/B passes were byte-identical for all 120 PNG outputs. After the midpoint change, frame 0 remained identical while frames 1–119 changed. This is exactly the direction predicted by time-varying interpolation: the t=0 endpoint remained unchanged, while later sampled values depended on the edited midpoint.

This result establishes an **evaluation-level** invariant, not a specific invalidation implementation:
`equivalent evaluated state at t -> equivalent output`, while an edit that changes the evaluated state over a temporal region changes output over that region.

The experiment does not yet distinguish push dirty propagation, pull validity traversal, render-GUID changes, or cache-key replacement. Those mechanisms remain targets for the Receipt and BEE/RG experiments.

See `F-EVAL-004` and `experiments/observatory/manifests/EXP-CORE-001.json`.
