---
status: active
last_verified: 2026-09-16
evidence: current Adobe workspace/preferences behavior + AEGP Command/ItemView/Guide contracts + extension/UI runtime evidence
---
# Product Shell, Panels, Commands and View State

The application shell is part of AE's implementation model because editing, selection, panels, views, tools, workspaces and commands determine **which project transaction or render request is produced**. But shell state must not be confused with project/render identity.

AEIG separates at least four state classes:

`document/project state | per-view/editor state | versioned user/workspace preferences | transient interaction/request state`.

## Workspace persistence is local and environment-sensitive
Adobe documents that workspace changes are tracked/saved locally. Projects can carry a workspace name, but another machine falls back to its current local workspace when no matching workspace exists or monitor configuration differs.

Therefore a workspace reference is not a portable description of exact panel geometry. It is closer to a local presentation-profile lookup.

This is a useful model for other UI state: **portable project semantics and local editor presentation can refer to each other without being the same persistence domain.**## Guides expose a clean state split
The 26.5 SDK adds `AEGP_GuideSuite`: guide orientation/position, optional percentage positioning, color and edge pinning belong to guide/document semantics. Separately, `AEGP_ItemViewSuite2` exposes whether guides are visible, snapping or locked in a particular item view.

That split is architecturally significant:

`guide geometry/style -> item/document state`

`visible/snap/lock -> view/editor presentation state`.

An effect or automation system should not assume that every visible editor choice participates in render identity or project serialization in the same way.

## Commands are another boundary
AEGP Command Suite and scripting `executeCommand` expose command invocation as a host-mediated operation rather than direct access to internal command objects. Command IDs/menu availability are host/version/context dependent.

A command can create project mutations, selection/view changes, modal UI or no-op depending on context. Treating `executeCommand(id)` as a stable semantic API is therefore weaker than using a dedicated documented suite/DOM method when one exists.

For automation research record command ID, localized menu text separately, enabled state, active panel/view, selection and undo result.## Interactive render state
Composition/Layer/Footage viewers can carry zoom, viewport origin, display channel, exposure, overlays, checkerboard and interactive quality state. Artisan/Canvas APIs show that some of this presentation state enters a renderer-facing context for interactive output without becoming persistent project semantics.

This is why `final render + UI overlay` is too simple a model for the viewer. AE can issue a render request whose context already encodes interactive presentation policy.

## Extension planes
Legacy ScriptUI/ExtendScript, CEP panels, AEGP panels/custom UI and newer UXP-related substrate occupy different execution and lifetime domains. A visible panel does not imply the same scripting engine, main-thread access path or persistence model.

## Failure modes
UI bugs often come from crossing state classes: persisting view-only state into project semantics, assuming selection/focus is stable during asynchronous work, blocking the main thread through CEP `evalScript`, or using numeric command IDs as version-independent API contracts.

## Experiments
For each shell feature classify what survives project save/reopen, AE restart, preference reset, workspace reset and migration to another machine. Separately trace whether the action creates an undo record, invalidates render state, changes only the view, or schedules an asynchronous UI render.

## Unknown frontier
AEIG does not yet claim a complete private panel-framework/widget hierarchy for current AE. Public suites, installed extension substrates and traces establish boundaries; exact internal ownership remains version-scoped research.

Cross-links: `../ui-system/overview.md`, `../ui-system/view-state-and-render-boundary.md`, `../host-integration/uxp-cep/cep-runtime.md`, and `../persistence/preferences.md`.