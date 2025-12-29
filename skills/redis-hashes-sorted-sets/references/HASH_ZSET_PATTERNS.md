# Redis Hashes and Sorted Sets: Patterns

## Hash Patterns

### 1. Object Storage
```redis
HSET user:123 name "John" email "john@example.com" role "admin"
HGETALL user:123
```

### 2. Counters per Entity
```redis
HINCRBY article:456:stats views 1
HINCRBY article:456:stats shares 1
HGETALL article:456:stats
```

## Sorted Set Patterns

### 1. Leaderboard
```redis
ZADD leaderboard 1500 player:1
ZREVRANGE leaderboard 0 9 WITHSCORES
```

### 2. Time-based Events
```redis
ZADD events 1704067200 "event:1"  # Unix timestamp as score
ZRANGEBYSCORE events 1704067200 1704153600
```

### 3. Priority Queue
```redis
ZADD priority:queue 1 "low:task"
ZADD priority:queue 10 "high:task"
ZPOPMAX priority:queue
```

## Best Practices
1. Use hashes for objects with many fields
2. Use sorted sets when ordering matters
3. ZINCRBY for atomic score updates
4. HSCAN for large hashes
