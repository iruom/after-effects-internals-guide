---
status: active
last_verified: 2026-09-15
---
# Host Reimplementation Failure Patterns

A host emulator is a powerful AE research instrument because failure localizes contracts that ordinary plug-in development rarely exposes. This page records failure classes, not blame on any one implementation.

## 1. Suite name matched, version ignored
**Pattern:** `AcquireSuite(name, version)` logs `version` but dispatches only on `name`.

**Why dangerous:** historical suite generations are not universally prefix-compatible. Function index and signature can diverge between versions.

**Evidence:** distributed old headers + AexExecutor dispatcher + observed plug-in requests.

**Correct research question:** which exact suite generation does the caller request, and what layout does AE return for that integer?

## 2. Unknown Adobe-looking suite returned as success
**Pattern:** return a large dummy function table for any name beginning with `AE`, `PF`, `ADBE`, `SP`, `Pr`, `Adobe`, `SweetPea`, or similar.

**Why dangerous:** acquisition success communicates capability. A caller can immediately execute a function whose semantics, output initialization, ownership and threading rules the host does not implement.

**Research use:** catalog which suites are only presence-tested versus actually invoked after acquisition.
## 3. Output storage treated as pre-initialized
**Pattern:** callback code assumes caller-provided output structs/pointers already contain valid objects.

**Why dangerous:** SDK-style callbacks often require the host to initialize caller storage completely. Independent emulators have exposed crashes from treating output slots as input objects.

## 4. Temporary wrapper escapes callback lifetime
**Pattern:** return a pointer into stack/local wrapper state.

**Why dangerous:** plug-ins may retain the returned world/checkout object for the documented checkout lifetime, not merely the callback duration.

## 5. Plug-in-owned strings/pointers retained without copying
**Pattern:** save parameter UI string pointers after parameter setup.

**Why dangerous:** ownership may remain with the plug-in only for the call. Host must copy when the contract requires persistence.

## 6. GPU callback return mistaken for completion
**Pattern:** host reads output immediately after a plug-in enqueues device work.

**Why dangerous:** queue submission and callback return can precede GPU completion. Host/device synchronization is part of the effective contract.

## 7. Editable project state and render state collapsed into one mutable object
**Pattern:** render callbacks read/write the same live project structures used by UI mutation.

**Why dangerous:** modern AE architecture explicitly separates/synchronizes render-side project state; MFR further multiplies concurrent render contexts.

## AEIG rule
For each failure, record the minimum missing host responsibility and design a micro-plug-in that isolates it. A failure becomes strong evidence only when the same boundary is supported by an Adobe contract, independent implementation, or controlled experiment.

## 8. Typed vtable returned for the wrong PICA integer
**Pattern:** improve on name-only dispatch by checking a numeric range, but return one typed table for every integer in that range.

**Why dangerous:** suite integers are not necessarily monotonic generations. `PFAppSuite6` is published as PICA version 1, while older Suite4 and Suite5 use 6 and 7. A contiguous range can therefore fabricate unsupported versions and map real historical versions to the wrong layout.

**Observed contrast:** AexExecutor ignores the integer almost entirely; aexlo checks ranges but still aliases several incompatible families. This is a useful progression of failure modes, not evidence that either behavior matches AE.

## 9. Callable success is mistaken for semantic implementation
**Pattern:** every vtable slot is non-null and returns success, but required outputs/state changes are omitted.

**Why dangerous:** ABI callability prevents an immediate indirect-call crash, yet the next host/plugin operation can consume uninitialized or stale state. Capability presence, ABI compatibility, and semantic compatibility must be tested separately.

See `research/findings/F-ABI-006-independent-host-suite-dispatch-failure-taxonomy.md` and `datasets/aexlo-suite-dispatch-audit.csv`.