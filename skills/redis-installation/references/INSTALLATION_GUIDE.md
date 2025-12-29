# Redis Installation Guide

## Overview

This guide covers Redis installation for all major platforms with best practices for production deployments.

## Prerequisites

- 1GB+ RAM (recommended)
- Linux kernel 3.x+ (for Linux)
- Docker 20.x+ (for containerized deployment)
- Network access to port 6379

## Platform-Specific Installation

### Ubuntu/Debian

```bash
# Add Redis repository for latest version
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt update
sudo apt install redis

# Verify
sudo systemctl status redis-server
```

### macOS

```bash
# Using Homebrew
brew install redis

# Start service
brew services start redis

# Configuration location
/usr/local/etc/redis.conf
```

### Docker (Recommended for Development)

```bash
# Quick start
docker run -d --name redis -p 6379:6379 redis:7-alpine

# With persistence
docker run -d --name redis \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:7-alpine redis-server --appendonly yes
```

## Post-Installation Configuration

### 1. Set Password
```bash
redis-cli CONFIG SET requirepass "your_strong_password"
```

### 2. Configure Memory
```bash
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### 3. Enable Persistence
```bash
redis-cli CONFIG SET appendonly yes
redis-cli CONFIG REWRITE
```

## Verification Checklist

- [ ] Redis server is running
- [ ] redis-cli can connect
- [ ] PING returns PONG
- [ ] SET/GET operations work
- [ ] Memory limits configured
- [ ] Persistence enabled (if needed)

## Common Issues

### Cannot connect to Redis
- Check if Redis is running: `systemctl status redis`
- Check bind address in redis.conf
- Verify firewall rules

### Redis keeps crashing
- Check available memory
- Review redis.log for errors
- Verify disk space for persistence

## Security Recommendations

1. Always set a strong password
2. Bind to localhost or specific IPs
3. Use TLS for remote connections
4. Enable protected-mode
5. Create specific ACL users

## Next Steps

After installation, proceed to:
- Configure for your use case
- Set up replication (if needed)
- Configure monitoring
- Plan backup strategy
