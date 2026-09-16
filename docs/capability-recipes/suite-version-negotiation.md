---
status: active
last_verified: 2026-09-15
---
# Recipe: Negotiate Suite Versions Safely

## Goal
Support multiple AE generations or implement a host without corrupting ABI when suite versions change.

## Core rule
The acquisition key is `(suite name, exact PICA selector)`. C table generation numbers and PICA selector integers are different dimensions.

AEIG's generated matrix currently contains 158 generation rows across 54 AEGP/PF suite families. Mechanically compared adjacent layouts include both prefix-safe and prefix-unsafe transitions.

## Why numeric ranges are unsafe
`PFAppSuite` demonstrates a selector reset from PICA `7` to `1` while the C table generation increases. Other families reorder, replace or remove fields. Therefore logic such as `if version <= newest return newest_table` is not a valid generic compatibility rule.

## Correct host/client strategy
- request the exact documented selector for the table type you compiled against;
- test the acquisition result, not numeric ordering;
- release every successfully acquired suite;
- if implementing a host, dispatch on exact `(name, selector)` pairs;
- alias a table only after a per-transition layout/semantic proof.

## Capability discovery
A plug-in can probe a known suite-name string with selector integers without dereferencing an unknown returned table. The canonical `EXP-PLUGIN-001` does this over 48 suite names × selectors 1..32 and immediately releases successful acquisitions.

This can discover that a host recognizes a newer selector, but it **does not** provide the newer C layout. Do not call an unknown table until its ABI is independently known.

## Emulator warning
A non-null suite pointer and success error code are insufficient. Independent hosts also fail through unwritten out-parameters, fake capability presence and success stubs with no semantic effect.

Related: `F-ABI-002`, `F-ABI-003`, `F-ABI-006`, `F-ABI-008`, `F-ABI-013`.

## Official client-side acquisition contract
Modern C++ SDK guidance recommends `AEFX_SuiteScoper`: acquire the exact suite name/version needed, release automatically, and either handle `A_Err_MISSING_SUITE` or opt into a nullable acquisition and test the pointer.

For a client supporting several host generations, the safe strategy is capability negotiation:

`try newest table you understand -> if missing, try previous known table -> adapt behavior to the acquired contract`.

Do not branch only on `app.version` and then dereference a suite you never acquired. Product version, C table generation and PICA selector evolve on different axes.

## Why exact selector dispatch matters for host implementations
AEIG's static layout analysis found both prefix-compatible and prefix-incompatible adjacent suite generations. Some tables append fields; others reorder/replace/remove. `PFAppSuite` additionally demonstrates that PICA selector numbering can reset while the C table generation increases.

Therefore an emulator/alternative host must dispatch exact `(suite_name, selector)` pairs and expose the table layout matching that selector. Returning one latest table for every selector is not generically ABI-safe.

## Runtime matrix adds empirical evidence
The canonical `EXP-PLUGIN-001` performed 1,536 selector attempts across 48 suite families × selectors 1..32 in AE 26.3. The observed accepted selector patterns are family-specific rather than one global monotonically increasing namespace.

This confirms a crucial rule: **a selector integer has meaning only together with the suite name**.

A successful acquisition of an unknown newer selector proves recognition, not that an older SDK knows the returned table ABI. Never call through an unknown layout merely because `AcquireSuite` returned success.

## Threading and lifetime
Suite acquisition/lifetime has its own rules. The AEGP implementation guide explicitly states `SPBasicSuite` itself is not thread-safe. Do not turn a suite pointer into a casually shared global capability merely because the pointed functions look stateless.

RAII acquisition should be scoped around the work that needs the suite unless the contract explicitly supports longer retention. Release exactly what was successfully acquired.

## Failure modes
- map host product version directly to a presumed suite table;
- treat selector integers as globally ordered versions;
- return latest table for an old selector in an emulator;
- accept an unknown selector and then cast it to the newest table type available in your SDK;
- forget that a suite can be absent in another Adobe host even when the same PF effect loads there;
- call suite acquisition from an unsupported render thread because the eventual function is thread-safe.

## Capability test matrix
For every used suite record: name string, selector, C table type/generation, earliest observed host, successful acquisition, required/optional capability and fallback path. For alternative-host compatibility, add semantic tests for every exposed function rather than declaring success from non-null suite pointers.

## Unknown frontier
Static headers and runtime selector acceptance do not reveal undocumented field semantics of unknown newer tables. The current 48-family runtime capture is one AE 26.3 environment, not a universal matrix for every host/build. Repeat across host versions and sibling Adobe hosts before generalizing.

Related: `docs/host-integration/pica-sweetpea/suite-versioning.md`, `docs/archaeology/pf-api-version-lineage.md`, `datasets/ae-suite-negotiation-matrix.csv`.
