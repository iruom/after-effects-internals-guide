---
status: active
last_verified: 2026-09-14
primary_evidence:
  - AE 25.6 SDK UI/HistoGrid/HistoGrid_UI_Handler.cpp
  - AE 25.6 SDK Headers/AE_GeneralPlug.h
  - AE 25.6 SDK Headers/AE_EffectSuites.h
  - AE 25.6 SDK Headers/AE_Effect.h
---
# Async Custom-UI Rendering

AE 13.5 introduced a managed asynchronous render path for effect custom UI. This is a particularly useful window into the post-13.5 UI/render-thread split because the API exists specifically to stop UI code from synchronously managing render lifetimes.

## Manager lifetime
`PF_GetContextAsyncManager()` returns a `PF_AsyncManagerP` associated with the current effect UI context. The SDK comment describes it as managing multiple asynchronous render requests over that context lifetime, especially for caching on the UI thread.

The matching AEGP suite is explicitly described as a render path managed by AE rather than by plug-in callbacks. As of 13.5, the exposed manager is tied to `PF_Event_DRAW` custom UI.
## Purpose IDs and automatic stale-request cancellation
Both item and layer async-manager calls take a caller-chosen `purpose_id`. Adobe describes this as a stable ID for requests serving the same UI purpose; when the render options change, the manager can automatically cancel older requests with that purpose.

This is a semantic request identity, not merely a task number:

`UI purpose + render options -> current desired request`

That model is stronger than "spawn a background render" because it lets AE recognize obsolete work as the UI state evolves.

## Nonblocking redraw loop
The HistoGrid sample requests a heavily downsampled upstream frame. If the frame is already available, a receipt is returned. Otherwise the async manager schedules rendering and a future `PF_Event_DRAW` is triggered. The UI draws cached/blank state in the meantime.

This produces a host-driven loop:
1. UI draw asks for current semantic result.
2. AE returns available receipt or schedules work.
3. UI remains responsive using stale/empty preview state.
4. Completion invalidates/redraws the UI.
5. The next draw asks again for the current desired result.

The plug-in never needs to own a worker thread or completion callback lifetime.
## Receipt semantics
The async checkout can succeed while returning a receipt whose world is empty. HistoGrid therefore obtains the receipt, calls `AEGP_GetReceiptWorld()`, handles a null world, and always checks the frame back in.

This distinguishes at least three states:
- no receipt yet / work pending,
- valid receipt with no pixel world,
- receipt with a world that can be consumed.

Do not model async availability as a single boolean.

## Architectural implication
`PF_OutFlag2_CUSTOM_UI_ASYNC_MANAGER` exists because, after the 13.5 render/UI separation, custom UI should no longer force synchronous frame acquisition from the UI thread. This is consistent with other 13.5 changes: render-side project copies, deadlock-avoidance behavior in `PF_GetCurrentState()` and sequence-data synchronization changes.

## Developer tips
Prefer semantic request IDs that survive redraws but change meaning only when the use-case changes. Treat render options as immutable request state. Never keep a receipt indefinitely; check it in promptly. Keep a cheap preview cache so the UI remains useful while a new render is pending.

For a modern node system, copy the *pattern* rather than the exact API: request-by-purpose, host-owned cancellation, stale-result rejection and redraw-on-availability are cleaner than direct synchronous render calls from UI code.
## UI-thread and project-mutation boundary
The 13.5 SDK tightened validation around AEGP use from render threads and passive UI callbacks. `PF_Event_DRAW` is not a general project-mutation phase; project changes belong on appropriate UI-thread/user-action paths.

When a specific user click requires an immediate project update and pixels are needed before continuing, the synchronous layer-frame checkout remains a narrow valid tool. For passive redraws, the async manager pattern is the intended architecture.

This distinction prevents two common errors: blocking every draw on a render, and moving project mutation into a render callback merely because the pixels became available there.

## Historical known bug as architecture evidence
Adobe's 13.5-era notes retain a known HistoGrid issue where drag-changing an upstream parameter might not refresh the histogram until the mouse later hovered over it. AEIG treats this as evidence that **render completion, dependency invalidation and UI redraw scheduling are separable events**.

The existence of such a bug does not prove the current implementation shares the same flaw. It is useful because it exposes the failure mode: pixels can become stale at the UI surface even when the underlying render dependency changed correctly.

## Robust generation pattern
Keep a monotonically increasing UI generation or equivalent immutable request snapshot. Every draw computes the desired render options from current UI/project state, uses a stable purpose ID for the semantic widget, and publishes a result only if it still matches the newest generation.

Do not attach long-lived meaning to `AEGP_FrameReceiptH` or a world pointer. Receipt lifetime, request lifetime, panel lifetime and cache lifetime are distinct.

## Controlled experiment
Instrument a histogram/keyer-style panel while scrubbing time and drag-changing an upstream effect rapidly. Log purpose ID, render-options fingerprint, receipt/world availability, redraw events and the generation actually painted.

Test panel close/reopen and project switch while work is pending. The correct result is no stale publish, no retained invalid handle and no UI-thread stall.

## Unknown frontier
Unresolved: exact mapping from Async Manager requests to modern BEE work-queue generations, cancellation depth after GPU/media submission, and whether current AE still has any redraw-only dependency gaps analogous to the historical HistoGrid issue.

Related: `docs/render-graph/async-render-requests.md`, `docs/ui-system/view-state-and-render-boundary.md`, `docs/architecture/project-vs-render-state.md`.
