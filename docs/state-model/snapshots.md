---
status: active
last_verified: 2026-09-16
evidence: AE 13.5 local-project-copy architecture + sequence-data synchronization contracts + MFR render copies + current BEE RenderTask project surfaces
---
# Snapshots and Synchronization

AEIG models editable project state and render-side state as related **semantic generations**, not as one universally shared mutable object graph.

## 13.5 made the split explicit
Adobe's 13.5 SDK notes state that the render thread has its own local copy of the project and can no longer modify the UI project. Rendering can no longer push mutated sequence data back to UI for custom-UI updates.

This was introduced for interactive performance/responsiveness and deliberately broke assumptions that older plug-ins could make when UI and render effectively behaved as one synchronous state domain.

A useful boundary is:

`editable UI project -> serialization/synchronization -> render-local project state -> evaluation/render request`.

The word **snapshot** in AEIG names this semantic boundary; it does not claim that AE serializes the entire project into one monolithic blob for every frame.

## Sequence data shows the publication mechanism
Starting in 13.5, AE may need to flatten/serialize effect `sequence_data` more frequently so UI-side changes can be sent to the render-side copy. `PF_Cmd_GET_FLATTENED_SEQUENCE_DATA` was added so AE can obtain a correct flattened copy without destroying the UI instance's live unflattened data.

`FORCE_RERENDER` also gained synchronization implications: in some cases it forces UI sequence state to be copied to the render project/effect clone. This is why FORCE_RERENDER is not merely a cache invalidation button.

## MFR strengthens the model
March-2021/MFR contracts make render-time `sequence_data` const by default. If the compatibility flag for mutable render sequence data is used, AE duplicates sequence data to each render thread; each thread gets an independent copy and modifications are discarded as render spans finish.

Therefore there are at least three distinct effect-state lifetimes:
- live/UI sequence state;
- synchronized immutable render state;
- optional thread-local mutable compatibility copy.

Shared derived computations belong in an explicit shared cache such as Compute Cache, not in thread-local mutable render sequence data.

## Runtime correlation
Local BEE runtime surfaces expose `RenderTask` accessors for a cloned project and a const project/render context. This is consistent with public snapshot semantics. AEIG treats it as implementation correlation, not proof that every public render callback maps to one specific `RenderTask` instance.

## Snapshot coherence versus identity
A snapshot/generation must be coherent enough that a render request observes mutually compatible property, sequence, expression and topology state. But coherence does not imply memory-address stability.

Persistent Item/Layer IDs can survive publication while:
- AEGP handles are reacquired;
- stream refs are rebuilt;
- evaluated values change;
- Render GUIDs change;
- RG nodes/tasks are recreated.

So "same project object" and "same render snapshot" are different identity questions.

## UI state is not all published equally
26.5 Guide/View APIs provide a clean public example: guide geometry/data belongs to document item/layer state while visibility/snap/lock can be per-view presentation state. Workspace/panel selection and other shell state likewise need not participate in render publication.

Snapshot membership should therefore be modeled by **semantic relevance**, not by "everything the application currently knows".

## Failure patterns
- render uses old UI-derived sequence state -> stale output after edit;
- UI expects data generated during render to appear in live sequence state -> broken custom UI after 13.5;
- cache AEGP refs across publication/topology changes -> invalid handles;
- mutate shared global state from concurrent render generations -> cross-frame races;
- force broad synchronization for data that could be represented as a semantic GUID/cache key -> UI stalls and lost cache reuse.

## Reconstruction experiments
For one effect instance, change exactly one state class at a time: ordinary parameter, sequence-only custom dialog state, expression source, topology, view-only state and external dependency.

Record UI generation, flattened sequence bytes/hash, render request identity, BEE/TDB/RG trace, output hash and whether Undo returns to a previous cache identity.

A high-value result is a **publication matrix** showing which state changes require a new render generation and which remain UI/view-local.

## Unknown frontier
Still unresolved:
- synchronization granularity and publication epoch boundaries;
- whether modern render projects are incrementally patched, copy-on-write, structurally shared or rebuilt through another strategy;
- exact lifecycle of BEE cloned projects across MFR tasks;
- how expression/preprocessor caches are scoped to snapshot generations;
- exact relationship between snapshot publication and Render GUID/cache-node invalidation.

Related: `docs/architecture/project-vs-render-state.md`, `docs/mfr/state-ownership.md`, `docs/state-model/object-identity.md`, `docs/render-graph/render-tasks.md`.
