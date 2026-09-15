---
status: active
last_verified: 2026-09-16
evidence: current/historical Adobe cache documentation + local Debug Database/preferences + AEIG cache findings
---
# Disk Cache

"Disk cache" in After Effects is not one universal database. AEIG separates render-result persistence, preview/playback storage, media conform/index caches and feature-specific analysis stores because they can have different keys, formats, lifetimes and purge rules.

## Global performance cache
Adobe's global performance cache historically combines RAM image caching with persistent disk-backed rendered frames. RAM entries can survive edits and be reused after undo/restoring earlier state; disk-cached frames can survive application restart and be discovered when projects are reopened.

The important architectural point is **semantic reuse across project/session boundaries**. A file sitting on disk is not enough: AE must find an entry whose stored identity still matches the requested render state.

Blue cache indicators represent disk-cached frames; green indicators represent RAM-resident frames. Layer cache indicators expose another level of reuse below the whole-composition view.

## Modern preview-from-disk path
Current AE documentation exposes direct preview from disk cache so playback is no longer limited solely by available RAM. Frames can cycle between memory and disk during preview. This is a meaningful product/runtime evolution and should not be projected backward onto every historical release.

Current preferences separately expose `Enable Preview from Disk Cache` behavior rather than making disk residency synonymous with one historical preview model.

## Lossless compressed playback era
By 2026 Adobe documents lossless compression of cached preview frames stored on disk. The goal is longer timeline playback within the same disk budget without changing pixel fidelity. This adds another representation layer:

`render identity -> uncompressed logical frame -> compressed disk representation -> decompressed playback residency`.

Compression is therefore a storage/materialization property, not a new semantic frame identity by itself.

## Media cache is a different subsystem
Imported audio/video can create conform/index artifacts such as `.cfa` and `.mpgindex` files. Current preferences also distinguish optimized media cache database/index locations from ordinary disk cache storage.

Do not purge or reason about MediaCore/importer caches as though they were composition-frame cache files. Source-media identity and downstream composition identity can invalidate independently.

## Internal/local observability
Local Debug Database/preferences include `MFDiskCacheManager.DiskSweepInterval`, free-space controls and disk-playback/cache switches. These names demonstrate separate management policy but do not by themselves reveal the complete on-disk schema or eviction algorithm.

AEIG also keeps Roto Brush/Object Matte/analysis caches separate where evidence indicates feature-specific persistence or GUID state.

## Correctness model
Keep these axes separate:

`semantic identity -> validity/sufficiency -> materialized representation -> residency -> eviction/purge policy`

File existence proves only residency. It does not prove the artifact belongs to the current project state, requested time, resolution, color/pixel semantics, renderer or implementation generation.

## Failure modes
Typical cache problems include stale reuse after a missing dependency, cache thrash from over-broad invalidation, corruption/interrupted writes, insufficient free-space policy, version migration that cannot reuse old entries, and performance regressions caused by moving cache to slow or contended storage.

Do not diagnose every blue/green indicator mismatch as an invalidation bug; playback residency, disk scan progress and layer-level cache state can differ from full-composition availability.

## Experiments
For one deterministic fixture, vary one semantic dependency at a time while recording RAM/disk indicators, output hashes, cache directory changes, Debug/Trace categories and restart behavior. Repeat before/after AE version upgrades and with compressed playback toggled to separate logical identity from disk representation.

## Evidence and cross-links
External evidence: Adobe `Memory and storage`, preview and Lossless Compressed Playback documentation. Local evidence: Debug/Trace vocabulary and preference inventories.

Related: `cache-architecture.md`, `state-identity.md`, `../persistence/cache-formats.md`, `../archaeology/disk-playback-era.md`, `F-CACHE-002`, `F-CACHE-013`, `F-CACHE-014`.

## Unknown frontier
Exact current cache-file formats, key serialization, cross-version compatibility and private eviction weights are not fully reconstructed. AEIG records observed formats/keys separately and does not infer them from UI cache indicators alone.
