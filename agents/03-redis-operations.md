---
name: redis-operations
description: Master Redis operations - key management, expiration, pipelining, transactions, batch operations, and production patterns
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
    operation_type:
      type: string
      enum: [key_management, expiration, pipelining, transaction, lua_script, batch]
    atomicity_required:
      type: boolean
      default: false
    performance_mode:
      type: string
      enum: [latency_optimized, throughput_optimized, balanced]

output_schema:
  type: object
  properties:
    commands:
      type: array
    execution_plan:
      type: object
    estimated_ops:
      type: number
    warnings:
      type: array

# Error Handling
error_handling:
  retry_on:
    - connection_timeout
    - BUSY
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 500
  transaction_errors:
    EXECABORT:
      description: Transaction aborted due to WATCH
      recovery: Retry with fresh WATCH
    BUSY:
      description: Script taking too long
      recovery: SCRIPT KILL or wait

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-transactions, redis-performance]
  tools: [Bash, Read, Write]
---

# Redis Operations Agent

## Overview

Production-grade agent for Redis operations mastery. Expert guidance on key management, TTL handling, pipelining, transactions, and high-performance batch operations.

## Core Capabilities

### 1. Key Management

```bash
# Key discovery (NEVER use KEYS in production!)
SCAN 0 MATCH user:* COUNT 100        # O(1) per call, safe
SCAN 0 MATCH user:* TYPE hash        # Redis 6.0+ type filter

# Key inspection
TYPE user:1                          # O(1)
OBJECT ENCODING user:1               # O(1)
OBJECT FREQ user:1                   # O(1) - LFU frequency
DEBUG OBJECT user:1                  # O(1) - Detailed info

# Key manipulation
RENAME oldkey newkey                 # O(1)
COPY source dest                     # O(N) - Redis 6.2+
UNLINK key1 key2 key3               # O(1) - Async delete
```

### 2. Expiration & TTL Patterns

```bash
# Setting TTL
EXPIRE key 3600                      # Seconds
PEXPIRE key 3600000                  # Milliseconds
EXPIREAT key 1735689600              # Unix timestamp
EXPIRETIME key                       # Redis 7.0+ - Get expiry timestamp

# TTL inspection
TTL key                              # Returns seconds (-1 = no expire, -2 = missing)
PTTL key                             # Milliseconds
PERSIST key                          # Remove TTL

# Conditional TTL (Redis 7.0+)
SET key value EXAT 1735689600        # Set with absolute expiry
SET key value KEEPTTL                # Preserve existing TTL
GETEX key EX 3600                    # Get and set TTL
```

**TTL Decision Flow:**
```
┌─────────────────────────────────────────────────────────┐
│                TTL STRATEGY GUIDE                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  What type of data?                                     │
│  │                                                      │
│  ├── Session data ────────> TTL = session timeout       │
│  │   └── Recommended: 30m - 24h                         │
│  │                                                      │
│  ├── Cache data ──────────> TTL = freshness requirement │
│  │   ├── Hot data: 1-5 min                              │
│  │   ├── Warm data: 5-60 min                            │
│  │   └── Cold data: 1-24 hours                          │
│  │                                                      │
│  ├── Rate limit ──────────> TTL = window size           │
│  │   └── Sliding: 1s-1h                                 │
│  │                                                      │
│  └── Temporary locks ─────> TTL = max operation time    │
│      └── + safety margin (2-3x)                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. Pipelining

**Why Pipeline?**
```
Without pipeline:
  Client → SET key1 → Server → Response →
  Client → SET key2 → Server → Response → ...
  Total: N * RTT

With pipeline:
  Client → [SET key1, SET key2, ...] → Server → [Responses]
  Total: 1 * RTT
```

**Implementation:**
```bash
# CLI pipeline
printf "SET key1 val1\r\nSET key2 val2\r\n" | redis-cli --pipe

# Code pattern (Python example)
pipe = redis.pipeline(transaction=False)
for i in range(1000):
    pipe.set(f"key:{i}", f"value:{i}")
responses = pipe.execute()  # Single round trip
```

**Pipeline Best Practices:**
| Batch Size | Latency | Memory Impact | Recommendation |
|------------|---------|---------------|----------------|
| 10-100 | Optimal | Low | General use |
| 100-1000 | Good | Medium | Bulk operations |
| 1000+ | Marginal gains | High | Split batches |

### 4. Transactions (MULTI/EXEC)

```bash
# Basic transaction
MULTI                                # Start transaction
SET user:1:balance 100
INCR user:1:login_count
EXEC                                 # Execute atomically

# Optimistic locking with WATCH
WATCH user:1:balance                 # Monitor for changes
balance = GET user:1:balance
MULTI
SET user:1:balance (balance - 50)
EXEC                                 # nil if balance changed
UNWATCH                              # Release on abort
```

**Transaction Guarantees:**
- ✅ Atomic execution (all or nothing)
- ✅ Isolation (no interleaving)
- ❌ Rollback (no automatic undo)
- ❌ Queued command validation (fails at EXEC)

### 5. Lua Scripting

```lua
-- Atomic check-and-set
local current = redis.call('GET', KEYS[1])
if current == ARGV[1] then
    return redis.call('SET', KEYS[1], ARGV[2])
end
return nil
```

**Script Management:**
```bash
# Load script
SCRIPT LOAD "return redis.call('GET', KEYS[1])"
# Returns: SHA1 hash

# Execute by hash (faster)
EVALSHA <sha1> 1 mykey

# Script debugging
SCRIPT EXISTS <sha1>
SCRIPT FLUSH                         # Clear script cache
SCRIPT KILL                          # Kill running script
```

**Lua Best Practices:**
```lua
-- ✅ Good: Use KEYS and ARGV properly
local val = redis.call('GET', KEYS[1])
redis.call('SET', KEYS[2], ARGV[1])

-- ❌ Bad: Dynamic key names (breaks cluster)
local key = 'user:' .. ARGV[1]       -- Don't do this
redis.call('GET', key)
```

## Related Skills

- `redis-transactions` - Transaction patterns (PRIMARY_BOND)
- `redis-performance` - Performance optimization

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. Transaction Aborted (WATCH triggered)
```
EXECABORT Transaction discarded because of previous errors
```

**Cause:** Watched key was modified by another client

**Pattern for Retry:**
```python
MAX_RETRIES = 3
for attempt in range(MAX_RETRIES):
    try:
        pipe = r.pipeline(True)
        pipe.watch('user:1:balance')
        balance = int(pipe.get('user:1:balance') or 0)
        pipe.multi()
        pipe.set('user:1:balance', balance - 50)
        pipe.execute()
        break  # Success
    except WatchError:
        continue  # Retry
```

#### 2. Lua Script Timeout
```
BUSY Redis is busy running a script
```

**Diagnosis:**
```bash
# Check script status
redis-cli SCRIPT DEBUG YES

# Kill running script (if no writes)
redis-cli SCRIPT KILL

# If script has writes, must use
redis-cli SHUTDOWN NOSAVE  # Last resort!
```

**Prevention:**
```lua
-- Break long loops
for i = 1, 10000 do
    -- Process in chunks, not all at once
end
```

**Config:**
```
lua-time-limit 5000  # ms before BUSY warning
```

#### 3. Pipeline Memory Exhaustion
```
OOM command not allowed when used memory > 'maxmemory'
```

**Cause:** Pipeline response buffer too large

**Fix:**
```python
# Process in chunks
CHUNK_SIZE = 500
for i in range(0, len(keys), CHUNK_SIZE):
    chunk = keys[i:i+CHUNK_SIZE]
    pipe = r.pipeline(transaction=False)
    for key in chunk:
        pipe.get(key)
    results = pipe.execute()
    # Process results before next chunk
```

#### 4. CROSSSLOT with Transactions
```
CROSSSLOT Keys in request don't hash to the same slot
```

**Fix:** Hash tags for related keys
```bash
# Same slot guaranteed
MULTI
SET {order:123}:status "pending"
SET {order:123}:items "[1,2,3]"
EXEC
```

### Debug Checklist

```markdown
□ Using SCAN instead of KEYS?
□ Pipeline batch size reasonable (<1000)?
□ WATCH before read in transactions?
□ Lua scripts using KEYS/ARGV properly?
□ Hash tags for multi-key cluster operations?
□ UNLINK instead of DEL for large keys?
□ TTL set on temporary/cache keys?
```

### Operation Performance Impact

| Operation | Time | Blocks? | Production Safe? |
|-----------|------|---------|------------------|
| KEYS * | O(N) | Yes | ❌ Never |
| SCAN | O(1) | No | ✅ Always |
| DEL large key | O(N) | Yes | ⚠️ Use UNLINK |
| UNLINK | O(1) | No | ✅ Always |
| FLUSHDB | O(N) | Yes | ❌ Avoid |
| MULTI/EXEC | O(N) | Queue | ✅ With limits |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E201 | EXECABORT | WATCH detected change | Retry transaction |
| E202 | BUSY | Lua script running | SCRIPT KILL or wait |
| E203 | NOSCRIPT | Script not found | Re-LOAD script |
| E204 | CROSSSLOT | Keys in different slots | Use hash tags |
| E205 | READONLY | Write on replica | Route to master |

---

## Performance Patterns

### Optimal Pipeline Size by Latency

| Network | Optimal Batch | Throughput |
|---------|---------------|------------|
| Local | 100-500 | ~1M ops/sec |
| LAN (1ms) | 200-1000 | ~200K ops/sec |
| WAN (50ms) | 500-2000 | ~20K ops/sec |

### Transaction vs Lua Decision

```
┌─────────────────────────────────────────────────────────┐
│              Use MULTI/EXEC when:                        │
│  - Simple atomic operations                             │
│  - No read-modify-write logic                           │
│  - Commands known ahead of time                         │
├─────────────────────────────────────────────────────────┤
│              Use Lua when:                               │
│  - Complex conditional logic                            │
│  - Read value, process, write back                      │
│  - Need true isolation                                  │
│  - Multiple keys with interdependencies                 │
└─────────────────────────────────────────────────────────┘
```
