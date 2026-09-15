---
status: active
last_verified: 2026-09-16
evidence: historical/current Adobe preview-cache documentation + 25.x/26.x preference lineage + known issues
---
# Disk Playback Era: From Persistent Cache to Active Preview Residency

After Effects' disk cache changed architectural role over time. Old descriptions and current behavior must not be merged into one timeless model.

## Earlier Global Performance Cache model
CS/CC-era Adobe documentation described Global RAM Cache and Persistent Disk Cache as distinct tiers. Cached disk frames survived application closure, but the documentation explicitly stated that disk cache was **not used for real-time preview playback** in the way RAM preview was.

That older rule is historically useful, not a current universal truth.

## Current high-performance preview model
Current Adobe preview documentation says AE can play previews from disk cache instead of requiring every rendered frame to fit in RAM. Cache indicators distinguish disk-resident blue frames from RAM-resident green frames, and AE can cycle between disk and memory as needed.

This is an architectural transition:

`disk as persistent backing/reuse -> disk as an active preview residency/playback tier`.## Lossless compressed cached frames
AE 2026 adds/advertises lossless compressed playback storage: cached frames are compressed in the background, remain visually lossless, consume less disk space and allow longer preview spans within the disk-cache limit.

Compression is a **residency representation** question. It should not be equated with a new render-result identity unless evidence shows the cache key itself changed.

## Known 26.0/26.2 failure
Adobe's current Known Issues page records crashes in After Effects 26.0 and 26.2 with Compressed Disk Caching enabled for some projects/hardware, with disabling lossless compressed frames as the workaround.

This is a useful real-world example of why AEIG separates:

`semantic frame validity -> cached representation -> compression/decompression implementation -> playback residency`.

A crash in the storage/playback tier does not by itself imply wrong render identity or wrong effect output.

## Other disk-backed domains
Do not merge preview frames with conformed media/database caches, importer/media caches, Object Matte disk persistence or arbitrary analysis artifacts merely because all are on disk. Current Preferences exposes separate media-cache database/cache controls, while Object Matte 26.5 has its own cross-project-close disk persistence behavior.## Experiments
Use deterministic rendered frames and trace RAM/disk state while varying only preview length, disk-cache limit, compressed-frame setting and host restart. Record file creation, readback, CPU/GPU transfer, output hashes and cache indicators.

Test a warm disk-resident frame after RAM pressure, after AE restart, after a reversible project edit and after a true render-relevant mutation. This distinguishes persistence/residency from semantic validity.

## Unknown frontier
The exact on-disk index/key relationship to BEE Render GUIDs/RG cache identity remains unproven. Likewise, current compression format/container details are implementation artifacts until directly reconstructed.

A filesystem filename, blue cache bar or compressed blob is not sufficient to name the internal semantic key.

## Version rule
Any claim about “disk cache behavior” must name the AE generation. Documentation from the older Global Performance Cache era can be correct for its time and simultaneously wrong for current high-performance preview playback.

Cross-links: `../cache-system/disk-cache.md`, `../memory-system/overview.md`, `../persistence/cache-formats.md`, and `../ai-analysis/overview.md`.