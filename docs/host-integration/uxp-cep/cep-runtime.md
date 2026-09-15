---
status: active
last_verified: 2026-09-16
evidence: Adobe CEP 12/10/8 cookbooks + CC 2015 AEFT samples + installed AE CEP substrate
---
# CEP Runtime and Host Bridge

CEP is a multi-runtime bridge, not "JavaScript inside After Effects". A panel can involve browser/CEF JavaScript, CEP native APIs, optional Node.js context and a separate host application's ExtendScript engine.

## Execution contexts
Adobe's CEP documentation distinguishes at least:
- **Browser context** — HTML DOM and browser runtime;
- **native `cep` context** — CEP/native services exposed to the panel;
- **Node context** — optional, with separate- or mixed-context behavior depending on launch flags;
- **host application context** — ExtendScript/Application DOM entered through `CSInterface.evalScript()`.

The Application DOM is not directly available in the panel's browser engine, and the panel DOM is not directly available from ExtendScript. Treat the boundary as RPC/message passing, not shared memory.

## `evalScript` is a host-main-thread boundary
Adobe documents that script passed through `evalScript` and the manifest `ScriptPath` executes in the host application's ExtendScript engine on the host main thread. CEP events are also dispatched from the host main thread.

Long-running JSX therefore blocks more than one panel callback: it can prevent CEP event scheduling and compete with other host-main-thread work. Adobe explicitly recommends splitting interacting scripts into smaller calls so event dispatch gets scheduling opportunities.

For AE this aligns with the wider rule that UI/script mutation is not the same execution plane as render/evaluation work.

## Event plane
`CSInterface.addEventListener`, `dispatchEvent` and `removeEventListener` operate on CEP's event infrastructure. ExtendScript can dispatch CSXS events through the PlugPlug external-object bridge where the host integrates it. Vulcan is a separate Adobe-wide inter-application messaging plane.

Do not use CEP events as an implicit synchronization primitive for render state. Event arrival means a message crossed the extension/host infrastructure; it does not guarantee that a requested AE render/cache/update has reached any particular internal phase.

CEP 5 removed support for the older global CEP event behavior that used `scope="GLOBAL"`; inter-application communication should be treated as a versioned contract rather than assumed from legacy samples.

## API-version and host-version discipline
CEP JavaScript APIs evolve independently from the AE product version. Adobe provides `CSInterface.getCurrentApiVersion()` so an extension can determine the CEP API integrated by the current host. A panel that works in one Creative Cloud generation can fail in another even if the AE scripting call it eventually makes is unchanged.

AEIG therefore records at least three versions separately:
`AE version / CEP runtime version / extension manifest host range`.

The retained CC 2015 Panel SDK samples target `AEFT` 13.0-15.9 with CSXS 4.0, while current installed AE builds still expose CEP/PlugPlug/Vulcan substrate. That proves architectural continuity, not browser-engine or API identity across releases.

## Node.js is another trust/lifetime plane
When Node is enabled, file/network/process capabilities may exist in a different JavaScript context from the browser DOM. Mixed context can make the distinction less visible to application code, but the extension should still separate privileged Node work, UI state and host mutation conceptually.

## Developer failure model
Common CEP/AE failures are boundary mistakes rather than DOM mistakes:
- assuming browser JS can directly retain AE object identity;
- issuing one giant `evalScript` operation and freezing host/UI/event progress;
- using panel state as authoritative render state;
- relying on undocumented CEP/runtime globals from a different Creative Cloud generation;
- loading multiple JSX files into shared global namespace and accidentally overwriting definitions;
- assuming an event implies completion of the host operation that triggered it.

Prefer narrow command messages with explicit inputs/outputs. Return stable IDs or serialized values rather than pretending host objects survive as JavaScript references across the bridge. Namespace ExtendScript globals because later-loaded JSX definitions can overwrite earlier global definitions.

## CEP vs UXP boundary
AE shipping UXP runtime components or first-party UXP extensions does not make CEP and UXP interchangeable. CEP has a documented third-party AEFT route and an established `CSInterface -> ExtendScript` bridge. General third-party AE UXP discovery/Host DOM remains a separately version-scoped capability in AEIG.

## Evidence and cross-links
Primary external evidence: Adobe `CEP 12 HTML Extension Cookbook`, older CEP cookbooks and Adobe CEP Getting Started resources. Local evidence: `datasets/ae-cc2015-panel-sdk-surface.csv`, `datasets/ae-2025-extension-substrates.csv`, and installed PlugPlug/Vulcan/CEP artifacts.

Related: `docs/capability-recipes/cep-vs-uxp-extension-plane.md`, `docs/host-integration/uxp-cep/uxp-after-effects-status.md`, scripting object-model pages, and the UI/main-thread boundary documentation.

## Unknown frontier
AEIG does not infer every CEP native hook or private AE panel service from the shared CEP runtime. First-party panels can use contracts unavailable to third-party extensions. Shared Adobe infrastructure is evidence of capability substrate, not proof of supported AE-specific API exposure.
