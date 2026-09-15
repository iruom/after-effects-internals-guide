---
status: generated
last_verified: 2026-09-15
---
# L5 Outcome Decision Table

These criteria are derived from the immutable prediction lock before the operator run. They define how outcomes affect the model without changing the locked prediction text.

| Prediction | Domain | Raw evidence | Confirm if | Refute if | Model revision if refuted |
|---|---|---|---|---|---|
| PRED-004 | state-identity | EXP-CACHE-002/receipt-matrix.tsv | all CHECK rows follow k<n => INCOMPLETE; k>=n => VALID | any controlled CHECK violates prefix rule | revise Canvas receipt-prefix semantics |
| PRED-005 | cache | EXP-CACHE-002/receipt-matrix.tsv | A/B matrices preserve the same prefix rule | mutation changes the abstract prefix rule | separate state mutation from receipt sufficiency model |
| PRED-006 | render-graph | EXP-RG-001/host-trace.log | RG target categories occur inside render window | successful render has no RG target trace | revise trace/provider assumptions or render-path model |
| PRED-007 | state-identity | EXP-RG-001/host-trace.log | identity/eval footprint changes after Blur mutation | confirmed mutation yields indistinguishable identity footprint | revise state-to-identity propagation model |
| PRED-008 | render-graph | EXP-RG-001/host-trace.log | RG/cache/work-queue footprint changes after mutation | confirmed mutation yields indistinguishable RG/cache footprint | revise invalidation/materialization model |
| PRED-009 | plugin-host | EXP-PLUGIN-001/suite-acquisition.tsv | families exhibit different accepted selector sets | all 48 families share one global selector sequence | revise suite-scoped selector model |
| PRED-010 | plugin-host | EXP-PLUGIN-001/suite-acquisition.tsv | runtime matrix cannot collapse to one latest-table alias | all families show universal latest-table behavior | revise exact-version dispatch requirement |

An incomplete capture is `inconclusive`, not a confirmation. Promotion remains controlled by the separate finalizer and promotion guard.
