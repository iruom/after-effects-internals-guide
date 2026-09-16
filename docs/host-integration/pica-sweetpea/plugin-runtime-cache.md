---
status: active
last_verified: 2026-09-16
evidence: distributed SweetPea `SPCaches.h`/runtime headers + Effect lifecycle contract
---
# SweetPea/PICA Plug-in Runtime Cache and Module Lifetime

SweetPea has a cache whose unit is **loaded plug-in/module runtime state**, not rendered pixels. Confusing it with AE's frame/cache systems leads to incorrect lifetime assumptions.

`SPCaches.h` describes PICA plug-ins as loadable/unloadable objects. The runtime can retain loaded plug-ins for reuse and later purge unused modules under memory pressure; adapters can participate in a cache-purge protocol.

## Effect lifetime is not module lifetime
The Effect API's `PF_Cmd_GLOBAL_SETUP` / `PF_Cmd_GLOBAL_SETDOWN` describe effect-global lifecycle. Current SDK documentation explicitly warns not to use `GLOBAL_SETDOWN` to decide when the plug-in module is removed from memory; OS-specific entry/unload mechanisms own that boundary.

Therefore keep these lifetimes separate:

`effect instance -> effect global state -> PICA plug-in/access state -> loaded code module`.

They can overlap, but they are not interchangeable destruction events.## Purge protocol
Adapters that advertise the conditional purge-caches message can receive `kSPPluginPurgeCachesSelector`. `SPCachesSuite::SPFlushCaches()` asks adapters to unload unused plug-ins and reports how many were actually unloaded.

This is host/runtime resource management, not semantic render invalidation. Flushing this cache must not be interpreted as purging frame, expression, media or GPU caches.

## Design implications
Module-global caches must tolerate module lifetime correctly. Initialization that accidentally assumes “loaded once for the entire AE process” can fail when the host legitimately unloads and later reloads a plug-in.

Likewise, external callbacks, worker jobs or native handles must not outlive the code/data lifetime they depend on unless ownership is transferred to a separately valid subsystem.

For suite providers, acquisition/release discipline matters independently from module-global C++ object lifetime. Do not infer that a cached C++ pointer remains safe merely because a suite name/version can be reacquired later.

## Cache taxonomy
AEIG uses qualified names:
- **module/runtime cache** — PICA/SweetPea loaded plug-ins;
- **Compute Cache** — derived values keyed by semantic input;
- **render/receipt cache** — frame/stage validity;
- **RAM/disk frame residency**;
- **media/decode cache**;
- **expression caches**;
- **GPU asset/device residency**.## Failure modes
Typical unload-sensitive defects include static/global state that is not rebuilt on reload, background work invoking code after unload, asymmetric OS entry/unload cleanup, duplicate registration after reload, and diagnostics that mistake a module reload for a new effect instance.

These are hypotheses to test per plug-in; the SweetPea contract establishes that unloadability must be considered, not that every AE effect is aggressively unloaded in ordinary sessions.

## Experiments
Build an instrumented plug-in that logs OS module attach/detach, PICA entry, `GLOBAL_SETUP/SETDOWN`, sequence lifecycle and suite acquisition. Exercise effect removal, project close, long idle periods, memory pressure and explicit host cache-purge paths where safely available.

The experiment should distinguish “effect no longer has instances” from “binary actually unloaded” and verify whether a subsequent use performs a true module reload.

## Unknowns
AE's current policy for when a particular third-party effect module becomes purge-eligible is not a public stable contract. SweetPea defines the architecture and purge mechanisms; concrete AE heuristics require version-scoped runtime observation.

Cross-links: `suite-versioning.md`, `runtime-architecture.md`, `../../memory-system/overview.md`, and `../../cache-system/cache-architecture.md`.