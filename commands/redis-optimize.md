# /redis-optimize - Performance Optimization

Optimize Redis for maximum performance and efficiency.

## Usage

```
/redis-optimize
/redis-optimize memory
/redis-optimize throughput
/redis-optimize latency
/redis-optimize connections
/redis-optimize persistence
```

## Quick Wins

These give **10-100x improvement**:

### 1. Use Pipelining
```python
# ❌ SLOW: 1000 round trips
for i in range(1000):
    r.set(f'key:{i}', f'value:{i}')

# ✅ FAST: 1 round trip
pipe = r.pipeline()
for i in range(1000):
    pipe.set(f'key:{i}', f'value:{i}')
pipe.execute()

# 10-100x faster
```

### 2. Use Connection Pooling
```python
# ❌ SLOW: New connection per operation
for op in operations:
    r = redis.Redis()  # New connection!
    r.get('key')

# ✅ FAST: Reuse connections
pool = ConnectionPool(max_connections=50)
r = redis.Redis(connection_pool=pool)
for op in operations:
    r.get('key')

# 5-10x faster
```

### 3. Use Hashes Instead of Multiple Keys
```python
# ❌ SLOW: 5 keys = ~500 bytes
r.set('user:1:name', 'Alice')
r.set('user:1:email', 'alice@ex.com')
r.set('user:1:age', '25')
# More operations

# ✅ FAST: 1 key = ~200 bytes
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@ex.com',
    'age': '25'
})

# 2-3x faster, 50% less memory
```

## Memory Optimization

### Memory Audit

```python
# Check memory usage
info = r.info()
print(f"Used: {info['used_memory_human']}")
print(f"Peak: {info['used_memory_peak_human']}")
print(f"Fragmentation: {info['mem_fragmentation_ratio']:.2f}")

# Slow memory analysis
for key in r.scan_iter():
    size = r.memory_usage(key)
    if size and size > 1000:
        print(f"{key}: {size} bytes")
```

### Memory Reduction Techniques

1. **Use Strings for Numbers**
   ```python
   # ❌ 40 bytes
   r.set('count', '100')

   # ✅ 8 bytes (INCR handles conversion)
   r.incr('count')
   ```

2. **Compress Large Values**
   ```python
   import zlib
   large_data = json.dumps(huge_dict)
   compressed = zlib.compress(large_data.encode())
   r.set('compressed', compressed)
   ```

3. **Set Appropriate TTLs**
   ```python
   # ❌ Data grows unbounded
   r.set('session:abc', data)

   # ✅ Auto-cleanup
   r.setex('session:abc', 1800, data)
   ```

4. **Use Sorted Set Compression**
   ```python
   # For leaderboards, use integers instead of strings
   r.zadd('leaderboard', {'user1': 100})  # ✅ Efficient
   ```

### MaxMemory Policy

```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru  # Evict LRU when full
# Options: noeviction, allkeys-lru, volatile-lru, allkeys-lfu, etc.
```

## Throughput Optimization

### Increase Throughput

1. **Batch Operations**
   ```python
   # Batch with pipeline
   pipe = r.pipeline(transaction=False)
   for item in items:
       pipe.rpush('queue', item)
   pipe.execute()
   ```

2. **Use Non-Blocking Operations**
   ```python
   # Non-blocking (better for throughput)
   r.rpush('queue', item)
   r.lpop('queue')

   # Blocking (low throughput)
   r.blpop('queue', 1)
   ```

3. **Parallel Workers**
   ```python
   from concurrent.futures import ThreadPoolExecutor

   def worker(item):
       process(item)

   with ThreadPoolExecutor(max_workers=10) as executor:
       executor.map(worker, items)
   ```

### Throughput Targets

| Scenario | Target | Configuration |
|----------|--------|-----------------|
| Single client | 100k ops/sec | Basic setup |
| 10 clients | 500k ops/sec | Pipelining |
| 50 clients | 1M+ ops/sec | Connection pool |
| Cluster | 5M+ ops/sec | Redis Cluster |

## Latency Optimization

### Find Slow Commands

```python
# Enable slowlog
r.config_set('slowlog-log-slower-than', 10000)  # 10ms

# Get slow commands
slow = r.slowlog_get(10)
for entry in slow:
    cmd_id, timestamp, duration, command = entry
    print(f"Duration: {duration}µs - {command}")
```

### Reduce Latency

1. **Avoid Large Values**
   ```python
   # ❌ 100MB value = slow network
   r.set('large', huge_json)

   # ✅ Split into smaller chunks
   for i, chunk in enumerate(chunks):
       r.set(f'large:{i}', chunk)
   ```

2. **Use Lua Scripts**
   ```python
   # ❌ Multi-trip (high latency)
   r.get('key')
   if condition:
       r.set('key', new_value)

   # ✅ Atomic (single trip)
   script = "if redis.call('get', KEYS[1]) then redis.call('set', KEYS[1], ARGV[1]) end"
   r.eval(script, 1, 'key', new_value)
   ```

3. **Reduce Network Round Trips**
   ```python
   # ❌ N round trips
   for key in keys:
       value = r.get(key)

   # ✅ 1 round trip
   values = r.mget(keys)
   ```

## Connection Optimization

### Connection Pool Configuration

```python
pool = ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,      # Adjust based on load
    socket_connect_timeout=5,
    socket_keepalive=True
)
r = redis.Redis(connection_pool=pool)
```

### Monitor Connections

```python
# Check connection info
info = r.client_list()
print(f"Connections: {len(info)}")

# Get maxclients
config = r.config_get('maxclients')
print(f"Max clients: {config['maxclients']}")

# Monitor new connections
r.info()['instantaneous_ops_per_sec']
```

## Persistence Optimization

### RDB for Backups

```conf
# redis.conf
save 900 1      # Save if 1 key changed in 900s
save 300 10     # Save if 10 keys changed in 300s
bgsave          # Background save (async)
```

### AOF for Durability

```conf
# redis.conf
appendonly yes
appendfsync everysec  # Balance: 1s loss vs performance
```

### Hybrid Approach

```conf
# Best of both worlds
save 900 1              # RDB backups
appendonly yes          # AOF safety
appendfsync everysec    # Good balance
```

## Benchmarking

### Test Performance

```bash
# Basic benchmark
redis-benchmark -h localhost -n 100000

# Test specific command
redis-benchmark -t set,get -n 1000000

# Test with pipelining
redis-benchmark -P 16 -n 100000  # Pipeline 16 commands

# Custom test
redis-benchmark -h localhost -q --csv
```

## Optimization Checklist

- [ ] Use connection pooling
- [ ] Use pipelining for batch ops
- [ ] Use hashes for related fields
- [ ] Set TTLs for temporary data
- [ ] Monitor slowlog regularly
- [ ] Compress large values
- [ ] Use Lua scripts for atomic ops
- [ ] Implement proper persistence
- [ ] Monitor memory fragmentation
- [ ] Test with actual load
- [ ] Profile with redis-benchmark

## Real-World Scenario

**Before Optimization**:
```
- Latency: 100ms average
- Throughput: 10k ops/sec
- Memory: 5GB for 100k keys
- Connections: 1000 (all new)
```

**After Optimization**:
```
- Latency: 1ms average (100x faster!)
- Throughput: 100k ops/sec (10x faster!)
- Memory: 500MB for 100k keys (10x reduction!)
- Connections: 50 (reused)
```

## Advanced Monitoring

```python
class RedisMonitor:
    def __init__(self, r):
        self.r = r

    def get_metrics(self):
        info = self.r.info()
        return {
            'ops_per_sec': info['instantaneous_ops_per_sec'],
            'connected_clients': info['connected_clients'],
            'used_memory_mb': info['used_memory'] / 1024 / 1024,
            'evicted_keys': info.get('evicted_keys', 0),
            'keyspace_hits': info['keyspace_hits'],
            'keyspace_misses': info['keyspace_misses'],
            'hit_rate': info['keyspace_hits'] / (info['keyspace_hits'] + info['keyspace_misses'])
        }
```

## Related Commands

- `/redis-learn` - Master Redis features
- `/redis-patterns` - Design patterns
- `/redis-code` - Code examples

**Ready to optimize?** Use `/redis-optimize` to start improving!
