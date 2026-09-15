---
status: active
last_verified: 2026-09-15
---
# Recipe: Keep a Stable Reference to AE Objects

## Goal
Remember an item/layer/property across callbacks, UI edits, save/reload or undo without caching an invalid host pointer.

## Rule 1 — never use raw handle identity as durable identity
AEGP documentation explicitly warns that many layer/stream references are short-lived. Object-count changes and even keyframe insertion can invalidate references. Reacquire handles when needed and dispose/release them according to the owning suite.

## Rule 2 — choose the correct identity namespace
- Item/Layer persistent scripting IDs: use where their documented persistence matches the task.
- AEGP handles: transient access token only.
- stream/path IDs: use only within their documented session/lifetime semantics.
- Render GUID/receipt: identifies evaluated render state, not the saved object itself.
- media `DocumentID`/`ContentState`: identifies source media/content, not layer identity.

## Property problem
Current scripting does not guarantee a universal persistent `Property.id`. Retained AE 2024/2025 vocabulary contains `EnableTDBStreamScriptingIDs`, indicating Adobe has prototyped stronger persistent Property IDs internally. Until publicly contracted, do not depend on it.

## Robust pattern
Persist a high-level stable ID plus enough structural locator data to reacquire the object, then validate semantic attributes after reacquisition. Treat reorder, duplicate, precompose, copy/paste, import and undo as separate identity transitions.

## Unsafe shortcut
Serializing `_AEGPp_*` pointers, C++ object addresses, BEE/TDB pointers or private stream objects is version- and lifetime-fragile.

Related: `F-STATE-002`, `F-STATE-005`, `docs/state-model/object-identity.md`.

## Reacquisition recipe by object class
For Items, persist the documented item ID plus project identity and validate item type/name/source after reacquisition. For Layers, use the documented layer ID within its project-lifetime scope and re-resolve the layer handle each operation.

For properties/streams, prefer a structural locator built from stable owner identity plus Match Names/group path and only use dynamic indices where the containing group contract makes them unavoidable. After reacquisition verify match name, type and expected parent chain before mutating.

For async UI/render work, never retain the host handle solely because a request is pending. Store a semantic locator/request generation; reacquire current host objects inside the valid callback/context before publishing results.

## Identity-transition experiment
Construct one item/layer/property and record every available identity surface. Apply rename, reorder, keyframe insertion, effect insertion, duplicate, precompose, copy/paste, project save/reload, import into a second project and Undo/Redo.

For each transition record which persistent IDs survive, which handles become invalid, whether structural locators still resolve and whether Render GUIDs change despite persistent object identity remaining constant.

This produces the practical table needed by plug-in authors: **which identifier answers which lifetime question**.

## Failure modes
- persist layer index -> wrong layer after reorder;
- persist duplicate-prone name -> ambiguous target;
- retain StreamRef across dynamic-group mutation -> invalid host reference;
- serialize session-unique stream ID -> broken after host restart;
- treat Render GUID as saved-object identity -> new ID after ordinary render-relevant edit;
- reacquire by path but skip semantic validation -> silently mutate a different property after schema/topology change.

## Unknown frontier
Current public APIs still do not provide one universal persistent Property ID. Copy/paste/import remapping of Item/Layer/property identity across projects is not fully documented. Private TDB scripting-ID prototypes are evidence of internal work, not a contract available to third parties.

Related: `docs/state-model/object-identity.md`, `docs/state-model/streams-properties.md`, `docs/state-model/snapshots.md`, `F-STATE-002-short-lived-references.md`, `F-STATE-005-tdb-stream-scripting-id-prototype.md`.
