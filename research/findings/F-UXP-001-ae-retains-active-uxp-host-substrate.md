---
status: strongly-supported-local-runtime
last_verified: 2026-09-15
evidence:
  - installed AE 2025 UXP manifest
  - AE Debug/Trace lineage 23.4-26.3
  - AfterFXLib -> dvauxphost imports
  - dvauxphost/dvauxpui export surface
---
# F-UXP-001 — Modern AE retains an active UXP host substrate even though current public UXP host positioning differs

The installed AE 2025 tree contains `UXP/plugins/com.adobe.ccx.start/manifest.json`. That Adobe-shipped Home Screen manifest explicitly includes host `aftereffects` with minimum version `22.5.0`.

AE stable Debug/Trace profiles from 23.4 through 26.3 retain `AEScripting.UXPAsMainInstance`, `dvauxphost.*`, `uxp`, and later `uxp.manifest` instrumentation.
## Active AE-side bridge
`AfterFXLib.dll` directly imports UXP-host functions including `LoadExtensionById`, `CreateHostView`, `AttachHostView`, `SendEventToJS`, and `SetClientHostAPIObject` from `dvauxphost.dll`. AfterFXLib also exports AE-side UXP Home Screen hooks such as `SetShowUXPHomeScreenFunction`, `SetHideUXPHomeScreenFunction`, and `SetIsUXPHomeScreenVisibleFunction`.

This is stronger than merely finding shared UXP DLLs beside AE: the AE host binary is linked to extension loading, host-view creation, JS event delivery, and client-host API bridging.

## Public-history versus current support
Older Adobe UXP integration documentation listed After Effects 22.x/23.0 as an integrated UXP host. Current UXP Hub host positioning no longer foregrounds After Effects in the same way. At the same time, modern AE continues to ship an Adobe first-party UXP extension targeting `aftereffects` and an active native UXP bridge.

The strongest justified conclusion is therefore three-layered:
1. **Platform/runtime:** confirmed present and actively connected in modern AE.
2. **Adobe first-party AE UXP use:** confirmed by the shipped Home Screen manifest and AE-side imports.
3. **Current third-party AE Host DOM/API support:** not established by the above evidence and must not be inferred from shared `dvauxphost` exports.

## Third-party-loader clue
`dvauxphost.dll` exposes shared infrastructure including `GetUXP3pDescriptors`, developer-plugin approval callbacks, descriptor scans, plugin lifecycle callbacks, panel/modeless/dialog view types, and host API registration. Because this DLL is shared Adobe infrastructure, those symbols are candidates rather than proof that AE enables every third-party path.

## Experiment
Use a disposable AE profile and a minimal no-host-DOM UXP descriptor to test discovery only. Capture `uxp`, `uxp.manifest`, and `dvauxphost` traces, descriptor scan results, and whether AE exposes a developer-extension loading path. Do not call undocumented native exports during the discovery experiment. A separate experiment can then test which JavaScript host namespaces, if any, are actually registered for third-party AE extensions.
