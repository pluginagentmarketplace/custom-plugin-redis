---
description: Generate optimized Redis configuration for your use case
allowed-tools: Read, Write, Bash
---

# /redis-config Command

Generate optimized Redis configuration.

## Usage

```
/redis-config [use-case]
```

## Available Use Cases

### cache
- High-performance caching
- Aggressive eviction
- Memory-optimized

### session
- Session storage
- TTL-based expiry
- Persistence enabled

### queue
- Message queue
- AOF persistence
- Reliable delivery

### analytics
- Real-time analytics
- Time-series ready
- High throughput

### production
- Balanced configuration
- HA-ready
- Security hardened

## What It Generates

1. **redis.conf**
   - Optimized settings
   - Comments explaining choices

2. **docker-compose.yml** (optional)
   - Ready-to-run setup
   - Volume configuration

3. **sentinel.conf** (if HA requested)
   - Sentinel configuration
   - Failover settings

## Example

```
/redis-config cache
```

Generates:
- `redis-cache.conf`
- Memory: 1GB, eviction: allkeys-lru
- Persistence: RDB only
- No authentication (add manually)
