---
status: active
last_verified: 2026-09-14
---
# Cache State Identity

AE exposes several opaque but related identity mechanisms: `PF_State`, render receipts, AEGP receipt GUIDs, SmartFX GUID mixing, Compute Cache input-state hashes, and runtime Render-GUID symbols.

The strongest current model is that cached results are indexed primarily by render-relevant state identity rather than only by `(comp, layer, frame)` coordinates.

A provisional identity composition is:

`K = H(source/version identity, temporal state, parameter state, upstream state, render context, pixel semantics, implementation version, explicit extra dependencies)`

Not every cache domain necessarily uses the same key or the same fields.

## Identity is separate from residency
Premiere's sibling-host PPix cache makes this distinction explicit: a GUID identifies a pixel result, while dependency registration controls whether that result is retained. AEIG should keep identity, validity, residency, and eviction as separate axes.

## Boundary-by-boundary reconstruction
The installed AE 2025 binaries now make the internal identity boundary more concrete without proving one monolithic cache key.

`BEE.dll` exports `GetRenderGuid()` on `BEE_RenderOptions` and `BEE_LayerRenderOptions`, `GetRenderGuidWithRO()` on layers/items, and dedicated `BEE_RenderGuidCache<...>` accessors. It also exposes explicit mixers for layer flags, transforms, lights, and time-varying stream values using `dvacore::utility::Murmur3MixerState`.

Its imported surfaces include `TDB_Stream::GetRenderGuid`, `TDB_Stream::MixInValueAtTime`, and `TDB_MixInTime`. This is strong evidence that stream state plus time participate in internal render-identity formation at the TDB→BEE boundary.

A separate work-queue export, `BEEp_WorkQueue_GetRenderGuidWithRO`, accepts Layer Render Options and produces a GUID through its callback path. Render identity therefore exists at scheduling time, not only after pixels have been materialized.

Do not infer that the public `PF_State`, SmartFX internal frame GUID, Frame Receipt GUID, and every BEE Render GUID are bit-identical. The evidence supports connected identity responsibilities, not universal GUID equality.
## Public state receipts are dependency identity, not serialized values
Adobe describes `PF_State` as an opaque receipt for the current state of selected parameters/layers and notes that it is used by AE's internal frame caching database. `PF_AreStatesIdentical()` asks an equivalence question without exposing the receipt layout.

When `AUTOMATIC_WIDE_TIME_INPUT` is active, a requested time range is expanded to include source times required to produce it. Therefore a PF state can represent a temporal dependency closure rather than just current parameter bytes.

This is a key architectural property: callers declare **what dependency scope matters**, while AE owns the canonical comparison representation.

## Compute Cache makes key construction explicit
Compute Cache uses a caller-defined computation type plus an `AEGP_GUID` key. Adobe's guidance is to mix every semantic input required to produce the cached value. For layer/frame dependencies, a host state receipt/hash should represent the relevant inputs rather than hashing rendered pixels after doing the expensive work.

The key should also include algorithm/schema/version information whenever changing implementation would change the derived value.

A cache key is therefore a semantic contract:

`key equality => recomputation would produce an interchangeable cached value`.

If that implication is false, the key is incomplete even if it has excellent statistical hash quality.

## Identity chain versus validity relation
A useful layered model is:

`project/persistent identity -> evaluated dependency state -> render-request identity -> result receipt/state -> residency entry`.

Different APIs can sit at different points in this chain. A Canvas receipt can answer whether a previously rendered effect prefix is still valid in a current context; a BEE Render GUID can fingerprint evaluated/request state; a Compute Cache key can identify arbitrary plug-in-derived data; a PF State can represent selected host-owned dependency state.

Do not assume two opaque GUID/receipt types should compare directly merely because both ultimately participate in caching.

## Failure modes
- omit one hidden/external dependency from a Compute Cache key -> deterministic stale reuse;
- key by persistent object ID but ignore time/render options -> stale frame;
- hash output pixels to build the key -> compute first, defeating the cache's purpose;
- include transient pointer/handle values -> cache misses across equivalent states and potential address-reuse bugs;
- include view-only/UI state in final-render identity -> false invalidation;
- forget algorithm/schema version -> reuse old derived representation after code update;
- treat cache miss as evidence that semantic state changed -> residency/eviction can also cause misses.

## Controlled identity experiments
Construct pairs of project states that differ in one dimension while holding output pixels intentionally equal, and pairs that preserve project object identity while changing evaluated output. Compare PF state equality, Compute Cache key, Canvas receipt status, BEE/TDB trace/GUID footprint and actual output hash.

Undo/redo is especially useful: when semantic state returns to an earlier value, a content-derived identity may converge and permit reuse even though edit history differs.

## Unknown frontier
Still unresolved: whether BEE/TDB Render GUIDs are deterministic solely from semantic state or incorporate generation/process salt, exact relation between RG cache-node keys and BEE GUIDs, whether Canvas receipts embed or reference a render GUID, and which render-context dimensions are mixed at which layer.

Related: `docs/evaluation/dirty-invalidation.md`, `docs/state-model/object-identity.md`, `docs/temporal-system/temporal-dependencies.md`, `docs/host-integration/cpp-sdk/host-compatible-hash-state.md`.
