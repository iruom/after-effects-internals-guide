---
status: active
last_verified: 2026-09-16
evidence: Premiere PrSDKMemoryManagerSuite contract + AE memory/cache architecture comparison
---
# Premiere Memory-Management Analogs

Premiere's `PrSDKMemoryManagerSuite` is useful sibling-host evidence because it makes several cache/residency concepts explicit that AE often exposes only indirectly.

Do **not** infer AE implements this exact suite internally. Use it to separate generic host-memory concerns that any large Adobe compositor/editor must solve.

## Reserved budget vs purgeable residency
Premiere separates:
- memory reserved/attributed to a plug-in;
- ordinary allocations;
- blocks registered with the host as purgeable managed memory.

This is a strong conceptual analogue for AEIG's distinction between **allocation ownership** and **cache residency policy**.

A block can belong to a plug-in while the host is allowed to reclaim it under pressure.

## One block, one cache owner
`AddBlock()` requires that the same bytes are not already represented in another suite cache. This prevents double-accounting and conflicting purge ownership.
The same design principle should be applied when analyzing AE: a frame in RAM, a GPU asset, a MediaFoundation frame and a Compute Cache value must not be treated as four references to one purgeable object unless ownership proves it.

## Recency/priority is explicit
Premiere's `TouchBlock()` raises a managed block's effective priority/recency so it is less likely to be purged. The exact eviction algorithm is private, but the contract proves that **recent use is distinct from mere existence**.

This is useful when reasoning about AE preview/cache behavior: a resident value can have policy state beyond valid/invalid.

## Purge callback threading
Adobe documents that the purge callback may run on any thread. Destruction and cache-removal code must therefore be thread-safe and independent of UI-thread-only services.

`RemoveBlock()` is different: deregistering a block manually does not invoke the purge callback. Host eviction and owner-initiated removal are separate lifecycle transitions.

## Cross-host mapping questions
Use this suite to ask, not answer, AE-side questions:
- what AE object is purgeable versus pinned?
- where is recency/priority recorded?
- which subsystem owns destruction?
- can purge happen from arbitrary worker threads?
- how is one byte range prevented from being double-accounted across caches?
- what is the equivalent of manual deregistration versus pressure eviction?
## AE comparison
AE exposes different public/private mechanisms:
- AEGP Compute Cache receipts and size reporting;
- PF/AE world lifetimes;
- MediaFoundation guards/data caches;
- GPUFoundation asset residency;
- BEE/cache purge paths;
- Adobe shared-application memory balancing.

The design concern is shared; the concrete API is not.

## Failure modes
- registering the same storage with two independent cache owners;
- assuming host eviction invokes the same path as explicit removal;
- touching/using a block without updating recency metadata where required;
- performing UI-only work from a purge callback;
- retaining dangling pointers after host-driven purge;
- importing Premiere's exact lifetime rules into AE without AE evidence.

## Experiment transfer
A useful AE experiment inspired by the Premiere contract is to tag one resident artifact, exercise it repeatedly versus leave another idle, then induce controlled memory pressure and observe which survives. The experiment can test for recency-sensitive policy without assuming Premiere's implementation.

Cross-links: `../../memory-system/overview.md`, `../../memory-system/runtime-architecture.md`, `opaque-effect-data.md`, `../../foundations/cross-host-triangulation.md`.