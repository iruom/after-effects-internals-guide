---
status: researched-seed
evidence_grade: E0
confidence: 0.99
versions: "SmartFX contract; historical and current SDK docs"
last_verified: 2026-09-14
---
# SmartFX content-bounds invariant

## Statement
SmartFX exposes a strong graph invariant: a node's content bounds are the largest possible result rectangle and must not depend on the current render request. Adobe explicitly warns that violating this invariant can break multiple parts of the host.

`request_rect`, `result_rect`, and `max_result_rect` therefore encode different concepts. AE may issue an empty request solely to compute `max_result_rect`, and it may skip Smart Render entirely after Pre-Render if downstream bounds prove the output unnecessary.

## Implementation hole
A plug-in that overestimates bounds remains correct but wastes cache memory and work. An underestimate is semantically incorrect because AE will never ask for pixels outside the declared maximum.

## Mathematical interpretation
Bounds form a conservative abstract domain over image support. Effects implement transfer functions over regions; correctness requires a superset of all potentially non-zero output support.

## Improvement direction
Use formal region algebra with explicit finite, transformed, unknown and infinite-support states. For infinite kernels, define a tail/error policy rather than silently choosing an oversized finite rectangle.

## Source
After Effects C++ SDK Guide, SmartFX: https://ae-plugins.docsforadobe.dev/smartfx/smartfx/
