---
status: active
last_verified: 2026-09-15
---
# Core L5 Operator Evidence Map

The final AEIG 1.0 operator run uses one controlled fixture but keeps its evidence planes separate. A file being present is not enough; the frozen analyzers and prediction gates determine whether it supports promotion.

| Raw artifact | Primary claim | Domain / prediction |
|---|---|---|
| `EXP-CACHE-002/receipt-matrix.tsv` | effect-prefix receipt sufficiency | State-Identity `PRED-004`; Cache `PRED-005` |
| `EXP-CACHE-002/fixture-script.log` | pass A/B, mutation, renderer and script lifecycle | all four core domains |
| `EXP-CACHE-002/fixture-output-A.avi` | controlled pre-mutation materialization | Cache / Evaluation context |
| `EXP-CACHE-002/fixture-output-B.avi` | controlled post-mutation materialization | Cache / Evaluation context |
| `EXP-CACHE-002/environment.txt` | host/build/OS/GPU environment | reproducibility |
| `EXP-PLUGIN-001/suite-acquisition.tsv` | suite-name + PICA selector acceptance matrix | Plugin Host `PRED-009/010` |
| `EXP-RG-001/host-trace.log` | BEE/TDB/GUID/RG/cache activity in render window | State-Identity `PRED-007`; Render Graph `PRED-006/008` |
| `EXP-RG-001/trace-control.tsv` | scoped trace begin/end and restoration | Render Graph / observability boundary |
| `EXP-SCRIPT-001/runtime-reflection.tsv` | runtime-visible ExtendScript members | scripting runtime comparison |
## Interpretation constraints

- Canvas `AEGP_RenderReceiptH` is not silently equated with `AEGP_FrameReceiptH` or any BEE/RG GUID type.
- Equal trace line counts do not prove equal internal state; content-level equivalence must be demonstrated or the result remains inconclusive.
- Successful `AcquireSuite` only proves runtime acceptance of that exact `(suite name, selector)` key. It does not prove semantic safety for a different suite generation.
- Runtime exports and trace category names are evidence surfaces, not supported third-party ABI contracts.
- Any refuted prospective prediction requires model revision before promotion; the release guard must not convert a contradiction into an L5 success.

## Failure diagnostics

`probes/process-tools/diagnose_aeig_l5_operator_run.py` reports the earliest missing stage without mutating evidence. Run it with Python when diagnostics are needed. It is diagnostic-only and is not part of the frozen promotion decision path.

## Version/build scope
The canonical package is scoped to After Effects 26.3 and records `app.version`, build number, OS and operator-session identity. Results are not automatically generalized to 26.5 or earlier releases; later replication is a separate version-lineage task.

The frozen AEX hash and prediction lock ensure the observation is interpreted against the exact pre-observation probe/model rather than a modified implementation.

## What this run does not prove
The run does not prove every internal BEE/RG class layout, every cache domain or universal suite availability. It tests a small set of pre-locked claims under one controlled fixture and uses that evidence only for the corresponding domain gates.

An `inconclusive` prediction remains unresolved. A refutation is preserved as evidence and blocks promotion until the model is explicitly revised; rerunning until a preferred answer appears is prohibited.

Related: `docs/reference/release-readiness.md`, `docs/foundations/evidence-model.md`, `docs/foundations/version-model.md`, `datasets/aeig-prediction-lock.csv`.
