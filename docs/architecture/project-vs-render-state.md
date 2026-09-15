---
status: active
last_verified: 2026-09-16
evidence: AE 13.5 render-project synchronization notes + current PF/MFR/UI contracts + local state/trace findings
---
# Project State vs Render State

After Effects must be modelled as having at least two ownership domains: the editable project/UI state and state consumed by render/evaluation work. They are related, but they are not safely interchangeable live object graphs.

A useful architectural model is:

```text
editable project / UI state
        |
        | mutation, undo, parameter supervision
        v
synchronization / flattening boundary
        |
        v
render-side effect/project state
        |
        +--> TDB/property evaluation
        +--> expressions/dependencies
        +--> BEE request identity/work queues
        +--> RG/checkouts/materialization
```

The exact internal serialization format and snapshot granularity remain unknown; the boundary itself is strongly supported by public SDK behavior.
## Public evidence for the boundary

AE 13.5 tightened rules that previously allowed plug-ins to get away with treating UI-side state as render-side state. Adobe documents that render project/effect copies must be synchronized, and that `PF_OutFlag_FORCE_RERENDER` historically participated in copying `sequence_data` from the UI instance to the render project/effect clone.

`PF_GetCurrentState()` provides another strong signal. It is useful for comparing render-relevant input state, but AE deliberately prevents it from being treated as an unrestricted live-state read from `PF_Cmd_UPDATE_PARAMS_UI`; the documented behavior exists to avoid unsafe synchronization/deadlock paths.

Modern MFR makes the separation unavoidable: render selectors can execute concurrently while UI selectors are active. Ordinary render-time sequence state is exposed through the Effect Sequence Data Suite as a render-side view rather than as freely mutable UI memory.

`PF_InFlag_PROJECT_IS_RENDER_ONLY`, valid during `PF_Cmd_SEQUENCE_RESETUP`, makes the host distinction explicit: a render-only effect instance should treat the project as read-only and will not receive UI selectors.

Async custom-UI rendering reinforces the same architecture. UI code requests a semantic render result through a host-managed manager instead of synchronously walking authoritative render state.
## Developer rules

- Do not keep raw UI-side handles/pointers and assume they are authoritative on render workers.
- Treat UI mutation and render consumption as a synchronization protocol, not shared-memory convenience.
- Put user-visible durable state in documented parameter/sequence/arb-data routes; put expensive derived state in host-managed cache mechanisms when possible.
- Reacquire render-side resources through the suite/context supplied for the current selector.
- If a UI event changes render semantics, use the documented invalidation/synchronization mechanism rather than mutating hidden render state directly.
- Never infer that a view-only change must invalidate render identity; project/document state, render state and per-view state are distinct axes.

## Failure patterns

Typical bugs caused by violating this model include stale render state after a UI edit, use-after-free of UI-owned handles, nondeterministic MFR results, deadlocks caused by host callbacks under plug-in locks, and caches keyed from state that is newer or older than the render snapshot actually being consumed.

Undo is a particularly useful adversarial test: a correct state identity mechanism should distinguish semantic state while still allowing old cached results to become reusable when the project returns to an earlier state. Blind `FORCE_RERENDER`-style invalidation loses that information.

## Experiments and unknowns

Measure UI mutation time, render callback time, sequence-data generation, `PF_State`/receipt changes and BEE/TDB/RG trace identity around the same edit. Repeat with Undo/Redo and MFR on/off. The unresolved questions are snapshot granularity, synchronization epoch boundaries, and whether different render subsystems consume one common epoch or independently materialized views.

Cross-links: `../state-model/snapshots.md`, `../mfr/overview.md`, `../mfr/state-ownership.md`, `../ui-system/view-state-and-render-boundary.md`, `../cache-system/state-identity.md`, and findings `F-THREAD-002` / `F-THREAD-003`.
