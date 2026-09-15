---
status: confirmed-symptom / implementation-link-inference
last_verified: 2026-09-15
evidence: E0-G 26.5 fixed issue
---
# F-AI-002 — Object Matte leaked internal stream-flag mutations into Undo history

Adobe's 26.5 fixed issues state that Object Matte no longer adds spurious `Set Stream Flags` steps to the undo history.

## Confirmed implication
An Object Matte workflow crossed an internal project-stream mutation boundary that participates in Undo. The leaked command name directly identifies stream flags as part of the affected path.

## Caution
The issue does not prove which specific stream flags Object Matte changes, nor whether the mutation is essential to propagation or incidental UI bookkeeping.

## Research value
Compare Object Matte selection/freeze operations with Dynamic Stream flag APIs, undo group boundaries, and AEP property-tree mutations. This is a useful bridge between a modern AI feature and AE's old Stream/Property state system.
