---
status: active
last_verified: 2026-09-16
evidence: AE 2025 BEE runtime exports + Trace vocabulary + MFR/public render contracts
---
# Render Tasks, Work Queues, and Executors

AEIG separates **render graph representation**, **render task objects**, **work-queue jobs**, and **execution resources**. Treating all of these as "threads" hides the most important scheduling and lifetime boundaries.

A practical model is:

```text
semantic render request / render options
        |
        v
BEE request identity + dependency planning
        |
        v
RG pre-render / graph / cache-node state
        |
        v
RenderTask / WorkQueue jobs
        |
        +--> CPU render workers
        +--> async checkout executor
        +--> media/audio queues
        +--> GPU/device submission
        v
receipt / output / cache residency
```

One graph node is not necessarily one task, one task is not necessarily one OS thread, and one frame is not necessarily one task graph.
## Concrete BEE task-manager evidence

Installed AE 2025 exports expose `bee::RenderTask` and `bee::RenderTaskManager` surfaces including cloned/const project access, renderer-status pointers, abort/progress handling, task initialization and retrieval of subsequent render tasks.

This is important because task execution is visibly associated with a project/render-context view rather than being an anonymous closure over global mutable project state.

The same runtime contains frame-range helpers that expose current frame time, current render options, outstanding output-queue size, finished-frame counts, out-of-memory state, cache-purge-limit state and methods for producing the next `RenderTask`.

These names are runtime implementation evidence, not a supported plug-in API. They justify a scheduling model with explicit task/project/status objects, but do not establish exact field layout or synchronization semantics.

## WorkQueue is a higher-level orchestration surface

`BEE_WorkQueue_*` exports cover item/layer checkout, cached checkout, frame ranges, synchronous and asynchronous paths, audio render, output render, generic analysis jobs, completion callbacks, cancellation, pause/resume, listener registration and speculative-preview control.

`BEEp_WorkQueue_GetRenderGuidWithRO` directly associates work-queue activity with layer render options and render identity. The queue therefore participates in semantic scheduling, not only raw thread dispatch.
## Scheduling dimensions

At least four forms of concurrency should be kept separate:
- **inter-frame concurrency**: MFR allows multiple frame-level requests to coexist;
- **intra-frame tasking**: graph/checkouts/effects may create multiple schedulable units inside one frame;
- **media/audio concurrency**: decode, prefetch and audio jobs can run on separate queue systems;
- **device concurrency**: GPU work may be submitted asynchronously and complete independently of CPU task creation.

The public MFR model adds another resource constraint: useful parallelism depends on CPU cores, available RAM, GPU work and project/effect characteristics. More schedulable tasks do not imply more useful workers.

Speculative Preview further proves that not all work is directly caused by an explicit foreground render. BEE exports include start/cancel/state-change surfaces for speculative work, so queue occupancy can include future/idle work that may be invalidated before use.

## Failure and performance interpretation

A stalled preview can come from graph dependency, queue admission, memory pressure, checkout latency, media decode or GPU synchronization. Thread count alone cannot identify the bottleneck.

Out-of-order completion is not evidence of incorrect graph order: schedulers may preserve dependency order while allowing independent work to complete in a different wall-clock sequence.

Cancellation must be treated as normal. A task can be valid when scheduled and obsolete before materialization because UI state, time, ROI or speculative-preview demand changed.
## Experiments and unknowns

Capture task/queue trace activity while varying one axis at a time: MFR on/off, RAM pressure, GPU effect presence, temporal dependency, ROI, speculative preview, media decode and cancellation. Record thread IDs, frame IDs, render GUIDs, checkout IDs, queue depth/performance counters and completion order.

High-value questions remain open:
- how many internal tasks one RG node can expand into;
- whether queue partitioning is per project, render context or global host;
- how cache hits bypass or shorten task construction;
- when a cloned project is allocated/reused across MFR frames;
- how GPU/device completion feeds task readiness;
- which scheduler owns async media and audio dependencies.

Do not infer FIFO behavior, fixed worker pools, graph-node/task 1:1 mapping or universal work stealing from symbol names alone.

Cross-links: `frame-checkout.md`, `render-graph-model.md`, `../evaluation/bee.md`, `../mfr/overview.md`, `../threading-system/overview.md`, `../cache-system/state-identity.md`, findings `F-RG-001` / `F-RG-003`, and `datasets/ae-2025-runtime-internal-surface.csv`.
