---
id: F-ABI-018
status: confirmed
evidence: local-adobe-sdk-distribution
last_verified: 2026-09-15
---
# SDK 25.6 Windows/macOS public header parity

## Finding
The retained After Effects 25.6 Windows and macOS SDK distributions expose the same public `Examples/Headers` source surface after packaging artifacts are normalized.

The macOS archive initially appeared to contain twice as many headers because it carries AppleDouble `._*.h` metadata entries. Excluding those entries leaves 68 meaningful headers, exactly matching Windows.

After UTF-8 BOM and newline normalization, all 68 corresponding headers are text-identical. A prefix-oriented identifier extraction also yields 4,104 identifiers on each platform with zero platform-only identifiers.

## Consequence
For this 25.6 distribution, public API inventory does not need separate Windows/macOS identifier branches. Platform behavior and binary/sample differences remain separate questions; this finding applies only to the distributed public header corpus.
