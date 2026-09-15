---
status: active
last_verified: 2026-09-14
---
# Cache Architecture

Do not model AE as having one cache. Current research tracks at least:
1. property/expression caches
2. render-state / GUID identity
3. SmartFX/per-node caches
4. RAM frame cache
5. persistent disk frame cache
6. playback-from-disk storage
7. Compute Cache
8. media/decode caches
9. GPU host/device asset caches
10. bounds/vector caches
11. feature-specific persistent caches

Each must be characterized by key, scope, owner, lifetime, invalidation and storage representation.

## Historical architectural evidence: interval-list validation
Adobe patent US7103839B1 is highly relevant because its inventors, Michael Natkin and David Simons, are documented After Effects designers/developers. It describes cached-frame validation over a compositing tree using edit-order timestamps and per-node temporal interval lists.

Important properties of that design:
- edit time and composition time are separate axes;
- a frame carries the edit-state timestamp at which it was rendered;
- each node can maintain multiple interval lists for different edit classes;
- validity is checked recursively at demand time;
- motion blur expands the queried interval;
- collateral expression/layer dependencies can add non-tree dependencies;
- the system deliberately permits conservative false invalidation, never false validity.

This should be treated as **historical architecture evidence**, not proof of the exact AE 26.x implementation. It provides concrete hypotheses to test against `BEE_Cache`, `MixHashGuid`, PF_State, frame receipts and modern Global Performance Cache behavior.

## Complexity / design analysis
An interval-list implementation can update by splitting/merging temporal segments and query endpoints by binary search, then inspect intersecting segments. This is memory-efficient when edits form long constant-state intervals, but pathological animation/edit patterns can fragment the list.

Potential modern alternatives include persistent segment trees, interval trees, typed version vectors, Merkle/content fingerprints or hybrid temporal dependency summaries. AEIG should compare these approaches rather than assuming Adobe's historical representation remains optimal.

## Sources
- https://patents.google.com/patent/US7103839B1
- https://ae-plugins.docsforadobe.dev/effect-details/parameter-supervision/
- https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/

## Additional cache/residency domains
Research now separates at least three additional concepts from ordinary frame caches:
- **analysis-result cache** — e.g. Object Matte/Roto propagation outputs; 26.5 makes Object Matte results disk-persistent across sessions.
- **ML model registry/residency** — model identity, delivery bundle and runtime residency; this is input capability state, not analysis-result storage.
- **purge-control loop** — policy deciding when/how aggressively memory/cache domains are reclaimed under pressure.

## Purge as a feedback controller
AE 2024 Beta resources describe ImprovedMCPurge as increasing MediaCore purge rate to keep pace with high allocation rates. RevisedPurge describes using memory footprint from OS counters, unifying success checks across purge procedures, and fixing purge behavior. Modern Debug Database keys such as MF.MemoryControlLoopActive and AE.PurgeFrequencyMillisec are consistent with an explicit control-loop architecture.

The useful model is therefore not cache -> purge when full, but pressure measurement -> purge-domain selection -> purge action -> success/footprint feedback -> next cadence. Identity and validity can remain correct while residency policy fails to respond fast enough, producing memory instability without semantic cache corruption.

## Cross-domain rule
For every cache-like structure record four orthogonal properties: semantic identity, validity/invalidation, physical residency/lifetime, and pressure/eviction policy. A result can be semantically valid but non-resident; resident but stale; or expensive enough to retain despite size.
