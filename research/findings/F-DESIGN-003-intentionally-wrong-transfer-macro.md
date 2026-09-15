---
id: F-DESIGN-003
status: legacy-unclassified
metadata_normalized: 2026-09-15
evidence_note: Legacy finding retained verbatim; evidence level requires explicit refresh before promotion.
---

# F-DESIGN-003 — Intentionally Preserved Incorrect Transfer-Mode Macro

## Status
Confirmed in the distributed AE 25.6 `AE_EffectCB.h`.

## Evidence
Adobe marks `PF_TransferMode_ZERO_ALPHA_NOP` deprecated because its meaning was confusing, then explicitly warns that `PF_TransferMode_ZERO_SRC_ALPHA_LEAVES_DST_UNCHANGED()` is incorrect for `PF_Xfer_COPY`.

The comment states the macro has behaved this way for so long that Adobe leaves it unchanged to avoid creating bugs by fixing it.

## Meaning
This is compatibility behavior fossilized as API semantics. Source-code truth, mathematical truth, and historical plug-in compatibility are not always identical in AE.
## Diagnostic implication
When diagnosing alpha/compositing discrepancies, do not infer behavior solely from helper names. Check the actual macro/host operation and the historical compatibility notes. A plug-in that 'corrects' this helper locally can diverge from legacy projects or sibling plug-ins.

## AEIG rule
Maintain a separate category for **compatibility bugs treated as contract**. These should not be normalized away when reconstructing AE semantics.
