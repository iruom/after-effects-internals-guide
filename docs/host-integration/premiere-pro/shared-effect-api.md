---
status: active
last_verified: 2026-09-16
evidence: current AE SDK Premiere-host compatibility docs + shared PF/PICA headers + dual-host samples
---
# Premiere Pro as a Cross-Host Probe for the AE Effect API

Premiere Pro hosts a substantial subset of the After Effects Effect API. This makes Premiere unusually valuable for AE archaeology: the same plug-in binary/API family can run under a different renderer, scheduler, timebase, pixel-format policy and suite set.

The correct question is not “does Premiere behave like AE?” but:

`which behavior belongs to the portable PF effect contract, and which behavior is contributed by AE's host/runtime?`

## Shared surface
The shared plane includes core PF selector lifecycle, parameter definitions, `PF_InData`/`PF_OutData`, PiPL discovery, SPBasic/PICA suite acquisition and many effect utility calls.

Adobe samples such as SDK_ProcAmp/Vignette deliberately exercise cross-host software paths, making them useful controlled probes of the common contract.

## Host identity must be explicit
Premiere-hosted AE effects report Premiere application identity (`appl_id` / host-specific version behavior). Code that assumes product version from PF API version can therefore fail even while the ABI loads successfully.
## Render-pipeline differences are semantic
Adobe's compatibility documentation explicitly warns that underlying render pipelines differ. Consequences include different time values/time scales, render ordering and suite availability.

A plug-in must treat time as a ratio, not hard-code a host's `time_scale`. Historical examples show NTSC/PAL values represented differently by Premiere and AE while denoting equivalent times.

## Missing/alternate surfaces
The compatibility guide documents important host gaps/alternatives, including AEGP absence and missing/partial support for 3D/SmartFX/high-bit-depth-era features in the documented compatibility surface.

Some Effect API suites missing in Premiere have macro/utility equivalents. Portable code therefore needs capability detection rather than assuming suite acquisition succeeds because it succeeds in AE.

No AEGP calls should be assumed available in a Premiere-hosted AE effect. Premiere-specific `PrSDKAESupport` surfaces are a different contract, not an AEGP backdoor.

## Why mismatches are useful evidence
If the same PF plug-in behaves differently in two hosts, classify the divergence:
- host timebase/request scheduling;
- pixel-format/world semantics;
- unsupported flag/suite;
- render-order or extent behavior;
- AE-specific state/receipt/cache machinery;
- Premiere-specific GPU/media integration.

This can reveal where AE-specific architecture begins.
## Dual-host experiment pattern
For a portable sample/effect:
1. log host identity and PF API version;
2. enumerate/acquire each suite conditionally;
3. record time_scale/time_step/field/ROI/extent;
4. run identical numerical input across both hosts;
5. separate host-provided conversions from effect math;
6. compare selector ordering/thread overlap;
7. mark any result that depends on an AE-only capability.

## Failure modes
- using AE product version as if it were the PF ABI version;
- unconditionally acquiring AE-only suites;
- hard-coding time-scale constants;
- treating Premiere's support for the Effect API as proof of AE renderer behavior;
- importing Premiere-specific GPU or memory semantics back into AE without AE-side evidence;
- concluding an undocumented AE invariant from behavior that is actually common PF contract.

## Evidence rule
Premiere documentation is **cross-host evidence**, not direct evidence of AE internals. A behavior becomes an AE fact only when the shared substrate is established and AE-side documentation/runtime/experiment corroborates it.

Cross-links: `render-graph-analogs.md`, `threading-async.md`, `memory-management-analogs.md`, `../cpp-sdk/cross-host-semantics.md`, `../../foundations/cross-host-triangulation.md`.