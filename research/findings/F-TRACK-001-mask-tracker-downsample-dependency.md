---
status: confirmed-symptom / causal-model-hypothesis
last_verified: 2026-09-15
evidence: E0-G 26.5 fixed issue
---
# F-TRACK-001 — Mask Tracker behavior depended incorrectly on composition resolution

Adobe's 26.5 fixed issues state that the new Mask Tracker no longer fails when the composition Resolution is set below Full.

## Confirmed implication
Tracker execution is coupled to preview/downsample resolution strongly enough that a non-Full setting previously broke tracking.

## Causal hypotheses
Potential fault classes include incorrect conversion between full-resolution mask/path coordinates and downsampled analysis pixels, an ROI/stride assumption tied to full resolution, or an analysis-input request that inherited viewer resolution when it required source-resolution data.

## Experiment
Track an identical mask at Full/Half/Quarter resolution while logging source checkout sizes, path coordinates, and final tracked vertices. The correct invariant is that UI preview resolution may change analysis cost but should not change semantic tracking coordinates/results beyond documented approximation.
