---
status: generated
last_verified: 2026-09-16
release_state: AEIG-1.0-static-rc
---
# AEIG 1.0 Static Release Candidate

The static side of AEIG 1.0 is frozen before the final operator experiment.

## Frozen identity

- Static RC manifest: `datasets/aeig-static-rc-manifest.csv`
- Immutable prediction lock: `datasets/aeig-prediction-lock.csv`
- Frozen artifacts: **56**
- Prospective predictions locked: **7**
- RC fingerprint: `406B70458F0D808891879AFAD610981C518ED7D7BADCC9C7720ACB31C6F64433`
- Fingerprint record: `datasets/aeig-static-rc-fingerprint.txt`

`verify_aeig_static_rc.py` validates every frozen artifact, the immutable prediction fields, and the aggregate fingerprint before promotion.

## Static completeness snapshot

- Domain target: **24/27** before the remaining operator evidence.
- Remaining below target: **state-identity, render-graph, cache**.
- C++ identifier inventory: **5,023** rows in the completeness classification.
- Master Surface Registry: **53,728 rows / 13 surface classes**.
- Findings audited: **127**.
- Capability Frontier: **24 capabilities**.

## Master Surface Registry query

Use `probes/process-tools/query_master_surface.py` for cross-surface search.

```powershell
python probes/process-tools/query_master_surface.py RenderGuid --kind bee
python probes/process-tools/query_master_surface.py BEE_Cache --facets
python probes/process-tools/query_master_surface.py --capability-only --format json
```

Treat `support_class`, `host_scope`, `version`, `evidence` and `contract_boundary` as mandatory context; runtime visibility is not a supported third-party contract.

## Remaining promotion gates

AEIG 1.0 remains unreleased while any required domain is below target, any locked prediction is pending, or any refutation remains unrevised.

## Operator handoff

`experiments/user-run/AEIG-L5-PREPARE.cmd` performs static verification, archives mutable prior captures, re-runs clean preflight, and installs the temporary probe.
The user then starts AE 26.3, uses a disposable empty project, runs `AEIG-1.0-L5/01_RUN_IN_AE.jsx` once, and closes AE.
`experiments/user-run/AEIG-L5-FINISH.cmd` removes the probe and invokes verification/finalization.
