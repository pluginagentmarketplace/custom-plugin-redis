---
name: redis-persistence
description: Master Redis persistence - RDB snapshots, AOF logging, backup strategies, and disaster recovery planning
sasmp_version: "1.3.0"
bonded_agent: redis-persistence
bond_type: PRIMARY_BOND
---

# Redis Persistence Skill

## RDB (Snapshotting)

Point-in-time snapshots of the dataset.

```conf
# redis.conf
save 900 1      # Save after 900s if 1 key changed
save 300 10     # Save after 300s if 10 keys changed
save 60 10000   # Save after 60s if 10000 keys changed

dbfilename dump.rdb
dir /var/lib/redis
```

### Manual Snapshots
```redis
SAVE      # Blocking (avoid in production)
BGSAVE    # Background save
LASTSAVE  # Last successful save timestamp
```

## AOF (Append-Only File)

Write-ahead log for durability.

```conf
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec  # always | everysec | no

# Rewrite settings
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

### AOF Commands
```redis
BGREWRITEAOF  # Compact AOF file
```

## Hybrid Persistence (Redis 4.0+)

```conf
aof-use-rdb-preamble yes
```

## Assets
- `backup-redis.sh` - Automated backup script
- `persistence-config.conf` - Optimized config

## References
- `PERSISTENCE_GUIDE.md` - Strategy guide
