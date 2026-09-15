---
status: confirmed
last_verified: 2026-09-15
evidence: E0-H + E0-L + E2-R/local-log
---
# F-ABI-002 — Suite generation name and PICA version integer are different namespaces

Distributed AE 25.6 headers show that the C struct generation and the integer passed to PICA `AcquireSuite()` do not numerically match.

Example: `AEGP_CompSuite10` uses PICA version integer `21`; `AEGP_CompSuite11` uses `25`; `AEGP_CompSuite12` uses `26`.

Therefore a runtime log such as `AcquireSuite("AEGP Comp Suite", 21)` must not be interpreted as evidence for an `AEGP_CompSuite21` type or private 21st generation.

Historical AexExecutor logs containing Comp Suite integer 21 are consistent with the public `AEGP_CompSuite10` contract frozen in AE 12.

## Research consequence
All suite-acquisition traces must first be decoded through the exact header-era name/version map before classifying an observed integer as undocumented.

Machine-readable mapping: `datasets/ae-sdk-25.6-suite-versions.csv`.
