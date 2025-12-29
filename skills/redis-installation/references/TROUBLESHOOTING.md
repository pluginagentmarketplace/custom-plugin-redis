# Redis Troubleshooting Guide

## Common Issues and Solutions

### Connection Issues

#### Issue: Cannot connect to Redis server
```
Could not connect to Redis at 127.0.0.1:6379: Connection refused
```

**Solutions:**
1. Check if Redis is running:
   ```bash
   systemctl status redis-server
   # or
   ps aux | grep redis
   ```

2. Check bind address:
   ```bash
   grep "^bind" /etc/redis/redis.conf
   ```

3. Verify port:
   ```bash
   netstat -tlnp | grep 6379
   ```

#### Issue: Authentication required
```
NOAUTH Authentication required
```

**Solution:**
```bash
redis-cli -a your_password
# or
redis-cli
AUTH your_password
```

### Memory Issues

#### Issue: Redis OOM (Out of Memory)
```
OOM command not allowed when used memory > 'maxmemory'
```

**Solutions:**
1. Increase maxmemory:
   ```bash
   redis-cli CONFIG SET maxmemory 512mb
   ```

2. Configure eviction policy:
   ```bash
   redis-cli CONFIG SET maxmemory-policy allkeys-lru
   ```

3. Analyze memory usage:
   ```bash
   redis-cli MEMORY DOCTOR
   redis-cli INFO memory
   ```

### Persistence Issues

#### Issue: RDB save failed
```
Can't save in background: fork: Cannot allocate memory
```

**Solutions:**
1. Enable overcommit_memory:
   ```bash
   sudo sysctl vm.overcommit_memory=1
   # Make permanent
   echo "vm.overcommit_memory=1" | sudo tee -a /etc/sysctl.conf
   ```

2. Reduce dataset size
3. Use AOF instead of RDB

#### Issue: AOF file corruption
```
Bad file format reading the append only file
```

**Solution:**
```bash
redis-check-aof --fix appendonly.aof
```

### Performance Issues

#### Issue: High latency
**Diagnosis:**
```bash
redis-cli --latency
redis-cli SLOWLOG GET 10
```

**Solutions:**
1. Check for blocking commands
2. Review slow log
3. Enable Redis latency monitoring:
   ```bash
   redis-cli CONFIG SET latency-monitor-threshold 100
   ```

#### Issue: High CPU usage
**Diagnosis:**
```bash
redis-cli INFO stats | grep ops
redis-cli CLIENT LIST
```

**Solutions:**
1. Check for inefficient commands (KEYS *)
2. Use SCAN instead of KEYS
3. Optimize data structures

### Replication Issues

#### Issue: Replica disconnects
```
MASTER aborted replication
```

**Solutions:**
1. Check network connectivity
2. Increase repl-timeout
3. Check repl-backlog-size

### Docker-Specific Issues

#### Issue: Data not persisting
**Solution:**
```bash
docker run -d --name redis \
  -v redis-data:/data \
  redis:7-alpine redis-server --appendonly yes
```

#### Issue: Cannot connect from host
**Solution:**
```bash
# Ensure port mapping
docker run -d -p 6379:6379 redis:7-alpine
```

## Diagnostic Commands

```bash
# General health
redis-cli PING
redis-cli INFO

# Memory analysis
redis-cli MEMORY DOCTOR
redis-cli MEMORY STATS

# Performance
redis-cli SLOWLOG GET 10
redis-cli --latency

# Client connections
redis-cli CLIENT LIST

# Persistence status
redis-cli LASTSAVE
redis-cli BGREWRITEAOF
```

## Getting Help

1. Check Redis logs: `/var/log/redis/redis-server.log`
2. Redis documentation: https://redis.io/docs
3. Stack Overflow: redis tag
4. GitHub Issues: redis/redis
