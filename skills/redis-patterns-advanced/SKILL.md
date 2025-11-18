---
name: redis-patterns-advanced
description: Production patterns: cache-aside, write-through, sessions, distributed locks, rate limiting, pub/sub, queues, and real-time features.
---

# Redis Patterns & Best Practices

Production-proven patterns for every use case.

## Pattern 1: Cache-Aside (Lazy Loading)

Application is responsible for loading data.

```python
def get_user(user_id):
    # 1. Check cache
    user = r.get(f'user:{user_id}')
    if user:
        return json.loads(user)

    # 2. Cache miss - load from database
    user = db.get_user(user_id)

    # 3. Store in cache with 1-hour TTL
    r.setex(f'user:{user_id}', 3600, json.dumps(user))

    return user

# On update: invalidate cache
def update_user(user_id, data):
    db.update_user(user_id, data)
    r.delete(f'user:{user_id}')  # Invalidate
```

**Pros**: Simple, doesn't require database sync
**Cons**: Cache miss on first request, stale data possible

## Pattern 2: Write-Through

Write to cache and database simultaneously.

```python
def update_user(user_id, data):
    # 1. Write to cache first
    r.hset(f'user:{user_id}', mapping=data)
    r.expire(f'user:{user_id}', 3600)

    # 2. Write to database
    db.update_user(user_id, data)
```

**Pros**: Cache stays synchronized
**Cons**: Slower writes, double operations

## Pattern 3: Write-Behind (Write-Back)

Write to cache immediately, database asynchronously.

```python
from celery import shared_task

def update_user(user_id, data):
    # 1. Write to cache immediately
    r.hset(f'user:{user_id}', mapping=data)

    # 2. Queue database update
    write_to_db_async.delay(user_id, data)

@shared_task
def write_to_db_async(user_id, data):
    db.update_user(user_id, data)
```

**Pros**: Fast writes
**Cons**: Potential data loss if cache crashes

## Pattern 4: Session Management

Store user sessions with TTL.

```python
class SessionManager:
    def __init__(self):
        self.prefix = 'session:'
        self.ttl = 1800  # 30 minutes

    def create_session(self, user_id):
        session_id = str(uuid.uuid4())
        session_data = {
            'user_id': str(user_id),
            'created_at': str(datetime.now()),
            'ip': request.remote_addr
        }
        r.hset(f'{self.prefix}{session_id}', mapping=session_data)
        r.expire(f'{self.prefix}{session_id}', self.ttl)
        return session_id

    def get_session(self, session_id):
        data = r.hgetall(f'{self.prefix}{session_id}')
        if data:
            # Extend TTL
            r.expire(f'{self.prefix}{session_id}', self.ttl)
        return data

    def destroy_session(self, session_id):
        r.delete(f'{self.prefix}{session_id}')
```

## Pattern 5: Distributed Locks

Prevent concurrent access to critical resources.

```python
import time
from uuid import uuid4

class DistributedLock:
    def __init__(self, key, timeout=10):
        self.key = f'lock:{key}'
        self.timeout = timeout
        self.identifier = str(uuid4())

    def acquire(self):
        """Acquire lock with unique identifier"""
        return r.set(
            self.key,
            self.identifier,
            nx=True,
            ex=self.timeout
        )

    def release(self):
        """Release lock safely using Lua script"""
        script = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """
        return r.eval(script, 1, self.key, self.identifier)

    def __enter__(self):
        while not self.acquire():
            time.sleep(0.1)
        return self

    def __exit__(self, *args):
        self.release()

# Usage
with DistributedLock('resource_id'):
    # Only one process can execute this at a time
    critical_operation()
```

## Pattern 6: Rate Limiting

Prevent abuse with token bucket algorithm.

```python
class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window

    def is_allowed(self, client_id):
        key = f'ratelimit:{client_id}'

        # Increment counter
        current = r.incr(key)

        # Set expiration on first increment
        if current == 1:
            r.expire(key, self.window)

        return current <= self.max_requests

    def get_remaining(self, client_id):
        key = f'ratelimit:{client_id}'
        current = r.get(key) or 0
        return max(0, self.max_requests - int(current))

# Usage in Flask
from flask import request, jsonify

@app.before_request
def rate_limit():
    limiter = RateLimiter(max_requests=100, window=60)
    if not limiter.is_allowed(request.remote_addr):
        return jsonify({'error': 'Too many requests'}), 429
```

## Pattern 7: Pub/Sub Messaging

Real-time message broadcasting.

```python
class PubSubMessenger:
    def publish(self, channel, message):
        """Publish message to channel"""
        subscribers = r.publish(channel, json.dumps(message))
        return subscribers  # Number of subscribers

    def subscribe(self, channel, callback):
        """Subscribe to channel and handle messages"""
        pubsub = r.pubsub()
        pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                callback(data)

# Usage
messenger = PubSubMessenger()

# Subscriber
def handle_notification(msg):
    print(f"Notification: {msg}")

# In background
def subscriber_thread():
    messenger.subscribe('notifications', handle_notification)

# Main
messenger.publish('notifications', {'type': 'alert', 'msg': 'Check now!'})
```

## Pattern 8: Queue System

Job processing with failure handling.

```python
class JobQueue:
    def __init__(self):
        self.queue = 'job_queue'
        self.processing = 'job_processing'
        self.failed = 'job_failed'

    def enqueue(self, job_data):
        """Add job to queue"""
        r.rpush(self.queue, json.dumps(job_data))

    def process_jobs(self, max_retries=3):
        """Process jobs from queue"""
        while True:
            # Blocking pop from queue
            result = r.brpoplpush(
                self.queue,
                self.processing,
                timeout=1
            )

            if not result:
                continue

            job = json.loads(result)

            try:
                self.execute_job(job)
                # Remove from processing on success
                r.lrem(self.processing, 1, result)
            except Exception as e:
                # Move to failed
                job['retries'] = job.get('retries', 0) + 1
                if job['retries'] < max_retries:
                    r.rpush(self.queue, json.dumps(job))
                else:
                    r.rpush(self.failed, json.dumps(job))
                r.lrem(self.processing, 1, result)

    def execute_job(self, job):
        print(f"Executing: {job}")
        # Job execution logic
```

## Best Practices

✅ **Do**:
- Use transactions for multi-step operations
- Set TTL for temporary data
- Monitor memory usage
- Use Lua scripts for atomic operations
- Implement circuit breakers
- Add retry logic for failures
- Monitor slowlog

❌ **Don't**:
- Store sensitive data without encryption
- Use FLUSHALL in production
- Ignore persistence
- Block operations in loops
- Store very large values
- Use synchronous blocking calls

## Common Use Cases Summary

| Use Case | Pattern | Data Structure |
|----------|---------|-----------------|
| Caching | Cache-aside | String |
| Sessions | Session manager | Hash |
| Leaderboard | Sorted set | Sorted Set |
| Job queue | Queue | List |
| Pub/Sub notifications | Pub/Sub | (Built-in) |
| Rate limiting | Token bucket | String+counter |
| Distributed lock | Lock with TTL | String |
| Unique items | Set ops | Set |
| Rankings | Score-based | Sorted Set |
