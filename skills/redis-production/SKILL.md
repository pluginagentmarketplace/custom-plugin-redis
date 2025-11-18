---
name: redis-production
description: Production deployment, persistence (RDB/AOF), replication, Sentinel for HA, Cluster for scaling, monitoring, and disaster recovery.
---

# Redis Production Deployment

Production-grade Redis architecture.

## Persistence

Two mechanisms for durability.

### RDB (Redis Database Snapshots)

Point-in-time snapshots of data.

```
# redis.conf
save 900 1          # Save if 1 key changed in 900 sec
save 300 10         # Save if 10 keys changed in 300 sec
save 60 10000       # Save if 10000 keys changed in 60 sec

# Trigger manually
redis-cli BGSAVE    # Background save (non-blocking)
redis-cli SAVE      # Blocking save (dangerous in production)

# Check RDB status
redis-cli LASTSAVE  # Last RDB time
```

**Pros**: Compact, fast to load
**Cons**: Data loss between snapshots

### AOF (Append-Only File)

Log every write command.

```
# redis.conf
appendonly yes
appendfsync everysec       # fsync every second (balance)
# appendfsync always       # fsync every write (slowest)
# appendfsync no          # OS decides (fastest)

# Monitor AOF size
redis-cli INFO persistence | grep aof_current_size

# Rewrite AOF file
redis-cli BGREWRITEAOF     # Compact AOF file
```

**Pros**: More durable
**Cons**: Larger files, slower writes

### Hybrid Approach

Use both for maximum durability:

```conf
# redis.conf
save 900 1              # RDB snapshots
appendonly yes          # AOF for safety
appendfsync everysec    # Balance safety/performance
```

## Replication (Master-Slave)

High availability with one-way replication.

```conf
# Master - no special config needed (default)
# Slaves - redis.conf
replicaof master_ip master_port 6379

# Monitor replication
redis-cli INFO replication
```

**Master perspective**:
```
role:master
connected_slaves:2
slave0:ip=192.168.1.2,port=6379,state=online,offset=1000
slave1:ip=192.168.1.3,port=6379,state=online,offset=1000
```

**Slave perspective**:
```
role:slave
master_host:192.168.1.1
master_port:6379
master_link_status:up
```

## Redis Sentinel

Automatic failover and monitoring.

```conf
# sentinel.conf
port 26379
sentinel monitor mymaster 192.168.1.1 6379 2
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel failover-timeout mymaster 180000

# Run Sentinel
redis-sentinel sentinel.conf

# Monitor Sentinel
redis-cli -p 26379 SENTINEL masters
redis-cli -p 26379 SENTINEL slaves mymaster
```

**How it works**:
1. Sentinel monitors master health
2. If master down, detects with quorum (2+ Sentinels)
3. Elects new master from slaves
4. Updates configuration
5. Notifies clients

## Redis Cluster

Distributed Redis for horizontal scaling.

```conf
# cluster-enabled yes
# cluster-config-file nodes.conf
# cluster-node-timeout 15000
# cluster-require-full-coverage yes
```

**Setup cluster**:
```bash
# Create nodes
redis-server --port 7000 --cluster-enabled yes
redis-server --port 7001 --cluster-enabled yes
redis-server --port 7002 --cluster-enabled yes
redis-server --port 7003 --cluster-enabled yes
redis-server --port 7004 --cluster-enabled yes
redis-server --port 7005 --cluster-enabled yes

# Create cluster
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1

# Monitor cluster
redis-cli -p 7000 CLUSTER INFO
redis-cli -p 7000 CLUSTER NODES
```

## Monitoring & Alerting

Track Redis health in production.

```python
import time
from prometheus_client import Counter, Gauge, Histogram

# Metrics
redis_commands = Counter('redis_commands_total', 'Total commands')
redis_memory = Gauge('redis_memory_bytes', 'Memory usage')
redis_latency = Histogram('redis_latency_seconds', 'Command latency')

def monitor_redis():
    while True:
        try:
            info = r.info()

            # Memory
            redis_memory.set(info['used_memory'])

            # Operations
            ops_per_sec = info['instantaneous_ops_per_sec']
            print(f"Ops/sec: {ops_per_sec}")

            # Replication lag
            if info['role'] == 'slave':
                lag = info['master_repl_offset'] - info['slave_repl_offset']
                print(f"Replication lag: {lag} bytes")

            # Slowlog
            slow_commands = r.slowlog_get(5)
            if slow_commands:
                print(f"Slow commands: {slow_commands}")

            time.sleep(60)

        except Exception as e:
            print(f"Monitoring error: {e}")
```

## Backup Strategy

Regular backups for disaster recovery.

```bash
# Manual backup
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb /backup/dump-$(date +%s).rdb

# Automated backup script
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/redis"
mkdir -p $BACKUP_DIR

redis-cli BGSAVE
sleep 1
cp /var/lib/redis/dump.rdb $BACKUP_DIR/dump_$TIMESTAMP.rdb

# Keep last 7 days
find $BACKUP_DIR -name "dump_*" -mtime +7 -delete

# Remote backup
aws s3 cp $BACKUP_DIR/dump_$TIMESTAMP.rdb s3://backup-bucket/redis/
```

## Security Configuration

```conf
# redis.conf

# Password protection
requirepass "strong_password_here"

# Rename dangerous commands
rename-command FLUSHDB ""
rename-command FLUSHALL ""
rename-command KEYS ""

# ACL (Redis 6+)
acl load  # Load ACL from aclfile
acl save  # Save ACL

# TLS/SSL (Redis 6+)
port 0                          # Disable unencrypted
tls-port 6379
tls-cert-file /path/to/cert.pem
tls-key-file /path/to/key.pem
tls-ca-cert-file /path/to/ca.pem
```

## Health Checks

```python
class RedisHealthCheck:
    def __init__(self, r):
        self.r = r

    def is_healthy(self):
        try:
            # Test connectivity
            self.r.ping()

            # Check memory
            info = self.r.info()
            if info['used_memory'] > info['maxmemory'] * 0.9:
                return False

            # Check replication
            if info['role'] == 'slave':
                if info['master_link_status'] != 'up':
                    return False

            return True
        except:
            return False

    def get_metrics(self):
        info = self.r.info()
        return {
            'memory_mb': info['used_memory'] / 1024 / 1024,
            'ops_per_sec': info['instantaneous_ops_per_sec'],
            'connected_clients': info['connected_clients'],
            'role': info['role'],
            'uptime_days': info['uptime_in_seconds'] / 86400
        }
```

## Production Checklist

- [ ] Persistence configured (RDB or AOF)
- [ ] Replication enabled
- [ ] Sentinel for monitoring and failover
- [ ] Memory limits configured
- [ ] Password protection enabled
- [ ] ACLs configured (Redis 6+)
- [ ] Dangerous commands renamed/disabled
- [ ] TLS/SSL enabled
- [ ] Monitoring and alerting setup
- [ ] Backup strategy in place
- [ ] Disaster recovery tested
- [ ] Slowlog monitoring
- [ ] Regular backups (daily+)
- [ ] Load testing completed
- [ ] Client connection limits set

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| High memory | No TTL, unbounded growth | Set TTL, monitor SLOWLOG |
| Slow operations | Large values, N+1 queries | Use pipeline, optimize keys |
| Replication lag | Slow network, heavy load | Use Sentinel, tune replication |
| Data loss | No persistence | Enable RDB/AOF |
| Connection errors | Connection limit | Increase max clients |

## Scaling Strategy

1. **Single instance**: <50k ops/sec
2. **Master-Slave**: <200k ops/sec (read scaling)
3. **Sentinel**: High availability
4. **Cluster**: >1M ops/sec (write scaling)
