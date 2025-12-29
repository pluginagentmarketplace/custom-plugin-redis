# Redis Advanced Types Guide

## Bitmaps

### Memory Efficiency
- 1 bit per flag vs 1 byte for string
- 512MB can store 4 billion bits
- Perfect for boolean flags at scale

### Common Patterns
```redis
# Daily active users
SETBIT dau:2024-01-15 12345 1  # User ID as offset

# Feature flags
SETBIT features:user:123 0 1  # Feature 0 enabled
SETBIT features:user:123 1 0  # Feature 1 disabled
```

## HyperLogLog

### When to Use
- Need approximate unique counts
- Dataset too large for exact counting
- 12KB fixed memory per key

### Accuracy
- Standard error: 0.81%
- Mergeable across keys
- Cannot retrieve elements

## Streams

### vs Pub/Sub
| Feature | Streams | Pub/Sub |
|---------|---------|---------|
| Persistence | Yes | No |
| Consumer Groups | Yes | No |
| Message History | Yes | No |
| Acknowledgment | Yes | No |

### Consumer Group Pattern
1. Create stream and group
2. Multiple consumers read with XREADGROUP
3. Process and XACK
4. Handle pending (unacked) messages

## Geospatial

### Precision
- Uses geohash internally
- ~0.5% distance error at equator
- Perfect for proximity searches

### Commands
```redis
# Add locations
GEOADD stores -122.4194 37.7749 "store:sf"

# Find nearby
GEOSEARCH stores FROMMEMBER "store:sf" BYRADIUS 50 km
```
