# Experiment — Canvas receipt partial-stage status

## Question
Test whether `AEGP_RenderReceiptStatus_VALID_BUT_INCOMPLETE` corresponds to a receipt that is still valid for an earlier effect-stack prefix but does not satisfy a later requested `num_effectsS` stage.

## Historical motivation
AE 6.0 receipt checking used render context, layer context, an old receipt, and a geometry-check flag, but no effect-count argument.

The retained old headers mark a later change: the receipt check gained `num_effectsS`, and `AEGP_GenerateRenderReceipt` was added to create a receipt as if the first N effects had already been rendered.

That makes effect-prefix completion the strongest current hypothesis for the third receipt status, while still not proving the enum's exact semantics.

## Fixture
Use one layer with three deterministic effects E1, E2, and E3. Give each effect an independently mutable parameter and visually distinct output.
## Matrix
For each generated receipt prefix `k` in {0,1,2,3}, check it against requested prefix `n` in {0,1,2,3,ALL}. Record the returned status before any mutation.

Then repeat after these isolated mutations:
- parameter change in an effect with index `<= k`;
- parameter change in an effect with index `> k`;
- layer transform/geometry change, with geometry checking both disabled and enabled;
- effect reorder across the prefix boundary;
- effect enable/disable across the prefix boundary.

## Key discriminant
If the prefix hypothesis is correct, the most informative cell is `k < n` with all state up through `k` unchanged. A `VALID_BUT_INCOMPLETE` result there, combined with `VALID` for `k >= n`, would directly support `CanContinueFrom` rather than direct satisfaction.

If `VALID_BUT_INCOMPLETE` instead tracks spatial, geometry, or bin completeness, that pattern should fail while another controlled dimension predicts the status.

## Capture
Record requested `num_effectsS`, generated prefix, geometry-check flag, receipt status, effect mutations, render-context identity, and any receipt GUID available through the relevant versioned API.