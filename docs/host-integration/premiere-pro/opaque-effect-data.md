---
status: active
last_verified: 2026-09-16
evidence: current Premiere Pro C++ SDK Guide Opaque Effect Data Suite; cross-host comparison only
---
# Opaque Effect Data as a Shared-State Design

Premiere Pro's `PrSDKOpaqueEffectDataSuite` is a useful sibling-host example of how Adobe separates **persistent sequence representation** from **shared live render state**. It must not be silently projected onto After Effects, but its explicit lifetime rules are valuable when reasoning about AE MFR, sequence cloning and Compute Cache.

## Problem solved by the suite
Premiere can create multiple render instances/clones of an effect on one track item. Ordinary flattened/unflattened sequence data is not sufficient when those clones need access to one shared live object.

The suite lets the effect associate opaque unflattened state with the effect instance identity while the host supplies reference counting. The host does not interpret the payload; thread safety remains the effect's responsibility.

## Render-clone signal
The current Premiere SDK describes a special lifecycle: render clones can receive `PF_Cmd_SEQUENCE_RESETUP` with `PF_InData->sequence_data == NULL`. In that case the clone acquires the already-registered opaque state instead of reconstructing ordinary sequence data.

A non-clone resetup with valid flattened sequence data reconstructs persistent state and may initialize/register opaque state when reopening a project.

This makes the distinction concrete:

`disk-safe sequence representation != live shared render object`.

## Registration race
Several threads may discover that no opaque state exists and race to create/register one. The host chooses one winning pointer and returns that shared object; losing threads must destroy the object they created but did not publish.

This is effectively a host-mediated compare-and-publish primitive. A plug-in must therefore design construction/destruction so a losing registration attempt is safe and leaves no leaked auxiliary resources.

## Lifetime and ownership
`AcquireOpaqueEffectData()` increments the host's reference count. `ReleaseOpaqueEffectData()` decrements it and tells the effect when the payload has reached the point where it should be destroyed.

Reference counting solves lifetime, not synchronization. If multiple render clones mutate the opaque payload concurrently, the effect still needs a coherent concurrency design. A refcounted data race is still a data race.

## Why this matters for AEIG
AE's modern MFR guidance moves ordinary render-time sequence state in the opposite direction: const render access by default, with expensive mutable per-thread copies only as a compatibility option, and Compute Cache recommended for reusable computed values.

Comparing the hosts exposes three distinct patterns:
- durable sequence state serialized with the project;
- shared host-lifetime-managed live state;
- regenerable host-cache state keyed from semantic inputs.

Those are different solutions to different ownership problems. Choosing the wrong one usually creates either persistence bugs, synchronization bugs or unnecessary recomputation.

## Failure modes and tests
Test at least: simultaneous first acquisition, project reopen, effect duplication, render-clone creation/destruction, cancellation, repeated setup/setdown and concurrent reads/writes. Instrument object creation/destruction and verify that exactly one published object survives a registration race.

Do not store process-local pointers in the flattened project representation and expect them to reconnect automatically. Conversely, do not assume the live opaque object is persisted merely because it originated from sequence state.

## AE comparison boundary
There is no evidence in AEIG that After Effects exposes or internally uses `PrSDKOpaqueEffectDataSuite`. The justified conclusion is narrower: Adobe hosts have needed explicit mechanisms to distinguish serialized effect-instance state from shared render-instance state, and AE's MFR/Compute Cache design should be analyzed with the same ownership questions.

Related pages: `docs/mfr/overview.md`, `docs/persistence/sequence-data.md`, `docs/cache-system/compute-cache.md`, and `docs/threading-system/overview.md`.

## Unknown frontier
The exact correspondence between Premiere render-clone machinery and AE's post-13.5 render-side copies is unresolved. Cross-host similarities are architectural evidence, not ABI equivalence or proof of common private implementation.
