---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Transform state has an explicit render-GUID mixing path

## Local evidence
A crash stack exposes `BEE_Layer::MixInGuidForTransform` immediately before layer/composition render-GUID computation.

## Interpretation
Transform state can be mixed into a broader render identity as a distinct component rather than forcing all upstream image state to be regenerated. This is compatible with historical Post-Effect Cache designs where effects can remain cached while downstream transforms change.

## Optimization implication
A modern graph can model transform state as a separable downstream fingerprint when no operator requires pre-transform materialization. This minimizes invalidation and enables transform concatenation.

## Next experiment
Compare position/scale/rotation changes against effect-parameter changes and look for upstream effect callback suppression plus transform-side graph activity.