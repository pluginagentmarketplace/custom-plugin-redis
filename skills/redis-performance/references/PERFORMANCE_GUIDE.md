# Redis Performance Guide

## Key Metrics

| Metric | Healthy Range | Check |
|--------|---------------|-------|
| Memory fragmentation | 1.0-1.5 | INFO memory |
| Hit rate | >90% | hits/(hits+misses) |
| Evictions | Low/stable | INFO stats |
| Slow commands | <10/min | SLOWLOG |
| Connected clients | <maxclients | INFO clients |

## Common Issues

### High Memory Fragmentation
- Enable active defrag
- Restart Redis (last resort)

### Low Hit Rate
- Review TTLs
- Check key patterns
- Warm cache

### Slow Commands
- Avoid KEYS *
- Use SCAN
- Check big keys

## Optimization Tips

1. Use pipelining
2. Use appropriate data structures
3. Set TTLs aggressively
4. Monitor and alert
5. Scale horizontally if needed

## Benchmarking

```bash
# Baseline
redis-benchmark -q -n 100000

# With realistic data
redis-benchmark -t set,get -d 1024 -n 100000

# Pipeline effect
redis-benchmark -t set -P 16 -n 100000
```
