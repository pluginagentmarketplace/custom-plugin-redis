---
name: redis-persistence
description: Master Redis persistence - RDB snapshots, AOF logging, hybrid persistence, backup strategies, and disaster recovery
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true

# Production Configuration
version: "2.1.0"
redis_versions: ["6.2", "7.0", "7.2", "7.4"]
last_updated: "2025-01"

# Input/Output Schema
input_schema:
  type: object
  properties:
    persistence_mode:
      type: string
      enum: [rdb_only, aof_only, hybrid, none]
    durability_requirement:
      type: string
      enum: [best_effort, fsync_every_second, fsync_always]
    recovery_point_objective:
      type: string
      description: Maximum acceptable data loss window
    storage_type:
      type: string
      enum: [ssd, hdd, nvme, network]

output_schema:
  type: object
  properties:
    recommended_config:
      type: object
    estimated_recovery_time:
      type: string
    backup_commands:
      type: array
    warnings:
      type: array

# Error Handling
error_handling:
  retry_on:
    - BGSAVE_IN_PROGRESS
    - disk_full
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 5000
  persistence_errors:
    BGSAVE_ERR:
      description: Background save failed
      recovery: Check disk space, permissions
    AOF_REWRITE_ERR:
      description: AOF rewrite failed
      recovery: Check disk, memory, run BGREWRITEAOF

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-persistence, redis-replication]
  tools: [Bash, Read, Write]
---

# Redis Persistence Agent

## Overview

Production-grade agent for Redis persistence mastery. Expert guidance on RDB snapshots, AOF logging, hybrid persistence, backup automation, and disaster recovery procedures.

## Persistence Strategy Selection

```
┌─────────────────────────────────────────────────────────────────────┐
│                  PERSISTENCE DECISION TREE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  What's your durability requirement?                                │
│  │                                                                  │
│  ├── Can lose minutes of data ──────────> RDB only                  │
│  │   └── Fastest restarts, smallest files                          │
│  │                                                                  │
│  ├── Can lose ~1 second ────────────────> AOF (everysec)            │
│  │   └── Good balance of safety/performance                        │
│  │                                                                  │
│  ├── Cannot lose any data ──────────────> AOF (always) + replicas  │
│  │   └── ⚠️ Performance impact                                      │
│  │                                                                  │
│  └── Best of both ──────────────────────> Hybrid (RDB + AOF)        │
│      └── ✅ Recommended for production                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Comparison Matrix

| Feature | RDB | AOF | Hybrid |
|---------|-----|-----|--------|
| Data loss window | Minutes | Seconds | Seconds |
| File size | Compact | Large | Medium |
| Restart speed | Fast | Slower | Fast |
| Write performance | High | Medium | High |
| Disk I/O | Spikes | Continuous | Balanced |
| Corruption recovery | Limited | Better | Best |
| Redis 7.0+ default | ❌ | ❌ | ✅ |

## RDB (Snapshotting)

### Configuration
```bash
# redis.conf - RDB settings
save 900 1        # Save if 1+ key changed in 15 min
save 300 10       # Save if 10+ keys changed in 5 min
save 60 10000     # Save if 10K+ keys changed in 1 min

dbfilename dump.rdb
dir /var/lib/redis

# Compression (recommended)
rdbcompression yes
rdbchecksum yes

# Stop writes on error
stop-writes-on-bgsave-error yes
```

### Manual Operations
```bash
# Trigger background save
redis-cli BGSAVE

# Check status
redis-cli LASTSAVE                    # Unix timestamp
redis-cli INFO persistence | grep rdb

# Blocking save (for shutdown)
redis-cli SAVE                        # ⚠️ Blocks Redis

# Disable/enable
redis-cli CONFIG SET save ""          # Disable
redis-cli CONFIG SET save "900 1 300 10"  # Re-enable
```

### RDB Best Practices

| Scenario | Configuration | Reason |
|----------|---------------|--------|
| Cache only | Disable (`save ""`) | No durability needed |
| Standard | `save 900 1 300 10` | Balanced |
| Write-heavy | `save 60 1000` | More frequent |
| Large dataset | `save 1800 1` | Reduce I/O spikes |

## AOF (Append-Only File)

### Configuration
```bash
# redis.conf - AOF settings
appendonly yes
appendfilename "appendonly.aof"

# Sync policy
appendfsync everysec     # ✅ Recommended (1 sec max loss)
# appendfsync always     # Every write (slow!)
# appendfsync no         # OS decides (fast, risky)

# Rewrite triggers
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Redis 7.0+ Multi-part AOF
aof-use-rdb-preamble yes
```

### AOF Sync Policies

| Policy | Durability | Performance | Use Case |
|--------|------------|-------------|----------|
| always | Best | Slowest | Financial |
| everysec | Good | Good | Default |
| no | Risk | Fastest | Dev/test |

### Manual Operations
```bash
# Trigger rewrite
redis-cli BGREWRITEAOF

# Check status
redis-cli INFO persistence | grep aof

# Fix corrupted AOF
redis-check-aof --fix appendonly.aof
```

## Hybrid Persistence (Redis 7.0+)

### Configuration
```bash
# Enable both RDB and AOF with RDB preamble
appendonly yes
aof-use-rdb-preamble yes

# Multi-part AOF directory (Redis 7.0+)
appenddirname "appendonlydir"
```

### How It Works
```
┌─────────────────────────────────────────────────────────────────────┐
│                    HYBRID PERSISTENCE FLOW                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Normal Operation:                                               │
│     Commands ──> AOF buffer ──> fsync (every second) ──> AOF file   │
│                                                                     │
│  2. BGREWRITEAOF:                                                   │
│     ┌──────────────────┐     ┌─────────────────────┐                │
│     │ RDB Snapshot     │  +  │ Incremental AOF     │                │
│     │ (compact)        │     │ (since snapshot)    │                │
│     └──────────────────┘     └─────────────────────┘                │
│                  ↓                                                  │
│     Combined file = Fast load + Minimal data loss                   │
│                                                                     │
│  3. Recovery:                                                       │
│     Load RDB preamble (fast) ──> Replay AOF commands ──> Ready      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Backup Strategies

### Automated Backup Script
```bash
#!/bin/bash
# backup-redis.sh

BACKUP_DIR="/backups/redis"
DATE=$(date +%Y%m%d_%H%M%S)
REDIS_DIR="/var/lib/redis"

# Trigger save
redis-cli BGSAVE

# Wait for completion
while [ $(redis-cli LASTSAVE) == $(cat /tmp/last_save 2>/dev/null) ]; do
    sleep 1
done
redis-cli LASTSAVE > /tmp/last_save

# Copy files
cp ${REDIS_DIR}/dump.rdb ${BACKUP_DIR}/dump_${DATE}.rdb
if [ -d "${REDIS_DIR}/appendonlydir" ]; then
    tar -czf ${BACKUP_DIR}/aof_${DATE}.tar.gz ${REDIS_DIR}/appendonlydir
fi

# Cleanup old backups (keep 7 days)
find ${BACKUP_DIR} -type f -mtime +7 -delete

echo "Backup completed: ${BACKUP_DIR}/dump_${DATE}.rdb"
```

### Backup Best Practices

| Practice | Implementation |
|----------|----------------|
| Regular backups | Cron job every hour |
| Off-site copy | S3, GCS, or remote server |
| Retention policy | 7 days hot, 30 days cold |
| Verification | Monthly restore tests |
| Encryption | GPG or age for sensitive data |

## Disaster Recovery

### Recovery Procedure
```bash
# 1. Stop Redis
systemctl stop redis-server

# 2. Backup current (possibly corrupted) data
mv /var/lib/redis /var/lib/redis.corrupted

# 3. Restore from backup
mkdir /var/lib/redis
cp /backups/redis/dump_latest.rdb /var/lib/redis/dump.rdb

# For AOF restore
tar -xzf /backups/redis/aof_latest.tar.gz -C /var/lib/redis

# 4. Fix permissions
chown -R redis:redis /var/lib/redis

# 5. Start Redis
systemctl start redis-server

# 6. Verify
redis-cli DBSIZE
redis-cli INFO persistence
```

## Related Skills

- `redis-persistence` - Detailed persistence patterns (PRIMARY_BOND)
- `redis-replication` - HA with persistence

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. BGSAVE Failed
```
Can't save in background: fork: Cannot allocate memory
```

**Diagnosis:**
```bash
redis-cli INFO persistence | grep rdb_last_bgsave_status
cat /var/log/redis/redis-server.log | grep -i "bgsave"
```

**Causes & Fixes:**
| Cause | Fix |
|-------|-----|
| Not enough memory | Enable overcommit: `vm.overcommit_memory=1` |
| Large dataset | Schedule during low traffic |
| Swap disabled | Add swap or increase RAM |

```bash
# Enable memory overcommit (Linux)
echo 1 > /proc/sys/vm/overcommit_memory
# Or permanently in /etc/sysctl.conf
vm.overcommit_memory = 1
```

#### 2. AOF Corruption
```
Bad file format reading the append only file
```

**Fix:**
```bash
# Check and fix AOF
redis-check-aof --fix /var/lib/redis/appendonly.aof

# For Redis 7.0+ multi-part AOF
redis-check-aof --fix /var/lib/redis/appendonlydir/appendonly.aof.1.incr.aof
```

#### 3. Slow Restart (Large AOF)
**Diagnosis:**
```bash
ls -lh /var/lib/redis/appendonly.aof
redis-cli INFO persistence | grep aof_current_size
```

**Fixes:**
```bash
# Trigger rewrite
redis-cli BGREWRITEAOF

# Enable RDB preamble
redis-cli CONFIG SET aof-use-rdb-preamble yes
redis-cli BGREWRITEAOF
```

#### 4. Disk Full During Save
```
Short write while saving RDB
```

**Prevention:**
```bash
# Monitor disk space
df -h /var/lib/redis

# Alert threshold: 80% used
```

**Recovery:**
```bash
# Clear space
rm /var/lib/redis/temp-*.rdb  # Remove incomplete saves
# Or expand disk
```

### Debug Checklist

```markdown
□ Disk space > 20% free?
□ Memory overcommit enabled?
□ Correct file permissions (redis:redis)?
□ Save/AOF settings applied?
□ Backup verification passing?
□ Recovery tested recently?
□ Monitoring alerts configured?
```

### Recovery Time Estimates

| Data Size | RDB Load | AOF (No Preamble) | Hybrid |
|-----------|----------|-------------------|--------|
| 1 GB | ~10s | ~30s | ~12s |
| 10 GB | ~100s | ~300s | ~120s |
| 100 GB | ~15min | ~50min | ~18min |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E401 | BGSAVE_ERR | Background save failed | Check memory/disk |
| E402 | AOF_CORRUPT | AOF file corrupted | redis-check-aof --fix |
| E403 | DISK_FULL | No space for save | Free disk space |
| E404 | FORK_FAILED | Cannot fork for save | Enable overcommit |
| E405 | PERMISSION | Cannot write to dir | Fix ownership |

---

## Production Configuration Template

```bash
# /etc/redis/redis.conf - Production Persistence

# === Hybrid Persistence (Recommended) ===
appendonly yes
appendfilename "appendonly.aof"
appenddirname "appendonlydir"
appendfsync everysec
aof-use-rdb-preamble yes

# AOF rewrite settings
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-rewrite-incremental-fsync yes

# RDB as backup
save 900 1
save 300 10
save 60 10000
dbfilename dump.rdb

# Directory
dir /var/lib/redis

# Safety
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes

# Performance
no-appendfsync-on-rewrite no
aof-load-truncated yes
```
