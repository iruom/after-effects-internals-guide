---
status: researched-seed
evidence_grade: E0/E1
confidence: 0.97
versions: "historical design plus current SmartFX contract"
last_verified: 2026-09-14
---
# Temporal footprint is wider than frame time

## Statement
Both historical Adobe design material and current SmartFX APIs model a frame as depending on a **time footprint**, not merely one timestamp. Motion blur, time remap, time stretch, expressions and effects that sample other times can expand or transform that footprint.

`PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT` lets AE track parameter checkouts over time so changes outside the actual dependency interval do not invalidate a cached frame. The older patent architecture similarly expands cache-validation intervals over the shutter-open range.

## Consequence
Temporal dependency should be represented as an interval/set transform attached to graph edges. Treating time as a scalar frame index loses essential semantics.

## Niche edge case
The SDK warns that time-dependent data cached in sequence data must be validated with `PF_GetCurrentState` / `PF_AreStatesIdentical`; otherwise the host's tracked temporal dependencies and the plug-in's private cache can disagree.

## Sources
1. PF_OutData / AUTOMATIC_WIDE_TIME_INPUT: https://ae-plugins.docsforadobe.dev/effect-basics/PF_OutData/
2. Parameter Supervision: https://ae-plugins.docsforadobe.dev/effect-details/parameter-supervision/
3. Adobe patent US7103839B1: https://patents.google.com/patent/US7103839B1
