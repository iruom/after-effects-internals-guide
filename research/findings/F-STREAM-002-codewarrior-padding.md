---
id: F-STREAM-002
status: confirmed-header
last_verified: 2026-09-14
---
# Historical `AEGP_StreamValue` compiler-padding ABI incident

## Observation
`AE_GeneralPlugOld.h` contains an explicit workaround for CodeWarrior 7.1 adding four padding bytes after `AEGP_StreamRefH` in `AEGP_StreamValue`. Adobe forces a historical alignment mode because plug-ins were already built against the previous binary structure.

## Confidence
High for the ABI incident; direct distributed-header evidence.

## Architectural meaning
AE's plug-in compatibility surface is sensitive to compiler packing and historical struct layout. Field-equivalent C/C++ declarations are not sufficient to reconstruct historical binary semantics.

## Developer consequence
Do not persist native SDK structs. Define explicit portable serialization and validate `sizeof`, alignment and offsets when targeting historical SDK binaries.