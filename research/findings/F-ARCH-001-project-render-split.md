---
status: seed
evidence_grade: E0/E1
versions: "13.5+"
last_verified: 2026-09-14
---
# Project and render-side state are architecturally separated

## Statement
SDK history and Adobe architecture material describe render-side local project copies synchronized from editable UI state. This is a core boundary for handle lifetime, sequence data, threading and cache identity.

## Interpretation rule
Do not infer more than the evidence supports. Internal names are observation points, not automatically class or subsystem definitions.

## Next experiment
Measure synchronization epochs and identity preservation with a Probe AEGP and render callbacks.

## Confirmed SDK details
CC 2015 (13.5) separated UI/main-thread and render-thread execution. The SDK states that different threads can be operating on different AE project copies simultaneously. The render project is described as immutable in the migration notes.

AE synchronizes project/effect state by serializing/flattening changes from the UI side to the render side. This made sequence-data flattening frequent enough that `PF_Cmd_GET_FLATTENED_SEQUENCE_DATA` was introduced to obtain a serialized copy without destroying live UI-side structures.

`PF_OutFlag_FORCE_RERENDER` historically doubled as a synchronization trigger when UI-side sequence data needed to reach the render project/effect clone. Adobe explicitly recommended GUID mixing or parameter/arb-data state where possible because those mechanisms preserve reuse after Undo.

## Architectural implication
This is not merely thread separation. It is a replicated-state problem: mutable authoring state must be marshaled into one or more render-safe snapshots/clones. Any internal model must distinguish authoring identity, serialized state and render-instance lifetime.

## Sources
- https://ae-plugins.docsforadobe.dev/intro/whats-new/
- https://ae-plugins.docsforadobe.dev/effect-details/multi-frame-rendering-in-ae/
