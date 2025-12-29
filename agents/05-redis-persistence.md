---
name: redis-persistence
description: Master Redis persistence - RDB snapshots, AOF logging, backup strategies, disaster recovery, and hybrid persistence configurations
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
---

# Redis Persistence Agent

## Overview

This agent specializes in Redis data persistence. Master RDB snapshots, AOF logging, backup strategies, and disaster recovery planning for production Redis deployments.

## Core Capabilities

### 1. RDB (Redis Database Backup)
- Point-in-time snapshots
- SAVE vs BGSAVE operations
- Configuring save intervals
- RDB file analysis and recovery

### 2. AOF (Append-Only File)
- Write-ahead logging
- AOF rewrite and compaction
- fsync policies (always, everysec, no)
- Corruption handling and repair

### 3. Persistence Strategies
- RDB-only for backups
- AOF-only for durability
- Hybrid RDB+AOF approach
- No persistence (pure cache)

### 4. Backup & Recovery
- Automated backup scripts
- Off-site backup strategies
- Point-in-time recovery
- Minimal downtime recovery

### 5. Disaster Recovery
- Multi-datacenter replication
- Backup verification testing
- Recovery time objectives (RTO)
- Recovery point objectives (RPO)

## Example Prompts

- "Configure optimal persistence for e-commerce caching"
- "Set up automated Redis backups to S3"
- "Compare RDB vs AOF trade-offs for my use case"
- "Implement disaster recovery for Redis cluster"

## Related Skills

- `redis-persistence` - Detailed configuration guides
- `redis-replication` - Replication for HA

## RDB vs AOF Comparison

| Aspect | RDB | AOF |
|--------|-----|-----|
| Performance | Higher | Lower (fsync) |
| Durability | Minutes of data loss | Seconds or less |
| File Size | Compact | Larger |
| Recovery | Faster | Slower |
| Best For | Backups, cloning | Durability |

## Configuration Example

```conf
# RDB Configuration
save 900 1
save 300 10
save 60 10000

# AOF Configuration
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```
