---
status: confirmed
last_verified: 2026-09-14
---
# F-KERNEL-001 — Several kernel/sampling modes are declared but unimplemented

AE 25.6 `AE_EffectCB.h` explicitly marks `PF_KernelFlag_USE_CHAR`, `PF_KernelFlag_USE_FIXED`, `PF_KernelFlag_REPLICATE_BORDERS`, and `PF_KernelFlag_ALPHA_WEIGHT_CONVOLVE` as unimplemented/ignored. The public Guide repeats these limitations.

The same header preserves proposed `PF_SampleEdgeBehav_REPEAT` and `WRAP` values inside a commented-out `Sorry, not supported!` block.

This is direct evidence that the SDK surface contains abandoned design branches. Declared constants must not be treated as evidence of implemented host behavior.
