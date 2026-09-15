---
id: F-ASYNC-001
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-ASYNC-001 — Async render manager tracks request purpose separately from render options

**Evidence:** E0-H  
**Version:** AEGP Render Async Manager, frozen AE 13.5  
**Confidence:** High

Async Manager checkout calls take a `purpose_id`. Adobe comments that requests with the same purpose can be automatically canceled when their RenderOptions change.

## Internal implication
Async render identity has at least two dimensions: what the result is for, and the concrete render options. This allows stale work to be canceled without conflating semantic purpose with frame-state identity.

Possible model:
`request = (purpose_id, render_options, generation)`.

## Connection
This is conceptually compatible with current BEE speculative work queues and stale-result rejection, but direct implementation continuity remains unproven.

## Design note
Separating purpose identity from content identity is a strong pattern for interactive graph systems: it enables replacement/cancellation without polluting reusable cache keys.