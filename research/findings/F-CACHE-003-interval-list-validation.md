---
status: researched-seed
evidence_grade: E1/E2
confidence: 0.94
versions: "historical design evidence; current applicability unverified"
last_verified: 2026-09-14
---
# Interval-list cache validation architecture

## Statement
Adobe patent US7103839B1 describes a compositing-cache validity system using per-node **interval lists** keyed by edit sequence timestamps. The inventors, Michael J. Natkin and David P. Simons, are independently documented by Adobe as After Effects designers/developers.

The design is explicitly pull-oriented at validation time: an edit updates local interval information, while a cached-frame lookup recursively checks relevant intervals in descendant nodes. Cached-frame timestamps are compared with the newest edit timestamp intersecting the frame's temporal footprint.

## Important details
- A timestamp is an edit-order integer, not composition time.
- Multiple interval lists may exist per comp/layer for different classes of edits.
- Motion blur expands the queried time interval to the shutter-open range.
- Time stretch/remap and non-local-time effects are first-class concerns.
- The algorithm is conservative: false invalidation is acceptable; false validity is not.

## Caution
This patent is exceptionally relevant historical evidence, but it does not prove that AE 26.x still uses the same data structure.

## Sources
1. Adobe patent US7103839B1: https://patents.google.com/patent/US7103839B1
2. Adobe Sci-Tech Award note: https://blog.adobe.com/en/publish/2018/12/13/adobe-after-effects-cc-photoshop-cc-wins-sci-tech-academy-award
