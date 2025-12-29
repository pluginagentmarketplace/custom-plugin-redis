---
name: redis-lists-sets
description: Master Redis Lists and Sets - queues, stacks, unique collections, set operations, and real-world implementation patterns
sasmp_version: "1.3.0"
bonded_agent: redis-data-structures
bond_type: PRIMARY_BOND
---

# Redis Lists and Sets Skill

## Lists Overview

Redis Lists are linked lists of string values, perfect for queues and stacks.

### List Commands
```redis
# Push operations
LPUSH key value [value ...]   # Push to head
RPUSH key value [value ...]   # Push to tail

# Pop operations
LPOP key [count]              # Pop from head
RPOP key [count]              # Pop from tail
BLPOP key [key ...] timeout   # Blocking pop

# Range operations
LRANGE key start stop         # Get range
LINDEX key index              # Get by index
LLEN key                      # Get length

# Manipulation
LMOVE source dest LEFT|RIGHT LEFT|RIGHT
LINSERT key BEFORE|AFTER pivot value
```

## Sets Overview

Redis Sets are unordered collections of unique strings.

### Set Commands
```redis
# Basic operations
SADD key member [member ...]   # Add members
SREM key member [member ...]   # Remove members
SMEMBERS key                   # Get all members
SISMEMBER key member           # Check membership
SCARD key                      # Get cardinality

# Set operations
SINTER key [key ...]           # Intersection
SUNION key [key ...]           # Union
SDIFF key [key ...]            # Difference
```

## Use Case: Message Queue

```redis
# Producer
RPUSH queue:tasks '{"id":1,"action":"process"}'

# Consumer
BLPOP queue:tasks 30
```

## Use Case: Unique Visitors

```redis
# Track unique visitors
SADD visitors:2024-01-15 "user:123"
SADD visitors:2024-01-15 "user:456"

# Count unique
SCARD visitors:2024-01-15
```

## Assets

- `queue-config.yaml` - Queue configuration template

## Scripts

- `queue-consumer.py` - Python queue consumer example

## References

- `LIST_SET_PATTERNS.md` - Common patterns guide
