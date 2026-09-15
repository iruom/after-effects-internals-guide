---
status: active
last_verified: 2026-09-15
---
# After Effects Internals Guide

AEIG reconstructs After Effects as a whole product and computational system. Public APIs are evidence surfaces, not the taxonomy.

Start with:
- `foundations/scope-and-coverage-model.md` — how completeness is measured;
- `architecture/product-system-atlas.md` — visible AE features mapped to internal domains;
- `architecture/system-overview.md` — current working architecture;
- `host-integration/cpp-sdk/guide-gap-matrix.md` — public Guide versus headers/runtime/reimplementations;
- `reference/version-matrix.md` — version archaeology.

The guide separates project/state, evaluation, render graph, temporal behavior, caches, image/color, memory/threading, GPU/3D, media/audio, expression runtime, persistence, UI/product shell, automation, host integration, observability and archaeology while preserving cross-links between them.

## AEIG 1.0 target
The current milestone is not “document every API”; it is to make the reconstructed model predictive and falsifiable. `../ROADMAP.md` defines the exit criteria, while `reference/roadmap-status.md` is generated from the coverage ledger.

Atlas breadth is closed: all 27 tracked domains are L2 or higher and no documentation page remains at `status: seed`. As of 2026-09-15, 23/27 domains meet the AEIG 1.0 target. The remaining gates are `state-identity`, `cache`, `render-graph`, and `plugin-host`, each requiring L5 runtime evidence from the canonical user-run package.

Recent runtime-model chapters include `color-pipeline/runtime-architecture.md`, `vector-shape-system/runtime-architecture.md`, `media-system/runtime-architecture.md`, `audio-system/runtime-architecture.md`, `memory-system/runtime-architecture.md`, `ui-system/view-state-and-render-boundary.md`, and `headless-system/runtime-architecture.md`.

## Practical entry points
- `capability-recipes/index.md` — start from an operation you want to accomplish.
- `reference/api-completeness-status.md` — API-surface completeness and classifications.
- `reference/release-readiness.md` — machine-generated 1.0 release gates.
- `reference/capability-frontier-status.md` — supported, internal-observation and unknown capability states.
