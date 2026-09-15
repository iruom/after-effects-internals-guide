---
status: confirmed-reimplementation-risk
last_verified: 2026-09-15
evidence: E2-R independent host source audit
versions: reviewed aexlo snapshot + local AexExecutor snapshot
---
# F-ABI-008 — Success stubs can fabricate host semantics while leaving outputs undefined

The reviewed `aexlo` suite source uses `stub_log!` callbacks that log and return `PF_Err_NONE` without touching any argument. A mechanical audit finds 48 such callbacks in the current suite snapshot.

Of those, **44 carry mutable or explicitly named output arguments**. Examples include media timecode, frame rate, duration/start, timeline ID, clip/file name, metadata strings, trim state and track-empty state. Returning success leaves caller-visible output storage untouched.

Four additional stubs represent setters/dependency declarations or capability-like actions that return success without implementing the state change.

This is not an ABI-layout problem: the function pointer can have the correct signature and still violate the host contract semantically.

AexExecutor exhibits the same failure class more broadly: `s_unknown_suite[1024]` fills every slot with `unknown_suite_fn`, and that function returns `A_Err_NONE` while its attempted output-zeroing code is disabled. Broad Adobe-looking suite names can therefore acquire successfully and expose a callable table with no suite-specific semantics.

## Compatibility hierarchy
`non-null/callable -> ABI-compatible -> output/ownership-correct -> semantically implemented`.

Each implication is one-way. Host-emulator testing should verify these layers separately.

## Reproducible audit
Run `probes/process-tools/audit_semantic_success_stubs.py`. It writes `datasets/independent-host-semantic-success-stubs.csv` with function-level classification.

Current snapshot summary:
- 44 `success-with-unwritten-output` rows;
- 4 `success-with-no-semantic-effect` rows;
- 1 AexExecutor `broad-success-fabrication` row.

These counts describe the reviewed independent implementations, not After Effects itself. Their research value is that they identify callbacks where a real host must provide hidden state or ownership semantics that a superficial ABI clone can omit.
