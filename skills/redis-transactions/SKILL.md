---
name: redis-transactions
description: Master Redis transactions - MULTI/EXEC, WATCH for optimistic locking, Lua scripting, and atomic operation patterns
sasmp_version: "1.3.0"
bonded_agent: redis-operations
bond_type: PRIMARY_BOND
---

# Redis Transactions Skill

## MULTI/EXEC Transactions

Execute multiple commands atomically.

```redis
MULTI
SET user:123:balance 100
INCR user:123:transactions
EXEC
```

## WATCH - Optimistic Locking

Abort if watched keys change.

```redis
WATCH user:123:balance
val = GET user:123:balance
MULTI
SET user:123:balance (val - 50)
EXEC  # Returns nil if balance changed
```

## Lua Scripting

True atomicity with complex logic.

```redis
EVAL "return redis.call('GET', KEYS[1])" 1 mykey
EVALSHA sha1 numkeys key [key ...] arg [arg ...]
SCRIPT LOAD "return 1"
```

## Use Case: Transfer Funds

```lua
-- Atomic fund transfer
local from = KEYS[1]
local to = KEYS[2]
local amount = tonumber(ARGV[1])

local balance = tonumber(redis.call('GET', from))
if balance >= amount then
    redis.call('DECRBY', from, amount)
    redis.call('INCRBY', to, amount)
    return 1
end
return 0
```

## Assets
- `transfer.lua` - Fund transfer script
- `distributed-lock.lua` - Distributed lock implementation

## References
- `TRANSACTION_PATTERNS.md` - Best practices
