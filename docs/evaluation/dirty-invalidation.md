---
status: active
last_verified: 2026-09-16
evidence: current/historical PF state + wide-time contracts + Render Suite timestamps + BEE/TDB/RG identity evidence
---
# Dirty Propagation and Invalidation

After Effects cannot be explained by one project-wide dirty bit. Different consumers care about different state, time spans, external resources and render contexts, so invalidation is layered and dependency-specific.

A useful model is:

```text
edit / external change
      |
      v
affected semantic state
      |
      +--> dependency footprint (including time)
      +--> explicit extra dependency declarations
      v
state / request identity
      |
      v
cache-validity decision
      |
      +--> reuse existing materialization
      `--> schedule new work
```

The project can be globally modified while many cached render results remain semantically reusable.
## PF_State: an explicit cache-state receipt

`PF_GetCurrentState()` returns an opaque `PF_State` describing selected effect inputs over an optional time span. Adobe documents that this state is used by the internal frame caching database. `PF_AreStatesIdentical()` then asks whether two such input-state receipts are equivalent.

That makes `PF_State` closer to a semantic cache receipt than to a mutable snapshot object. Plug-ins should compare it, not inspect or serialize private contents.

The queried scope matters. Callers can include all parameters, exclude layer params, honor explicit exclusions, or focus the relevant time span. Two states can therefore be identical for one dependency query and different for another.

`PF_IsIdenticalCheckout()` is narrower still: it compares one parameter at two times. It should not be promoted into a whole-effect identity test.
## Temporal dependency tracking

`PF_OutFlag_WIDE_TIME_INPUT` tells AE that an effect can read parameters/layers at times other than the current output time. The modern `PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT` lets the host track actual parameter checkouts and build a tighter temporal dependency footprint.

The difference is substantial. With only the coarse wide-time declaration, an upstream change anywhere in time may force a rerender. With automatic tracking, a cached output frame that actually read only times 0-17 need not be invalidated by a change at frame 18+.

This is dependency registration, not merely a performance hint. If an effect keeps its own time-dependent derived state outside host-tracked checkouts, it must validate that state separately with `PF_GetCurrentState()` / `PF_AreStatesIdentical()` or an equivalent supported mechanism.

The historical `PF_HaveInputsChangedOverTimeSpan` contract is useful architecture evidence: when an unchanged span was queried, AE both allowed cache reuse and learned the temporal dependency for future selective invalidation. The API is deprecated, but the dependency principle remains.
## Other explicit invalidation dimensions

AE exposes several flags precisely because parameter values alone do not describe every dependency:
- external files/fonts via `PF_OutFlag_I_HAVE_EXTERNAL_DEPENDENCIES`;
- unreferenced masks via `PF_OutFlag2_DEPENDS_ON_UNREFERENCED_MASKS`;
- composition timecode/start settings via `PF_OutFlag2_I_USE_COMP_TIMECODE`;
- shutter-angle dependency via `PF_OutFlag_I_USE_SHUTTER_ANGLE`;
- audio dependency via `PF_OutFlag_I_USE_AUDIO`;
- non-parameter variation via `PF_OutFlag_NON_PARAM_VARY`.

These contracts are direct evidence that AE's dependency model is multi-domain. A correct cache key or dirty-propagation system must include hidden context that cannot be inferred from the visible parameter list alone.

`PF_OutFlag_FORCE_RERENDER` is therefore a coarse escape hatch, not a substitute for semantic identity. Adobe has progressively added more specific mechanisms because indiscriminate invalidation destroys reuse and can interact poorly with render-side state synchronization.
## Explicit GUID dependency mixing

SmartFX adds a more semantic route than blind rerender flags. With `PF_OutFlag2_I_MIX_GUID_DEPENDENCIES`, `GuidMixInPtr()` lets the effect mix render-relevant state that AE cannot infer automatically into the host's internal cached-frame GUID during PreRender.

This preserves information that `PF_OutFlag_FORCE_RERENDER` throws away. If the project returns to a previously seen semantic state through Undo, a matching GUID can make an older cached frame reusable instead of globally discarding it.

The mixed bytes must therefore represent semantic render dependencies, not pointers, allocation addresses, thread IDs or ephemeral container layout.

## Project timestamps are another coordinate

`AEGP_GetCurrentTimestamp()` provides a project edit generation, while `AEGP_HasItemChangedSinceTimestamp()` asks whether an item's **video** changed over a requested interval since that generation. Adobe explicitly notes that audio is not tracked by this query.

This is useful for speculative/external renderers but is not a universal cache key. `AEGP_IsItemWorthwhileToRender()` should be checked before expensive external work and again before checking the completed frame back in, because the project can change while the work is in flight.
## Internal correlation without collapsing identities

Local AE 2025 runtime evidence shows TDB streams exposing render-GUID/value-at-time mixing, BEE layer/item/render-options objects producing render GUIDs, BEE work queues requesting GUIDs before scheduling, and RG cache nodes validating node data before rendering.

This supports a boundary chain:

`stream/property state -> BEE request identity -> work scheduling -> RG cache validation`.

It does **not** prove that `PF_State`, AEGP frame-receipt GUIDs, SmartFX mixed GUIDs, BEE Render GUIDs and RG cache-node keys are byte-identical or interchangeable. Keep them separate until a controlled experiment connects them.

## Failure classes

- **missing dependency**: output changes but the host was never told about the causal state;
- **over-broad dependency**: harmless edits invalidate large cache regions;
- **wrong temporal footprint**: an effect samples another time without registering it;
- **ephemeral identity input**: pointer/address/order is mixed into a supposedly semantic key;
- **stale private cache**: plug-in-owned derived state survives after host-visible dependencies changed;
- **view/render confusion**: UI-only state is accidentally treated as pixel-render state.

These failures can produce either wrong pixels or merely catastrophic performance. Both belong in an invalidation model.
## Experiments

Use adversarial edits that isolate dependency classes: parameter change, upstream layer edit inside/outside the sampled time range, mask not referenced by a parameter, comp start-time change, external file change, audio-only edit, guide/view-state edit, sequence-data mutation and Undo back to a prior state.

For each case record `PF_State` equality where available, project timestamp change, SmartFX mixed GUID input, frame receipt/GUID, BEE/TDB/RG trace footprint, cache marks and output hash. This reveals where invalidation is precise, over-broad or missing.

A particularly valuable test is temporal sparsity: render frame N whose effect samples only a bounded interval, then edit just outside that interval. A correct tracked dependency should preserve N while invalidating frames whose footprints include the edited time.

## Unknown frontier

The exact composition of BEE Render GUIDs, how TDB dependency paths are canonicalized, the relationship between Canvas receipts and RG cache-node validity, and how external/media dependencies enter render identity remain partially reconstructed.

Cross-links: `../cache-system/state-identity.md`, `../render-graph/frame-checkout.md`, `../architecture/project-vs-render-state.md`, `../temporal-system/time-model.md`, `../expression-engine/architecture.md`, and experiments `EXP-CACHE-002` / `EXP-RG-001`.
