---
status: confirmed-header
last_verified: 2026-09-15
evidence: AE-25.6-distributed-headers + independent-host-review
---
# F-ABI-005 — Suite numeric versions are not a monotonic generation number

The `PF AE App Suite` demonstrates that Suite generation and PICA version integer are independent and the integer sequence is not globally monotonic:

- `PFAppSuite4` uses numeric version 6.
- `PFAppSuite5` uses numeric version 7.
- `PFAppSuite6` uses numeric version 1.

In addition, Suite4→5 is not prefix-compatible: `PF_AppGetLanguage` is inserted at index 2, shifting later slots.

Therefore a host must not infer `newer >= older`, pick the largest numeric version, or blindly alias a numeric range to one latest vtable.
## Independent-host consequence
At the reviewed snapshot, `aexlo` accepts `PF AE App Suite` versions `1..=6` and returns one `PFAppSuite6` table. Because historical layouts are not universally prefix-compatible and version integers are non-monotonic, this alias range is an emulator convenience, not a valid general AE compatibility rule.

The same caution applies to `PF Param Utils Suite`: the old v1 table contains obsolete state/change functions, while v3 replaces early slots and has fewer functions. Returning the v3 table for v1 requests would reinterpret function indices/signatures.

## Safe host rule
Treat `(suite_name, requested_version)` as an exact ABI key. Provide a compatibility alias only after a header-level table comparison proves the requested generation is prefix-compatible with the returned table and the overlapping signatures/semantics are unchanged.