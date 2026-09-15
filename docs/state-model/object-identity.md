---
status: active
last_verified: 2026-09-16
evidence: AEGP Item/Layer/Stream ID contracts + short-lived handle rules + local BEE/TDB render-identity symbols + media identity surfaces
---
# Object Identity

After Effects has multiple identity namespaces with different lifetime and semantic scopes. Treating them as one universal object ID is a common cause of stale references, cache errors and persistence bugs.

## Identity namespace table
| Question | Suitable identity | Scope |
|---|---|---|
| Same project item across save/load? | `AEGP_GetItemID` / documented Item ID | persistent across project saves/loads |
| Same layer during project lifetime? | `AEGP_GetLayerID` | stable for lifetime of the project |
| Same currently acquired host object? | AEGP handle/ref | short-lived; reacquire after structural edits |
| Same stream during current session? | `AEGP_GetUniqueStreamID` | explicitly session-unique from StreamSuite6/22.5+ |
| Same evaluated render state? | render GUID / PF state / receipt relation | request/evaluation/cache context |
| Same source media content? | media `DocumentID` / `ContentState` / decode identity | media subsystem scope |

These identities can coincide operationally without being interchangeable.

## Persistent/editor identity
`AEGP_GetItemID` returns an item ID documented to persist across project saves and loads. `AEGP_GetLayerID` returns a layer ID that does not change during the project lifetime.

Those contracts are stronger than pointer or handle identity, but their scopes are still different. A layer ID is not automatically a globally persistent database key outside its project, and an Item ID does not establish render equivalence.

## Handles are capabilities, not IDs
Adobe explicitly describes many AEGP references as "nasty, brutish, and short". Structural edits can invalidate them; even adding a keyframe can invalidate references to that stream. Render-queue item refs are invalidated when queue structure changes.

Therefore a handle means "the host currently grants access to this object through this opaque token", not "this is the object's durable identity".

Rules:
- do not serialize handles or pointers;
- do not retain them across arbitrary UI hooks, async generations or topology edits;
- reacquire from a stronger semantic identity/path when needed;
- dispose owned refs/values exactly according to suite contract.

## Stream/property identity
AEGP StreamSuite6, introduced in AE 22.5, adds `AEGP_GetUniqueStreamID`, explicitly described as returning a **session-unique** numeric ID. That scope is narrower than Item persistence.

A stream also has other address dimensions: parent hierarchy, match name, dynamic-stream index, layer/effect ownership and render stage. A `PF_Param_LAYER` stream in StreamSuite7 now carries both source-layer identity and an independently selectable pipeline stage.

Retained internal feature vocabulary such as `EnableTDBStreamScriptingIDs` suggests stronger internal stream identity experiments have existed, but AEIG does not promote private TDB IDs into a public persistence guarantee.

## Render identity is evaluated semantic identity
Local AE 2025 BEE/TDB surfaces expose render-guid construction at stream/layer/comp boundaries. Examples include `MixInGuidForTransform`, `MixInGuidForLayerFlags`, `MixInGuidForLights`, and `MixInValueAtTime` for stream values. This strongly supports a model where render identity is built from **render-relevant evaluated state**, not copied from project object IDs.

Thus the same Layer ID can legitimately produce many Render GUIDs as time, effects, render options, context, source state or dependencies change.

A useful distinction is:

`persistent object identity -> evaluated semantic state -> render fingerprint -> cached/materialized result`.

## Receipts and state objects are not GUID aliases
Canvas Render Receipts, Frame Receipts, `PF_State`, public `AEGP_GUID`/Hash Suite values and internal Render GUIDs all participate in identity/validity workflows, but their equality relation is not assumed bit-identical.

A receipt can encode "this result remains valid in this current context" without being the canonical semantic hash used elsewhere. A PF state is an opaque host receipt for selected input state, not a serialized parameter object.

## Media identity is another namespace
MediaCore/EAMedia exposes document/content identity, decode-request identity and GUID-keyed residency concepts. `ContentState` can change while the media document remains the same logical source. This is analogous to project object versus render-state identity but belongs to a different subsystem.

Do not use a file path alone as content identity: relink, growing media, proxies and external modification can preserve path while changing content semantics.

## Identity failure patterns
- store `AEGP_StreamRefH` and use it after a keyframe/topology edit -> invalid handle;
- use layer index as durable identity -> wrong object after reorder;
- use layer name as unique identity -> duplicate-name ambiguity;
- key a render cache only by persistent Layer ID -> stale output across evaluated-state changes;
- treat cancellation request ID as frame identity -> destroy useful cache reuse;
- treat media path as immutable source identity -> stale decode/cache after external change.

## Reconstruction experiments
Track a single semantic object through rename, reorder, keyframe insertion, duplication, precompose, save/reload, import and Undo. Record Item/Layer/Stream IDs, newly acquired handles, AEP/AEPX persistent references, Render GUID/receipt changes and output hashes.

A high-value result is an **identity transition table** showing which operations preserve each namespace and which replace it.

## Unknown frontier
Still unresolved:
- current relationship between TDB internal stream identity and public session-unique stream IDs;
- exact components mixed into each BEE Render GUID class;
- whether identical render state reached through different project histories converges to identical render GUIDs;
- relationship among Canvas receipts, RG cache-node identity and BEE render GUIDs;
- copy/paste/import remapping rules for persistent layer/item/property identity across projects.

Related: `docs/state-model/streams-properties.md`, `docs/state-model/snapshots.md`, `docs/evaluation/dirty-invalidation.md`, `docs/media-system/media-identity.md`.
