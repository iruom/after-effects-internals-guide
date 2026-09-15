---
status: confirmed-symptom / causal-model-hypothesis
last_verified: 2026-09-15
evidence: E0-G + E0-Historical
---
# F-3D-002 — Modern Advanced 3D still exposes a 3D-bin state boundary

Adobe's 26.2 fixed-issues notes state that Essential Property values are no longer shared across precomps in the same 3D bin when Advanced 3D is used with Collapse Transformations.

This is unusually strong modern evidence for a `3D bin` concept. Historical Canvas/Artisan APIs independently expose `AEGP_BinType_2D` and `AEGP_BinType_3D` plus bin iteration functions.

## Confirmed implication
A modern Advanced 3D render path groups work into a domain Adobe itself calls a 3D bin, and state isolation between collapsed precomp instances has previously failed within that domain.

## Causal hypothesis
The bug is consistent with an identity/context key that distinguished the bin but insufficiently distinguished precomp instance or Essential Property override state. This is not yet proven.

## Experiment
Create two instances of one precomp in a single Advanced 3D bin, apply distinct Essential Property overrides, toggle Collapse Transformations, reorder coplanar layers, and compare AE 26.1/26.2+ if available. Record BEE/RG traces and cache reuse where possible.
