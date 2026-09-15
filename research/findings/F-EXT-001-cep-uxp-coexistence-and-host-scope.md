---
status: active
evidence_grade: confirmed-local-runtime-plus-current-public-positioning
versions: "AE 2025 local; public docs checked 2026-09-15"
last_verified: 2026-09-15
---
# CEP and UXP coexist as distinct extension planes in modern After Effects

## Confirmed local CEP plane
The installed AE 2025 tree contains `CEPManager.aex`, `CEPHtmlEngine`, `csxsmanager.dll`, `PlugPlug.dll`, `PlugPlugExternalObject.dll`, `VulcanControl.dll`, and `VulcanMessage5.dll`.

AE-shipped CSXS manifests explicitly target `AEFT`. Examples include Learning Panel (`CSXS 11.0`, AEFT `[22,99.9]`), Libraries (`CSXS 5.0`, AEFT `[23.0,99.9]`), Frame.io (`CSXS 6.0`, AEFT `15.0`), and SUSI (`CSXS 6.0`, AEFT `[13.5,99.9]`).

`CEPManager.aex` contains/uses `GPMain_CEPManager`, `AE CEP Suite`, a CEP `ScriptingEngine`, PlugPlug extension load/unload/event APIs, and Vulcan messaging. This establishes an AE-specific bridge rather than merely shared CEP binaries beside the application.

## Confirmed local UXP plane
AE also ships and actively links a UXP host substrate. Adobe first-party UXP manifests target `aftereffects`, and `AfterFXLib.dll` imports extension loading, host-view creation, JS event, and host-API bridge functions from `dvauxphost.dll`.
## Third-party asymmetry
The shared UXP host DLL contains `GetUXP3pDescriptors`, `ThirdPartyHostAPI`, manifest scanning, developer-plugin approval callbacks and third-party flags. However, the AE-specific `AfterFXLib.dll` import set observed here does not directly import those third-party scanner functions; it imports the explicit extension-loading/host-view bridge instead.

Therefore:
- CEP third-party extension loading is an established AE extension plane.
- UXP first-party AE hosting is established.
- current general third-party AE UXP discovery remains unproven and must not be inferred from shared UXP infrastructure.

Current Adobe UXP host/version tables foreground Photoshop, InDesign and Premiere rather than After Effects, reinforcing the need to distinguish installed first-party runtime support from a current public third-party host contract.

## Architectural consequence for AEIG
Do not define "After Effects API" as only PF/AEGP. Model at least five capability planes: native PF/AEGP/AEIO, ExtendScript, CEP/CSXS, UXP, and cross-application Vulcan messaging. A task unavailable in one plane may be available in another, but threading, ownership, security and cache semantics do not transfer between planes.

## Reproducibility
`inventory_extension_substrates.py` currently records 724 manifest/import rows. `inventory_extension_loader_strings.py` records the loader vocabulary without mutating AE or user profiles.
