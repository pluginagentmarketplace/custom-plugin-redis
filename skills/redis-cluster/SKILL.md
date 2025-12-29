---
name: redis-cluster
description: Master Redis Cluster - horizontal scaling, hash slots, resharding, cluster management, and distributed architecture
sasmp_version: "1.3.0"
bonded_agent: redis-clustering
bond_type: PRIMARY_BOND
---

# Redis Cluster Skill

## Cluster Overview

- 16384 hash slots distributed across nodes
- Automatic sharding
- Built-in replication
- No external dependencies

## Creating Cluster

```bash
# Create 6-node cluster (3 masters, 3 replicas)
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1
```

## Cluster Commands

```redis
CLUSTER INFO
CLUSTER NODES
CLUSTER SLOTS
CLUSTER KEYSLOT key
CLUSTER GETKEYSINSLOT slot count
```

## Resharding

```bash
# Move slots between nodes
redis-cli --cluster reshard 127.0.0.1:7000

# Add node
redis-cli --cluster add-node new_node:port existing_node:port

# Remove node
redis-cli --cluster del-node host:port node_id
```

## Multi-Key Operations

```redis
# Hash tags for same slot
SET {user:123}:name "John"
SET {user:123}:email "john@example.com"
MGET {user:123}:name {user:123}:email
```

## Assets
- `cluster-config.conf` - Cluster node configuration
- `docker-compose-cluster.yml` - Cluster with Docker

## References
- `CLUSTER_GUIDE.md` - Complete setup guide
