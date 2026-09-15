---
status: researched-seed
evidence_grade: E1
confidence: 0.97
versions: "historical AE animation architecture"
last_verified: 2026-09-14
---
# Arc-length reparameterization of animation paths

## Statement
Adobe patent US6115051A explicitly names After Effects and describes decoupling a spatial path `Q(u)` from motion over time `S(t)` by reparameterizing the path with arc length.

The system approximates `s=A(u)` numerically, using sampled `(u,s)` pairs. One embodiment recursively subdivides the spline until arc distance between samples is below a threshold, then fits one or more differentiable Bezier curves to approximate `A` or its inverse.

Runtime evaluation becomes:
1. `s = S(t)` from the temporal motion graph;
2. `u = A^-1(s)` from the stored reparameterization;
3. `position = Q(u)`.

## Why it matters
This gives a mathematical ancestry for separating spatial interpolation from temporal velocity control. It also exposes an approximation strategy, error threshold and storage/performance tradeoff.

## Improvement direction
Modern implementations can use adaptive Gauss-Legendre integration, monotone cubic interpolation or table + Newton refinement. AEIG should measure current AE error/continuity against the historical algorithm rather than assuming it survived unchanged.

## Source
Adobe patent US6115051A: https://patents.google.com/patent/US6115051A/en
