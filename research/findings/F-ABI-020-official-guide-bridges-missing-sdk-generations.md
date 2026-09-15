---
id: F-ABI-020
status: confirmed
evidence: official-historical-document-lineage
last_verified: 2026-09-15
---
# Official Guide bridges missing SDK generations without replacing header evidence

## Finding
The current official C++ Guide preserves an API-version table spanning AE 3.1 through 22.0. It records product release, Effect API version and—where available—AEGP API version as separate axes.

Examples include CC 2017 / 14.0 = Effect API `13.13`, AEGP API `114.0`; CC 2017.1 / 14.2 = Effect API `13.14`; AE 15.0 = `13.15`; AE 16.0 = `13.16`; AE 18.2 = `13.25`; AE 22.0 = `13.27`.

The docsforadobe Git history begins in October 2018 and independently preserves later public transitions, including the June 2020 MFR documentation, March 2021 sequence-data/Compute Cache update, October 2021 AE 22.0 update, 2023 ColorSettingsSuite5/OCIO documentation, and later 25.x/26.5 changes.

## Boundary
This evidence fills chronology gaps but is not a substitute for missing distributed SDK header snapshots. It cannot prove exact struct layout, selector integer, ownership, threading or ABI compatibility for a missing generation.

## Consequence
AEIG must track at least four independent coordinates: product release, Effect API pair, AEGP API version, and exact suite-name/PICA generation. See `datasets/ae-official-api-version-lineage.csv`, `datasets/ae-official-guide-history-milestones.csv`, `datasets/ae-suite-negotiation-matrix.csv`, and `F-ABI-013-suite-negotiation-is-a-two-key-contract.md`.
