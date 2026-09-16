---
status: active
last_verified: 2026-09-16
evidence: current Adobe aerender documentation + AEIG headless/runtime inventories
---
# Choose Fresh vs Reused Headless Host State

`aerender` has two materially different host-lifecycle modes. By default it starts a new After Effects instance even when AE is already running. With `-reuse`, it asks an already-running AE instance to perform the render.

Treat these as different execution environments, not interchangeable launch optimizations.

## Fresh host
A default aerender launch creates a new AE process for the render and tells that process to quit when rendering finishes. This gives the cleanest process-lifetime boundary for experiments: module initialization, process-local caches, static plug-in state and host startup all begin in the new process.

Adobe documents that preferences are not written on quit in this fresh aerender-owned path.

## `-reuse`
With `-reuse`, aerender uses the currently running AE instance when available. That instance is not terminated when the render finishes, so loaded modules, process-local caches, allocator state, previous scripts/extensions and other host-lifetime state can survive into the job.

Adobe also documents different preference persistence: preferences are written when the reused AE eventually quits. That alone is enough to make fresh/reuse runs non-equivalent for strict reproducibility.

## What must be recorded
For automation, record at least AE version/build, command line, fresh vs reuse mode, project hash/path, render-setting/output-module templates, plug-in set, GPU/renderer state, relevant preferences, environment variables and whether an interactive AE process pre-existed.

Do not report a cache-speed comparison without separating cold-process startup from warm-process reuse. Likewise, a plug-in that appears to "load only sometimes" may actually be crossing host-mode or already-loaded-module boundaries.

## Capability boundary
Headless rendering does not imply that every interactive extension plane is present. UI panels, menu integrations, CEP/UXP surfaces, some AEGP behaviors and first-party UI services may have different loading or availability in a render-oriented host context.

Probe the capability you need in the actual target mode. Do not infer headless support from the fact that the same binary works in an interactive session.

## Determinism and contamination tests
Run the same project in four conditions where practical: fresh process first run, fresh process repeated run, reused process after unrelated work, and reused process after a prior render of the same project. Compare output hashes, startup logs, module inventories, cache hit behavior and timing separately.

If only reuse fails, inspect stale process state. If only fresh fails, inspect initialization/order assumptions. If outputs differ but timings do not, investigate nondeterministic state rather than cache warmth alone.

## Failure modes
Typical mistakes are benchmarking warm reused state against cold fresh state, depending on initialization side effects from an interactive session, assuming preferences are persisted identically, leaving process-global plug-in state dirty between jobs, or using `-reuse` in a render farm where isolation was expected.

For CI/render-farm correctness, fresh-process execution is usually the cleaner baseline. Reuse is appropriate only when its retained-state semantics are explicitly part of the deployment design and are tested as such.

## Evidence and cross-links
Primary contract: Adobe Help `Automated rendering and network rendering in After Effects`. Local runtime evidence: `datasets/ae-2025-headless-entrypoint.csv` and headless/plugin-loading experiments.

Related: `docs/headless-system/overview.md`, `docs/host-integration/command-line/index.md`, cache/persistence pages and Observatory environment-capture conventions.

## Unknown frontier
AEIG does not claim a complete inventory of which private services, extension hosts or background subsystems are suppressed or altered in every headless mode/release. Capability availability remains version- and host-context-specific and should be observed rather than guessed.
