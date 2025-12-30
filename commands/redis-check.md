---
description: Check Redis server health, connection status, and key metrics
allowed-tools: Read, Bash
sasmp_version: "1.3.0"
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  host:
    type: string
    required: false
    default: "localhost"
  port:
    type: integer
    required: false
    default: 6379
  auth:
    type: string
    required: false
    description: "Redis password or user:pass for ACL"
  tls:
    type: boolean
    required: false
    default: false
  verbose:
    type: boolean
    required: false
    default: false

# Retry Configuration
retry_config:
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 500

# Thresholds
thresholds:
  memory_warning_percent: 75
  memory_critical_percent: 90
  fragmentation_warning: 1.5
  fragmentation_critical: 2.0
  latency_warning_ms: 5
  latency_critical_ms: 20
  connected_clients_warning: 100
  connected_clients_critical: 500
---

# /redis-check Command

Perform a comprehensive Redis health check with production-grade diagnostics.

## Usage

```
/redis-check [host] [port] [--auth password] [--tls] [--verbose]
```

## What It Does

### 1. Connection Test
- Verify Redis is reachable
- Check PING response latency
- Validate authentication
- Test TLS connection (if enabled)

### 2. Server Info
- Redis version and mode
- Uptime and process info
- OS and architecture
- Loaded modules

### 3. Memory Status
| Metric | Warning | Critical |
|--------|---------|----------|
| Used % | >75% | >90% |
| Fragmentation | >1.5 | >2.0 |
| Peak memory | Trend | Spike |
| RSS vs used | Mismatch | Large gap |

### 4. Persistence Status
- RDB: Last save time, changes since save
- AOF: Status, rewrite progress, fsync
- Hybrid: Preamble status
- Backup verification

### 5. Replication Status
- Role (master/replica/sentinel)
- Connected replicas
- Replication lag (seconds)
- Offset delta

### 6. Performance Metrics
- Instantaneous ops/sec
- Hit ratio (if applicable)
- Rejected connections
- Expired/evicted keys

### 7. Cluster Status (if applicable)
- Cluster state (ok/fail)
- Known nodes
- Slot coverage
- Migrating slots

## Health Check Script

```bash
#!/bin/bash
# redis-health-check.sh

HOST=${1:-localhost}
PORT=${2:-6379}
AUTH=${3:-}

REDIS_CMD="redis-cli -h $HOST -p $PORT"
[ -n "$AUTH" ] && REDIS_CMD="$REDIS_CMD -a $AUTH"

echo "=== Redis Health Check ==="
echo "Host: $HOST:$PORT"
echo "Time: $(date)"
echo ""

# Connection test
echo -n "Connection: "
if $REDIS_CMD PING > /dev/null 2>&1; then
    echo "OK"
else
    echo "FAILED"
    exit 1
fi

# Get INFO
INFO=$($REDIS_CMD INFO 2>/dev/null)

# Parse key metrics
VERSION=$(echo "$INFO" | grep "redis_version:" | cut -d: -f2 | tr -d '\r')
UPTIME=$(echo "$INFO" | grep "uptime_in_seconds:" | cut -d: -f2 | tr -d '\r')
USED_MEMORY=$(echo "$INFO" | grep "used_memory_human:" | cut -d: -f2 | tr -d '\r')
MAX_MEMORY=$(echo "$INFO" | grep "maxmemory_human:" | cut -d: -f2 | tr -d '\r')
CLIENTS=$(echo "$INFO" | grep "connected_clients:" | cut -d: -f2 | tr -d '\r')
ROLE=$(echo "$INFO" | grep "role:" | cut -d: -f2 | tr -d '\r')
RDB_STATUS=$(echo "$INFO" | grep "rdb_last_bgsave_status:" | cut -d: -f2 | tr -d '\r')
AOF_ENABLED=$(echo "$INFO" | grep "aof_enabled:" | cut -d: -f2 | tr -d '\r')

# Display
echo ""
echo "Server:"
echo "  Version: $VERSION"
echo "  Uptime: $((UPTIME / 86400))d $((UPTIME % 86400 / 3600))h"
echo "  Role: $ROLE"
echo ""
echo "Memory:"
echo "  Used: $USED_MEMORY"
echo "  Max: ${MAX_MEMORY:-unlimited}"
echo ""
echo "Connections:"
echo "  Clients: $CLIENTS"
echo ""
echo "Persistence:"
echo "  RDB: $RDB_STATUS"
echo "  AOF: $([ "$AOF_ENABLED" = "1" ] && echo "enabled" || echo "disabled")"
echo ""

# Health assessment
ISSUES=0
echo "Health Assessment:"

# Memory check
MEM_FRAG=$(echo "$INFO" | grep "mem_fragmentation_ratio:" | cut -d: -f2 | tr -d '\r')
if (( $(echo "$MEM_FRAG > 2.0" | bc -l) )); then
    echo "  [CRITICAL] High memory fragmentation: $MEM_FRAG"
    ((ISSUES++))
elif (( $(echo "$MEM_FRAG > 1.5" | bc -l) )); then
    echo "  [WARNING] Memory fragmentation: $MEM_FRAG"
fi

# RDB check
if [ "$RDB_STATUS" != "ok" ]; then
    echo "  [CRITICAL] RDB save failed: $RDB_STATUS"
    ((ISSUES++))
fi

# Final status
echo ""
if [ $ISSUES -eq 0 ]; then
    echo "Status: HEALTHY"
    exit 0
else
    echo "Status: ISSUES DETECTED ($ISSUES)"
    exit 1
fi
```

## Example Output

```
=== Redis Health Check ===
Host: redis.example.com:6379
Time: 2025-01-15 10:30:00 UTC

Connection: OK

Server:
  Version: 7.2.4
  Uptime: 45d 12h
  Role: master
  Modules: search, json, timeseries

Memory:
  Used: 2.5GB / 4GB (62%)
  Peak: 3.1GB
  Fragmentation: 1.12 (OK)

Connections:
  Clients: 48 / 10000
  Blocked: 2

Persistence:
  RDB: OK (last save: 5 min ago)
  AOF: enabled (size: 1.2GB)
  Hybrid: active

Replication:
  Role: master
  Replicas: 2 connected
  Lag: 0 seconds

Performance:
  Ops/sec: 15,234
  Hit ratio: 98.5%
  Keyspace: 1,250,000 keys

Health Assessment:
  [OK] Memory usage normal
  [OK] Persistence healthy
  [OK] Replication in sync
  [OK] No slow commands detected

Status: HEALTHY
```

## Actions

### On HEALTHY
- Log metrics for trending
- Report success

### On WARNING
- Alert operations team
- Suggest optimizations
- Schedule investigation

### On CRITICAL
- Immediate alert
- Provide remediation steps
- Check runbook

## Error Codes

| Code | Status | Description | Action |
|------|--------|-------------|--------|
| CHK001 | OK | All checks passed | None |
| CHK002 | WARN | Memory >75% | Monitor closely |
| CHK003 | WARN | High fragmentation | Consider restart |
| CHK004 | CRIT | Memory >90% | Evict or scale |
| CHK005 | CRIT | Persistence failed | Check disk/logs |
| CHK006 | CRIT | Replication broken | Investigate sync |
| CHK007 | CRIT | Cluster state fail | Check nodes |

## Integration

### Prometheus Metrics Export
```bash
# Export for Prometheus
redis-cli INFO | awk -F: '/^[a-z]/ {print "redis_" $1 " " $2}'
```

### Alertmanager Rules
```yaml
- alert: RedisMemoryHigh
  expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
  for: 5m
  labels:
    severity: critical
```

### Datadog Check
```python
# datadog_checks/redis_custom.py
def check_redis_health(host, port):
    # Custom health check logic
    pass
```
