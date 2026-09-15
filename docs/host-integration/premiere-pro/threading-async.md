---
status: active
last_verified: 2026-09-16
evidence: Premiere threaded-work/async/deferred contracts + AE MFR/Async Manager/BEE comparison
---
# Premiere Threading and Async Contracts as a Comparison Surface

Premiere exposes several scheduling concerns through explicit public suites. AE exposes different APIs, but the comparison is valuable because it separates **semantic work** from **execution policy**.

Do not infer AE uses these Premiere suites internally.

## Threaded work registration
`PrSDKThreadedWorkSuite` allows plug-ins to register work with the host rather than own arbitrary worker threads.

The contract distinguishes:
- work that may run concurrently on render workers;
- serialized/single-threaded callback entry;
- registration identity and queued instances;
- plug-in instance lifetime associated with queued work.

Queueing the same concurrent registration multiple times can produce overlapping callback execution.
Versioned contracts also tie queued work to plug-in-instance validity: when the host knows the instance is gone, the associated work can be suppressed rather than letting callbacks race a destroyed object.

That is a useful lifetime pattern for analyzing AE's host-managed async work.

## Async operation hierarchy
`PrSDKAsyncOperationSuite` models operations/sub-operations with IDs, progress and execution-policy flags. `PrSDKDeferredProcessingSuite` separately represents delayed/pending work.

This separation is instructive:
- **identity/progress tree** is one concern;
- **worker concurrency policy** is another;
- **deferral/readiness** is another.

A single “background task” abstraction hides all three.

## AE comparison map
AE exposes analogous concerns through different surfaces:
- MFR selector concurrency;
- effect custom-UI Async Manager;
- AEGP async frame requests/checkouts;
- Compute Cache single-flight/in-flight state;
- internal BEE WorkQueue / RenderTaskManager;
- MediaFoundation decode queues;
- GPU queue/device work.

The overlap is conceptual, not ABI identity.
## Questions to carry back to AE
- Is request cancellation tied to semantic request identity or only task ID?
- Does instance destruction suppress queued work, or must the extension cancel explicitly?
- Which callbacks may re-enter plug-in code concurrently?
- Which progress/cancellation APIs are safe from worker threads?
- Can host-managed work be serialized without forcing UI-thread execution?
- What state must be immutable/snapshotted before queueing?

## Failure modes
- confusing “single-threaded” with “UI-thread”;
- owning raw instance pointers across queued work without lifetime protection;
- assuming cancellation means a worker stopped synchronously;
- treating progress hierarchy as execution dependency;
- applying Premiere callback-thread guarantees to AE without confirmation.

## Experiment transfer
For AE Async Manager/BEE work, create two semantic requests with the same purpose but different render options, cancel/replace one, then trace callback/task lifetime. Separately destroy or invalidate the owning project/effect state and observe whether work is suppressed, cancelled or completes into a stale-result path.

Cross-links: `../../threading-system/overview.md`, `../../render-graph/render-tasks.md`, `../../ui-system/async-custom-ui-rendering.md`, `../../foundations/cross-host-triangulation.md`.