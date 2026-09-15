---
status: active
last_verified: 2026-09-16
evidence: current Adobe memory-pool/cache behavior + Compute Cache contracts + local MediaFoundation/GPU/BEE pressure surfaces
---
# Memory Pressure and Residency Architecture

AEIG separates memory management from cache semantics. The runtime contains several residency domains with distinct pressure signals and purge controls.

```text
OS/process footprint   allocation rate   GPU adapter budget
        \                  |                  /
         \                 |                 /
          +------ pressure observations -----+
                         |
                         v
               domain-specific policy
          /              |               \
 MediaFoundation      BEE/cache        GPU AssetCache
 memory/data cache    residency        device residency
          \              |               /
           +---- purge / evict action ---+
                         |
                         v
             reclaimed size / success
                         |
                         +----> next cadence/policy
```
## MediaFoundation residency
`CacheGuard` and `UIPurgeableSupport` expose a lease-like boundary around reclaimable media objects. Managed memory caches, DataCache chains and disk-cache volumes should be treated as different stores even when one logical media request can move through several of them.

## GPU residency
`GPUFoundation::AssetCache` has its own purge and lazy-purge surfaces. Adapter-budget change callbacks provide an external pressure signal from the graphics device/OS. GPU memory exhaustion can therefore require different diagnostics from host-memory pressure.

## AE/BEE residency
BEE owns frame/work-queue and feature-specific caches and exposes broad purge entry points. These coexist with public Compute Cache leases and with media/GPU caches; the user-facing word "cache" does not identify one allocation pool.

## Research rule
For every memory-owning subsystem record:
1. semantic key and validity;
2. resident representation and byte footprint;
3. owner/process/device;
4. pin/checkout/guard lifetime;
5. pressure signal;
6. purge/eviction policy;
7. persistence across process/session boundaries.

Next experiments should correlate OS private bytes/working set, GPU budget, MediaCore allocations and purge traces under controlled pressure. Primary evidence: `F-MEM-001` and `datasets/ae-2025-memory-pressure-symbols.csv`.

## Application-level shared memory pool
Current Adobe documentation still describes `RAM reserved for other applications` as controlling memory available to After Effects and applications that share its memory pool, independently of whether MFR is enabled. Historical Adobe documentation exposed the underlying policy more explicitly: participating applications register minimum/maximum/current usage and priority with a memory balancer intended to avoid OS swapping.

AEIG treats the historical balancer details as architectural lineage, not a promise that 26.x uses the identical scheduler. The current observable contract is that AE does not own all available RAM in isolation.

Consequences:
- foreground/background Adobe applications can change effective host-memory pressure without any project edit;
- Media Encoder/Premiere-hosted AE rendering can compete inside the shared Adobe allocation domain;
- MFR worker admission is constrained by usable memory as well as CPU availability;
- OS free-memory alone is not a complete predictor of AE cache residency.

## Residency is not validity
A render result can remain semantically valid after its resident pixels are purged. Recomputing a purged value is a residency miss, not necessarily an identity/invalidation event.

Keep these states separate:

`semantic key -> validity -> resident representation -> pin/lease state -> eviction priority -> persistence tier`.

This distinction is essential when analyzing why AE recomputed something: the key may be unchanged while the bytes were simply evicted.

## Compute Cache pinning and purge policy
Public Compute Cache makes lifetime explicit. A checked-out cache value is accessed through a receipt; entries can be purged when memory is needed, and `approx_size_value()` feeds the host's purge heuristic. Cache contents are not project-persistent and must be treated as recomputable.

`delete_compute_value()` owns destruction of all resources attached to the cached value. The host only stores the opaque pointer and cannot release nested allocations on the effect's behalf.

This produces a clean design rule: cache identity/compute logic and resource ownership/destruction must be explicit and symmetric.

## Failure modes by residency domain
### Host/shared RAM
- reserve too little for OS/other apps -> paging and global slowdown;
- retain large plug-in allocations outside host-aware cache systems -> pressure invisible to host eviction policy;
- assume warm RAM cache will survive another Adobe application's load -> brittle performance.

### Compute Cache
- inaccurate `approx_size_value` -> poor purge decisions;
- rely on entry always existing -> correctness failure after purge/reopen;
- leak resources in `delete_compute_value` -> pressure grows even as host thinks entries were removed;
- hold receipts longer than needed -> reduce reclaimability.

### Media/cache guards
- retain media guards/leases indefinitely -> decode/media cache cannot reclaim memory;
- double-cache same decoded representation in plug-in state -> duplicate residency across domains.

### GPU
- treat VRAM pressure as ordinary host-RAM pressure -> wrong diagnostics;
- keep stale device assets across adapter/device reset -> invalid resources;
- trigger repeated upload/download because CPU/GPU residency state is not tracked separately -> performance collapse without semantic invalidation.

## Pressure experiment matrix
Use a deterministic heavy comp and vary one pressure source at a time:
1. cold versus warm AE RAM cache;
2. another shared-pool Adobe application idle versus actively allocating;
3. Compute Cache value sizes and checkout lifetimes;
4. media decode cache warm/cold;
5. GPU memory pressure from device-resident frames/textures;
6. MFR worker count/resource pressure;
7. explicit Purge versus passive eviction;
8. host restart versus project reopen.

Record OS private bytes/working set, AE Memory Details, GPU budget, relevant cache file activity, Compute Cache compute/delete callbacks, BEE/MediaFoundation/GPU trace activity and output hashes.

The objective is to classify every recomputation as one of: semantic invalidation, ordinary eviction, backend migration, device reset, process/session boundary or explicit purge.

## Version boundary
Historical Global Performance Cache terminology, current disk-backed preview, MFR-era memory admission and modern GPU/AI caches should not be projected backward or forward as one unchanged implementation. Record host version for every pressure observation.

## Unknown frontier
Still unresolved:
- current 26.x application memory-balancer algorithm and priorities;
- exact admission policy that converts RAM pressure into MFR concurrency changes;
- coordination, if any, between BEE frame residency and MediaFoundation/GPU eviction heuristics;
- whether disk-backed preview acts as a spill tier chosen directly by memory pressure or by a separate preview/cache policy;
- how AI-analysis/result caches participate in global pressure accounting;
- precise device-budget thresholds and hysteresis for GPU asset purge.

Related: `docs/memory-system/overview.md`, `docs/cache-system/disk-cache.md`, `docs/cache-system/compute-cache.md`, `docs/gpu-system/overview.md`, `docs/media-system/overview.md`.
