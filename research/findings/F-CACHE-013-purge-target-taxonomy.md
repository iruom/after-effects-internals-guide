---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G scripting/fixed-issue history
---
# F-CACHE-013 — AE distinguishes all-cache purge from RAM-only purge

Adobe's 24.4 fixed issues state that `app.purge(PurgeTarget.ALL_CACHES)` was corrected to match Edit > Purge > All Caches, and a separate `PurgeTarget.ALL_MEMORY_CACHES` was added for RAM-only clearing.

## Architectural consequence
'Cache' is not synonymous with the in-memory frame cache. The scripting surface now explicitly separates a global/all-cache operation from a memory-only cache operation.

The 26.5 UI also names Disk Cache, 3D Cache and All Caches as separately purgeable domains. Treat these names as cache-policy surfaces, not proof that each corresponds to one physical store.

## Diagnostic use
A bug that survives `ALL_MEMORY_CACHES` but disappears after `ALL_CACHES` is evidence against a purely RAM-resident stale result and should redirect investigation toward disk, media, 3D, analysis or other persistent cache domains.
