---
status: active
last_verified: 2026-09-15
---
# Terminology

AEIG uses terms narrowly because After Effects has several unrelated mechanisms that would otherwise collapse into the same word.

## State terms
- **Project state**: editable/persistent document semantics such as items, layers, streams and settings.
- **Render-side state**: the synchronized/evaluated state used to answer a render request; not assumed pointer-identical to project/UI objects.
- **View state**: presentation/editor state associated with a viewer or panel, such as guide visibility/snap/lock.
- **Snapshot**: a coherent render/evaluation view of mutable project state. This is an architectural boundary, not a claim about one serialization blob.

## Identity terms
- **Persistent ID**: documented object identity intended to survive a defined persistence scope.
- **Handle/reference**: host-owned access token with suite-defined lifetime; never automatically a stable ID.
- **Render GUID**: render-state fingerprint used by BEE/TDB-style request/cache paths.
- **Receipt**: proof/status object tied to a render result/request context; not synonymous with GUID.
- **ContentState/DocumentID**: media identity vocabulary, distinct from compositing identity.

## Rendering terms
- **Stream/property**: persistent semantic parameter/data source.
- **Render request/options**: time, stage, ROI, downsample, channel/decode and related coordinates describing requested output.
- **Render node**: request-specific RG execution/planning object, not automatically a project object.
- **Checkout**: host-mediated acquisition of input/materialized data that can also register dependencies.
- **Temporal footprint**: source-time interval/set on which an output depends.
- **Bounds/ROI**: spatial planning information; valid bounds do not imply valid pixels.

## Cache terms
AEIG separates **identity**, **validity**, **residency**, **pin/lease** and **eviction policy**. A cache hit/miss is therefore not one universal boolean mechanism.

Avoid using `DAG`, `node`, `cache`, `ID`, `dirty`, `frame` or `GUID` without identifying the subsystem and evidence surface.
## Evidence qualifiers are part of the term
AEIG terms are version- and evidence-scoped. “Render GUID observed in BEE exports” is a different statement from “documented public GUID contract”, even when both contain the words render and GUID.

When a term comes from a private symbol, trace category, preference key, sibling Adobe host or community parser, retain that provenance instead of silently upgrading it to an AE public concept.

## Version-sensitive vocabulary
The same user-facing word can change implementation role over time. “Disk cache” is a concrete example: older Global Performance Cache documentation and current disk-backed preview playback describe materially different roles. Likewise “thread-safe effect” before and after MFR/13.5 refers to different host concurrency assumptions.

## Failure patterns caused by vocabulary collapse
Many implementation bugs begin as terminology bugs: treating a handle as a persistent ID, a cached file as a valid result, a layer as a render stage, a project time as layer/source time, or a loaded DLL as proof of feature ownership.

Whenever two terms are about to be equated, state the conversion/evidence that justifies it.

## Research experiment rule
A useful experiment changes one coordinate named by the terminology while holding the others constant: identity without residency, residency without semantic state, view state without project state, or render stage without source layer identity. If the supposed distinction produces no observable difference across a discriminating corpus, the model should be revised.## Unknown terminology
Private Adobe vocabulary is retained even when ownership is unresolved, but it should be labeled as an observed name rather than expanded into a guessed acronym or class role. If no authoritative expansion exists, AEIG leaves the name unexplained.

Terms such as BEE, TDB and RG are therefore tied to observed modules/classes/categories and measured behavior, not invented backronyms.

## Cross-links
See `evidence-model.md`, `cross-host-triangulation.md`, `../state-model/object-identity.md`, `../temporal-system/time-model.md`, `../render-graph/layer-pipeline-stages.md`, and `../cache-system/cache-architecture.md` for the boundaries summarized here.