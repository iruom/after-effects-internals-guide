---
status: active
last_verified: 2026-09-16
evidence: AE_Effect.h compatibility macros + Guide compatibility table + retained SDK generations
---
# PF Effect API Version Lineage

After Effects product version, PF Effect API version and suite generation are separate compatibility axes. Treating them as one number is a recurring source of broken version checks.

## The three-axis model
A robust plug-in asks separately:

`Host/Product = After Effects build/version`

`PF ABI = PF_AE_PLUG_IN_VERSION + PF_AE_PLUG_IN_SUBVERS`

`Capability = exact suite name + suite selector/version + successful acquisition`

None can be safely inferred from either of the others.

## Historical ledger
`AE_Effect.h` preserves release markers (`PF_AE*_PLUG_IN_VERSION` / `SUBVERS`) reaching back through decades of AE releases. AEIG's extracted lineage contains 36 release markers spanning AE 3.1 through the 23.x era in the retained current header corpus.
The sequence is intentionally non-uniform: some AE product releases share the same PF API marker, while other capabilities arrive through independently versioned suites without changing the core PF version.

The retained 25.6 SDK still aliases the current PF compatibility macros to the AE 23.5-era pair `13/29`. That does **not** mean AE 25.6 behaves like AE 23.5; it means no incompatible core Effect API bump was required for that axis.

## Why product-version checks are weak
A host can expose a newer product version while retaining older PF ABI numbering. Conversely, a sibling host such as Premiere can report a PF-compatible interface while differing in suite availability and render semantics.

Therefore code like:

`if (PF version >= X) assume suite Y exists`

is weaker than acquiring suite Y and handling absence explicitly.

## Suite lineage is often the real capability version
Modern additions frequently arrive by bumping a suite generation:
- StreamSuite7 in AE 26.5 adds layer-input render-stage access;
- historical Comp/Layer/Canvas suites add specific behaviors independently;
- Color Settings, Track Matte, Guide and ItemView features evolve through suite versions.

This allows Adobe to preserve old PF entry-point compatibility while expanding host functionality.
## Failure modes
- using `app.version` / product major as a proxy for PF ABI;
- assuming a historical PF subversion uniquely identifies the full host build;
- assuming the newest suite exists because the PF API version is new enough;
- using PF version to infer Premiere/other-host semantics;
- hard-coding capability tables instead of attempting suite acquisition where possible.

## Archaeological value
Version macros are still useful as a **compatibility ledger**. They establish lower bounds for when a core ABI revision existed and help date sample/header code whose surrounding documentation has drifted.

Cross-check them with:
- exact SDK package/date;
- header comments and suite-version macros;
- sample code using the feature;
- product release notes;
- runtime suite-negotiation observations.

## Experiment
Build a tiny probe that logs host/product version, PF version/subversion and the success/failure of selected suite generations. Run it across retained AE versions. This produces an empirical capability matrix rather than relying on release-number inference.

Dataset: `datasets/ae-pf-api-version-lineage.csv`. Finding: `F-ABI-019-product-version-is-not-pf-api-version.md`. Cross-links: `../host-integration/cpp-sdk/suite-versioning-and-abi.md`, `../host-integration/pica-sweetpea/runtime-architecture.md`.