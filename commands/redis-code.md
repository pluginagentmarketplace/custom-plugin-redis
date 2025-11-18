# /redis-code - Ready-to-Use Code Examples

Copy-paste ready examples in Python, Node.js, Java, and Go.

## Usage

```
/redis-code python
/redis-code nodejs
/redis-code java
/redis-code go
```

## Python Examples

### Setup

```python
import redis
import json
from datetime import datetime

# Basic connection
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Connection pool
from redis import ConnectionPool
pool = ConnectionPool(host='localhost', port=6379, max_connections=50)
r = redis.Redis(connection_pool=pool)

# Test connection
print(r.ping())  # True
```

### Caching

```python
def cache_function(ttl=3600):
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            result = r.get(cache_key)
            if result:
                return json.loads(result)
            result = func(*args, **kwargs)
            r.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_function(ttl=1800)
def expensive_operation(param):
    return {'result': param * 2}
```

### Session Management

```python
class SessionManager:
    def __init__(self, ttl=1800):
        self.ttl = ttl

    def create(self, user_id):
        import uuid
        sid = str(uuid.uuid4())
        r.hset(f'session:{sid}', mapping={
            'user_id': user_id,
            'created': str(datetime.now())
        })
        r.expire(f'session:{sid}', self.ttl)
        return sid

    def get(self, sid):
        data = r.hgetall(f'session:{sid}')
        if data:
            r.expire(f'session:{sid}', self.ttl)
        return data

    def destroy(self, sid):
        r.delete(f'session:{sid}')
```

### Rate Limiter

```python
class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max = max_requests
        self.window = window

    def is_allowed(self, client_id):
        key = f'ratelimit:{client_id}'
        current = r.incr(key)
        if current == 1:
            r.expire(key, self.window)
        return current <= self.max
```

### Job Queue

```python
class JobQueue:
    def enqueue(self, job_data):
        r.rpush('job_queue', json.dumps(job_data))

    def process(self):
        while True:
            result = r.brpop('job_queue', timeout=1)
            if result:
                job = json.loads(result[1])
                self.execute(job)

    def execute(self, job):
        print(f"Executing: {job}")
```

## Node.js Examples

### Setup

```javascript
const redis = require('redis');
const client = redis.createClient({
  host: 'localhost',
  port: 6379
});

client.on('connect', () => console.log('Connected'));
client.on('error', (err) => console.error(err));

// Async/await support
const { promisify } = require('util');
const getAsync = promisify(client.get).bind(client);
```

### Caching

```javascript
async function getWithCache(key, loader, ttl = 3600) {
  const cached = await getAsync(key);
  if (cached) return JSON.parse(cached);

  const value = await loader();
  client.setex(key, ttl, JSON.stringify(value));
  return value;
}

// Usage
const user = await getWithCache(
  `user:${userId}`,
  () => db.getUser(userId),
  1800
);
```

### Rate Limiter

```javascript
async function checkRateLimit(clientId, max = 100, window = 60) {
  const key = `ratelimit:${clientId}`;
  const current = await client.incr(key);

  if (current === 1) {
    await client.expire(key, window);
  }

  return current <= max;
}

// Usage in Express
app.use(async (req, res, next) => {
  const allowed = await checkRateLimit(req.ip);
  if (!allowed) return res.status(429).json({error: 'Too many requests'});
  next();
});
```

### Pub/Sub

```javascript
// Subscriber
const subscriber = redis.createClient();
subscriber.subscribe('notifications', (err, count) => {
  console.log(`Subscribed to ${count} channels`);
});

subscriber.on('message', (channel, message) => {
  console.log(`${channel}: ${message}`);
});

// Publisher
const publisher = redis.createClient();
publisher.publish('notifications', 'New message!');
```

### Queue

```javascript
async function enqueuenJob(job) {
  await client.rpush('job_queue', JSON.stringify(job));
}

async function processJobs() {
  while (true) {
    const result = await new Promise((resolve) => {
      client.brpop('job_queue', 1, (err, data) => {
        resolve(data);
      });
    });

    if (result) {
      const job = JSON.parse(result[1]);
      await executeJob(job);
    }
  }
}
```

## Java Examples

### Setup

```java
import redis.clients.jedis.*;

JedisPool pool = new JedisPool(
  new JedisPoolConfig(),
  "localhost",
  6379
);

try (Jedis jedis = pool.getResource()) {
  jedis.set("key", "value");
  String value = jedis.get("key");
}
```

### Caching

```java
public class CacheManager {
  private static final JedisPool pool = new JedisPool();

  public String getWithCache(String key, String loader) {
    try (Jedis jedis = pool.getResource()) {
      String cached = jedis.get(key);
      if (cached != null) return cached;

      String value = loader;
      jedis.setex(key, 3600, value);
      return value;
    }
  }
}
```

### Rate Limiter

```java
public class RateLimiter {
  private static final JedisPool pool = new JedisPool();

  public boolean isAllowed(String clientId, int max, int window) {
    try (Jedis jedis = pool.getResource()) {
      long current = jedis.incr("ratelimit:" + clientId);
      if (current == 1) {
        jedis.expire("ratelimit:" + clientId, window);
      }
      return current <= max;
    }
  }
}
```

### Distributed Lock

```java
public class DistributedLock {
  private static final JedisPool pool = new JedisPool();

  public synchronized void executeWithLock(String resource, Runnable task) throws Exception {
    try (Jedis jedis = pool.getResource()) {
      String lockId = UUID.randomUUID().toString();

      // Acquire
      while (jedis.set(
        "lock:" + resource,
        lockId,
        SetParams.setParams().nx().ex(10)
      ) == null) {
        Thread.sleep(10);
      }

      try {
        task.run();
      } finally {
        // Release with script
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] then redis.call('del', KEYS[1]) end";
        jedis.eval(script, 1, "lock:" + resource, lockId);
      }
    }
  }
}
```

## Go Examples

### Setup

```go
import "github.com/go-redis/redis/v8"

rdb := redis.NewClient(&redis.Options{
  Addr: "localhost:6379",
})

// Test connection
err := rdb.Ping(ctx).Err()
```

### Caching

```go
func getWithCache(ctx context.Context, key string, loader func() (string, error)) (string, error) {
  val, err := rdb.Get(ctx, key).Result()
  if err == nil {
    return val, nil
  }

  value, err := loader()
  if err != nil {
    return "", err
  }

  rdb.SetEX(ctx, key, value, time.Hour)
  return value, nil
}
```

### Rate Limiter

```go
func isAllowed(ctx context.Context, clientID string, max, window int) bool {
  key := fmt.Sprintf("ratelimit:%s", clientID)
  current, err := rdb.Incr(ctx, key).Result()

  if current == 1 {
    rdb.Expire(ctx, key, time.Duration(window)*time.Second)
  }

  return current <= int64(max)
}
```

### Queue

```go
func enqueueJob(ctx context.Context, job interface{}) error {
  data, _ := json.Marshal(job)
  return rdb.RPush(ctx, "job_queue", string(data)).Err()
}

func processJobs(ctx context.Context) {
  for {
    result := rdb.BRPop(ctx, time.Second, "job_queue")
    if result.Err() == nil {
      var job interface{}
      json.Unmarshal([]byte(result.Val()[1]), &job)
      executeJob(ctx, job)
    }
  }
}
```

## Common Patterns

All languages support these patterns:

```
1. String operations (GET, SET, INCR)
2. Hash operations (HSET, HGET, HGETALL)
3. List operations (LPUSH, RPOP, BLPOP)
4. Set operations (SADD, SMEMBERS, SINTER)
5. Sorted Set operations (ZADD, ZRANGE, ZRANK)
6. Transactions (MULTI, EXEC)
7. Pub/Sub (SUBSCRIBE, PUBLISH)
```

## Performance Tips

All languages:
- ✅ Use connection pooling
- ✅ Use pipelining for batch ops
- ✅ Use Lua scripts for atomic ops
- ✅ Handle errors gracefully
- ✅ Test with your expected load

## Library Recommendations

| Language | Library | Features |
|----------|---------|----------|
| Python | redis-py | Full-featured, async support |
| Node.js | redis | Official, async/await |
| Java | Jedis | Mature, widely used |
| Go | go-redis | Modern, type-safe |

## Related Commands

- `/redis-learn` - Understand concepts
- `/redis-patterns` - Design patterns
- `/redis-optimize` - Performance tips

**Need working code?** Use `/redis-code {language}` to get examples!
