---
status: active
last_verified: 2026-09-16
evidence: SmartFX wide-time contracts + PF state APIs + expression/time-mapping behavior + historical cache-validity design
---
# Temporal Dependencies

A rendered frame in AE can depend on state from times other than its nominal output time. AEIG models this as a **temporal dependency footprint**, not as one global frame index.

## Dependency footprint model
For an output request at time `t`, define a footprint `D(t)` describing source-time samples/intervals required to produce the result.

Examples:
- ordinary current-time effect: approximately `{t}`;
- frame blending: neighboring source samples;
- motion blur: transform/effect samples across a shutter interval;
- expression `valueAtTime(t+x)`: explicit shifted dependency;
- time remap: output comp time mapped into source/layer time;
- nested comp: composed time mappings across levels;
- temporal denoise/analysis: potentially wider past/future window.

The footprint may be sparse, interval-like, mapped or conservatively unknown/all-time.

## `AUTOMATIC_WIDE_TIME_INPUT` is dependency registration
`PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT` tells AE to track actual parameter checkouts for SmartFX. Adobe's example is explicit: if cached frame 17 checked out upstream times 0-17, a change only at frame 18 or later need not invalidate frame 17.

That is stronger than simply declaring "this effect uses other times". The host records an observed temporal dependency footprint and uses it for cache validity.

The contract also warns that a plug-in must not hide additional time-dependent data in `sequence_data` or elsewhere unless it validates that private cache with `PF_GetCurrentState()` / `PF_AreStatesIdentical()`. Otherwise the host's dependency footprint is incomplete.

## State receipts and temporal closure
`PF_GetCurrentState()` can capture selected parameter/layer state over a time range, while `PF_AreStatesIdentical()` tests whether the dependency state remains equivalent. With automatic wide-time input, the effective state can represent more than authored keyframes: it can include the source-time dependencies needed to produce the interval.

A useful conceptual chain is:

`output time -> mapped source times -> observed checkouts -> temporal footprint -> dependency/state receipt -> render GUID/cache validity`.

The exact internal representation is not public.

## Time-coordinate composition
Temporal dependencies become difficult because AE has multiple time spaces. A nested request can pass through:

`comp time -> layer time/stretch -> time remap/source time -> nested comp time -> effect/expression offset -> shutter/frame-blend samples`.

A footprint must therefore be transformed when it crosses a time-mapping boundary. Treating all times as seconds in one coordinate system will produce incorrect invalidation and sampling models.

## Sparse versus interval dependencies
A three-sample temporal filter may depend only on `{t-1, t, t+1}`, whereas a motion-blur integration conceptually depends on an interval. Representing the sparse set as one wide interval is safe but can over-invalidate; representing an interval as too few samples can be incorrect.

This yields a recurring design tradeoff:
- precise dependency metadata -> better cache reuse, more bookkeeping;
- conservative interval/all-time dependency -> simpler tracking, more false invalidation.

## Failure modes
- cache private time-dependent data outside the host's tracked checkout graph -> stale results;
- use old broad `WIDE_TIME_INPUT` semantics when exact checkout tracking is available -> excessive rerender;
- forget a future/past source checkout -> locally correct frame until upstream edit exposes stale reuse;
- compare time values after lossy float conversion -> wrong interval identity near rational frame boundaries;
- fail to map footprint through time remap/nested comps -> invalidate the wrong source range;
- expression resolution changes can alter `D(t)` even when the sampled value happens to stay equal.

## Controlled experiment matrix
Use an effect/expression fixture whose dependencies are analytically known. Test:
1. current-time only;
2. one fixed past sample;
3. one fixed future sample;
4. sparse past/current/future samples;
5. continuously widened interval;
6. time-remapped source;
7. nested comp with non-unit stretch;
8. motion blur and frame blending.

Mutate upstream state just inside and just outside the predicted footprint. Record rerender decisions, PF state equality, output hashes and BEE/TDB/RG trace/cache behavior.

A strong implementation test is whether edits outside `D(t)` preserve reuse while edits inside it invalidate exactly the affected outputs.

## Version and compatibility boundary
The old `PF_OutFlag_WIDE_TIME_INPUT` remains for compatibility and is conservative. `PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT` adds host-observed checkout tracking for SmartFX. Do not assume older hosts or non-SmartFX paths provide the same precision.

## Unknown frontier
Still unresolved:
- current internal data structure for temporal footprints;
- whether BEE/RG stores exact samples, intervals or compressed dependency summaries;
- how expression dynamic lookup modifies a previously learned footprint;
- motion-blur sampling footprint before/after effect stages;
- how speculative rendering predicts future temporal dependencies before they are fully observed.

Related: `docs/temporal-system/time-model.md`, `docs/temporal-system/motion-blur.md`, `docs/evaluation/dirty-invalidation.md`, `docs/evaluation/collateral-dependencies.md`.
