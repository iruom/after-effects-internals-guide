---
status: confirmed-local
last_verified: 2026-09-14
---
# F-MFR-002 — Adobe's Supervisor sample documents a live sequence-data/MFR conflict

AE 25.6 `Supervisor.cpp` explicitly says the effect is not marked thread-safe because it writes sequence data during `PF_Cmd_UPDATE_PARAMS_UI`, and that an existing issue prevents the pattern from working with Multi-Frame Rendering.

The same sample also writes `seqP->advanced_modeB` during `SmartRender` and comments that the value should be established during SequenceSetup but the sample author does not know how to do so.

This is direct evidence of architectural friction between UI-owned mutable instance state and concurrent render-side state. It is particularly valuable because it remains in a current distributed Adobe sample rather than only historical documentation.
