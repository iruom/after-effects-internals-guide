---
status: active
last_verified: 2026-09-15
---
# Recipe: Escape Native Plug-in API Limits with the Extension Plane

## Goal
Build UI, automation or cross-application behavior that does not fit PF/AEGP render callbacks.

## Supported routes
Use ExtendScript for document/UI automation and CEP/CSXS for HTML-panel hosting plus scripting/event bridges. AE 2025 still ships `CEPManager.aex`, PlugPlug and Vulcan infrastructure, and AEFT-targeted CSXS manifests across several CSXS generations.

## Architectural separation
Treat the extension plane as a **control/UI plane**, not as a render-dependency plane. A mutation performed through ExtendScript/CEP can change the project, but that does not mean arbitrary CEP state is automatically registered as a PF render dependency.

## Cross-app messaging
CEP/PlugPlug/Vulcan provide messaging infrastructure for Adobe applications. Message namespaces, payload schemas and service lifetimes are feature-specific; internal Adobe messages are not automatically public contracts.

## UXP caution
AE 2025/26.x contains an active first-party UXP host substrate and Adobe-shipped AE-targeted UXP manifests. `AfterFXLib` imports extension loading/view/JS bridge functions. However, a current general third-party AE UXP DOM/discovery contract has not been established by AEIG.

Therefore:
- first-party UXP hosting: confirmed runtime capability;
- shared `dvauxphost` third-party scanner symbols: implementation evidence;
- generic third-party UXP for AE: **unknown-current-contract**, not a supported recipe yet.

## Design pattern
Keep render-critical algorithms in PF/AEGP/native code, document automation in scripting, and rich panels/service orchestration in the supported extension plane. Connect them with explicit project mutations or a documented IPC/command boundary.

Related: `F-EXT-001-cep-uxp-coexistence-and-host-scope`, `datasets/ae-2025-extension-substrates.csv`.

## Failure and threading boundaries
CEP panel JavaScript, Node-capable extension context and host ExtendScript are distinct execution domains. `evalScript`/host events cross into AE's host scripting/main-thread domain; long synchronous work there can block UI even if the panel itself remains responsive.

Project mutation must still obey AE's undo/state semantics. Extension-local state is not a render dependency until it is committed through supported project/native mechanisms, so hiding pixel-affecting configuration only inside a panel/service can create stale native caches.

First-party UXP runtime presence must not be used as a shortcut to undocumented third-party loading. Version/current-host support is a product contract question, not a DLL-discovery question.

## Experiment matrix
Build equivalent commands in ExtendScript and CEP→ExtendScript, measuring UI blocking, undo grouping, project mutation visibility and downstream render invalidation. For cross-app messaging, restart one application and test reconnection/duplicate message handling separately from project semantics.

A useful safety invariant is: automation may orchestrate supported state changes, but render-critical state must become visible through the host's supported dependency/persistence model before results are cached.

Related: `docs/host-integration/uxp-cep/cep-runtime.md`, `docs/host-integration/uxp-cep/uxp-after-effects-status.md`, `docs/ui-system/view-state-and-render-boundary.md`, `docs/threading-system/overview.md`.
