---
name: database-systems
description: Master SQL, PostgreSQL, MongoDB, Redis, and database optimization. Learn schema design, query optimization, indexing strategies, and caching patterns for scalable data systems.
---

# Database Systems Skill

Master relational databases (PostgreSQL, SQL), NoSQL databases (MongoDB), and caching systems (Redis).

## Quick Start

### SQL Fundamentals (50 hours)
```sql
-- CRUD operations
SELECT id, name, email FROM users WHERE active = true;
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
UPDATE users SET email = 'john.new@example.com' WHERE id = 1;
DELETE FROM users WHERE active = false;

-- Joins and aggregations
SELECT u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name
ORDER BY post_count DESC;

-- Window functions
SELECT
  name,
  salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) as rank,
  LAG(salary) OVER (ORDER BY salary DESC) as prev_salary
FROM employees;
```

### PostgreSQL Advanced (50 hours)
```sql
-- JSON/JSONB support
SELECT id, data->>'name' as name, data->'age' as age
FROM users
WHERE data @> '{"role": "admin"}'::jsonb;

-- Full-text search
SELECT id, title, ts_rank(to_tsvector(content), query) as rank
FROM posts, plainto_tsquery('database') as query
WHERE to_tsvector(content) @@ query
ORDER BY rank DESC;

-- Transactions with isolation
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Partial indexes
CREATE INDEX idx_active_users ON users(id) WHERE active = true;
```

### MongoDB Fundamentals (50 hours)
```javascript
// Document insertion
db.users.insertOne({
  _id: ObjectId(),
  name: "John",
  email: "john@example.com",
  tags: ["admin", "active"],
  profile: {
    age: 30,
    location: "NYC"
  }
});

// Query with aggregation
db.posts.aggregate([
  { $match: { published: true } },
  { $group: { _id: "$author", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
]);

// Schema validation
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "name"],
      properties: {
        email: { bsonType: "string", pattern: "^.+@.+$" },
        name: { bsonType: "string" }
      }
    }
  }
});
```

### Redis Caching (40 hours)
```python
import redis

# String operations
r = redis.Redis()
r.set('user:1', '{"name": "John"}', ex=3600)  # 1 hour TTL
user = r.get('user:1')

# List operations (queues)
r.lpush('job_queue', 'job_1', 'job_2')
job = r.rpop('job_queue')

# Set operations
r.sadd('tags', 'python', 'redis', 'database')
tags = r.smembers('tags')

# Hash operations
r.hset('user:1', mapping={'name': 'John', 'email': 'john@example.com'})
user_data = r.hgetall('user:1')

# Pub/Sub messaging
pubsub = r.pubsub()
pubsub.subscribe('notifications')
for message in pubsub.listen():
    print(f"Message: {message['data']}")

# Lua scripting for atomic operations
script = """
local count = redis.call('get', KEYS[1])
if tonumber(count) > 0 then
  redis.call('decr', KEYS[1])
  return 1
else
  return 0
end
"""
result = r.eval(script, 1, 'limit_key')
```

## Schema Design

### Relational Schema
```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Posts table with foreign key
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  content TEXT,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Index for query optimization
CREATE INDEX idx_posts_user_published ON posts(user_id, published);
```

### MongoDB Document Design
```javascript
// Embedding strategy (denormalization)
db.users.insertOne({
  _id: ObjectId(),
  email: "john@example.com",
  name: "John",
  profile: {
    age: 30,
    location: "NYC",
    bio: "Software engineer"
  },
  recentPosts: [
    { id: ObjectId(), title: "Post 1" },
    { id: ObjectId(), title: "Post 2" }
  ]
});

// Referencing strategy (normalization)
db.users.insertOne({
  _id: ObjectId(),
  email: "john@example.com",
  postIds: [ObjectId(...), ObjectId(...)]
});
```

## Query Optimization

### EXPLAIN Analysis
```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT u.id, u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;

-- Look for Sequential Scans without indexes
-- Output shows: Seq Scan, Index Scan, Hash Join, Nested Loop
```

### Indexing Strategies
```sql
-- B-tree index (default)
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_posts_user_published ON posts(user_id, published);

-- Partial index (for filtering)
CREATE INDEX idx_active_users ON users(id) WHERE active = true;

-- GiST index for spatial/range queries
CREATE INDEX idx_address_location ON addresses USING GIST(location);
```

## Data Integrity

### Constraints
```sql
-- Primary key
ALTER TABLE users ADD PRIMARY KEY (id);

-- Unique constraint
ALTER TABLE users ADD UNIQUE(email);

-- Check constraint
ALTER TABLE orders ADD CHECK (amount > 0);

-- Foreign key
ALTER TABLE posts ADD FOREIGN KEY (user_id) REFERENCES users(id);
```

## Performance Patterns

### Caching Layers
```
1. Application Cache (Redis) - 99% hit rate
2. Database Cache (query result cache)
3. Disk/SSD - persistent data
```

### Denormalization vs Normalization
```
Normalization Benefits:
- Eliminates data redundancy
- Easier updates and maintenance
- Better storage efficiency

Denormalization Benefits:
- Faster queries (fewer joins)
- Reduced computational overhead
- Better for read-heavy workloads
```

## Monitoring

### Query Performance
```sql
-- Top slow queries (PostgreSQL)
SELECT query, calls, mean_time, max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- MongoDB query profiling
db.setProfilingLevel(2);  // Profile all operations
db.system.profile.find().pretty();
```

## Best Practices

- [ ] Index frequently queried columns
- [ ] Use EXPLAIN to analyze queries
- [ ] Avoid SELECT * queries
- [ ] Use prepared statements
- [ ] Implement connection pooling
- [ ] Regular VACUUM and ANALYZE
- [ ] Monitor disk usage
- [ ] Set appropriate TTLs for caches
- [ ] Use transactions for consistency
- [ ] Test performance at scale

## Tools & Libraries

- **PostgreSQL**: psql, pgAdmin, DBeaver
- **MongoDB**: MongoDB Compass, mongosh
- **Redis**: Redis CLI, Redis Insights
- **ORMs**: Prisma, SQLAlchemy, Mongoose
- **Tools**: DataGrip, pgBench

## When to Invoke This Skill

Invoke when:
- Designing database schemas
- Optimizing queries
- Creating indexes
- Implementing caching
- Data migration
- Performance tuning
- Choosing databases
- Backup strategies
