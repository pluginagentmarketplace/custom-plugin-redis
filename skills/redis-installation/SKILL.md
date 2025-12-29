---
name: redis-installation
description: Complete Redis installation guide for all platforms - Linux, macOS, Docker, and cloud deployments with configuration templates
sasmp_version: "1.3.0"
bonded_agent: redis-fundamentals
bond_type: PRIMARY_BOND
---

# Redis Installation Skill

## Overview

This skill provides comprehensive Redis installation guidance for all major platforms with production-ready configuration templates.

## Supported Platforms

### Linux (Ubuntu/Debian)
```bash
# Update and install
sudo apt update
sudo apt install redis-server

# Start and enable
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify
redis-cli ping  # Returns PONG
```

### Linux (RHEL/CentOS)
```bash
# Install EPEL and Redis
sudo yum install epel-release
sudo yum install redis

# Start and enable
sudo systemctl start redis
sudo systemctl enable redis
```

### macOS (Homebrew)
```bash
# Install
brew install redis

# Start as service
brew services start redis

# Or run manually
redis-server /usr/local/etc/redis.conf
```

### Docker
```bash
# Simple run
docker run -d --name redis -p 6379:6379 redis:7-alpine

# With persistence
docker run -d --name redis \
  -p 6379:6379 \
  -v redis-data:/data \
  redis:7-alpine redis-server --appendonly yes

# With custom config
docker run -d --name redis \
  -p 6379:6379 \
  -v $(pwd)/redis.conf:/usr/local/etc/redis/redis.conf \
  redis:7-alpine redis-server /usr/local/etc/redis/redis.conf
```

## Verification Commands

```bash
# Test connection
redis-cli ping

# Check version
redis-cli INFO server | grep redis_version

# Test basic operations
redis-cli SET test "hello"
redis-cli GET test
redis-cli DEL test
```

## Assets

- `docker-compose.yml` - Production Docker setup
- `redis.conf` - Optimized configuration template

## Scripts

- `install-redis.sh` - Cross-platform installation script
- `verify-installation.sh` - Health check script

## References

- `INSTALLATION_GUIDE.md` - Detailed installation steps
- `TROUBLESHOOTING.md` - Common issues and solutions
