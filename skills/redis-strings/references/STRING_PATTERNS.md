# Redis Strings: Common Patterns

## 1. Caching Pattern

```redis
# Cache with TTL
SET cache:user:123 '{"name":"John","email":"john@example.com"}' EX 3600

# Check before fetching from DB
GET cache:user:123
# If nil, fetch from DB and SET
```

## 2. Counter Pattern

```redis
# Page views
INCR pageviews:article:456

# Daily counter with auto-expiry
INCR daily:visits:2024-01-15
EXPIRE daily:visits:2024-01-15 86400
```

## 3. Distributed Lock

```redis
# Acquire lock
SET lock:resource:123 "owner_id" NX EX 30

# Release lock (only if owner)
-- Use Lua script for atomic check-and-delete
```

## 4. Session Storage

```redis
# Create session
SET session:token123 '{"user_id":1}' EX 1800

# Refresh session
EXPIRE session:token123 1800

# Invalidate
DEL session:token123
```

## 5. Rate Limiting

```redis
# Fixed window
INCR rate:ip:1.2.3.4:minute:2024-01-15T10:30
EXPIRE rate:ip:1.2.3.4:minute:2024-01-15T10:30 60

# Check limit
GET rate:ip:1.2.3.4:minute:2024-01-15T10:30
```

## Best Practices

1. Use meaningful key names: `type:entity:id:field`
2. Always set TTL for cache keys
3. Use NX for distributed locks
4. Use MGET/MSET for batch operations
5. Consider INCR for counters (atomic)
