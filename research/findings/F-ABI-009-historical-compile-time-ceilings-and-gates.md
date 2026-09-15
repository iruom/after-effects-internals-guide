---
status: confirmed-cross-version-header-differential
last_verified: 2026-09-15
evidence:
  - CS6 header archive (third-party provenance recorded)
  - distributed AE 25.6 headers
---
# F-ABI-009 — Removed identifiers often encode API evolution rather than lost capability

After fixing the Atlas to compare exact identifier tokens, the CS6 corpus has six identifiers absent from the raw 25.6 corpus: `PF_ANSICallbacks`, `PF_App_Color_TLW_NEEDLE`, `PF_ENABLE_PS12_MODES`, `PF_ExtendedSuiteTool_CAMERA_ORBIT`, `PF_MAX_THREADS`, and `PF_RenderOutputFlag_RESERVED`.

None of the examined cases justifies the blanket conclusion "capability removed".

## Lifted ceiling: PF_MAX_THREADS
CS6 defines `PF_MAX_THREADS` as 32. Current `AE_Effect.h` explicitly records the AE 23.4 API change as allowing more than 32 maximum threads for PF Iterate. The vanished constant represents a lifted historical ceiling.

## Gate removal: PF_ENABLE_PS12_MODES
CS6 conditionally exposes `PF_Xfer_SUBTRACT` and `PF_Xfer_DIVIDE` behind this macro. In 25.6 the gate is gone and both modes are unconditional.

## UI semantic split: PF_App_Color_TLW_NEEDLE
The CS6 timeline needle color becomes separate `PF_App_Color_TLW_NEEDLE_CURRENT_TIME` and `PF_App_Color_TLW_NEEDLE_PREVIEW_TIME` entries in 25.6. One old UI role became two independently addressable roles.
## Tool rename/restructure: PF_ExtendedSuiteTool_CAMERA_ORBIT
CS6 uses `PF_ExtendedSuiteTool_CAMERA_ORBIT`. In 25.6 the camera tool family is reorganized around names including `PF_ExtendedSuiteTool_CAMERA_ORBIT_CAMERA`, `...PAN_CAMERA`, `...DOLLY_CAMERA`, and newer cursor/tool variants. Treat the old numeric position as historical ABI, not a stable semantic name.

## Reserved bit repurposing: PF_RenderOutputFlag_RESERVED
CS6 assigns bit `0x2` to `PF_RenderOutputFlag_RESERVED`. In 25.6 the same bit value is `PF_RenderOutputFlag_GPU_RENDER_POSSIBLE`; a new `RESERVED1` occupies `0x4`. This is a concrete example where preserving an old symbolic meaning against a modern host would be wrong even though the bit position is unchanged.

## Callback-container migration: PF_ANSICallbacks
CS6 exposes a `PF_ANSICallbacks` block. The modern headers use `PF_ANSICallbacksBlock` in the legacy callback block and `PF_ANSICallbacksSuite1` for the PICA suite. `AE_Effect.h` also records an AE 23.5 SDK transition referring to a new `PF_ANSICallbacksSuite2`, even though that exact Suite2 declaration is not present in the inspected 25.6 header corpus. This inconsistency remains a version/distribution archaeology target rather than a reason to synthesize an ABI.

## API-atlas rule
A disappearing symbol must be classified as one of: removed capability, rename/split, lifted limit, compile-time gate removal, reserved-slot repurpose, ABI folding, callback-container migration, or documentation/distribution drift. Preserve numeric values and version context separately from names.

## Developer consequence
Host reimplementations must key behavior by the requested SDK/host version rather than projecting modern names backwards. In particular, reserved values are not promises of permanent semantic emptiness; Adobe may assign them in a later ABI generation.
