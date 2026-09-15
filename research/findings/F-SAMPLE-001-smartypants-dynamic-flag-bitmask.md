---
status: probable-source-bug
last_verified: 2026-09-14
evidence: AE-25.6-distributed-sample + sibling-sample comparison
---
# F-SAMPLE-001 — SmartyPants likely contains a Dynamic Flags bitmask defect

`SmartyPants::QueryDynamicFlags()` executes `out_data->out_flags2 &= PF_OutFlag2_DOESNT_NEED_EMPTY_PIXELS` when its channel parameter selects alpha.

That expression retains only the target bit; it does not clear the target bit. In the same AE 25.6 SDK, `Resizer::QueryDynamicFlags()` uses the conventional and semantically expected clear form `out_flags2 &= ~FLAG` for dynamic 3D flags.

SmartyPants' Global Setup and PiPL do not advertise `PF_OutFlag2_DOESNT_NEED_EMPTY_PIXELS`, making the line especially suspicious: absent host-provided state, the expression can collapse unrelated dynamic bits while still failing to set the intended bit.

## Confidence
High confidence as a source-level logic defect candidate. Runtime impact remains host-contract dependent and should be measured before labeling it an observable AE bug.

## Test
Instrument Query Dynamic Flags, record incoming/outgoing `out_flags2`, toggle the Alpha channel, and compare cache/bounds behavior against a corrected local build using `|=` or `&= ~` according to intended semantics.