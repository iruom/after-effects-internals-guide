---
status: active
last_verified: 2026-09-14
---
# Evidence Model

AEIG grades evidence by provenance and reproducibility. Grades are not a simple ranking: a current Guide page may define supported behavior, while a distributed header can expose ABI details and comments absent from the Guide.

| Grade | Evidence class | Typical use |
|---|---|---|
| E0-G | Current Adobe Guide / release documentation | supported public contract |
| E0-H | Distributed Adobe SDK header | exact types, flags, suite versions, raw developer comments |
| E0-S | Distributed Adobe sample source | host assumptions demonstrated by Adobe code |
| E0-L | Distributed old/deprecated SDK header | historical contract and removed observation surfaces |
| E1-A | Adobe patent, engineer statement, historical Adobe material | architecture history and design intent |
| E2-L | Locally observed AE artifact | trace/debug DB, prefs, crash symbols, module inventory |
| E2-X | Reproducible controlled experiment | behavioral confirmation / falsification |
| E2-T | Reproducible third-party parser or analysis | independently inspectable implementation clue |
| E3 | Community/forum/crash anecdote | discovery clue only |
| H | Explicit hypothesis | must have a falsification path |

A claim may cite multiple evidence classes. Cross-class agreement is preferred over multiple sources of the same kind.
## Third-party implementation evidence
`E2-T` is split conceptually into parser/analysis evidence and executable reimplementation evidence. Use `E2-R` when a third party has reimplemented an Adobe-facing ABI, host service, or persistence reader/writer and the implementation can be inspected or executed.

| Grade | Evidence class | Typical use |
|---|---|---|
| E2-R | Reproducible independent reimplementation | ABI/lifecycle constraints that had to be reproduced for compatibility |

Third-party repositories are graded at the **claim level**, not the repository level. Within one repository distinguish:
- README/documentation claim;
- source-code assumption;
- automated test expectation;
- fixture or real-file observation;
- behavior reproduced against actual AE/Premiere.

A source file outweighs a stale README only for describing what that implementation currently does; neither proves what AE itself does. A failing or divergent reimplementation is also valuable evidence because the failure localizes a hidden contract.

## Evidence is claim-specific
No grade is universally strongest. A current Guide is authoritative for supported contract but may omit ABI comments; a header is stronger for exact struct/selector layout; a runtime export proves implementation presence but not supported invocation; a controlled experiment proves behavior only under its recorded environment.

Every claim should therefore state **what dimension the evidence supports**: public support, ABI/layout, runtime presence, behavioral semantics, version lineage, ownership/lifetime or design intent.

## Promotion and contradiction rules
A hypothesis becomes a Finding only when its evidence and falsification status are explicit. Contradictory experiment results are preserved and force model revision; they are not averaged away by accumulating more same-direction prose sources.

Cross-host and historical evidence can motivate predictions but cannot silently promote an AE-current claim. Likewise multiple binary strings from one build are not independent confirmations.

## Negative evidence
Absence is useful only when the observation surface is known complete for that claim. A missing export, trace line or Guide entry may reflect stripping, disabled instrumentation, host scope or documentation omission. AEIG records negative evidence with the completeness assumption that makes it meaningful.

## Cross-links
See `docs/troubleshooting/failure-model.md`, `docs/troubleshooting/fixed-issue-architecture-mining.md`, `docs/capability-recipes/observe-internals-safely.md`, `docs/foundations/version-model.md`, and `docs/reference/bug-quirk-registry.md`.
