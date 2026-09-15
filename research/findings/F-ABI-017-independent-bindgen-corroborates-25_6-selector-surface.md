---
id: F-ABI-017
status: strongly-supported
confidence: high
evidence: [E0-H, E1-X]
version_scope: "SDK 25.6 headers versus third-party after-effects-sys bindgen snapshot at commit 83dcc93734fd5db1335b6ec83cba7a6505a39dcc"
last_verified: 2026-09-15
---
# F-ABI-017 — Independent bindgen output corroborates the 25.6 selector/version surface

AEIG compared numeric PF API version macros and suite selector/version macros from the distributed 25.6 headers with `after-effects-sys/bindings_win.rs`.

- 310 distinct numeric selector/version names were inventoried across the two surfaces.
- 282 names exist in both.
- All 282/282 common names have exactly identical numeric values.
- No numeric mismatches were observed.
- Remaining one-sided names are primarily wrapper/allowlist or generated-current aliases rather than value conflicts.

The 25.6 `AE_Effect.h` history mentions `PF_ANSICallbacksSuite2` at the AE 23.5 API bump, but the distributed corpus does not define a corresponding Suite2 selector/table; the independent bindgen output likewise exposes Suite1 and no `PF_ANSICallbacksSuite2` symbol.

## Consequence
This binding is useful as independent corroboration of the distributed selector surface, but it is not an Adobe authority and must not replace the original headers or historical SDK corpora. It strengthens the classification of the ANSI Suite2 mention as a distribution/documentation inconsistency rather than evidence of a callable distributed Suite2 ABI.

Machine evidence: `datasets/ae-after-effects-sys-binding-corroboration.csv` and `docs/reference/binding-corroboration-status.md`.
