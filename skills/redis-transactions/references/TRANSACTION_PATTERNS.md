# Redis Transaction Patterns

## MULTI/EXEC vs Lua

| Feature | MULTI/EXEC | Lua Script |
|---------|------------|------------|
| Atomicity | Batch only | True atomic |
| Conditionals | No | Yes |
| Rollback | No | Manual |
| Performance | Multiple RTT | Single RTT |

## Pattern: Check-and-Set

```lua
local current = redis.call('GET', KEYS[1])
if current == ARGV[1] then
    redis.call('SET', KEYS[1], ARGV[2])
    return 1
end
return 0
```

## Pattern: Inventory Reserve

```lua
local stock = tonumber(redis.call('GET', KEYS[1]))
local qty = tonumber(ARGV[1])
if stock >= qty then
    redis.call('DECRBY', KEYS[1], qty)
    return stock - qty
end
return -1  -- Insufficient stock
```

## Best Practices

1. Keep Lua scripts short
2. Avoid infinite loops
3. Use EVALSHA for performance
4. Test scripts thoroughly
5. Handle nil values
