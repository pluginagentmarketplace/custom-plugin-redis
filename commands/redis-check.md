---
description: Check Redis server health, connection status, and key metrics
allowed-tools: Read, Bash
---

# /redis-check Command

Perform a comprehensive Redis health check.

## Usage

```
/redis-check [host] [port]
```

## What It Does

1. **Connection Test**
   - Verify Redis is reachable
   - Check PING response

2. **Server Info**
   - Redis version
   - Uptime
   - Connected clients

3. **Memory Status**
   - Used memory
   - Max memory
   - Fragmentation ratio

4. **Persistence Status**
   - RDB last save time
   - AOF status
   - Rewrite status

5. **Replication Status**
   - Role (master/replica)
   - Connected replicas
   - Replication lag

## Example Output

```
Redis Health Check
==================
Status: HEALTHY
Version: 7.2.0
Uptime: 5 days, 3 hours

Memory: 256MB / 1GB (25%)
Clients: 15 connected
Keys: 150,000

Persistence: RDB + AOF
Last Save: 5 minutes ago

Replication: Master
Replicas: 2 connected
```

## Actions

- Reports issues if found
- Suggests optimizations
- Provides quick fixes
