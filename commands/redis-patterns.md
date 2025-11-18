# /redis-patterns - Proven Design Patterns

Explore production-ready Redis design patterns for common problems.

## Usage

```
/redis-patterns
/redis-patterns caching
/redis-patterns sessions
/redis-patterns queues
/redis-patterns locks
/redis-patterns rate-limiting
/redis-patterns pubsub
/redis-patterns leaderboards
```

## All Patterns

### 1. Cache-Aside (Lazy Loading)

**When**: Read-heavy workloads, web applications

**How**:
```
1. Check cache for data
2. If miss: load from database
3. Store in cache with TTL
4. Return data
```

**Benefits**: Simple, doesn't require sync
**Drawback**: Cache miss latency, potential stale data

### 2. Write-Through Caching

**When**: Data consistency is critical

**How**:
```
1. Write to cache
2. Write to database
3. Return success
```

**Benefits**: Cache always in sync
**Drawback**: Slower writes

### 3. Session Management

**When**: Web applications, user sessions

**Pattern**:
- Store session in Redis hash
- Set TTL for expiration
- Update TTL on each request
- Distribute across servers

### 4. Distributed Locks

**When**: Critical sections, mutual exclusion

**Pattern**:
- SET key value NX EX timeout
- Lua script for atomic check-and-delete
- Retry with backoff
- Timeout to prevent deadlocks

**Use Case**: Inventory updates, financial transactions

### 5. Rate Limiting

**When**: API protection, DoS prevention

**Patterns**:
- **Token Bucket**: INCR with EXPIRE
- **Sliding Window**: ZSET with timestamps
- **Leaky Bucket**: LPUSH + BLPOP

**Implementation**: Token bucket easiest

### 6. Pub/Sub Messaging

**When**: Real-time notifications, live updates

**Pattern**:
- Subscribe to channel
- Publisher sends messages
- All subscribers receive instantly
- Fire-and-forget (no persistence)

**Use Case**: Chat, notifications, live feeds

### 7. Queues

**When**: Async job processing, task queues

**Patterns**:
- **FIFO Queue**: LPUSH + BRPOP
- **Priority Queue**: ZADD with score
- **Job Processing**: BRPOPLPUSH for reliability

**Features**: Blocking, atomic, fast

### 8. Leaderboards

**When**: Rankings, scoreboards, topN

**Pattern**:
- ZADD for score updates
- ZREVRANGE for top N
- ZREVRANK for user position
- ZINCRBY for score increment

### 9. Real-Time Counters

**When**: Analytics, metrics, stats

**Pattern**:
- INCR for atomic increment
- SETEX for time-windowed counters
- EXPIRE for cleanup
- ZADD for time-series

### 10. Unique Items Tracker

**When**: Unique visitors, deduplication

**Pattern**:
- SADD to track items
- SCARD for total count
- SISMEMBER for membership test
- SUNION for combined sets

### 11. Distributed Session Store

**When**: Multi-server applications

**Pattern**:
```
- Session ID: unique identifier
- Data: user info, preferences
- TTL: inactivity timeout
- Storage: hash structure
```

### 12. Cache Warming

**When**: Prevent thundering herd

**Pattern**:
```
1. Preload hot data
2. Schedule refresh
3. Update cache proactively
4. Handle cache misses
```

## Quick Pattern Selector

**Question**: What's your use case?

**I need to...** → **Pattern** → **Data Structure**
- Cache data → Cache-Aside → String
- Store sessions → Session Manager → Hash
- Track unique items → Set Operations → Set
- Rank users → Leaderboard → Sorted Set
- Run background jobs → Queues → List
- Send notifications → Pub/Sub → (Built-in)
- Prevent abuse → Rate Limiting → String
- Coordinate servers → Distributed Lock → String
- Log events → Streams → Stream
- Message queue → Queues → List

## Implementation Examples

### Caching Implementation

```python
def get_with_cache(key, loader, ttl=3600):
    """Generic cache-aside pattern"""
    value = r.get(key)
    if not value:
        value = loader()
        r.setex(key, ttl, value)
    return value

# Usage
user_data = get_with_cache(
    f'user:{user_id}',
    lambda: db.get_user(user_id),
    ttl=1800
)
```

### Session Implementation

```python
class SessionStore:
    def create(self, user_id):
        sid = str(uuid4())
        r.hset(f'session:{sid}', mapping={
            'user_id': user_id,
            'created': time.time()
        })
        r.expire(f'session:{sid}', 1800)
        return sid

    def get(self, sid):
        data = r.hgetall(f'session:{sid}')
        if data:
            r.expire(f'session:{sid}', 1800)  # Extend
        return data
```

### Queue Implementation

```python
class JobQueue:
    def enqueue(self, job):
        r.rpush('job_queue', json.dumps(job))

    def process(self):
        while True:
            job_json = r.brpop('job_queue', 1)
            if job_json:
                job = json.loads(job_json[1])
                self.execute(job)
```

### Rate Limiter Implementation

```python
class RateLimiter:
    def __init__(self, max_req=100, window=60):
        self.max_req = max_req
        self.window = window

    def is_allowed(self, client):
        key = f'ratelimit:{client}'
        current = r.incr(key)
        if current == 1:
            r.expire(key, self.window)
        return current <= self.max_req
```

## Best Practices

✅ **Do**:
- Choose pattern based on requirements
- Test with expected load
- Monitor performance
- Set appropriate TTLs
- Handle failures gracefully
- Document your patterns

❌ **Don't**:
- Mix patterns unnecessarily
- Ignore edge cases
- Forget about TTL
- Assume zero latency
- Store sensitive data unencrypted

## Pattern Performance

| Pattern | Latency | Throughput | Use Case |
|---------|---------|-----------|----------|
| Cache-Aside | <1ms | 100k+ ops/s | General caching |
| Sessions | <1ms | 100k+ ops/s | Web apps |
| Queues | <5ms | 50k+ ops/s | Job processing |
| Locks | <1ms | 10k ops/s | Critical sections |
| Rate Limiting | <1ms | 100k+ ops/s | API protection |
| Pub/Sub | <1ms | 100k+ ops/s | Real-time |
| Leaderboards | <5ms | 10k ops/s | Rankings |

## Common Mistakes

❌ **Mistake 1**: Cache without TTL
```python
# WRONG
r.set('data', value)  # Never expires!

# RIGHT
r.setex('data', 3600, value)  # 1 hour TTL
```

❌ **Mistake 2**: Ignoring cache invalidation
```python
# WRONG
r.set('user:1', cached_data)
# Database updated but cache still old!

# RIGHT
r.set('user:1', cached_data)
# On DB update:
r.delete('user:1')
```

❌ **Mistake 3**: Long-running locks
```python
# WRONG
with DistributedLock('resource'):
    time.sleep(1000)  # Lock held too long!

# RIGHT
with DistributedLock('resource', timeout=10):
    # Only 10 seconds max
```

## Related Commands

- `/redis-learn` - Master each pattern
- `/redis-optimize` - Performance tuning
- `/redis-code` - Code examples

**Ready to use Redis patterns?** Use `/redis-patterns {name}` to explore specific patterns!
