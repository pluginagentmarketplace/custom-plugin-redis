---
name: redis-hashes-sorted-sets
description: Master Redis Hashes and Sorted Sets - object storage, field operations, leaderboards, rankings, and scoring systems
sasmp_version: "1.3.0"
bonded_agent: redis-data-structures
bond_type: PRIMARY_BOND
---

# Redis Hashes and Sorted Sets Skill

## Hashes Overview

Redis Hashes are maps between string fields and string values - perfect for object storage.

### Hash Commands
```redis
# Basic operations
HSET key field value [field value ...]
HGET key field
HGETALL key
HDEL key field [field ...]
HEXISTS key field

# Bulk operations
HMSET key field value [field value ...]
HMGET key field [field ...]

# Numeric operations
HINCRBY key field increment
HINCRBYFLOAT key field increment

# Metadata
HLEN key
HKEYS key
HVALS key
```

## Sorted Sets Overview

Sorted Sets combine Sets with scores, enabling ranked collections.

### Sorted Set Commands
```redis
# Add with scores
ZADD key [NX|XX] [GT|LT] [CH] [INCR] score member [score member ...]

# Range queries
ZRANGE key start stop [WITHSCORES]
ZREVRANGE key start stop [WITHSCORES]
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]

# Ranking
ZRANK key member
ZREVRANK key member
ZSCORE key member

# Modifications
ZINCRBY key increment member
ZREM key member [member ...]

# Cardinality
ZCARD key
ZCOUNT key min max
```

## Use Case: User Profile Storage

```redis
# Store user as hash
HSET user:123 name "John" email "john@example.com" age 30

# Get specific field
HGET user:123 email

# Update field
HINCRBY user:123 age 1
```

## Use Case: Leaderboard

```redis
# Add scores
ZADD leaderboard 1000 "player:1"
ZADD leaderboard 1500 "player:2"
ZADD leaderboard 800 "player:3"

# Get top 10
ZREVRANGE leaderboard 0 9 WITHSCORES

# Get player rank
ZREVRANK leaderboard "player:1"
```

## Assets

- `leaderboard.lua` - Atomic leaderboard operations

## Scripts

- `hash-migration.py` - Hash data migration script

## References

- `HASH_ZSET_PATTERNS.md` - Pattern guide
