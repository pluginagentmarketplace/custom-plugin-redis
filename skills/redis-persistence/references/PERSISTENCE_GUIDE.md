# Redis Persistence Guide

## Strategy Comparison

| Aspect | RDB Only | AOF Only | Hybrid |
|--------|----------|----------|--------|
| Data Loss | Minutes | Seconds | Seconds |
| Startup | Fast | Slow | Fast |
| Disk I/O | Low | Higher | Medium |
| Recommended | Backups | Durability | Production |

## Choosing Strategy

### Use RDB Only When:
- Data loss of minutes is acceptable
- Need fast restarts
- Memory-constrained environment

### Use AOF Only When:
- Minimal data loss required
- Can afford slower restarts
- Write-heavy workload

### Use Hybrid When:
- Production environment
- Need both durability and fast restart
- Redis 4.0+

## Backup Best Practices

1. **Schedule regular backups**
   - Hourly for critical data
   - Daily minimum

2. **Test restore process**
   - Verify backups work
   - Measure recovery time

3. **Off-site storage**
   - S3, GCS, or similar
   - Different region/datacenter

4. **Monitor backup success**
   - Alert on failures
   - Check backup sizes

## Recovery Steps

```bash
# Stop Redis
systemctl stop redis

# Replace data files
cp /backup/dump.rdb /var/lib/redis/

# Start Redis
systemctl start redis

# Verify
redis-cli PING
```
