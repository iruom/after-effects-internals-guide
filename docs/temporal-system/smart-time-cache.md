---
status: active
last_verified: 2026-09-15
---
# Smart Time Cache

Temporal cache validity is best modeled as a **dependency footprint over source time**, not simply "this frame depends on the previous frame".

## Public contract evidence
`PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT` allows AE to observe temporal checkouts made by an effect. Historical `PF_HaveInputsChangedOverTimeSpan` explicitly states that an unchanged queried span may be reused and that AE records the temporal dependency so later upstream changes invalidate the dependent result.

`PF_GetCurrentState` / `PF_AreStatesIdentical` extend state comparison over selected parameters and time ranges. For simulation-style effects using automatic wide time, the effective range can expand to include earlier times required to produce the requested interval.

## Internal correlation
BEE/TDB expose time-mixing and stream Render-GUID surfaces (`MixInValueAtTime`, `TDB_MixInTime`, stream/layer/comp `GetRenderGuid`). This is structurally consistent with time coordinates participating in render identity, without proving the exact cache-key algorithm.

## Model
`requested output time/range -> temporal checkouts/dependency footprint -> observed upstream state over that footprint -> render identity -> cache validity`.

A change at source time `t1` should invalidate only outputs whose registered footprint intersects `t1`, unless the effect declares broader dependency semantics.

## Smart Time preference evidence
Retained preferences include `Pref_DISABLE_SMART_TIME_CACHING` and historical SmartFX time-comparison vocabulary. These prove host policy exists around temporal reuse, but preference names alone do not define the algorithm.

## Failure modes
- reading time-dependent state without registering/checkout semantics;
- under-reporting simulation history;
- assuming one-frame locality for motion blur, echo, temporal denoise or expressions;
- caching plug-in-private temporal state without aligning it to host-observed dependencies.

## Experiment
Render A/B/A while moving one upstream edit inside and outside the effect's observed span. Compare output hashes, `MixHashGuid`/TDB trace, receipt/cache reuse and effect callbacks. This directly tests the footprint model.

## Version lineage and precision
Legacy `PF_OutFlag_WIDE_TIME_INPUT` is broad/conservative, while SmartFX-era automatic wide-time tracking lets AE observe actual time checkouts. Historical cache-validity patents and retained preferences show that temporal reuse predates MFR; MFR changes concurrency, not the basic need for temporal dependency identity.

Do not equate the retained `Pref_DISABLE_SMART_TIME_CACHING` key with a public switch or exact algorithm description. It is lineage evidence that temporal-cache policy remains independently controllable inside the host.

## Sparse versus interval identity
An effect that samples `{t-2,t,t+5}` can in principle have a sparse footprint, while motion blur may require an interval. AE's public API does not reveal whether internal cache metadata preserves sparse sets, merges them into intervals or uses another compressed representation.

This matters because over-approximating a sparse footprint is correct but reduces reuse, while under-approximating it can produce stale frames.

## Failure and falsification probes
Build deterministic temporal effects whose exact dependency sets are known. Mutate upstream frames immediately inside/outside those sets and compare callbacks/cache reuse. Then add nested time remap/stretch to test footprint transformation across time spaces.

For simulation-style state, test whether requesting a later interval first causes the host to widen state comparison backward. Compare current-state receipts and output hashes after edits just before the claimed history boundary.

A result where an edit outside the declared/observed footprint changes the output would falsify the footprint model or reveal an unregistered dependency.

## Unknown frontier
Unresolved: internal footprint representation; persistence of learned/observed dependencies across requests; interaction with speculative rendering; whether expression dynamic lookup can widen a previously established footprint; relation between temporal dependency metadata and exact TDB/BEE Render GUID composition.

Related: `docs/temporal-system/temporal-dependencies.md`, `docs/evaluation/dirty-invalidation.md`, `docs/cache-system/state-identity.md`.
