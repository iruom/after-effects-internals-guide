---
status: researched-seed
evidence_grade: E0
confidence: 0.99
versions: "current AEGP Render Suite contract"
last_verified: 2026-09-14
---
# Speculative rendering is guarded against stale work

## Statement
AEGP Render Suite exposes `AEGP_IsItemWorthwhileToRender()` together with project timestamps and `AEGP_HasItemChangedSinceTimestamp()`. Adobe tells speculative renderers to check worthwhileness twice: before dispatching work and again when the render completes, before adopting the result into AE's cache.

## Internal implication
AE explicitly anticipates asynchronous render work becoming stale while it is in flight. Cache admission is therefore a race-sensitive operation, not just "render then store".

A minimal model is:
1. capture project/edit timestamp;
2. test whether work is worth dispatching;
3. render externally/asynchronously;
4. revalidate against edits that occurred during the render;
5. adopt only if still valid.

## Design lesson
Long-running tasks need versioned inputs and a commit-time validity test. Cancellation alone is insufficient because edits can race completion.

## Experiment
Create an AEGP speculative-render harness, mutate only unrelated versus related state during long renders, and record which completed results AE accepts.

## Source
AEGP Render Suite: https://ae-plugins.docsforadobe.dev/aegps/aegp-suites/
