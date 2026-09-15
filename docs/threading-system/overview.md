---
status: active
last_verified: 2026-09-16
evidence: current MFR contract + AE 13.5 threading restrictions + AE 2025 runtime queue/executor surfaces
---
# Threading and Concurrency System

After Effects does not have one meaningful "render thread pool". AEIG separates several concurrency domains because they have different ownership, cancellation and host-callback rules.

At minimum:

```text
UI / main thread
    | project mutation, event/UI selectors, host lifecycle
    |
render/effect workers
    | PF render selectors, MFR frame concurrency
    |
BEE / RG scheduling
    | work queues, graph tasks, async checkout
    |
media + audio workers
    | I/O, decode, prefetch, audio render
    |
GPU/device work
    | device queues, kernels, transfer/synchronization
```

These domains can overlap in time but should not be assumed to share one executor or one lock hierarchy.
## Main-thread and render-side boundaries

Adobe's MFR contract explicitly permits render-related selectors to run concurrently when `PF_OutFlag2_SUPPORTS_THREADED_RENDERING` is enabled. `PF_Cmd_GLOBAL_SETUP` and `PF_Cmd_GLOBAL_SETDOWN` remain lifecycle boundaries rather than arbitrary worker callbacks.

Project mutation is much more restricted. AE 13.5 tightened previously tolerated calls: several stream/undo/effect operations must be moved to the UI thread, and passive draw callbacks are not a place to change project state.

`PF_GetCurrentState()` provides a deliberately adversarial signal. In `PF_Cmd_UPDATE_PARAMS_UI` AE returns a randomized state instead of synchronously crossing the unsafe state boundary. Code that accidentally uses it as a real cache identity in that selector should fail visibly rather than sometimes deadlock.

Render-only instances are another ownership class. During render-only sequence setup, the project is read-only and UI selectors are not part of that instance's lifecycle.
## The host callback deadlock rule

The most important MFR threading rule is broader than MFR: **do not hold a blocking plug-in lock while calling back into the host**. Adobe explicitly warns that mutexes/gates held across suite calls or checkout calls are likely to deadlock.

The reason is architectural. A host callback can block, acquire host locks, schedule other work, wait for a dependency or re-enter code whose lock order is outside the plug-in's control. A plug-in mutex therefore participates in a lock graph much larger than the code that created it.

Safer patterns are immutable snapshots, atomics for small state, message passing, request-local data, host-managed caches/single-flight operations, or releasing a local lock before the host call and revalidating afterwards.

A lock-free data structure does not automatically make an effect MFR-safe: object lifetime, sequence-data mutation, global/static state, external libraries and non-thread-safe host APIs can still violate the contract.
## Runtime evidence for layered schedulers

AE 2025 runtime surfaces expose `BEE_WorkQueue`, `bee::RenderTaskManager`, async checkout executors, MediaFoundation decode queues, audio-source/prefetch objects and GPUFoundation/device vocabulary. `BEE_Project::GetOriginationThreadID` also shows that project/thread provenance exists as an explicit runtime concern.

These surfaces support separate scheduler/lifetime domains. They do not prove that each name corresponds to a dedicated OS pool, nor that all queues are active for every render.

## Performance implications

Adobe's current MFR guidance makes resource admission explicit: useful speedup depends on CPU cores, available RAM, GPU compute and the effects/project being rendered. If a frame's memory footprint is high, adding more frame concurrency can reduce rather than improve throughput by increasing pressure, eviction and synchronization.

Composition Profiler time should therefore be interpreted together with concurrency and residency. A slow layer may be CPU-heavy, but it may also serialize through a non-MFR effect, force expensive media/GPU synchronization, or inflate per-frame memory enough to reduce simultaneous frames.

## Experiments

Log selector/thread IDs, BEE/RG queue activity, checkout latency, media/GPU events and memory pressure while varying MFR, CPU reservation, RAM availability, temporal dependencies and GPU effects. Look for overlap and causal waits, not just total thread count.

Unknowns include the exact mapping from BEE work items to worker pools, lock ordering between major subsystems, GPU completion integration and how aggressively workers are reused across project/render epochs.

Cross-links: `../mfr/overview.md`, `../mfr/state-ownership.md`, `../render-graph/render-tasks.md`, `../architecture/project-vs-render-state.md`, and findings `F-THREAD-001` / `F-THREAD-002` / `F-THREAD-003`.
