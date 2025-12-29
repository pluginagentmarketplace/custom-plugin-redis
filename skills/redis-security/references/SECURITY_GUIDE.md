# Redis Security Guide

## Security Checklist

- [ ] Strong password set (requirepass)
- [ ] ACL users configured
- [ ] Bind to localhost or specific IPs
- [ ] Protected mode enabled
- [ ] TLS configured (production)
- [ ] Dangerous commands disabled
- [ ] Firewall rules in place
- [ ] Regular security updates

## ACL Best Practices

1. Disable default user
2. Create specific users per application
3. Limit key patterns (~app:*)
4. Limit command categories (+@read)
5. Monitor ACL LOG

## Network Hardening

```conf
# Only local connections
bind 127.0.0.1

# Enable protected mode
protected-mode yes

# Timeout idle connections
timeout 300
```

## TLS Setup

1. Generate certificates
2. Configure redis.conf
3. Update client connections
4. Test with redis-cli --tls

## Monitoring

```redis
# Check connected clients
CLIENT LIST

# Monitor commands
MONITOR  # Use carefully!

# ACL audit log
ACL LOG 10
```
