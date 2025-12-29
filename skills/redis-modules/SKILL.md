---
name: redis-modules
description: Master Redis modules - RedisJSON, RediSearch, RedisTimeSeries, RedisBloom, and extending Redis functionality
sasmp_version: "1.3.0"
bonded_agent: redis-production
bond_type: SECONDARY_BOND
---

# Redis Modules Skill

## RedisJSON

JSON document storage and manipulation.

```redis
JSON.SET user:1 $ '{"name":"John","age":30}'
JSON.GET user:1 $.name
JSON.NUMINCRBY user:1 $.age 1
JSON.ARRAPPEND user:1 $.tags '"redis"'
```

## RediSearch

Full-text search and secondary indexing.

```redis
FT.CREATE idx:users ON JSON PREFIX 1 user: SCHEMA $.name AS name TEXT $.email AS email TAG

FT.SEARCH idx:users "@name:John"
FT.SEARCH idx:users "@email:{john@example.com}"
```

## RedisTimeSeries

Time-series data storage and queries.

```redis
TS.CREATE sensor:temp RETENTION 86400000 LABELS type temperature
TS.ADD sensor:temp * 25.5
TS.RANGE sensor:temp - + AGGREGATION avg 3600000
```

## RedisBloom

Probabilistic data structures.

```redis
BF.ADD filter:emails "user@example.com"
BF.EXISTS filter:emails "user@example.com"
CF.ADD filter:users "user123"
```

## Loading Modules

```conf
loadmodule /path/to/rejson.so
loadmodule /path/to/redisearch.so
loadmodule /path/to/redistimeseries.so
loadmodule /path/to/redisbloom.so
```

## Assets
- `docker-compose-stack.yml` - Redis Stack with modules

## References
- `MODULES_GUIDE.md` - Module usage guide
