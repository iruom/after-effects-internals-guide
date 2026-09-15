---
status: seed
evidence_grade: E2-L
versions: "23.x-26.3 observed"
last_verified: 2026-09-14
---
# Expression runtime exposes multiple cache/lifetime concepts

## Statement
Debug Database and preferences expose time-invariant value cache, subproperty cache, engine recycling, post-expression cache size and a code-cache delegate candidate.

## Interpretation rule
Do not infer more than the evidence supports. Internal names are observation points, not automatically class or subsystem definitions.

## Next experiment
Build expression corpus separating source changes, dependency changes, property resolution and result values.
