---
status: strongly-supported-cross-surface
last_verified: 2026-09-15
evidence: E0-G + E1-H + E2-L
versions: AE 24.4-26.5 public lineage + AE 2025 runtime
---
# F-MEM-001 — Memory pressure is a multi-domain feedback problem, not one RAM-cache threshold

Public AE history already distinguishes RAM-only purge from All Caches, while AE 2024 feature resources describe revised purge logic driven by OS memory footprint and by whether purge actions actually reclaimed pressure. The installed AE 2025 runtime exposes separate purge/residency primitives in MediaFoundation, GPUFoundation and BEE.

`MediaFoundation.dll` has `CacheGuard`, `GetManagedMemoryCache`, `MM::Purge(size, PurgeUrgency)`, managed disk-cache volumes and purgeable-support interfaces. `CacheGuard` couples a purgeable object with an amount/size, consistent with temporary residency protection or accounting while a consumer holds the resource.

`GPUFoundation.dll` separately exposes `AssetCache::Purge`, lazy-purge control and adapter-budget change callbacks. GPU residency can therefore react to device budget changes independently from ordinary host RAM pressure.

`BEE.dll` exposes `BEE_PurgeAllCaches` and `BEE_PurgeNonAECaches` alongside cached-frame WorkQueue checkouts and subsystem-specific caches. Compute Cache headers add another pressure-aware domain where plug-ins report approximate value size and the host chooses purge policy.

## Working control model
`pressure observation -> select reclaimable residency domain -> purge/evict -> measure reclaimed bytes/success -> adjust cadence/policy`.

The pressure observation itself may differ by domain: OS/process footprint, allocation rate, MediaCore memory demand and GPU adapter budget are all independently visible surfaces.

## Critical distinction
Semantic identity/validity, physical residency, pin/lease state and eviction policy are orthogonal. A frame can remain semantically valid while being evicted; a result can be resident but invalid; and a valid resident object can be temporarily non-purgeable while checked out or guarded.

Do not infer that `BEE_PurgeAllCaches` literally calls every lower-level purge primitive, nor infer purge ordering, until trace/behavioral evidence confirms it.

Reproduction: `probes/process-tools/inventory_memory_pressure_symbols.py` -> `datasets/ae-2025-memory-pressure-symbols.csv`.
