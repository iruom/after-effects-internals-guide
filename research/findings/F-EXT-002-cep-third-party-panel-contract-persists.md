---
id: F-EXT-002
status: confirmed-lineage
confidence: high
evidence: [E0-S, E1-L]
version_scope: "CC 2015 Panel SDK samples / AE 13.x contract through installed AE 2025 CEP substrate"
last_verified: 2026-09-15
---
# F-EXT-002 — The CEP third-party panel contract has a continuous AE lineage

The retained CC 2015 Panel SDK contains four CSXS manifests. All four target host `AEFT` version `[13.0,15.9]`, require CSXS 4.0, and declare `Panel` UI entries backed by HTML plus an ExtendScript `ScriptPath`.

The distributed `CSInterface-4.0.0.js` exposes the standard HTML/host bridge including `evalScript`, event add/remove/dispatch, host-environment/application lookup, system paths, extension opening, and browser URL launching.

Installed AE 2025 retains AEFT-targeted CSXS manifests across CSXS runtime generations 5, 6, 9 and 11, while `CEPManager.aex`/`csxsmanager.dll` import PlugPlug extension load/unload and event-dispatch surfaces. The installed Common Files corpus also contains third-party AEFT-targeted CEP manifests.

## Consequence
CEP should be modeled as a long-lived extension capability plane, not as a transient legacy UI technology that disappeared when UXP arrived. Exact Chromium/CEP implementation details are versioned, but the architectural route `HTML/JS panel -> CSInterface/PlugPlug -> ExtendScript/host` has clear continuity.

Machine evidence: `datasets/ae-cc2015-panel-sdk-surface.csv` and `datasets/ae-2025-extension-substrates.csv`.
