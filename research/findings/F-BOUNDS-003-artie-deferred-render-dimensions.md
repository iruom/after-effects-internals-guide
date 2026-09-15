---
id: F-BOUNDS-003
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-BOUNDS-003 — Rendered layer dimensions are deferred until effect-expanded texture state

**Evidence:** E0-S  
**Version:** AE 25.6 SDK `AEGP/Artie` sample  
**Confidence:** High

Artie comments that layer height and width may change because of buffer-expanding effects and therefore waits until texture acquisition before treating rendered dimensions as authoritative.

The sample distinguishes source-item dimensions from the size of the rendered texture world.

## Internal implication
Bounds are computed render state, not immutable layer metadata. Effect evaluation can alter spatial extent before downstream transform/composite stages.

A useful model is:
`rendered_bounds = F(source_bounds, effect_stack, time, resolution, render_context)`.

## Design consequence
A graph system that stores only static node dimensions will either clip expanding operators or conservatively over-render. Bounds should be a first-class evaluable property with explicit dependency propagation.