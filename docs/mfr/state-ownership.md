---
status: active
last_verified: 2026-09-16
evidence: current MFR/sequence-data contracts + AE 13.5 render-state split + 25.6 Supervisor sample
---
# MFR State Ownership: Where Mutable Data Belongs

Multi-Frame Rendering turns effect-instance state into an ownership problem. "Is my render function reentrant?" is only one part of the question; the harder question is **which copy of state each concurrent render is allowed to observe and mutate**.

AEIG separates six useful state classes:

```text
1. global process/module state
2. UI/main-thread instance state
3. persistent/serialized sequence state
4. render-side const sequence snapshot
5. shared derived Compute Cache state
6. request-local pre-render/frame/transient state
```

Putting data in the wrong class creates stale-state, race, duplication or persistence bugs even when individual memory accesses are synchronized.
## Global and UI-side state

Global/static state is shared across effect instances and render calls. If a threaded effect uses it, every read/write path must remain race-free. Prefer immutable tables or one-time initialization; a process-global mutable cache is usually a poor substitute for host-managed cache identity/lifetime.

UI selectors remain on the main thread, but render/sequence selectors may run concurrently. UI-visible state must therefore reach render work through parameters, serialized sequence state or another documented synchronization path rather than through an unsynchronized side channel.

AE 13.5's render-project separation makes this especially important: the UI effect instance and render-side effect/project copy can be at different ownership boundaries even when they represent the same logical plug-in instance.

## Sequence data: persistence is not a render scratchpad

Sequence data is instance-scoped persistent/custom state. If it needs flattening, the flat representation must be portable across project save/load and, where relevant, macOS/Windows byte-order/layout differences.

With modern MFR, render-time sequence data is read-only by default and retrieved through `PF_EffectSequenceDataSuite1`. This is the normal fast path because many render threads can observe the same semantic state without treating it as a live accumulator.
## Mutable render sequence data is a compatibility mode

`PF_OutFlag2_MUTABLE_RENDER_SEQUENCE_DATA_SLOWER` restores render-time writes for legacy designs, but AE does so by giving each render thread its own sequence-data copy. Those copies are **not shared or synchronized with each other**.

That means mutable sequence data cannot be treated as a cross-frame accumulator. If frame A updates its copy, frame B is not entitled to observe that update. Expensive initialization may be redundantly repeated on multiple render threads.

This flag therefore solves compatibility, not shared computation.

## Compute Cache is the shared-derived-state route

Use Compute Cache when multiple render requests need the same expensive derived object. Its key should encode the semantic inputs that make the derived value valid, and its checkout receipt gives the host a lifetime/eviction boundary.

The cache can single-flight duplicate computation across threads, unlike per-thread mutable sequence copies. It is also integrated into AE's broader cache pressure instead of remaining an invisible plug-in allocation.

Do not move user-visible persistent state into Compute Cache: eviction must never destroy project semantics. Cache values should be reconstructable from durable inputs.
## Request-local state

`pre_render_data`, frame-local stack/heap objects and selector-local checkouts belong to one render request. They are ideal for bounds/planning decisions or temporary objects that should not survive into unrelated frames.

SmartFX ownership is asymmetric: PreRender may have no matching SmartRender, so data handed to the host must have an independent destruction path. Never make request-local cleanup depend on a future render callback occurring.

## Supervisor sample: a negative design example

Adobe's `Supervisor` sample is valuable precisely because it exposes an awkward ownership pattern. It mutates sequence-derived state from UI/render paths and is not advertised as a clean MFR-safe state model. Treat this as evidence that "we have a mutex" is not enough when one object is simultaneously persistent UI state and mutable render state.

For new designs, decompose instead:
- parameters/arb data: user-authored semantic state;
- sequence data: durable instance metadata/snapshot source;
- Compute Cache: expensive shared derived state;
- pre-render data: request planning state;
- local variables / explicit thread-local objects: transient execution state.

## Failure signatures

State-ownership bugs often appear as MFR-only flicker, non-deterministic cache keys, Undo/Redo mismatch, project reload differences, memory leaks after cancellation, repeated expensive setup on every render thread, or a render result depending on which frame happened to execute first.

A particularly strong test is to render the same frame set in different concurrency/order conditions and compare hashes. Correct semantic state should not depend on scheduling order.

Cross-links: `overview.md`, `../threading-system/overview.md`, `../architecture/project-vs-render-state.md`, `../cache-system/state-identity.md`, `../capability-recipes/compute-cache-deduplicate-work.md`, and the current MFR/Compute Cache SDK contracts.
