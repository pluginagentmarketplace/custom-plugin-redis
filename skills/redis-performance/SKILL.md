---
name: redis-performance
description: Master Redis performance - memory optimization, slow log analysis, benchmarking, monitoring, and tuning strategies
sasmp_version: "1.3.0"
bonded_agent: redis-production
bond_type: PRIMARY_BOND
---

# Redis Performance Skill

## Memory Management

```conf
maxmemory 1gb
maxmemory-policy allkeys-lru
```

### Memory Policies
| Policy | Description |
|--------|-------------|
| noeviction | Return error on write |
| allkeys-lru | Evict LRU keys |
| volatile-lru | Evict LRU with TTL |
| allkeys-random | Random eviction |
| volatile-ttl | Evict by TTL |

## Slow Log

```redis
CONFIG SET slowlog-log-slower-than 10000  # 10ms
CONFIG SET slowlog-max-len 128

SLOWLOG GET 10
SLOWLOG LEN
SLOWLOG RESET
```

## Benchmarking

```bash
# Basic benchmark
redis-benchmark -q -n 100000

# Specific commands
redis-benchmark -t set,get -n 100000 -q

# With pipelining
redis-benchmark -t set -n 100000 -P 16 -q
```

## Memory Analysis

```redis
MEMORY DOCTOR
MEMORY STATS
MEMORY USAGE key
INFO memory
DEBUG OBJECT key
```

## Latency Monitoring

```redis
CONFIG SET latency-monitor-threshold 100
LATENCY DOCTOR
LATENCY HISTORY command
```

## Assets
- `performance-config.conf` - Optimized config
- `monitoring-queries.txt` - Key metrics

## References
- `PERFORMANCE_GUIDE.md` - Tuning guide
