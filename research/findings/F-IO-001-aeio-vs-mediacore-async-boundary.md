---
id: F-IO-001
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-IO-001 — AEIO and MediaCore Expose Different I/O Concurrency Eras

## Status
Confirmed interface difference; host-internal scheduling remains partly unknown.

## AEIO evidence
AE 25.6 still distributes `AEIO_FunctionBlock4`, explicitly frozen in AE 10. The input path is callback-oriented: initialize an InSpec, flatten/inflate options, query extent/dimensions/time, and synchronously return pixels through `AEIO_DrawSparseFrame`.

`AEIO_DrawSparseFramePB` carries a time range, rational scale, `required_region`, quality, field request and interrupt callbacks. AEIO therefore already supports demand-limited spatial reads, but the public function block exposes no equivalent to Premiere's reentrant asynchronous importer lifecycle.

Output has explicit `StartAdding`, per-frame/chunk writes, `EndAdding`, `Flush`, and an `Idle` hook.
## Premiere contrast
Premiere's `AsyncImporterEntry` is explicitly reentrant except for close; close may arrive while other calls are executing. `Flush` is the synchronization barrier. The async importer must not retain a link to its creator because their lifetimes are deliberately decoupled; relevant state must be copied.

## Interpretation
The difference is useful evidence of two architectural generations: AEIO preserves a legacy host-callback/state-handle model while MediaCore exposes explicit asynchronous ownership and cancellation semantics.

Adobe's current AEIO guide itself recommends a MediaCore importer when possible because it is shared across Adobe video/audio applications.

## Diagnostic value
I/O crashes should be classified separately as state-lifetime bugs, region/time request bugs, cancellation/barrier bugs, and decoder/cache bugs. 'Importer problem' is too coarse.