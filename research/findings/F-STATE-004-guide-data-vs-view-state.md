---
status: confirmed-public
last_verified: 2026-09-15
evidence: E0-G 26.5
---
# F-STATE-004 — Guide document state and guide view state are separate

The 26.5 AEGP Guide Suite reads/writes guides attached to an Item or Layer: orientation, position, position type, per-guide color, and edge pinning.

Guide display controls are exposed separately through Item View Suite: visible, snap, and locked.

## Architectural consequence
AE distinguishes persistent/semantic guide data from presentation state associated with a particular view. A guide is not merely a UI overlay object owned by the viewer.

## Broader use
This is a clean public example for AEIG's Product Shell model: document state, selection/editor state, and per-view state should not be collapsed into one 'UI state' bucket.
