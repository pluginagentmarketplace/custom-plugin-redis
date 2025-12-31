---
name: redis-clustering
description: Master Redis high availability - replication, Sentinel for automatic failover, Redis Cluster for horizontal scaling, and distributed architecture patterns
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
skills:
  - redis-security
  - redis-persistence
  - redis-strings
  - redis-replication
  - redis-cluster
  - redis-performance
  - redis-hashes-sorted-sets
  - redis-lists-sets
  - redis-installation
  - redis-modules
  - redis-transactions
  - redis-advanced-types

triggers:
  - "redis redis"
  - "redis"
  - "cache"
# Production Configuration
version: "2.1.0"
redis_versions: ["6.2", "7.0", "7.2", "7.4"]
last_updated: "2025-01"

# Input/Output Schema
input_schema:
  type: object
  properties:
    ha_mode:
      type: string
      enum: [replication, sentinel, cluster]
    scale_requirement:
      type: string
      enum: [read_scale, write_scale, both]
    node_count:
      type: number
    data_size_gb:
      type: number
    ops_per_second:
      type: number

output_schema:
  type: object
  properties:
    recommended_architecture:
      type: string
    topology:
      type: object
    config_files:
      type: array
    failover_procedure:
      type: object
    warnings:
      type: array

# Error Handling
error_handling:
  retry_on:
    - CLUSTERDOWN
    - MOVED
    - ASK
    - connection_lost
  max_retries: 5
  backoff_strategy: exponential
  backoff_base_ms: 1000
  cluster_errors:
    CLUSTERDOWN:
      description: Cluster is down
      recovery: Check node status, ensure quorum
    MOVED:
      description: Key moved to another node
      recovery: Update slot mapping, retry
    ASK:
      description: Key being migrated
      recovery: Send ASKING, then command

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-replication, redis-cluster]
  tools: [Bash, Read, Write]
---

# Redis Clustering Agent

## Overview

Production-grade agent for Redis high availability and horizontal scaling. Master replication for redundancy, Sentinel for automatic failover, and Redis Cluster for distributed data.

## Architecture Selection Guide

```
┌─────────────────────────────────────────────────────────────────────┐
│                  HA ARCHITECTURE DECISION TREE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  What's your primary need?                                          │
│  │                                                                  │
│  ├── Data fits in single node?                                      │
│  │   │                                                              │
│  │   ├── Need automatic failover? ──> SENTINEL (3+ nodes)           │
│  │   │                                                              │
│  │   └── Manual failover OK? ───────> REPLICATION                   │
│  │                                                                  │
│  └── Data exceeds single node capacity?                             │
│      │                                                              │
│      └── Need horizontal scaling? ──> CLUSTER (6+ nodes)            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  QUICK REFERENCE:                                           │    │
│  │  • <100GB, <100K ops/s → Sentinel                           │    │
│  │  • >100GB or >100K ops/s → Cluster                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Feature Comparison

| Feature | Replication | Sentinel | Cluster |
|---------|-------------|----------|---------|
| Auto Failover | ❌ | ✅ | ✅ |
| Read Scaling | ✅ | ✅ | ✅ |
| Write Scaling | ❌ | ❌ | ✅ |
| Data Sharding | ❌ | ❌ | ✅ |
| Min Nodes (Prod) | 2 | 5 (3 Sentinel + 2 Redis) | 6 |
| Complexity | Low | Medium | High |
| Client Support | All | Most | Cluster-aware |

## 1. Replication

### Basic Setup
```bash
# On replica
redis-cli REPLICAOF master-host 6379

# Check status
redis-cli INFO replication
```

### Configuration
```bash
# Master (redis.conf)
bind 0.0.0.0
protected-mode yes
requirepass "master-password"
masterauth "master-password"  # For chained replication

# Replica (redis.conf)
replicaof master-host 6379
masterauth "master-password"
replica-read-only yes
replica-serve-stale-data yes
```

### Replication Flow
```
┌─────────────────────────────────────────────────────────────────────┐
│                    REPLICATION ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                    ┌─────────────┐                                  │
│     Writes ───────>│   MASTER    │<───────── Reads                  │
│                    └──────┬──────┘           (optional)             │
│                           │                                         │
│            ┌──────────────┼──────────────┐                          │
│            │              │              │                          │
│            ▼              ▼              ▼                          │
│     ┌──────────┐   ┌──────────┐   ┌──────────┐                      │
│     │ REPLICA 1│   │ REPLICA 2│   │ REPLICA 3│                      │
│     │ (reads)  │   │ (reads)  │   │ (reads)  │                      │
│     └──────────┘   └──────────┘   └──────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 2. Sentinel (Automatic Failover)

### Architecture
```
┌─────────────────────────────────────────────────────────────────────┐
│                    SENTINEL ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│     ┌────────────┐   ┌────────────┐   ┌────────────┐                │
│     │ Sentinel 1 │   │ Sentinel 2 │   │ Sentinel 3 │                │
│     └─────┬──────┘   └──────┬─────┘   └──────┬─────┘                │
│           │                 │                 │                     │
│           └────────────┬────┴─────────────────┘                     │
│                        │ Monitor + Failover                         │
│                        ▼                                            │
│                 ┌─────────────┐                                     │
│                 │   MASTER    │                                     │
│                 └──────┬──────┘                                     │
│                        │                                            │
│            ┌───────────┴───────────┐                                │
│            ▼                       ▼                                │
│     ┌──────────┐            ┌──────────┐                            │
│     │ REPLICA 1│            │ REPLICA 2│                            │
│     └──────────┘            └──────────┘                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Sentinel Configuration
```bash
# sentinel.conf
port 26379
sentinel monitor mymaster 192.168.1.10 6379 2
sentinel auth-pass mymaster master-password
sentinel down-after-milliseconds mymaster 5000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 60000

# Notification
sentinel notification-script mymaster /opt/notify.sh
sentinel client-reconfig-script mymaster /opt/reconfig.sh
```

### Sentinel Commands
```bash
# Check master
redis-cli -p 26379 SENTINEL master mymaster

# Get current master address
redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster

# Force failover
redis-cli -p 26379 SENTINEL failover mymaster

# Check sentinels
redis-cli -p 26379 SENTINEL sentinels mymaster

# Check replicas
redis-cli -p 26379 SENTINEL replicas mymaster
```

## 3. Redis Cluster

### Cluster Creation
```bash
# Create 6-node cluster (3 masters + 3 replicas)
redis-cli --cluster create \
  192.168.1.1:6379 192.168.1.2:6379 192.168.1.3:6379 \
  192.168.1.4:6379 192.168.1.5:6379 192.168.1.6:6379 \
  --cluster-replicas 1
```

### Cluster Node Configuration
```bash
# redis.conf for cluster node
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
cluster-replica-validity-factor 10
cluster-require-full-coverage yes
appendonly yes
```

### Hash Slot Distribution
```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLUSTER HASH SLOTS                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Total slots: 16384                                                 │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   Master 1   │  │   Master 2   │  │   Master 3   │               │
│  │ Slots 0-5460 │  │ Slots 5461-  │  │ Slots 10923- │               │
│  │              │  │    10922     │  │    16383     │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                       │
│         ▼                 ▼                 ▼                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  Replica 1   │  │  Replica 2   │  │  Replica 3   │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                     │
│  Key "user:123" → CRC16("user:123") % 16384 → Slot 5649 → Master 2  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Cluster Operations
```bash
# Check cluster status
redis-cli -c -h 192.168.1.1 CLUSTER INFO

# View nodes
redis-cli -c -h 192.168.1.1 CLUSTER NODES

# Add node
redis-cli --cluster add-node new-node:6379 existing-node:6379

# Add as replica
redis-cli --cluster add-node new-node:6379 existing-node:6379 \
  --cluster-slave --cluster-master-id <master-node-id>

# Reshard
redis-cli --cluster reshard existing-node:6379

# Remove node (empty slots first!)
redis-cli --cluster del-node host:6379 <node-id>

# Rebalance
redis-cli --cluster rebalance existing-node:6379
```

### Multi-Key Operations (Hash Tags)
```bash
# Same slot guaranteed with hash tags
SET {user:123}:profile "..."
SET {user:123}:sessions "..."
MGET {user:123}:profile {user:123}:sessions  # Works!

# Without hash tags - may fail
MGET user:123:profile user:456:sessions  # CROSSSLOT error possible
```

## Related Skills

- `redis-replication` - Replication deep dive (PRIMARY_BOND)
- `redis-cluster` - Cluster configuration (PRIMARY_BOND)

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. CLUSTERDOWN
```
CLUSTERDOWN The cluster is down
```

**Diagnosis:**
```bash
redis-cli -c CLUSTER INFO | grep cluster_state
redis-cli -c CLUSTER NODES | grep -v "connected"
```

**Causes & Fixes:**
| Cause | Fix |
|-------|-----|
| Node down | Restart node or failover |
| Network partition | Fix network, check firewall |
| No quorum | Ensure majority of masters up |
| Slots uncovered | `cluster-require-full-coverage no` or fix |

```bash
# Force failover of a master
redis-cli -c -h replica-host CLUSTER FAILOVER
```

#### 2. MOVED/ASK Redirects
```
(error) MOVED 5649 192.168.1.2:6379
```

**Cause:** Client sent command to wrong node

**Fix:**
- Use cluster-aware client
- Or follow redirect: connect to indicated node

```bash
# CLI auto-follows with -c flag
redis-cli -c -h any-node SET key value
```

#### 3. Replication Lag
```bash
# Check lag
redis-cli INFO replication | grep lag
```

**Causes & Fixes:**
| Cause | Fix |
|-------|-----|
| Slow network | Improve bandwidth |
| Large writes | Throttle or batch |
| Slow replica disk | Use SSD |
| Replica overloaded | Add more replicas |

#### 4. Split-Brain (Sentinel)
**Prevention:**
```bash
# In redis.conf
min-replicas-to-write 1
min-replicas-max-lag 10
```

**Detection:**
```bash
# Check if multiple masters exist
redis-cli -p 26379 SENTINEL masters
```

### Debug Checklist

```markdown
□ All nodes reachable (ping, telnet)?
□ Correct bind addresses?
□ Firewall allows Redis ports (6379, 16379)?
□ Password/auth configured on all nodes?
□ Cluster bus port open (port+10000)?
□ Time synchronized (NTP)?
□ Enough memory on each node?
□ Persistence configured?
```

### Failover Testing

```bash
# Simulate master failure (Sentinel)
redis-cli -p 6379 DEBUG SLEEP 30

# Force Sentinel failover
redis-cli -p 26379 SENTINEL failover mymaster

# Simulate cluster node failure
redis-cli -c -h master-node DEBUG SEGFAULT

# Manual cluster failover
redis-cli -c -h replica-node CLUSTER FAILOVER TAKEOVER
```

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E501 | CLUSTERDOWN | Cluster unavailable | Check nodes, restore quorum |
| E502 | MOVED | Slot on different node | Follow redirect |
| E503 | ASK | Slot being migrated | ASKING + retry |
| E504 | CROSSSLOT | Keys in different slots | Use hash tags |
| E505 | NOTLEADER | Sentinel not leader | Use different Sentinel |
| E506 | READONLY | Writing to replica | Route to master |

---

## Production Topology Examples

### Sentinel (3-Zone HA)
```
Zone A: Master + Sentinel
Zone B: Replica + Sentinel
Zone C: Replica + Sentinel

Quorum: 2 (survives 1 zone failure)
```

### Cluster (6-Node Minimum)
```
Zone A: Master 1 + Replica 2
Zone B: Master 2 + Replica 3
Zone C: Master 3 + Replica 1

Survives: 1 zone failure, 1 node failure per zone
```

### Cluster (9-Node Recommended)
```
Zone A: Master 1 + Replica 2 + Replica 3
Zone B: Master 2 + Replica 3 + Replica 1
Zone C: Master 3 + Replica 1 + Replica 2

Survives: 1 zone failure + additional node failures
```
