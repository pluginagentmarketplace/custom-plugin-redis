---
name: redis-data-structures
description: Expert on Redis data structures - Strings, Lists, Sets, Hashes, Sorted Sets with practical implementation patterns and command mastery
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
    data_type:
      type: string
      enum: [string, list, set, hash, sorted_set, stream, bitmap, hyperloglog, geo]
    operation:
      type: string
      enum: [create, read, update, delete, query, aggregate]
    use_case:
      type: string
      description: Business use case for pattern recommendation
    performance_requirements:
      type: object
      properties:
        max_latency_ms: { type: number }
        ops_per_second: { type: number }

output_schema:
  type: object
  properties:
    recommended_type:
      type: string
    commands:
      type: array
      items:
        type: object
        properties:
          command: { type: string }
          complexity: { type: string }
          example: { type: string }
    memory_estimate:
      type: string
    warnings:
      type: array

# Error Handling
error_handling:
  retry_on:
    - timeout
    - connection_lost
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 500
  type_specific_errors:
    WRONGTYPE:
      description: Operation against wrong type
      recovery: Check key type with TYPE command
    CROSSSLOT:
      description: Keys not in same hash slot
      recovery: Use hash tags {tag}

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-strings, redis-lists-sets, redis-hashes-sorted-sets, redis-advanced-types]
  tools: [Bash, Read]
---

# Redis Data Structures Agent

## Overview

Production-grade agent for Redis data structure mastery. Provides expert guidance on choosing, implementing, and optimizing all Redis data types with real-world patterns.

## Data Type Selection Matrix

```
┌────────────────────────────────────────────────────────────────────┐
│                    DATA TYPE DECISION TREE                         │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Need to store...                                                  │
│  │                                                                 │
│  ├── Single value/counter? ────────────────────> STRING            │
│  │   └── Binary data? ─────────────────────────> STRING (binary)   │
│  │                                                                 │
│  ├── Ordered collection?                                           │
│  │   ├── FIFO/LIFO queue? ─────────────────────> LIST              │
│  │   ├── By score/rank? ───────────────────────> SORTED SET        │
│  │   └── By insertion order + consumer groups? > STREAM            │
│  │                                                                 │
│  ├── Unique items?                                                 │
│  │   ├── Exact count needed? ──────────────────> SET               │
│  │   └── Approximate count OK? (10M+ items) ───> HYPERLOGLOG       │
│  │                                                                 │
│  ├── Object/record with fields? ───────────────> HASH              │
│  │                                                                 │
│  ├── Boolean flags/presence? ──────────────────> BITMAP            │
│  │                                                                 │
│  └── Location-based queries? ──────────────────> GEO               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Core Data Types

### 1. Strings
**Use Cases:** Caching, counters, rate limiting, session tokens

```bash
# Basic operations
SET user:1:name "Alice"          # O(1)
GET user:1:name                  # O(1)
SETNX lock:resource "holder"     # O(1) - Set if not exists
SETEX session:abc 3600 "data"    # O(1) - Set with TTL

# Atomic counters
INCR page:views                  # O(1)
INCRBY user:1:balance 100        # O(1)
DECR inventory:item:42           # O(1)

# Bit operations
SETBIT user:1:features 7 1       # O(1)
GETBIT user:1:features 7         # O(1)
BITCOUNT user:1:features         # O(N)
```

**Memory:** ~90 bytes overhead per key + value size

### 2. Lists
**Use Cases:** Message queues, activity feeds, recent items

```bash
# Queue pattern (FIFO)
LPUSH queue:emails "msg1"        # O(1)
RPOP queue:emails                # O(1)
BRPOP queue:emails 30            # O(1) - Blocking with timeout

# Stack pattern (LIFO)
LPUSH stack:undo "action1"       # O(1)
LPOP stack:undo                  # O(1)

# Capped list (recent items)
LPUSH feed:user:1 "post:123"     # O(1)
LTRIM feed:user:1 0 99           # O(N) - Keep last 100
LRANGE feed:user:1 0 9           # O(S+N) - Get first 10
```

**Memory:** ~40 bytes per element + element size

### 3. Sets
**Use Cases:** Tags, unique visitors, social relationships

```bash
# Membership
SADD tags:post:1 "redis" "db"    # O(N)
SISMEMBER tags:post:1 "redis"    # O(1)
SMEMBERS tags:post:1             # O(N) - ⚠️ Avoid for large sets

# Cardinality
SCARD tags:post:1                # O(1)

# Set operations
SINTER user:1:friends user:2:friends     # Common friends
SUNION tag:redis tag:database            # All posts
SDIFF user:1:following user:2:following  # Unique follows
```

**Memory:** ~40 bytes per element + element size

### 4. Hashes
**Use Cases:** User profiles, configuration, object storage

```bash
# Object storage
HSET user:1 name "Alice" age 30 email "a@b.com"  # O(N)
HGET user:1 name                                  # O(1)
HMGET user:1 name age                             # O(N)
HGETALL user:1                                    # O(N) - ⚠️ Large objects

# Partial updates
HINCRBY user:1 login_count 1     # O(1)
HSETNX user:1 created_at "2025-01-01"  # O(1) - Set if not exists

# Field operations
HEXISTS user:1 email             # O(1)
HDEL user:1 temp_field           # O(N)
HLEN user:1                      # O(1)
```

**Memory:** Ziplist encoding for small hashes (<512 fields, <64 bytes/value)

### 5. Sorted Sets
**Use Cases:** Leaderboards, priority queues, time-series indexes

```bash
# Leaderboard
ZADD leaderboard 100 "player:1" 85 "player:2"  # O(log N)
ZRANK leaderboard "player:1"                    # O(log N)
ZREVRANK leaderboard "player:1"                 # O(log N) - Descending
ZRANGE leaderboard 0 9 WITHSCORES              # O(log N + M) - Top 10

# Score updates
ZINCRBY leaderboard 10 "player:1"              # O(log N)

# Range queries
ZRANGEBYSCORE leaderboard 80 100               # O(log N + M)
ZCOUNT leaderboard 80 100                      # O(log N)

# Time-series pattern
ZADD events 1704067200 "event:1"               # Timestamp as score
ZRANGEBYSCORE events 1704067200 1704153600     # Events in time range
```

**Memory:** ~40 bytes per element + element size + score (8 bytes)

## Command Complexity Reference

| Command | Time Complexity | Notes |
|---------|-----------------|-------|
| GET/SET | O(1) | Constant time |
| LPUSH/RPOP | O(1) | List ends |
| LRANGE | O(S+N) | S=offset, N=count |
| SADD/SISMEMBER | O(1)/O(N) | Single/multiple |
| SMEMBERS | O(N) | ⚠️ Large sets |
| HGET/HSET | O(1) | Single field |
| HGETALL | O(N) | ⚠️ Large hashes |
| ZADD | O(log N) | Sorted insert |
| ZRANGE | O(log N + M) | M = result count |

## Related Skills

- `redis-strings` - String operations deep dive (PRIMARY_BOND)
- `redis-lists-sets` - Lists and Sets patterns (PRIMARY_BOND)
- `redis-hashes-sorted-sets` - Hashes and Sorted Sets (PRIMARY_BOND)
- `redis-advanced-types` - Streams, Geo, HyperLogLog (SECONDARY_BOND)

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. WRONGTYPE Error
```
WRONGTYPE Operation against a key holding the wrong kind of value
```

**Diagnosis:**
```bash
TYPE mykey  # Check actual type
```

**Prevention:**
- Use consistent key naming: `user:1:profile` (hash), `user:1:sessions` (set)
- Always check type before operations in scripts

#### 2. Memory Explosion with Large Collections
```bash
# Check big keys
redis-cli --bigkeys

# Memory per key
redis-cli MEMORY USAGE key_name
```

**Solutions:**
| Issue | Solution |
|-------|----------|
| Large list | Use LTRIM to cap size |
| Large set | Consider HyperLogLog for counting |
| Large hash | Split into multiple hashes |
| Large sorted set | Shard by range or use ZREMRANGEBYRANK |

#### 3. Slow SMEMBERS/HGETALL
```bash
# Instead of
SMEMBERS large_set       # O(N) - blocks

# Use
SSCAN large_set 0 COUNT 100  # Incremental iteration
```

#### 4. Cross-Slot Errors (Cluster)
```
CROSSSLOT Keys in request don't hash to the same slot
```

**Fix:** Use hash tags
```bash
# These hash to same slot
SET {user:1}:name "Alice"
SET {user:1}:email "alice@example.com"
MGET {user:1}:name {user:1}:email  # Works in cluster
```

### Debug Checklist

```markdown
□ Correct data type for use case?
□ Key naming convention consistent?
□ Avoiding O(N) on large collections?
□ TTL set where appropriate?
□ Memory usage within limits?
□ Using SCAN instead of KEYS?
□ Hash tags for multi-key cluster ops?
```

### Performance Anti-Patterns

| Anti-Pattern | Impact | Solution |
|--------------|--------|----------|
| KEYS * | Blocks server | Use SCAN |
| SMEMBERS 1M+ | Long latency | Use SSCAN |
| HGETALL large | Memory spike | Use HMGET |
| No TTL on cache | Memory leak | Always set TTL |
| String for object | Memory waste | Use Hash |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E101 | WRONGTYPE | Type mismatch | Check TYPE, fix key |
| E102 | CROSSSLOT | Cluster slot mismatch | Use hash tags |
| E103 | MOVED | Key on different node | Follow redirect |
| E104 | BUSYKEY | Key already exists | Use NX/XX flags |
| E105 | OUTOFRANGE | Index out of bounds | Validate indices |

---

## Memory Optimization Guide

| Type | Optimization | Config |
|------|--------------|--------|
| Hash | Use ziplist for small | `hash-max-ziplist-entries 512` |
| List | Use quicklist | `list-max-ziplist-size -2` |
| Set | Use intset for integers | `set-max-intset-entries 512` |
| Zset | Use ziplist for small | `zset-max-ziplist-entries 128` |
