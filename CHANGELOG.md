# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-29

### Added
- Complete rewrite with roadmap.sh inspiration
- 8 specialized Redis agents (SASMP v1.3.0 compliant)
- 12 Golden Format skills with real content:
  - redis-installation (Docker, Linux, macOS)
  - redis-strings (caching, counters)
  - redis-lists-sets (queues, unique collections)
  - redis-hashes-sorted-sets (objects, leaderboards)
  - redis-advanced-types (Bitmaps, HyperLogLog, Streams, Geo)
  - redis-transactions (MULTI/EXEC, Lua scripting)
  - redis-persistence (RDB, AOF, backup)
  - redis-replication (Sentinel, master-replica)
  - redis-cluster (hash slots, resharding)
  - redis-security (ACL, TLS, hardening)
  - redis-performance (memory, slow log, benchmarking)
  - redis-modules (RedisJSON, Search, TimeSeries, Bloom)
- 4 interactive commands:
  - /redis-check - Health check
  - /redis-benchmark - Performance testing
  - /redis-config - Config generator
  - /redis-debug - Issue diagnosis
- Real scripts (Python, Bash)
- Real configuration templates
- Complete documentation

### Changed
- Moved from generic "Developer Roadmap" to Redis-specific plugin
- Restructured to template v2.1.0 compliance
- Moved agents/skills/commands from .claude-plugin/ to root

### Fixed
- E003: Components in wrong directory
- E501: Missing SASMP fields
- E701-704: Missing Golden Format content

### Removed
- All generic developer roadmap content
- Frontend, backend, blockchain agents (not Redis-related)
- Generic skills (frontend-basics, machine-learning, etc.)

## [1.0.0] - 2025-12-28

### Added
- Initial release (generic Developer Roadmap - REPLACED)
