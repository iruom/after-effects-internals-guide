---
status: confirmed-local
evidence_grade: E2-L
versions: "23.6/24.5-era crash logs"
last_verified: 2026-09-14
---
# Checkout receipts bridge BEE state to RG pixel worlds

## Local evidence
`BEE_CheckoutReceipt::pSetReceiptWorld` appears adjacent to `RGp_CheckoutResultImpl` operations and `RG_XformNode`/composite rendering in crash stacks.

## Interpretation
At least one internal receipt object carries or attaches a rendered world/result across the BEE ↔ RG boundary. This gives concrete implementation support to the broader public SDK concept of checkout receipts.

## Open questions
Is the receipt immutable after publication? Does it own a cache reference, a world reference, or both? Does partial-region validity live on the receipt or elsewhere?

## Experiment
Hold/release public AEGP frame receipts while varying memory pressure and use Probe AEGP to observe cache retention and rendered-region behavior.