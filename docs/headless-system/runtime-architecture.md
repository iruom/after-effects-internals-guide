---
status: active
last_verified: 2026-09-15
---
# Headless Runtime Architecture

The installed 25.6 aerender contract shows a controller/host split rather than a separately linked render engine.

```text
aerender.exe
  CLI parsing / logging / policy overrides
        |
        +--> launch a new AE instance (default)
        |
        +--> request an already-running AE instance (-reuse)
                         |
                         v
                After Effects host
          project + render queue state
                         |
          BEE / PF / Media / GPU / output
                         |
                         v
                       files
```

This model explains why headless comparison remains valuable even though the renderer is shared: startup mode, loaded services, preferences, UI availability, plug-in policy, GPU/device selection, cache state and process lifetime may differ.
## Controller-exposed policy dimensions
`-mem_usage` changes image-cache and total-memory percentages. `-mfr` changes MFR enablement and CPU-use policy. `-close` affects project/save/lifetime behavior. These are host execution-context dimensions and should be captured with every headless Observatory result.

The runtime help also distinguishes preference persistence: reused AE and newly launched AE do not have identical preference-write behavior on completion. Headless reproducibility tests must therefore record whether `-reuse` was used.

## Differential experiment axes
- fresh aerender-launched AE versus `-reuse` interactive AE;
- MFR on/off and CPU cap;
- identical project with warm/cold media and disk caches;
- GPU-enabled versus CPU-only/render-engine-safe paths;
- plug-in load/module inventory;
- missing-footage continuation policy;
- byte/pixel hashes plus render-time trace categories.

Primary evidence: `F-HEADLESS-001` and `datasets/ae-2025-headless-entrypoint.csv`.

## Fresh process and `-reuse` are different experiments
Current Adobe aerender documentation makes the process-lifetime difference explicit. By default aerender starts a new After Effects instance even when one is already running; that instance is told to quit when rendering finishes. With `-reuse`, the already-running AE instance performs the render and is not quit by aerender.

Preference persistence also differs: Adobe documents preference-file writing on completion for the reused path but not for the fresh aerender-launched instance. Therefore fresh versus reuse can differ in process globals, loaded modules, warm caches, preferences and extension/plug-in lifetime even with the same project and render settings.

Treat `fresh` and `reuse` as distinct Observatory environment coordinates, not as interchangeable ways to launch identical work.

## AEGP/process-instance identity trap
The public AEGP implementation guide warns that when a second command-line AE instance is launched, an AEGP's handles are duplicated. Plug-ins that persist/compare opaque handles without associating them with a specific plug-in/host instantiation can therefore break under multi-instance/headless workflows.

This is a concrete example of `handle identity != semantic object identity != process identity`.

## Scheduler/resource policy is CLI-visible
`-mfr ON|OFF max_cpu_percent` changes frame-level concurrency and CPU admission. `-mem_usage image_cache_percent max_mem_percent` changes image-cache and total-memory limits.

A benchmark that changes these switches is not measuring only rendering code; it is changing scheduler and residency policy. Record them with process freshness, GPU/backend and cache temperature.

## Failure modes
- compare interactive render against fresh aerender but forget one side has warm module/media/disk caches;
- reuse a long-lived AE instance and call it a clean headless run;
- serialize AEGP handles or global pointers across host/process instances;
- assume UI-unavailable means UI-side services/extensions cannot influence startup/module policy;
- omit `-mfr`/CPU cap or memory policy from performance evidence;
- treat preference changes produced by a reused session as if a fresh render engine wrote them.

## Controlled differential matrix
Run the same deterministic project in at least four modes: fresh interactive AE, fresh aerender, `-reuse` interactive AE and render-engine/network-render context where available. For each, record process tree/PID, module inventory, plug-in loading log, preferences/profile hash, MFR/memory flags, GPU identity, cache temperature, render trace and output hash.

Repeat with one deliberate cache purge and one full process restart. This separates result semantics from process-local residency/lifetime effects.

## Unknown frontier
Still unresolved: exact service/module suppression policy in each render-engine mode, whether every UI/extension subsystem initializes under `-reuse`, process-local lifetime of BEE/TDB/RG caches across consecutive aerender jobs, and differences between aerender reuse and Dynamic Link/Media Encoder hosting.

Related: `docs/host-integration/cpp-sdk/index.md`, `docs/memory-system/runtime-architecture.md`, `docs/render-graph/render-tasks.md`.
