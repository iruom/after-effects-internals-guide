---
status: generated
last_verified: 2026-09-15
---
# AEIG 1.0 Static Release Candidate

Static RC fingerprint: `37893B3E6B3837965E9B1F6548D93B981992E18C33F0F7BC85B62D50535C959B`.
Frozen artifacts: **32**; prospective predictions locked: **7**.
Domain target progress: **23/27**.
C++ identifier inventory: **5023** classified identifiers.
Master Surface Registry: **53810** normalized rows.
Evidence corpora: **18**.
Finding registry: **125** entries.

## Remaining release blockers
- `domain-targets`: 23/27 domains meet target; unmet=state-identity,render-graph,cache,plugin-host
- `predictive-validation`: prospective=7 locked=7 confirmed=0 pending=7 refuted_unrevised=0

The remaining blockers are intentionally operator-evidence gates. Static evidence, documentation, frozen predictions, and analysis tooling must not be altered to fit the eventual operator result.

## Promotion path
1. Run the canonical disposable AE operator experiment.
2. Preserve raw captures unchanged.
3. Run the frozen finalizer and update prediction outcomes.
4. Run `promote_aeig_1_0.py`; it verifies the Static RC before touching coverage.
5. Promotion succeeds only if all four core L5 evidence gates and prediction gates pass.
