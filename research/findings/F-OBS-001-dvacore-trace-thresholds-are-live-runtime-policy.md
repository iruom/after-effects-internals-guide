---
id: F-OBS-001
status: replicated-local
last_verified: 2026-09-15
evidence_grade: E3-X
versions: "AE 25.6.4 installed dvacore.dll"
---
# dvacore trace thresholds are live runtime policy

## Observation
`EXP-OBS-002` loaded the installed `dvacore.dll` in two fresh standalone processes, loaded the AE 25.6 Trace Database text, installed `MasterTraceToStdErr`, and evaluated messages through `TraceEnabled` before emission.

With category volume 5, master volume 3 produced `enabled246=100`; master volume 10 produced `enabled246=110`. Level 2 was emitted in the low-master condition, level 4 only in the high-master condition, and level 6 was rejected in both because it exceeded category volume 5.

Both replications exited 0 and produced identical decision stdout hashes.
## Model
The effective predicate is consistent with a threshold bounded by both the global/master volume and the category volume. The low-level `Trace()` export itself emits directly; the filter lives in the caller-visible `TraceEnabled()` predicate.

## Important negative result
`SetTraceVolume` increments `TraceChangeCount` in the standalone process but does not alter `GetTraceVolume`; category-level dynamic mutation therefore remains unresolved and must not be assumed to work outside the full host registration context.

## Reproducibility
Manifest: `experiments/observatory/manifests/EXP-OBS-002.json`.
Raw captures, executable, source, environment and SHA-256 records are retained under `experiments/observatory/runs/EXP-OBS-002/`.

## Consequence
Trace Database categories such as BEE/RG/TDB/GPU are not merely archaeological vocabulary. The installed runtime contains an active thresholded trace system that can support controlled AEIG experiments once the relevant providers are registered by the host.
