---
status: generated
last_verified: 2026-09-15
---
# Corpus Coverage Status

AEIG completeness is measured against explicit corpora. A successful scan never implies that unacquired private or historical corpora do not exist.

Registered corpora: **18**. Scanned/fetched: **18**. Corpora with an unresolved note or scan failure: **15**.

## Coverage manifest

- `sdk-25.6-headers` — scanned; 68 files/items; 1.3 MiB; SHA-256 `873b5ad7089dcd28…`
- `sdk-25.6-mac-headers` — scanned; 68 files/items; 1.2 MiB; SHA-256 `deec382a1b227fc8…`
- `sdk-local-pre25.6-headers` — scanned; 66 files/items; 1.2 MiB; SHA-256 `afd6922856e486de…`
- `sdk-cs6-headers` — scanned; 34 files/items; 0.8 MiB; SHA-256 `4c8429860433007d…`
- `sdk-cc2014-headers` — scanned; 62 files/items; 1.0 MiB; SHA-256 `7c33d81735bae8de…`
- `ae-2025-runtime-pe` — scanned; 1111 files/items; 3458.1 MiB; SHA-256 `d127e993f8fc9d83…`
- `ae-debug-trace-stable` — scanned; 34 files/items; 0.3 MiB; SHA-256 `845b383d673b93cf…`
- `aexlo-snapshot` — scanned; 106 files/items; 0.6 MiB; SHA-256 `0bcf1f2387e7718d…`
- `aexexecutor-source` — scanned; 2432 files/items; 15.3 MiB; SHA-256 `e695357e1da6324a…`
- `aexexecutor-failure-logs` — scanned; 5 files/items; 6.1 MiB; SHA-256 `00ec1944c999ac15…`
- `sdk-25.6-premiere-shared` — scanned; 2 files/items; 0.0 MiB; SHA-256 `b8ece946e47e54ba…`
- `extension-substrate-ae2025` — scanned; 1 files/items; 0.1 MiB; SHA-256 `91c2eafe95ee35be…`
- `aep-experiment-corpus` — scanned; 17 files/items; 0.0 MiB; SHA-256 `2ef7c260bcbd0833…`
- `after-effects-sys-bindings` — scanned; 1 files/items; 1.0 MiB; SHA-256 `2c3a9e1ef751c658…`
- `cc2015-panel-sdk-samples` — scanned; 18 files/items; 0.1 MiB; SHA-256 `91661bb9606f036c…`
- `guide-26.5` — scanned-live; 1 files/items; 1.3 MiB; SHA-256 `7536e99abb8850b5…`
- `scripting-guide-current` — scanned-live; 1 files/items; 1.4 MiB; SHA-256 `92c512d269779fad…`
- `expression-reference-current` — scanned-live; 1 files/items; 0.5 MiB; SHA-256 `595088294c87fdaf…`

## Completeness rule

A corpus is reproducibly scanned only when its source/provenance, item count, byte count, aggregate digest and parser are recorded. `missing-or-empty` and `fetch-failed` remain explicit gaps.
Binary export coverage means exported PE surface coverage for the installed build; it does not cover non-exported internal functions, dynamic registrations, stripped symbols, or semantic contracts.
Historical completeness is open-ended until original SDK/install artifacts for missing release eras are acquired and hashed.

See `datasets/aeig-corpus-coverage-manifest.csv` for full provenance and unresolved notes.
