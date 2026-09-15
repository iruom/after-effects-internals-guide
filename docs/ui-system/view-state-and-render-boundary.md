---
status: active
last_verified: 2026-09-15
---
# View State and Render Boundary

AEIG does not treat all visible editor state as project/render state. Public and sample contracts expose several distinct layers.

## Document-semantic state
Guides are attached to Items/Layers and carry orientation, position/type, color and pinning. Properties, masks, layer/effect state and other render inputs live in project/stream domains.

## Per-view presentation state
Guide visibility, snapping and locking are exposed separately through Item View APIs. Selection/editor focus, panel state, zoom/display configuration and overlays likewise need not participate in rendered-pixel identity.

## UI request state
Async custom-UI rendering adds a third kind of state: a stable `purpose_id` plus current render options identify what a UI surface wants now. AE can cancel stale requests and trigger redraw when the desired result becomes available.

```text
project/document state -----> render/evaluation state
          |                         |
          |                         +--> async UI render result
          v                                   |
view/editor state ---> UI purpose/current request <---+
```
## Synchronization boundary
Since AE 13.5, `PF_GetCurrentState()` deliberately returns randomized state from `PF_Cmd_UPDATE_PARAMS_UI` rather than crossing an unsafe synchronization boundary. This is strong evidence that UI callbacks cannot be modelled as freely reading the authoritative render-side state graph.

Custom UI should instead use host-managed async checkout when pixels are required. A receipt may exist before it contains a consumable world, so UI availability is multi-state rather than a boolean.

## Architectural rule
For every UI feature ask separately:
- What is persisted project/document state?
- What is per-view/editor state?
- What state affects render identity?
- What result is only a display cache?
- Can UI synchronously access it, or must it request/cancel/redraw asynchronously?

Cross-links: `async-custom-ui-rendering.md`, `F-STATE-004-guide-data-vs-view-state.md`, and `F-THREAD-002-ui-state-query-randomized.md`.

## Persistence matrix
A useful UI-state model has at least four scopes:
- **document state**: saved project semantics such as guide geometry and layer/property values;
- **view state**: visibility/snap/lock, zoom, overlays and other viewer-local presentation;
- **profile/workspace state**: application/user configuration outside the project semantic graph;
- **transient request state**: current selection, hover, drag generation and async UI render purpose.

The same visible control can touch more than one scope. For example, editing a guide position mutates document state while toggling guide visibility can remain a view preference.

## Render identity rule
Only state that changes the requested rendered semantics should enter render identity. A view zoom or panel size may alter which preview resolution/ROI is requested without changing the underlying composition's project identity. Display Color Management may alter viewer pixels while leaving project render data untouched.

Therefore distinguish **project render identity** from **preview request identity** and **display transformation state**.

## Failure patterns
- save view-only state into a render cache key -> unnecessary invalidation;
- omit document-semantic guide/layer state from persistence -> project mismatch after reopen;
- mutate project state from passive draw callback -> thread/synchronization errors;
- keep selection/hover state in undoable document storage -> polluted undo history;
- assume a screenshot difference proves project-render difference -> false diagnosis when only display/view transform changed.

## Controlled boundary tests
For each candidate UI property, vary it alone and record: project dirty flag, Undo entry, AEP/AEPX diff, render GUID/receipt change, async request change, output-file hash and viewer screenshot.

This produces a practical classification table: `persistent semantic`, `render-request-only`, `view/profile`, or `pure transient UI`.

## Unknown frontier
Still unresolved: exact persistence scope of many panel/editor states, how workspace/view state is represented across machine/monitor configurations, and which preview-only settings are folded into internal BEE/RG request identity versus handled downstream by viewer/display code.

Related: `docs/product-shell/overview.md`, `docs/state-model/snapshots.md`, `docs/color-pipeline/runtime-architecture.md`.
