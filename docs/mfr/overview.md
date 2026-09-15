---
status: active
last_verified: 2026-09-16
evidence: current Adobe MFR contract + AE 25.6 headers/samples + local runtime scheduling vocabulary
---
# Multi-Frame Rendering

Multi-Frame Rendering (MFR) is not merely "render several frames at once". It changes the ownership model for effect-instance state, selector concurrency, sequence-data access, cache design and the circumstances under which host callbacks are safe.

## Contract transition
Effects opt into concurrent frame rendering with `PF_OutFlag2_SUPPORTS_THREADED_RENDERING`. Once enabled, render-related work may execute concurrently while UI/lifecycle activity exists elsewhere in the host. Code that was accidentally safe under single-frame serialization can become racy without any API signature changing.

Adobe's March 2021 SDK changed the sequence-data model used by MFR. Render-time sequence data is read as const through `PF_EffectSequenceDataSuite1`; writing ordinary `sequence_data` during render is no longer the normal supported model. Effects built against the earlier June 2020 MFR SDK needed recompilation for the revised behavior.

`PF_OutFlag2_MUTABLE_RENDER_SEQUENCE_DATA_SLOWER` exists only as a compatibility escape hatch. AE duplicates sequence data for render threads, so each rendering thread owns an independent mutable copy rather than a synchronized shared accumulator. Adobe explicitly warns that this reduces MFR performance and recommends Compute Cache when expensive computed state must be shared/reused.

## State model
A useful decomposition is:

`persistent instance state -> render-safe snapshot -> per-render-thread view -> frame task -> host checkout/render/cache work`

Do not collapse persistent sequence state, mutable UI state, per-frame scratch data and reusable computed cache state into one object simply because all four were historically reachable from one effect instance.

## Thread-safety is wider than Render()
MFR safety is a property of the whole effect implementation, not just the pixel loop. Static/global variables, shared helper libraries, lazy initialization, logging, allocator wrappers, mutable caches and callbacks reached indirectly from a render thread all participate in the concurrency contract.

The practical audit question is therefore not "does Render write globals?" but "can two independent frame tasks enter any shared mutable path at once, and can UI/main-thread activity race that path?".

A plug-in mutex is not automatically a fix. Holding a plug-in lock while calling AE suites, checking out frames, acquiring host resources or entering another effect-dependent path can invert lock ordering against host internals. Prefer immutable snapshots, host-managed caches and short lock-free/leaf critical sections over serializing the host from inside a plug-in.

## Sequence data vs Compute Cache
Sequence data is appropriate for persistent per-instance information that must survive project save/load after flattening. Compute Cache is appropriate for expensive derived values that can be regenerated and are not project persistence.

That distinction matters under MFR:
- persistent configuration belongs in parameters/sequence data;
- immutable render-readable state can be snapshotted from sequence state;
- expensive derived state should prefer Compute Cache when shareable;
- per-frame temporary state belongs to the frame/render invocation;
- mutable thread-local sequence copies are a compatibility mechanism, not a cross-frame communication channel.

The Compute Cache is not written to the project file. A project reopened on another machine must be able to reconstruct its cached values from durable inputs.

## Sequence persistence trap
`sequence_data` may contain pointers/handles only in its live form. When flattened for project persistence those process-local references must be replaced by disk-safe representation and reconstructed during resetup. MFR does not relax this rule; it makes accidental lifetime coupling harder to hide.

## Performance model
More concurrent frames are useful only while another bottleneck is not dominant. Real limits include RAM pressure, source decode throughput, temporal dependencies, plug-in compatibility, GPU queue contention, synchronization and cache churn. An effect can be technically MFR-safe yet scale poorly if each frame expands memory residency or serializes around a shared resource.

For optimization work, measure at least:
- frames concurrently admitted;
- peak resident memory per concurrent frame;
- source/decode reuse across frames;
- CPU work vs GPU submission/wait time;
- Compute Cache hit rate and value size;
- lock wait time inside plug-in code;
- checkout fan-out caused by temporal sampling.

## Failure signatures
Common MFR-specific bugs include nondeterministic output, crashes only at high concurrency, stale derived state, accidental cross-frame mutation, per-thread state mistaken for global accumulation, project-load failures caused by invalid persisted pointers, and performance regressions caused by the mutable-sequence compatibility mode.

A deterministic single-frame render is not sufficient validation. Compare repeated renders at different MFR concurrency levels and deliberately vary frame ordering. Hash outputs and record host/build/GPU/environment data so scheduling-sensitive failures can be distinguished from numerical drift.

## Evidence and cross-links
Primary public contract: Adobe C++ SDK Guide, `Multi-Frame Rendering in AE` and `Global, Sequence, & Frame Data`. Local evidence includes AE 25.6 headers/samples and runtime scheduling/trace vocabulary.

Related pages: `docs/threading-system/overview.md`, `docs/persistence/sequence-data.md`, `docs/cache-system/compute-cache.md`, and Findings `F-MFR-002`, `F-THREAD-001`, `F-THREAD-002`, `F-THREAD-003`.

## Unknown frontier
AEIG does not claim to know AE's exact MFR admission heuristic, worker-pool implementation, memory-pressure thresholds or scheduling priority rules. Those require controlled host observations; public MFR contracts establish plug-in obligations, not the complete internal scheduler.
