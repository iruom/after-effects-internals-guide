---
status: generated
last_verified: 2026-09-16
---
# Roadmap Status

Domains meeting the AEIG 1.0 minimum: **24/27**.

## Current coverage distribution

- L2: 7 domains
- L3: 11 domains
- L4: 6 domains
- L5: 3 domains

## Largest gaps

| Domain | Current | Target | Gap | Next evidence |
|---|---:|---:|---:|---|
| cache | L4 | L5 | 1 | disk format and cache-key experiments |
| render-graph | L4 | L5 | 1 | RG node/runtime trace correlation |
| state-identity | L4 | L5 | 1 | GUID/receipt runtime probes |

This page is generated from `datasets/aeig-domain-coverage.csv` by `report_roadmap_progress.py`.
The target rule is intentionally conservative: core domains L5, other high/critical domains L3, all others L2.
