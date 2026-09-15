---
status: active
last_verified: 2026-09-16
---
# Debug Database

`Debug Database.txt` is a locally retained After Effects implementation artifact containing internal switches, constants, feature experiments and subsystem tuning values. It is one of AEIG's most useful **vocabulary and lineage** sources, but it is not a public configuration API and a key's presence does not make changing it supported or safe.

The normalized corpus is combined with Trace Database material in `datasets/ae-debug-trace-vocabulary.csv`. The current retained vocabulary contains more than ten thousand versioned rows across stable and beta profiles; `datasets/ae-debug-trace-lineage.csv` collapses repeated names into first/last-seen and value/default variants.

## What the file can prove

A persistent debug key can provide strong evidence that a subsystem, optimization or implementation concern exists in the host. Names such as `AE.VectorBoundsCache`, `Expressions.RecycleEnginesAggressively`, `CacheTimeInvariantExpressionValues`, `Expressions.CacheSubProperties`, `MFDiskCacheManager.DiskSweepInterval` and `GPUKernels.GPUMemoryReserve` reveal concerns that are often invisible in the public SDK.

The strongest interpretation is structural: the host has code paths that consult or register vocabulary for those concerns. The file alone does **not** prove when a path executes, whether a key is still wired to live code, or whether changing a value is equivalent to a supported preference.

## Version lineage matters

Many keys survive across multiple releases. For example, the retained profiles show `AE.VectorBoundsCache`, `TransformEffectNumSamples`, expression-cache switches and `AE.DisableGlobalPreProcessorR` recurring from 23.x-era profiles through locally retained 26.3 material. Other names appear only in beta or in a narrow release range.

This makes version-diffing more valuable than reading one file in isolation. A newly appearing key can indicate a new implementation path or experiment; a disappearing key can mean removal, rename, compile-time retirement or migration elsewhere. None of those possibilities should be collapsed without additional evidence.
## Useful implementation clusters

The database is especially valuable when names are interpreted in families rather than individually:

- **cache/evaluation:** time-invariant expression caching, sub-property caching, vector bounds caching, disk-cache sweep policy;
- **expressions:** engine recycling, preprocessing/caching behavior and internal engine policy;
- **GPU/3D:** GPU memory reserve, adaptive quality and renderer-specific controls;
- **sampling/rendering:** transform sample counts and other quality/performance constants;
- **feature gates:** beta or experimental switches that can reveal hidden development branches before they are public product surfaces.

These clusters should be correlated with public behavior, runtime symbols, traces, preferences and controlled experiments. A suggestive name is a research lead, not a semantic conclusion.

## Developer and reverse-engineering use

For plug-in developers, the most useful role of Debug Database is hypothesis generation. If a host-only failure appears around expression reuse, bounds, disk cache, GPU memory or adaptive rendering, the vocabulary can identify internal dimensions worth testing even when no SDK call exposes them directly.

A good workflow is:

`observed symptom -> find related debug/trace vocabulary -> check version lineage -> locate SDK/runtime surfaces -> construct minimal fixture -> confirm or falsify behavior`

This is safer and more informative than blindly toggling undocumented keys. AEIG should prefer observation and differential testing over mutation of a user's normal profile.

## Failure modes and traps

- **Dead-key trap:** a retained key can survive after the underlying code path has changed or disappeared.
- **Default-value trap:** a textual default does not prove that every launch/context uses that value.
- **Beta/stable trap:** a beta key may never ship, or may ship under a different mechanism.
- **causality trap:** a key name that resembles a bug symptom does not establish that subsystem as the cause.
- **profile contamination:** changing internal switches can alter later experiments and make results non-reproducible.

For reproducible work, record the AE version/profile, preserve the original file, and isolate experiments from production preferences.
## Relationship to Trace Database

Debug Database and Trace Database answer different questions. Debug keys expose implementation switches/constants; trace categories expose observable runtime channels. When both exist for the same conceptual area, they form a stronger experiment surface: the debug vocabulary suggests a mechanism and the trace vocabulary can show whether activity changes under a controlled operation.

Do not assume their ABIs are stable. The locally studied dvacore trace category-volume signature changed between 25.6 and 26.3 even though category names remained recognizable. See `docs/observability/trace-database.md`.

## Evidence discipline

AEIG classifies these names as hidden diagnostic/implementation evidence. They should never be copied into a public API table merely because they are readable. A statement such as "AE has a `GPUKernels.GPUMemoryReserve` debug key" is directly evidenced; a statement such as "setting it to N guarantees N MB of usable GPU memory" requires a separate behavioral experiment.

## Open research

High-value next work includes grouping all keys by subsystem and version, correlating changed defaults with release behavior, identifying keys that map to exported symbols or preferences, and constructing disposable-profile experiments for a small set of high-value switches. Results should record both positive and negative observations so dead or context-gated keys remain visible as such.

Related machine-readable sources:

- `datasets/ae-debug-trace-vocabulary.csv`
- `datasets/ae-debug-trace-lineage.csv`

Related pages: `docs/observability/trace-database.md`, `docs/cache-system/disk-cache.md`, `docs/cache-system/expression-cache.md`, and `docs/gpu-system/overview.md`.
