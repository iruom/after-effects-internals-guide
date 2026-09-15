---
status: confirmed-local
last_verified: 2026-09-14
---
# F-SEQUENCE-002 — Sequence flatten and flattened snapshot are semantically different operations

`PathMaster` implements `PF_Cmd_SEQUENCE_FLATTEN` by serializing the live state and then deleting/discarding the unflattened representation.

Its `PF_Cmd_GET_FLATTENED_SEQUENCE_DATA` implementation deliberately creates the same portable form without destroying the live representation; Adobe comments that preserving the unflattened data is the whole point.

This distinction is critical for UI/render-project synchronization introduced by the post-13.5 architecture. Treating both selectors as interchangeable can destroy live UI state during synchronization.
