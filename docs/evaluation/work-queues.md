---
status: active
last_verified: 2026-09-15
---
# Evaluation Work Queues

AEIG distinguishes **semantic/request scheduling** from **pixel execution scheduling**. The installed runtime contains evidence for both, but their exact ownership boundary is not yet a public contract.

## Confirmed runtime surfaces
- Trace vocabulary includes `BEE_WorkQueue`, `RenderTaskManager` and `RenderThreadExecutor`.
- BEE exports work-queue functions that carry `BEE_LayerRenderOptions` and obtain a render GUID through callback paths.
- BEE also imports/uses RG pre-render, cache validation and graph execution surfaces.
- Media and audio subsystems separately expose asynchronous `Future`/prefetch/cancellation paths, showing that not all AE work is scheduled by one universal queue.

## Working separation
`dependency/request construction -> BEE work item -> render identity -> RG graph request -> render task/thread execution`.

This model explains why an operation may be known/scheduled before any pixels are required. SmartFX PreRender with no Render call is a public example of planning that can terminate before materialization.

## What is not proven
- `BEE_WorkQueue` is not proven to be one physical queue.
- A BEE work item is not proven to map 1:1 to an RG node or OS thread.
- `RenderTaskManager` / `RenderThreadExecutor` naming alone does not prove MFR ownership.
- Queue ordering, priorities, work stealing and affinity remain internal policy.

## Probe strategy
The canonical `EXP-RG-001` capture raises `BEE_WorkQueue`, `BEE_Eval`, RG cache/xform and TDB trace categories around one controlled render. Correlation can establish phase ordering without requiring undocumented queue objects to be invoked directly.

For threading-specific behavior, combine selector-concurrency probes with queue trace; never infer thread safety from parallelism alone.

## Queue identity, cancellation and materialization
A scheduled work item should not be equated with a frame or graph node. The same render identity may be requested by several consumers/generations, and one consumer can become obsolete without making a reusable cached result invalid.

Public async rendering provides a useful analogue: purpose/request generation and frame receipt are separate identities. BEE runtime names for cached checkout, cancellation, pause/resume, speculative preview and async execution support the same high-level separation without proving one shared implementation.

A useful model is:

`consumer/purpose -> semantic render request -> BEE work item/generation -> RG planning -> backend task(s) -> materialized/cacheable result`.

Cancellation can act at several layers: remove an unstarted queue item, stop CPU traversal, signal a decoder, discard a completed obsolete result, or fail to physically abort already-submitted GPU work. Do not infer which happened from a cancelled UI request alone.

## Admission is resource-sensitive
Work scheduling interacts with memory/VRAM pressure, MFR CPU policy, media prefetch, dependency readiness and speculative priority. A work queue is therefore not necessarily FIFO and a larger queue does not automatically mean more useful parallelism.

BEE's VRAM-aware/thread-count surfaces are evidence that scheduling policy can incorporate resource budgets before final backend work is admitted.

## Failure patterns and experiments
Failure classes to separate include stale-result publication, starvation/priority inversion, duplicated equivalent work, resource oversubscription, cancellation that arrives after materialization and lock inversion between host callbacks and plug-in code.

Probe with identical semantic requests from multiple consumers while varying time scrub speed, MFR CPU cap, GPU memory pressure and cache warmth. Record purpose/request generation, BEE/RG/TDB trace timestamps, thread IDs, cancellation events and output hashes.

A second experiment should schedule an expensive request and make it obsolete immediately, then measure whether CPU/GPU/media work stops, continues but is discarded, or completes into a reusable cache entry.

## Version and unknown frontier
Current work-queue evidence is primarily local 25.x/26.x runtime/trace vocabulary plus public async/MFR contracts. Queue priorities, work stealing, affinity, task fusion, dependency wakeups and exact ownership of `RenderTaskManager` versus BEE WorkQueue remain private policy.

Related: `docs/render-graph/async-render-requests.md`, `docs/render-graph/render-tasks.md`, `docs/threading-system/overview.md`, `docs/memory-system/runtime-architecture.md`.
