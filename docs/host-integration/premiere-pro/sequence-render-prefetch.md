---
status: active
last_verified: 2026-09-14
---
# Premiere Sequence Render and Media Prefetch

Premiere's `PrSDKSequenceRenderSuite` exposes a render pipeline that is useful as a cross-host probe for MediaCore behavior below the After Effects Effect API.

## Renderer identity
A caller creates a video renderer with a plugin/timeline identity and frame rate, receives a renderer ID, renders frames through that ID, and releases it explicitly. Timeline- and stream-label-specific renderer constructors show that the render session identity can include both timeline and logical stream selection.

## Render parameters are part of semantic identity
Frame requests include an ordered pixel-format preference list, dimensions, pixel aspect ratio, render quality, field type, deinterlace policy, deinterlace quality and composite-on-black. Later revisions add color-space and export-LUT identifiers.

This strongly suggests that a reusable frame cannot be identified by timeline time alone. The output contract depends on render-configuration state.

## Prefetch is media preparation, not speculative pixel rendering
`PrefetchMedia` asks importers to begin reading media needed for a future video-frame render. Parameter-aware variants pass the same render description used by the final render request. Color-managed variants add color-space identity.

The suite separately exposes cancellation of outstanding prefetches and readiness queries, so prefetch has its own asynchronous lifecycle distinct from final frame production.

### Architectural model
`timeline request -> dependency/media discovery -> importer prefetch -> decode/import cache -> intermediate/render graph -> final PPix`

Prefetch therefore belongs before the pixel render boundary. It is best modeled as a dependency-warming operation whose usefulness can disappear when the render request changes.
## Cache-policy flags
`PrRenderCacheType` exposes independent policy bits for imported frames, imported still frames, intermediate frames, rendered frames, rendered still frames, and persistent prefetch. This is direct evidence that MediaCore does not treat frame caching as one homogeneous layer.

A useful cross-host comparison is:
- importer/decode cache;
- still-frame specializations;
- intermediate graph results;
- final rendered output;
- persistent prefetch state.

AE's public cache UI collapses more of these distinctions, but local traces and Compute Cache/Media Cache behavior indicate similarly layered mechanisms internally.

## Async render ownership
Async Sequence Render returns a `PPixHand` through a completion callback. The callback contract requires the receiver to dispose the returned PPix. Cancellation and completion are therefore separate from image ownership.

## Research tests
- Change only requested pixel-format order and observe cache/prefetch reuse.
- Change render quality without changing dimensions or time.
- Compare color-space/LUT-only changes.
- Queue prefetch, mutate timeline state, then test whether outstanding work is cancelled or simply rejected at consumption.
- Compare imported/intermediate/rendered cache flags under identical export requests.
## Temporal repeat metadata
Sequence Render exposes `repeatCount` both through `GetFrameInfo` and the frame-render return record. The returned frame may therefore be declared reusable for a contiguous run of output frames.

The exporter is explicitly expected to represent those repeats appropriately for its format, for example through null/repeat frames or duration changes. This is a temporal compression/reuse signal distinct from ordinary frame-cache lookup.

The render return also carries marker presence separately from pixel output, showing that per-frame timeline metadata can travel alongside a reusable image.

## Prefetch readiness identity is partially opaque
Parameter-aware prefetch receives the full render-parameter record, but `IsPrefetchedMediaReady` queries readiness only with renderer ID and time. The public API therefore does not expose every dimension used by readiness bookkeeping.

Experiment: prefetch the same time with two incompatible format/quality/color requests and test readiness/cancellation ordering. This can reveal whether the renderer session tracks multiple variants, replaces the prior request, or treats media readiness as decode-independent.

## Version and failure boundary
Later Sequence Render revisions add color/output interpretation fields while the prefetch/readiness APIs retain their own identity surface. This shows why scheduler/readiness identity can evolve differently from final frame identity.

Failure modes include warming media for an obsolete render generation, treating readiness=true as proof that the final render contract is cached, forgetting to cancel old prefetch after timeline/request mutation, and reusing repeat metadata after a semantic edit that breaks the repeated-frame run.

## AE comparison
Use Premiere prefetch as a concrete model for separating **dependency warming** from speculative final-pixel rendering. In AE, MediaFoundation prefetch/decode queues and BEE speculative render work must be traced separately before claiming the same mechanism.

## Unknown frontier
Unresolved: how readiness variants are keyed internally; whether persistent prefetch survives process/project boundaries; exact interaction with PPix cache retention; whether AE exposes comparable media readiness state below its public render APIs.

Related: `docs/media-system/runtime-architecture.md`, `docs/evaluation/work-queues.md`, `docs/render-graph/render-tasks.md`, `docs/foundations/cross-host-triangulation.md`.
