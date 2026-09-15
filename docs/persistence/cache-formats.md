---
status: active
last_verified: 2026-09-15
evidence: filesystem/runtime cache archaeology across render/media/analysis subsystems
---
# Cache Formats

AEIG separates on-disk caches by semantic owner. A single "Adobe cache" model is too coarse for After Effects.

Observed or documented domains include render/disk playback storage, MediaFoundation/media caches, importer-side frame caches, Compute Cache data, AI-analysis persistence and feature-specific stores.

## Investigation method
Use controlled fixture changes, cache purge boundaries and file-I/O tracing to determine which store reacts to which semantic mutation.

Record for every observed file or directory:
- producer process/module;
- host version;
- creation/update trigger;
- key/path vocabulary;
- whether data survives restart;
- whether deletion affects correctness or only reuse/performance.

## Identity rule
A filesystem key is not automatically the same identity as a BEE RenderGuid, Media `DocumentID/ContentState`, Compute Cache GUID or Canvas Receipt. Correlate before equating them.

## Safety
Treat caches as disposable implementation artifacts unless a public API states otherwise. Reverse engineering should prefer read-only inspection and copies of files from disposable profiles.

Related pages: `cache-system/disk-cache.md`, media runtime architecture, Object Matte persistence findings.## Failure modes
Cache archaeology is vulnerable to false attribution. Temporary files may be prefetch, metadata, database journals or unrelated Adobe shared-media state rather than frame payloads. A file timestamp changing with a render is correlation only.

Compression/container changes can also make byte-level diffs look like semantic invalidation when only residency representation changed. Conversely, a stable filename can point to replaced content behind an index/database entry.

Deleting caches during research may force recomputation and alter timing without changing semantics; that difference must be recorded rather than treated as a bug.

## Unknown frontier
AEIG does not yet equate any private disk filename/index with BEE/RG render GUIDs. The exact current compressed-frame container/index, Object Matte disk record and MediaCore database schema remain versioned reconstruction targets.

## Cross-links
See `../cache-system/disk-cache.md`, `../archaeology/disk-playback-era.md`, `../media-system/runtime-architecture.md`, `../ai-analysis/overview.md`, and `../memory-system/runtime-architecture.md`.

A future parser should be validated by controlled cache creation/lookup/eviction behavior, not merely by successfully decoding bytes.
## Cross-links
See `docs/cache-system/disk-cache.md`, `docs/archaeology/disk-playback-era.md`, `docs/media-system/runtime-architecture.md`, `docs/ai-analysis/overview.md`, `docs/memory-system/runtime-architecture.md`, and `docs/reference/bug-quirk-registry.md`.
