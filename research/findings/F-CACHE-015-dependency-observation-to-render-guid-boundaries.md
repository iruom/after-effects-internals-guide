---
status: strong-structural-correlation
last_verified: 2026-09-15
evidence: AE-25.6-headers + AE-2025-export-import-surface
---
# F-CACHE-015 — Dependency observation and render identity meet at explicit boundaries

AE's public Effect API and the installed AE 2025 binary surface expose adjacent pieces of a dependency-to-identity pipeline, but they must not be collapsed into one undocumented function chain.

## Public dependency/state side
`PF_OutFlag2_AUTOMATIC_WIDE_TIME_INPUT` tells AE to track parameter checkouts so over-time dependencies are known by the host.

The retained `PF_HaveInputsChangedOverTimeSpan()` contract is unusually explicit: when a queried span is unchanged, the plug-in may reuse its own cache **and** AE's internal cache records a temporal dependency on that span so later upstream changes invalidate dependent frames.

Current `PF_GetCurrentState()` / `PF_AreStatesIdentical()` generalize input-state comparison over a selected parameter set and time range. For simulation effects using automatic wide time, the queried range is expanded to include times needed to produce that range.
## Public explicit-extra-dependency side
With `PF_OutFlag2_I_MIX_GUID_DEPENDENCIES`, SmartFX PreRender receives `GuidMixInPtr`. Adobe's header says the plug-in mixes additional render-relevant state into AE's internal GUID for the cached frame, allowing AE to detect an already-existing frame instead of forcing unconditional invalidation.

This proves that host-inferred dependencies and plug-in-supplied dependency bytes can both participate in cached-frame identity. It does **not** prove that `PF_State` itself is serialized or hashed directly into that GUID.

## Installed AE 2025 render-identity surface
`BEE.dll` exports render-GUID formation at several levels:
- `BEE_RenderOptions::GetRenderGuid`, `BEE_LayerRenderOptions::GetRenderGuid`;
- Layer/AVLayer/CompItem `GetRenderGuidWithRO`;
- `BEE_RenderGuidCache<LayerRenderOptions>` and `<ItemRenderOptions>` accessors;
- `MixInGuidForLayerFlags`, `MixInGuidForTransform`, `MixInGuidForLights`;
- multiple `MixInValueAtTime(..., Murmur3MixerState, A_Time, ...)` paths.

BEE also imports `TDB_Stream::GetRenderGuid`, `TDB_Stream::MixInValueAtTime`, and `TDB_MixInTime`, giving a concrete stream/time-to-render-identity boundary.
## Scheduling and graph boundary
`BEEp_WorkQueue_GetRenderGuidWithRO` takes `BEE_LayerRenderOptions` and supplies a `Guid` through its callback path. This places render GUID generation directly on a work-queue surface rather than only inside passive cache metadata.

Separately, `BEE.dll` has a direct PE dependency on `RG.dll` and imports `RG_CacheNodeBase` construction/validation/render methods, `RG_Traverser::PreRenderGraph`, and `RG_ExecuteGraph`.

`RG_CacheNodeBase` itself exports `CacheIsValid`, `IsValidCacheNodeData`, `ChildRequestHook`, `PreRender`, and `Render`. Thus BEE-side request/identity/scheduling code and RG-side render/cache graph code are linked modules in the installed product.

## Strongest model currently justified
```text
parameter / stream / host-state observation
        ↓
temporal + semantic dependency registration
        ↓
state equivalence / render options
        ↓
render-GUID formation and explicit extra mix-ins
        ↓
work-queue request identity
        ↓
RG pre-render / cache-validity / graph execution
```

The arrows are architectural adjacency/correlation except where the public headers explicitly state dependency registration or GUID mixing. A literal call chain from `PF_State` to `BEEp_WorkQueue_GetRenderGuidWithRO` remains unproven.
## Reproducible artifact
- `probes/process-tools/inventory_render_identity_symbols.py`
- `datasets/ae-2025-render-identity-symbols.csv`

## Next discriminating experiments
1. Toggle one stream value at one time and correlate trace `MixHashGuid` / Render-GUID activity with cache invalidation.
2. Compare automatic-wide-time checkout ranges against upstream edits outside/inside the observed span.
3. A-B-A a render-relevant stream value and test whether the earlier frame identity becomes reusable.
4. Add a non-stream dependency only through `GuidMixInPtr` and compare receipt GUID/cache reuse with under-mixed and correctly mixed variants.
5. Repeat under collapsed transformations to test project topology versus effective render-context topology.