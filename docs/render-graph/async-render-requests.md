---
status: active
last_verified: 2026-09-16
evidence: AE 13.5 Render/Async Manager contracts + HistoGrid async UI pattern + current BEE work-queue comparison
---
# Async Render Requests and Obsolescence

Asynchronous rendering in AE is not merely a way to avoid blocking. It creates a separate identity/lifetime problem: **a frame can be semantically valid while the request that asked for it has become obsolete**.

## 13.5 architecture boundary
The 13.5 Render Suite moved passive UI drawing away from synchronous frame checkout. Adobe still recommends async retrieval for passive custom UI, while synchronous checkout remains appropriate for narrow user actions that must immediately update project state.

This makes UI responsiveness part of the host contract rather than a plug-in-local optimization.

## Request identity is not frame identity
`AEGP_RenderAndCheckoutLayerFrame_Async` returns an opaque `AEGP_AsyncRequestId`. Completion reports that request ID, cancellation state, render error, frame receipt and caller refcon.

At least three identities must remain separate:
- **request identity**: one scheduled operation;
- **render/frame identity**: the semantic image state represented by options/receipt/cache;
- **consumer generation**: whether the UI/tool still wants this result.

Cancelling one request therefore does not imply that an equivalent frame result is globally invalid. Conversely, a successful frame can be useless to a consumer that already advanced to a newer generation.

## Async Manager adds purpose identity
The 13.5 Async Manager adds a caller-defined `purpose_id`. Requests with the same purpose can supersede each other when their Render Options change, allowing stale work to be cancelled automatically.

A useful model is:

`purpose -> consumer generation -> render options -> async request id -> frame receipt/result`.

`purpose_id` is cancellation/replacement policy, not automatically part of reusable render-content identity.

## Completion and lifetime
Older async Render Suite comments guarantee completion unless AE is shutting down. Production code must still distinguish normal success, render error, explicit/implicit cancellation and host teardown.

Before publishing pixels or derived UI state, a completion callback should verify that its owner still exists and that the request remains the newest relevant generation.

## Common obsolescence triggers
- time scrub;
- ROI/view change;
- parameter edit;
- layer/comp topology edit;
- project switch or close;
- custom UI destruction;
- newer request for the same semantic purpose.

Some of these only obsolete the **consumer request**; they do not necessarily invalidate the **frame cache entry**.

## Relationship to current BEE work queues
Local BEE runtime surfaces expose asynchronous work-queue items, cancellation, pause/resume, speculative preview and cached checkout operations. The high-level pattern is compatible with public async request semantics, but AEIG does not claim that the 13.5 Async Manager and current BEE WorkQueue are the same implementation.

## Failure modes
- publish-on-completion without generation check -> stale histogram/preview flashes;
- retain project/layer handles across async completion -> invalid reference after topology change;
- equate cancellation with cache invalidation -> unnecessary rerender;
- use synchronous checkout for passive redraw -> UI stalls/deadlock exposure;
- reuse caller refcon after panel/effect destruction -> use-after-free;
- perform heavy post-processing after cancellation -> wasted work.

## Controlled experiment
Use a custom-UI fixture that requests frames while rapidly changing time, ROI and one render-affecting parameter. Log request IDs, purpose IDs, RenderOptions fingerprints, callbacks, cancellation flags, receipts and the generation finally published to UI.

The expected invariant is: only the newest relevant generation publishes, while semantically equivalent frames may still be reusable by cache even if an older request was cancelled.

## Unknown frontier
Unresolved in current AE:
- mapping between public async request IDs and internal BEE work-queue IDs;
- how far cancellation propagates into RG traversal and backend work;
- whether already-submitted GPU/media work is physically aborted or merely discarded on completion;
- priority interaction between speculative preview and explicit custom-UI async work.

Related: `F-ASYNC-001`, `docs/ui-system/async-custom-ui-rendering.md`, `docs/render-graph/render-tasks.md`, `docs/threading-system/overview.md`.