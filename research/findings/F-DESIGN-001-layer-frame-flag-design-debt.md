---
id: F-DESIGN-001
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-DESIGN-001 — Layer-frame API preserves an explicitly acknowledged design mistake

**Evidence:** E0-H  
**Version:** AEGP Render Suite 5 / legacy Suite 4 behavior  
**Confidence:** High

The distributed header says `render_plain_layer_frameB` was confusing and is not the design Adobe wanted going forward. The newer call removes the choice and behaves as the old `false` path; callers needing the old `true` adjustment-layer-mask behavior are directed to Suite 4.

## Why AEIG keeps this
This is direct evidence of historical semantic overload in the render API. One boolean encoded materially different upstream-frame meanings, including an adjustment-layer-specific case.

## Internal lesson
Adjustment-layer input acquisition likely crosses a special graph boundary that did not fit cleanly into a generic "plain layer" boolean.

## Better-design direction
Represent requested render stage explicitly: source, effect-input, post-effect, mask-input, adjustment-input, post-geometry, composite, etc., rather than overloading booleans.