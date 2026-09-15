---
status: confirmed-public
evidence_grade: E0
versions: "legacy-current SDK contract"
last_verified: 2026-09-14
---
# Sequence data has serialization-driven duplication semantics

## Official contract
`PF_Cmd_SEQUENCE_FLATTEN` occurs on save and duplication. `PF_Cmd_SEQUENCE_RESETUP` occurs after disk load, precomposition and copying. During duplication, RESETUP is sent to both old and new sequences, and plug-ins must not assume FLATTEN occurs between successive RESETUPs.

## Interpretation
Effect instance state crosses a serialization boundary even inside an editing session. Duplication is therefore not necessarily a shallow in-memory clone; the contract permits reconstruction through a flattened representation.

## Implementation risk
Pointers/handles embedded in sequence state are nonportable and must be rebuilt. Hidden ownership or aliasing assumptions can break under duplicate/copy/precomp/MFR.

## Research target
Trace instance identities and sequence blob hashes through duplicate, copy/paste, precompose, undo/redo, save/reload and MFR worker copies.

## Sources
https://ae-plugins.docsforadobe.dev/effect-basics/command-selectors/
https://ae-plugins.docsforadobe.dev/effect-details/global-sequence-frame-data/