---
name: redis-strings
description: Master Redis Strings - SET, GET, INCR, DECR, atomic counters, binary-safe operations, and caching patterns
sasmp_version: "1.3.0"
bonded_agent: redis-data-structures
bond_type: PRIMARY_BOND
---

# Redis Strings Skill

## Overview

Master Redis String data type - the most versatile and commonly used data structure in Redis.

## Core Commands

### Basic Operations
```redis
SET key value [EX seconds] [PX milliseconds] [NX|XX]
GET key
DEL key [key ...]
EXISTS key [key ...]
```

### Atomic Counters
```redis
INCR key
DECR key
INCRBY key increment
DECRBY key decrement
INCRBYFLOAT key increment
```

### String Manipulation
```redis
APPEND key value
STRLEN key
GETRANGE key start end
SETRANGE key offset value
```

### Batch Operations
```redis
MSET key value [key value ...]
MGET key [key ...]
MSETNX key value [key value ...]
```

## Use Case: Rate Limiter

```redis
# Sliding window rate limiter
SETEX user:123:requests 60 1      # First request
INCR user:123:requests            # Subsequent requests
GET user:123:requests             # Check count
```

## Use Case: Session Cache

```redis
# Store session with expiry
SET session:abc123 '{"user_id":1,"name":"John"}' EX 3600

# Get session
GET session:abc123
```

## Assets

- `rate-limiter.lua` - Lua script for atomic rate limiting
- `session-store.yaml` - Session configuration template

## Scripts

- `string-benchmark.sh` - Performance testing script

## References

- `STRING_PATTERNS.md` - Common patterns guide
