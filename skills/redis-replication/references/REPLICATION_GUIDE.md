# Redis Replication Guide

## Architecture Options

### 1. Simple Replication
```
Master → Replica
```
- Manual failover
- Read scaling

### 2. Sentinel HA
```
Master → Replica₁, Replica₂
   ↑
Sentinel₁, Sentinel₂, Sentinel₃
```
- Automatic failover
- Quorum-based decisions

## Failover Process

1. Sentinel detects master down
2. Quorum agrees on failure
3. Sentinel elects new master
4. Reconfigures replicas
5. Notifies clients

## Client Configuration

```python
from redis.sentinel import Sentinel

sentinel = Sentinel([
    ('sentinel1', 26379),
    ('sentinel2', 26379),
    ('sentinel3', 26379)
])

master = sentinel.master_for('mymaster')
replica = sentinel.slave_for('mymaster')
```

## Best Practices

1. Use odd number of Sentinels (3, 5)
2. Distribute across failure domains
3. Monitor replication lag
4. Test failover regularly
