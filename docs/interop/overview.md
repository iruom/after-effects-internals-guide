---
status: active
last_verified: 2026-09-15
---
# Inter-Application and Format Interop

After Effects shares infrastructure and state with other Adobe applications and external content ecosystems. AEIG treats those boundaries as architecture, not incidental workflow features.

## Scope
Adobe Media Encoder handoff; Dynamic Link; Premiere-hosted effect compatibility; Illustrator/SVG exchange; Photoshop assets; Substance materials; USD/3D assets; XMP/media identity.

## Questions
- Which work is delegated to another process versus executed inside After Effects?
- What identity survives inter-process handoff: file path, XMP GUID, project/item IDs, render request IDs or serialized settings?
- Which caches are shared across applications?
- Where do AE and Premiere intentionally diverge while sharing SDK concepts?
- Which media/color/GPU services come from common Adobe frameworks?

## Evidence surfaces
AE/Premiere SDK comparison; MediaCore/cache artifacts; XMP; process/IPC traces; module inventory; AME and Dynamic Link logs; controlled cross-application experiments.

Cross-host agreement is evidence of a shared Adobe substrate; disagreement is equally valuable because it localizes host-specific semantics.

## Dynamic Link runtime boundary
Installed AE 2025 exposes Dynamic Link media as a MediaCore-compatible object rather than only a transport endpoint. `DynamicLinkMedia::BaseMediaInfo` carries separate DocumentID, ContentState and RuntimeGuid surfaces, creates MediaFoundation sources/streams, and participates in async Future/cancellation lifecycles.

Working model:
`remote/project source -> Dynamic Link identity + request/future -> MediaCore source/stream -> VideoFrame/media consumers`.

This is useful because it predicts two independent invalidation classes: source-content/version changes and transport/request/session changes. Downstream AE compositing changes should be treated as a third class rather than folded into either one.

See `research/findings/F-INTEROP-001-dynamic-link-media-identity-futures.md` and `datasets/ae-2025-media-pipeline-symbols.csv`.

## Dynamic Link is a versioned inter-process contract
Current Adobe documentation requires matching After Effects and Premiere versions for Dynamic Link. This is a strong product-level compatibility boundary: a linked composition is not just a pathname to an `.aep`, but a host-to-host contract whose protocol/runtime version must agree.

Creating a link can launch After Effects and create a project/composition using dimensions, pixel aspect, frame rate and audio sample rate from the originating Premiere sequence. Interop therefore transfers semantic project/request state, not only rendered frames.

## Identity layers across the link
Local runtime evidence supports at least four identities:
- remote project/composition identity;
- media-level `DocumentID` / mutable `ContentState`;
- runtime/session GUID and request/future identity;
- downstream AE/Premiere render/cache identity.

A reconnect can change session/request identity without changing source content. A source edit can change ContentState while preserving the logical linked asset. A downstream AE effect edit can invalidate compositing without changing remote media identity.

## Cache and transport separation
Dynamic Link results can participate in ordinary MediaCore/frame consumption after fulfillment, but transport connectivity and frame semantic validity are different concerns. A cached frame may remain semantically useful after a request finishes, while a live connection failure can block acquisition of new versions.

Do not treat Dynamic Link as a shared-memory shortcut. Model it as asynchronous inter-process/source resolution feeding the shared media/render substrate.

## Cross-application failure classes
- application version mismatch -> protocol/host compatibility failure;
- stale ContentState -> source invalidation failure;
- session disconnect/restart -> transport/runtime failure;
- differing color/GPU/media policy across hosts -> representation/context mismatch;
- missing external project/media -> persistence/relink failure;
- downstream cache reuse after remote edit -> identity propagation failure.

## Controlled experiments
Link one composition and change independently: remote AE project pixels, composition dimensions/frame rate, Premiere downstream effects, application restart, cache purge and network/process interruption. Record Dynamic Link process/module activity, DocumentID/ContentState/runtime GUID where observable, frame hashes and cache reuse.

A strong experiment distinguishes **content invalidation** from **transport invalidation**: restart only the serving AE instance without changing project content, then compare media identity and downstream frame reuse.

## Broader interop rule
Apply the same identity-first method to AME, SVG/Illustrator, Photoshop, Substance and 3D/USD interchange. Ask what is copied, linked, materialized or delegated; which side owns persistence; and which representation becomes native AE project state.

## Unknown frontier
Unresolved: exact current Dynamic Link IPC protocol and cache sharing; whether MediaCore content identity survives every host restart; how OCIO/ICC/view settings are negotiated cross-host; where AME handoff changes renderer/process identity; persistence semantics of newer native SVG/3D import materialization.

Related: `F-INTEROP-001-dynamic-link-media-identity-futures.md`, `docs/media-system/media-identity.md`, `docs/host-integration/premiere-pro/shared-effect-api.md`, `docs/headless-system/runtime-architecture.md`.
