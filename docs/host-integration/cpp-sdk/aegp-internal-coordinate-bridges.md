---
status: active
last_verified: 2026-09-15
---
# AEGP Coordinates at the BEE/TDB Boundary

Public AEGP objects should be modeled as host-owned coordinates, not as independent data structures whose opaque handles merely hide implementation details. Installed AE 2025 runtime symbols expose explicit normalization bridges from AEGP collection/stream coordinates into BEE/TDB identities.

## Public coordinate forms
The 25.6 SDK represents selections and streams with combinations such as:

- `AEGP_EffectCollectionItem = (AEGP_LayerH, effect index)`
- `AEGP_LayerStreamCollectionItem = (AEGP_LayerH, AEGP_LayerStream)`
- mask/effect stream collection variants
- `AEGP_CollectionItemV2`, which additionally carries `AEGP_StreamRefH`

These are public, supported values. Their containing handles remain host-owned and opaque.

## Runtime normalization bridges
`MEE.dll` exports conversions that place public AEGP coordinate types and internal BEE/TDB types in the same signatures. Reproducible examples are inventoried in `datasets/ae-2025-aegp-internal-bridges.csv`.
Observed bridge families include:

- AEGP effect/stream/mask/keyframe collection items -> corresponding `BEE_*Spec`
- `_AEGPp_Stream*` -> `BEE_StreamSpec`
- `(BEE_Layer*, AEGP_LayerStream)` -> `TDB_StreamIDPath`
- `TDB_StreamIDPath` -> `AEGP_LayerStream`
- `AEGP_MaskStream` -> `TDB_MatchName`
- layer-parameter IDs <-> BEE layer parameters

This supports the semantic chain:

`public AEGP coordinate -> MEE normalization -> BEE/TDB stream identity -> dependency/render systems`

The final step is supported by separate TDB RenderGuid and BEE/RG evidence; it must not be collapsed into a single undocumented function call.

## Why this matters for plug-in design
An effect index or layer-stream enum is an address into host state, not necessarily a persistent semantic identity. Reorder, insertion, duplication and topology edits can change which BEE/TDB object that coordinate resolves to. When the SDK provides persistent IDs, match names, receipts or state-comparison APIs, use those contracts instead of persisting raw host pointers or reverse-engineered internal addresses.

## Hard boundary
AEIG documents these bridges to explain host behavior. It does not endorse dereferencing `AEGP_*H`, manufacturing BEE/TDB objects, or linking to unsupported exports. Ownership, allocator, thread, generation and invalidation contracts remain internal unless independently established.

## Version boundary
The observed normalization symbols come from the installed AE 2025 runtime and are not a promise that earlier/later builds use identical private class names. Public AEGP coordinate types themselves have evolved: collection variants gained richer stream references, StreamSuite6 added session-unique stream IDs, and StreamSuite7 adds layer render-stage identity.

Therefore reverse mappings must be version-scoped even when the public semantic concept remains stable.

## Why normalization exists
Public coordinates intentionally compress host state into supported values: layer handle + enum/index, stream ref, match name or collection item. The host must resolve these against current project topology before evaluation. That resolution step is exactly where reorder/insertion, dynamic groups and source/stage changes can alter meaning.

A robust conceptual pipeline is:
`supported coordinate -> validate owner/generation -> normalize semantic stream/path -> evaluate at time/context -> mix into dependency/render identity`.

## Experiments
Track one selected property through effect insertion/reorder, mask insertion, keyframe mutation and duplicate/precompose. Reacquire public coordinates each step and compare generated AEGP bridge inventory/trace evidence, stream IDs, Match Names and render identity.

Test both stable semantic locators and fragile numeric indices. The expected difference is that supported reacquisition can follow the intended semantic object while stale indices/handles can resolve differently or become invalid.

## Failure classes
- cache raw collection/effect index across topology mutation;
- assume `_AEGPp_Stream*` address equals persistent property identity;
- manufacture internal `TDB_StreamIDPath` from guessed layout;
- use a bridge symbol from one binary version as if it were a public ABI;
- treat reverse conversion as lossless when the public coordinate type cannot express newer semantic dimensions.

## Unknown frontier
Unresolved: exact normalization ownership between MEE/BEE/TDB in current 26.x; how StreamSuite7 stage is represented in internal paths; whether public session-unique Stream IDs are derived from or merely correlated with TDB IDs; normalization/cache behavior for large dynamic property trees.

Related: `docs/state-model/streams-properties.md`, `docs/state-model/object-identity.md`, `docs/capability-recipes/stable-object-references.md`, `datasets/ae-2025-aegp-internal-bridges.csv`.
