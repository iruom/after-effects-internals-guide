---
id: F-CACHE-016
status: strongly-supported
evidence: [E0-H, E0-L]
version_scope: "AE 6.0 Canvas lineage; AE 7.0+ effect-prefix receipts; current 25.6 distributed headers"
last_verified: 2026-09-15
---
# F-CACHE-016 — Render receipts encode partial effect-stack validity

Canvas APIs can render or generate a receipt for only the first `num_effectsS` effects. `AEGP_CheckRenderReceipt` validates an old receipt against the current render/layer context, optionally checking geometrics. Receipt status includes `INVALID`, `VALID`, and `VALID_BUT_INCOMPLETE`.

## Confirmed implication
Cache validity is richer than a frame-level boolean. Effect-prefix state is part of receipt validity, and geometry validity is independently selectable during the check.

A useful evidence-backed model is:
`receipt ~= identity(layer state, effect prefix, geometry mode, render context)`

The equality sign is intentionally avoided: the exact internal receipt payload remains opaque.

## Historical lineage
The AE 6.0 Canvas API checked receipt validity without an effect-count argument. Retained later headers explicitly describe the AE 7.0 change as adding `num_effectsS` and adding `AEGP_GenerateRenderReceipt` for a receipt representing "as if first N effects rendered" state.

This makes effect-prefix insufficiency the leading interpretation of `VALID_BUT_INCOMPLETE`, but does **not** yet prove that the status means "can continue from this receipt" in every context.

## Falsification / experiment
`experiments/canvas-receipt-prefix-status.md` and `EXP-CACHE-002` test the full generated-prefix × requested-prefix matrix with geometry checks held constant, followed by isolated before/inside/after-prefix mutations.
