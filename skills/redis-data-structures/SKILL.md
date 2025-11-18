---
name: redis-data-structures
description: Master all Redis data structures: strings, lists, sets, sorted sets, hashes, and streams. Learn when to use each structure and how to optimize their usage.
---

# Redis Data Structures

Master every Redis data type with practical examples and optimization tips.

## 1. Strings (Simplest & Most Versatile)

**Best for**: Caching, counters, sessions, user data, configuration

```python
import redis
r = redis.Redis()

# Basic operations
r.set('name', 'John')                    # Set value
value = r.get('name')                    # Get value
r.append('name', ' Doe')                 # Append to string
r.strlen('name')                         # Get length
r.setex('temp', 60, 'data')             # Set with TTL
r.setnx('unique', 'value')              # Set if not exists

# Counters
r.incr('page:views')                     # Increment
r.incrby('score', 10)                    # Increment by amount
r.decr('inventory')                      # Decrement
r.incrbyfloat('price', 1.99)            # Increment float

# Multiple operations
r.mset({'user:1:name': 'Alice', 'user:2:name': 'Bob'})
values = r.mget(['user:1:name', 'user:2:name'])
```

## 2. Lists (Ordered, Blocking)

**Best for**: Queues, message processing, recent items, activity feeds

```python
# Push operations
r.lpush('queue', 'job1')                 # Push to left
r.rpush('queue', 'job2')                 # Push to right
r.lpushx('queue', 'job0')                # Push only if exists

# Pop operations
r.lpop('queue')                          # Pop from left (FIFO)
r.rpop('queue')                          # Pop from right (LIFO)

# Blocking operations (perfect for queues)
job = r.blpop('queue', timeout=10)       # Block until available
r.brpoplpush('source', 'dest', 10)      # Blocking move

# Range operations
r.lrange('queue', 0, -1)                 # Get all
r.ltrim('queue', 0, 99)                  # Keep first 100
r.llen('queue')                          # Length
r.lindex('queue', 0)                     # Get by index
r.lset('queue', 0, 'new_value')         # Set by index
```

**Use case: Job Queue**
```python
# Producer
def enqueue_job(job_data):
    r.rpush('job_queue', json.dumps(job_data))

# Consumer
def process_jobs():
    while True:
        job_json = r.blpop('job_queue', timeout=1)
        if job_json:
            job = json.loads(job_json[1])
            process(job)
```

## 3. Sets (Unique, Unordered)

**Best for**: Unique items, membership checks, intersections, tags

```python
# Add/Remove
r.sadd('tags:post1', 'python', 'redis', 'database')
r.srem('tags:post1', 'python')
r.scard('tags:post1')                    # Count

# Check membership
r.sismember('tags:post1', 'redis')       # True/False
r.smembers('tags:post1')                 # Get all

# Set operations
r.sunion('tags:post1', 'tags:post2')     # Union
r.sinter('tags:post1', 'tags:post2')     # Intersection
r.sdiff('tags:post1', 'tags:post2')      # Difference

# Move between sets
r.smove('source', 'dest', 'member')

# Random operations
r.spop('tags:post1')                     # Random remove
r.srandmember('tags:post1', 3)           # Random 3 members
```

**Use case: Friend Network**
```python
# Add friends
r.sadd(f'user:{user_id}:friends', friend1, friend2, friend3)

# Check if friend
r.sismember(f'user:{user_id}:friends', other_user_id)

# Common friends
common = r.sinter(
    f'user:{user1}:friends',
    f'user:{user2}:friends'
)
```

## 4. Sorted Sets (Ordered by Score)

**Best for**: Leaderboards, rankings, time-series data, priorities

```python
# Add with score
r.zadd('leaderboard', {'Alice': 100, 'Bob': 95, 'Carol': 105})
r.zadd('leaderboard', {'Dave': 110})

# Score operations
r.zscore('leaderboard', 'Alice')         # Get score
r.zrank('leaderboard', 'Alice')          # Position (ascending)
r.zrevrank('leaderboard', 'Alice')       # Position (descending)
r.zcard('leaderboard')                   # Count

# Range operations
top_3 = r.zrevrange('leaderboard', 0, 2) # Top 3 (highest score)
bottom_3 = r.zrange('leaderboard', 0, 2) # Bottom 3 (lowest score)

with_scores = r.zrevrange('leaderboard', 0, -1, withscores=True)

# Score range
above_100 = r.zrangebyscore('leaderboard', 100, float('inf'))

# Increment score
r.zincrby('leaderboard', 5, 'Alice')     # Alice gains 5 points

# Remove
r.zrem('leaderboard', 'Dave')
r.zremrangebyrank('leaderboard', 0, 2)  # Remove bottom 3
r.zremrangebyscore('leaderboard', 0, 50) # Remove low scores
```

**Use case: Leaderboard**
```python
# Record score
def update_score(user_id, points):
    r.zadd('leaderboard:2025', {user_id: points})

# Get top 10
def get_top_10():
    return r.zrevrange('leaderboard:2025', 0, 9, withscores=True)

# Get user rank and score
def get_user_stats(user_id):
    rank = r.zrevrank('leaderboard:2025', user_id)
    score = r.zscore('leaderboard:2025', user_id)
    return {'rank': rank + 1, 'score': score}
```

## 5. Hashes (Field-Value Pairs)

**Best for**: Objects, user profiles, configurations, aggregating related data

```python
# Set fields
r.hset('user:1', mapping={'name': 'Alice', 'email': 'alice@example.com'})
r.hset('user:1', 'age', 25)              # Single field
r.hsetnx('user:1', 'city', 'NYC')        # Only if not exists

# Get fields
r.hget('user:1', 'name')                 # Single field
r.hmget('user:1', ['name', 'email'])     # Multiple fields
r.hgetall('user:1')                      # All fields
r.hkeys('user:1')                        # All field names
r.hvals('user:1')                        # All values
r.hlen('user:1')                         # Field count

# Check existence
r.hexists('user:1', 'name')              # Field exists?

# Increment
r.hincrby('user:1', 'age', 1)            # Increment age
r.hincrbyfloat('user:1', 'score', 1.5)

# Delete
r.hdel('user:1', 'city')                 # Delete field
```

**Use case: User Profile**
```python
class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.key = f'user:{user_id}'

    def set_profile(self, **kwargs):
        r.hset(self.key, mapping=kwargs)

    def get_profile(self):
        return r.hgetall(self.key)

    def update_field(self, field, value):
        r.hset(self.key, field, value)

# Usage
profile = UserProfile(1)
profile.set_profile(name='Alice', email='alice@ex.com', age=25)
print(profile.get_profile())  # All user data
```

## 6. Streams (Event Logs)

**Best for**: Event sourcing, message logs, time-series, consumer groups

```python
# Add to stream
r.xadd('events', {'user_id': '123', 'action': 'login'})
# Returns ID like: 1609459200000-0

# Read stream
events = r.xrange('events')              # All events
recent = r.xrevrange('events', count=10) # Last 10

# Consumer groups
r.xgroup_create('events', 'mygroup')     # Create group
messages = r.xreadgroup({'mygroup': '>'}, 'consumer1', count=1)

# Acknowledge processing
r.xack('events', 'mygroup', message_id)

# Get pending messages
pending = r.xpending('events', 'mygroup')
```

## Memory Optimization Tips

```python
# 1. Use appropriate data types
# ❌ WRONG: Storing list as string (JSON)
r.set('items', json.dumps(['a', 'b', 'c']))

# ✅ RIGHT: Use list type
r.rpush('items', 'a', 'b', 'c')

# 2. Compress large values
import zlib
large_json = json.dumps(huge_dict)
compressed = zlib.compress(large_json.encode())
r.set('compressed_data', compressed)

# 3. Use hashes for related fields
# ❌ WRONG: Many separate keys
r.set('user:1:name', 'Alice')
r.set('user:1:email', 'alice@ex.com')
r.set('user:1:age', 25)

# ✅ RIGHT: One hash with multiple fields
r.hset('user:1', mapping={
    'name': 'Alice',
    'email': 'alice@ex.com',
    'age': 25
})

# 4. Set TTL for temporary data
r.setex('session:abc123', 3600, json.dumps(session_data))
```

## When to Use Each Type

| Type | Use Case | Example |
|------|----------|---------|
| String | Cache, counters, simple values | Page views, user token |
| List | Queues, feeds, ordered items | Job queue, activity feed |
| Set | Unique items, tags, relationships | Tags, followers, visited IPs |
| Sorted Set | Rankings, leaderboards, time-series | Leaderboard, trending topics |
| Hash | Objects, related fields | User profile, product details |
| Stream | Event logs, message queues | Event sourcing, chat logs |

## Performance Checklist

- [ ] Use appropriate data type
- [ ] Set TTL for temporary data
- [ ] Index frequently queried fields
- [ ] Monitor memory usage
- [ ] Use pipelining for batch operations
- [ ] Avoid large values (>10MB)
- [ ] Compress if needed
- [ ] Profile with SLOWLOG
