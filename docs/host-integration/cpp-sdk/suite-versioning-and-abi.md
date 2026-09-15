---
status: active
last_verified: 2026-09-15
---
# Suite Versioning and ABI

PICA suite names, C struct generation names, and the integer version passed to `AcquireSuite()` are separate identifiers.

A log such as `AcquireSuite("AEGP Comp Suite", 21)` does **not** imply a type named `AEGP_CompSuite21`.

## Concrete Comp Suite mapping from the AE 25.6 distribution

| Struct generation | PICA integer | Header annotation |
|---|---:|---|
| `AEGP_CompSuite1` | 4 | frozen AE 5.0 |
| `AEGP_CompSuite2` | 6 | frozen AE 5.5 |
| `AEGP_CompSuite3` | 7 | frozen AE 6.0 |
| `AEGP_CompSuite4` | 9 | frozen AE 6.5 |
| `AEGP_CompSuite5` | 11 | frozen AE 7.0 |
| `AEGP_CompSuite6` | 14 | frozen AE 8.0 |
| `AEGP_CompSuite7` | 15 | frozen AE 9.0 |
| `AEGP_CompSuite8` | 18 | frozen AE 10.5 |
| `AEGP_CompSuite9` | 19 | frozen AE 11 |
| `AEGP_CompSuite10` | 21 | frozen AE 12 |
| `AEGP_CompSuite11` | 25 | frozen AE 23.5 |
| `AEGP_CompSuite12` | 26 | frozen AE 24.0 |
## Prefix compatibility is not guaranteed
Mechanical comparison of historical function-pointer tables shows that many suite transitions reorder, insert or remove functions rather than merely append them.

Examples from the distributed old headers:
- `CompSuite9 → CompSuite10` is not prefix-compatible; the first mismatch occurs at function index 7.
- `ItemSuite2 → ItemSuite3` shrinks the table.
- `ItemSuite8 → ItemSuite9` also changes size/layout.
- later `LayerSuite5 → 6 → 7 → 8 → 9` transitions are prefix-compatible, but this cannot be generalized to all suites or eras.

Therefore a host emulator must dispatch by **requested suite name + requested PICA version** and return a layout compatible with that exact contract. Returning one modern-looking vtable for every version can redirect a plug-in's function index to the wrong callback.

## AexExecutor observation
Historical AexExecutor logs contain requests such as:
- `AEGP Comp Suite` integer 21 → public `AEGP_CompSuite10`;
- `AEGP Layer Suite` integer 12 → public `AEGP_LayerSuite6`;
- `AEGP Item Suite` integer 10 → public `AEGP_ItemSuite6`;
- `AEGP Comp Suite` integer 14 → public `AEGP_CompSuite6`.

These requests are evidence that real plug-ins may intentionally negotiate old stable ABIs on modern systems. They are not evidence of secret `Suite21`-style generations.

AexExecutor's dispatcher logged the requested integer but selected most implemented AEGP suites only by suite name. That design is an ABI-risk pattern and a candidate explanation for some historical instability, subject to crash/call-stack confirmation.

Machine-readable sources: `datasets/ae-sdk-25.6-suite-versions.csv` and `datasets/ae-sdk-25.6-suite-prefix-compat.csv`.

## Effect-side audit: numeric versions can reset and special-case layouts exist
The same rule is visible outside AEGP suites.

| Suite family | Published mapping / transition | Compatibility result |
|---|---|---|
| `PFAppSuite` | Suite4=PICA 6, Suite5=PICA 7, Suite6=PICA 1 | Suite4→5 is not prefix-compatible; the numeric version then resets to 1 |
| `PF_ParamUtilsSuite` | Suite1=PICA 2, Suite3=PICA 3 | not prefix-compatible; obsolete state APIs are replaced |
| `PF_PixelDataSuite` | v1=PICA 1, v2=PICA 2 | prefix-compatible; GPU accessor appended |
| `PF Iterate8 Suite` | v1=PICA 1, v2=PICA 2 | reviewed layouts are prefix-compatible |
| `PF Utility Suite` | current Premiere support family plus special v4 | Adobe explicitly requires a distinct v4 table because `GetClipName` was mis-versioned |

This means a numeric range such as `1..=N` is not a valid substitute for a version map. The integer is an ABI token scoped to the suite name, not an ordinal generation counter.

A useful negative control is PixelData/Iterate: some aliases really are safe. AEIG therefore records compatibility per transition rather than adopting either an always-compatible or never-compatible rule.
## Generated negotiation matrix
AEIG now materializes the name/version rule as `datasets/ae-suite-negotiation-matrix.csv`.

The current 25.6 corpus yields 158 generation rows across 54 AEGP/PF suite families. Of mechanically comparable adjacent transitions, 26 are prefix-safe and 20 are prefix-unsafe; another 58 transitions remain intentionally `unknown` rather than assumed compatible.

The matrix also captures the `PFAppSuite` PICA reset from 7 to 1. Consumers should therefore treat a PICA integer as an opaque ABI selector scoped to the suite name.

Static layout evidence does not replace runtime acquisition testing. Installed-host acceptance is tracked separately by the AE Observatory Plugin Host experiment.
