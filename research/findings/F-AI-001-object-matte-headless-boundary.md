---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G
---
# F-AI-001 — Object Matte crosses the headless render boundary

Adobe's 26.2.1 fixed issues state that `aerender` no longer fails when rendering a composition containing Object Matte.

## Consequence
Object Matte cannot be modeled as Layer-panel-only interactive state. Enough of its semantic result/state is available to the non-interactive render path for `aerender` to consume it.

This raises a useful persistence question: does headless rendering consume frozen/project-serialized matte state, an analysis cache, or recompute through a headless-compatible analysis service?

## Experiment
Save matched projects with Object Matte in unfrozen, frozen, cache-warm, and cache-cold states. Render through GUI, aerender, and after project restart; compare whether propagation is recomputed and which files are touched.
