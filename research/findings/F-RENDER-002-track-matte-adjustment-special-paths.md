---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Track mattes and adjustment layers have explicit structural render paths

## Local evidence
Crash symbols expose `BEE_VerifyValidPossibleTrackMatte` and `BEE_GetNumLayersToRenderGivenAdjLayer` near render-GUID and pre-render-graph operations.

## Interpretation
These features are not merely blend flags applied at the final pixel stage. They affect graph construction/dependency selection and therefore cache identity and render-subgraph topology.

## Research questions
- Does a track matte create a cross-layer graph edge or a special composite node?
- Does an adjustment layer define a range/barrier over the layer stack?
- Which edits alter graph topology versus only node parameters?

## Experiment
Move adjustment layers and matte providers one slot at a time and compare GUID activity, RG graph traces, effect callbacks, ROI and cache reuse.