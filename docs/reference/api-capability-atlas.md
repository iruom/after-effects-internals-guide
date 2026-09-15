---
status: active
last_verified: 2026-09-15
---
# API / Capability Atlas

AEIG separates **API inventory** from **capability reconstruction**. A symbol existing in a Guide, header or DLL does not prove that a plug-in can safely perform the corresponding operation.

## API identity
A callable contract is keyed by more than a name:

`surface × host × version × suite-name × PICA/version integer × callback/layout × selector/context × thread/execution domain`

Two entries with the same human-readable suite name may therefore be ABI- or semantics-incompatible.

## Evidence surfaces
- official/current Guide contract;
- current distributed headers and Adobe samples;
- distributed `Old` compatibility headers;
- historical SDK snapshots with provenance;
- Scripting and Expression object models;
- Premiere/shared-host parallels;
- installed PE exports/imports and module dependencies;
- debug database, trace, preferences, logs and crash/runtime artifacts;
- AEP/AEPX/FFX persistence differentials;
- independent hosts/reimplementations used as adversarial specifications.
## Capability maturity
AEIG records supported and unsupported surfaces on separate ladders.

| Level | Meaning |
|---|---|
| `S0` | name/contract fragment known |
| `S1` | supported API contract identified |
| `S2` | valid host/context/thread/ownership rules identified |
| `S3` | dependency, invalidation and cache-safety implications identified |
| `S4` | behavior reproduced by controlled experiment |
| `I1` | internal binary/diagnostic candidate exists |
| `I2` | internal call path or semantics triangulated from multiple artifacts |
| `I3` | unsupported integration reproduced with exact version constraints |

`I3` never becomes `S1`: reproducible internal use remains unsupported and version-locked unless Adobe exposes a contract.

## Safety dimensions
For each capability record ownership, lifetime, UI/render-thread legality, reentrancy, dependency registration, cache invalidation, project mutation legality, host scope, version scope and failure mode.

A call that returns success but omits required output state is not implemented. A query that obtains render-relevant state without registering dependency is not cache-safe. A DLL export is not a public API. A Guide entry scoped to Premiere is not an AE capability.

## Unknown frontier
No inventory can prove completeness outside its corpus. Private non-exported methods, first-party-only extension contracts, generated runtime objects and host capabilities with no stable symbol/documentation surface remain explicit frontier classes.

Capability absence is therefore reported as "not present in current evidence surfaces" unless the observation surface is known complete for that capability class.

The Master Surface Registry should be used to triangulate names across surfaces, while the capability frontier records whether those observations have matured into supported or reproducible behavior.

## Cross-links
See `docs/host-integration/capability-frontier.md`, `docs/reference/master-surface-query.md`, `docs/foundations/evidence-model.md`, `docs/capability-recipes/suite-version-negotiation.md`, and `datasets/ae-master-surface-registry.csv`.
