# Redis Lists and Sets: Common Patterns

## List Patterns

### 1. Message Queue (FIFO)
```redis
# Producer
RPUSH queue:emails '{"to":"user@example.com"}'

# Consumer
LPOP queue:emails
# Or blocking
BLPOP queue:emails 30
```

### 2. Stack (LIFO)
```redis
# Push
LPUSH stack:undo '{"action":"delete","id":123}'

# Pop
LPOP stack:undo
```

### 3. Recent Items
```redis
# Add new item (keep last 100)
LPUSH recent:user:123 '{"item":"article:456"}'
LTRIM recent:user:123 0 99

# Get recent
LRANGE recent:user:123 0 9
```

### 4. Priority Queue
```redis
# Use sorted sets for priorities
# But for simple high/low priority:
LPUSH queue:high:priority "urgent_task"
RPUSH queue:low:priority "normal_task"

# Process high first
BLPOP queue:high:priority queue:low:priority 30
```

## Set Patterns

### 1. Tagging System
```redis
# Tag articles
SADD tag:redis "article:1" "article:5"
SADD tag:database "article:1" "article:3"

# Find articles with both tags
SINTER tag:redis tag:database

# Articles with either tag
SUNION tag:redis tag:database
```

### 2. Unique Visitors
```redis
# Track unique visitors per day
SADD visitors:2024-01-15 "user:123"

# Count
SCARD visitors:2024-01-15

# Check if visited
SISMEMBER visitors:2024-01-15 "user:123"
```

### 3. Online Users
```redis
# User comes online
SADD online:users "user:123"

# User goes offline
SREM online:users "user:123"

# Get online count
SCARD online:users

# Is user online?
SISMEMBER online:users "user:123"
```

### 4. Friend Relationships
```redis
# User A follows
SADD following:userA "userB" "userC"

# User B follows
SADD following:userB "userA" "userC"

# Mutual follows
SINTER following:userA following:userB
```

## Best Practices

1. Use LTRIM after LPUSH for bounded lists
2. Use BLPOP for blocking queue consumers
3. Use SISMEMBER before SADD to avoid duplicates
4. Use SCAN variants for large sets
5. Consider memory impact of large collections
