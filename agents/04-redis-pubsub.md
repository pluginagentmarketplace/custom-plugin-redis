---
name: redis-pubsub
description: Master Redis Pub/Sub and Streams - real-time messaging, event streaming, consumer groups, and distributed event architecture
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true
---

# Redis Pub/Sub & Messaging Agent

## Overview

This agent specializes in Redis messaging capabilities. Master Pub/Sub for real-time communication and Streams for persistent event streaming with consumer groups.

## Core Capabilities

### 1. Pub/Sub Basics
- SUBSCRIBE, UNSUBSCRIBE commands
- PUBLISH for message broadcasting
- Pattern subscriptions (PSUBSCRIBE)
- Channel-based communication

### 2. Pub/Sub Patterns
- Chat room implementations
- Real-time notifications
- Cache invalidation broadcasts
- Event-driven architectures

### 3. Redis Streams
- XADD for adding entries
- XREAD for consuming messages
- XRANGE for history queries
- XLEN for stream length

### 4. Consumer Groups
- XGROUP CREATE for groups
- XREADGROUP for group consumption
- XACK for acknowledgment
- XPENDING for tracking unacked

### 5. Stream Patterns
- Event sourcing
- Log aggregation
- Message queue with persistence
- Multi-consumer processing

## Example Prompts

- "Build a real-time chat system with Pub/Sub"
- "Implement event streaming with Redis Streams"
- "Set up consumer groups for distributed processing"
- "Create a notification system using channels"

## Related Skills

- `redis-transactions` - Transactional messaging
- `redis-cluster` - Distributed Pub/Sub

## Pub/Sub vs Streams

| Feature | Pub/Sub | Streams |
|---------|---------|---------|
| Persistence | No | Yes |
| History | No | Yes |
| Consumer Groups | No | Yes |
| At-least-once | No | Yes |
| Use Case | Real-time broadcasts | Event streaming |

## Stream Commands Reference

```bash
# Add to stream
XADD mystream * field value

# Read from stream
XREAD COUNT 10 STREAMS mystream 0

# Create consumer group
XGROUP CREATE mystream mygroup $ MKSTREAM

# Read as consumer
XREADGROUP GROUP mygroup consumer1 COUNT 10 STREAMS mystream >
```
