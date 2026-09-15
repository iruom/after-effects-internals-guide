---
status: active
last_verified: 2026-09-15
evidence: versioned headers, retained preferences/debug-trace profiles, product/runtime archaeology
---
# Architecture Timeline

AEIG uses architectural eras so evidence is never projected across incompatible generations without a version bridge.

- **AE 9 era:** retained vocabulary already exposes SmartFX stack/time comparison, stream-path caching and sequence-data lifecycle concepts.
- **CS6 / AE 11:** Global Performance Cache-era contracts strengthen temporal/state comparison and cache invalidation; historical thread ceilings and compile-time gates are visible in headers.
- **CC2014 / AE 13.0:** the recovered header corpus already contains CanvasSuite8, LayerRenderOptions/effect-prefix request surfaces, bicubic layer sampling, plug-in path discovery and Drawbot. The three-point SDK lineage records 468 identifiers introduced by this point and retained into 25.6.
- **CC 2015 / 13.5:** Adobe-described complete re-architecture separates editable/UI state from render-side copies and changes threading assumptions.
- **14.0→16.0:** the official Guide records Effect API `13.13→13.16`; AEGP `114.0` is explicitly recorded for 14.0. This official-doc lineage bridges missing distributed-header snapshots but does not prove per-suite ABI.
- **17.x→18.2:** Effect API advances `13.18→13.25` across the Guide's version table while individual suites continue on independent generation/PICA tracks.
- **17.5+ / 2020 era:** public Hash/Compute-related identity surfaces begin to expose more host-compatible state/cache primitives; the Guide Git history adds explicit MFR documentation in June 2020.
- **22.x:** modern Multi-Frame Rendering makes frame-level concurrency, sequence ownership and host-callback locking explicit plug-in concerns; the official table records Effect API `13.27` for 22.0.
- **25.2+:** disk-oriented preview/playback becomes a distinct residency architecture line.
- **25.6→26.x:** Guide/runtime gaps, AI-analysis growth, compressed disk playback and continuing internal ABI drift are directly observable.

## Rule
A similar name across eras is continuity evidence, not proof of unchanged implementation or ABI.

Every historical claim should carry a version range and evidence source. Removed identifiers are classified as removed, renamed, folded, gate-lifted or repurposed where possible rather than treated as simple deletion.

Machine-readable API, SDK-lineage and Debug/Trace datasets provide the detailed chronology behind this page. See `datasets/ae-sdk-lineage-cs6-cc2014-25_6.csv` and `F-ABI-016-cc2014-transitional-api-surface.md`.
## Failure patterns in historical reconstruction
The same symbol can survive while ownership, threading or semantics change; a removed key can reflect ungating/renaming rather than feature removal. Product release notes can also describe user-visible change later than the underlying substrate first appeared.

A common archaeology error is to infer an introduction date from the first archive AEIG happens to possess. Treat every corpus gap as censored observation, not absence.

## Boundary experiments
Where two runnable host generations are available, use identical minimal projects/plug-ins and compare suite acquisition, callback/thread pattern, persistence bytes, trace categories and output hash. Change one API-era feature at a time instead of comparing large production projects.

For historical cache/threading claims, reproduce A→B→A state changes under each host and compare reuse/callback behavior rather than relying only on names in old headers.

## Unknown frontier
Direct distributed SDK coverage remains incomplete for portions of 11.x→23.x. Private BEE/TDB/RG introduction dates are bounded by retained binaries/traces but not fully pinned to releases. Some Adobe-wide substrate changes can precede AE product exposure.

Related: `docs/foundations/version-model.md`, `docs/reference/version-matrix.md`, `docs/host-integration/cpp-sdk/sdk-distribution-archaeology.md`, `datasets/ae-sdk-lineage-cs6-cc2014-25_6.csv`.
