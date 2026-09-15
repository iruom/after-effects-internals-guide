---
status: confirmed
last_verified: 2026-09-14
evidence: AE-25.6-distributed-header
---
# F-THREAD-003 — Threaded rendering changes selector concurrency and sequence-data access

`AE_Effect.h` states that with `PF_OutFlag2_SUPPORTS_THREADED_RENDERING`, Sequence Setup, Sequence Resetup, Sequence Setdown, PreRender, and Render can execute on multiple threads concurrently with UI selectors.

Global Setup and Global Setdown remain main-thread-only and are not concurrent with other selectors.

During render, normal sequence data is read-only and must be accessed through `PF_EffectSequenceDataSuite`; `in_data->sequence_data` is NULL.

If an effect requires mutable render-time sequence state, `PF_OutFlag2_MUTABLE_RENDER_SEQUENCE_DATA_SLOWER` requests per-render-thread replicas. The header warns that mutations are regularly discarded, currently after spans such as a RAM Preview or Render Queue export.

## Architectural implication
The live effect instance, UI-side state, render-thread state, and persistent sequence representation are distinct ownership domains.

## Developer rule
Do not treat sequence data as a durable mutable accumulator during MFR. Use Compute Cache for shared derived state when possible.