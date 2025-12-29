---
name: redis-security
description: Master Redis security - authentication, ACL, TLS encryption, network hardening, and production security best practices
sasmp_version: "1.3.0"
bonded_agent: redis-security
bond_type: PRIMARY_BOND
---

# Redis Security Skill

## Authentication

```conf
# redis.conf
requirepass your_strong_password_here
```

```redis
AUTH password
AUTH username password  # Redis 6+
```

## Access Control Lists (ACL)

```redis
# Create user
ACL SETUSER app_user on >password ~app:* +@read +@write -@dangerous

# List users
ACL LIST

# Check permissions
ACL WHOAMI
ACL CAT

# Audit log
ACL LOG [count]
```

## TLS Configuration

```conf
# redis.conf
tls-port 6379
port 0  # Disable non-TLS

tls-cert-file /path/to/redis.crt
tls-key-file /path/to/redis.key
tls-ca-cert-file /path/to/ca.crt

tls-auth-clients yes
```

## Network Security

```conf
bind 127.0.0.1 -::1
protected-mode yes
```

## Command Renaming

```conf
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
rename-command CONFIG "CONFIG_b840fc02"
```

## Assets
- `acl-users.conf` - ACL user definitions
- `security-checklist.md` - Security audit

## References
- `SECURITY_GUIDE.md` - Complete security guide
