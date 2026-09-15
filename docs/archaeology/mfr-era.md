---
status: active
last_verified: 2026-09-15
evidence: MFR public contract + AE 25.6 sample/header evidence
---
# Multi-Frame Rendering Era

Modern MFR turns frame-level concurrency into a first-class plug-in compatibility boundary. Effects must declare threaded-rendering support and obey stricter sequence-data and locking rules.

With threaded rendering enabled, render-related selectors can execute concurrently while UI selectors remain active. Global lifecycle selectors stay on the main-thread boundary.

Render-time sequence data is separated from the live instance: normal sequence state is read through `PF_EffectSequenceDataSuite`, while mutable render sequence data requires slower per-render replicas whose mutations are not durable.

Adobe's current `Supervisor` sample documents an unresolved pattern where UI-side sequence-data mutation prevents the sample from being marked thread-safe for MFR.

## Architectural meaning
MFR should be modeled as an evolution of the post-13.5 snapshot architecture, not as "run the old renderer N times".

It strengthens separation among UI/live state, synchronized render state, per-frame work and shared derived-cache state.

## Compatibility lesson
A plug-in that is pixel-correct in single-frame mode can still be architecturally invalid under MFR because of sequence ownership, host-callback locks or hidden mutable globals.

See `docs/mfr/overview.md` and `F-THREAD-003`.## Version boundary
Adobe's public timeline makes MFR a staged transition rather than one release switch. MFR support appeared in AE Beta in June 2020; the March 2021 SDK changed render-time sequence-data semantics; AE 2022/22.x then carried the production-era contract forward.

Effects built for the June 2020 MFR contract had to be recompiled against the March 2021 SDK to participate in the newer sequence-data model. This is a concrete example where “supports MFR” is versioned behavior, not one timeless flag.

## Evidence from selector concurrency
With MFR enabled, sequence setup/resetup/setdown and render-related selectors may execute on multiple threads concurrently with UI selectors, while Global Setup/Setdown remain isolated on the main thread.

Render-time `sequence_data` is const by default and retrieved through `PF_EffectSequenceDataSuite`. The mutable compatibility flag creates independent per-render-thread copies that are not shared or synchronized and are regularly discarded.

This strongly favors a decomposition into immutable render instance state plus host-managed shared Compute Cache, rather than using sequence data as a cross-frame accumulator.

## Observable performance contract
Adobe warns that mutable render sequence data significantly reduces MFR benefit and exposes a warning icon to users. Thread-safety declarations are therefore both correctness and user-visible performance contracts.## Experiments
For one deterministic effect, compare single-frame mode, MFR with const sequence data, and mutable-compatibility mode. Record selector/thread overlap, number of render-side sequence copies, shared derived computation count, peak memory and total frame throughput.

Add a deliberate global mutable counter and a sequence-data accumulator in a diagnostic build. The experiment should demonstrate which state races, which state is duplicated and which mutations are discarded rather than assuming the host serializes access.

Use Compute Cache for the expensive derived value in a fourth variant; compare whether duplicate computation collapses without reintroducing plug-in-global locking.

## Open questions
Public MFR contracts do not expose the complete frame-admission heuristic: RAM pressure, GPU work, temporal dependencies and host scheduling all influence how many frames actually execute concurrently. Current BEE work-queue surfaces constrain this problem but do not define the public scheduler algorithm.

Cross-links: `../mfr/overview.md`, `../mfr/state-ownership.md`, `../threading-system/effect-selector-concurrency.md`, `../cache-system/compute-cache.md`, and `cc2015-rearchitecture.md`.