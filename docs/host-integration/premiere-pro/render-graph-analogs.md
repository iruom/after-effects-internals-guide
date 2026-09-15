---
status: active
last_verified: 2026-09-14
---
# Premiere Render-Graph Analogs

Premiere 26.0 exposes a graph-like render contract much more directly than AE's public API. `PrSDKVideoSegmentRenderSuite` addresses timeline nodes, clip nodes, effect operators and transition nodes explicitly.

## Operator-range rendering
`ApplyOperatorsToFrameAsync` accepts an operator start index and operator count. A caller can therefore render a contiguous subrange of an effect/operator stack, optionally supplying the input frame itself.

This is a strong sibling-host analog for AE's older Canvas receipt APIs, where a receipt can represent a layer with the first N effects rendered. It does not prove shared implementation, but both hosts expose intermediate effect-stack state as a meaningful render boundary.

## Node vs operator distinction
Premiere comments state that `ProduceFrameAsync` is suitable for input-like nodes but not effect/operator nodes. Operators are invoked through a separate call family. This suggests an explicit semantic distinction between data-producing graph nodes and transform/operator stages.

## Two time coordinates
Every node/operator render can carry both containing-sequence time and node-relative segment time. The sequence time is specifically needed when a filter requests other media during its own render.

AEIG should test whether AE's comp-time/layer-time distinction and temporal checkouts play an analogous role without assuming common implementation.

## Cache identity pairing
Most async render entry points have a matching `GetIdentifierFor...` function documented as allowing cache lookup before render. Request description and cache identity are therefore deliberately paired at API level.

## Completion can precede API return
The async render comments explicitly warn that the completion callback may run before the initiating function returns. `outRequestID` is therefore useful mainly for later cancellation, not as a guarantee that the request is still pending when control returns.

This is a classic reentrancy hazard. Caller state needed by the completion path must be fully initialized *before* invoking the request, and code must tolerate completion occurring inline or on another host-managed execution path.

## Request identity and execution are separate APIs
The paired `GetIdentifierFor...` calls take essentially the same semantic inputs as their render counterparts. This is strong evidence for a deliberate two-phase model:

1. canonicalize/hash the render request into an identifier;
2. consult cache or dependency state;
3. launch execution only if necessary.

AE's Render GUID/receipt system should be compared against this separation rather than assuming GUID generation happens only after rendering begins.
## Request semantics evolve without replacing the graph API
Later suite revisions add `imRenderContext`, effect bypass and color-managed extended render parameters while retaining the same node/operator model. This is a useful modernization pattern: keep graph topology stable while extending render-context semantics.

The paired identifier functions also evolve with render semantics. For example, bypassing non-intrinsic effects is included in newer identifier calls. This strongly suggests that cache identity must evolve in lockstep with any option capable of changing pixels.

## Clip descriptor negotiation and prefetch
The suite separates `SelectClipFrameDescriptor()` from `InitiateClipPrefetch()`. A caller first negotiates a source-native/closest frame descriptor, then prefetches a media-time frame in that descriptor. This cleanly separates capability negotiation from asynchronous data acquisition.

## Developer lessons
- Initialize completion-visible state before issuing an async request.
- Put every pixel-relevant render option into request identity.
- Keep cache-ID generation callable without forcing expensive execution.
- Separate source-format negotiation from rendering/prefetch.
- Model sequence/timeline time and node-relative/media time as distinct coordinates.