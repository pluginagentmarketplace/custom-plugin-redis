---
description: Debug Redis issues - slow queries, memory problems, connection issues
allowed-tools: Read, Bash
---

# /redis-debug Command

Diagnose and debug Redis issues.

## Usage

```
/redis-debug [issue-type]
```

## Issue Types

### slow
- Analyze slow log
- Find expensive commands
- Suggest optimizations

### memory
- Memory analysis
- Big key detection
- Fragmentation check

### connection
- Client list analysis
- Connection issues
- Timeout problems

### replication
- Replication lag
- Sync issues
- Failover problems

### all
- Comprehensive diagnosis
- All checks

## What It Does

1. **Collects Data**
   - INFO all
   - SLOWLOG
   - CLIENT LIST
   - MEMORY DOCTOR

2. **Analyzes**
   - Pattern detection
   - Anomaly identification
   - Root cause analysis

3. **Recommends**
   - Specific fixes
   - Configuration changes
   - Best practices

## Example

```
/redis-debug slow
```

Output:
```
Slow Query Analysis
===================
Found 15 slow commands in last hour

Top Offenders:
1. KEYS * (avg 250ms) - 8 times
   FIX: Use SCAN instead

2. SMEMBERS large_set (avg 50ms) - 12 times
   FIX: Use SSCAN or limit set size

3. HGETALL big_hash (avg 30ms) - 25 times
   FIX: Use HMGET for specific fields
```
