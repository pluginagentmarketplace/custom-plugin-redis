# Redis Cluster Guide

## Hash Slot Distribution

- 16384 slots total
- CRC16(key) mod 16384 = slot
- Use hash tags `{tag}` for co-location

## Minimum Setup

- 3 master nodes (minimum)
- 1 replica per master (recommended)
- Total: 6 nodes for production

## Commands Not Supported

- Multi-key across slots (without hash tags)
- SELECT (single database)
- KEYS (use SCAN)

## Failover Scenarios

### Manual Failover
```redis
CLUSTER FAILOVER
```

### Force Failover
```redis
CLUSTER FAILOVER FORCE
```

## Scaling

### Add Master
```bash
redis-cli --cluster add-node new:port existing:port
redis-cli --cluster reshard existing:port
```

### Add Replica
```bash
redis-cli --cluster add-node new:port existing:port --cluster-slave
```
