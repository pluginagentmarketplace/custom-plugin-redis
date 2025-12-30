---
description: Generate optimized Redis configuration for your use case
allowed-tools: Read, Write, Bash
sasmp_version: "1.3.0"
version: "2.1.0"
last_updated: "2025-01"

# Parameters
parameters:
  use_case:
    type: string
    required: true
    enum: [cache, session, queue, analytics, production, development]
  memory:
    type: string
    required: false
    default: "1gb"
  ha:
    type: boolean
    required: false
    default: false
  tls:
    type: boolean
    required: false
    default: false
  cluster:
    type: boolean
    required: false
    default: false

# Output Options
output:
  formats:
    - redis.conf
    - docker-compose.yml
    - kubernetes
    - sentinel.conf
---

# /redis-config Command

Generate optimized Redis configuration with production-ready defaults.

## Usage

```
/redis-config [use-case] [--memory 4gb] [--ha] [--tls] [--cluster]
```

## Available Use Cases

### cache
High-performance caching with aggressive eviction.

```conf
# Cache-optimized configuration
maxmemory 4gb
maxmemory-policy allkeys-lru
maxmemory-samples 10

# No persistence (volatile cache)
save ""
appendonly no

# Performance tuning
tcp-keepalive 300
timeout 0

# Memory optimization
activerehashing yes
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
```

### session
Session storage with persistence and TTL management.

```conf
# Session-optimized configuration
maxmemory 2gb
maxmemory-policy volatile-lru

# Persistence for durability
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes

# Session-specific
timeout 0
tcp-keepalive 300

# Expire handling
notify-keyspace-events Ex
```

### queue
Message queue with reliable delivery.

```conf
# Queue-optimized configuration
maxmemory 4gb
maxmemory-policy noeviction  # Never lose messages

# Strong persistence
appendonly yes
appendfsync everysec
save 900 1
save 300 10

# Performance
tcp-keepalive 60
timeout 0
tcp-backlog 511

# Blocking operations
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

### analytics
Real-time analytics with high throughput.

```conf
# Analytics-optimized configuration
maxmemory 8gb
maxmemory-policy allkeys-lfu  # Keep frequently accessed

# Balanced persistence
appendonly yes
appendfsync everysec
save 900 1

# High throughput
tcp-backlog 511
tcp-keepalive 300

# Memory for large datasets
hash-max-listpack-entries 512
hash-max-listpack-value 64
zset-max-listpack-entries 128
```

### production
Balanced production configuration with security.

```conf
# Production configuration
maxmemory 4gb
maxmemory-policy allkeys-lru

# Security
requirepass ${REDIS_PASSWORD}
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
protected-mode yes
bind 127.0.0.1 -::1

# Persistence (hybrid)
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes
save 900 1
save 300 10
save 60 10000

# Performance
tcp-keepalive 300
tcp-backlog 511
timeout 0

# Logging
loglevel notice
logfile /var/log/redis/redis.log

# Memory optimization
lazyfree-lazy-eviction yes
lazyfree-lazy-expire yes
lazyfree-lazy-server-del yes
```

### development
Development-friendly configuration.

```conf
# Development configuration
maxmemory 256mb
maxmemory-policy allkeys-lru

# No password (dev only!)
# requirepass ""
protected-mode no
bind 0.0.0.0

# Minimal persistence
appendonly no
save ""

# Debug-friendly
loglevel debug
logfile ""
```

## Generated Files

### 1. redis.conf
Primary configuration file with optimized settings.

### 2. docker-compose.yml (if requested)

```yaml
version: '3.8'
services:
  redis:
    image: redis:7.2-alpine
    container_name: redis
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "6379:6379"
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf:ro
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - redis-network
    deploy:
      resources:
        limits:
          memory: 4G

volumes:
  redis_data:

networks:
  redis-network:
    driver: bridge
```

### 3. docker-compose-ha.yml (if --ha)

```yaml
version: '3.8'
services:
  redis-master:
    image: redis:7.2-alpine
    command: redis-server /etc/redis/redis.conf
    ports:
      - "6379:6379"
    volumes:
      - ./redis-master.conf:/etc/redis/redis.conf
      - master_data:/data

  redis-replica-1:
    image: redis:7.2-alpine
    command: redis-server /etc/redis/redis.conf
    ports:
      - "6380:6379"
    volumes:
      - ./redis-replica.conf:/etc/redis/redis.conf
    depends_on:
      - redis-master

  redis-replica-2:
    image: redis:7.2-alpine
    command: redis-server /etc/redis/redis.conf
    ports:
      - "6381:6379"
    volumes:
      - ./redis-replica.conf:/etc/redis/redis.conf
    depends_on:
      - redis-master

  sentinel-1:
    image: redis:7.2-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26379:26379"
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
    depends_on:
      - redis-master

  sentinel-2:
    image: redis:7.2-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26380:26379"
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
    depends_on:
      - redis-master

  sentinel-3:
    image: redis:7.2-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    ports:
      - "26381:26379"
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
    depends_on:
      - redis-master

volumes:
  master_data:
```

### 4. sentinel.conf (if --ha)

```conf
port 26379
sentinel monitor mymaster redis-master 6379 2
sentinel auth-pass mymaster ${REDIS_PASSWORD}
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

# Notification script
# sentinel notification-script mymaster /scripts/notify.sh

# Client reconfiguration script
# sentinel client-reconfig-script mymaster /scripts/failover.sh
```

### 5. Kubernetes Manifests (if --k8s)

```yaml
# redis-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis.conf: |
    # Generated configuration
    maxmemory 4gb
    maxmemory-policy allkeys-lru
    ...

---
# redis-statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  serviceName: redis
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    spec:
      containers:
      - name: redis
        image: redis:7.2-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: config
          mountPath: /etc/redis
        - name: data
          mountPath: /data
      volumes:
      - name: config
        configMap:
          name: redis-config
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## Configuration Matrix

| Setting | Cache | Session | Queue | Analytics | Production |
|---------|-------|---------|-------|-----------|------------|
| maxmemory-policy | allkeys-lru | volatile-lru | noeviction | allkeys-lfu | allkeys-lru |
| appendonly | no | yes | yes | yes | yes |
| appendfsync | - | everysec | everysec | everysec | everysec |
| RDB saves | no | yes | yes | yes | yes |
| requirepass | optional | yes | yes | yes | yes |
| TLS | optional | recommended | recommended | recommended | required |

## Example

```bash
/redis-config production --memory 8gb --ha --tls
```

Generates:
- `redis.conf` - Master configuration
- `redis-replica.conf` - Replica configuration
- `sentinel.conf` - Sentinel configuration
- `docker-compose-ha.yml` - HA Docker setup
- `tls/` - Certificate generation script

## Validation

After generation, validate with:

```bash
# Check syntax
redis-server redis.conf --test-memory 1024

# Verify settings
redis-cli CONFIG GET "*"
```

## Troubleshooting

### Memory Setting Invalid
```
# Error: maxmemory must be positive integer
# Fix: Use format like "4gb", "512mb"
```

### TLS Certificate Error
```
# Error: Could not load certificate
# Fix: Generate certificates first
./generate-certs.sh
```
