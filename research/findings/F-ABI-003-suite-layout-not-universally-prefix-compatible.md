---
status: confirmed
last_verified: 2026-09-15
evidence: E0-H + E0-L
---
# F-ABI-003 — Historical AEGP suite layouts are not universally append-only

Mechanical parsing of `AE_GeneralPlug.h` and `AE_GeneralPlugOld.h` shows that multiple adjacent suite generations are not prefix-compatible.

Examples:
- `AEGP_CompSuite9 → AEGP_CompSuite10`: first function-order mismatch at index 7.
- `AEGP_ItemSuite2 → AEGP_ItemSuite3`: the newer table is shorter.
- `AEGP_ItemSuite8 → AEGP_ItemSuite9`: table size and ordering change.
- several later Layer Suite generations are prefix-compatible, demonstrating that compatibility strategy varies by suite and era.

## Consequence
A host emulator cannot safely satisfy arbitrary historical requests by returning one later suite table unless that exact transition has been proven prefix-compatible.

The requested PICA version is therefore ABI-significant, not merely advisory capability metadata.

Machine-readable comparison: `datasets/ae-sdk-25.6-suite-prefix-compat.csv`.
