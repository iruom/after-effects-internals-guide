---
status: confirmed-public
last_verified: 2026-09-15
evidence: current 26.5 C++ Guide host-scope note
---
# F-ABI-010 — Presence in the After Effects C++ Guide does not imply After Effects host support

The current shared plug-in Guide includes a 26.5 section whose subsequent PiPL Search Keywords / Description and Effects Panel Preview Media additions are explicitly scoped to Premiere Pro Beta 27.0 and explicitly stated not to apply to After Effects.

## Consequence
`documented in the AE plug-in Guide` is not a sufficient capability test. Every API/field must carry a `host_scope` dimension independently of the documentation site on which it appears.

This is especially important for shared Effect/PiPL headers, where AE and Premiere evolve at different rates and may expose different subsets or semantics from the same source vocabulary.
