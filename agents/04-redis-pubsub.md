---
name: redis-pubsub
description: Master Redis Pub/Sub - messaging patterns, Streams with consumer groups, event-driven architecture, and real-time data streaming
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
skills:
  - redis-security
  - redis-persistence
  - redis-strings
  - redis-replication
  - redis-cluster
  - redis-performance
  - redis-hashes-sorted-sets
  - redis-lists-sets
  - redis-installation
  - redis-modules
  - redis-transactions
  - redis-advanced-types

triggers:
  - "redis redis"
  - "redis"
  - "cache"
# Production Configuration
version: "2.1.0"
redis_versions: ["6.2", "7.0", "7.2", "7.4"]
last_updated: "2025-01"

# Input/Output Schema
input_schema:
  type: object
  properties:
    messaging_type:
      type: string
      enum: [pubsub, streams, hybrid]
    delivery_guarantee:
      type: string
      enum: [at_most_once, at_least_once, exactly_once]
    use_case:
      type: string
      enum: [notifications, event_sourcing, task_queue, real_time_feed, chat]

output_schema:
  type: object
  properties:
    recommended_approach:
      type: string
    architecture:
      type: object
    commands:
      type: array
    consumer_group_config:
      type: object

# Error Handling
error_handling:
  retry_on:
    - connection_lost
    - timeout
    - NOGROUP
  max_retries: 5
  backoff_strategy: exponential
  backoff_base_ms: 1000
  stream_errors:
    NOGROUP:
      description: Consumer group doesn't exist
      recovery: Create group with XGROUP CREATE
    BUSYGROUP:
      description: Consumer group already exists
      recovery: Use MKSTREAM option or ignore

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-transactions, redis-cluster]
  tools: [Bash, Read]
---

# Redis Pub/Sub & Streams Agent

## Overview

Production-grade agent for Redis messaging systems. Master Pub/Sub for fire-and-forget messaging and Streams for persistent, exactly-once message processing with consumer groups.

## Messaging System Selection

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MESSAGING DECISION TREE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Do you need message persistence?                                   │
│  │                                                                  │
│  ├── NO ────────────────────────────────> PUB/SUB                   │
│  │   ├── Real-time notifications                                    │
│  │   ├── Chat messages                                              │
│  │   └── Live updates                                               │
│  │                                                                  │
│  └── YES ───────────────────────────────> STREAMS                   │
│      │                                                              │
│      ├── Need consumer groups?                                      │
│      │   ├── YES ─────> STREAMS + XREADGROUP                        │
│      │   └── NO ──────> STREAMS + XREAD                             │
│      │                                                              │
│      └── Need exactly-once processing?                              │
│          └── YES ─────> STREAMS + XACK + Idempotency                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Feature Comparison

| Feature | Pub/Sub | Streams |
|---------|---------|---------|
| Message Persistence | ❌ | ✅ |
| Consumer Groups | ❌ | ✅ |
| Message Replay | ❌ | ✅ |
| At-least-once | ❌ | ✅ |
| Blocking reads | ❌ | ✅ |
| Pattern subscriptions | ✅ | ❌ |
| Cluster support | ⚠️ Limited | ✅ Full |
| Memory efficiency | ✅ Higher | Medium |

## Pub/Sub Patterns

### Basic Pub/Sub
```bash
# Subscriber (run first)
redis-cli SUBSCRIBE channel:news

# Publisher
redis-cli PUBLISH channel:news "Breaking news!"

# Pattern subscription
redis-cli PSUBSCRIBE channel:*
redis-cli PSUBSCRIBE user:*:notifications
```

### Pub/Sub Commands
```bash
# Channel management
PUBSUB CHANNELS               # List active channels
PUBSUB NUMSUB channel:news    # Subscriber count
PUBSUB NUMPAT                 # Pattern subscription count

# Subscription
SUBSCRIBE ch1 ch2 ch3         # Multiple channels
UNSUBSCRIBE ch1               # Leave channel
PSUBSCRIBE news:*             # Pattern match
PUNSUBSCRIBE news:*           # Leave pattern
```

### Pub/Sub Best Practices

| Concern | Solution |
|---------|----------|
| No persistence | Use Streams if messages must survive restarts |
| Slow subscribers | Messages dropped if buffer fills |
| No ACK | Implement application-level confirmation |
| Cluster sharding | All nodes receive, app filters |

## Redis Streams

### Stream Basics
```bash
# Add entries (auto-generated ID)
XADD events * action "click" user_id "123" page "/home"
# Returns: 1704067200000-0

# Add with custom ID
XADD events 1704067200000-0 action "view" user_id "456"

# Read entries
XREAD COUNT 10 STREAMS events 0      # From beginning
XREAD COUNT 10 STREAMS events $      # Only new entries
XREAD BLOCK 5000 STREAMS events $    # Block 5 seconds for new
```

### Consumer Groups (Production Pattern)
```bash
# Create consumer group
XGROUP CREATE events mygroup $ MKSTREAM

# Read as consumer (blocking)
XREADGROUP GROUP mygroup consumer1 \
  COUNT 10 BLOCK 5000 STREAMS events >

# Acknowledge processed messages
XACK events mygroup 1704067200000-0

# Check pending (unacked) messages
XPENDING events mygroup

# Claim old pending messages (stale consumer recovery)
XCLAIM events mygroup consumer2 60000 1704067200000-0
# Takes messages idle > 60 seconds

# Auto-claim (Redis 6.2+)
XAUTOCLAIM events mygroup consumer2 60000 0-0 COUNT 10
```

### Stream Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONSUMER GROUP ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Producer 1 ──┐                                                     │
│  Producer 2 ──┼──> XADD ──> [Stream: events] ──┬──> Consumer 1      │
│  Producer 3 ──┘                                │    (mygroup)       │
│                                                ├──> Consumer 2      │
│                                                │    (mygroup)       │
│                                                └──> Consumer 3      │
│                                                     (mygroup)       │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────┐        │
│  │ Message Flow:                                           │        │
│  │  1. XADD → Stream                                       │        │
│  │  2. XREADGROUP → Consumer (exclusive delivery)          │        │
│  │  3. Process message                                     │        │
│  │  4. XACK → Remove from pending                          │        │
│  │  5. On failure: XCLAIM by another consumer              │        │
│  └─────────────────────────────────────────────────────────┘        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Stream Commands Reference

| Command | Purpose | Complexity |
|---------|---------|------------|
| XADD | Add entry | O(1) |
| XREAD | Read entries | O(N) |
| XREADGROUP | Consumer group read | O(M) |
| XACK | Acknowledge | O(1) |
| XPENDING | Check pending | O(N) |
| XCLAIM | Claim message | O(log N) |
| XAUTOCLAIM | Auto-claim stale | O(1) |
| XTRIM | Limit stream size | O(N) |
| XLEN | Stream length | O(1) |
| XINFO GROUPS | Group info | O(1) |

## Production Patterns

### Exactly-Once Processing
```python
def process_stream():
    while True:
        # Read with consumer group
        messages = r.xreadgroup(
            'mygroup', 'consumer1',
            {'events': '>'},
            count=10, block=5000
        )

        for stream, entries in messages:
            for msg_id, data in entries:
                try:
                    # Idempotency check
                    if r.sismember('processed', msg_id):
                        r.xack('events', 'mygroup', msg_id)
                        continue

                    # Process message
                    process(data)

                    # Mark as processed (atomic)
                    pipe = r.pipeline()
                    pipe.sadd('processed', msg_id)
                    pipe.xack('events', 'mygroup', msg_id)
                    pipe.execute()

                except Exception as e:
                    # Message stays pending, will be retried
                    log.error(f"Failed: {msg_id}", e)
```

### Stream Trimming Strategies
```bash
# By max length (approximate)
XADD events MAXLEN ~ 10000 * field value

# By min ID (exact)
XTRIM events MINID = 1704067200000-0

# Capped + LIMIT (Redis 6.2+)
XTRIM events MAXLEN ~ 10000 LIMIT 100
```

## Related Skills

- `redis-transactions` - Atomic operations
- `redis-cluster` - Distributed streams

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. NOGROUP Error
```
NOGROUP No such key 'mystream' or consumer group 'mygroup'
```

**Fix:**
```bash
# Create stream + group
XGROUP CREATE mystream mygroup $ MKSTREAM

# Or create on existing stream
XGROUP CREATE mystream mygroup 0
```

#### 2. Messages Not Delivered
**Diagnosis:**
```bash
# Check pending entries
XPENDING events mygroup

# Detailed pending info
XPENDING events mygroup - + 10 consumer1
```

**Causes & Fixes:**
| Cause | Fix |
|-------|-----|
| Consumer crashed | XCLAIM or XAUTOCLAIM |
| No XACK sent | Add XACK after processing |
| Consumer blocked | Check consumer health |

#### 3. Memory Growth (Unbounded Stream)
```bash
# Check stream length
XLEN events

# Memory used
MEMORY USAGE events
```

**Fix:**
```bash
# Cap at creation
XADD events MAXLEN ~ 100000 * field value

# Manual trim
XTRIM events MAXLEN ~ 100000
```

#### 4. Pub/Sub Messages Lost
**Causes:**
- No subscribers when published
- Subscriber too slow (buffer overflow)
- Connection dropped

**Mitigation:**
```bash
# Check subscriber count before publish
PUBSUB NUMSUB channel:critical
# If 0, queue in Stream instead
```

### Debug Checklist

```markdown
□ Consumer group exists?
□ Using correct stream/group names?
□ XACK sent after processing?
□ Handling pending messages on restart?
□ Stream size capped with MAXLEN?
□ Consumer claiming stale messages?
□ Idempotency for exactly-once?
```

### Log Patterns

| Log Pattern | Meaning | Action |
|-------------|---------|--------|
| Pending entries growing | Consumers failing | Check consumer health |
| Memory increasing | Unbounded stream | Add MAXLEN |
| Zero deliveries | No new messages | Normal if idle |
| High claim rate | Consumer failures | Investigate crashes |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E301 | NOGROUP | Group doesn't exist | XGROUP CREATE |
| E302 | BUSYGROUP | Group already exists | Ignore or use different name |
| E303 | XREAD_TIMEOUT | No messages in timeout | Normal, retry |
| E304 | STREAM_FULL | Reached MAXLEN | Trim or increase limit |
| E305 | CONSUMER_STALE | Consumer not responding | XAUTOCLAIM |

---

## Performance Tuning

### Consumer Group Sizing

| Throughput | Consumers | COUNT | BLOCK |
|------------|-----------|-------|-------|
| Low (<1K/s) | 1-2 | 100 | 5000ms |
| Medium (<10K/s) | 3-5 | 500 | 2000ms |
| High (<100K/s) | 10+ | 1000 | 1000ms |

### Stream vs Pub/Sub Performance

| Metric | Pub/Sub | Streams |
|--------|---------|---------|
| Publish latency | ~0.1ms | ~0.2ms |
| Memory per message | 0 (transient) | ~100 bytes |
| Max throughput | 1M+/s | 500K/s |
| Consumer scaling | Broadcast | Partitioned |
