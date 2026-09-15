---
status: confirmed
last_verified: 2026-09-14
evidence: AE-25.6-distributed-header
---
# F-ABI-001 — Parameter-flag bits are reused by parameter type and host

`PF_ParamFlag_USE_VALUE_FOR_OLD_PROJECTS` occupies bit 7 for ordinary parameter types. For `PF_Param_LAYER`, the exact same bit is aliased as `PF_ParamFlag_LAYER_PARAM_IS_TRACKMATTE`.

The Header states that the Track Matte interpretation is supported by Premiere and ignored in After Effects. A serialized/raw bit value therefore does not have a globally unique semantic meaning; interpretation depends on parameter type and host.

The same enum also exposes bit 10 as `unused, feel free to use this`, while bit 11 is reserved for internal use with the unusually explicit warning `it IS in use, don't use it!`.

## Architectural implication
Effect ABI bitfields are historical compatibility spaces, not clean modern enums. Reserved and aliased bits preserve old project behavior and host-specific extensions without changing structure layout.

## Developer rule
Never infer semantics from raw flag bits without `(SDK generation, host, parameter type)` context. Preserve unknown/reserved bits when transforming persisted structures unless the contract explicitly says to clear them.