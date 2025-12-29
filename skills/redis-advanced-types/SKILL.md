---
name: redis-advanced-types
description: Master Redis advanced data types - Bitmaps, HyperLogLog, Streams, and Geospatial indexes for specialized use cases
sasmp_version: "1.3.0"
bonded_agent: redis-data-structures
bond_type: SECONDARY_BOND
---

# Redis Advanced Types Skill

## Bitmaps

Memory-efficient bit operations for flags and counters.

```redis
SETBIT key offset value
GETBIT key offset
BITCOUNT key [start end]
BITOP AND|OR|XOR|NOT destkey key [key ...]
BITPOS key bit [start [end]]
```

### Use Case: User Activity Tracking
```redis
# User logged in on day 0, 5, 10
SETBIT user:123:logins 0 1
SETBIT user:123:logins 5 1
SETBIT user:123:logins 10 1

# Count login days
BITCOUNT user:123:logins
```

## HyperLogLog

Probabilistic cardinality estimation (0.81% error).

```redis
PFADD key element [element ...]
PFCOUNT key [key ...]
PFMERGE destkey sourcekey [sourcekey ...]
```

### Use Case: Unique Visitors
```redis
PFADD visitors:2024-01 "user:1" "user:2" "user:3"
PFCOUNT visitors:2024-01  # ~3
```

## Streams

Append-only log with consumer groups.

```redis
XADD stream * field value
XREAD COUNT 10 STREAMS stream 0
XRANGE stream - +
XGROUP CREATE stream group $ MKSTREAM
XREADGROUP GROUP group consumer STREAMS stream >
```

## Geospatial

Location-based data with distance queries.

```redis
GEOADD key longitude latitude member
GEOPOS key member
GEODIST key member1 member2 [unit]
GEOSEARCH key FROMMEMBER member BYRADIUS 10 km
```

## Assets
- `stream-consumer.py` - Stream consumer implementation

## References
- `ADVANCED_TYPES_GUIDE.md` - Complete guide
