---
name: redis-security
description: Master Redis security - authentication, ACL system, TLS encryption, network security, and security hardening best practices
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
    security_level:
      type: string
      enum: [basic, standard, hardened, compliance]
    compliance_requirements:
      type: array
      items:
        type: string
        enum: [pci_dss, hipaa, sox, gdpr]
    network_exposure:
      type: string
      enum: [localhost, private_network, public]

output_schema:
  type: object
  properties:
    security_config:
      type: object
    acl_rules:
      type: array
    tls_config:
      type: object
    audit_checklist:
      type: array
    warnings:
      type: array

# Error Handling
error_handling:
  retry_on:
    - connection_reset
  max_retries: 2
  backoff_strategy: exponential
  backoff_base_ms: 1000
  security_errors:
    NOAUTH:
      description: Authentication required
      recovery: Provide AUTH credentials
    NOPERM:
      description: No permission for command
      recovery: Check ACL rules

# Token Optimization
token_config:
  max_input_tokens: 4000
  max_output_tokens: 8000
  streaming: true

# Dependencies
requires:
  skills: [redis-security, redis-production]
  tools: [Bash, Read, Write]
---

# Redis Security Agent

## Overview

Production-grade agent for Redis security hardening. Expert guidance on authentication, Access Control Lists (ACL), TLS encryption, network security, and compliance requirements.

## Security Maturity Levels

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SECURITY LEVEL MATRIX                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Level 1: Basic (Development)                                       │
│  ├── Password authentication                                        │
│  └── Localhost binding                                              │
│                                                                     │
│  Level 2: Standard (Internal Production)                            │
│  ├── Strong password                                                │
│  ├── ACL with role-based access                                     │
│  ├── Private network only                                           │
│  └── Dangerous command disabled                                     │
│                                                                     │
│  Level 3: Hardened (External/Sensitive)                             │
│  ├── TLS encryption                                                 │
│  ├── Certificate-based auth                                         │
│  ├── Audit logging                                                  │
│  └── Key rotation policy                                            │
│                                                                     │
│  Level 4: Compliance (PCI-DSS, HIPAA)                               │
│  ├── All of Level 3                                                 │
│  ├── Encryption at rest                                             │
│  ├── Regular security scans                                         │
│  └── Documented procedures                                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 1. Authentication

### Password Authentication (Legacy)
```bash
# redis.conf
requirepass "your-strong-password-here-min-32-chars"

# Connect with auth
redis-cli -a "your-password"
redis-cli AUTH "your-password"

# Check auth status
redis-cli PING  # Returns PONG if authenticated
```

### ACL System (Redis 6.0+)
```bash
# Default admin user
ACL SETUSER default on >password ~* &* +@all

# Create application user (limited)
ACL SETUSER appuser on >app-secret ~app:* +@read +@write -@dangerous

# Create read-only user
ACL SETUSER readonly on >readonly-secret ~* +@read -@write

# Create admin user
ACL SETUSER admin on >admin-secret ~* &* +@all
```

### ACL Rule Syntax
```bash
ACL SETUSER <username>
  [on|off]                    # Enable/disable user
  [>password]                 # Add password
  [#hash]                     # Add password hash
  [~pattern]                  # Key pattern access
  [&channel]                  # Pub/Sub channel access
  [+command|-command]         # Allow/deny command
  [+@category|-@category]     # Allow/deny command category
```

### ACL Categories
| Category | Commands | Typical Use |
|----------|----------|-------------|
| @read | GET, MGET, HGET, etc. | Read-only apps |
| @write | SET, DEL, HSET, etc. | Read-write apps |
| @admin | CONFIG, DEBUG, etc. | Administrators |
| @dangerous | KEYS, FLUSHALL, etc. | Never for apps |
| @slow | O(N) commands | Avoid in prod |
| @pubsub | SUBSCRIBE, PUBLISH | Messaging apps |

### ACL Best Practices
```bash
# /etc/redis/users.acl

# Admin (full access, specific IP recommended)
user admin on >$(ADMIN_PASSWORD) ~* &* +@all

# Application (specific keys, no dangerous commands)
user appuser on >$(APP_PASSWORD) ~app:* ~cache:* +@read +@write -@dangerous -KEYS -FLUSHALL -FLUSHDB -DEBUG

# Monitoring (read-only INFO and PING)
user monitor on >$(MONITOR_PASSWORD) ~* +INFO +PING +CLIENT|ID +SLOWLOG|GET

# Replication (for replicas)
user replication on >$(REPL_PASSWORD) +PSYNC +REPLCONF +PING
```

## 2. TLS Encryption

### Certificate Generation
```bash
# Generate CA
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt \
  -subj "/CN=Redis CA"

# Generate server certificate
openssl genrsa -out redis.key 2048
openssl req -new -key redis.key -out redis.csr \
  -subj "/CN=redis-server"
openssl x509 -req -in redis.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out redis.crt -days 365 -sha256

# Generate client certificate (optional)
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr \
  -subj "/CN=redis-client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365 -sha256
```

### TLS Configuration
```bash
# redis.conf
port 0                              # Disable non-TLS
tls-port 6379                       # TLS port
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file /etc/redis/tls/redis.key
tls-ca-cert-file /etc/redis/tls/ca.crt

# Require client certificates (optional, high security)
tls-auth-clients yes

# Cipher suites (TLS 1.2+)
tls-protocols "TLSv1.2 TLSv1.3"
tls-ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256

# For replication
tls-replication yes
tls-cluster yes
```

### TLS Client Connection
```bash
# CLI with TLS
redis-cli --tls \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  --cacert /path/to/ca.crt \
  -h redis-server -p 6379

# Verify TLS
redis-cli --tls --cacert ca.crt INFO server | grep tcp_port
```

## 3. Network Security

### Binding & Exposure
```bash
# redis.conf

# Localhost only (development)
bind 127.0.0.1 -::1

# Private network
bind 10.0.0.5 127.0.0.1

# All interfaces (requires other protections!)
bind 0.0.0.0

# Protected mode (rejects external without auth)
protected-mode yes
```

### Firewall Rules
```bash
# iptables - Allow only app servers
iptables -A INPUT -p tcp --dport 6379 -s 10.0.1.0/24 -j ACCEPT
iptables -A INPUT -p tcp --dport 6379 -j DROP

# UFW
ufw allow from 10.0.1.0/24 to any port 6379

# Security group (AWS)
# Inbound: TCP 6379 from app-server-sg
```

### Disable Dangerous Commands
```bash
# redis.conf - Rename dangerous commands
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
rename-command CONFIG "CONFIG_b840fc02d524045429"
rename-command SHUTDOWN "SHUTDOWN_b840fc02d524045429"
rename-command KEYS ""

# Or use ACL (preferred in Redis 6.0+)
ACL SETUSER default -FLUSHALL -FLUSHDB -DEBUG -KEYS
```

## 4. Security Hardening Checklist

```markdown
## Network Layer
□ Bind to specific IP (not 0.0.0.0)
□ Enable protected-mode
□ Configure firewall rules
□ Use private network/VPC
□ Disable Redis port on public interfaces

## Authentication
□ Strong password (32+ chars, random)
□ Use ACL system (Redis 6.0+)
□ Separate users per application
□ No default user with full access
□ Regular password rotation

## Encryption
□ TLS enabled for client connections
□ TLS for replication traffic
□ TLS for cluster bus (if applicable)
□ Strong cipher suites only
□ Regular certificate rotation

## Command Security
□ Dangerous commands disabled/renamed
□ KEYS command disabled
□ DEBUG commands disabled
□ CONFIG restricted to admins

## Monitoring
□ Failed auth attempt alerts
□ Connection spike detection
□ Command audit logging
□ Anomaly detection

## Compliance
□ Encryption at rest (disk-level)
□ Regular security assessments
□ Documented access procedures
□ Incident response plan
```

## Related Skills

- `redis-security` - Security patterns (PRIMARY_BOND)
- `redis-production` - Production hardening

---

## Troubleshooting Guide

### Common Issues & Solutions

#### 1. NOAUTH Error
```
NOAUTH Authentication required
```

**Fix:**
```bash
# Provide password
redis-cli -a "your-password"

# Or authenticate after connect
redis-cli
AUTH your-password
```

#### 2. NOPERM Error
```
NOPERM this user has no permissions to run the 'config' command
```

**Diagnosis:**
```bash
# Check current user
redis-cli ACL WHOAMI

# Check user permissions
redis-cli ACL GETUSER username
```

**Fix:**
```bash
# Grant permission (as admin)
redis-cli ACL SETUSER username +CONFIG
```

#### 3. TLS Handshake Failed
```
Error: Connection reset by peer
```

**Diagnosis:**
```bash
# Test TLS manually
openssl s_client -connect redis-server:6379 -CAfile ca.crt
```

**Causes & Fixes:**
| Cause | Fix |
|-------|-----|
| Wrong CA | Use correct ca.crt |
| Expired cert | Regenerate certificates |
| Protocol mismatch | Match tls-protocols |
| Missing client cert | Provide cert if required |

#### 4. Protected Mode Blocking
```
DENIED Redis is running in protected mode
```

**Explanation:** Redis blocks external connections without auth

**Fixes:**
```bash
# Option 1: Set password
redis-cli CONFIG SET requirepass "your-password"

# Option 2: Disable protected mode (NOT recommended)
redis-cli CONFIG SET protected-mode no

# Option 3: Bind to specific IP
redis-cli CONFIG SET bind "10.0.0.5"
```

### Security Audit Script
```bash
#!/bin/bash
# redis-security-audit.sh

REDIS_CLI="redis-cli -a ${REDIS_PASSWORD}"

echo "=== Redis Security Audit ==="

# Check auth
echo -n "Authentication required: "
$REDIS_CLI PING 2>&1 | grep -q "NOAUTH" && echo "YES ✓" || echo "NO ✗"

# Check protected mode
echo -n "Protected mode: "
$REDIS_CLI CONFIG GET protected-mode | grep -q "yes" && echo "YES ✓" || echo "NO ✗"

# Check bind address
echo -n "Bind address: "
$REDIS_CLI CONFIG GET bind

# Check dangerous commands
echo -n "KEYS command: "
$REDIS_CLI KEYS "*" 2>&1 | grep -q "NOPERM\|unknown" && echo "DISABLED ✓" || echo "ENABLED ✗"

echo -n "FLUSHALL command: "
$REDIS_CLI FLUSHALL 2>&1 | grep -q "NOPERM\|unknown" && echo "DISABLED ✓" || echo "ENABLED ✗"

# Check TLS
echo -n "TLS port: "
$REDIS_CLI CONFIG GET tls-port
```

### Debug Checklist

```markdown
□ Password/ACL configured correctly?
□ User exists and enabled (ACL LIST)?
□ Key patterns match access rules?
□ Command in allowed category?
□ TLS certificates valid and not expired?
□ Network path allows connection?
□ Firewall rules permit traffic?
□ Protected mode considerations?
```

---

## Error Codes Reference

| Code | Name | Description | Recovery |
|------|------|-------------|----------|
| E601 | NOAUTH | Auth required | Provide AUTH |
| E602 | NOPERM | No permission | Check/update ACL |
| E603 | WRONGPASS | Bad password | Correct password |
| E604 | TLS_HANDSHAKE | TLS failure | Check certs |
| E605 | PROTECTED | Protected mode | Set auth or bind |

---

## Production Security Config

```bash
# /etc/redis/redis.conf - Hardened Configuration

# === Network Security ===
bind 10.0.0.5 127.0.0.1
port 0
tls-port 6379
protected-mode yes

# === TLS ===
tls-cert-file /etc/redis/tls/redis.crt
tls-key-file /etc/redis/tls/redis.key
tls-ca-cert-file /etc/redis/tls/ca.crt
tls-auth-clients optional
tls-protocols "TLSv1.2 TLSv1.3"
tls-replication yes

# === Authentication ===
aclfile /etc/redis/users.acl

# === Dangerous Commands ===
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
rename-command KEYS ""

# === Timeouts ===
timeout 300
tcp-keepalive 60

# === Limits ===
maxclients 1000
```
