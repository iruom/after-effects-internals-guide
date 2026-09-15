---
status: active
last_verified: 2026-09-15
---
# Headless and Command-Line Host

Headless rendering is a separate observation surface for determining which AE services are intrinsic to project/render execution and which require the interactive application shell.

## Scope
`aerender`; headless plug-in loading; render queue execution; environment/preferences; licensing/startup boundaries; deterministic automation.

## Questions
- Which plug-ins/suites are loaded or omitted in headless mode?
- Does headless execution construct the same render-side project state and cache identities?
- Which UI-dependent callbacks fail, return sentinel state or are never invoked?
- Are RAM/disk/media caches shared with interactive AE?
- Which environment variables/preferences alter concurrency, GPU selection and media services?
- Can identical projects produce byte-identical or pixel-identical output across interactive/headless paths?

## Evidence surfaces
`aerender` CLI; HeadlessPlugin Loading logs; process/module inventory; SDK host checks; environment capture; render hashes; trace/debug databases.

Headless comparison should become a standard differential axis for AE Observatory experiments.

## Current host model
Installed 25.6 evidence shows `aerender.exe` as a controller/launcher: it either starts a new After Effects instance or asks an already-running AE instance to render with `-reuse`. The underlying render owner is therefore an AE host instance rather than a separately linked aerender engine.

This sharpens the differential question: compare **fresh render-host mode**, **reused interactive-host mode**, and ordinary interactive rendering while controlling cache warmth, preferences, plug-in/module load, MFR, CPU limits and GPU state.

See `runtime-architecture.md`, `research/findings/F-HEADLESS-001-aerender-is-a-controller-for-ae-host.md`, and `datasets/ae-2025-headless-entrypoint.csv`.

## Version-sensitive execution modes
Fresh aerender-launched AE and `-reuse` are distinct process-lifetime modes. `-reuse` delegates to an already-running host, inheriting its warm modules/caches/global state, and Adobe documents different preference-write behavior on completion.

`-mfr` and `-mem_usage` further alter scheduler/resource policy. A headless benchmark without recording these flags is not a reproducible host environment.

## Unknown frontier
Still unresolved: exact IPC used by `-reuse`; which UI-shell services remain initialized in render-engine/headless contexts; cache partitioning between reused/fresh hosts; renderer/GPU-device selection equivalence; licensing/service startup differences across platforms.

Headless parity must be proven per subsystem. A feature can render correctly in interactive AE while failing in aerender because analysis/UI/runtime initialization crosses an unsupported boundary, as historical Object Matte failures demonstrated.

Related: `docs/headless-system/runtime-architecture.md`, `docs/troubleshooting/failure-model.md`, `F-HEADLESS-001-aerender-is-a-controller-for-ae-host.md`, `F-AI-001-object-matte-headless-boundary.md`.
