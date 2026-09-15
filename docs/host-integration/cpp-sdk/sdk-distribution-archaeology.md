---
status: active
last_verified: 2026-09-16
evidence: AE 25.6 distributed SDK deep-mining corpus + platform parity + historical headers
---
# SDK Distribution Archaeology

The downloadable SDK is not merely build scaffolding. It is a versioned primary-source corpus containing ABI layout, retired suite generations, loader/runtime infrastructure, developer warnings, internal-build boundaries and Adobe-authored call sequences that the prose Guide cannot reproduce exhaustively.

AEIG therefore treats **Guide prose**, **distributed headers**, **samples/utilities**, and **runtime observation** as separate evidence surfaces.

## Current mined corpus
The retained 25.6 distribution has been machine-mined into:
- **284 files** in the deep-mining inventory;
- **388 scored developer-comment leads**;
- **5,680 API/suite usage records**;
- current suite/version/name registries;
- old/current prefix-layout comparisons;
- Windows/macOS semantic header parity;
- private/internal gate candidates.

These counts describe the retained corpus, not all Adobe source code.## High-value files and why
`AE_GeneralPlug.h` gives current AEGP/Artisan contracts; `AE_GeneralPlugOld.h` preserves more than ten thousand lines of retired generations and is often the best source for when a capability appeared or changed. `AE_Effect.h` and old Effect suites preserve selector/flag compatibility history.

`AE_ComputeCacheSuite.h` is unusually rich in operational comments about single-flight behavior, checkout receipts, memory sizing and purge lifetime. `AE_HashSuite.h` exposes host-compatible GUID construction. `AE_AdvEffectSuites.h` contains state/time/rerender escape hatches.

The SweetPea/PICA headers (`SPRuntme.h`, `SPPlugs.h`, `SPSuites.h`, `SPCaches.h`, `SPAccess.h`) reveal module loading, suite negotiation and cache/purge behavior beneath AE-specific wrappers.

Samples reveal real integration sequences. `ProjDumper`, `QueueBert`, `Persisto`, `Supervisor`, `SmartyPants`, `Resizer`, `HistoGrid` and GPU samples are especially valuable because they exercise state, rendering, persistence, threading and UI boundaries.

## Evidence ranking
A declaration proves that a contract was distributed, not that every host/version supports it identically. A comment can clarify intended semantics but can be stale. A sample proves Adobe expected a call sequence to work for its target generation, not that the sample is bug-free or modern best practice.

Therefore surprising sample behavior is always checked against headers, Guide prose, sibling samples and runtime evidence.## Version archaeology workflow
For a symbol/suite/flag:
1. locate it in the current header;
2. search frozen/old suite generations;
3. record suite name and PICA selector independently from product version;
4. inspect comments around introduction/deprecation;
5. inspect Adobe samples using it;
6. compare retained SDK releases and current host negotiation;
7. only then infer version availability.

Do not infer runtime availability from header presence alone. A header can retain obsolete ABI, a suite can be context-scoped, and a newer host may accept selector integers not present in an older distributed SDK.

## Platform boundary
The retained 25.6 Windows/macOS public headers normalize to the same semantic text/identifier surface, but that does not imply binary-loader, calling-convention, resource, filesystem or sample-project parity. Header parity removes one source of API divergence; it does not erase platform implementation differences.

## Failure and bug mining
Developer comments such as explicit thread-safety warnings, obsolete compatibility notes, internal/deprecated markers and receipt/cache warnings are promoted into research leads rather than silently discarded. Sample defects are tracked separately in `sample-pitfalls.md`.

## Unknown frontier
Distributed SDK archaeology cannot expose non-distributed private source/layout. It can establish public ABI history, adjacent private vocabulary and falsifiable expectations, but runtime/private implementation claims require another evidence class.

Machine evidence: `datasets/ae-sdk-25.6-deep/`, `datasets/ae-sdk-lineage-cs6-cc2014-25_6.csv`, `datasets/ae-sdk-25.6-suite-versions.csv`, and the Master Surface Registry.