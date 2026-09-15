---
status: confirmed-local
evidence_grade: E2-L
versions: "23.5-24.x crash logs"
last_verified: 2026-09-14
---
# BEE contains an explicitly named ephemeral cache path

## Local evidence
`BEE_SetEphemeralCache` occurs repeatedly around render task, GUID computation, checkout and speculative-preview stacks.

## Interpretation
BEE has at least one transient cache/state domain distinct by name from long-lived frame/disk caches. Its key, payload and lifetime remain unknown.

## Hypotheses to discriminate
1. per-render-call memoization
2. per-work-queue temporary state
3. short-lived render GUID/result cache
4. cache used during graph construction or pre-render only

## Experiment
Trace creation/destruction boundaries across one-frame renders, multi-frame preview, cancellation, undo, idle speculative render and process-wide cache purge.