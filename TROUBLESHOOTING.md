# Redis Plugin Troubleshooting Guide

> Production-grade troubleshooting reference for the Redis Development Assistant Plugin

## Quick Diagnostic Commands

```bash
# Connection test
redis-cli PING

# Full health check
redis-cli INFO

# Memory analysis
redis-cli MEMORY DOCTOR

# Slow query log
redis-cli SLOWLOG GET 10

# Latency check
redis-cli --latency

# Big keys detection
redis-cli --bigkeys
```

---

## Common Issues by Category

### 1. Connection Issues

#### Cannot Connect to Redis

**Symptoms:**
```
Could not connect to Redis at 127.0.0.1:6379: Connection refused
```

**Diagnosis:**
```bash
# Check if Redis is running
systemctl status redis
ps aux | grep redis

# Check port
netstat -tlnp | grep 6379
ss -tlnp | grep 6379

# Check bind configuration
redis-cli CONFIG GET bind
```

**Solutions:**
| Cause | Fix |
|-------|-----|
| Redis not running | `systemctl start redis` |
| Wrong port | Check `redis.conf` port setting |
| Bind to wrong IP | Set `bind 0.0.0.0` or correct IP |
| Firewall blocking | `ufw allow 6379` |

#### Authentication Failed

**Symptoms:**
```
NOAUTH Authentication required
WRONGPASS invalid username-password pair
```

**Solutions:**
```bash
# Legacy auth
redis-cli -a your_password

# ACL auth (Redis 6+)
redis-cli --user username --pass password

# Check ACL users
redis-cli ACL LIST
```

#### TLS Connection Failed

**Symptoms:**
```
SSL_connect: certificate verify failed
```

**Diagnosis:**
```bash
# Verify certificate
openssl x509 -in redis.crt -noout -dates

# Test TLS connection
openssl s_client -connect redis.example.com:6379
```

**Solutions:**
```bash
# Connect with TLS
redis-cli --tls \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  --cacert /path/to/ca.crt
```

---

### 2. Memory Issues

#### Out of Memory (OOM)

**Symptoms:**
```
OOM command not allowed when used memory > 'maxmemory'
```

**Diagnosis:**
```redis
INFO memory
# Check: used_memory, maxmemory, maxmemory_policy
```

**Solutions:**
```redis
# Increase maxmemory
CONFIG SET maxmemory 8gb

# Enable eviction
CONFIG SET maxmemory-policy allkeys-lru

# Find and remove big keys
redis-cli --bigkeys
DEL big:key:name
```

#### High Memory Fragmentation

**Symptoms:**
- `mem_fragmentation_ratio` > 1.5
- High RSS with lower used_memory

**Diagnosis:**
```redis
INFO memory
# Check mem_fragmentation_ratio
```

**Solutions:**
```redis
# Active defragmentation (Redis 4.0+)
CONFIG SET activedefrag yes
CONFIG SET active-defrag-threshold-lower 10

# Manual purge
MEMORY PURGE

# Last resort: restart during maintenance window
```

#### Memory Leak Suspicion

**Diagnosis:**
```bash
# Track memory over time
while true; do
  redis-cli INFO memory | grep used_memory_human
  sleep 60
done
```

**Solutions:**
- Check for missing TTL on cache keys
- Review APPEND operations on strings
- Check for unbounded list/stream growth

---

### 3. Performance Issues

#### Slow Commands

**Diagnosis:**
```redis
# Configure slow log
CONFIG SET slowlog-log-slower-than 10000

# Get slow commands
SLOWLOG GET 20
```

**Common Slow Commands & Fixes:**

| Command | Issue | Fix |
|---------|-------|-----|
| `KEYS *` | O(N) scan | Use `SCAN` |
| `SMEMBERS` | Large set | Use `SSCAN` |
| `HGETALL` | Large hash | Use `HMGET` |
| `LRANGE 0 -1` | Full list | Paginate |
| `SORT` | Complex sort | Pre-compute |

#### High Latency

**Diagnosis:**
```bash
# Check latency
redis-cli --latency
redis-cli --latency-history

# Intrinsic latency (host baseline)
redis-cli --intrinsic-latency 10

# Latency doctor
redis-cli LATENCY DOCTOR
```

**Common Causes & Fixes:**

| Cause | Symptom | Fix |
|-------|---------|-----|
| BGSAVE | Periodic spikes | Schedule off-peak |
| AOF fsync | Write latency | `appendfsync everysec` |
| THP | Random spikes | Disable THP |
| Network | Consistent high | Check network |
| Swap | Severe spikes | Disable swap |

**Disable Transparent Huge Pages:**
```bash
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
```

---

### 4. Persistence Issues

#### RDB Save Failing

**Symptoms:**
```
Background saving error
Can't save in background: fork: Cannot allocate memory
```

**Solutions:**
```bash
# Enable overcommit
echo 1 > /proc/sys/vm/overcommit_memory
echo "vm.overcommit_memory=1" >> /etc/sysctl.conf

# Check disk space
df -h /var/lib/redis

# Verify permissions
ls -la /var/lib/redis
```

#### AOF Corruption

**Symptoms:**
```
Bad file format reading the append only file
```

**Solutions:**
```bash
# Check and repair
redis-check-aof --fix appendonly.aof

# Verify fix
redis-check-aof appendonly.aof
```

#### RDB Corruption

**Solutions:**
```bash
# Verify RDB file
redis-check-rdb dump.rdb

# Restore from backup
cp /backup/dump.rdb /var/lib/redis/dump.rdb
chown redis:redis /var/lib/redis/dump.rdb
```

---

### 5. Replication Issues

#### Replica Not Syncing

**Diagnosis:**
```redis
INFO replication
# Check: master_link_status, master_sync_in_progress
```

**Solutions:**

| Issue | Fix |
|-------|-----|
| master_link_status: down | Check network connectivity |
| MASTERAUTH mismatch | Verify password |
| Timeout during sync | Increase `repl-timeout` |
| Disk too slow | Increase `repl-diskless-sync-delay` |

#### High Replication Lag

**Diagnosis:**
```redis
# On master
INFO replication
# Check slave0:...,lag=N

# On replica
INFO replication
# Check master_last_io_seconds_ago
```

**Solutions:**
```conf
# Increase output buffer
client-output-buffer-limit replica 512mb 128mb 60

# Use diskless replication
repl-diskless-sync yes
```

---

### 6. Cluster Issues

#### Cluster State Not OK

**Diagnosis:**
```redis
CLUSTER INFO
# Check cluster_state

CLUSTER NODES
# Check for failed nodes
```

**Solutions:**
```redis
# Fix slots
CLUSTER FIX

# Manual slot assignment
CLUSTER ADDSLOTS 0 1 2 3...

# Forget failed node
CLUSTER FORGET node-id

# Add new node
CLUSTER MEET ip port
```

#### Slot Migration Stuck

**Diagnosis:**
```redis
CLUSTER NODES | grep migrating
CLUSTER NODES | grep importing
```

**Solutions:**
```redis
# Complete migration
CLUSTER SETSLOT slot-number NODE node-id

# Abort migration
CLUSTER SETSLOT slot-number STABLE
```

---

## Debug Checklists

### Pre-Production Checklist

```markdown
□ maxmemory set appropriately
□ maxmemory-policy configured
□ Persistence strategy defined
□ Password/ACL configured
□ bind set correctly
□ protected-mode yes (or configured)
□ THP disabled
□ vm.overcommit_memory=1
□ Backup strategy in place
□ Monitoring configured
```

### Performance Investigation

```markdown
□ Check SLOWLOG GET 10
□ Run redis-cli --latency
□ Check INFO memory fragmentation
□ Verify no KEYS/SMEMBERS on large keys
□ Check client-side connection pooling
□ Review network latency
□ Check persistence impact
□ Verify no swap usage
```

### Replication Investigation

```markdown
□ Check INFO replication on all nodes
□ Verify network between master/replica
□ Check master_link_status
□ Review replication buffer size
□ Check for partial resync failures
□ Verify diskless sync if large dataset
```

---

## Error Code Reference

### Connection Errors

| Code | Description | Action |
|------|-------------|--------|
| CONN001 | Connection refused | Check Redis running |
| CONN002 | Connection timeout | Check network/firewall |
| CONN003 | TLS handshake failed | Verify certificates |

### Authentication Errors

| Code | Description | Action |
|------|-------------|--------|
| AUTH001 | NOAUTH | Provide password |
| AUTH002 | WRONGPASS | Check credentials |
| AUTH003 | NOPERM | Check ACL |

### Memory Errors

| Code | Description | Action |
|------|-------------|--------|
| MEM001 | OOM | Increase maxmemory/enable eviction |
| MEM002 | Fragmentation | Enable activedefrag |
| MEM003 | Fork failed | Enable overcommit |

### Persistence Errors

| Code | Description | Action |
|------|-------------|--------|
| PERS001 | RDB save failed | Check disk/permissions |
| PERS002 | AOF corrupt | redis-check-aof --fix |
| PERS003 | Disk full | Free space |

### Replication Errors

| Code | Description | Action |
|------|-------------|--------|
| REPL001 | Link down | Check network |
| REPL002 | Sync timeout | Increase timeout |
| REPL003 | Buffer overflow | Increase buffer |

### Cluster Errors

| Code | Description | Action |
|------|-------------|--------|
| CLUS001 | State fail | Check failed nodes |
| CLUS002 | Slots uncovered | Assign slots |
| CLUS003 | Migration stuck | SETSLOT STABLE |

---

## Getting Help

### Collect Diagnostic Information

```bash
#!/bin/bash
# collect-redis-diagnostics.sh

OUTPUT_DIR="redis-diagnostics-$(date +%Y%m%d_%H%M%S)"
mkdir -p $OUTPUT_DIR

# Basic info
redis-cli INFO ALL > $OUTPUT_DIR/info.txt
redis-cli CONFIG GET "*" > $OUTPUT_DIR/config.txt
redis-cli SLOWLOG GET 100 > $OUTPUT_DIR/slowlog.txt
redis-cli CLIENT LIST > $OUTPUT_DIR/clients.txt

# Memory
redis-cli MEMORY DOCTOR > $OUTPUT_DIR/memory-doctor.txt
redis-cli MEMORY STATS > $OUTPUT_DIR/memory-stats.txt

# Latency
redis-cli LATENCY DOCTOR > $OUTPUT_DIR/latency-doctor.txt 2>/dev/null

# Cluster (if applicable)
redis-cli CLUSTER INFO > $OUTPUT_DIR/cluster-info.txt 2>/dev/null
redis-cli CLUSTER NODES > $OUTPUT_DIR/cluster-nodes.txt 2>/dev/null

echo "Diagnostics collected in: $OUTPUT_DIR"
tar -czf $OUTPUT_DIR.tar.gz $OUTPUT_DIR
```

### Resources

- [Redis Documentation](https://redis.io/documentation)
- [Redis GitHub Issues](https://github.com/redis/redis/issues)
- [Redis Discord](https://discord.gg/redis)
