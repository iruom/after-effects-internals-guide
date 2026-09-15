---
status: active
last_verified: 2026-09-16
---
# BEE Evaluation Runtime

`BEE` is one of the clearest internal seams exposed by the installed After Effects runtime, but it is **not** a public SDK namespace and AEIG does not treat its exported names as supported APIs. The evidence supports a working model in which BEE sits between project/stream state and lower-level render-graph execution, carrying render-relevant state, request identity, scheduling, cache interaction and specialized evaluated representations.

A useful provisional boundary is:

`project / AEGP / TDB streams -> BEE evaluated state + render options + identity/work queues -> RG graph/cache execution -> image/materialized result`

This is a reconstruction from binary linkage, exported/imported symbol vocabulary and trace categories. It is not a claim about Adobe's private class ownership or source layout.

## Direct runtime evidence

The reproducible inventory `datasets/ae-2025-render-identity-symbols.csv` contains 124 render/identity-related surfaces: 106 associated with `BEE.dll` and 18 with `RG.dll`. Within that set, 93 are classified as identity-related, 30 as RG/cache-graph related, and one as an explicit work-queue render-GUID route.

BEE exports include render-identity mixers for layer flags, transforms, lights and time-varying stream values. Examples include `MixInGuidForLayerFlags`, `MixInGuidForTransform`, `MixInGuidForLights`, and multiple `MixInValueAtTime` implementations using `dvacore::utility::Murmur3MixerState`.

That vocabulary is strong evidence that internal render identity is assembled from render-relevant state rather than from a simple `(layer, frame)` address.
## TDB -> BEE state boundary

`BEE.dll` imports TDB render-identity operations including `TDB_Stream::GetRenderGuid`, `TDB_Stream::MixInValueAtTime`, and `TDB_MixInTime`. Together with BEE-side `MixInValueAtTime` methods, this supports a model where stream state and evaluation time cross from the TDB/property representation into BEE's render-relevant identity domain.

The bridge is visible from the public-host side as well. `datasets/ae-2025-aegp-internal-bridges.csv` records MEE runtime exports such as `LayerStreamToBEEStream`, `AEGPMaskStreamToBEEMaskStream`, collection-to-BEE-spec conversions, and BEE/TDB-to-AEGP stream translations. These are internal bridge artifacts, not callable recommendations, but they show that the public AEGP object model is translated into different internal stream/spec representations.

Do not assume that `AEGP_StreamRefH`, a TDB stream ID/path and a BEE stream object have identical identity or lifetime. The existence of conversion helpers is evidence for a boundary, not for pointer or ABI equivalence.

## BEE -> RG execution boundary

The installed `BEE.dll` directly imports `RG_Traverser::PreRenderGraph`, both observed `RG_ExecuteGraph` overloads and multiple `RG_CacheNodeBase` methods such as `CacheIsValid`, `IsValidCacheNodeData`, `ChildRequestHook`, `PreRender`, `Render`, content-bounds queries and GPU-support checks.

This is stronger than naming similarity: BEE code has a binary dependency on the render-graph module. AEIG therefore places graph/cache execution below or adjacent to BEE, while leaving exact object ownership open.

The practical non-equivalence is important for developers: one project layer should not be assumed to map to one BEE object, one RG node, one cache entry or one pixel buffer. Collapsed transformations, track mattes, effect-prefix receipts, 2D/3D binning and intermediate materialization all permit one-to-many or many-to-one relationships.

See `docs/render-graph/render-graph-model.md` and `docs/cache-system/state-identity.md` for the neighboring boundaries.
## Scheduling and work queues

A dedicated export, `BEEp_WorkQueue_GetRenderGuidWithRO`, accepts layer render options and returns a GUID through a work-queue callback path. This indicates that render identity is needed while work is being scheduled, before final pixels necessarily exist.

That distinction helps separate four concepts that plug-in code often accidentally conflates:

1. **request identity** — whether two requested computations represent the same render-relevant state;
2. **validity** — whether a previously computed result still satisfies the request;
3. **scheduling** — when and where the request is executed;
4. **residency** — whether the materialized result remains available in memory/disk caches.

A stale preview, unexpected recomputation or apparently duplicated work can originate in different layers of this chain. Treating all four as "the cache" makes debugging harder.

## Observability vocabulary

Retained Trace Database profiles expose categories including `BEE_Eval`, `BEE_Cache`, `BEE_CacheLog`, `BEE_Project`, `BEE_Undo`, `BEE_WorkQueue` and `BEE_VectorArt`. `datasets/ae-debug-trace-lineage.csv` keeps stable and beta lineage rather than treating a category name as timeless.

Trace names are observability vocabulary, not semantic contracts. A category surviving across releases does not prove that the corresponding subsystem retained the same ownership, event format or threshold ABI. The dvacore trace ABI itself changed between the locally studied 25.6 and 26.3 builds; see `docs/observability/trace-database.md`.

## Developer-facing implications

For public plug-in development, BEE is most useful as an explanatory model, not an integration target. If an effect forgets a dependency, mixes an incomplete state key, assumes frame-local identity, or violates host threading/context rules, the visible symptom may occur much later in BEE/RG scheduling or cache reuse.

When debugging an apparent host bug, ask which upstream state should have contributed to identity, whether the SDK contract actually registered that dependency, and whether the render request changed context (time, ROI, pixel format, renderer, GPU path, layer flags, transforms or upstream source state). This is more actionable than attempting to call an undocumented BEE export.
## Failure patterns and interpretation

Evidence currently supports several classes of failure without assigning every symptom to BEE itself:

- **identity omission:** a render-relevant input is absent from the host-visible dependency/state model, allowing inappropriate reuse;
- **identity over-invalidation:** state that should be irrelevant is mixed into identity, producing unnecessary recomputation;
- **context mismatch:** the same UI state is requested under different render options, ROI, renderer or execution path;
- **lifetime mismatch:** public handles or sequence data are retained beyond their documented lifetime even though internal state has moved on;
- **thread/context misuse:** a host API is called from an execution context where it is not valid, while the resulting symptom appears in evaluation/rendering.

These are diagnostic categories, not claims that BEE is the defect source. AEIG should preserve that distinction when documenting regressions and host quirks.

## Version and falsification work

The strongest BEE model is currently anchored by installed AE 2025 binary archaeology plus 25.6/26.3 trace work. Exact class layouts, non-exported methods and historical ownership remain outside the retained corpus. Names visible in one build must therefore be version-scoped.

The canonical `EXP-RG-001` experiment is designed to correlate a controlled Blur-only mutation with BEE/TDB/GUID/RG/cache trace footprints inside real render windows. A result that shows no expected identity or graph footprint is allowed to refute the current model; it must not be rewritten into a confirmation.

High-value next experiments include property edit vs undo, source replacement, temporal-only changes, collapse-transform changes, ROI-only requests, CPU/GPU path switches and vector/text mutations while correlating public callback activity with BEE/RG/TDB traces.

## Open questions

- Which BEE objects are persistent project/evaluation objects versus request-local render objects?
- Where exactly is the boundary between TDB stream identity and BEE render identity?
- Which fields of render options are mixed directly into GUIDs, and which instead alter graph topology or cache namespace?
- How are `BEE_VectorArt` and other evaluated representations materialized and invalidated?
- Which work queues correspond to MFR, UI-thread rendering, background cache fill and media/decode work?
- Which BEE names are long-lived architecture and which are implementation vocabulary that can disappear between releases?

Until those questions are experimentally closed, BEE should be treated as a strongly evidenced **internal architectural seam**, not a completely reconstructed private API.
