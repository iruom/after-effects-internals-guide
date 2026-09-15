---
status: active-hypothesis
last_verified: 2026-09-15
evidence: retained/current preference vocabulary + public render-admission APIs
---
# Speculative Evaluation

After Effects exposes long-lived concepts for idle/speculative/background caching. Retained/current preferences include a `Speculative Preview Preference Section` with controls for idle delay, cache range and caching behavior.

Public render APIs also expose host decisions about whether work is worthwhile to render speculatively.

The strongest safe model is therefore not a separate renderer, but an alternate request/admission source feeding the same broad evaluation/render infrastructure with a different priority or cache policy.

## Questions that remain open
- Does speculative work build the same RG node/request identities as foreground preview?
- Are admission and cancellation policies distinct while cache entries remain shared?
- Does speculative work use a different work queue or only different priority metadata?
- How do memory pressure and MFR limits suppress idle work?

## Discriminating experiment
Use one deterministic project and compare foreground preview versus idle caching while collecting BEE/RG/work-queue trace. If identical render identities appear under different scheduling traces, that supports shared graph/cache identity with alternate admission.

A different render GUID/cache namespace would falsify that simpler model.

Until trace correlation is captured, AEIG labels this scheduling relationship as a hypothesis rather than a confirmed internal path.
## Public stale-work contract
The AEGP Render Suite explicitly anticipates speculative work racing project edits. `AEGP_IsItemWorthwhileToRender()` is meant to be checked before dispatch and again after completion, while project timestamp/change queries determine whether the result is still admissible.

This establishes a two-phase model:
`generation/admission check -> asynchronous render -> commit-time revalidation -> cache adoption or discard`.

Cancellation alone is insufficient because work can finish after the semantic generation that requested it has already become obsolete.

## Version/runtime correlation
Retained 23.5-24.x BEE symbols expose speculative work-queue entry points, pause-scoped speculative preview, render GUID lookup and cache-state vocabulary. This is compatible with the public stale-work contract but does not prove exact API-to-private-call mapping or unchanged behavior in 26.x.

## Failure modes
- admit completed work without rechecking generation -> stale cache pollution;
- cancel request but still publish late result -> visible rollback/stale preview;
- include scheduling priority in semantic frame identity -> unnecessary cache fragmentation;
- treat unrelated edit as invalidating every speculative result -> lost background-cache value;
- let memory pressure compete equally with foreground work -> responsiveness regression.

## Extended experiment
Introduce a controlled long render and mutate either an unrelated metadata field, a true upstream dependency or only the UI/view state while it runs. Record project timestamp, worthwhileness result before/after, render GUID/receipt, BEE work-queue trace and whether the completed image becomes reusable in foreground preview.

The key discriminator is commit-time adoption, not merely whether the worker finished.

## Unknown frontier
Still unresolved: exact priority/admission algorithm; relation between speculative and normal BEE queue objects; whether speculative results share identical RG/cache-node identity; how MFR/resource admission caps idle work; meaning of internal `MarkDubious`/ephemeral-cache states.

Related: `F-EVAL-001-speculative-render-race.md`, `F-BEE-001-render-task-cache-speculative.md`, `docs/evaluation/work-queues.md`, `docs/render-graph/render-tasks.md`, `docs/cache-system/state-identity.md`.
