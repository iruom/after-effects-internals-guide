---
id: F-EVAL-004
status: observed
experiment: EXP-CORE-001
evidence: [E1]
version_scope: "AE 26.3"
last_verified: 2026-09-15
---
# F-EVAL-004 — Deterministic temporal output under a keyframed state mutation

`EXP-CORE-001` evaluated the same 120 frame times twice from unchanged project state and then repeated the evaluation after changing only the midpoint Gaussian Blur keyframe on three layers from 60 to 110.

## Observed
- Pass A vs B: **120/120 PNG files are SHA-256 identical**.
- Pass B vs C after the mutation: **1/120 identical, 119/120 different**.
- The sole unchanged frame is `f000`, whose blur endpoint value remained 5.

This validates two evaluation-level properties for the fixture: unchanged semantic state reproduced byte-identical output, while changing an interpolation control point propagated to sampled times whose evaluated value depended on that control point.

## What this does not prove
The experiment does not identify the internal GUID, receipt, dirty bit, cache entry, or dependency node responsible for invalidation. It therefore cannot by itself prove a particular cache-key or state-identity implementation.

The contemporaneous RIP samples also **must not** be interpreted as render execution evidence: their five-second capture windows ended 7.3–8.2 seconds before each render pass began. AEIG records that defect explicitly in `datasets/exp-core-001-sampler-audit.csv`.

## Reproducibility assets
See `experiments/observatory/manifests/EXP-CORE-001.json`, `datasets/exp-core-001-frame-diff.csv`, the preserved PNG sequences, and `runs/EXP-CORE-001/sha256.txt`.
