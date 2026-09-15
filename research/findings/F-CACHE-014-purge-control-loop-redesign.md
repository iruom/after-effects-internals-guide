---
status: confirmed-local-feature-surface
last_verified: 2026-09-15
---
# F-CACHE-014 — AE 2024 exposes a purge-control redesign using OS memory footprint

AE 2024 localization resources contain two Beta features relevant to memory pressure. ImprovedMCPurge describes increasing the MediaCore purge rate to keep pace with high allocation rates. RevisedPurge describes using memory footprint from OS counters, unifying success checks across purge procedures, and applying multiple fixes to purge logic.

## Internal implication
Purge is not merely a user command that empties caches. AE has an adaptive memory-pressure subsystem whose behavior can depend on allocation rate, measured process/system footprint, and whether previous purge actions actually reduced pressure. This is consistent with later Debug Database keys such as MF.MemoryControlLoopActive and AE.PurgeFrequencyMillisec.

## Diagnostic implication
Memory failures should distinguish allocator pressure, cache residency, purge cadence, purge effectiveness, and external/OS footprint. A high cache hit rate can still be unhealthy if residency policy cannot react quickly enough to allocation bursts.

## Research action
Correlate memory-allocation bursts with purge traces and OS working-set/private-byte counters; compare 24.x/25.x/26.x debug keys; force distinct RAM/GPU/media-cache pressure and observe which purge domains respond.
