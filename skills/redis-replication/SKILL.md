---
name: redis-replication
description: Master Redis replication - master-replica setup, Sentinel for HA, failover handling, and read scaling patterns
sasmp_version: "1.3.0"
bonded_agent: redis-clustering
bond_type: PRIMARY_BOND
---

# Redis Replication Skill

## Master-Replica Setup

```conf
# On replica server
replicaof master_ip 6379
masterauth master_password
replica-read-only yes
```

### Dynamic Configuration
```redis
REPLICAOF master_ip 6379
REPLICAOF NO ONE  # Promote to master
```

## Redis Sentinel

Automatic failover management.

```conf
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel auth-pass mymaster password
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
```

### Sentinel Commands
```redis
SENTINEL masters
SENTINEL replicas mymaster
SENTINEL failover mymaster
SENTINEL get-master-addr-by-name mymaster
```

## Monitoring Replication

```redis
INFO replication
# role:master/slave
# connected_slaves
# master_repl_offset
# slave_repl_offset
```

## Assets
- `sentinel.conf` - Sentinel configuration
- `docker-compose-ha.yml` - HA setup with Docker

## References
- `REPLICATION_GUIDE.md` - Setup guide
