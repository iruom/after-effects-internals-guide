---
status: confirmed-local
 evidence_grade: E2-L
versions: "23.5-24.x observed"
last_verified: 2026-09-14
---
# BEE couples render tasks, speculative preview, cache, and render GUIDs

## Local evidence
Crash stacks expose `bee::RenderTaskManager::Shutdown`, `PauseSpeculativePreviewScoped`, `BEE_CacheLog::MarkDubious`, `BEE_SetEphemeralCache`, `BEE_WorkQueue_StartSpeculativeRender`, `BEE_RenderState::WorkQueue_SetItemCurrent`, and `BEEp_WorkQueue_GetRenderGuidWithRO` inside the BEE module.

## Inference
BEE is not merely a trace label. It contains concrete render scheduling/state/cache machinery and participates in speculative preview and render-identity computation.

## Caution
The expansion of the acronym BEE and exact subsystem ownership are still unknown. `RO` is also intentionally unresolved.

## Next experiments
Correlate `BEE_WorkQueue` trace output with idle preview, normal preview, render queue, cancellation and project edits; test whether `MarkDubious` corresponds to invalidation, tentative results, or diagnostic-only state.