---
status: confirmed-local
last_verified: 2026-09-14
---
# F-CHANNEL-002 — AE has a generic typed auxiliary raster system beside RGBA worlds

The frozen AE 5.0 `PF_ChannelSuite1` exposes time-dependent per-layer channels by index/type. `PF_ChannelDesc` carries channel type, name, elementary data type and vector dimension; `PF_ChannelChunk` carries width, height, row bytes, dimension, host handle and locked pointer.

Known types include depth, normals, object ID, motion vectors, background color, texture, coverage, node, material, unclamped data and later anti-aliased depth.

This is not just a set of special structs. It is a generic typed raster side-channel architecture whose storage parallels an image world.
