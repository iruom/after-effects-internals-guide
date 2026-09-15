---
status: generated
last_verified: 2026-09-15
---
# API Completeness Status

This page is generated from the locally scanned SDK/header corpora plus the current official Guide identifier surface.

Unique discoverable identifiers: **5023**.

## Corpus counts

- `guide-current`: 2341 rows
- `sdk-13.5-thirdparty-snapshot`: 6563 rows
- `sdk-25.6`: 7466 rows
- `sdk-cc2014-thirdparty-archive`: 6390 rows
- `sdk-cs6-thirdparty-archive`: 5386 rows
- `sdk-local-pre25.6`: 7334 rows

## Visibility classes

- `cross-host-distributed`: 562
- `historical-compat-distributed`: 4671
- `official-public-guide`: 2341
- `private-gate-reference`: 61
- `public-distributed`: 9506
- `thirdparty-historical-archive`: 18339

## Cross-surface deltas

- Guide 26.5 identifiers absent from the raw local SDK 25.6 corpus: **255**
- Guide identifiers present in raw 25.6 headers but missed by structured extraction: **0**
- SDK 25.6 structured identifiers absent from current Guide: **2660**
- Local pre-25.6 raw identifiers absent from SDK 25.6 raw corpus: **2**
- CS6 archive identifiers absent from raw SDK 25.6: **8**
- Raw SDK 25.6 identifiers absent from the CS6 archive: **885**
- CC2014-only identifiers absent from both CS6 and SDK 25.6: **7**
- Identifiers introduced between CS6 and CC2014: **475**
- CC2014 identifiers absent from SDK 25.6: **12**
- Raw SDK 25.6 identifiers absent from the CC2014 archive: **417**

The `sdk-local-pre25.6` snapshot is deliberately not assigned an exact AE release until its provenance is independently verified.
Header-only does not automatically mean hidden/unsupported; it can be ABI detail, sample support, cross-host support, deprecated compatibility, or documentation lag.
