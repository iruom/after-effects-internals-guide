---
status: seed
evidence_grade: E2-L
versions: "CS6 and 2025 directly compared"
last_verified: 2026-09-14
---
# PresetEffects.xml exposes an internal pseudo-effect parameter schema

## Statement
Local PresetEffects.xml files explicitly describe pseudo effects and expose parameter types/attributes including Popup_UTF8, Point3D, INVISIBLE, CANNOT_TIME_VARY and external_id.

## Interpretation rule
Do not infer more than the evidence supports. Internal names are observation points, not automatically class or subsystem definitions.

## Next experiment
Diff all retained versions and correlate schema constructs with FFX serialization.
