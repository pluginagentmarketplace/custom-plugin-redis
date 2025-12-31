---
name: redis-production
description: Master Redis production - monitoring, performance tuning, modules (RedisJSON, Search, TimeSeries), enterprise features, and operational excellence
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
skills:
  - redis-security
  - redis-persistence
  - redis-strings
  - redis-replication
  - redis-cluster
  - redis-performance
  - redis-hashes-sorted-sets
  - redis-lists-sets
  - redis-installation
  - redis-modules
  - redis-transactions
  - redis-advanced-types

triggers:
  - "redis redis"
  - "redis"
  - "cache"
# Production Configuration
version: "2.1.0"
redis_versions: ["6.2", "7.0", "7.2", "7.4"]
last_updated: "2025-01"

# Input/Output Schema
input_schema:
  type: object
  properties:
    operation_type:
      type: string
      enum: [monitoring, performance, modules, troubleshooting, capacity_planning]
    environment:
      type: string
      enum: [development, staging, production, enterprise]
    metrics_required:
      type: array
      items:
        type: string

output_schema:
  type: object
  properties:
    recommendations:
      type: array
    config_changes:
      type: object
    monitoring_queries:
      type: array
    alerts:
      type: array
    runbook:
      type: object

# Error Handling
error_handling:
  retry_on:
    - timeout
    - connection_lost
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 1000
  production_errors:
    OOM:
      description: Out of memory
      recovery: Eviction policy or scale
    LOADING:
      description: Dataset loading
      recovery: Wait for load completion

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-performance, redis-modules]
  tools: [Bash, Read, Write]
---

# Redis Production Agent

## Overview

Production-grade agent for Redis operational excellence. Expert guidance on monitoring, performance optimization, module integration, capacity planning, and enterprise operations.

## Production Readiness Checklist

```
┌─────────────────────────────────────────────────────────────────────┐
│                  PRODUCTION READINESS MATRIX                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  □ High Availability                                                │
│    ├── Replication configured                                       │
│    ├── Sentinel or Cluster deployed                                 │
│    └── Failover tested                                              │
│                                                                     │
│  □ Persistence                                                      │
│    ├── RDB + AOF enabled                                            │
│    ├── Backup automation                                            │
│    └── Restore procedure tested                                     │
│                                                                     │
│  □ Security                                                         │
│    ├── ACL configured                                               │
│    ├── TLS enabled                                                  │
│    └── Network restricted                                           │
│                                                                     │
│  □ Monitoring                                                       │
│    ├── Metrics collection                                           │
│    ├── Alerting configured                                          │
│    └── Dashboards ready                                             │
│                                                                     │
│  □ Capacity                                                         │
│    ├── Memory sized correctly                                       │
│    ├── maxmemory set                                                │
│    └── Eviction policy chosen                                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 1. Monitoring

### Essential Commands
```bash
# Server info
redis-cli INFO                    # All sections
redis-cli INFO server             # Version, uptime
redis-cli INFO clients            # Connected clients
redis-cli INFO memory             # Memory usage
redis-cli INFO stats              # Operations stats
redis-cli INFO replication        # Replication status
redis-cli INFO cluster            # Cluster info

# Real-time monitoring
redis-cli MONITOR                 # ⚠️ Performance impact!
redis-cli CLIENT LIST             # Connected clients
redis-cli SLOWLOG GET 25          # Slow queries
redis-cli LATENCY DOCTOR          # Latency analysis
```

### Key Metrics Dashboard

| Metric | Command | Healthy | Warning | Critical |
|--------|---------|---------|---------|----------|
| Memory | `INFO memory` | <75% | 75-90% | >90% |
| CPU | `INFO cpu` | <70% | 70-85% | >85% |
| Connections | `INFO clients` | <80% max | 80-95% | >95% |
| Hit Rate | `INFO stats` | >95% | 90-95% | <90% |
| Replication Lag | `INFO replication` | <1s | 1-10s | >10s |
| Ops/sec | `INFO stats` | baseline | +50% | +100% |

### Prometheus Integration
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']  # redis_exporter

# Key metrics to alert on
- redis_connected_clients
- redis_memory_used_bytes
- redis_memory_max_bytes
- redis_keyspace_hits_total
- redis_keyspace_misses_total
- redis_commands_processed_total
- redis_connected_slaves
- redis_master_repl_offset
```

### Alerting Rules
```yaml
# prometheus/alerts.yml
groups:
- name: redis
  rules:
  - alert: RedisDown
    expr: redis_up == 0
    for: 1m
    labels:
      severity: critical

  - alert: RedisMemoryHigh
    expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
    for: 5m
    labels:
      severity: warning

  - alert: RedisReplicationBroken
    expr: redis_connected_slaves < 1
    for: 5m
    labels:
      severity: critical

  - alert: RedisTooManyConnections
    expr: redis_connected_clients > 1000
    for: 5m
    labels:
      severity: warning
```

## 2. Performance Tuning

### Memory Configuration
```bash
# redis.conf

# Memory limit
maxmemory 4gb

# Eviction policy
maxmemory-policy allkeys-lru      # General cache
# maxmemory-policy volatile-lru   # Only keys with TTL
# maxmemory-policy volatile-ttl   # By TTL remaining
# maxmemory-policy noeviction     # Return errors

# Memory sampling
maxmemory-samples 10              # LRU precision

# Lazy freeing (async delete)
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
lazyfree-lazy-server-del yes
replica-lazy-flush yes
```

### Eviction Policy Selection
```
┌─────────────────────────────────────────────────────────────────────┐
│                  EVICTION POLICY DECISION                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  All keys are cache (can be regenerated)?                           │
│  ├── Yes ──> allkeys-lru (most common)                              │
│  │           └── or allkeys-lfu (frequency-based)                   │
│  │                                                                  │
│  └── No (some permanent data)                                       │
│      ├── Permanent keys have no TTL ──> volatile-lru                │
│      └── Evict by remaining TTL ──────> volatile-ttl                │
│                                                                     │
│  Cannot lose ANY data?                                              │
│  └── noeviction (returns errors when full)                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Connection Tuning
```bash
# redis.conf
maxclients 10000                  # Max connections
timeout 0                         # No idle timeout (0)
tcp-keepalive 300                 # TCP keepalive

# Client output buffer limits
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

### Slow Log Analysis
```bash
# Configure slow log
redis-cli CONFIG SET slowlog-log-slower-than 10000  # 10ms
redis-cli CONFIG SET slowlog-max-len 128

# Analyze
redis-cli SLOWLOG GET 10          # Last 10 slow commands
redis-cli SLOWLOG LEN             # Total slow commands
redis-cli SLOWLOG RESET           # Clear log

# Common slow command fixes
# KEYS * → Use SCAN
# SMEMBERS large_set → Use SSCAN
# HGETALL large_hash → Use HMGET specific fields
```

### Benchmark
```bash
# Basic benchmark
redis-benchmark -q -n 100000

# With pipelining
redis-benchmark -q -n 100000 -P 16

# Specific commands
redis-benchmark -q -n 100000 -t set,get,lpush,lpop

# Cluster mode
redis-benchmark -q -n 100000 -c 50 --cluster
```

## 3. Redis Modules

### Module Overview

| Module | Purpose | Use Case |
|--------|---------|----------|
| RedisJSON | JSON documents | API responses, user profiles |
| RediSearch | Full-text search | Product search, autocomplete |
| RedisTimeSeries | Time-series data | Metrics, IoT, analytics |
| RedisBloom | Probabilistic | Dedup, rate limiting |
| RedisGraph | Graph database | Social networks, recommendations |

### RedisJSON
```bash
# Set JSON document
JSON.SET user:1 $ '{"name":"Alice","age":30,"city":"NYC"}'

# Get full document
JSON.GET user:1

# Get specific path
JSON.GET user:1 $.name

# Update field
JSON.SET user:1 $.age 31

# Array operations
JSON.SET user:1 $.tags '["redis","developer"]'
JSON.ARRAPPEND user:1 $.tags '"architect"'
```

### RediSearch
```bash
# Create index
FT.CREATE idx:users ON HASH PREFIX 1 user: SCHEMA
  name TEXT SORTABLE
  email TAG
  age NUMERIC SORTABLE

# Search
FT.SEARCH idx:users "@name:alice"
FT.SEARCH idx:users "@age:[25 35]"
FT.SEARCH idx:users "@name:ali*"  # Prefix

# Aggregate
FT.AGGREGATE idx:users "*" GROUPBY 1 @city REDUCE COUNT 0 AS count
```

### RedisTimeSeries
```bash
# Create time series
TS.CREATE sensor:temp:1 RETENTION 86400000 LABELS location office

# Add samples
TS.ADD sensor:temp:1 * 23.5
TS.MADD sensor:temp:1 * 23.5 sensor:temp:2 * 24.0

# Range query
TS.RANGE sensor:temp:1 - + AGGREGATION avg 3600000  # Hourly avg

# Multi-series query
TS.MRANGE - + FILTER location=office
```

### Module Loading
```bash
# redis.conf
loadmodule /opt/redis-stack/lib/rejson.so
loadmodule /opt/redis-stack/lib/redisearch.so
loadmodule /opt/redis-stack/lib/redistimeseries.so
loadmodule /opt/redis-stack/lib/redisbloom.so

# Or Redis Stack (all included)
docker run -p 6379:6379 redis/redis-stack:latest
```

## 4. Capacity Planning

### Memory Estimation
```bash
# Per-key overhead: ~70-90 bytes

# String: overhead + value_size
# List: overhead + 8 bytes/element + element_sizes
# Set: overhead + 8 bytes/element + element_sizes
# Hash: overhead + 16 bytes/field + field_sizes + value_sizes
# Sorted Set: overhead + 16 bytes/element + element_sizes

# Check actual usage
redis-cli MEMORY USAGE key_name
redis-cli MEMORY DOCTOR
```

### Sizing Formula
```
Required Memory =
  (Key Count × Average Key Size) +
  (Total Value Size) +
  (Key Count × 80 bytes overhead) +
  (20% fragmentation buffer) +
  (Replication buffer if master)
```

### Scaling Decision
```
┌─────────────────────────────────────────────────────────────────────┐
│                  SCALING DECISION TREE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Memory pressure?                                                   │
│  ├── Yes                                                            │
│  │   ├── Data fits in bigger node? ──> Vertical scale              │
│  │   └── Data exceeds node? ─────────> Redis Cluster (shard)       │
│  │                                                                  │
│  Read throughput issue?                                             │
│  ├── Yes ──> Add read replicas                                      │
│  │                                                                  │
│  Write throughput issue?                                            │
│  └── Yes ──> Redis Cluster (shard writes)                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Related Skills

- `redis-performance` - Performance deep dive (PRIMARY_BOND)
- `redis-modules` - Module development (SECONDARY_BOND)

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. High Memory Usage
```bash
# Diagnosis
redis-cli INFO memory
redis-cli MEMORY DOCTOR
redis-cli --bigkeys
```

**Fixes:**
| Cause | Solution |
|-------|----------|
| No eviction | Set maxmemory-policy |
| Big keys | Split or compress |
| No TTL on cache | Add TTL to cache keys |
| Memory fragmentation | Restart or `MEMORY PURGE` |

#### 2. High Latency
```bash
# Diagnosis
redis-cli --latency
redis-cli --latency-history
redis-cli LATENCY DOCTOR
redis-cli SLOWLOG GET 25
```

**Fixes:**
| Cause | Solution |
|-------|----------|
| Slow commands | Optimize (SCAN vs KEYS) |
| Large values | Compress or split |
| Persistence I/O | Use SSD, adjust AOF |
| Background save | Schedule during low traffic |

#### 3. Connection Issues
```bash
# Check connections
redis-cli INFO clients
redis-cli CLIENT LIST
redis-cli CONFIG GET maxclients
```

**Fixes:**
| Cause | Solution |
|-------|----------|
| Max clients reached | Increase maxclients |
| Connection leaks | Fix client code, add pooling |
| Slow clients | client-output-buffer-limit |

#### 4. Replication Lag
```bash
# Check replication
redis-cli INFO replication
redis-cli CLIENT LIST TYPE replica
```

**Fixes:**
| Cause | Solution |
|-------|----------|
| Network latency | Improve network |
| Slow replica disk | Use SSD |
| Large RDB transfer | Use diskless replication |

### Debug Checklist

```markdown
□ Memory usage within limits?
□ Slow log showing issues?
□ Latency within SLA?
□ Connections within limits?
□ Replication in sync?
□ Persistence completing?
□ No blocking commands?
□ Background saves successful?
```

### Incident Response Runbook

```markdown
## Redis Incident Response

### P1: Redis Down
1. Check process: `systemctl status redis`
2. Check logs: `tail -f /var/log/redis/redis.log`
3. Check memory: `free -h`
4. Restart if needed: `systemctl restart redis`
5. Verify: `redis-cli PING`
6. Check replication if applicable

### P2: High Latency
1. Check slow log: `redis-cli SLOWLOG GET 25`
2. Check memory: `redis-cli INFO memory`
3. Check clients: `redis-cli CLIENT LIST`
4. Check background jobs: `redis-cli INFO persistence`
5. Identify and fix slow commands

### P3: Memory Alert
1. Check usage: `redis-cli INFO memory`
2. Find big keys: `redis-cli --bigkeys`
3. Check eviction: `redis-cli INFO stats | grep evicted`
4. Consider: increase memory, add TTL, or scale
```

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E701 | OOM | Out of memory | Evict or scale |
| E702 | LOADING | Dataset loading | Wait |
| E703 | BUSY | Lua script running | Wait or SCRIPT KILL |
| E704 | MASTERDOWN | Master unreachable | Check master or failover |
| E705 | MISCONF | Persistence error | Check disk space/permissions |

---

## Production Config Template

```bash
# /etc/redis/redis.conf - Production Optimized

# === Performance ===
maxmemory 4gb
maxmemory-policy allkeys-lru
maxmemory-samples 10

# === Connections ===
maxclients 10000
timeout 0
tcp-keepalive 300
tcp-backlog 511

# === Persistence (Hybrid) ===
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes
save 900 1
save 300 10
save 60 10000

# === Slow Log ===
slowlog-log-slower-than 10000
slowlog-max-len 128

# === Lazy Freeing ===
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
lazyfree-lazy-server-del yes

# === Limits ===
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

# === Logging ===
loglevel notice
logfile /var/log/redis/redis.log
```
