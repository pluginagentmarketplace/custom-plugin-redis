---
description: Debug Redis issues - slow queries, memory problems, connection issues
allowed-tools: Read, Bash
sasmp_version: "1.3.0"
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  issue_type:
    type: string
    required: true
    enum: [slow, memory, connection, replication, cluster, all]
  host:
    type: string
    required: false
    default: "localhost"
  port:
    type: integer
    required: false
    default: 6379
  duration:
    type: integer
    required: false
    default: 60
    description: "Monitoring duration in seconds"
  verbose:
    type: boolean
    required: false
    default: false

# Analysis Thresholds
thresholds:
  slow_query_ms: 10
  memory_fragmentation: 1.5
  blocked_clients: 10
  replication_lag_seconds: 5
---

# /redis-debug Command

Diagnose and debug Redis issues with comprehensive analysis.

## Usage

```
/redis-debug [issue-type] [--duration 60] [--verbose]
```

## Issue Types

### slow
Analyze slow queries and performance bottlenecks.

```bash
# Slow query analysis script
#!/bin/bash

echo "=== Slow Query Analysis ==="

# Configure slow log
redis-cli CONFIG SET slowlog-log-slower-than 10000  # 10ms
redis-cli CONFIG SET slowlog-max-len 128

# Get slow log
echo ""
echo "Recent Slow Commands:"
echo "---------------------"
redis-cli SLOWLOG GET 20 | while read -r line; do
    echo "$line"
done

# Analyze patterns
echo ""
echo "Command Frequency:"
redis-cli SLOWLOG GET 100 | grep -E "^\s+[0-9]+\)" | \
    awk '{print $2}' | sort | uniq -c | sort -rn | head -10

# Check for problematic patterns
echo ""
echo "Pattern Analysis:"
echo "-----------------"

# KEYS command detection
KEYS_COUNT=$(redis-cli SLOWLOG GET 100 | grep -c "KEYS")
if [ $KEYS_COUNT -gt 0 ]; then
    echo "[CRITICAL] KEYS command detected $KEYS_COUNT times"
    echo "  FIX: Replace KEYS with SCAN"
fi

# SMEMBERS on large sets
SMEMBERS_COUNT=$(redis-cli SLOWLOG GET 100 | grep -c "SMEMBERS")
if [ $SMEMBERS_COUNT -gt 0 ]; then
    echo "[WARNING] SMEMBERS detected $SMEMBERS_COUNT times"
    echo "  FIX: Use SSCAN for large sets"
fi

# HGETALL detection
HGETALL_COUNT=$(redis-cli SLOWLOG GET 100 | grep -c "HGETALL")
if [ $HGETALL_COUNT -gt 0 ]; then
    echo "[WARNING] HGETALL detected $HGETALL_COUNT times"
    echo "  FIX: Use HMGET for specific fields"
fi
```

### memory
Analyze memory usage and detect issues.

```bash
# Memory analysis script
#!/bin/bash

echo "=== Memory Analysis ==="

# Overall memory info
echo ""
echo "Memory Overview:"
redis-cli INFO memory | grep -E "^(used_memory|maxmemory|mem_fragmentation)"

# Memory doctor
echo ""
echo "Memory Doctor:"
redis-cli MEMORY DOCTOR

# Big keys analysis
echo ""
echo "Big Keys Detection:"
echo "-------------------"
redis-cli --bigkeys 2>/dev/null | tail -20

# Sample key memory usage
echo ""
echo "Top Keys by Memory (sample):"
redis-cli SCAN 0 COUNT 100 | tail -n +2 | while read -r key; do
    SIZE=$(redis-cli MEMORY USAGE "$key" 2>/dev/null)
    if [ -n "$SIZE" ] && [ "$SIZE" -gt 1000 ]; then
        echo "  $key: $SIZE bytes"
    fi
done | sort -t: -k2 -rn | head -10

# Check eviction policy
echo ""
echo "Eviction Configuration:"
redis-cli CONFIG GET maxmemory-policy
redis-cli CONFIG GET maxmemory-samples

# Check memory fragmentation
FRAG=$(redis-cli INFO memory | grep "mem_fragmentation_ratio" | cut -d: -f2 | tr -d '\r')
echo ""
echo "Fragmentation Ratio: $FRAG"
if (( $(echo "$FRAG > 1.5" | bc -l) )); then
    echo "  [WARNING] High fragmentation detected"
    echo "  FIX: Consider MEMORY PURGE or restart during maintenance"
fi
```

### connection
Diagnose connection and client issues.

```bash
# Connection analysis script
#!/bin/bash

echo "=== Connection Analysis ==="

# Client list summary
echo ""
echo "Client Statistics:"
redis-cli INFO clients

# Detailed client list
echo ""
echo "Active Clients:"
redis-cli CLIENT LIST | head -20

# Check for blocked clients
BLOCKED=$(redis-cli INFO clients | grep "blocked_clients" | cut -d: -f2 | tr -d '\r')
echo ""
echo "Blocked Clients: $BLOCKED"
if [ "$BLOCKED" -gt 0 ]; then
    echo "  [WARNING] Clients blocked on BLPOP/BRPOP/WAIT"
    echo "  Details:"
    redis-cli CLIENT LIST | grep "flags=.*b"
fi

# Check connection limits
echo ""
echo "Connection Limits:"
redis-cli CONFIG GET maxclients
CURRENT=$(redis-cli INFO clients | grep "connected_clients" | cut -d: -f2 | tr -d '\r')
MAX=$(redis-cli CONFIG GET maxclients | tail -1)
echo "  Current: $CURRENT / $MAX"

# Check for connection issues
echo ""
echo "Rejected Connections:"
redis-cli INFO stats | grep rejected_connections

# TCP configuration
echo ""
echo "TCP Configuration:"
redis-cli CONFIG GET tcp-backlog
redis-cli CONFIG GET timeout
```

### replication
Debug replication and sync issues.

```bash
# Replication analysis script
#!/bin/bash

echo "=== Replication Analysis ==="

# Role and status
echo ""
echo "Replication Status:"
redis-cli INFO replication

# Check lag
ROLE=$(redis-cli INFO replication | grep "role:" | cut -d: -f2 | tr -d '\r')

if [ "$ROLE" = "master" ]; then
    echo ""
    echo "Master Status:"
    echo "--------------"
    redis-cli INFO replication | grep -E "^(connected_slaves|slave[0-9])"

    # Check each replica lag
    redis-cli INFO replication | grep "slave" | while read -r line; do
        LAG=$(echo "$line" | grep -o "lag=[0-9]*" | cut -d= -f2)
        if [ -n "$LAG" ] && [ "$LAG" -gt 5 ]; then
            echo "[WARNING] High replication lag: ${LAG}s"
            echo "  $line"
        fi
    done
elif [ "$ROLE" = "slave" ]; then
    echo ""
    echo "Replica Status:"
    echo "---------------"
    LINK=$(redis-cli INFO replication | grep "master_link_status" | cut -d: -f2 | tr -d '\r')
    echo "Master Link: $LINK"

    if [ "$LINK" != "up" ]; then
        echo "[CRITICAL] Master link is down!"
        echo "Diagnostics:"
        redis-cli INFO replication | grep -E "^(master_host|master_port|master_link_down_since)"
    fi

    # Check sync status
    SYNC=$(redis-cli INFO replication | grep "master_sync_in_progress" | cut -d: -f2 | tr -d '\r')
    if [ "$SYNC" = "1" ]; then
        echo "[INFO] Sync in progress"
        redis-cli INFO replication | grep "master_sync"
    fi
fi

# Replication backlog
echo ""
echo "Replication Backlog:"
redis-cli INFO replication | grep "repl_backlog"
```

### cluster
Debug Redis Cluster issues.

```bash
# Cluster analysis script
#!/bin/bash

echo "=== Cluster Analysis ==="

# Cluster info
echo ""
echo "Cluster State:"
redis-cli CLUSTER INFO

# Check if cluster is healthy
STATE=$(redis-cli CLUSTER INFO | grep "cluster_state:" | cut -d: -f2 | tr -d '\r')
if [ "$STATE" != "ok" ]; then
    echo "[CRITICAL] Cluster state is: $STATE"
fi

# Slots coverage
echo ""
echo "Slots Coverage:"
redis-cli CLUSTER SLOTS | head -30

# Check for failed nodes
echo ""
echo "Node Status:"
redis-cli CLUSTER NODES | while read -r line; do
    if echo "$line" | grep -q "fail"; then
        echo "[CRITICAL] Failed node detected:"
        echo "  $line"
    fi
done

# Check for migrating slots
echo ""
echo "Slot Migration Status:"
MIGRATING=$(redis-cli CLUSTER NODES | grep -c "migrating")
IMPORTING=$(redis-cli CLUSTER NODES | grep -c "importing")
echo "  Migrating: $MIGRATING"
echo "  Importing: $IMPORTING"

# Node health
echo ""
echo "Node Health Summary:"
redis-cli CLUSTER NODES | awk '{
    split($3, flags, ",");
    role = "unknown";
    for (i in flags) {
        if (flags[i] == "master") role = "master";
        if (flags[i] == "slave") role = "replica";
    }
    if ($3 ~ /fail/) status = "FAILED";
    else status = "OK";
    printf "  %s (%s): %s\n", $1, role, status;
}'
```

### all
Comprehensive diagnosis of all areas.

```bash
#!/bin/bash
echo "=== Comprehensive Redis Diagnosis ==="
echo "Time: $(date)"
echo ""

# Run all diagnostics
for CHECK in slow memory connection replication; do
    echo "========================================"
    echo "Running: $CHECK"
    echo "========================================"
    # Run respective check
done
```

## Diagnostic Commands Reference

### Quick Diagnostics
```redis
# Server status
INFO server
INFO stats
INFO replication
INFO cpu
INFO keyspace

# Performance
SLOWLOG GET 10
LATENCY DOCTOR
LATENCY HISTORY command

# Memory
MEMORY DOCTOR
MEMORY STATS
DEBUG OBJECT key

# Clients
CLIENT LIST
CLIENT INFO
```

### Real-time Monitoring
```bash
# Live command monitor (use briefly!)
redis-cli MONITOR

# Live stats
redis-cli --stat

# Latency monitoring
redis-cli --latency
redis-cli --latency-history
redis-cli --latency-dist

# Intrinsic latency (measure host)
redis-cli --intrinsic-latency 5
```

## Common Issues & Fixes

### Issue: High Latency Spikes

**Symptoms:**
- P99 latency >50ms occasionally
- Application timeouts

**Diagnosis:**
```bash
# Check slow log
SLOWLOG GET 20

# Check for BGSAVE
INFO persistence
# rdb_bgsave_in_progress:1 = problem

# Check AOF rewrite
INFO persistence
# aof_rewrite_in_progress:1 = problem
```

**Fixes:**
```conf
# Disable THP
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# Schedule persistence
save ""  # Disable auto-save
# Run BGSAVE via cron during low traffic

# Tune AOF
no-appendfsync-on-rewrite yes
```

### Issue: Memory Growing Unbounded

**Symptoms:**
- used_memory constantly increasing
- No eviction happening

**Diagnosis:**
```bash
# Check eviction policy
CONFIG GET maxmemory-policy
# If "noeviction", keys never removed

# Check for missing TTL
redis-cli DEBUG SLEEP 0
redis-cli SCAN 0 COUNT 100 | tail -n +2 | while read key; do
    TTL=$(redis-cli TTL "$key")
    if [ "$TTL" = "-1" ]; then
        echo "No TTL: $key"
    fi
done
```

**Fixes:**
```bash
# Set eviction policy
CONFIG SET maxmemory-policy allkeys-lru

# Add TTL to keys
EXPIRE key 3600

# Find and remove unused keys
# Use redis-cli --bigkeys first
```

### Issue: Connection Refused

**Symptoms:**
- "Connection refused" errors
- Intermittent connectivity

**Diagnosis:**
```bash
# Check max clients
CONFIG GET maxclients
INFO clients

# Check TCP backlog
CONFIG GET tcp-backlog
# Compare with: cat /proc/sys/net/core/somaxconn

# Check bind settings
CONFIG GET bind
```

**Fixes:**
```conf
# Increase max clients
maxclients 10000

# Increase TCP backlog
tcp-backlog 511
# Also: sysctl net.core.somaxconn=512

# Check firewall
ufw status
iptables -L
```

## Error Codes

| Code | Area | Description | Priority |
|------|------|-------------|----------|
| DBG001 | Slow | Query >100ms | High |
| DBG002 | Slow | KEYS command | Critical |
| DBG003 | Memory | Fragmentation >2.0 | High |
| DBG004 | Memory | OOM imminent | Critical |
| DBG005 | Connection | Max clients reached | Critical |
| DBG006 | Connection | High blocked count | Medium |
| DBG007 | Replication | Lag >10s | High |
| DBG008 | Replication | Link down | Critical |
| DBG009 | Cluster | State not OK | Critical |
| DBG010 | Cluster | Slots uncovered | Critical |

## Example Output

```
=== Redis Debug Report ===
Host: redis.example.com:6379
Time: 2025-01-15 10:30:00 UTC
Mode: all

SLOW QUERIES
------------
[CRITICAL] 3 issues found

1. KEYS * detected (8 occurrences)
   Avg time: 250ms
   FIX: Replace with SCAN

2. SMEMBERS large:set (12 occurrences)
   Avg time: 50ms
   FIX: Use SSCAN or paginate

3. HGETALL user:* (25 occurrences)
   Avg time: 30ms
   FIX: Use HMGET for specific fields

MEMORY
------
[WARNING] 1 issue found

1. Fragmentation ratio: 1.8
   FIX: Schedule MEMORY PURGE or restart

Recommendation: Consider activedefrag yes

CONNECTIONS
-----------
[OK] No issues

Clients: 48/10000
Blocked: 0

REPLICATION
-----------
[OK] No issues

Role: master
Replicas: 2 (all in sync)
Lag: 0 seconds

SUMMARY
-------
Critical: 1
High: 2
Medium: 0
Low: 0

Recommended Actions:
1. [CRITICAL] Replace KEYS with SCAN immediately
2. [HIGH] Optimize SMEMBERS usage
3. [HIGH] Switch HGETALL to HMGET
4. [MEDIUM] Schedule memory defragmentation
```
