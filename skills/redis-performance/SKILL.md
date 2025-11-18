---
name: redis-performance
description: Performance tuning, memory optimization, pipelining, transactions, Lua scripting, and benchmarking for maximum Redis efficiency.
---

# Redis Performance Optimization

Maximize Redis throughput and efficiency.

## Pipelining

Send multiple commands without waiting for responses.

```python
# ❌ SLOW: Individual requests (N round trips)
for i in range(1000):
    r.set(f'key:{i}', f'value:{i}')
# Total time: 1000 * round_trip_time

# ✅ FAST: Pipelined (1 round trip)
pipe = r.pipeline()
for i in range(1000):
    pipe.set(f'key:{i}', f'value:{i}')
pipe.execute()
# Total time: 1 * round_trip_time
```

**Performance gain**: 10-100x faster for bulk operations

## Transactions

Atomic operations with MULTI/EXEC/WATCH.

```python
def transfer_money(from_user, to_user, amount):
    pipe = r.pipeline()
    while True:
        try:
            # WATCH: Monitor for changes
            pipe.watch(f'user:{from_user}:balance')

            # Get current balance
            balance = int(pipe.get(f'user:{from_user}:balance') or 0)

            if balance < amount:
                pipe.reset()
                return False

            # MULTI: Start transaction
            pipe.multi()
            pipe.decrby(f'user:{from_user}:balance', amount)
            pipe.incrby(f'user:{to_user}:balance', amount)

            # EXEC: Commit atomically
            pipe.execute()
            return True

        except redis.WatchError:
            # Retry if watched key changed
            continue
        finally:
            pipe.reset()
```

## Lua Scripting

Atomic multi-step operations.

```python
# Define Lua script for atomic check-and-set
CHECK_AND_SET_SCRIPT = """
if redis.call('get', KEYS[1]) == ARGV[1] then
    redis.call('set', KEYS[1], ARGV[2])
    return 1
else
    return 0
end
"""

script = r.register_script(CHECK_AND_SET_SCRIPT)
result = script(keys=['mykey'], args=['oldvalue', 'newvalue'])

# Complex rate limiter in Lua
RATE_LIMIT_SCRIPT = """
local current = redis.call('get', KEYS[1])
if current and tonumber(current) >= tonumber(ARGV[1]) then
    return 0
end
redis.call('incr', KEYS[1])
redis.call('expire', KEYS[1], ARGV[2])
return 1
"""

limiter = r.register_script(RATE_LIMIT_SCRIPT)
allowed = limiter(keys=[client_id], args=[100, 60])  # 100 req/60sec
```

## Memory Optimization

Reduce memory usage.

```python
# 1. Use hash instead of individual keys
# ❌ 6 keys = ~900 bytes
r.set('user:1:name', 'Alice')
r.set('user:1:email', 'alice@ex.com')
r.set('user:1:age', '25')
# And 3 more...

# ✅ 1 key = ~400 bytes
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@ex.com',
    'age': '25'
})

# 2. Use integers instead of strings
# ❌ '100' = 40 bytes
r.set('count', '100')

# ✅ 100 = 8 bytes
r.incr('count')

# 3. Compression for large values
import zlib
large_data = json.dumps(big_dict)
compressed = zlib.compress(large_data.encode())
r.set('compressed_data', compressed)

# Decompress when reading
compressed_data = r.get('compressed_data')
decompressed = zlib.decompress(compressed_data)
data = json.loads(decompressed)

# 4. Set appropriate TTL
r.setex('session:abc', 1800, session_data)  # 30 min expiry
r.setex('temp_cache:xyz', 60, cached_data)  # 1 min expiry
```

## Key Expiration

Manage data lifetime efficiently.

```python
# Set TTL
r.expire('mykey', 60)           # 60 seconds
r.expireat('mykey', timestamp)  # At specific time
r.setex('key', 3600, 'value')   # Set with TTL

# Check TTL
ttl = r.ttl('mykey')            # Seconds remaining (-1 = no expiry, -2 = missing)
pttl = r.pttl('mykey')          # Milliseconds

# Remove expiry
r.persist('mykey')              # Remove TTL

# Sliding window expiration
def extend_session_ttl(session_id, duration=1800):
    """Extend session by duration on each request"""
    r.expire(f'session:{session_id}', duration)
```

## Connection Pooling

Reuse connections efficiently.

```python
from redis import ConnectionPool

# ❌ Bad: New connection per operation
for i in range(1000):
    r = redis.Redis()
    r.set(f'key:{i}', f'value:{i}')

# ✅ Good: Connection pooling
pool = ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50
)
r = redis.Redis(connection_pool=pool)

for i in range(1000):
    r.set(f'key:{i}', f'value:{i}')
```

## Benchmarking

Measure performance.

```bash
# Official Redis benchmark
redis-benchmark -h localhost -p 6379 -c 50 -n 10000

# Test specific command
redis-benchmark -h localhost -t set,get -n 100000

# Custom test
redis-benchmark -h localhost -q --csv
```

## Slow Log Monitoring

Find performance bottlenecks.

```python
# Enable slowlog (commands slower than 10ms)
r.config_set('slowlog-log-slower-than', 10000)  # microseconds

# Get slowlog
slow_commands = r.slowlog_get(10)  # Last 10 slow commands
for entry in slow_commands:
    cmd_id, timestamp, duration, command = entry
    print(f"Command: {command}, Duration: {duration}µs")

# Clear slowlog
r.slowlog_reset()
```

## Optimization Checklist

- [ ] Use pipelining for bulk operations
- [ ] Implement connection pooling
- [ ] Use Lua scripts for atomic operations
- [ ] Monitor slowlog regularly
- [ ] Set appropriate TTLs
- [ ] Use hashes for related fields
- [ ] Compress large values
- [ ] Monitor memory usage
- [ ] Use transactions wisely
- [ ] Test with redis-benchmark

## Performance Tips

| Operation | Speed | Optimization |
|-----------|-------|--------------|
| GET/SET | ~50µs | Use pipeline |
| LPUSH/RPOP | ~50µs | Blocking ops good |
| SADD/SINTER | ~100µs | Monitor cardinality |
| ZADD/ZRANGE | ~200µs | Monitor score precision |
| HSET/HGET | ~50µs | Hash over string |
| INCR | ~50µs | Use for counters |
| EVAL (Lua) | ~100µs | Avoid N+1 queries |

## Monitoring Metrics

Track Redis health:

```python
info = r.info()
print(f"Connected clients: {info['connected_clients']}")
print(f"Memory used: {info['used_memory_human']}")
print(f"Operations/sec: {info['instantaneous_ops_per_sec']}")
print(f"Hit rate: {info['keyspace_hits']/(info['keyspace_hits']+info['keyspace_misses'])*100:.1f}%")
```

## Real-World Performance

Typical Redis performance:
- **Throughput**: 100k+ ops/sec
- **Latency**: <1ms p50, <10ms p99
- **Memory**: ~1KB per small string entry
- **Persistence**: RDB ~100k keys/sec, AOF slower
