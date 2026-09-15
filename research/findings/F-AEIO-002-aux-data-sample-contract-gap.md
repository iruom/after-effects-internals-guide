---
status: observed
last_verified: 2026-09-14
evidence: distributed-sample + distributed-header
---
# F-AEIO-002 — SDK_IO advertises auxiliary data but leaves aux callbacks unset

The AE 25.6 `AEGP/IO` sample sets `AEIO_MFlag_HAS_AUX_DATA` in `AEIO_ModuleInfo`.

However, its `ConstructFunctionBlock()` zero-initializes `AEIO_FunctionBlock4` and does not assign `AEIO_GetNumAuxChannels`, `AEIO_GetAuxChannelDesc`, `AEIO_DrawAuxChannel`, or `AEIO_FreeAuxChannel`.

The public Guide marks these callbacks optional in the generic function-block table, but `HAS_AUX_DATA` semantically claims that the format carries depth, normals, or other non-color per-pixel data.

## Interpretation
Treat this as a sample-contract inconsistency or unfinished scaffold, not proof that null auxiliary callbacks are a supported implementation of `HAS_AUX_DATA`.

## Developer warning
Do not cargo-cult the sample flag set. If your AEIO advertises auxiliary data, implement and test the corresponding enumeration/draw/free path explicitly.