---
status: seed
evidence_grade: E2-L
versions: "23.x-26.3 observed"
last_verified: 2026-09-14
---
# BEE and RG vocabulary exists in local trace instrumentation

## Statement
Local Trace Database files contain BEE_Eval/BEE_Cache/BEE_WorkQueue and RenderNode.RG_CacheNodeBase/RG_XformNode plus render task/executor categories.

## Interpretation rule
Do not infer more than the evidence supports. Internal names are observation points, not automatically class or subsystem definitions.

## Next experiment
Enable trace capture under one-operation-at-a-time tests and correlate emitted events.
