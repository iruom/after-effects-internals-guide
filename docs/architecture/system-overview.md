---
status: active
last_verified: 2026-09-16
evidence: public SDK contracts + local runtime exports/imports + trace/debug lineage + controlled experiments
---
# System Overview

AEIG models After Effects as a set of connected state/evaluation/execution systems rather than as one monolithic "composition renderer". The visible project tree is only one representation; render-time identity, scheduling, media decode, graph materialization, caches and UI/extension state live on different boundaries.

## High-level execution chain

```text
Editable Project / UI State
        |
        v
Persistent items, layers, properties, streams, expressions
        |
        +--> project save / AEP-AEPX / sequence-data persistence
        |
        v
Evaluation / dependency state (TDB/BEE-facing)
        |
        +--> time/value sampling
        +--> expressions
        +--> source/media requests
        +--> temporal/upstream dependencies
        v
Render request identity / receipts / GUIDs
        |
        v
BEE scheduling / work queues / render options
        |
        v
RG graph expansion / pre-render / cache nodes / transforms
        |
        +--> CPU effect/render work
        +--> GPU execution paths
        +--> MediaCore decode/frame residency
        +--> audio parallel pipeline
        v
Worlds / frames / output + RAM/disk/playback caches
```

## State is not one object
A project item/layer/property is the editable semantic object seen by users and APIs. Render execution can operate on derived/snapshotted state, evaluated streams and host-created render contexts. UI callbacks, render threads and media/decode workers should therefore not be assumed to share one mutable object graph.

This separation is visible in several independent contracts: post-13.5 UI/render synchronization rules, MFR const render-time sequence state, asynchronous custom-UI checkout, Canvas/Artisan render contexts, receipt validity and timestamp APIs.

## TDB / stream layer
TDB vocabulary and BEE imports expose stream-oriented value/time identity beneath project-facing properties. Local binaries show `TDB_Stream::GetRenderGuid`, value-at-time mixing and explicit AEGP/MEE bridges that translate public layer/mask stream concepts into BEE/TDB-side identities.

Do not equate a property handle with its evaluated value, its stream identity or its contribution to a render GUID.

## BEE boundary
Local `BEE.dll` surfaces connect layer/item render options, GUID mixing, source/media bridges, work queues and direct imports from `RG.dll`. AEIG therefore uses BEE as the strongest observed boundary between evaluated project/request state and lower graph/scheduling execution, while keeping exact private class ownership provisional.

## RG boundary
`RG_CacheNodeBase`, `RG_XformNode`, `RG_ExecuteGraph` and `RG_Traverser::PreRenderGraph` provide direct evidence for a graph runtime distinct from the project tree. One project layer need not correspond to one render node, one texture or one cache entry.

Collapse transformations, track mattes, effects, ROI/bounds, 2D/3D bins and temporal dependencies are all reasons graph topology/materialization can differ from visible hierarchy.

## Media and audio are parallel substrates
Media decode has its own asset/content identity, async request queues and frame residency before downstream composition identity is formed. Audio likewise has conform/source residency, prefetch, processor/mix state and device/output buffering. Neither should be reduced to "another RG node" without evidence.

The same source media can remain decode-resident while composition/effect state invalidates downstream pixels. Conversely, changing source content can invalidate decode-derived data even when the composition topology is unchanged.

## Cache is plural
AEIG distinguishes at least:
- semantic/render identity;
- validity/sufficiency;
- resident value/materialization;
- eviction policy;
- disk persistence;
- playback/preview residency;
- plug-in Compute Cache state.

A cache hit in one layer does not imply all downstream layers are reusable. Receipt validity, BEE/RG cache nodes, MediaCore frame caches, disk cache and Compute Cache are related but not interchangeable namespaces.

## UI, scripting and extension planes
Scripting, expressions, AEGP, effects, AEIO, Artisans, CEP/UXP and command-line interfaces are observation/control surfaces around the system. They expose different lifetimes, threads and support contracts. An identifier visible in a binary or first-party extension is not automatically a supported third-party API.

UI/view state also differs from document/render state. Viewer zoom, channels, exposure or panel state may affect presentation without participating in final render identity, while project property changes can invalidate render state without changing the current UI layout.

## Debugging by boundary
When a result is wrong, first locate the failing boundary instead of treating AE as a black box:
1. Did editable/persistent state contain the intended value?
2. Was stream/expression evaluation correct at the requested time?
3. Did request identity include the changed dependency?
4. Was the render graph/materialization path legal for the context?
5. Did CPU/GPU/media execution produce the expected intermediate?
6. Was a stale cache/receipt incorrectly accepted?
7. Was the mismatch only interactive/display state rather than final pixels?

This boundary-first diagnosis is what lets the Guide answer implementation questions rather than only enumerate APIs.

## Version model
No arrow in this diagram is assumed ABI-stable across AE history. CC 2015's render-side architecture changes, MFR, modern 3D, evolving MediaCore, CEP/UXP integration and private trace ABI drift all demonstrate that the same conceptual boundary can move while public names survive.

Every detailed page should therefore state version/evidence scope. "Observed in AE 26.x" is stronger than timeless wording when the lineage is unknown.

## Evidence discipline
The diagram combines multiple evidence classes. Public SDK behavior is a support contract; distributed headers reveal additional structure; binary imports/exports reveal runtime-visible relationships; trace/debug vocabulary exposes observation points; controlled experiments establish behavior. None alone is permission to invent private source-level semantics.

## Cross-links
Start with `docs/foundations/scope-and-coverage-model.md`, `docs/evaluation/evaluation-model.md`, `docs/cache-system/state-identity.md`, `docs/render-graph/render-graph-model.md`, `docs/media-system/runtime-architecture.md`, `docs/audio-system/runtime-architecture.md`, `docs/threading-system/overview.md`, and `docs/persistence/aep-binary-model.md`.

## Unknown frontier
AEIG does not possess Adobe private source code. Exact private object layouts, graph construction heuristics, scheduler policy, cache-key representation and many first-party-only bridges remain open unless independently observed. The purpose of this overview is to make those unknowns localizable and testable, not to hide them behind a plausible diagram.
