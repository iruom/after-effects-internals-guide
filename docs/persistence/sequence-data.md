---
status: active
last_verified: 2026-09-14
---
# Sequence Data: Instance State, Serialization, and Render-Side Copies

Sequence data is not merely a convenient per-effect struct. It sits at the intersection of effect-instance identity, project serialization, UI-side mutable state, render-side project snapshots, duplication/copy, undo, and Multi-Frame Rendering.

A useful model is to treat it as an instance-local object with at least three representations:

`live/unflattened state -> flattened portable representation -> render-thread representation`

The representations have different lifetime and mutability rules. Confusing them is a major source of stale state, crashes, leaks, and nondeterministic rendering.

## Flattening is a serialization boundary
The SDK documentation explicitly describes flattening as a miniature file format. Any pointer/handle into external memory must be replaced by portable contiguous data before persistence. Byte order and ABI-dependent representation are the plug-in's responsibility.
## PathMaster exposes the destructive/non-destructive split
Adobe's `PathMaster` sample is unusually explicit. Its `PF_Cmd_SEQUENCE_FLATTEN` implementation creates the flat copy, deletes heap-backed unflattened payload, disposes the old sequence-data handle, and replaces it with the flat representation.

`PF_Cmd_GET_FLATTENED_SEQUENCE_DATA`, added later, deliberately performs the same serialization without destroying the live unflattened state. The sample comments that preserving the live data is the entire point of this selector.

This distinction became architecturally important after AE 13.5, when UI-side state and render-side project copies had to be synchronized without destructively flattening state during interactive operations.

### Developer rule
Treat `SEQUENCE_FLATTEN` as a representation transition and `GET_FLATTENED_SEQUENCE_DATA` as a snapshot operation. Reusing one implementation carelessly for both can destroy UI state or introduce reentrancy/lifetime bugs.

## Cross-platform traps
`PathMaster` intentionally contains warnings that direct numeric copies are not cross-platform safe. Production flat data should define byte order, field widths, versioning, and migration explicitly rather than serializing compiler-native structs.
## MFR changes the ownership model
With modern MFR, render-time sequence data is read-only by default and is marshalled to render threads. Mutable render-time sequence data requires an explicit slower compatibility mode that duplicates sequence data per render thread.

That design exposes an important invariant: mutable instance state cannot safely be treated as a single process-global object once multiple frames render concurrently.

For expensive mutable derived data, the Compute Cache is the preferred shared substrate because it coordinates computation across render threads instead of forcing every thread to rebuild its own copy.

## Historical clues
Old local preferences include `Unflatten sequence data before NewContext`, evidence that sequence representation and context creation have long been coupled internally.

## Failure modes to diagnose
- flat/unflat discriminator corrupted or missing;
- pointer serialized directly into project data;
- old flattened version interpreted as new struct layout;
- sequence data mutated during MFR without the proper contract;
- destructive flatten performed during interactive UI synchronization;
- stale render-side copy after UI mutation;
- handle resized during a selector where resizing is not permitted.

## Selector concurrency under MFR
The AE 25.6 header is explicit that threaded rendering changes more than `PF_Cmd_RENDER`. Sequence Setup, Sequence Resetup, Sequence Setdown, Smart PreRender, Render and Smart Render may execute on multiple threads while UI selectors are simultaneously handled on the main thread.

Global Setup and Global Setdown remain serialized main-thread phases. This gives sequence state at least two synchronization boundaries: process/global lifetime and instance/render lifetime.

During threaded render, ordinary `in_data->sequence_data` is intentionally NULL. Read-only state is obtained through `PF_EffectSequenceDataSuite`; direct render-time mutation is not the normal contract.

`PF_OutFlag2_MUTABLE_RENDER_SEQUENCE_DATA_SLOWER` restores writable per-render-thread replicas, but those mutations are ephemeral and may be discarded after render spans such as RAM Preview or Render Queue export.

### Developer rule
Never use mutable render-time sequence data as the authoritative long-lived state of the effect. Treat it as a compatibility-local working copy. Shared expensive derived state belongs in Compute Cache or another explicitly synchronized substrate.