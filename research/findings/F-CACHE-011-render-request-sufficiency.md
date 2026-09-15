---
id: F-CACHE-011
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-CACHE-011 — Render reuse exposes a host-defined sufficiency relation

**Evidence:** E0-H  
**Version:** `AEGP_RenderOptionsSuite4` / `AEGP_RenderSuite5`  
**Confidence:** High for API semantics; unknown for exact comparison rules

`AEGP_IsRenderedFrameSufficient` compares the Render Options associated with an already rendered frame against a proposed Render Options object and reports whether the prior result is sufficient.

Render Options independently expose time, time-step, field, world type, X/Y downsample, ROI, matte representation, channel order, guide-layer rendering and footage decode quality.

## Implication
AE's reuse decision cannot be reconstructed safely as only `hash(request) == hash(cached_request)`. The public API admits a semantic relation between two requests.

A useful formalization is `S(cached, requested)`, with exact symmetry/transitivity/containment behavior left unproven.

## Experiment
Build a directed sufficiency matrix by varying one Render Options axis at a time and querying both directions. Then test pairwise combinations to discover whether independently sufficient dimensions compose.
