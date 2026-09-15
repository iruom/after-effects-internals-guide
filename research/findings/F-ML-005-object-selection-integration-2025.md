---
status: confirmed-local-version-diff
last_verified: 2026-09-15
---
# F-ML-005 — A high-level Object Selection integration layer appears between AE 2024 and 2025

A binary-string comparison of local installs shows the following identifiers absent from AE 2024 `AfterFXLib.dll` but present in AE 2025:
- `ObjectSelectPreSeg`
- `RegisterObjectSelectionModels`
- `RotoBrush4`
- `ObjectSelection`
- `TriggerPreSegmentation`
- `DoMarqueeSegmentation`
- `CheckoutPreSegLayer_Complete`
- `VectorSelectionTracker`

AE 2024 also lacks `AeCompute.dll`; AE 2025 introduces it. In parallel, `Roto Brush.aex` changes from a FastMask2-only reference in 2024 to FastMask2 + FastMask3 references in 2025.
## Product-surface corroboration
AE 2025 localization dictionaries contain Beta feature strings for EnableRotoBrush4, EnableRotoLive, and EnableRotoSelectionBrush. The RotoBrush4 description says automatic object selection can intelligently choose an isolated subject before propagating the selection. The same installation also contains ObjectSelectionTool/PreSegmentationFailed.

AE 2024 dictionaries do not expose the RotoBrush4 strings found in the 2025 corpus, strengthening the 2024→2025 integration boundary observed in binaries. Treat localization resources as product-integration evidence rather than proof of shipping feature enablement.
