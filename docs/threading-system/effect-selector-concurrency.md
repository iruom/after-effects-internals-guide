---
status: active
last_verified: 2026-09-16
evidence: MFR selector contracts + sequence-data ownership + dynamic-flag warnings + 13.5 thread/project split
---
# Effect Selector Concurrency

Thread safety in modern AE is a **selector/lifetime/state contract**, not merely "the pixel loop has no globals".

## Selector concurrency classes
### Main-thread serialized lifecycle
`PF_Cmd_GLOBAL_SETUP` and `PF_Cmd_GLOBAL_SETDOWN` are guaranteed on the main thread and are not sent concurrently with other selectors. They are appropriate for process/module-lifetime registration, not per-instance mutable render state.

### Main-thread UI/edit selectors
UI/event selectors execute on the UI thread, but can overlap in time with render-side selectors once an effect participates in threaded rendering. `PF_Cmd_UPDATE_PARAMS_UI` is cosmetic-only; checking out parameters there is explicitly unsafe.

### Potentially concurrent render/sequence selectors
With `PF_OutFlag2_SUPPORTS_THREADED_RENDERING`, Adobe documents that `PF_Cmd_SEQUENCE_SETUP`, `PF_Cmd_SEQUENCE_RESETUP`, `PF_Cmd_SEQUENCE_SETDOWN`, `PF_Cmd_SMART_PRE_RENDER`, `PF_Cmd_RENDER` and `PF_Cmd_SMART_RENDER` may be sent on multiple threads while UI selectors are active.

Therefore setup/resetup/setdown code is not automatically a serialized safe zone.

## State ownership under MFR
Modern render-time `sequence_data` is const and read through `PF_EffectSequenceDataSuite`; direct writable access is disabled by default.

`PF_OutFlag2_MUTABLE_RENDER_SEQUENCE_DATA_SLOWER` restores write access by creating independent per-render-thread copies. Those copies are **not shared state** and their mutations are discarded regularly after render spans.

Use the right storage class:
- immutable configuration -> synchronized sequence/render state;
- shared expensive derived value -> Compute Cache or another explicitly synchronized cache;
- per-thread scratch -> `thread_local` or frame/request-local storage;
- cross-frame evolving simulation -> validated state with explicit temporal identity, not accidental shared sequence mutation.

## Lock-boundary rule
Adobe's MFR guidance warns against calling host services while holding plug-in mutexes when those calls can re-enter or block on AE. The safe default is:
1. acquire plug-in lock;
2. snapshot/update plug-in-owned state;
3. release lock;
4. call host suites/checkouts/render services;
5. reacquire only if needed to publish results.

This reduces lock inversion between plug-in locks and host project/render locks.

## Dynamic-flag race boundary
`PF_Cmd_QUERY_DYNAMIC_FLAGS` may occur independently of the eventual render. Header comments specifically warn that asynchronously changing `PF_OutFlag2_OUTPUT_IS_WATERMARKED` can produce incorrect cached frames if the rendered state does not match the last queried flags.

General invariant:

**Any dynamic flag that changes pixel semantics must be derived from the same versioned state consumed by the corresponding render generation.**

A robust implementation snapshots semantic state, answers Query Dynamic Flags from that snapshot/generation, and renders from the same generation instead of rereading mutable external state later.

## UI/render shared-state anti-patterns
Dangerous designs include:
- UI writes a global structure while render reads it without versioning;
- render mutates sequence state expecting UI to see it;
- UI owns a pointer referenced by render copies without publication/lifetime control;
- one mutex protects everything and is held while calling AE;
- static scratch buffers are reused by concurrent frames;
- lazy initialization is race-prone because multiple render selectors enter simultaneously.

## Host-specific divergence
Premiere's `PF_OutFlag2_PPRO_DO_NOT_CLONE_SEQUENCE_DATA_FOR_RENDER` changes host ownership policy. Adobe advises against using it because of historical parameter-UI problems. Host-specific flags should be treated as semantic ownership contracts, not "faster" switches.

Cross-host thread behavior must be tested independently even when the PF ABI is shared.

## Test matrix
A proper concurrency test must vary more than frame count:
1. same effect instance, many frames;
2. multiple instances of same effect;
3. UI parameter drag while frames render;
4. sequence resetup/setdown concurrent with other instances;
5. cancellation/abort during expensive host checkout;
6. project close/effect deletion near async completion;
7. MFR on/off and different worker counts;
8. cache warm/cold to alter callback ordering.

Use deterministic output hashes and race instrumentation. A test that merely "does not crash" is insufficient: stale semantic state and nondeterministic pixels are concurrency failures too.

## Failure signatures
- output differs between MFR on/off -> shared mutable state or non-deterministic dependency;
- rare stale frame after UI edit -> publication/dynamic-flag generation race;
- deadlock under scrub/cancel -> lock inversion with host callback;
- crash during close -> async/request lifetime escapes effect instance;
- performance collapses only with mutable render sequence flag -> per-thread copy/serialization overhead.

## Unknown frontier
Still unresolved for AE internals:
- exact worker pools used by PF render selectors versus BEE/RG task execution;
- which host callbacks can re-enter plug-in selectors on the same or another thread;
- scheduling/fairness between MFR, speculative preview, media decode and GPU queues;
- whether some sequence lifecycle operations are internally serialized per instance even though the public contract requires thread safety.

Related: `docs/threading-system/overview.md`, `docs/mfr/state-ownership.md`, `docs/state-model/snapshots.md`, `docs/render-graph/async-render-requests.md`.
