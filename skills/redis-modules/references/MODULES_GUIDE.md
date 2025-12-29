# Redis Modules Guide

## Available Modules

| Module | Purpose | Key Commands |
|--------|---------|--------------|
| RedisJSON | JSON documents | JSON.SET, JSON.GET |
| RediSearch | Full-text search | FT.CREATE, FT.SEARCH |
| RedisTimeSeries | Time-series | TS.CREATE, TS.ADD |
| RedisBloom | Probabilistic | BF.ADD, CF.ADD |
| RedisGraph | Graph database | GRAPH.QUERY |

## Redis Stack

Pre-packaged Redis with popular modules:
- RedisJSON
- RediSearch
- RedisTimeSeries
- RedisBloom

```bash
docker run -d -p 6379:6379 redis/redis-stack:latest
```

## Use Cases

### RedisJSON
- User profiles
- Product catalogs
- Configuration storage

### RediSearch
- Product search
- Log analysis
- Document search

### RedisTimeSeries
- IoT sensor data
- Metrics storage
- Stock prices

### RedisBloom
- Duplicate detection
- Recommendation filtering
- Rate limiting

## Best Practices

1. Use Redis Stack for convenience
2. Check module compatibility
3. Monitor memory usage
4. Test performance impact
