---
status: active
last_verified: 2026-09-16
evidence: AEGP Stream/Dynamic Stream contracts + scripting property behavior + local TDB/BEE stream/path runtime surfaces
---
# Streams and Properties

Streams are one of the most important semantic abstractions in AE. Public AEGP documentation states that effect parameters, layers, masks and shapes are conceptually handled as streams, while scripting exposes a related hierarchy of properties and property groups.

AEIG treats these as correlated surfaces over a property/evaluation system, **not** as guaranteed 1:1 wrappers around one private class.

## Public stream model
An `AEGP_StreamRefH` identifies a host-owned stream access path. Streams may represent layer properties, effect parameters, masks/text/paint dynamic properties and other time-varying or static semantic values.

Key distinctions:
- `AEGP_CanVaryOverTime`: the stream type can be animated;
- `AEGP_IsStreamTimevarying`: current effective state varies over time and includes expressions;
- keyframe enumeration: authored keyframe data;
- `AEGP_GetNewStreamValue(..., pre_expressionB)`: evaluate before or after expressions.

Therefore **can vary**, **has keyframes**, **is time-varying**, and **evaluated value changes** are different questions.

## Ownership and lifetime
New stream refs and stream values have explicit disposal rules. A stream ref is not a borrowed stable project pointer. Adobe's AEGP lifetime guidance warns that structural edits — even adding a keyframe — can invalidate refs.

Effect stream ownership adds another constraint: streams derived from an `AEGP_EffectRefH` must not outlive the checkout relationship that produced them.

Production rule: acquire close to use, copy only semantic data you own, dispose host refs promptly, and reacquire after topology changes.

## Path, match name and grouping identity
Dynamic Stream APIs expose named groups, indexed groups, match names, child indices and parent traversal. Scripting similarly distinguishes named and indexed property groups.

Indexed groups are structurally mutable; adding children may reconstruct the group and invalidate existing scripting references. Match names are generally stronger semantic selectors than display names, but a match-name path is still not a universal persistent ID because repeated/indexed children can share type/match-name structure.

A robust property address therefore needs some combination of:

`owner identity + hierarchical path + group/index semantics + match names + session/persistent IDs where available`.

## Session-unique stream identity
StreamSuite6, available from AE 22.5, adds `AEGP_GetUniqueStreamID`, returning a **session-unique** numeric ID. This is stronger than a raw handle but weaker than a documented cross-save property ID.

StreamSuite7 adds another independent coordinate for `PF_Param_LAYER`: the source layer and the render stage can be read/set separately. A layer-valued property is therefore not fully described by a bare layer ID.

## Internal TDB/BEE correlation
Local AE 2025 runtime inventory contains thousands of TDB/BEE stream-related symbols, including `TDB_StreamIDPath`, `TDB_MatchName`, `TDB_Stream`, `TDB_DerivedStream` specializations, stream factories, cloning parameters and BEE stream specifications.

UI and rendering code repeatedly pass `TDB_StreamIDPath` rather than raw private pointers when addressing properties. BEE also exposes value-at-time/render-guid mixing for specific stream types.

This strongly supports an internal model with hierarchical stream identity/path plus evaluated values, but it does not prove every scripting `Property` maps to exactly one `TDB_Stream` instance.

## Base versus derived streams
The runtime surface includes many `TDB_DerivedStream<...Traits>` specializations. This is evidence that some visible/evaluated properties can be computed or adapted from other semantic state rather than stored as one literal field.

AEIG therefore separates:
- **stored/authored state**: constants, keyframes, expressions and persistent settings;
- **derived/evaluated stream state**: value under time/context;
- **render-stage materialization**: pixels or renderer-specific output depending on those values.

This distinction matters for inspection tooling: a value visible to the user may be derived without having a writable persistent slot of the same form.

## Expression state is not only a UI checkbox
Older headers note that expressions can be disabled automatically by the parser during playback/error conditions. `AEGP_GetExpressionState` can therefore expose runtime expression state, not necessarily only the authored enable toggle.

Test syntax errors, runtime errors, cycles and playback-only failures while comparing scripting `expressionEnabled`, AEGP expression state, pre/post-expression values and render behavior.

## Structural mutation failure patterns
- retain scripting child references after adding to an indexed group -> invalid object/reference;
- retain AEGP stream refs after keyframe or topology mutation -> invalid opaque ref;
- use display names as semantic identity -> break on rename/localization/duplicates;
- use child index as permanent identity -> break on reorder/insert/delete;
- infer time invariance from no keyframes -> miss expressions/derived state;
- serialize `AEGP_StreamValue` native memory -> ABI/packing and ownership violation.

## ABI archaeology
Historical headers contain an explicit CodeWarrior 7.1 packing workaround for `AEGP_StreamValue`: extra padding would have broken binary compatibility. Native stream structs are ABI transport structures, not persistence formats.

## Controlled reconstruction matrix
For Effect, Mask, Text Animator and shape/property hierarchies:
1. capture scripting path/matchName/index;
2. capture AEGP stream ID/ref-derived metadata;
3. mutate value only;
4. add/remove/reorder sibling;
5. add/remove keyframe;
6. enable/disable or change expression;
7. save/reload;
8. compare AEP/AEPX diffs and TDB/BEE trace/render identity.

This separates address stability, handle lifetime, persistent identity and render identity.

## Unknown frontier
Still unresolved:
- mapping between public session-unique stream IDs and `TDB_StreamIDPath` internals;
- whether property persistent IDs are generalized internally beyond public scripting support;
- exact lifecycle of derived-stream objects across project snapshot/render cloning;
- how stream path identity changes under duplication/precompose/import;
- which evaluated stream states are mixed directly into render GUIDs versus represented through higher-level dependency identity.

Related: `docs/state-model/object-identity.md`, `docs/state-model/snapshots.md`, `docs/evaluation/bee.md`, `docs/persistence/aep.md`.
