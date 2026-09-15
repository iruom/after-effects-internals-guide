---
status: researched-seed
evidence_grade: E0
confidence: 0.99
versions: "current AEGP Render Suite contract"
last_verified: 2026-09-14
---
# Frame receipts can represent partially rendered regions

## Statement
`AEGP_GetRenderedRegion()` returns the region of a frame receipt's world that has already been rendered. Adobe explicitly notes that only portions of an image that changed may be rendered, so callers must verify whether the region they need is actually present.

## Internal implication
A frame receipt is not necessarily equivalent to a fully materialized frame. At least some render/caching paths preserve region validity inside a frame-sized world or can produce partial results.

This intersects with SmartFX ROI/bounds, incremental redraw and cache reuse. It raises an important question: is region validity tracked as one rectangle, multiple regions internally collapsed to one rectangle, or a richer structure hidden behind the receipt?

## Experiment
Render a sparse moving object over a static layer and query rendered regions across small edits, masks and ROI changes. Correlate with `RenderNode.RG_CacheNodeBase` traces and SmartFX request rectangles.

## Design opportunity
A modern tile/region cache can represent sparse validity more precisely than one bounding rectangle, but metadata and fragmentation costs must be measured.

## Source
AEGP Render Suite: https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
