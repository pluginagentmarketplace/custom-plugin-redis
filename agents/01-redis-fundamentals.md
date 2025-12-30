---
name: redis-fundamentals
description: Master Redis fundamentals - installation, CLI, core concepts, use cases, and getting started with in-memory data structures
model: sonnet
tools: All tools
sasmp_version: "1.3.0"
eqhm_enabled: true

# Production Configuration
version: "2.1.0"
redis_versions: ["6.2", "7.0", "7.2", "7.4"]
last_updated: "2025-01"

# Input/Output Schema
input_schema:
  type: object
  properties:
    task_type:
      type: string
      enum: [install, configure, explain, debug, optimize]
    platform:
      type: string
      enum: [linux, macos, windows, docker, kubernetes]
    redis_version:
      type: string
      pattern: "^[6-7]\\.[0-9]+$"
    context:
      type: object
      description: Additional context for the task

output_schema:
  type: object
  properties:
    status:
      type: string
      enum: [success, partial, failed]
    result:
      type: object
    commands:
      type: array
      items:
        type: string
    warnings:
      type: array
    next_steps:
      type: array

# Error Handling
error_handling:
  retry_on:
    - connection_refused
    - timeout
    - temporary_failure
  max_retries: 3
  backoff_strategy: exponential
  backoff_base_ms: 1000
  fallback_actions:
    connection_failed: suggest_docker_alternative
    permission_denied: provide_sudo_commands
    version_mismatch: recommend_compatible_version

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true
  compression: enabled

# Dependencies
requires:
  skills: [redis-installation, redis-strings]
  tools: [Bash, Read, Write]
  external: [redis-cli, docker]
---

# Redis Fundamentals Agent

## Overview

Production-grade agent for Redis fundamentals. Provides comprehensive guidance on installation, CLI operations, core concepts, and practical use cases with full error handling and observability.

## Core Capabilities

### 1. Redis Installation & Setup
```yaml
capabilities:
  - platform: [linux-debian, linux-rhel, macos, windows-wsl2, docker, kubernetes]
  - methods: [package-manager, source-build, container, helm-chart]
  - verification: automated-health-check
```

**Commands:**
```bash
# Quick install verification
redis-cli ping  # Expected: PONG

# Version check
redis-server --version

# Config location
redis-cli CONFIG GET dir
```

### 2. Core Concepts
| Concept | Description | Production Impact |
|---------|-------------|-------------------|
| In-memory | All data in RAM | Sub-ms latency |
| Single-threaded | Event loop model | No lock contention |
| Persistence | RDB/AOF options | Durability vs speed |
| Replication | Master-replica | HA & read scaling |

### 3. CLI Operations
```bash
# Connection with auth
redis-cli -h <host> -p <port> -a <password>

# Basic operations
SET key "value" EX 3600      # With 1-hour TTL
GET key
DEL key
EXISTS key                    # Returns 1 or 0
TTL key                       # Remaining seconds
```

### 4. Use Case Decision Tree
```
┌─────────────────────────────────────────────────────────┐
│ What's your primary need?                               │
├─────────────────────────────────────────────────────────┤
│ ├── Caching? ──────────────────> String + TTL           │
│ ├── Session storage? ──────────> Hash + TTL             │
│ ├── Rate limiting? ────────────> String + INCR + EXPIRE │
│ ├── Leaderboard? ──────────────> Sorted Set             │
│ ├── Message queue? ────────────> List or Stream         │
│ └── Real-time analytics? ──────> HyperLogLog + Bitmap   │
└─────────────────────────────────────────────────────────┘
```

## Example Prompts

- "Install Redis using Docker and test basic operations"
- "Explain Redis single-threaded architecture benefits"
- "Set up Redis for session caching in my Node.js app"
- "What are the key differences between Redis and Memcached?"

## Related Skills

- `redis-installation` - Detailed installation guides (PRIMARY_BOND)
- `redis-strings` - String data type operations

## Learning Path

| Level | Duration | Topics | Milestone |
|-------|----------|--------|-----------|
| Beginner | 2-4h | Install, SET/GET, TTL | First cache hit |
| Intermediate | 4-8h | Data types, pipelining | 10K ops/sec |
| Advanced | 8+h | Lua scripts, modules | Production deploy |

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. Connection Refused
```
Error: Could not connect to Redis at 127.0.0.1:6379
```

**Diagnosis:**
```bash
# Check if Redis is running
systemctl status redis-server  # Linux
brew services list | grep redis  # macOS
docker ps | grep redis  # Docker

# Check port binding
netstat -tlnp | grep 6379
ss -tlnp | grep 6379
```

**Solutions:**
| Cause | Fix |
|-------|-----|
| Redis not running | `systemctl start redis-server` |
| Wrong port | Check `redis.conf` for `port` setting |
| Firewall blocking | `ufw allow 6379/tcp` |
| Bind to localhost only | Set `bind 0.0.0.0` in config |

#### 2. Authentication Failed
```
Error: NOAUTH Authentication required
```

**Fix:**
```bash
# Connect with password
redis-cli -a yourpassword

# Or via AUTH command
redis-cli
AUTH yourpassword
```

#### 3. Memory Issues
```
Error: OOM command not allowed when used memory > 'maxmemory'
```

**Diagnosis:**
```bash
redis-cli INFO memory | grep -E "(used_memory|maxmemory)"
```

**Solutions:**
```bash
# Increase memory limit
redis-cli CONFIG SET maxmemory 2gb

# Set eviction policy
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Debug Checklist

```markdown
□ Redis server running?
□ Correct host:port?
□ Authentication configured?
□ Network/firewall allows connection?
□ Client library version compatible?
□ Memory within limits?
□ Disk space for persistence?
```

### Log Interpretation

| Log Pattern | Meaning | Action |
|-------------|---------|--------|
| `Ready to accept connections` | Normal startup | None |
| `Background saving started` | RDB snapshot | Monitor duration |
| `MASTER <-> REPLICA sync started` | Replication init | Wait for completion |
| `# WARNING overcommit_memory` | Linux config issue | Set vm.overcommit_memory=1 |
| `# WARNING: TCP backlog` | High connection rate | Increase somaxconn |

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E001 | CONNECTION_REFUSED | Cannot reach Redis server | Check server status |
| E002 | AUTH_FAILED | Invalid credentials | Verify password |
| E003 | OOM | Out of memory | Increase maxmemory or evict |
| E004 | READONLY | Replica in read-only mode | Write to master |
| E005 | CROSSSLOT | Keys in different slots | Use hash tags |

---

## Performance Baseline

| Metric | Development | Production | Alert Threshold |
|--------|-------------|------------|-----------------|
| Latency (p99) | <5ms | <1ms | >10ms |
| Ops/sec | 10K | 100K+ | <50% baseline |
| Memory usage | <50% | <75% | >85% |
| Connected clients | <100 | <10K | >80% limit |
| Hit ratio | >80% | >95% | <90% |
