---
status: active
last_verified: 2026-09-15
evidence: full AE 2025 PE inventory + import/export archaeology
---
# Module Inventory

AEIG maintains a full installed-runtime module inventory rather than sampling a few interesting DLLs.

The AE 2025 Support Files corpus scan covered 1,111 PE modules and produced 567,585 export rows with scanner failure 0. A higher-signal internal subset keeps BEE/TDB/RG/PF/AEGP/AEIO/AGM/TXT/OM/GPU/media-related surfaces separate from third-party library noise.

Examples of subsystem-bearing modules include `BEE.dll`, `TDB.dll`, `RG.dll`, `PF.dll`, `MediaFoundation.dll`, `VideoFrame.dll`, `GPUFoundation.dll`, `ColorSpaceConverter.dll`, `TXT.dll`, `AGM.dll`, `dvacore.dll` and extension-host modules.

## Interpretation rule
A module name is evidence of a deployable boundary, not proof that the module exclusively owns the named feature. Import edges, exported types, trace activity and controlled feature toggles provide stronger attribution.

## Version rule
The corpus manifest hashes the installed binaries. Comparisons across AE releases must use binary identity, not merely repeated filenames.

Primary datasets:
- `ae-2025-runtime-export-atlas.csv`
- `ae-2025-runtime-internal-surface.csv`
- domain-specific symbol inventories under `datasets/`.

Use module observations to discover boundaries; use public contracts and experiments to assign semantics.## Controlled attribution experiments
A module inventory becomes stronger when paired with feature toggles. Capture process modules before/after enabling one renderer, importer, extension plane or analysis feature; then repeat in a fresh host and compare binary hashes rather than filenames alone.

For a suspected owner, add import/export adjacency and runtime trace evidence. If disabling the feature removes neither the module nor the relevant calls, module presence alone was not discriminating evidence.

## Unknowns and failure modes
Delay-loaded modules, shared Adobe infrastructure and helper processes can make ownership appear broader or narrower than it is. A module can remain resident after a feature stops using it, and code can be statically linked or hidden behind a common substrate.

PE export names can also reflect ABI/compiler artifacts rather than semantic entry points. Never promote an exported C++ symbol into a supported API unless it is independently documented.

Cross-links: `process-tracing.md`, `logging.md`, `../architecture/subsystem-boundaries.md`, and `../reference/corpus-coverage-status.md`.
## Remaining unknowns
The inventory cannot by itself resolve runtime ownership for delay-loaded code, static libraries, shared helper processes or modules that stay resident after feature use. Those cases require process tracing, import adjacency, feature toggles or stacks.

Related: `docs/observability/process-tracing.md`, `docs/observability/logging.md`, `docs/architecture/subsystem-boundaries.md`, `docs/reference/corpus-coverage-status.md`.
