---
status: active
last_verified: 2026-09-16
evidence: Adobe Help memory contract (2026) + AE 2025 runtime residency/purge surfaces
---
# Memory System

AE memory behavior is not one heap plus one cache. It is a set of **residency domains, leases and pressure policies** spanning host RAM, shared Creative Cloud memory, media caches, render caches, GPU device memory and plug-in-owned allocations.

The first rule is:

`semantic identity != validity != residency != pin/lease lifetime != eviction policy`

A valid render result may be evicted. A resident object may be semantically stale. A checked-out object may be temporarily non-purgeable without becoming globally valid.

## Adobe application memory pool
Current Adobe documentation says After Effects shares a memory pool with other Creative Cloud applications such as Premiere, Photoshop and Audition.

A memory balancer coordinates applications using reported minimum need, maximum usable memory, current usage and priority. Foreground AE/Premiere can receive higher priority than background processes.
That makes another Adobe application starting or stopping a legitimate cause of preview-memory capacity changing without any project edit.

`RAM reserved for other applications` constrains the Adobe pool but is not itself the size of one AE cache.

## Runtime residency domains
Local AE 2025 evidence exposes multiple independent owners:
- MediaFoundation managed/data caches and `CacheGuard`-style lease objects;
- BEE/work-queue and feature-specific frame/cache residency;
- GPUFoundation `AssetCache` and adapter-budget pressure paths;
- public AEGP Compute Cache with explicit checkout receipt and size accounting;
- plug-in/global/sequence/pre-render allocations owned by the extension itself.

These domains can respond differently to the same system pressure.

## Pressure and purge
Memory pressure should be modeled as:

`pressure signal -> domain policy -> candidate eviction/purge -> reclaimed bytes -> re-evaluate pressure`

OS private bytes, working set, shared Adobe pool pressure and GPU adapter budget are different signals. A host-RAM purge need not free GPU residency; a GPU purge need not invalidate semantic render state.
## Preview memory is policy-driven
Adobe's low-memory behavior has changed by version. For example, the 22.5/22.6-era preview warning logic could extend assigned RAM in order to cache a minimum number of frames rather than treating the preference limit as an absolute hard wall.

Therefore performance experiments must record AE version and actual process/memory-detail state, not only preference values.

## MFR changes the pressure shape
Multi-Frame Rendering increases the number of concurrent frame requests and therefore can multiply:
- input/output worlds;
- effect scratch buffers;
- decoded source frames;
- Compute Cache checkouts;
- GPU resources;
- render-snapshot/task metadata.

More frame concurrency is useful only while memory/residency pressure does not force destructive churn or swapping.

## Developer diagnostics
For each memory problem record:
1. semantic key / request identity;
2. current validity state;
3. resident representation and approximate bytes;
4. owner process/subsystem/device;
5. pin/receipt/guard lifetime;
6. pressure source;
7. purge or eviction trigger;
8. whether recomputation requires CPU, decode, disk I/O or GPU work.

A generic “clear the cache” diagnosis hides the subsystem that actually owns the bytes.

## Failure modes
- retaining host worlds/receipts longer than their documented lifetime;
- treating a Compute Cache receipt as permanent ownership;
- using process-global caches without memory-pressure integration;
- under-reporting Compute Cache value size and distorting host purge heuristics;
- diagnosing GPU OOM as ordinary host-RAM exhaustion;
- benchmarking MFR without accounting for memory churn/swapping;
- assuming another Adobe application's memory use is unrelated to AE.

## Unknown frontier
Exact global arbitration between BEE/cache residency, Adobe shared-memory balancing, MediaFoundation and GPU budgets is not public. AEIG keeps those policies separate until traces/pressure experiments establish coupling.

Cross-links: `runtime-architecture.md`, `../cache-system/cache-architecture.md`, `../mfr/overview.md`, `../gpu-system/overview.md`, `F-MEM-001`, `F-CACHE-013`, `F-CACHE-014`, `datasets/ae-2025-memory-pressure-symbols.csv`.