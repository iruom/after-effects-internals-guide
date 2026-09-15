# AEIG 1.0 Operator Handoff

Static RC fingerprint: `37893B3E6B3837965E9B1F6548D93B981992E18C33F0F7BC85B62D50535C959B`

The Static RC is frozen at 32 artifacts plus 7 prospective predictions. Do not edit the canonical package, probe binary, fixture, analyzers, prediction text, or frozen manifests before the run.

## Before opening After Effects

1. Save normal AE work and close After Effects yourself.
2. Run `AEIG-1.0-L5-PREFLIGHT.cmd` from this directory.
3. Continue only if it reports `AEIG L5 OPERATOR PREFLIGHT: PASS (0 blocker(s))`.
4. Open `AEIG-1.0-L5\README.md` and follow its steps exactly.

## During the run

Use a disposable empty project. Run `01_RUN_IN_AE.jsx` exactly once via **File > Scripts > Run Script File...**. Do not edit generated logs or retry individual passes inside the same capture.

## After the run

Close AE yourself, remove the temporary probe with the canonical removal script, then run `02_VERIFY_RESULTS.cmd`. Preserve all raw captures even if verification reports incomplete or a refuted prediction.
